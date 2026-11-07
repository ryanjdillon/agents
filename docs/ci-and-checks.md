# Checks and CI

This doc tells how a repo declares its dependencies, defines its checks, and
runs them on a local machine and in CI. The objectives are:

- A contributor who does not use Nix can follow the usual workflow of the
  language.
- CI is fast and uses little compute.
- The supply chain is secure.

## Declare dependencies in the language manifest

The language manifest is the only declaration of dependencies:
`pyproject.toml` with `uv.lock`, or `Cargo.toml` with `Cargo.lock`.

- Declare the dev tools in the manifest too. Put `ruff` and `pytest` in a uv
  dependency group. Put the Rust version in `rust-toolchain.toml`. Then the
  lockfile also pins the tools that do the checks.
- The Nix devshell supplies only the toolchains: `uv`, `rustup` or `cargo`,
  `just`, and the hook runner. Do not declare a dependency in Nix and in the
  manifest. Two declarations drift apart.

## Define each check one time

Each check has one definition: a `just` recipe that calls the language tools.
The hooks and CI call the same recipe.

```just
# Format, lint, and test. CI runs this recipe.
check: lint test audit

lint:
    uv run --locked ruff format --check
    uv run --locked ruff check

test:
    uv run --locked pytest

audit:
    uv run --locked pip-audit
```

For Rust, use `cargo fmt --check`, `cargo clippy --locked -- -D warnings`,
`cargo test --locked`, and `cargo deny check`.

If a hook and CI do not call the same command, they will drift apart. Then a
change that passes on your machine can fail in CI, or the opposite.

## Hooks are for speed; CI is the gate

CI blocks the merge. Hooks only give fast feedback before you push. Do not
rely on hooks, because each contributor configures a machine differently.

- Use `prek`. It reads `.pre-commit-config.yaml`, and it works without Nix.
  A contributor who uses `pre-commit` can use the same config.
- Run `prek install` one time in each clone to install the git hooks.
- Write the hooks as local hooks that call the `just` recipes. Do not use a
  third-party remote hook repository. It is an additional supply chain. The
  shared checks in `ryanjdillon/workflows` are the exception: pin a release
  by its commit SHA, with `# frozen: vX.Y.Z` after the `rev:`.
- Run only the fast checks (format and lint) in a pre-commit hook. Run the
  tests in CI, or in a pre-push hook.
```yaml
repos:
  - repo: local
    hooks:
      - id: lint
        name: lint
        entry: just lint
        language: system
        pass_filenames: false
  - repo: https://github.com/ryanjdillon/workflows
    rev: <commit SHA>
    hooks:
      - id: check-instructions
```

- If you use Nix, `nix flake check` can run the same checks on your machine.
  Do not make Nix the only way to run a check in a service.

## Run CI without Nix

Use Nix on your machine if you want to. Do not install Nix in the normal CI
workflow, also in a repo that uses Nix for its devshell. A cold
`nix flake check` installs Nix and downloads hundreds of MB of toolchain on
each run. The language setup actions cache with no configuration.

- Use the setup action of the language, for example `astral-sh/setup-uv` with
  its cache enabled. Then run `just check`.
- If the repo has Nix files, add a second workflow that calls
  `ryanjdillon/workflows` `nix-check.yml`. Filter it on the paths `**.nix` and
  `flake.lock`. Then only a change to Nix files pays for Nix.
- Do not make the Nix workflow a required status check. When the path filter
  skips it, a required check stays pending and the PR cannot merge.
- A repo that builds Nix outputs as its product, for example a system config,
  runs Nix in its normal CI.
- Set `permissions: contents: read` at the top of each workflow. Give more
  permissions only to the job that needs them.
- Set `persist-credentials: false` on `actions/checkout` when the job does not
  push.

## Secure the supply chain

- **Lock with hashes, and enforce the lock.** `uv.lock` records hashes, and
  `Cargo.lock` records checksums. Use `--locked` in CI so that a manifest that
  does not agree with its lockfile fails.
- **Pin actions by commit SHA,** with the version in a comment. A tag is
  mutable.
- **Wait before you take a new release.** Set Renovate `minimumReleaseAge`, or
  uv `exclude-newer`. Most malicious releases are found and removed in a few
  days. A delay keeps them out of the lockfile.
- **Let Renovate keep the pins current.** Extend the shared preset in
  `renovate.json`: `github>ryanjdillon/workflows//renovate/default#v1`. It
  waits 7 days for a release, pins actions by digest, and updates the prek
  `rev:` pins and the lockfiles. See the README of `ryanjdillon/workflows`.
- **Audit known vulnerabilities** with `pip-audit`, `cargo deny`, or
  `osv-scanner`.
- **Audit the workflows** with `zizmor`.

## Shared checks

A check that many repos use lives in `ryanjdillon/workflows`. It has one
script, and an adapter for each environment:

| Environment | Adapter |
| --- | --- |
| GitHub Actions | A composite action: `uses: ryanjdillon/workflows/<check>@<sha> # vX.Y.Z` |
| prek (or pre-commit) | `.pre-commit-hooks.yaml`, with `rev: <sha> # frozen: vX.Y.Z` |
| Nix | The flake: a package, and a `lib` function for flake `checks` |

Each adapter runs the same script. Thus a local run and CI give the same
result. Pin the same release of `ryanjdillon/workflows` in CI and in the
prek `rev:`. The shared Renovate preset moves all these pins in one PR.
Renovate updates a `flake.lock` input from its branch, not from a release.
Thus use the Nix adapter only if the repo does not also pin a release.

`check-instructions` checks `SYSTEM.md` and a repo `AGENTS.md` against the
budget in `system-prompt.md`. It also makes sure that `AGENTS.md` ends with the
`# SYSTEM.md` section. See the README of `ryanjdillon/workflows` for the
configuration of each adapter.
