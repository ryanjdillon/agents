# The shareable half of this repo, isolated from the Nix plumbing so a tool
# config that loads SYSTEM.md or WORKFLOW.md only rebuilds when the rules
# change. Each consumer joins the files that it needs.
{ inputs, pkgs, ... }:
pkgs.runCommand "agents-base" { } ''
  mkdir -p "$out"
  cp ${inputs.self}/SYSTEM.md ${inputs.self}/WORKFLOW.md "$out"/
  cp -r ${inputs.self}/docs ${inputs.self}/templates "$out"/
''
