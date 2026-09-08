---
id: zspectral.codec.decoder.latent_decoding
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: latent_decoding
    path: Planning/node_0_2_codec/node_0_2_1_decoder/node_0_2_1_2_latent_decoding/CORE_0_2_1_2_latent_decoding.md
super_node:
    name: decoder
    path: ../CORE_0_2_1_decoder.md
sub_nodes: []
---

# CORE 0_2_1_2 — latent_decoding

## metadata

- **id:** zspectral.codec.decoder.latent_decoding
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [decoder](../CORE_0_2_1_decoder.md)

## sub_nodes

*(none yet)*

## definition

The composition on the decode side: `decode_stream(latent_tokens,
target_intervals)` runs the assembler over the engine and returns the
flat stream, which
[geometry_interpreter](../../../node_0_1_geometry/node_0_1_2_geometry_interpreter/CORE_0_1_2_geometry_interpreter.md)
then folds back into N dimensions.
