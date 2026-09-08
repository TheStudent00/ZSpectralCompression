---
id: zspectral.open_work.lossless_mode
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: lossless_mode
    path: Planning/node_0_6_open_work/node_0_6_0_lossless_mode/CORE_0_6_0_lossless_mode.md
super_node:
    name: open_work
    path: ../CORE_0_6_open_work.md
sub_nodes: []
---

# CORE 0_6_0 — lossless_mode

## metadata

- **id:** zspectral.open_work.lossless_mode
- **level:** 2
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [open_work](../CORE_0_6_open_work.md)

## sub_nodes

*(none yet)*

## definition

Establish what the real pyramid costs at `merge_threshold = 0`, on
`smooth_1d` and `smooth_2d_raw`.

## why this measurement and not another

The harness in [findings](../../node_0_5_findings/CORE_0_5_findings.md)
cannot distinguish two explanations of its own totals: that the
Chebyshev basis does not fit the data, or that a fixed 8-sample window
is too crude to amortise the coefficients. Running the prototype's own
adaptive merging separates them, and it is one run.

## the number that decides it

The harness reported 1.74 and 2.88 bits per byte for those two files
against `xz -9` at 0.28 and 0.32. If adaptive merging closes most of
that gap, lossless mode is worth building. If it does not, the
conclusion is that lossless via this route is bounded below by the
residual and the project's compression half should stay lossy.

## what lossless would have to mean here

Encode the residual exactly alongside the coefficients, the way FLAC
encodes the residual of its linear prediction. That makes the
polynomial fit a *predictor* rather than a representation, and moves
the compression into whatever entropy coder handles the residual —
which is a real design, and a different one from what exists.
