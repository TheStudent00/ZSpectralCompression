---
id: zspectral.evaluation.vision_geometry_config
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: vision_geometry_config
    path: Planning/node_0_4_evaluation/node_0_4_0_vision_geometry_config/CORE_0_4_0_vision_geometry_config.md
super_node:
    name: evaluation
    path: ../CORE_0_4_evaluation.md
sub_nodes: []
---

# CORE 0_4_0 — vision_geometry_config

## metadata

- **id:** zspectral.evaluation.vision_geometry_config
- **lev## definition

The configuration used for image runs: `min_patch_size = 4`,
`merge_threshold = 0.02`, and the 4x4 Chebyshev basis matrix `A`
evaluated at four equispaced points with its pseudo-inverse.

`min_patch_size = 4` with a degree-3 basis means the leaf fit is
square and therefore exact — four coefficients through four points.
All approximation in the codec comes from merging, never from the
leaves.

The prototype's comment on the threshold states the intent plainly:
"Allow up to 2% error to trigger topological merging (compression!)".
nding — generated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_4_evaluation/CORE_0_4_evaluation.md; the definition and `designation` are the owner's to
write.)*
