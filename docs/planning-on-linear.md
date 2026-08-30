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
| Typo, one-line fix, mechanical rename | No issue |
| Anything worth reviewing | One issue |
| Several related changes | Parent issue plus sub-issues |
| Spans milestones or repos | Linear project with a dependency graph |

Create the parent before the sub-issues, so the sub-issues are filed against a
decided shape rather than an improvised one.

## Drift detection

Before starting, check whether the issue still describes reality. If the
codebase has moved on, update the issue first — then work. Working from a stale
issue silently produces the wrong change.

## Do not

- Invent issues to create the appearance of progress.
- Work substantial changes off-issue.
- Batch-close issues without confirming each one actually shipped.
