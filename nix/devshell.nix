{ pkgs, ... }:
pkgs.mkShell {
  packages = [
    pkgs.just
    pkgs.prek
    pkgs.python3
    pkgs.shellcheck
  ];
}
