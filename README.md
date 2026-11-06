# agents

`SYSTEM.md` is one set of rules for how AI coding agents work in all my
repos: plan on Linear, stay on the critical path, keep context small with
sub-agents, write in Simplified Technical English, and keep docs correct.
Agent tools load it as the system prompt. Each repo adds its own rules in its
`AGENTS.md`.

## What is in here

| Path | Purpose |
| --- | --- |
| `SYSTEM.md` | The rules for all repos. Short by design: rules only. |
| `AGENTS.md` | The rules for this repo. |
| `docs/` | The reasons and edge cases for each rule. Agents read them on demand. |
| `templates/` | Starters for a repo `AGENTS.md` and `docs/index.md`. |
| `skills/` | Agent skills, one directory for each skill, with a `SKILL.md`. |
| `scripts/` | `validate-skills.py`, and `promote.py` for the promotion process. They use only the Python standard library. |

## Design

**System prompt, not a copy.** Agent tools load `SYSTEM.md` from this repo.
A consuming repo commits only its own `AGENTS.md`. Thus a change to the
shared rules does not need a change in each repo.

**Not a dependency.** Consuming repos do not take this repo as a flake input.
Nix fetches each input when it evaluates the flake, for each user. Only your
tool config needs `SYSTEM.md`.

**Rules move up.** A repo `AGENTS.md` ends with a `# SYSTEM.md` section. A rule
in that section must apply to all repos. A periodic process moves it into
`SYSTEM.md` through a PR. See [docs/promotion.md](docs/promotion.md).

**Short system prompt, deep docs.** Each session of each repo loads
`SYSTEM.md`, so each rule has a cost in all sessions. `nix flake check`
limits it to 8 KB. Put longer text in `docs/`. See
[docs/system-prompt.md](docs/system-prompt.md).

**No tool dependency.** Nothing here needs a specific agent runtime or Nix.
The scripts use only the Python standard library. The Nix packages are a
convenience.

See [docs/adoption.md](docs/adoption.md) for setup.

## Skills

Skills are plain directories — `skills/<name>/SKILL.md` — which makes the same
tree usable three ways:

- **Nix skill source**: point any `skillSources`-style option at this flake's
  `skills` package, or at `${inputs.agents}/skills`.
- **Claude plugin**: `.claude-plugin/marketplace.json` makes the repo
  installable directly.
- **Vanilla install**: copy or symlink `skills/<name>` into `~/.claude/skills/`.

Frontmatter is validated locally — name format and length, non-empty
description, name matching the directory, no duplicate names, no symlinks
escaping a skill directory:

```bash
just check-skills     # or: nix build .#checks.<system>.skills
```

## Development

```bash
nix develop
just check            # nix flake check: format, skills, instruction files
just check-instructions
just fmt
```
