{ pkgs, ... }:
pkgs.mkShell {
  packages = [
    pkgs.just
    pkgs.python3
    pkgs.shellcheck
  ];
}
