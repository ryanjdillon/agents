# Promoting rules to SYSTEM.md

`SYSTEM.md` holds the rules for all repos. A repo `AGENTS.md` holds the rules
for one repo. Sometimes a rule starts in one repo and then must apply to all
repos. The `# SYSTEM.md` section moves that rule to `SYSTEM.md`.

## The section

Each repo `AGENTS.md` ends with this section:

```markdown
# SYSTEM.md

<!-- Rules for all repos. A periodic process moves them to SYSTEM.md. -->
```

- The heading is exactly `# SYSTEM.md`, as a level-one heading.
- The section is the last section of the file. It continues to the end of the
  file.
- Write each rule in the form that it must have in `SYSTEM.md`: a `##` heading
  and its text. The process copies the text without changes.
- Keep the section and its comment when the section is empty. The process
  finds the section by its heading.

## When to put a rule in the section

Put a rule in the section only if it passes the admission test in
`system-prompt.md`. If you are not sure, put the rule in the repo part of
`AGENTS.md`. You can move it later.

## The process

The process runs periodically from this repo. For each consuming repo:

1. Read `AGENTS.md` and find the `# SYSTEM.md` section.
2. If the section has no rules, go to the next repo.
3. Open a PR to `ryanjdillon/agents` that adds the rules to `SYSTEM.md`.
4. When that PR merges, open a PR to the consuming repo that empties the
   section.

The PR to `SYSTEM.md` is the review step. Edit the rule there, or reject it,
before it applies to all repos. Do not empty the section before the first PR
merges. If you do, a rejected rule is lost.

`SYSTEM.md` has a size limit. A promoted rule must fit in the limit. Move its
details into `docs/` if necessary. See `system-prompt.md`.
