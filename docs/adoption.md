# Adopting the rules in a repo

## How it works

Three files give an agent its rules:

- `SYSTEM.md` in this repo has the rules for all repos and all agents. Your
  agent tools load it as the system prompt, from a checkout of this repo or
  from the `base` package of this flake.
- `WORKFLOW.md` in this repo has the rules for interactive coding sessions:
  Linear, sub-agents, hand-off, memory, and promotion. Load it after
  `SYSTEM.md` in interactive coding tools. Do not load it in an agent that
  runs unattended in a platform, or that does not have these tools.
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

## Load the rules in your tools

Join `SYSTEM.md` and, where it applies, `WORKFLOW.md` into one file in your
tool config, for example with `pkgs.concatText` in Nix. Then point each tool
at that file when it starts, or in its user-level config:

| Tool | How to load the joined file |
| --- | --- |
| Claude Code | Start `claude` with `--append-system-prompt-file /path/to/the/joined/file`, for example in a wrapper script. The flag takes one file. |
| pi | `$PI_CODING_AGENT_DIR/APPEND_SYSTEM.md` (by default `~/.pi/agent/APPEND_SYSTEM.md`), or `--append-system-prompt`. Do not name it `SYSTEM.md` there: pi then replaces its own system prompt with the file. |
| Codex | `~/.codex/AGENTS.md` (or `$CODEX_HOME/AGENTS.md`). Codex reads only the first file that is not empty, and `AGENTS.override.md` comes before `AGENTS.md`. |
| opencode | `~/.config/opencode/AGENTS.md`, or a path in `instructions` in `~/.config/opencode/opencode.json`. |

opencode does not read `@` imports, and the Codex docs do not describe them.
For these tools, link or copy the joined file to the path.

Do not import `SYSTEM.md` with `@` in `~/.claude/CLAUDE.md` if you use more
than one Claude Code profile. Each profile that uses the same config directory
reads that file, so a work profile also gets these rules. A flag in the
wrapper of each profile applies the rules only to that profile.

The `base` package of this flake contains `SYSTEM.md`, `WORKFLOW.md`, and
`docs/`. A Nix system config can join the files from it, give the store path
of the result to the flag, or link it to the paths above. Then the flake
lock of the system config is the pin.

Claude Code reads skills only from `.claude/skills` directories, not from
`.agents/skills`.

Sources: <https://code.claude.com/docs/en/memory>,
the pi README (Context Files, System Prompt),
<https://code.claude.com/docs/en/skills>,
<https://learn.chatgpt.com/docs/agent-configuration/agents-md>,
<https://opencode.ai/docs/rules/>.
