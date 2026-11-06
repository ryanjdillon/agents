# agents

This repo holds `SYSTEM.md`, the rules for agents in all my repos, and the
docs and skills that go with it. Agent tools load `SYSTEM.md` as the system
prompt. This file has the rules for work in this repo only.

## Linear

- Team: `software` (issue prefix `DIL`)
- Project: Reusable agent conventions (ryanjdillon/agents base)

## Common commands

```bash
prek install          # one time: run the hooks on each commit
just check            # nix flake check: format, skills, instruction files
just check-instructions
just check-skills
just test             # unit tests for scripts/promote.py
just promote          # dry run of the promotion process
just fmt
```

## Invariants

- `SYSTEM.md` is 8 KB or smaller. `check-instructions` in
  `ryanjdillon/workflows` enforces this.
  Move detail into `docs/` and leave a pointer. Do not increase the limit.
- `SYSTEM.md` is for all repos. Do not put rules for this repo in it.
- Each rule in `SYSTEM.md` that has a doc ends with a `See docs/<topic>.md`
  pointer, and `docs/index.md` lists that doc.
- Nothing here needs a specific agent runtime. Scripts use only bash or the
  Python standard library.
- CI does not install Nix. `nix.yml` runs `nix flake check` only when Nix
  files change.

## Drift discipline

| When you change | Also update |
| --- | --- |
| A rule in `SYSTEM.md` | Its doc in `docs/` |
| A file in `docs/` (add or remove) | `docs/index.md` |
| The admission test | `docs/system-prompt.md` |
| The size limits | `check-instructions.py` in `ryanjdillon/workflows`, and `docs/system-prompt.md` |
| The `ryanjdillon/workflows` pin | `flake.lock`, `.pre-commit-config.yaml`, and both workflows in `.github/workflows/`, to the same commit |
| `scripts/promote.py` | `docs/promotion.md` and `scripts/test_promote.py` |
| The `# SYSTEM.md` section format | `docs/promotion.md`, `templates/AGENTS.md` |
| How a repo loads or adopts the rules | `docs/adoption.md`, `README.md` |

# SYSTEM.md

<!-- Rules for all repos, not only this repo. A periodic process moves them to
     SYSTEM.md. See docs/promotion.md. -->
