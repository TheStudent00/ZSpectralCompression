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

- [evaluation_engine](node_0_2_1_0_evaluation_engine/CORE_0_2_1_0_evaluation_engine.md) — Rebuilds a Chebyshev basis at whatever length a token needs, caches it per length, and evaluates the token's coefficients against it.
- [signal_assembler](node_0_2_1_1_signal_assembler/CORE_0_2_1_1_signal_assembler.md) — Evaluates every token and concatenates the pieces back into one stream, in interval order.
- [latent_decoding](node_0_2_1_2_latent_decoding/CORE_0_2_1_2_latent_decoding.md) — The composition on the decode side: `decode_stream(latent_tokens, target_intervals)` runs the assembler over the engine and returns the flat stream, which [geometry_interpreter](../../../node_0_1_geometry/node_0_1_2_geometry_interpreter/CORE_0_1_2_geometry_interpreter.md) then folds back into N dimensions.

## definition

Tokens back to a one-dimensional stream.

Each token's coefficients are evaluated against a Chebyshev basis
generated at that token's own length, and the pieces are concatenated
in order. The upper and lower curves are averaged to a single output
curve, which is the point at which the interval representation
collapses to one value.
