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

Put `SYSTEM.md` at a stable path, for example `~/.config/agents/SYSTEM.md`.
Then point each tool at it in its user-level config:

| Tool | User-level config |
| --- | --- |
| Claude Code | Add `@~/.config/agents/SYSTEM.md` to `~/.claude/CLAUDE.md`. An import in the user-level file loads without an approval dialog. |
| Codex | `~/.codex/AGENTS.md` (or `$CODEX_HOME/AGENTS.md`). Codex reads only the first file that is not empty, and `AGENTS.override.md` comes before `AGENTS.md`. |
| opencode | `~/.config/opencode/AGENTS.md`, or a path in `instructions` in `~/.config/opencode/opencode.json`. |

opencode does not read `@` imports, and the Codex docs do not describe them.
For these tools, link or copy `SYSTEM.md` to the path.

The `base` package of this flake contains `SYSTEM.md` and `docs/`. A Nix
system config can link `SYSTEM.md` from that package to these paths. Then the
flake lock of the system config is the pin.

Claude Code reads skills only from `.claude/skills` directories, not from
`.agents/skills`.

Sources: <https://code.claude.com/docs/en/memory>,
<https://code.claude.com/docs/en/skills>,
<https://learn.chatgpt.com/docs/agent-configuration/agents-md>,
<https://opencode.ai/docs/rules/>.
