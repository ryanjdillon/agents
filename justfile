default:
    @just --list

# Validate every skill's frontmatter.
check-skills:
    python3 scripts/validate-skills.py skills

# Fail if a prompt file is missing or contains `{{`. pi renders its system
# prompt as a template, so the text would change.
check-templates:
    test -f SYSTEM.md && test -f WORKFLOW.md && ! grep -n '{{{{' SYSTEM.md WORKFLOW.md

# Check SYSTEM.md, WORKFLOW.md and AGENTS.md against their size budget.
check-instructions:
    prek run check-instructions --all-files

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
