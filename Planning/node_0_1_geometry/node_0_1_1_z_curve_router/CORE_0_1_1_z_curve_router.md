---
id: zspectral.geometry.z_curve_router
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: z_curve_router
    path: Planning/node_0_1_geometry/node_0_1_1_z_curve_router/CORE_0_1_1_z_curve_router.md
super_node:
    name: geometry
    path: ../CORE_0_1_geometry.md
sub_nodes: []
---

# CORE 0_1_1 — z_curve_router

## metadata

- **id:** zspectral.geometry.z_curve_router
- **level:** 2
- ## definition

Orders the cells of a padded canvas by Morton code, and reports where
each group of cells came from.

- `get_permutation` builds each cell's Z-code by interleaving the bits
  of its coordinates, one bit per axis per round, and returns the
  sort order.
- `sequence` returns the reordered flat stream **and** the bounding
  box, in original coordinates, of every group of `min_token_size`
  consecutive cells. Those boxes are what let a token be placed back
  in N dimensions.
- `unsequence` scatters a 1D stream back through the same
  permutation.

The ordering is the project's load-bearing geometric choice, measured
in [edit_locality](../../node_0_5_findings/node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md).
nerated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_1_geometry/CORE_0_1_geometry.md; the definition and `designation` are the owner's to
write.)*
