# <repo name>

<One paragraph: what this repo is and what it is for.>

## Linear

- Team: `<TEAM>` (issue prefix `<PRE>`)
- Project: <link, if this repo maps to one>

## Tech stack

- <language / runtime / framework>
- <datastore>
- <deploy target>

## Common commands

```bash
just <build>
just <test>
just <deploy>
```

## Architecture

<The shape of the system: the top-level pieces and how they relate. Detail
belongs in `docs/`, not here.>

## Invariants

<Things that must stay true. Each one should be a fact an agent could otherwise
break without noticing.>

- <invariant>

## Drift discipline

Which docs must be updated alongside which code, in the same commit.

| When you change | Also update |
| --- | --- |
| <path> | <doc> |

## Deployment operations

```bash
# <deploy>
# <migrate>
# <rollback>
```

Hosts: <names, and how to reach them>

## Known issues

- <non-blocking thing an agent will otherwise trip over and try to "fix">
