# Validated skill bundle. Exposes both `skills/` (for Nix skill sources and
# plugin consumers) and `.claude/skills/` (for a vanilla Claude install).
{ inputs, pkgs, ... }:
pkgs.runCommand "agents-skills"
  {
    nativeBuildInputs = [ pkgs.python3 ];
  }
  ''
    python3 ${inputs.self}/scripts/validate-skills.py ${inputs.self}/skills

    mkdir -p "$out/skills" "$out/.claude"
    cp -r ${inputs.self}/skills/. "$out/skills/"
    ln -s ../skills "$out/.claude/skills"
  ''
