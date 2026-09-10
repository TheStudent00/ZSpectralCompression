---
id: zspectral.findings.leaf_projection_defect
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: finding
node:
    name: leaf_projection_defect
    path: Planning/node_0_5_findings/node_0_5_4_leaf_projection_defect/CORE_0_5_4_leaf_projection_defect.md
super_node:
    name: findings
    path: ../CORE_0_5_findings.md
sub_nodes: []
---

# CORE 0_5_4 — leaf_projection_defect

## metadata

- **id:** zspectral.findings.leaf_projection_defect
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

The mechanism the codec compresses by had never run. Found 2026-09-08
on the first execution of the real pipeline.

## the symptom

Sweeping the one knob produced no change at all:

```
=== smooth_1d, 32768 bytes ===        (before the fix)
threshold   tokens  mean len      ratio   round-exact
    0.000     8192       4.0      1.52x        96.6%
    0.050     8192       4.0      1.52x        96.6%
```

8192 tokens of length 4 is the leaf level untouched. The pyramid was
built and then discarded, at every threshold, on every input.

## the cause

`_BaseLeafMinter._project` read `matmul(patches, self.leaf_basis)`.
`leaf_basis` is `pinv(A)` with `A` shaped `[points, basis]`, and
reconstruction is `coeffs @ A.t()`, so the projection must be
`patches @ pinv(A).T`. The two agree only if `A` is symmetric, and the
Chebyshev basis matrix is not.

Measured on one patch: reconstruction error 0.9437 as written, exactly
0.0000 with the transpose. Level 0 must be exact — four coefficients
through four points is a square system — and it was wrong by most of
the dynamic range.

So every node carried a `max_err` of 1.2 to 2.6 on data spanning 0.6,
and `_PyramidWalker` keeps a node only where `max_err <= threshold`.
Nothing above the leaves was ever kept.

`_DualCurveFitter.fit` at stage 4 already used the correct form. The
two stages disagreed and the wrong one fed every error estimate.

## what changed

| data | threshold | ratio before | ratio after |
|---|---|---|---|
| smooth_1d | 0.004 | 1.52x | **17.03x** |
| smooth_1d | 0.020 | 1.52x | **143.72x** |
| photo tile | 0.100 | 1.52x | **7.76x** |
| python_source | 0.100 | 1.52x | 2.97x |

## what it invalidates

- `optimal_thresh = 1.1`, chosen by a Pareto sweep against errors that
  ran 1.2 to 2.6. Against correct errors it merges everything.
- the reported 4.17x on the JWST image, for the same reason.
- **nothing in logs 001-004** — those used an independently written
  fixed-window fit and never called the prototype.

Record: `~/Programming/PUBLIC/ZSpectralCompression/DevComms/log_005_leaf_projection_defect.md`.
