---
id: zspectral.container
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: container
    path: Planning/node_0_3_container/CORE_0_3_container.md
super_node:
    name: zspectral
    path: ../CORE_0.md
sub_nodes:
    - name: topology_serializer
      path: node_0_3_0_topology_serializer/CORE_0_3_0_topology_serializer.md
    - name: vector_quantizer
      path: node_0_3_1_vector_quantizer/CORE_0_3_1_vector_quantizer.md
    - name: zspectral_compressor
      path: node_0_3_2_zspectral_compressor/CORE_0_3_2_zspectral_compressor.md
---

# CORE 0_3 — container

## metadata

- **id:** zspectral.container
- **level:** 1
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [zspectral](../CORE_0.md)

## sub_nodes

- [topology_serializer](node_0_3_0_topology_serializer/CORE_0_3_0_topology_serializer.md) — Encodes the segment lengths as a pre-order bitmask over a binary subdivision of the total length.
- [vector_quantizer](node_0_3_1_vector_quantizer/CORE_0_3_1_vector_quantizer.md) — Replaces each token's three shape coefficients with an index into a learned codebook.
- [zspectral_compressor](node_0_3_2_zspectral_compressor/CORE_0_3_2_zspectral_compressor.md) — Assembles a payload and takes one apart.

## definition

The stored form: what a compressed payload actually contains, and how
the token set is reduced to bytes.

## design

A payload holds four things, and only the last two carry the signal:

| part | shape | cost |
|---|---|---|
| `topology_bytes` | one bit per node of the segmentation tree | 1 bit per segment plus 1 per internal node |
| `codebook` | K entries of 3 float32 | K x 12 bytes, amortised over the whole payload |
| `labels` | one index per token | 1 byte per token at K <= 256 |
| `c0_quantized` | the DC term per token | 1 byte per token |

The separation of `c0` from the other three coefficients is the design
decision worth naming: the mean level of a segment varies over the
whole range and is quantised directly, while the *shape* of a segment
repeats across a data set and is therefore worth a codebook. That is
why one is a uint8 and the other is an index.

**The intervals are not stored.** They are recovered by replaying the
binary-tree bitmask against the total length, which is what makes
`topology_bytes` cheap enough to be an afterthought rather than the
dominant cost.

## measured, 2026-09-08

The codebook shifts cost rather than removing it — see
[codebook_tradeoff](../node_0_5_findings/node_0_5_1_codebook_tradeoff/CORE_0_5_1_codebook_tradeoff.md).
Storing an index instead of four coefficients is cheaper by roughly
2.3 bits per byte on text, and *more expensive* on smooth data,
because the residual from a codebook entry is larger than the residual
from the segment's own fit.
