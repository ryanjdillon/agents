# Planning strategically

The layer above project decomposition. Its job is to stop two failure modes:
shortsighted shortcuts that cause rework, and gold-plating that never reaches
the objective.

## The descent

**Initiative** (the goal, one sentence) → **projects** (each with acceptance
criteria) → **critical path** → **classified work**.

## Two paths, mapped separately

- The **critical path to the objective**: the shortest honest route to the goal.
- The **path to the target state**: what the system should look like when it is
  clean.

These diverge. Mapping them together produces a plan that is either too slow
(every cleanup on the critical path) or too dirty (no cleanup ever). Map them
apart, then classify.

## Classification

Every body of work is exactly one of:

- **strategic-critical** — on the critical path. Do it now.
- **drift-guard** — off the path, but deferring it means redoing work later.
  Do it now, and say why.
- **target-state-deferrable** — improves the end state, costs nothing to defer.
  File it and move on.

If you cannot classify a piece of work, the plan is not finished.

## The rule

No shortsighted shortcuts; no gold-plating. A shortcut that creates a
drift-guard for later is not a shortcut, it is a loan.

## Mapping a project

For work spanning several subsystems, or decomposing into more than a handful
of sub-issues, map it as a Linear project **before writing code**, so the
critical path and the parallelisable branches are explicit rather than buried
in prose.

1. **Create the project.** Its description is the source of truth: settled
   design decisions, the explicit critical path, what is out of scope or
   deferred (linked), and the definition of done. Set a priority.
2. **Feature parents** — one per shippable slice, each carrying scope and a
   definition of done.
3. **Task sub-issues** under each parent, small enough to land in one commit.
   Split tests into their own sub-issue when that keeps the slice reviewable.
4. **Make the graph legible.** Set priorities so the critical path reads high
   and leaf work reads low. Encode real dependencies as `blocks` / `blockedBy`
   **edges, not sentences** — "this parallels X once the data model lands" must
   be an edge, or nobody can see the critical path at a glance.
5. **Tests are the definition of done.** Written, run, and passing before a
   parent closes — and the parent-before-subs rule still applies.
6. **Record the project in memory** with its issue range and critical path, so
   a later session picks it up without re-deriving it.
