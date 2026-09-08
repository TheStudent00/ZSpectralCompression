---
id: zspectral.evaluation.metrics
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: metrics
    path: Planning/node_0_4_evaluation/node_0_4_2_metrics/CORE_0_4_2_metrics.md
super_node:
    name: evaluation
    path: ../CORE_0_4_evaluation.md
sub_nodes: []
---

# CORE 0_4_2 — metrics

## metadata

- **id:** zspectral.evaluation.metrics
- **level:** 2
- **st## definition

Counts payload bytes analytically from the parts rather than
measuring a serialised file: labels at 1 or 2 bytes per token, `c0`
at 1 byte per token, the codebook at `K * 3 * 4` bytes, plus the
topology byte tensor.

**Two assumptions, both worth carrying forward as limitations.**
`raw_bytes = raw_pixels * 1` assumes one byte per input sample, which
holds for 8-bit image data and nothing else. And no entropy coder is
applied to the labels before counting, which
[index_stream_entropy](../../node_0_5_findings/node_0_5_2_index_stream_entropy/CORE_0_5_2_index_stream_entropy.md)
measures as leaving a large amount on the table.
ated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_4_evaluation/CORE_0_4_evaluation.md; the definition and `designation` are the owner's to
write.)*
