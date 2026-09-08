---
id: zspectral.codec.decoder.evaluation_engine
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: evaluation_engine
    path: Planning/node_0_2_codec/node_0_2_1_decoder/node_0_2_1_0_evaluation_engine/CORE_0_2_1_0_evaluation_engine.md
super_node:
    name: decoder
    path: ../CORE_0_2_1_decoder.md
sub_nodes: []
---

# CORE 0_2_1_0 — evaluation_engine

## metadata

- **id:** zspectral.codec.decoder.evaluation_engine
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

Rebuilds a Chebyshev basis at whatever length a token needs, caches
it per length, and evaluates the token's coefficients against it.

The cache is what makes decoding cheap for a segmentation of mixed
lengths: the number of distinct lengths is small — they are all
powers of two times `min_patch_size` — even when the number of tokens
is large.
