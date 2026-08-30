# Session handoff docs

Long-running work — multi-phase buildouts, rollouts, migrations — outlives a
single session. Carry that state forward in a **handoff doc** rather than
relying on context surviving a compaction.

## When to write one

- Before clearing or compacting a session with unfinished multi-step work.
- At the end of any session whose remaining work spans more than one sitting.
- When the user asks for one, or work passes to another session.

## Where it goes

`<TOPIC>-HANDOFF.md` in the repo root. Keep it **untracked** — these are working
state, not documentation. Do not move one into `docs/`; that tree is for
durable, publishable material.

Delete the handoff once its work is done, promoting anything with lasting value
into `docs/` as a proper document first.

## What goes in it

Write for a session with *no* prior context:

1. **Goal and architecture** — decisions already made, marked settled so they
   are not relitigated.
2. **Hosts and how to operate** — access paths and the operating rules in force.
3. **What is done and verified** — with commit SHAs, so claims are checkable.
4. **Remaining work** — ordered, each item concrete enough to start from cold.
5. **Known open issues** — root causes, gotchas, and dead ends, so they are not
   rediscovered.
6. **Verification snippets** — the exact commands that prove the system healthy.
7. **Untouched WIP** — files touched by unrelated work, flagged do-not-touch.

## What must never go in it

Never paste secret **values** — no API keys, tokens, or decrypted secrets.
Reference them by name and location, and use placeholders like
`__GITHUB_TOKEN__` in config excerpts.

## Relationship to memory

Handoff docs are per-effort and disposable. Durable, cross-project facts belong
in memory instead, and the handoff should link to the relevant memory entries by
name.
