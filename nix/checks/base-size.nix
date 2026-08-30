# The base is loaded in every session of every consuming repo, so its length is
# a recurring cost multiplied across all of them. Detail belongs in docs/, which
# agents read on demand.
{ inputs, pkgs, ... }:
pkgs.runCommand "check-base-size" { } ''
  limit=150
  count=$(wc -l <${inputs.self}/AGENTS.base.md)
  echo "AGENTS.base.md: $count lines (limit $limit)"
  if [ "$count" -gt "$limit" ]; then
    echo "error: the base has outgrown its budget." >&2
    echo "Move detail into docs/ and leave a pointer, rather than raising the limit." >&2
    exit 1
  fi
  touch "$out"
''
