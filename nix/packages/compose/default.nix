{
  inputs,
  flake,
  pkgs,
  ...
}:
let
  base = flake.packages.${pkgs.stdenv.hostPlatform.system}.base;
in
pkgs.writeShellApplication {
  name = "agents-compose";
  runtimeInputs = [ pkgs.diffutils ];
  text = ''
    export AGENTS_BASE="''${AGENTS_BASE:-${base}}"
    exec ${inputs.self}/scripts/compose.sh "$@"
  '';
}
