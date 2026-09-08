---
id: zspectral.codec.encoder.base_leaf_minter
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: base_leaf_minter
    path: Planning/node_0_2_codec/node_0_2_0_encoder/node_0_2_0_0_base_leaf_minter/CORE_0_2_0_0_base_leaf_minter.md
super_node:
    name: encoder
    path: ../CORE_0_2_0_encoder.md
sub_nodes: []
---

# CORE 0_2_0_0 — base_leaf_minter

## metadata

- **id:** zspectral.codec.encoder.base_leaf_minter
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

Stage 1. Cuts the flat stream into fixed patches of `min_patch_size`
samples and projects each onto the Chebyshev basis, recording two
error figures per patch: the root-mean-square residual and the
largest absolute residual.

At `min_patch_size = 4` with a degree-3 basis the projection is
square, so **the leaf fit is exact**. Every approximation in the codec
enters later, at the merge. The two error figures start at zero and
are inflated on the way up the pyramid.

It also widens each coefficient vector into the dual (lower, upper)
form the rest of the algebra expects, initially with both bounds
equal.
