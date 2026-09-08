---
id: zspectral.codec.interface
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: interface
    path: Planning/node_0_2_codec/node_0_2_2_interface/CORE_0_2_2_interface.md
super_node:
    name: codec
    path: ../CORE_0_2_codec.md
sub_nodes: []
---

# CORE 0_2_2 — interface

## metadata

- **id:** zspectral.codec.interface
- **level:** 2
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [codec](../CORE_0_2_codec.md)

## sub_nodes

*(none yet)*

## definition

The thin composition: `encode` runs the geometry boundary then
[encoder](../node_0_2_0_encoder/CORE_0_2_0_encoder.md); `decode` runs
[decoder](../node_0_2_1_decoder/CORE_0_2_1_decoder.md) then the
inverse boundary.

It holds one config object and no logic of its own. It is a node
rather than a `realize: false` entry because it is the surface
[zspectral_compressor](../../node_0_3_container/node_0_3_2_zspectral_compressor/CORE_0_3_2_zspectral_compressor.md)
calls, and a reader looking for "where does compression start" lands
here.
