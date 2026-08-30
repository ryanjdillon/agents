# Staying on target

## Capture and continue

When work spawns work — a fix reveals a second bug, a read reveals a bad
abstraction, a dependency turns out to be stale — the default is:

> File it as a Linear issue. Continue what you were doing.

This is the single behaviour that most protects a session. Rabbit-holing burns
context and delivers nothing; silent scope expansion delivers something nobody
asked for and makes the change unreviewable.

## When to break the default

Do the new work now only if it is **strategic-critical** (the current task
genuinely cannot land without it) or a **drift-guard** (deferring it means
redoing the current change). Say which, out loud, before switching.

## When to stop instead

If the discovery invalidates the plan itself — the approach cannot work, or the
issue describes something that no longer exists — stop and say so. Do not
improvise a replacement plan mid-change. A wrong plan executed well is the
expensive failure.

## Reporting

At the end, say plainly what was finished, what was filed for later, and what
was left out. Scaling work down is the user's decision, not the agent's.
