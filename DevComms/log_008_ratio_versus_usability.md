# log 008 — compression against usability, and a correction to every comparison so far

Repo: `~/Programming/ZSpectralCompression`. Written 2026-09-09 by
Claude. Airlock `sandbox-runner`. Tool:
`Tools/compare_matched_granularity.py`.

the owner, 2026-09-09:

> is there theory that states some kind of constraint on compression
> vs compressed-form-usability? [...] kind of like a trade-off between
> space and time complexities.

---

## 1. The correction this log exists for

**Every comparison in logs 001-007 was unfair to ZSC, in one specific
way.** They put ZSC's ratio next to `xz -9` and `zstd -19` on the
whole file. But those tools decode strictly from the start: to read
byte 30,000 you decompress the preceding 30,000. ZSC does not — each
segment is decodable alone.

So the comparison was "a random-access format against sequential-only
formats", scored only on ratio. Correcting it means giving the
general-purpose tools the same constraint: compress each block
independently, so any block can be read alone.

## 2. Matched granularity, both lossless

Each row is a granularity — the size of the unit either format can
decode without touching the rest. zstd figures have the measured
9-byte frame overhead removed, so the comparison is of the coding
itself.

### smooth_1d — whole-file sequential `xz -9` = 26.09x

| granularity | ZSC | zstd -19 |
|---|---|---|
| 16 B | **7.23x** | 1.65x |
| 64 B | **13.22x** | 4.94x |
| 256 B | **23.23x** | 11.67x |
| 512 B | **26.56x** | 15.26x |
| 1024 B | **20.59x** | 18.15x |

**ZSC at 512-byte random access reaches 26.56x — above what `xz`
achieves with the whole file and no random access at all.** On its
target data it is not behind; it was being scored against a different
sport.

### photo tile — `xz -9` = 1.81x

| granularity | ZSC | zstd -19 |
|---|---|---|
| 16 B | **1.54x** | 1.00x |
| 128 B | **1.50x** | 1.19x |
| 512 B | **1.45x** | 1.34x |
| 1024 B | 1.43x | 1.43x |

ZSC is nearly **flat** in granularity — 1.54x down to 1.43x across a
64-fold change. zstd falls off a cliff, 1.43x to 1.00x. Fine-grained
access costs ZSC almost nothing and costs zstd everything.

### python_source — `xz -9` = 3.80x

| granularity | ZSC | zstd -19 |
|---|---|---|
| 16 B | **1.09x** | 1.01x |
| 32 B | **1.13x** | 1.03x |
| 64 B | **1.18x** | 1.13x |
| 128 B | 1.21x | **1.40x** |
| 1024 B | 1.26x | **2.26x** |

ZSC wins below about 64 bytes and loses above it. `elf_binary` is the
one file where zstd wins at every granularity.

## 3. So is there a theorem?

Three separate bodies of work, and they do not say what the folk
version says.

### 3.1 The foundational statement: time-bounded Kolmogorov complexity

`K(x)` is the length of the shortest program that outputs `x`. It is
uncomputable, and it ignores time entirely.

The time-bounded version `K^t(x)` restricts to programs halting within
`t` steps, and **`K^t(x)` grows as `t` shrinks** — less decode time
means a longer shortest description. Levin's `Kt(x) = min_p (|p| +
log(time(p)))` makes the trade explicit in a single quantity.

This is the closest thing to what the owner described, and it is real. It is
also asymptotic and non-constructive: it says a trade exists, not how
steep it is for any actual format.

### 3.2 The proven, quantified version: succinct data structures

A structure is **succinct** if it uses `Z + o(Z)` bits, where `Z` is
the information-theoretic minimum, while still answering queries. The
field's whole business is the space-time frontier, and it has real
lower bounds in the cell-probe model — for several problems, driving
the redundancy `r` toward zero provably forces query time up, on the
order of `log(n/r)`.

Two things worth taking from it:

- The trade is **proven**, not folklore.
- The penalties are **logarithmic**, not catastrophic. Near-optimal
  space with near-constant query time is usually achievable.

### 3.3 The counterexample that kills the folk law

Compressed self-indexes — the **FM-index** (Ferragina-Manzini), built
on the Burrows-Wheeler transform plus rank structures — occupy space
close to the entropy of the text, **and** answer "where does this
pattern occur" in time proportional to the pattern length, without
decompressing anything.

It is *smaller than the original file* and *faster to search than the
original file*. More compression bought more usability, not less.

## 4. What the real principle is

Not "more compression, less usable". Rather:

> **Compression removes redundancy. Whether the compressed form stays
> usable depends on whether the operation you want survives the
> particular redundancy that was removed — that is, on whether the
> compressor's model happens to be a structure your operation can use.**

Three cases, all in this conversation:

| format | what its model is | what that model gives you for free |
|---|---|---|
| gzip / xz | back-references into recent history | nothing but reconstruction — a back-reference serves no other question |
| FM-index | the sorted rotations of the text | substring search, because the model *is* an index |
| ZSC | a piecewise polynomial over a space-filling curve | evaluate anywhere, resample, differentiate, do arithmetic, replace a region in N dimensions |

The quantity of compression is not the variable. The *shape* of the
model is.

## 5. The one place the trade is genuinely hard

Entropy coding destroys addressability, and this part is not a design
choice.

To reach the entropy bound a symbol of probability `p` must cost
`-log2(p)` bits, which is not an integer. So symbols do not begin at
addressable positions, and you cannot seek to symbol `i` without
either decoding from the start or storing an auxiliary index of
positions. That index is redundancy — bits above the entropy — and
buying random access means buying it.

That is exactly the quantity the succinct-structures bounds in §3.2
measure. It is also, in practical form, the entire content of §2: a
block boundary is a place where the coder resets so that seeking is
possible, and the ratio lost is the price.

## 6. Where this leaves ZSC

**ZSC sits at the fine-granularity end of that curve by construction**,
because its segments are independent. That is why its ratio is nearly
flat in granularity where zstd's collapses.

- On smooth data it is the better format at every granularity
  measured, and at 512 bytes it beats whole-file `xz`.
- On a photo tile it wins below about 1 KB.
- On text it wins below about 64 bytes and loses above.
- On a compiled binary it loses everywhere.

The honest summary is not "ZSC compresses badly". It is: **ZSC pays
for fine-grained addressability, and on data whose structure it models
the price is negative — it gets the addressability and a better ratio
at the same time.**

## 7. See also

- `~/Programming/ZSpectralCompression/DevComms/log_007_model_classes.md`
  §6 — what a ZSC payload can do that an encoding cannot.
- `~/Programming/ZSpectralCompression/Planning/node_0_5_findings/node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md`
  — the N-dimensional version of the same property.
