# The shareable half of this repo, isolated from the Nix plumbing so consumers
# only rebuild when the conventions themselves change.
{ inputs, pkgs, ... }:
pkgs.runCommand "agents-base" { } ''
  mkdir -p "$out"
  cp ${inputs.self}/AGENTS.base.md ${inputs.self}/agents.just "$out"/
  cp -r ${inputs.self}/docs ${inputs.self}/templates "$out"/
''
