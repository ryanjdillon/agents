{ ... }:
{
  projectRootFile = "flake.nix";

  programs = {
    nixfmt.enable = true;
    ruff-check.enable = true;
    ruff-format.enable = true;
    shfmt.enable = true;
  };

  settings.global.excludes = [
    "LICENSE"
    "*.md"
  ];
}
