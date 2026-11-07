# Writing SYSTEM.md and AGENTS.md

`SYSTEM.md` and each repo `AGENTS.md` are instruction files. The agent loads
them at the start of each session, before it reads the task. This doc tells
how to keep these files small and effective.

## Why size is a risk

The agent loads each line of an instruction file in each session. Each line
has a token cost in each session of each repo.

The number of rules is a larger risk than the token cost. Studies show that an
agent obeys fewer rules when a file has more rules. The agent usually omits
rules; it does not break them. It obeys the first rules more than the last
rules. The tool's own system prompt and the repo `AGENTS.md` add more rules
to the same context.

An unnecessary rule also has a cost. Agents obey rules that the task does not
need, and this makes the task slower and more expensive.

## What to measure

Measure bytes and rules. Do not measure lines. A change to line wrap changes
the line count, but it does not change the cost.

| File | Byte limit | Rule warning |
| --- | --- | --- |
| `SYSTEM.md` | 8 KB (about 2,000 tokens) | 60 rules |
| A repo `AGENTS.md` | 8 KB | 60 rules |

A rule is a list item or a numbered step. The limits are judgement, not
results from a study. The `check-instructions` check in
`ryanjdillon/workflows` enforces them, and its script is the only definition
of the numbers. If you change a limit, change this table too. Vendor limits are higher: Claude Code advises fewer than
200 lines, and Codex stops reading at 32 KiB.

If a file is near its limit, first move rules out of it. Increase the limit
only when each rule in the file passes the admission test.

## The admission test

A rule goes into `SYSTEM.md` only if all of these conditions are true:

1. The rule applies to each task in each repo.
2. No tool can enforce it.
3. The agent does not already do it without the rule.
4. It does not contradict a different rule.

If condition 1 is false, the rule goes into a repo `AGENTS.md`, a nested
`AGENTS.md`, or a skill. If condition 2 is false, the rule goes into a check.
If condition 3 is false, remove the rule.

A repo `AGENTS.md` uses the same test, for the tasks in that repo.

## Where a rule goes

| The rule is | Put it in |
| --- | --- |
| Necessary for each task in each repo | `SYSTEM.md` |
| Necessary for each task in one repo | The repo `AGENTS.md` |
| Necessary for one directory of a repo | An `AGENTS.md` in that directory |
| A procedure that the agent does sometimes | A skill (`SKILL.md`) |
| The reason for a rule, or an edge case | A doc in `docs/`, with a pointer |
| Mechanical, and a tool can examine it | A check: a linter, a hook, or CI |

A skill loads only its name and description until the agent needs it. Claude
Code, Codex, and opencode support skills.

An `AGENTS.md` in a subdirectory loads only when the agent works in that
directory. Claude Code and Codex support this. opencode reads only the root
file.

## How to write a rule

- Write the rule as a command, in Simplified Technical English. See
  `simplified-technical-english.md`.
- Put the most important rules first.
- Give the reason in a few words when the reason is not clear. A reason helps
  the agent with cases that the rule does not name.
- Do not use capitals, "IMPORTANT", or "MUST" for emphasis. Newer models apply
  emphasised rules too widely. If the agent ignores a rule, the file is too
  long. Emphasis does not repair that.
- Make sure that two rules do not contradict. If two rules contradict, the agent
  selects one, and you cannot predict which.

## Bring old work up to the conventions

A new convention does not start a sweep of all files. A sweep makes large
diffs that are hard to review, and they conflict with other work. Instead,
old work comes up to the conventions when normal work touches it. This is a
ratchet: the number of files that obey the conventions only increases.

- **Files.** A PR that changes a file also makes the rest of that file obey
  the conventions, for example STE. The rewrite is a separate commit in the
  same PR, so that the reviewer can examine the content change and the
  rewrite one at a time. A rewrite commit does not change a meaning. The PR
  does not change other files only to rewrite them. If the rewrite spreads to
  other files, for example a rename in code, it is a separate issue.
- **Rules.** A rule that a tool can enforce goes into a check (see the table
  above). When you add, change, or obey such a rule, add the check and remove
  the rule. A check costs no context, and it does not depend on the agent.
  Put a check that many repos can use in `ryanjdillon/workflows`, with its
  adapters. Keep the rule in the repos where the check does not run, because
  the agent still needs it there.

## What does not reduce size

An `@import` in a `CLAUDE.md` loads the imported file at the start, in full. It
makes the files easier to organise, but it does not reduce the context. opencode
does not read `@import` lines.

## Evidence

- IFScale: adherence falls as the number of instructions increases.
  <https://arxiv.org/abs/2507.11538>
- Context files add more than 20% cost and do not increase success.
  <https://arxiv.org/abs/2602.11988>
- Claude Code memory and rules: <https://code.claude.com/docs/en/memory>
- Claude Code best practices:
  <https://www.anthropic.com/engineering/claude-code-best-practices>
- Effective context engineering:
  <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- Codex `AGENTS.md`: <https://learn.chatgpt.com/docs/agent-configuration/agents-md>
- opencode rules: <https://opencode.ai/docs/rules/>
- The `AGENTS.md` format: <https://agents.md/>
