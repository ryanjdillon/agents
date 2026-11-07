{
  description = "Reusable agent conventions: a shared AGENTS.md base, docs, and skills";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    blueprint = {
      url = "github:numtide/blueprint";
      inputs.nixpkgs.follows = "nixpkgs";
    };
    treefmt = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs:
    inputs.blueprint {
      inherit inputs;
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "aarch64-darwin"
      ];
      prefix = "nix/";
    };
}
