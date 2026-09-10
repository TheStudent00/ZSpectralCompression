# log 006 — the lossless criterion is a rate criterion, not an error criterion

Repo: `~/Programming/PUBLIC/ZSpectralCompression`. Written 2026-09-09 by
Claude. Airlock `sandbox-runner` with torch. Follows
`log_005_leaf_projection_defect.md`, without which none of this could
be measured.

the owner, 2026-09-08:

> oh optimal_threshold was for images. i think we can have a different
> criteria for lossless no?

Yes. And the obvious different criterion turns out to be the wrong
one, which is the finding.

---

## 1. The obvious criterion, and what it costs

For byte data normalised to [0,1], "the reconstruction rounds back to
the exact original byte" is `max_err < 0.5/255 = 0.00196`. A derived
constant, not a tuned one — no `optimal_thresh` needed.

Run through the prototype's own walker, with the coefficients
quantised before the correction stream is measured (so the price is
honest), keeping only configurations that restore **100% of bytes**:

| file | threshold | tokens | mean segment | coef bits | ratio | `xz -9` |
|---|---|---|---|---|---|---|
| smooth_1d | 0.00098 | 2080 | 15.8 | 12 | **2.51x** | 26.09x |
| photo tile | — | — | — | — | never reached 100% | 1.81x |
| python_source | 0.00098 | 8031 | 4.1 | 10 | **0.78x** | 3.80x |

2.51x where `xz` gets 26x, and outright expansion on source code.

## 2. Why it is the wrong criterion

The error criterion splits a segment the moment it would push one
sample past half a quantisation step. That forces **short** segments —
a mean of 15.8 samples on smooth data, 4.1 on source. And a segment
costs four coefficients whatever its length, so short segments make
the coefficients the dominant cost:

    4 coefficients x 12 bits / 15.8 samples = 3.04 bits per byte,
    before a single correction is stored.

The criterion optimises the wrong quantity. Exactness is not something
the *merge* has to deliver — the correction stream delivers it. What
the merge should decide is only whether merging is **cheaper**.

## 3. The right criterion, measured

Merge while the coefficients saved exceed the corrections added. Same
machinery, same fit, same exactness guarantee — every row below
restores 100% of bytes, with the corrections priced in:

| file | segment | coef bits | samples needing no correction | ratio | `xz -9` |
|---|---|---|---|---|---|
| smooth_1d | 512 | 12 | 97.28% | **25.89x** | 26.09x |
| photo tile | 64 | 8 | 8.93% | **1.51x** | 1.81x |
| python_source | 1024 | 8 | 0.33% | **1.22x** | 3.80x |

**On smooth data: 2.51x becomes 25.89x.** A factor of 10.3, on
identical data with identical machinery, from changing what the merge
decision optimises. It lands level with `xz -9` at 26.09x — on a file
whose byte histogram carries 7.51 of 8 bits, where a histogram coder
gets nothing.

The mechanism in one line: **it is roughly ten times cheaper to accept
2.7% of samples being wrong and pay to correct them than to split the
segment so they are right.**

Note the third column. At the optimum only 8.93% of photo samples and
0.33% of source samples need no correction — the fit is wrong almost
everywhere and it does not matter, because the correction stream is
priced at its entropy and the coefficients are not being spent on
short segments.

## 4. What is still true

- **Source code stays a loss**: 1.22x against `xz` at 3.80x. Consistent
  with logs 001 and 003, and for the reason given there — a polynomial
  basis models numeric proximity, and text's redundancy is repetition
  and context. See `node_0_5_0_one_dimensional_behaviour`.
- **The photo tile is read here in raster order**, not Z-order, so 1.51x
  against 1.81x is a floor for the real pipeline. Closing that gap is
  what the space-filling curve is for.
- The prototype does not implement any of this. It has no correction
  stream in the payload at all, and its walker takes an error
  threshold. Both would have to change.

## 5. What this asks of the plan

`node_0_6_0_lossless_mode` asked for one number: what adaptive merging
reaches at threshold zero. The answer is 2.51x, and it is the wrong
question — the node should ask for the rate criterion instead. Updated
accordingly.

## 6. See also

- `~/Programming/PUBLIC/ZSpectralCompression/DevComms/log_005_leaf_projection_defect.md`
  — the fix that made the walker function at all.
- `~/Programming/PUBLIC/ZSpectralCompression/DevComms/log_003_roundable_to_exact.md`
  §3 — the fixed-length sweep that first showed long segments winning.
