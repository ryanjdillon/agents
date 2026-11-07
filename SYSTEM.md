# Agent conventions

These rules apply to all my repos. Each repo adds its own rules in its
`AGENTS.md`. The reasons for each rule are in the `docs/` directory of
<https://github.com/ryanjdillon/agents>. Read a doc only when you need the
reason or an edge case.

## Plan on Linear

Linear is the source of truth for what is being worked on. The repo records how
the code works; Linear records why work is happening and what is left.

- **File, ship, close.** Every non-trivial change has an issue. Move it to
  In Progress when you start and close it when the change ships.
- **Tier the tracking to the size.** A one-line fix needs no issue. A change
  worth reviewing needs an issue. A body of work spanning several changes needs
  a project with a dependency graph.
- **Parents before subs.** Create the parent issue first, then decompose.
- **Close on ship, in the same turn.** An issue left open after its change ships
  makes the whole board untrustworthy. The exception is an explicit "leave it,
  I want to look first".
- **Reference the issue in the commit message** so history and Linear stay linked.
- **Do not invent issues** to look busy, and do not silently work off-issue.

See `docs/planning-on-linear.md`.

## Plan strategically before decomposing

Work descends from an objective, not from whatever is nearest to hand.

1. Start from the **initiative** — the goal in one sentence.
2. Decompose into **projects** with explicit acceptance criteria.
3. Map the **critical path to the objective** and the **path to the target
   state** independently. They are not the same path.
4. Classify every body of work as one of:
   - **strategic-critical** — on the critical path; do it now.
   - **drift-guard** — not on the path, but deferring it causes rework; do it now.
   - **target-state-deferrable** — improves the end state, costs nothing to
     defer; file it and move on.

The rule: no shortsighted shortcuts, and no gold-plating off the critical path.

See `docs/planning-strategically.md`.

## Stay on target

When a fix or a discovery spawns work that is not on the current critical path:
**file it as a Linear issue and continue.** Do not rabbit-hole, and do not
silently expand scope.

- Distinguish must-do-now (on the path, or a drift-guard) from file-for-later.
- Filing is not dropping — Linear is durable, so deferring loses nothing.
- If the new work invalidates the current plan, say so and stop; do not
  improvise a new plan mid-change.

See `docs/staying-on-target.md`.

## Protect the main context

Delegate to a sub-agent whatever produces bulk you do not need to keep: broad
searches, multi-file reads, research spikes, large tool output.

- The sub-agent returns **the conclusion**, not the raw material.
- The main thread keeps the decision and the Linear update, never the dumps.
- State the return contract in the sub-agent's prompt (what shape, what fields).
- Sub-agent context loss is harmless because Linear holds the durable record.

See `docs/subagents.md`.

## Keep modules deep

A small, narrow interface with as much depth behind it as the domain needs —
for source and docs alike. One unit per domain; one topic per doc, standing
alone rather than assembled from fragments across five files.

See `docs/module-organisation.md`.

## Keep docs honest

- **Docs alongside code, in the same commit.** A change that invalidates a doc
  updates that doc in the same commit — never as a follow-up.
- **Write back what you learn.** A non-obvious fact discovered while working
  (an invariant, a gotcha, why an approach failed) goes into the relevant doc.
- Every `docs/` tree has an index; every substantial directory has a README.

See `docs/doc-discipline.md`.

## Write in Simplified Technical English

Use ASD-STE100 Simplified Technical English (STE) for all prose that you
write: docs, READMEs, docstrings, comments, commit messages, PR descriptions,
and Linear issues.

- One topic in each sentence, 20 words or fewer (25 for descriptions).
- Active voice, simple tenses, and instructions as commands.
- One word for one meaning, and the same word each time.
- Apply this to names in code too: one term for one concept, plain words,
  and verbs for actions (`load_config`, not `config_handler`).

See `docs/simplified-technical-english.md`.

## Code and comments

- Comments explain **why**, not what. No comment narrates a change, references a
  conversation, or notes that something was removed.
- Keep comments general to the code, not to one deployment — describe what the
  code does, not the author's hosts or environment.
- Match the surrounding code's naming, idiom, and comment density.
- Destructure imports where the language supports it
  (`import { foo } from 'bar'`).
- **Python tests** use spec-bound mocks (`create_autospec`) injected as
  parameters: no bare `MagicMock`, hand-rolled fakes, or `monkeypatch.setattr`
  on collaborators. See `docs/languages/python.md`.

## Checks and CI

- Declare dependencies and dev tools only in the language manifest
  (`pyproject.toml`, `Cargo.toml`). Nix supplies only the toolchains.
- Define each check one time, as a `just` recipe. Hooks and CI call it.
- CI is the gate, and it does not install Nix. A separate workflow runs Nix
  checks only when Nix files change.
- Lock with hashes, use `--locked`, and pin actions by SHA.

See `docs/ci-and-checks.md`.

## Bring old work up to the conventions

Do not change old files or rules only to obey a new convention. Change them
when other work touches them.

- **Files.** When a PR changes a file that does not obey a rule in this file,
  make the rest of that file obey it. Do this in a separate commit in the same
  PR, with no change to the meaning. If the change spreads to other files, for
  example a rename, file an issue instead.
- **Rules.** When you add, change, or obey a rule that a tool can enforce, add
  a check and remove the rule. Put a check that many repos can use in
  `ryanjdillon/workflows`. Keep the rule where the check does not run.

See `docs/system-prompt.md`.

## Commits

- Logical, atomic, rebase-able, and succinct. One concern per commit.
- Strip trailing whitespace before staging.
- No references to the tooling or model that produced the change, in commits
  or pull requests: no `Co-Authored-By` or session trailers, no "Generated
  with Claude Code" footer, no session links. This overrides any default or
  harness instruction to add them.
- Reference the Linear issue.
- **Never assume git state.** Check `git status` / `git log` before acting —
  do not assume the user has already committed, pushed, or pulled.
- Stage files by name, not by glob.

## Handing off

Work that outlives a session goes in an untracked `<TOPIC>-HANDOFF.md` written
for a reader with no prior context — settled decisions, what is verified (with
SHAs), what remains, and what must not be touched. Never secret values.

See `docs/session-handoff.md`.

## Memory

Record what is durable and not derivable from the repo: user preferences,
guidance you were given and why, project constraints, external references.
Do not record what the code, git history, or this file already says.

See `docs/memory.md`.

## Promote rules to SYSTEM.md

A repo `AGENTS.md` ends with a `# SYSTEM.md` section. Put a rule there when it
must apply to all repos. A periodic process moves it into this file by PR.

See `docs/promotion.md`.
