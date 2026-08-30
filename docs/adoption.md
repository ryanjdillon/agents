# Adopting the base in a repo

## Mechanism

The base is a flake input, so `flake.lock` is the pin and `nix flake update` is
the upgrade. A compose step writes a **committed** `AGENTS.md` from the base
plus the repo's overlay, so every tool — Claude, Codex, opencode, or a human —
reads one complete file with no import-following and no submodule checkout.

## Setup

1. Add the input:

   ```nix
   inputs.agents = {
     url = "github:ryanjdillon/agents";
     inputs.nixpkgs.follows = "nixpkgs";
   };
   ```

2. Re-export the compose package so it resolves through this repo's lock:

   ```nix
   packages.compose = inputs.agents.packages.${system}.compose;
   ```

3. Copy `templates/AGENTS.repo.md` to `AGENTS.repo.md` and fill it in.
4. Run `nix run .#compose`. It writes `AGENTS.md` and `agents.just`, and
   symlinks `CLAUDE.md` to `AGENTS.md`.
5. Add `import 'agents.just'` at the top of the repo justfile.
6. Commit `AGENTS.md`, `agents.just`, `AGENTS.repo.md`, and the `CLAUDE.md`
   symlink.

## Without a flake

```bash
git clone https://github.com/ryanjdillon/agents /path/to/agents
/path/to/agents/scripts/compose.sh --base /path/to/agents
```

The script is plain bash with no dependency on Nix or on any particular agent
tool.

## Keeping it honest

`AGENTS.md` and `agents.just` are generated and carry a banner saying so. Wire
`nix run .#compose -- --check` into CI so a hand-edit or a stale base fails the
build instead of rotting quietly.

## Updating

```bash
just agents-update   # nix flake update agents && just agents
```
