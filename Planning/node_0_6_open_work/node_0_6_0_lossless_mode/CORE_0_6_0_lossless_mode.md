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

## partly answered, 2026-09-08

the owner's clarification — "exact" means the reconstruction must *round* to
the original byte, not be bit-exact before rounding — makes the
question measurable without running the prototype, by counting how
often the rounded fit already equals the source.

| file | segment length | rounds exact | correction | coefficients | lossless total |
|---|---|---|---|---|---|
| smooth_1d | 128 | 97.6% | 0.19 | 1.00 | 1.19 |
| smooth_1d | 512 | 97.8% | 0.18 | 0.25 | **0.43** |
| python_source | 512 | 0.3% | 6.54 | 0.25 | 6.79 |

Bits per byte; coefficients priced pessimistically at four float32 per
segment.

- **On smooth data lossless is viable and wants long segments.** 0.43
  bits per byte at length 512 against `xz -9` at 0.28, and roughly
  0.31 if the coefficients are quantised to 16 bits — level with the
  baseline, on data where a histogram coder gets nothing.
- **The correction stream plateaus at 0.18 bits per byte** past length
  128. That is the floor from the source having been quantised to
  bytes, not a limit of the basis.
- **Text is not viable at any length**, now measured across five.

What remains for the prototype's own run: the harness segments at
fixed lengths, so it cannot show what *adaptive* merging reaches, and
it reads 2D data in raster order rather than Z-order. Both are
expected to move the numbers the same way — better — so these are a
floor.

Record: `~/Programming/ZSpectralCompression/DevComms/log_003_roundable_to_exact.md` §3.
