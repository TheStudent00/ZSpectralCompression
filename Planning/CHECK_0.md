---
id: zspectral.check
---

# CHECK 0 — ZSpectralCompression

## completeness

    complete(node) = status is `settled` AND every sub-node complete

- `zspectral` is `draft`, so the root is not complete. Expected: the
  tree was opened 2026-09-08.

## the question this node answers

Does the tree describe the prototype that exists, rather than a
system someone would like to exist?

- Read `~/Programming/ZSpectralCompression/zspectral_compression.py`.
- Every class in it appears as a node in this tree, or is named in a
  node's `## design` with `realize: false`.
- No node in this tree names code that is not in that file. Where one
  does, it lives under [open_work](node_0_6_open_work/CORE_0_6_open_work.md)
  and says so.
