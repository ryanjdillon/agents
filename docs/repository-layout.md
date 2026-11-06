# Repository layout

Group by language first, then by package: `python/<package>/src/`,
`rust/<crate>/src/`, `go/<module>/` — each following that ecosystem's own
idiomatic internal layout underneath.

## Why language-first

A bare `src/` at the repo root reads as "the packages," with each package
following its own language's convention below it (Python's `src/<name>/src/`
layout, for instance). That works until a second language shows up. There is
then nowhere sensible for it to go: either `src/` gets overloaded to mean two
different things depending on which subdirectory you're in, or the second
language invents its own inconsistent exception. Neither is a decision worth
making under time pressure once the second language already needs a home.

## Decide it early

Pick the top-level split even in a repo that is single-language today, if a
second language is plausible later — a data-heavy service that might grow a
Rust component for performance, for instance. Retrofitting the split later is a
real, if mechanical, refactor: every workspace manifest, build-system package
path, CI path filter, and doc reference that names the old layout has to move
with it. Deciding once, before the second language lands, avoids paying that
cost twice.
