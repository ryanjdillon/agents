#!/usr/bin/env bash
# Compose a repo's committed AGENTS.md (and agents.just) from the shared base
# plus the repo overlay. Both outputs are generated and must not be hand-edited.
set -euo pipefail

base="${AGENTS_BASE:-}"
overlay="AGENTS.repo.md"
out="AGENTS.md"
just_out="agents.just"
check=0
link_claude=1

usage() {
  cat <<'USAGE'
usage: compose [options]

  --base DIR       shared base checkout or store path (default: $AGENTS_BASE)
  --overlay FILE   repo overlay (default: AGENTS.repo.md)
  --out FILE       composed output (default: AGENTS.md)
  --just-out FILE  composed just recipes (default: agents.just)
  --check          verify the committed outputs are up to date; write nothing
  --no-claude-link do not symlink CLAUDE.md to the composed output
USAGE
}

while [ $# -gt 0 ]; do
  case "$1" in
  --base)
    base="$2"
    shift 2
    ;;
  --overlay)
    overlay="$2"
    shift 2
    ;;
  --out)
    out="$2"
    shift 2
    ;;
  --just-out)
    just_out="$2"
    shift 2
    ;;
  --check)
    check=1
    shift
    ;;
  --no-claude-link)
    link_claude=0
    shift
    ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    echo "compose: unknown argument: $1" >&2
    usage >&2
    exit 2
    ;;
  esac
done

if [ -z "$base" ]; then
  echo "compose: no base given; pass --base or set AGENTS_BASE" >&2
  exit 2
fi
if [ ! -f "$base/AGENTS.base.md" ]; then
  echo "compose: $base/AGENTS.base.md not found" >&2
  exit 2
fi
if [ ! -f "$overlay" ]; then
  echo "compose: overlay $overlay not found; copy it from $base/templates/AGENTS.repo.md" >&2
  exit 2
fi

# banner <open> <line-prefix> <close> <sources...>
banner() {
  local open="$1" prefix="$2" close="$3"
  shift 3
  [ -n "$open" ] && printf '%s\n' "$open"
  printf '%sGENERATED FILE — do not edit.\n' "$prefix"
  local source
  for source in "$@"; do
    printf '%sSource: %s\n' "$prefix" "$source"
  done
  printf '%sRegenerate with: just agents\n' "$prefix"
  [ -n "$close" ] && printf '%s\n' "$close"
}

render() {
  banner '<!--' '  ' '-->' "<base>/AGENTS.base.md (shared conventions)" \
    "$overlay (this repo)"
  printf '\n'
  cat "$base/AGENTS.base.md"
  printf '\n---\n\n'
  cat "$overlay"
}

render_just() {
  banner '' '# ' '' "<base>/agents.just"
  printf '\n'
  cat "$base/agents.just"
}

write_or_check() {
  local target="$1" renderer="$2" tmp
  tmp="$(mktemp)"
  trap 'rm -f "$tmp"' RETURN
  "$renderer" >"$tmp"

  if [ "$check" -eq 1 ]; then
    if ! diff -u "$target" "$tmp" >/dev/null 2>&1; then
      echo "compose: $target is out of date; run 'just agents'" >&2
      diff -u "$target" "$tmp" >&2 || true
      return 1
    fi
    return 0
  fi

  if [ -f "$target" ] && cmp -s "$target" "$tmp"; then
    return 0
  fi
  cp "$tmp" "$target"
  chmod 644 "$target"
  echo "compose: wrote $target"
}

status=0
write_or_check "$out" render || status=1
write_or_check "$just_out" render_just || status=1

if [ "$link_claude" -eq 1 ] && [ "$check" -eq 0 ]; then
  if [ ! -L CLAUDE.md ] || [ "$(readlink CLAUDE.md)" != "$out" ]; then
    if [ -e CLAUDE.md ] && [ ! -L CLAUDE.md ]; then
      echo "compose: CLAUDE.md exists and is not a symlink; leaving it alone" >&2
    else
      ln -sfn "$out" CLAUDE.md
      echo "compose: linked CLAUDE.md -> $out"
    fi
  fi
fi

exit "$status"
