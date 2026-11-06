# Promoting rules to SYSTEM.md

`SYSTEM.md` holds the rules for all repos. A repo `AGENTS.md` holds the rules
for one repo. Sometimes a rule starts in one repo and then must apply to all
repos. The `# SYSTEM.md` section moves that rule to `SYSTEM.md`.

## The section

Each repo `AGENTS.md` ends with this section:

```markdown
# SYSTEM.md

<!-- Rules for all repos. A periodic process moves them to SYSTEM.md. -->
```

- The heading is exactly `# SYSTEM.md`, as a level-one heading.
- The section is the last section of the file. It continues to the end of the
  file.
- Write each rule in the form that it must have in `SYSTEM.md`: a `##` heading
  and its text. The process copies the text without changes.
- Keep the section and its comment when the section is empty. The process
  finds the section by its heading.

## When to put a rule in the section

Put a rule in the section only if it passes the admission test in
`system-prompt.md`. If you are not sure, put the rule in the repo part of
`AGENTS.md`. You can move it later.

## The process

`scripts/promote.py` does the process. The `promote` workflow runs it each
Monday, and you can start it by hand from the Actions tab. `just promote`
shows what it would do, and changes nothing.

Each run reads the state of GitHub again, so the process keeps no state of its
own. It finds the repos that the repo-ci-bot App can reach, and reads the
`# SYSTEM.md` section of the root `AGENTS.md` of each repo. Each `##` block in
the section is one rule. The process identifies a rule by a hash of its text
in the source repo. Then, for each rule:

| The rule is in | The process |
| --- | --- |
| No promotion PR | Opens a promotion PR to `SYSTEM.md`, one for each source repo |
| An open promotion PR | Waits |
| A merged promotion PR | Opens a PR that removes the rule from the source repo |
| A promotion PR that was closed without a merge | Reports it as rejected |

A promotion PR adds the rules above the "Promote rules to SYSTEM.md" section
of `SYSTEM.md`. A hidden marker in the PR body records the source repo, the
commit, and the hash of each rule.

## Review a promotion PR

The promotion PR is the review step. Edit, shorten, or move a rule in the PR
before it applies to all repos. The process matches rules by their text in the
source repo, so an edit in the PR does not stop the cleanup.

To reject a rule, close the PR without a merge. The process then reports the
rule as rejected in each run. Remove it from the source repo by hand.

`SYSTEM.md` has a size limit. If a promotion PR makes `SYSTEM.md` too large,
`check-instructions` fails on the PR. Move details into `docs/` before you
merge. See `system-prompt.md`.

## Set up the App

The workflow uses the repo-ci-bot GitHub App for its token. The token expires
after one hour, and PRs that it opens start CI.

1. Give the App these repository permissions: Contents (read and write),
   Pull requests (read and write), and Metadata (read).
2. Install the App on this repo and on each repo that has an `AGENTS.md`. The
   token can reach each repo where the App is installed, so do not install it
   on other repos.
3. In this repo, set the variable `REPO_CI_BOT_CLIENT_ID` to the client ID of
   the App, and the secret `REPO_CI_BOT_PRIVATE_KEY` to its private key.
