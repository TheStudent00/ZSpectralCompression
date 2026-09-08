---
id: zspectral.codec.encoder.pyramid_walker
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: pyramid_walker
    path: Planning/node_0_2_codec/node_0_2_0_encoder/node_0_2_0_2_pyramid_walker/CORE_0_2_0_2_pyramid_walker.md
super_node:
    name: encoder
    path: ../CORE_0_2_0_encoder.md
sub_nodes: []
---

# CORE 0_2_0_2 — pyramid_walker

## metadata

- **id:** zspectral.codec.encoder.pyramid_walker
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [encoder](../CORE_0_2_0_encoder.md)

## sub_nodes

*(none yet)*

## definition

Stage 3. Descends the pyramid from its single root, breadth-first,
carrying a boolean mask of which nodes are still being considered.

At each node: if its inflated error is under `error_threshold`, keep
it whole and stop descending; otherwise split into its two children
and continue. What survives is the segmentation — a set of intervals
of mixed lengths, fine where the data is complicated and coarse where
it is smooth.

**This is the only place the lossy/lossless decision is made.** The
threshold is the codec's single knob. The mask is carried on the
compute device rather than tested in Python, which its docstring
records as the reason for the design: "eliminate CPU sync overhead".
