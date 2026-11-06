# The budget for SYSTEM.md and this repo's AGENTS.md. The check is defined in
# ryanjdillon/workflows; CI runs the same script through its action.
{ inputs, pkgs, ... }:
inputs.workflows.lib.checkInstructions {
  inherit pkgs;
  files = [
    "${inputs.self}/SYSTEM.md"
    "${inputs.self}/AGENTS.md"
  ];
}
