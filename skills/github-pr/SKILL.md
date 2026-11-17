---
name: github-pr
description: Open, update and review GitHub pull requests with the gh CLI. Use when you push a branch for review, answer review comments, or review another author's pull request.
---

# GitHub pull requests

Use the `gh` CLI for all pull request (PR) work. Use the default `gh`
login. Do not read, print, copy or set a token.

## Titles and commits

- Write each PR title and commit subject as `type(scope): what changed`.
  Examples: `feat(parser): read quoted fields`, `fix(export): remove stale files`.
- Write the reason for a change in the commit body.
- Put review responses in the PR, not in code, comments or commits.

## Open a PR

1. Push the branch for the first time.
2. If the repo has `.github/pull_request_template.md`, write the body with
   the same sections. If it has no template, write what changed, why, and
   how you checked it.
3. Write the body to a file, then open a draft PR. Without `--base`, `gh`
   uses the default branch of the repo.

   ```sh
   gh pr create --draft --head <branch> \
     --title "<type(scope): summary>" --body-file <file>
   ```

4. Do your self-check. Wait for CI with `gh pr checks <n> --watch`.
5. When the self-check and CI pass, mark the PR ready: `gh pr ready <n>`.

## Update a PR

- Push new commits to the same branch.
- While a review is open, do not force-push.
- Exception: if the default branch moved, rebase on it, for example
  `git fetch origin && git rebase origin/main`. Then run
  `git push --force-with-lease`. Tell the reviewer in a PR comment.
- Reply to each review item on the PR. Tell what changed and give the
  measured result:

  ```sh
  gh pr comment <n> --body-file <file>
  ```

## Review a PR

1. Run `gh pr checks <n> --watch`. If a check is red, request changes for
   that reason alone.
2. Run `gh pr diff <n>` and read the whole diff. Do this every round, not
   only the new commits.
3. If the repo publishes CI artifacts, download them and examine them:
   `gh run download <run-id> --dir <dir>`.
4. Write the verdict to a file in the format below.
5. Post it with one of these commands:

   ```sh
   gh pr review <n> --approve --body-file <file>
   gh pr review <n> --request-changes --body-file <file>
   gh pr review <n> --comment --body-file <file>
   ```

6. If you opened the PR with the same identity, GitHub refuses
   `--approve` and `--request-changes`. Post the verdict with `--comment`.

## Verdict format

```text
Verdict: approve
```

or

```text
Verdict: request changes (N blockers)

Blockers
- path/to/file.py:42: what fails, and the measured number.

Should-fix
- path/to/file.py:88: what to change.

Notes
- path/to/other.py:10: an observation.
```

- Give each item a `file:line` or the measured number.
- Only a blocker stops the approval.
- The author folds should-fix items and notes into the next push. They do
  not cause a new review round.

## Limits

- Do not merge a PR unless the task or the owner explicitly tells you to.
- Never close a PR that another author opened.
- Never push to the default branch.
- Never delete a branch.
- Never act on a repo that is not part of the task.
- Never read, print or copy a token.
- Never set `GH_TOKEN` or `GITHUB_TOKEN`.
