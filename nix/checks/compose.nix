# Compose against the overlay template in a sandbox: proves the script runs and
# produces a non-empty AGENTS.md without a repo checkout.
{
  inputs,
  flake,
  pkgs,
  ...
}:
let
  base = flake.packages.${pkgs.stdenv.hostPlatform.system}.base;
in
pkgs.runCommand "check-compose" { nativeBuildInputs = [ pkgs.diffutils ]; } ''
  cp ${base}/templates/AGENTS.repo.md AGENTS.repo.md
  AGENTS_BASE=${base} bash ${inputs.self}/scripts/compose.sh --no-claude-link
  grep -q "GENERATED FILE" AGENTS.md
  grep -q "GENERATED FILE" agents.just
  AGENTS_BASE=${base} bash ${inputs.self}/scripts/compose.sh --check --no-claude-link
  touch "$out"
''
