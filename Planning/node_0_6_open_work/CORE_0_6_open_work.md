---
id: zspectral.open_work
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: open_work
    path: Planning/node_0_6_open_work/CORE_0_6_open_work.md
super_node:
    name: zspectral
    path: ../CORE_0.md
sub_nodes:
    - name: lossless_mode
      path: node_0_6_0_lossless_mode/CORE_0_6_0_lossless_mode.md
    - name: stride_discovery
      path: node_0_6_1_stride_discovery/CORE_0_6_1_stride_discovery.md
    - name: chunker_framing
      path: node_0_6_2_chunker_framing/CORE_0_6_2_chunker_framing.md
---

# CORE 0_6 — open_work

## metadata

- **id:** zspectral.open_work
- **level:** 1
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [zspectral](../CORE_0.md)

## sub_nodes

- [lossless_mode](node_0_6_0_lossless_mode/CORE_0_6_0_lossless_mode.md) — Establish what the real pyramid costs at `merge_threshold = 0`, on `smooth_1d` and `smooth_2d_raw`.
- [stride_discovery](node_0_6_1_stride_discovery/CORE_0_6_1_stride_discovery.md) — Recover the hidden dimensionality of a flat byte stream before encoding it, and reshape accordingly.
- [chunker_framing](node_0_6_2_chunker_framing/CORE_0_6_2_chunker_framing.md) — Decide whether the project's centre is the codec or the addressing scheme.

## definition

Work the findings point at. Nothing here is implemented; each node
names the measurement that would settle it.

## why these three and not others

Each follows from one measured result rather than from a preference:

- **lossless_mode** — the harness cannot separate "the basis does not
  fit" from "the fixed window is too crude". Running the real pyramid
  at `merge_threshold = 0` separates them, and that one number decides
  whether lossless is worth building.
- **stride_discovery** — a stride search recovered the true row width
  of a 2D field from a flat byte stream with no metadata, and
  correctly reported "no structure" for text. Nothing in the prototype
  does this; it is the part of the N-dimensional claim that generic
  compressors cannot reach.
- **chunker_framing** — the edit-locality result stands on its own
  without any compression at all. Whether that becomes the project's
  centre is a question about what this is for, and therefore the owner's.
