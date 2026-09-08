---
id: zspectral.codec.encoder.topological_pyramid
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: topological_pyramid
    path: Planning/node_0_2_codec/node_0_2_0_encoder/node_0_2_0_1_topological_pyramid/CORE_0_2_0_1_topological_pyramid.md
super_node:
    name: encoder
    path: ../CORE_0_2_0_encoder.md
sub_nodes: []
---

# CORE 0_2_0_1 — topological_pyramid

## metadata

- **id:** zspectral.codec.encoder.topological_pyramid
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

Stage 2. Repeatedly pairs adjacent tokens and merges each pair into
one, until a single token spans the whole stream. The result is the
full hierarchy, kept — not just its top.

Per merge:

- the coefficients are merged by `enforce_left_complexity(paired,
  target_s=1)`, the algebra's own two-segments-to-one operation;
- the **distortion** is the largest absolute difference between the
  original pair and the merged token re-expanded back to two
  segments — how much the merge lied;
- the error figures are inflated by that distortion, with constants
  `0.52` on the RMS term and `0.72` on the maximum term. Unverified:
  neither constant is derived anywhere in the prototype.
- the interval is the union of the pair's bounding boxes.

Keeping every level is what makes the descent in stage 3 possible,
and it is also what makes this a hash-hierarchy candidate — see
[chunker_framing](../../../node_0_6_open_work/node_0_6_2_chunker_framing/CORE_0_6_2_chunker_framing.md).
