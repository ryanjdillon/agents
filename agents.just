# Recompose AGENTS.md and agents.just from the shared base plus this repo's overlay.
agents:
    nix run .#compose

# Pull the latest shared base, then recompose.
agents-update:
    nix flake update agents
    just agents

# Fail if the committed AGENTS.md or agents.just have drifted from their sources.
agents-check:
    nix run .#compose -- --check
