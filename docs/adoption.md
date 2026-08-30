# Adopting the base in a repo

## Mechanism

The base is a **maintainer-side generator**, not a build dependency. A compose
step writes a **committed** `AGENTS.md` from the base plus the repo's overlay,
so every tool — Claude, Codex, opencode, or a human — reads one complete file
with no import-following, no submodule, and no flake input.

That last point matters: a flake input is fetched whenever the consuming flake
is evaluated, by everyone, forever. The base has no business being in that path
when the only thing that needs it is the person regenerating the file.

## Setup

1. Copy `templates/AGENTS.repo.md` to `AGENTS.repo.md` and fill it in.
2. Run the compose:

   ```bash
   nix run --refresh 'github:ryanjdillon/agents#compose'
   ```

   `--refresh` matters: without it Nix serves the flake from its tarball cache
   for up to an hour, so a base change pushed minutes ago composes silently
   stale.

   It writes `AGENTS.md` and `agents.just`.
3. Add `import 'agents.just'` at the top of the repo justfile.
4. Commit `AGENTS.md`, `agents.just`, and `AGENTS.repo.md`.

No `CLAUDE.md` is created. Claude Code reads `AGENTS.md` directly (verified
against 2.1.233), as do Codex and opencode. Pass `--claude-link` only for a tool
that looks exclusively for `CLAUDE.md`.

The repo's own `flake.nix` is untouched.

## Pinning

`agents.just` carries an `agents_rev` variable, defaulting to `main`. Set it to
a tag or SHA to freeze the base for that repo. Because the composed output is
committed, an unpinned base still cannot change a repo silently — it can only
produce a diff you review before committing.

## Without Nix

```bash
git clone https://github.com/ryanjdillon/agents /path/to/agents
/path/to/agents/scripts/compose.sh --base /path/to/agents
```

The script is plain bash with no dependency on Nix or on any agent tool.

## Keeping it honest

`AGENTS.md` and `agents.just` are generated and carry a banner saying so. Wire
`just agents-check` into CI so a hand-edit or a stale base fails the build
instead of rotting quietly.

## Updating

```bash
just agents    # recompose against agents_rev
```
