---
id: zspectral.findings.index_stream_entropy
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: finding
node:
    name: index_stream_entropy
    path: Planning/node_0_5_findings/node_0_5_2_index_stream_entropy/CORE_0_5_2_index_stream_entropy.md
super_node:
    name: findings
    path: ../CORE_0_5_findings.md
sub_nodes: []
---

# CORE 0_5_2 — index_stream_entropy

## metadata

- **id:** zspectral.findings.index_stream_entropy
- **level:** 2
- **status:** draft
- **designation:** finding
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [findings](../CORE_0_5_findings.md)

## sub_nodes

*(none yet)*

## definition

Whether the compressed output can be compressed again. Measured
2026-09-08 on the label streams produced by the codebook stage.

| stream | labels | H0 | H1 | after `xz -9` |
|---|---|---|---|---|
| smooth 1D | 32,768 | 7.41 | **0.85** | **1.50** |
| smooth 2D raw | 32,768 | 7.67 | **1.69** | **2.04** |
| Python source | 7,788 | 7.64 | 4.48 | 7.68 |
| English prose | 6,595 | 7.79 | 4.42 | 7.97 |

Bits per label. `H0` is the label histogram; `H1` is a label given the
previous label.

## what it says

the owner expected no further compression. There is a large amount, on
exactly the data the codec is good at.

- **The labels are individually near-uniform and sequentially highly
  correlated.** k-means balances its clusters, so the histogram looks
  random at 7.41 of 8 bits. But adjacent segments of a smooth signal
  have similar shapes and therefore the same or neighbouring label,
  which a first-order model sees immediately: 0.85 bits.
- `xz` recovers most of it — 8 bits per label down to 1.50, a further
  factor of 5.3 — and
  [metrics](../../node_0_4_evaluation/node_0_4_2_metrics/CORE_0_4_2_metrics.md)
  currently counts labels at a flat 1 byte each, so the prototype's
  reported ratios understate what the format can reach.
- On symbol data there is nothing to recover, consistent with the
  codec having no purchase on it in the first place.

## the general point

"Already compressed" is only ever true relative to a model. An output
whose symbols look uniform can still carry order in its *sequence*,
and that is a different model class from the one the codec applied.
This is why image and video standards entropy-code their mode and
index streams rather than emitting them raw.
