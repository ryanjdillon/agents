# Module organisation

Ousterhout's deep-module principle, applied to both source and docs: **a small,
narrow interface with as much depth behind it as the domain actually has.**

The goal is that a contributor — or an agent — can load exactly one module to do
exactly one job, without dragging in unrelated context.

## Source

One unit per domain, and that unit is the narrow door. The internals behind it
can be as deep as the feature requires. Do not spread a single domain across
many files until the file itself becomes the bottleneck; file count is not a
measure of modularity.

## Docs

**One topic per file.** Each file stands alone: an entry sentence stating
audience and scope, full coverage of that topic, and cross-links to siblings
where genuinely useful — but **no duplicated content**.

The failure mode this prevents: opening five files to assemble one answer. If
looking up a single subject requires stitching together fragments, the split is
wrong.

When a topic outgrows one file, promote it to a coherent subdirectory with its
own index — not to ad-hoc cross-references scattered across the tree.

## Categorisation

Split docs by **audience** first. When adding a doc, pick the
audience-narrowest home that fits. Only genuinely cross-audience material
belongs at the top level.
