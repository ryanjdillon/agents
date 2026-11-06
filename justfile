default:
    @just --list

# Validate every skill's frontmatter.
check-skills:
    python3 scripts/validate-skills.py skills

# Check SYSTEM.md and AGENTS.md against their size budget.
check-instructions:
    nix run --inputs-from . workflows#check-instructions -- SYSTEM.md AGENTS.md

# Report what the promotion process would do. CI does the real runs.
promote *args:
    python3 scripts/promote.py --dry-run {{args}}

# Test the promotion script.
test:
    python3 -m unittest discover -s scripts

# Run every flake check.
check:
    nix flake check

fmt:
    nix fmt
