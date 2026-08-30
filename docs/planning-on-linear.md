# Planning on Linear

## Why Linear rather than the repo

Git history explains what changed. It does not explain what was considered and
deferred, what is blocked on what, or what "done" means. Keeping that in Linear
means a deferred discovery survives the end of a session, so deferring costs
nothing — which is what makes [capture-and-continue](staying-on-target.md)
safe.

## Lifecycle

1. **File** before starting anything worth reviewing.
2. **Move to In Progress** when work actually begins, not when it is planned.
3. **Ship**, referencing the issue identifier in the commit message.
4. **Close** on ship. An issue left open after its change ships is worse than no
   issue — it makes the board untrustworthy.

## Tracking tiers

| Size | Tracking |
| --- | --- |
| Trivial: typo, whitespace, one-line doc tweak | No issue — just commit |
| Single change: 3+ steps, or one subsystem | One issue |
| Multi-step within one subsystem | Parent issue plus task sub-issues |
| Spans subsystems, or more than a handful of subs | Linear project with a dependency graph |

Create the parent before the sub-issues, so the sub-issues are filed against a
decided shape rather than an improvised one. Track multi-step work as parent
plus subs **up front** — do not one-shot it and retrofit the structure.

## Auto-close on ship

When work is implemented and committed, mark its issue **Done in the same
turn**. Issues left in "In Review" indefinitely are what produces board drift
that later has to be cleaned up by hand.

The exception is an explicit "leave it open, I want to look first" — then leave
it In Review and let the user close it.

**Parent lifecycle:** never mark a parent Done while any sub is still open.
Close every sub first, then the parent.

**Operator or external work** — DNS changes, third-party onboarding, manual
production data fixes — stays In Progress until the user confirms it happened
out of band. A repo grep cannot verify it, so do not close it on inference.

## Drift detection

Before starting, check whether the issue still describes reality. If the
codebase has moved on, update the issue first — then work. Working from a stale
issue silently produces the wrong change.

**When picking up a session**, scan `In Review` and `In Progress` first. Anything
sitting in either state for more than about a week without commit activity is
suspect and may already have shipped. Verify by grepping the repo for the
issue's named files and symbols, then close it.

## Commit messages

For a commit that resolves an issue, put the identifier in the subject
(`(ABC-123)` or `Closes ABC-123`) so the link is visible in `git log`. The
status transition still happens through the Linear MCP tools — the commit
message alone does not move the issue.

Use the MCP tools for every state change rather than telling the user to open
the web UI, unless the action genuinely requires it.

## Batches

When processing several issues at once, drive them through a queue: one issue
per branch, verify and commit each, then merge least-conflict-first. Decide up
front what makes you stop and ask rather than guess.

## Drift detection

Before starting, check whether the issue still describes reality. If the
codebase has moved on, update the issue first — then work. Working from a stale
issue silently produces the wrong change.

## Do not

- Invent issues to create the appearance of progress.
- Work substantial changes off-issue.
- Batch-close issues without confirming each one actually shipped.
