---
name: design-review
description: Checklist and method to review engineering work such as code, CAD parts and schematics. Use when you review a pull request, a part, a circuit or a plan that another author made.
---

# Design review

Review the work against the requirement, not against your own preferred
solution. Do not rewrite the work unless the author asks you to.

## Before you start

1. Find the requirement or spec that the work answers. If there is none,
   say so first.
2. Read every other review of the work. For each item, agree, disagree with
   a reason, or confirm that it is fixed.
3. Read the CI result first. If CI is red, request changes for that reason.
   Do not run again a check that CI ran.

## How to review

- Review the whole change against the full checklist in each round. Do not
  review only the new commits.
- Build or run the work yourself. Print the numbers that you judge, for
  example a bounding box, a volume, a radius or an error count.
- Run one or more negative checks. Give the work a known defect and make
  sure that the check fails.
- A review that only reads the diff is not complete.

## Checklist

1. **Requirement.** The work does what the requirement asks, for the stated
   load, environment and duty cycle. Units, tolerances and limits are
   correct.
2. **Interfaces and fit.** Each interface agrees with the part or module on
   the other side. Mating dimensions, pin maps and API contracts agree.
3. **Safety.** Examine pinch points, rotating parts, heat, electrical
   isolation, batteries and failure modes. An unhandled hazard is a blocker.
4. **Parameters.** Each parameter has a validated range. The design is
   consistent at each limit of the range, not only at the default.
5. **Geometry where features meet.** Probe the material at each place where
   two features meet, not only in the middle of a wall. Do this for each
   variant that the tests use.
6. **Tests mean something.**
   - No assertion compares a value with itself or a parameter with a
     parameter. Tests measure the built result.
   - Each negative check fails on its seeded defect.
   - The envelope is asserted on all axes, for the default and each variant.
7. **Hygiene.**
   - No `sys.path` edits. Import the code as a package.
   - No unused imports.
   - No part number or rating without a source.
   - Code, comments and commit messages describe the design, not the
     review. They contain no review item numbers and no review words such
     as "blocker", "should-fix", "finding N", "re-review" or "hand-back".
   - A commit message refers to its issue. This is correct and expected.
8. **Scope.** Mark changes that are not related to the requirement, and
   features that nobody asked for.

## Verdict

- Mark each item as **blocker**, **should-fix** or **note**.
- Give each item a `file:line` or the measured number.
- Tell what fails and why.
- The first line of the verdict comment is exactly `Verdict: approve` or
  `Verdict: request changes (N blockers)`. Plain text: no `#`, no `**`,
  nothing before it. Use `1 blocker` for one blocker. Example first line:

  ```text
  Verdict: request changes (2 blockers)
  ```

- If the review has its own issue, give it the title
  `Review PR #<n> round <k>` or `Review <branch>@<sha> round <k>`. Round 1
  is the first review. Each new review of the same work adds 1.
- List the blockers, then the should-fix items, then the notes.
- Only a blocker stops the approval. A should-fix item never causes a new
  review round. The author folds it into the next push.
- Do not push to the author's branch. Do not change the author's issue.
