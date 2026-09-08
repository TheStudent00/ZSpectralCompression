---
id: zspectral.codec.encoder.dual_curve_fitter
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: dual_curve_fitter
    path: Planning/node_0_2_codec/node_0_2_0_encoder/node_0_2_0_3_dual_curve_fitter/CORE_0_2_0_3_dual_curve_fitter.md
super_node:
    name: encoder
    path: ../CORE_0_2_0_encoder.md
sub_nodes: []
---

# CORE 0_2_0_3 — dual_curve_fitter

## metadata

- **id:** zspectral.codec.encoder.dual_curve_fitter
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

Stage 4. Re-fits every surviving segment against the raw stream, at
that segment's true length.

Segments are grouped by length so that all segments of one length are
fitted in a single batched matrix multiplication, with the Chebyshev
basis and its pseudo-inverse built once per length.

The re-fit is not redundant. The coefficients coming out of stage 2
are a projection of a projection and have drifted; these are fitted
directly to the data. It is also where a variable-length segment
first gets coefficients that mean anything at its own scale.
