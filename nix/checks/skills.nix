{ inputs, pkgs, ... }:
pkgs.runCommand "check-skills" { nativeBuildInputs = [ pkgs.python3 ]; } ''
  python3 ${inputs.self}/scripts/validate-skills.py ${inputs.self}/skills
  touch "$out"
''
