# agents

One maintained base for how AI coding agents work across my repos: planning on
Linear, staying on the critical path, protecting context with sub-agents, and
keeping docs honest. Repo-specific detail stays in each repo; the reusable
process lives here once and is referenced everywhere.

## What is in here

| Path | Purpose |
| --- | --- |
| `AGENTS.base.md` | The shared conventions. Thin by design — rules only. |
| `docs/` | The reasoning and edge cases behind each rule, read on demand. |
| `templates/` | `AGENTS.repo.md` overlay and `docs/index.md` starters. |
| `skills/` | Agent skills, one directory per skill with a `SKILL.md`. |
| `scripts/` | `compose.sh` and `validate-skills.py`, both dependency-free. |
| `agents.just` | Recipes a consuming repo imports. |

## Design

**Composed, not imported.** A consuming repo commits a full `AGENTS.md`
generated from `AGENTS.base.md` plus its own `AGENTS.repo.md`. Every tool reads
one complete file — no `@import` following, no submodule checkout, and the file
still works for a reader with none of this tooling installed.

**A generator, not a dependency.** Consuming repos do not take this as a flake
input — an input is fetched on every evaluation by everyone, and only the person
regenerating the file needs the base. `just agents` runs it on demand; the
`agents_rev` variable pins it when a repo wants that.

**Thin base, deep docs.** `AGENTS.base.md` loads in every session of every repo,
so it stays around 100 lines. Anything longer lives in `docs/` and is read only
when it is needed.

**No tool dependency.** Nothing here requires a particular agent runtime or Nix
distribution. `scripts/compose.sh` is plain bash; `scripts/validate-skills.py`
is stdlib-only Python. The Nix packaging is a convenience, not a requirement.

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
just check            # nix flake check: format, skills, compose round-trip
just fmt
```
