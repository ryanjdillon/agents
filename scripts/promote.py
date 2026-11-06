#!/usr/bin/env python3
"""Move rules from the `# SYSTEM.md` section of each repo AGENTS.md into SYSTEM.md.

Each run reconciles from the state of GitHub, so it keeps no state of its own.
A rule is a `##` block in the section, identified by a hash of its source text.
For each rule:

- not in a promotion PR: open a promotion PR to SYSTEM.md in the agents repo;
- in an open promotion PR: wait;
- in a merged promotion PR: open a PR that removes it from the source repo;
- in a closed, unmerged promotion PR: it was rejected; report it.

The hash comes from the source text, so a reviewer can edit a rule in the
promotion PR and the source still matches. See docs/promotion.md.

Stdlib only, and all GitHub access goes through the `gh` CLI, so the same
script runs locally (`just promote`) and in CI with an App token.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field

SECTION_HEADING = "# SYSTEM.md"
PROMOTE_ANCHOR = "## Promote rules to SYSTEM.md"
PROMOTE_PREFIX = "promote/"
CLEANUP_PREFIX = "promote/cleanup-"
MARKER_RE = re.compile(
    r"<!-- promotion source=(?P<source>\S+) commit=(?P<commit>[0-9a-f]+) "
    r"rules=(?P<rules>[0-9a-f,]+) -->"
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")


# --- Parsing (pure) ---------------------------------------------------------


@dataclass(frozen=True)
class Section:
    """The `# SYSTEM.md` section of an AGENTS.md, split for editing."""

    before: str  # everything up to and including the heading line
    preamble: str  # comments and blank lines before the first rule
    rules: tuple[str, ...]  # one `##` block each, without edge blank lines


def _outside_fences(lines: list[str]) -> list[bool]:
    flags, in_fence = [], False
    for line in lines:
        if FENCE_RE.match(line):
            in_fence = not in_fence
            flags.append(False)
            continue
        flags.append(not in_fence)
    return flags


def parse_section(text: str) -> Section | None:
    """Return the section, or None when the file has no `# SYSTEM.md` heading.

    The section is the last level-one heading and runs to the end of the file,
    the same rule that check-instructions enforces.
    """
    lines = text.splitlines()
    outside = _outside_fences(lines)
    starts = [
        i
        for i, line in enumerate(lines)
        if outside[i] and line.rstrip() == SECTION_HEADING
    ]
    if not starts:
        return None
    start = starts[-1]
    body = lines[start + 1 :]
    body_outside = outside[start + 1 :]

    first_rule = next(
        (
            i
            for i, line in enumerate(body)
            if body_outside[i] and line.startswith("## ")
        ),
        len(body),
    )
    rules: list[str] = []
    current: list[str] = []
    for i, line in enumerate(body[first_rule:], first_rule):
        if body_outside[i] and line.startswith("## ") and current:
            rules.append(_trim(current))
            current = []
        current.append(line)
    if current:
        rules.append(_trim(current))

    return Section(
        before="\n".join(lines[: start + 1]),
        preamble=_trim(body[:first_rule]),
        rules=tuple(rule for rule in rules if rule),
    )


def _trim(lines: list[str]) -> str:
    stripped = [line.rstrip() for line in lines]
    while stripped and not stripped[0]:
        stripped.pop(0)
    while stripped and not stripped[-1]:
        stripped.pop()
    return "\n".join(stripped)


def rule_hash(rule: str) -> str:
    return hashlib.sha256(rule.encode("utf-8")).hexdigest()[:12]


def remove_rules(text: str, hashes: set[str]) -> str:
    """Return the AGENTS.md text without the rules whose hash is in `hashes`.

    The heading and the preamble comment stay: the process finds the section by
    its heading, and the comment tells the next writer what the section is for.
    """
    section = parse_section(text)
    if section is None:
        return text
    kept = [rule for rule in section.rules if rule_hash(rule) not in hashes]
    parts = [section.before]
    if section.preamble:
        parts.append(section.preamble)
    parts.extend(kept)
    return "\n\n".join(parts) + "\n"


def insert_rules(system_text: str, rules: list[str]) -> str:
    """Insert the rules above the promotion section of SYSTEM.md, or at the end."""
    block = "\n\n".join(rules)
    lines = system_text.splitlines()
    for i, line in enumerate(lines):
        if line.rstrip() == PROMOTE_ANCHOR:
            head = "\n".join(lines[:i]).rstrip("\n")
            tail = "\n".join(lines[i:])
            return f"{head}\n\n{block}\n\n{tail}\n"
    return f"{system_text.rstrip()}\n\n{block}\n"


def make_marker(source: str, commit: str, hashes: list[str]) -> str:
    return (
        f"<!-- promotion source={source} commit={commit} rules={','.join(hashes)} -->"
    )


# --- Planning (pure) --------------------------------------------------------


@dataclass(frozen=True)
class PromotionPR:
    number: int
    state: str  # "open", "merged", or "rejected"
    source: str
    rules: frozenset[str]


def parse_promotion_pr(pull: dict) -> PromotionPR | None:
    if not pull.get("head", {}).get("ref", "").startswith(PROMOTE_PREFIX):
        return None
    match = MARKER_RE.search(pull.get("body") or "")
    if not match:
        return None
    if pull.get("merged_at"):
        state = "merged"
    elif pull.get("state") == "open":
        state = "open"
    else:
        state = "rejected"
    return PromotionPR(
        number=pull["number"],
        state=state,
        source=match["source"],
        rules=frozenset(match["rules"].split(",")),
    )


@dataclass
class RepoPlan:
    repo: str
    new: list[str] = field(default_factory=list)
    waiting: list[str] = field(default_factory=list)
    promoted: list[str] = field(default_factory=list)
    rejected: list[str] = field(default_factory=list)
    promoted_by: set[int] = field(default_factory=set)


def plan_repo(repo: str, section: Section, prs: list[PromotionPR]) -> RepoPlan:
    """Sort each rule of one repo by the state of the promotion PRs."""
    plan = RepoPlan(repo)
    by_state: dict[str, dict[str, int]] = {"merged": {}, "open": {}, "rejected": {}}
    for pr in prs:
        if pr.source != repo:
            continue
        for rule in pr.rules:
            by_state[pr.state][rule] = pr.number
    for rule in section.rules:
        digest = rule_hash(rule)
        # Merged wins over rejected: a rule that was rejected once and then
        # promoted in a later PR is in SYSTEM.md, so it must leave the repo.
        if digest in by_state["merged"]:
            plan.promoted.append(rule)
            plan.promoted_by.add(by_state["merged"][digest])
        elif digest in by_state["open"]:
            plan.waiting.append(rule)
        elif digest in by_state["rejected"]:
            plan.rejected.append(rule)
        else:
            plan.new.append(rule)
    return plan


def rule_title(rule: str) -> str:
    return rule.splitlines()[0].removeprefix("## ").strip()


# --- GitHub I/O -------------------------------------------------------------


class GitHubError(RuntimeError):
    def __init__(self, status: int | None, message: str):
        super().__init__(message)
        self.status = status


class GitHub:
    """A thin wrapper over `gh api`. Tests replace it with a spec-bound mock."""

    def api(self, method: str, path: str, body: dict | None = None) -> object:
        cmd = [
            "gh",
            "api",
            "-X",
            method,
            path,
            "-H",
            "Accept: application/vnd.github+json",
        ]
        if body is not None:
            cmd += ["--input", "-"]
        result = subprocess.run(
            cmd,
            input=json.dumps(body) if body is not None else None,
            capture_output=True,
            text=True,
            check=False,  # the return code is examined below, with the HTTP status
        )
        if result.returncode != 0:
            status = re.search(r"\(HTTP (\d{3})\)", result.stderr)
            raise GitHubError(
                int(status[1]) if status else None,
                f"{method} {path}: {result.stderr.strip()}",
            )
        return json.loads(result.stdout) if result.stdout.strip() else None

    def paginate(self, path: str, key: str | None = None) -> list:
        items: list = []
        page = 1
        while True:
            sep = "&" if "?" in path else "?"
            data = self.api("GET", f"{path}{sep}per_page=100&page={page}")
            batch = data[key] if key else data
            items.extend(batch)
            if len(batch) < 100:
                return items
            page += 1

    def repos(self, owner: str) -> list[str]:
        """List the repos to scan: the App installation's repos, else the owner's.

        An App token lists only the repos the App can write to, which are the
        only repos where the process can open a cleanup PR.
        """
        try:
            repos = self.paginate("installation/repositories", key="repositories")
        except GitHubError:
            # A personal token: `users/<owner>/repos` lists only public repos,
            # so use the private-aware list when the token belongs to the owner.
            if self.api("GET", "user")["login"] == owner:
                repos = self.paginate("user/repos?affiliation=owner")
            else:
                repos = self.paginate(f"users/{owner}/repos?type=owner")
        return sorted(
            r["full_name"]
            for r in repos
            if r["owner"]["login"] == owner
            and not r.get("archived")
            and not r.get("fork")
        )

    def read_file(self, repo: str, path: str) -> tuple[str, str, str] | None:
        """Return (text, blob sha, default branch), or None if the file is absent."""
        branch = self.api("GET", f"repos/{repo}")["default_branch"]
        try:
            data = self.api("GET", f"repos/{repo}/contents/{path}?ref={branch}")
        except GitHubError as error:
            if error.status == 404:
                return None
            raise
        text = base64.b64decode(data["content"]).decode("utf-8")
        return text, data["sha"], branch

    def head_commit(self, repo: str, branch: str) -> str:
        return self.api("GET", f"repos/{repo}/commits/{branch}")["sha"]

    def open_pull_heads(self, repo: str) -> set[str]:
        return {
            p["head"]["ref"] for p in self.paginate(f"repos/{repo}/pulls?state=open")
        }

    def all_pulls(self, repo: str) -> list[dict]:
        return self.paginate(f"repos/{repo}/pulls?state=all")

    def propose(
        self,
        repo: str,
        base: str,
        branch: str,
        path: str,
        text: str,
        blob_sha: str,
        message: str,
        title: str,
        body: str,
    ) -> str:
        """Commit one file to a new branch and open a PR. Return the PR URL."""
        self.api(
            "POST",
            f"repos/{repo}/git/refs",
            {"ref": f"refs/heads/{branch}", "sha": self.head_commit(repo, base)},
        )
        self.api(
            "PUT",
            f"repos/{repo}/contents/{path}",
            {
                "message": message,
                "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
                "sha": blob_sha,
                "branch": branch,
            },
        )
        pull = self.api(
            "POST",
            f"repos/{repo}/pulls",
            {"title": title, "head": branch, "base": base, "body": body},
        )
        return pull["html_url"]


# --- Run --------------------------------------------------------------------


def promotion_body(repo: str, commit: str, rules: list[str]) -> str:
    titles = "\n".join(f"- {rule_title(rule)}" for rule in rules)
    hashes = [rule_hash(rule) for rule in rules]
    return f"""These rules are in the `# SYSTEM.md` section of \
