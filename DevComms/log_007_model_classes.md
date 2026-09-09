# log 007 — what ZSC's model can and cannot see

Repo: `~/Programming/ZSpectralCompression`. Written 2026-09-09 by
Claude. Airlock `sandbox-runner`.

the owner, 2026-09-09:

> i wanted to understand what other compressors do that ZSC cant.

---

## 1. The frame: every lossless compressor is a model plus an entropy coder

- The **entropy coder** turns a probability into bits: a symbol the
  model gave probability *p* costs `-log2(p)` bits. Arithmetic coding
  achieves that to within a fraction of a bit, so this half is solved
  and identical everywhere.
- The **model** assigns those probabilities. Everything that
  distinguishes one compressor from another lives here.

So "what can others do that ZSC cannot" is entirely a question about
model classes.

**ZSC's model, stated exactly:** *the data are samples of a
piecewise-smooth function of position; inside a segment the value is a
degree-3 polynomial of the index.*

## 2. The three structures that model cannot express

| structure | who models it | ZSC |
|---|---|---|
| **repetition at a distance** — "these 40 bytes occurred 12,000 bytes ago" | LZ77, LZMA, zstd | no mechanism at all. Segments describe where they are, never what they resemble |
| **symbolic context** — "after `retur` comes `n`" | PPM, context mixing, the entropy stage of every modern codec | none. Its model is over numeric values, not symbol identity |
| **adaptation during the stream** | every adaptive coder | none. Basis fixed, codebook fitted once per payload |

Measured weight of the first: **70.2%** of a C++ source file is a
literal repeat of something within the preceding 64 KB (log 007 §5).
Of the second: order-1 context alone takes English from 4.86 to 3.53
bits per byte with no transform.

## 3. The one structure ZSC models and LZ cannot — and its catch

**Numeric proximity.** A ramp 0,1,2,...,255 contains no repeated
substring, so LZ sees nothing, but it is one polynomial.

The catch, measured: **byte-quantising a smooth signal converts
smoothness into repetition**, and LZ eats repetition.

| signal | adjacent bytes equal | xz | ZSC |
|---|---|---|---|
| slow smooth sum of sines, 8-bit | 88.4% | 9.27x | **20.17x** |
| aperiodic smooth walk k=8, 8-bit | 84.5% | **6.30x** | 3.72x |
| aperiodic smooth walk k=128, 8-bit | 94.9% | **15.09x** | 13.06x |

When a signal varies slowly and is stored in 8 bits, 85–95% of
adjacent samples are *identical*. That is a run, and a run is a
repeat. So on 8-bit smooth data the two model classes overlap almost
entirely, and LZ usually wins.

## 4. Where the overlap disappears: more bits per sample

The same signals at 16-bit resolution, which is what audio and sensor
logs actually use:

| signal | adjacent equal | xz | xz + delta filter | ZSC |
|---|---|---|---|---|
| walk k=8, 8-bit | 84.5% | 6.30x | 9.36x | 3.72x |
| walk k=8, **16-bit** | **0.8%** | **1.47x** | 2.54x | 1.97x |
| walk k=32, 8-bit | 88.5% | 7.90x | 13.34x | 6.80x |
| walk k=32, **16-bit** | **1.1%** | **1.54x** | 4.39x | 3.17x |
| walk k=128, 8-bit | 94.9% | 15.09x | 20.38x | 13.06x |
| walk k=128, **16-bit** | **2.0%** | **1.51x** | 8.19x | 7.18x |

**Plain xz collapses to 1.5x on 16-bit smooth data** — the runs are
gone, and repetition was the only structure it could see. ZSC holds
its ratio (7.18x on the smoothest), because smoothness did not go
anywhere.

## 5. But numeric proximity is not ZSC's private property

The `xz + delta` column is `xz` run over first differences. **A delta
filter is a degree-0 polynomial predictor.** It is the same model
class, one line of preprocessing, and it beats ZSC in every row above.

The same idea appears as PNG's per-row filters, FLAC's linear
prediction, and `xz --delta=dist=N`.

So the honest position on ratio: ZSC's model class is *reachable* by
general-purpose tools through a filter, and their filters are
currently better tuned than ZSC's implementation of it. What ZSC has
that a delta filter does not is **variable segment length chosen by
the data** — a delta filter is fixed-order and fixed-stride.

## 6. What ZSC has that no entropy coder has, and it is not a ratio

A gzip or zstd payload is an **encoding**: the only thing you can do
with it is decode it. A ZSC payload is a **model** — a piecewise
polynomial. Without decompressing you can:

- evaluate at any position, including positions between samples
  (resample, zoom) — the representation is resolution-independent;
- differentiate or integrate, in closed form;
- do arithmetic between two payloads. That is what
  [algebra](../Planning/node_0_0_algebra/CORE_0_0_algebra.md) is —
  `add`, `multiply`, `matmul`, `composition`, `integrate`, with
  interval bounds propagated;
- address a region in N dimensions and replace it, which
  [edit_locality](../Planning/node_0_5_findings/node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md)
  measured at 1 changed chunk against 16 for raster order.

None of that is available from a repetition or context model, because
neither ever forms a continuous object. This is the capability
argument for the design, and it is independent of the ratio argument —
which §5 says is the weaker of the two.

## 7. See also

- `~/Programming/ZSpectralCompression/DevComms/log_006_lossless_criterion.md`
  — the rate criterion, and the lossy-plus-corrections structure.
- `~/Programming/ZSpectralCompression/Planning/node_0_5_findings/node_0_5_0_one_dimensional_behaviour/CORE_0_5_0_one_dimensional_behaviour.md`
