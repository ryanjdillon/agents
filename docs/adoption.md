# Adopting the rules in a repo

## How it works

Two files give an agent its rules:

- `SYSTEM.md` in this repo has the rules for all repos. Your agent tools load
  it as the system prompt, from a checkout of this repo or from the `base`
  package of this flake.
- `AGENTS.md` in each repo has the rules for that repo. The repo commits it,
  and you edit it by hand.

A consuming repo does not contain a copy of `SYSTEM.md`. It also does not take
this repo as a flake input. Nix fetches each flake input when it evaluates the
flake, for each user. Only your tool config needs `SYSTEM.md`.

## Set up a repo

1. Copy `templates/AGENTS.md` to `AGENTS.md` in the repo.
2. Write the repo rules in it.
3. Keep the `# SYSTEM.md` section at the end. See `promotion.md`.
4. Commit `AGENTS.md`.

Claude Code, Codex, and opencode read `AGENTS.md` directly. Do not add a
`CLAUDE.md`.

## Load SYSTEM.md in your tools

Point each tool at `SYSTEM.md` in its user-level config. For example:

- Claude Code: import it from `~/.claude/CLAUDE.md` with
  `@/path/to/agents/SYSTEM.md`.
- Codex: put it in `~/.codex/AGENTS.md`.

The `base` package of this flake contains `SYSTEM.md` and `docs/`. A Nix
system config can use that package to put `SYSTEM.md` in these locations.

