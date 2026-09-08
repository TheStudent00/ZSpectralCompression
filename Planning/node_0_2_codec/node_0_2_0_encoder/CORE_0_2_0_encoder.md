---
id: zspectral.codec.encoder
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: encoder
    path: Planning/node_0_2_codec/node_0_2_0_encoder/CORE_0_2_0_encoder.md
super_node:
    name: codec
    path: ../CORE_0_2_codec.md
sub_nodes:
    - name: base_leaf_minter
      path: node_0_2_0_encoder_0_base_leaf_minter/CORE_0_2_0_encoder_0_base_## definition

Raw one-dimensional stream to a set of variable-length polynomial
tokens, in five stages.

The stages run in a fixed order and each has its own node: mint fixed
leaves, build the merge pyramid, descend it against the error
threshold, re-fit the surviving segments at their true lengths, then
attach the kinematic metadata.

The re-fit is the stage most easily mistaken for redundant. Merged
coefficients are a projection of a projection and drift from the
data; the final fit is against the raw stream.
_2_pyramid_walker/CORE_0_2_0_encoder_2_pyramid_walker.md
    - name: dual_curve_fitter
      path: node_0_2_0_encoder_3_dual_curve_fitter/CORE_0_2_0_encoder_3_dual_curve_fitter.md
    - name: physics_minter
      path: node_0_2_0_encoder_4_physics_minter/CORE_0_2_0_encoder_4_physics_minter.md
    - name: latent_encoding
      path: node_0_2_0_encoder_5_latent_encoding/CORE_0_2_0_encoder_5_latent_encoding.md
---

# CORE 0_2_0 — encoder

## metadata

- **id:** zspectral.codec.encoder
- **level:** 2
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [codec](../CORE_0_2_codec.md)

## sub_nodes

- [base_leaf_minter](node_0_2_0_0_base_leaf_minter/CORE_0_2_0_0_base_leaf_minter.md)

## definition

*(pending — generated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_2_codec/CORE_0_2_codec.md; the definition and `designation` are the owner's to
write.)*
