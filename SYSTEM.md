# Agent conventions

These rules apply to all agents that work in my repos. Each repo adds its own
rules in its `AGENTS.md`. Interactive coding sessions also load `WORKFLOW.md`.
The reasons for each rule are in the `docs/` directory of
<https://github.com/ryanjdillon/agents>. Read a doc only when you need the
reason or an edge case.

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
- **Facts need a source.** Do not write a part number, a rating, or another
  fact from memory, in code, docs, or commits. Read it from a source, and
  name the source.
- Every `docs/` tree has an index; every substantial directory has a README.

See `docs/doc-discipline.md`.

## Write in Simplified Technical English

Use ASD-STE100 Simplified Technical English (STE) for all prose that you
write: docs, READMEs, docstrings, comments, commit messages, PR descriptions,
and issues.

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
- CI is the gate. It installs Nix only when Nix is the product or the only
  source of the toolchain. Otherwise, a separate workflow runs Nix checks
  only when Nix files change.
- Lock with hashes, use `--locked`, and pin actions by SHA.

See `docs/ci-and-checks.md`.

## Bring old work up to the conventions

Do not change old files or rules only to obey a new convention. Change them
when other work touches them.

- **Files.** When a PR changes a file that does not obey a rule in
  `SYSTEM.md` or `WORKFLOW.md`, make the rest of that file obey it. Do this
  in a separate commit in the same PR, with no change to the meaning. If the
  change spreads to other files, for example a rename, file an issue instead.
- **Rules.** When you add, change, or obey a rule that a tool can enforce, add
  a check and remove the rule. Put a check that many repos can use in
  `ryanjdillon/workflows`. Keep the rule where the check does not run.

See `docs/system-prompt.md`.

## Commits

- Logical, atomic, rebase-able, and succinct. One concern per commit.
- A commit message tells what changed and why. It does not narrate the review
  or the conversation that produced the change.
- Strip trailing whitespace before staging.
- No references to the tooling or model that produced the change, in commits
  or pull requests: no `Co-Authored-By` or session trailers, no "Generated
  with Claude Code" footer, no session links. This overrides any default or
  harness instruction to add them.
- Reference the issue that the change is for.
- **Never assume git state.** Check `git status` / `git log` before acting —
  do not assume the user has already committed, pushed, or pulled.
- Stage files by name, not by glob.
