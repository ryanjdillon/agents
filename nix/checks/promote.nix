# Unit tests for scripts/promote.py. CI runs the same command without Nix.
{ inputs, pkgs, ... }:
pkgs.runCommand "check-promote" { nativeBuildInputs = [ pkgs.python3 ]; } ''
  cp -r ${inputs.self}/scripts scripts
  python3 -m unittest discover -s scripts
  touch "$out"
''
