---
id: zspectral.codec.encoder.physics_minter
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: physics_minter
    path: Planning/node_0_2_codec/node_0_2_0_encoder/node_0_2_0_4_physics_minter/CORE_0_2_0_4_physics_minter.md
super_node:
    name: encoder
    path: ../CORE_0_2_0_encoder.md
sub_nodes: []
---

# CORE 0_2_0_4 — physics_minter

## metadata

- **id:** zspectral.codec.encoder.physics_minter
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

Stage 5. Attaches the kinematic metadata to the finished tokens:
mass (a constant 1), length (the volume of the token's bounding box),
and confidence (the reciprocal of the gap between the upper and lower
curves).

Unverified: none of these three reach the stored payload.
[zspectral_compressor](../../../node_0_3_container/node_0_3_2_zspectral_compressor/CORE_0_3_2_zspectral_compressor.md)
stores labels, `c0`, the codebook and the topology, and nothing else.
This stage exists for the algebra half of the project rather than for
compression.
