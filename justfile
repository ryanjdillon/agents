default:
    @just --list

# Validate every skill's frontmatter.
check-skills:
    python3 scripts/validate-skills.py skills

# Check SYSTEM.md and AGENTS.md against their size budget.
check-instructions:
    nix run --inputs-from . workflows#check-instructions -- SYSTEM.md AGENTS.md

# Run every flake check.
check:
    nix flake check

fmt:
    nix fmt
