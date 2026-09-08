---
id: zspectral.open_work.stride_discovery
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: stride_discovery
    path: Planning/node_0_6_open_work/node_0_6_1_stride_discovery/CORE_0_6_1_stride_discovery.md
super_node:
    name: open_work
    path: ../CORE_0_6_open_work.md
sub_nodes: []
---

# CORE 0_6_1 — stride_discovery

## metadata

- **id:** zspectral.open_work.stride_discovery
- **level:** 2
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [open_work](../CORE_0_6_open_work.md)

## sub_nodes

*(none yet)*

## definition

Recover the hidden dimensionality of a flat byte stream before
encoding it, and reshape accordingly.

## the result this rests on

A stride search — for each candidate stride, predict each byte from
its left and upper neighbours at that stride, keep the stride with the
lowest residual entropy — recovered **1000**, the true row width, from
a flat 1 MB stream of a 1000x1000 field with no metadata. It reported
stride 1 for C++ source, Python source, English prose and an ELF
binary, correctly saying "this is one-dimensional".

At the recovered stride that file drops from 7.44 to 1.26 bits per
byte under a two-dimensional predictor.

## why it belongs to this project rather than to a general compressor

General-purpose compressors have the machinery and not the discovery:
`xz --delta=dist=N` applies exactly this, and `N` must be supplied by
hand. A format that already thinks in N dimensions can search for the
dimension and then use it, which a 1D format cannot.

## scope

- Search cost and false-positive rate on real files are unmeasured.
- Nothing in the prototype does any of this; the shape is supplied by
  the caller as `task_metadata["shape"]`.
