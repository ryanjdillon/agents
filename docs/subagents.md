# Sub-agents and context hygiene

## The principle

The main thread should hold decisions, not the material the decisions were made
from. Anything that produces bulk you will not re-read belongs in a sub-agent.

## Delegate

- Broad searches across many files or naming conventions
- Multi-file reads where you need a conclusion, not the contents
- Research spikes with an uncertain number of steps
- Digesting large tool output (logs, test dumps, API responses)

## Keep in the main thread

- The decision and its rationale
- The Linear update
- The edits themselves
- Anything a single targeted read answers — delegation has a cost, and a
  one-file lookup is cheaper done directly

## Return contracts

State in the sub-agent's prompt what shape the answer must take: the fields, the
maximum length, and that raw excerpts are not wanted. A sub-agent that returns
its transcript has defeated the purpose.

Sub-agent context is discarded when it finishes. That is safe precisely because
[Linear holds the durable record](planning-on-linear.md) — if a discovery
matters, it becomes an issue, not a paragraph in a transcript.
