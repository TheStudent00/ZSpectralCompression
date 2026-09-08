---
id: zspectral.evaluation
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: evaluation
    path: Planning/node_0_4_evaluation/CORE_0_4_evaluation.md
super_node:
    name: zspectral
    path: ../CORE_0.md
sub_nodes:
    - name: vision_geometry_config
      path: node_0_4_0_vision_geometry_config/CORE_0_4_0_vision_geometry_config.md
    - name: rate_distortion_optimizer
      path: node_0_4_1_rate_distortion_optimizer/CORE_0_4_1_rate_distortion_optimizer.md
    - name: metrics
      path: node_0_4_2_metrics/CORE_0_4_2_metrics.md
---

# CORE 0_4 — evaluation

## metadata

- **id:** zspectral.evaluation
- **level:** 1
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [zspectral](../CORE_0.md)

## sub_nodes

*(rebuilt by the generator)*

## definition

How the codec is configured, what is counted when it runs, and the
sweep that trades size against error.

## design

- The configuration is one object holding `min_patch_size`,
  `merge_threshold`, and the Chebyshev basis matrices derived from
  the first of those. Everything else is derived.
- `calculate_metrics` counts bytes analytically from the payload
  parts rather than measuring a serialised file, and assumes one byte
  per input sample. Both assumptions hold for 8-bit image data and
  for nothing else, which is a limitation to record rather than a bug.
- The rate-distortion sweep varies the threshold and reports mean
  squared error against payload size.

## limitation to carry forward

There is no test suite. The `test_*` and `visualize_*` functions in
the prototype are demonstrations that print and plot; nothing asserts.
Every CHECK in this tree is a by-hand question for that reason.
