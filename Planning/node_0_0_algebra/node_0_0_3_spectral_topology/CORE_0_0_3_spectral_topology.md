---
id: zspectral.algebra.spectral_topology
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: spectral_topology
    path: Planning/node_0_0_algebra/node_0_0_3_spectral_topology/CORE_0_0_3_spectral_topology.md
super_node:
    name: algebra
    path: ../CORE_0_0_algebra.md
sub_nodes: []
---

# CORE 0_0_3 — spectral_topology

## metadata

- **id:** zspectral.algebra.spectral_topology
- **level:** 2
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [algebra](../CORE_0_0_algebra.md)

## sub_nodes

*(none yet)*

## definition

Changing how many segments a spline is expressed in, without changing
the function it denotes.

One 4x8 split matrix carries a single segment to two; its
pseudo-inverse carries two back to one. Any power-of-two ratio is
built by composing block-diagonal copies of those two recursively,
and cached per ratio.

**This is the only part of the algebra the codec calls.**
`upsample_to_match` aligns two operands, and
`enforce_left_complexity` restores the left operand's segment count
after an operation. The pyramid's merge step is
`enforce_left_complexity(paired, target_s=1)`.
