# The shareable half of this repo, isolated from the Nix plumbing so a tool
# config that loads SYSTEM.md only rebuilds when the rules themselves change.
{ inputs, pkgs, ... }:
pkgs.runCommand "agents-base" { } ''
  mkdir -p "$out"
  cp ${inputs.self}/SYSTEM.md "$out"/
  cp -r ${inputs.self}/docs ${inputs.self}/templates "$out"/
''
