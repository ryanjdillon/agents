default:
    @just --list

# Validate every skill's frontmatter.
check-skills:
    python3 scripts/validate-skills.py skills

# Run every flake check.
check:
    nix flake check

fmt:
    nix fmt
