# log 002 — the codebook, the index stream, and the reverse-engineered plan

Repo: `~/Programming/ZSpectralCompression`. Written 2026-09-08 by
Claude. Measurements ran in the Airlock `sandbox-runner` container in
pure Python; nothing was installed into it.

---

## 1. The codebook: the owner's reading was right about coefficients, and the residual moves the other way

the owner, 2026-09-08:

> the algorithm uses a table of fits that are referenced by index (or
> hash or whatever) correct? i would think that would make the entropy
> mostly neutral because its not storing a unique fit for every single
> curve segment.

Correct about the mechanism. `ZSpectralCompressor.compress` separates
`c0` (quantised to a uint8) from `c1,c2,c3` (standardised, then
k-means to at most 256 centroids), so a token costs one index plus one
byte rather than four coefficient values.

Measured at K = 256, 256 KB of each file, bits per byte:

| file | lossless via codebook | lossless with exact coefficients |
|---|---|---|
| python_source | **6.95** | 9.28 |
| english_prose | **7.37** | 9.75 |
| smooth_1d | 1.92 | **1.41** |
| smooth_2d_raw | 2.85 | **1.79** |

**The trade is coefficient cost against residual cost, and its sign
depends on the data.** A centroid reconstructs a segment worse than
that segment's own fit does, so the residual grows by exactly as much
as the index saved, plus or minus.

- On symbol data the codebook wins by about 2.3 bits per byte. The
  fits there are near-random and expensive to store exactly, and the
  residual was already near-maximal so it has little room to worsen.
- On smooth data the codebook loses. The exact fit is nearly perfect,
  so the residual is where all the remaining cost lives and inflating
  it costs more than the index saves.

Neither column reaches the raw order-0 entropy of the symbol files
(4.86–4.88 bits/byte), so the method remains a loss on that class.

---

## 2. The index stream is not incompressible, and by a wide margin

the owner:

> if we ran the compression system again but on the already compressed
> sequence of indexes, it is possible to extract any further
> compression? not that i would expect it to. just curious.

There is a large amount, on exactly the data the codec is good at.

| stream | labels | H0 | H1 | after `xz -9` |
|---|---|---|---|---|
| smooth_1d | 32,768 | 7.41 | **0.85** | **1.50** |
| smooth_2d_raw | 32,768 | 7.67 | **1.69** | **2.04** |
| python_source | 7,788 | 7.64 | 4.48 | 7.68 |
| english_prose | 6,595 | 7.79 | 4.42 | 7.97 |

Bits per label. `H0` is the label histogram; `H1` is a label given the
previous label.

### Why it is there

**The labels are individually near-uniform and sequentially highly
correlated.** k-means balances its clusters, so the histogram looks
almost random — 7.41 of 8 bits. But adjacent segments of a smooth
signal have similar shapes and therefore the same or a neighbouring
label, which a first-order model sees at once: 0.85 bits.

`xz` recovers most of it: 8 bits per label down to 1.50, a further
factor of 5.3. And `calculate_metrics` counts labels at a flat 1 byte
each, so **the prototype's reported ratios understate what the format
already reaches.**

On symbol data there is nothing to recover, consistent with the codec
having no purchase on that data in the first place.

### The general statement

"Already compressed" is only ever true relative to a model. An output
whose symbols look uniform can still carry order in its *sequence*,
and sequence is a different model class from the one the codec
applied. Image and video standards entropy-code their mode and index
streams for this reason rather than emitting them raw.

---

## 3. The plan, reverse-engineered from the prototype

the owner:

> another thing is that i would love to reverse-engineer the current
> prototype into a PlanPlan in the `Planning` folder. the prototype
> was painful built with earlier LL models.

Built 2026-09-08 against
`~/Programming/PlanPlan/framework/PROTOCOL.md`, from a full read of
the 1,568-line `zspectral_compression.py`.

| measure | value |
|---|---|
| nodes | 42 |
| depth | 4 levels (root, module, class-group, class) |
| `render_plan.py` grammar problems | **0** |
| `check_plans.py` | **0 errors, 1 warning** (see §4) |
| rendered view | `~/Programming/ZSpectralCompression/Planning/plan.html` |

Level 1 is the pipeline plus what has been learned about it:

- `algebra` — the SpectralTensor value type and the arithmetic closed
  over it. Recorded with the fact that **nothing on the compression
  path calls it** except two segment-count operations.
- `geometry` — pad to powers of two, order by Morton code, and back.
- `codec` — leaves, pyramid, descend, re-fit, in `encoder`; evaluate
  and stitch in `decoder`.
- `container` — the topology bitmask, the quantiser, the payload.
- `evaluation` — the config, the metrics, the rate-distortion sweep.
- `findings` — the four measured results, each with the harness that
  produced it and an explicit statement of what it does not support.
- `open_work` — three items, each naming the one measurement that
  would settle it.

### Two things the read surfaced that were not obvious from running it

- **The leaf fit is exact.** `min_patch_size = 4` with a degree-3
  basis is a square system, so all approximation enters at the merge,
  never at the leaves. That is why `merge_threshold` is the single
  lossy/lossless knob.
- **The `meta` channels never reach the payload.** `_PhysicsMinter`
  computes mass, length and confidence, and
  `ZSpectralCompressor.compress` stores labels, `c0`, the codebook and
  the topology — nothing else. That stage serves the algebra half of
  the project, not compression.

### Left for the owner, per PROTOCOL §2

- The tree carries `super_node: null`. Whether the project hangs under
  `~/Programming/PseudoCoupHQ/Planning/node_0_0_projects/` is a
  level-0 question.
- `node_0_6_2_chunker_framing` asks whether the project's centre is
  the codec or the addressing scheme. That is a question about what
  the project is for, which §2 puts at level 0.

---

## 4. A framework defect found while conforming, not fixed

`check_plans.py` reports:

> [WARN] projection: `## sub_nodes` is not the first section on 42
> CORE(s) — (first section is "## metadata")

`PROTOCOL.md` §1b says the opposite:

> - **`## metadata`** — the projection of scalar YAML fields, first,
>   always (§1).
> - **`## super_node`** — the projection of the upward hierarchy edge
>   (§1).
> - **`## sub_nodes`** — the register's projection, immediately after
>   super_node (§1).

So the checker carries a rule from before the `## metadata` block was
introduced (§1 dates that to 2026-08-23). Confirmed not local to this
tree: the same warning fires on the reference project,
`~/Programming/PseudoCoup_v6/Planning`, and on
`~/Programming/GitSpaceTime/Planning`.

**Not fixed here.** The fix is one line in
`~/Programming/PlanPlan/framework/check_plans.py`, and PlanPlan is a
higher-level document set. Recorded so it is not mistaken for a defect
in this tree.

---

## 5. See also

- `~/Programming/ZSpectralCompression/DevComms/log_001_one_dimensional_measurements.md`
  — the 1D and edit-locality measurements this log continues.
- `~/Programming/ZSpectralCompression/Planning/CORE_0.md` — the plan's
  root.
- `~/Programming/PlanPlan/framework/PROTOCOL.md` — the framework this
  tree conforms to; §4 above is about its checker.
