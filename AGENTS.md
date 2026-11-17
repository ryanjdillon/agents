# agents

This repo holds `SYSTEM.md`, the rules for agents in all my repos,
`WORKFLOW.md`, the rules for interactive coding sessions, and the docs and
skills that go with them. Agent tools load them as the system prompt. This file has the rules for work in this repo only.

## Linear

- Team: `software` (issue prefix `DIL`)
- Project: Reusable agent conventions (ryanjdillon/agents base)

## Common commands

```bash
prek install          # one time: run the hooks on each commit
just check            # nix flake check: format, skills, promotion tests
just check-instructions
just check-skills
just check-templates  # fail if SYSTEM.md or WORKFLOW.md contains `{{`
just test             # unit tests for scripts/promote.py
just promote          # dry run of the promotion process
just fmt
```

## Invariants

- `SYSTEM.md` and `WORKFLOW.md` are each 8 KB or smaller.
  `check-instructions` in `ryanjdillon/workflows` enforces this.
  Move detail into `docs/` and leave a pointer. Do not increase the limit.
- `SYSTEM.md` is for all repos and all agents. A rule that needs Linear or
  sub-agents goes in `WORKFLOW.md`. Do not put rules for this repo in either.
- Do not commit a file that joins `SYSTEM.md` and `WORKFLOW.md`. Consumers
  join them.
- Skill frontmatter has only `name` and `description`, each on one line. Some
  consumers read only flat `key: value` lines, and Claude Code parses YAML.
  `scripts/validate-skills.py` enforces this.
- Each rule in `SYSTEM.md` that has a doc ends with a `See docs/<topic>.md`
  pointer, and `docs/index.md` lists that doc.
- Nothing here needs a specific agent runtime. Scripts use only bash or the
  Python standard library.
- CI does not install Nix. `nix.yml` runs `nix flake check` only when Nix
  files change.

## Drift discipline

| When you change | Also update |
| --- | --- |
| A rule in `SYSTEM.md` or `WORKFLOW.md` | Its doc in `docs/` |
| A file in `docs/` (add or remove) | `docs/index.md` |
| The admission test | `docs/system-prompt.md` |
| The size limits | `check-instructions.py` in `ryanjdillon/workflows`, and `docs/system-prompt.md` |
| The `ryanjdillon/workflows` pin | `.pre-commit-config.yaml` and both workflows in `.github/workflows/`, to the same release. Renovate moves them in one PR. |
| `scripts/promote.py` | `docs/promotion.md` and `scripts/test_promote.py` |
| The `# SYSTEM.md` section format | `docs/promotion.md`, `templates/AGENTS.md` |
| How a repo loads or adopts the rules | `docs/adoption.md`, `README.md` |

# SYSTEM.md

<!-- Rules for all repos, not only this repo. A periodic process moves them to
     SYSTEM.md. See docs/promotion.md. -->
