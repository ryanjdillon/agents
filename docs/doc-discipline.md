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

## Facts need a source

Do not write a part number, a rating, a price, or another fact from memory.
This applies to code, docs, and commit messages. A fact from memory can be
wrong, and the reader cannot see that it is not verified.

- Read the fact from a source in the current task: a datasheet, a standard,
  the manufacturer, or the code.
- Name the source next to the fact, for example with a URL.
- If you cannot read a source, leave the field blank and write "to verify".

The `web-research` skill tells how to fetch and label a source.

## Structure

- Every `docs/` tree has an `index.md` listing its contents with one-line hooks.
- Every substantial directory has a README explaining what lives there and why.
- Docs live next to what they describe, not in a distant central pile.

## Voice

Concise, never verbose. Lead with the point, order sections the way a reader
meets the topic, and stop when the point is made. One clear framing beats three
restatements.

A README is a landing page, not a manual: a short orientation that links into
the docs. Direct and spoken-word — welcoming without being cutesy, confident
without selling. Say what the thing does and how to run it; let the quality show
rather than asserting it.

## Deslop

Cut the tells of machine-written prose:

- No marketing adjectives — `powerful`, `seamless`, `robust`, `blazing-fast`,
  `elegant`.
- No `simply` / `just` / `of course` filler.
- No "it's not just X, it's Y" and no "whether you're… or…" constructions.
- No rule-of-three padding, throat-clearing intros, or "in summary" outros.
- No emoji bullets.

Prefer concrete nouns and verbs over hedging.
