---
id: zspectral.codec.decoder
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: decoder
    path: Planning/node_0_2_codec/node_0_2_1_decoder/CORE_0_2_1_decoder.md
super_node:
    name: codec
    path: ../CORE_0_2_codec.md
sub_nodes:
    - name: evaluation_engine
      path: node_0_2_1_0_evaluation_engine/CORE_0_2_1_0_evaluation_engine.md
    - name: signal_assembler
      path: node_0_2_1_1_signal_assembler/CORE_0_2_1_1_signal_assembler.md
    - name: latent_decoding
      path: node_0_2_1_2_latent_decoding/CORE_0_2_1_2_latent_decoding.md
---

# CORE 0_2_1 — decoder

## metadata

- **id:** zspectral.codec.decoder
- **level:** 2
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [codec](../CORE_0_2_codec.md)

## sub_nodes

*(rebuilt by the generator)*

## definition

Tokens back to a one-dimensional stream.

Each token's coefficients are evaluated against a Chebyshev basis
generated at that token's own length, and the pieces are concatenated
in order. The upper and lower curves are averaged to a single output
curve, which is the point at which the interval representation
collapses to one value.
