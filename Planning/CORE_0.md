---
id: zspectral
level: 0
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: zspectral
    path: Planning/CORE_0.md
    repo: ZSpectralCompression
    remote: https://github.com/TheStudent00/ZSpectralCompression.git
super_node: null
sub_nodes:
    - name: algebra
      path: node_0_0_algebra/CORE_0_0_algebra.md
    - name: geometry
      path: node_0_1_geometry/CORE_0_1_geometry.md
    - name: codec
      path: node_0_2_codec/CORE_0_2_codec.md
    - name: container
      path: node_0_3_container/CORE_0_3_container.md
    - name: evaluation
      path: node_0_4_evaluation/CORE_0_4_evaluation.md
    - name: findings
      path: node_0_5_findings/CORE_0_5_findings.md
    - name: open_work
      path: node_0_6_open_work/CORE_0_6_open_work.md
---

# CORE 0 — ZSpectralCompression

## metadata

- **id:** zspectral
- **level:** 0
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

- [algebra](node_0_0_algebra/CORE_0_0_algebra.md) — The value type the whole project operates on — a piecewise Chebyshev spline carrying an upper and a lower bound at every point — and the arithmetic closed over it.
- [geometry](node_0_1_geometry/CORE_0_1_geometry.md) — The boundary between data of any dimension and the one-dimensional sequence everything downstream operates on, together with the inverse.
- [codec](node_0_2_codec/CORE_0_2_codec.md) — The conversion between a one-dimensional stream of samples and a set of variable-length tokens, each token one Chebyshev polynomial over one interval.
- [container](node_0_3_container/CORE_0_3_container.md) — The stored form: what a compressed payload actually contains, and how the token set is reduced to bytes.
- [evaluation](node_0_4_evaluation/CORE_0_4_evaluation.md) — How the codec is configured, what is counted when it runs, and the sweep that trades size against error.
- [findings](node_0_5_findings/CORE_0_5_findings.md) — What has been measured about this representation, on what data, with what harness — and which claims the measurements do not support.
- [open_work](node_0_6_open_work/CORE_0_6_open_work.md) — Work the findings point at.

## definition

A representation that describes data of any dimension as a set of
variable-length polynomial segments laid along a space-filling curve,
addressed by a merge hierarchy. Compression is one use of that
representation; local addressability is the other.

## the two things this project is

Stated as two because the measurements in [findings](node_0_5_findings/CORE_0_5_findings.md)
separate them, and conflating them is what made the prototype hard to
judge.

- **A codec.** Fit each segment with a degree-3 Chebyshev polynomial,
  merge adjacent segments wherever the fit error stays under a
  threshold, quantise the resulting coefficient vectors against a
  learned codebook. Measured: strong on smooth sampled signals, a
  loss on symbol data such as text and compiled code.
- **An addressing scheme.** Because segments are independent and laid
  along a Z-order curve, a change to a compact region in N dimensions
  touches a small, contiguous set of segments. Measured: a 64x64 edit
  in a 1024x1024 field touches 1 chunk under Z-order against 16 under
  row order.

## provenance

The 1,568-line prototype at
`~/Programming/ZSpectralCompression/zspectral_compression.py` came
first; this plan was reverse-engineered from it on 2026-09-08 at the owner's
request, the prototype having been built with earlier models. Where
the plan and the prototype disagree, the prototype is the fact and the
plan is the defect, until the owner settles otherwise.

## open at the root

- This tree carries `super_node: null`. Whether the project hangs
  under `~/Programming/PseudoCoupHQ/Planning/node_0_0_projects/` is a
  level-0 question and therefore the owner's, per PROTOCOL §2.
