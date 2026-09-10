---
id: zspectral.findings
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: findings
    path: Planning/node_0_5_findings/CORE_0_5_findings.md
super_node:
    name: zspectral
    path: ../CORE_0.md
sub_nodes:
    - name: one_dimensional_behaviour
      path: node_0_5_0_one_dimensional_behaviour/CORE_0_5_0_one_dimensional_behaviour.md
    - name: codebook_tradeoff
      path: node_0_5_1_codebook_tradeoff/CORE_0_5_1_codebook_tradeoff.md
    - name: index_stream_entropy
      path: node_0_5_2_index_stream_entropy/CORE_0_5_2_index_stream_entropy.md
    - name: edit_locality
      path: node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md
    - name: leaf_projection_defect
      path: node_0_5_4_leaf_projection_defect/CORE_0_5_4_leaf_projection_defect.md
    - name: break_even_guarantee
      path: node_0_5_5_break_even_guarantee/CORE_0_5_5_break_even_guarantee.md
---

# CORE 0_5 — findings

## metadata

- **id:** zspectral.findings
- **level:** 1
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [zspectral](../CORE_0.md)

## sub_nodes

- [one_dimensional_behaviour](node_0_5_0_one_dimensional_behaviour/CORE_0_5_0_one_dimensional_behaviour.md) — What the polynomial basis does to one-dimensional data that is not a sampled signal.
- [codebook_tradeoff](node_0_5_1_codebook_tradeoff/CORE_0_5_1_codebook_tradeoff.md) — What the k-means codebook does to the cost, measured 2026-09-08 at K = 256 against the same files.
- [index_stream_entropy](node_0_5_2_index_stream_entropy/CORE_0_5_2_index_stream_entropy.md) — Whether the compressed output can be compressed again.
- [edit_locality](node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md) — What the Z-order traversal is worth when data changes.
- [leaf_projection_defect](node_0_5_4_leaf_projection_defect/CORE_0_5_4_leaf_projection_defect.md) — The mechanism the codec compresses by had never run.
- [break_even_guarantee](node_0_5_5_break_even_guarantee/CORE_0_5_5_break_even_guarantee.md) — Whether ZSC ever costs more than storing the bytes raw.

## definition

What has been measured about this representation, on what data, with
what harness — and which claims the measurements do not support.

## the four results in one line each

- **On symbol data the polynomial fit raises entropy.** C++ source
  goes from 5.17 to 5.88 bits per byte after fitting. The transform
  destroys structure rather than concentrating it.
- **On smooth sampled data it wins large.** A signal whose byte
  histogram carries 7.56 of 8 bits drops to 0.32 bits per byte.
- **The codebook shifts cost between coefficients and residual**, and
  which way it shifts depends on the data.
- **The merge had never run.** `_BaseLeafMinter._project` was missing a
  transpose, so every pyramid error was nonsense and the walker kept
  nothing above the leaves at any threshold. Fixed 2026-09-08; smooth
  data went from 1.52x to 17.03x.
- **The index stream is far from incompressible.** Its symbols look
  uniform and its *sequence* does not: 7.41 bits per label by
  histogram, 0.85 conditioned on the previous label.

## the harness, stated because it bounds every number above

Not the prototype. A degree-3 Chebyshev fit over fixed 8-sample
windows, integer coefficients, exact residual, written in pure Python
and run in the Airlock `sandbox-runner` container on 2026-09-08.

- The prototype merges segments adaptively, so a smooth region becomes
  one long token and the coefficient cost amortises. The harness pays
  four coefficients per eight bytes always.
- Therefore **every total-cost number here is a floor on the
  prototype, not a ceiling.** The per-window residual entropies are a
  fair reading of whether the basis fits the data at all; the totals
  are not a fair reading of the prototype's ratio.
- Full record: `~/Programming/PUBLIC/ZSpectralCompression/DevComms/log_001_one_dimensional_measurements.md`.
