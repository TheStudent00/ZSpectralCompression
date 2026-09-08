---
id: zspectral.evaluation.rate_distortion_optimizer
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: rate_distortion_optimizer
    path: Planning/node_0_4_evaluation/node_0_4_1_rate_distortion_optimizer/CORE_0_4_1_rate_distortion_optimizer.md
super_node:
    name: evaluation
    path: ../CORE_0_4_evaluation.md
sub_nodes: []
---

# CORE 0_4_1 — rate_distortion_optimizer

## metadata

- **id:** zspectral.evaluation.rate_distortion_optimizer
- **## definition

Sweeps `merge_threshold` and reports, per setting, the payload size
against the mean squared error of the reconstruction.

It is the node that makes the lossy/lossless question concrete: the
sweep's left endpoint is `merge_threshold = 0`, and what the codec
costs there is the measurement
[lossless_mode](../../node_0_6_open_work/node_0_6_0_lossless_mode/CORE_0_6_0_lossless_mode.md)
asks for.
(pending — generated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_4_evaluation/CORE_0_4_evaluation.md; the definition and `designation` are the owner's to
write.)*
