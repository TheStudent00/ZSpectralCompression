---
id: zspectral.codec.encoder.latent_encoding
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: latent_encoding
    path: Planning/node_0_2_codec/node_0_2_0_encoder/node_0_2_0_5_latent_encoding/CORE_0_2_0_5_latent_encoding.md
super_node:
    name: encoder
    path: ../CORE_0_2_0_encoder.md
sub_nodes: []
---

# CORE 0_2_0_5 — latent_encoding

## metadata

- **id:** zspectral.codec.encoder.latent_encoding
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

The composition of the five stages, and the only object the rest of
the codec holds.

`encode_stream(raw_1d_data, spatial_intervals)` runs mint, build,
walk, fit, mint-physics in that order and returns the token set. It
owns one instance of each stage and no state between calls.