[`{repo}` AGENTS.md](https://github.com/{repo}/blob/{commit}/AGENTS.md):

{titles}

Edit or move the rules here as necessary. When this PR merges, the next run \
opens a PR that removes them from `{repo}`. If you close this PR without a \
merge, the rules are rejected: the next run reports them, and you remove them \
from `{repo}` by hand.

{make_marker(repo, commit, hashes)}
"""


def cleanup_body(agents_repo: str, rules: list[str], numbers: set[int]) -> str:
    titles = "\n".join(f"- {rule_title(rule)}" for rule in rules)
    links = ", ".join(f"{agents_repo}#{n}" for n in sorted(numbers))
    return f"""These rules are now in `SYSTEM.md` ({links}), so this PR removes \
them from the `# SYSTEM.md` section:

{titles}

The heading and its comment stay.
"""


def run(
    gh: GitHub, owner: str, agents_repo: str, only: list[str], dry_run: bool
) -> tuple[str, bool]:
    """Reconcile each repo. Return the report, and whether every repo succeeded."""
    pulls = gh.all_pulls(agents_repo)
    prs = [pr for p in pulls if (pr := parse_promotion_pr(p))]
    agents_heads = {p["head"]["ref"] for p in pulls}
    report: list[str] = []
    ok = True
    for repo in only or gh.repos(owner):
        # One repo's API error must not stop the others; report it and go on.
        try:
            report += reconcile(gh, repo, agents_repo, prs, agents_heads, dry_run)
        except GitHubError as error:
            report += [f"## {repo}", f"- error: {error}"]
            ok = False
    return ("\n".join(report) if report else "No rules to promote."), ok


def reconcile(
    gh: GitHub,
    repo: str,
    agents_repo: str,
    prs: list[PromotionPR],
    agents_heads: set[str],
    dry_run: bool,
) -> list[str]:
    report: list[str] = []
    found = gh.read_file(repo, "AGENTS.md")
    if found is None:
        return report
    text, blob_sha, branch = found
    section = parse_section(text)
    if section is None or not section.rules:
        return report
    plan = plan_repo(repo, section, prs)
    commit = gh.head_commit(repo, branch)
    report.append(f"## {repo}")
    for label, rules in (
        ("waiting for review", plan.waiting),
        ("rejected; remove by hand", plan.rejected),
    ):
        report += [f"- {label}: {rule_title(rule)}" for rule in rules]

    if plan.promoted:
        heads = gh.open_pull_heads(repo)
        if any(head.startswith(CLEANUP_PREFIX) for head in heads):
            report.append("- cleanup PR already open")
        elif dry_run:
            report.append(f"- would remove {len(plan.promoted)} promoted rule(s)")
        else:
            url = gh.propose(
                repo,
                branch,
                f"{CLEANUP_PREFIX}{commit[:7]}",
                "AGENTS.md",
                remove_rules(text, {rule_hash(r) for r in plan.promoted}),
                blob_sha,
                "docs: remove rules that moved to SYSTEM.md",
                "docs: remove rules that moved to SYSTEM.md",
                cleanup_body(agents_repo, plan.promoted, plan.promoted_by),
            )
            report.append(f"- opened cleanup PR {url}")

    if plan.new:
        name = repo.split("/")[1]
        head = f"{PROMOTE_PREFIX}{name}-{commit[:7]}"
        if head in agents_heads:
            report.append(f"- branch {head} already used; skipped")
        elif dry_run:
            report += [f"- would promote: {rule_title(rule)}" for rule in plan.new]
        else:
            system = gh.read_file(agents_repo, "SYSTEM.md")
            if system is None:
                raise GitHubError(404, f"{agents_repo} has no SYSTEM.md")
            system_text, system_sha, system_branch = system
            url = gh.propose(
                agents_repo,
                system_branch,
                head,
                "SYSTEM.md",
                insert_rules(system_text, plan.new),
                system_sha,
                f"docs: promote rules from {name} to SYSTEM.md",
                f"docs: promote rules from {name} to SYSTEM.md",
                promotion_body(repo, commit, plan.new),
            )
            report.append(f"- opened promotion PR {url}")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--owner", default="ryanjdillon")
    parser.add_argument("--agents-repo", default="ryanjdillon/agents")
    parser.add_argument(
        "--repo", action="append", default=[], help="scan only this repo (repeatable)"
    )
    parser.add_argument("--dry-run", action="store_true", help="report; change nothing")
    args = parser.parse_args(argv)

    report, ok = run(GitHub(), args.owner, args.agents_repo, args.repo, args.dry_run)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as handle:
            handle.write(
                f"# Promotion{' (dry run)' if args.dry_run else ''}\n\n{report}\n"
            )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
