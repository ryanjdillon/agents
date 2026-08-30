# Doc discipline

## Docs alongside code, in the same commit

A change that invalidates a doc updates that doc **in the same commit**. Not in
a follow-up, not in a cleanup pass. The follow-up does not happen, and a doc
that is wrong is worse than a doc that is missing — it is trusted.

This makes each commit self-consistent, which is what makes the history
rebase-able and reviewable.

## Write back what you learn

When you discover something non-obvious while working — an invariant, a gotcha,
why the obvious approach fails, the actual reason a config value is what it is —
put it in the relevant doc before you finish. The cost of rediscovering it is
paid every session, by everyone.

Write back facts, not narrative. "Peer auth means this must run as the service
user" is a fact. "I tried X and it failed" is narrative.

## Structure

- Every `docs/` tree has an `index.md` listing its contents with one-line hooks.
- Every substantial directory has a README explaining what lives there and why.
- Docs live next to what they describe, not in a distant central pile.
