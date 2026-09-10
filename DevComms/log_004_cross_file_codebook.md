# log 004 — the cross-file codebook, measured; and the metrics, restated as ratios

Repo: `~/Programming/PUBLIC/ZSpectralCompression`. Written 2026-09-08 by
Claude. Airlock `sandbox-runner`; `numpy`, `scikit-learn`, `pillow`
and `zstandard` were installed into it for this work (see §4).

---

## 1. The metrics, in the units the owner asked for

the owner, 2026-09-08:

> im also not sure i understand the metrics. compressed size compared
> to uncompressed size makes sense to me.

Logs 001–003 reported **bits per byte**, which is a rate, not a ratio.
The conversion is one division:

    ratio = 8 / (bits per byte)

So the earlier headline numbers, restated:

| result | bits/byte | **ratio** |
|---|---|---|
| smooth_1d, lossless, 512-sample segments | 0.43 | **18.6x** |
| smooth_1d, same with 16-bit coefficients | 0.31 | **25.8x** |
| smooth_1d, `xz -9` | 0.28 | 28.6x |
| C++ source, after the polynomial fit | 5.88 | **1.36x** |
| C++ source, raw byte histogram | 5.17 | 1.55x |
| C++ source, `xz -9` | 1.18 | 6.78x |

Everything below is a ratio. Above 1.0 is compression; below 1.0 is
expansion.

---

## 2. the owner's hypothesis: a codebook shared across files

> im mildly surprised theres no benefit or neutrality for text files.
> i would think for a larger set of files, the codebook would make
> things more efficient. a benefit that other compression systems dont
> use across files. this one could and im very curious about that.

### 2.1 The test

Three corpora, 24 files of 32 KB each. Codebook trained on the first
16; **every number is measured on the 8 held-out files the codebook
never saw.** All figures are lossless — the correction stream that
restores the exact bytes is priced in at its measured entropy.

- **text** — concatenated Blink `.cc` source, cut into 24 pieces.
- **signal** — 24 synthetic smooth traces, each with its own random
  frequencies, amplitudes and phases. Models similar-but-not-identical
  sensor data.
- **photo** — 24 greyscale 128x256 tiles from a real image
  (`jwst_final_goldilocks.jpg`). The most realistic "many similar
  files" case here.

### 2.2 The result

| corpus | window | per-file codebook | **shared codebook** | xz -9 | zstd -19 | zstd + trained dict |
|---|---|---|---|---|---|---|
| text | 8 | 0.96x | **1.05x** | 7.53x | 7.66x | **9.60x** |
| text | 32 | 1.04x | **1.15x** | 7.53x | 7.66x | **9.60x** |
| signal | 8 | 2.80x | **3.75x** | 57.54x | 57.53x | 58.02x |
| signal | 32 | 5.08x | **9.23x** | 57.54x | 57.53x | 58.02x |
| photo | 8 | 1.46x | **1.63x** | 2.51x | 2.27x | 2.25x |
| photo | 32 | 1.48x | **1.67x** | 2.51x | 2.27x | 2.25x |

**the owner's prediction holds in direction on every row.** The shared
codebook beats the per-file codebook in all six, by 9% to 82%.

### 2.3 But the reason is not the one that would be exciting

Decomposing the gain: a codebook is `256 * 3 * 4 = 3072` bytes.
Per-file, that is 9.4% of a 32 KB file. Shared across 24, it is 0.4%.
Removing that difference alone accounts for:

| corpus, window | measured gain | explained by amortisation alone |
|---|---|---|
| text, 32 | 0.11x | 0.11x |
| signal, 32 | 4.15x | 4.26x |
| photo, 32 | 0.19x | 0.23x |

**The entire gain is amortisation of the codebook's fixed cost.**
Generalisation contributes nothing — slightly less than nothing, since
the amortisation column slightly exceeds the measured gain, meaning
centroids fitted on other files reconstruct a held-out file a shade
worse than its own would.

That is still a real and useful finding, and it is not trivial: the
centroids transfer to unseen files at **almost no loss**. The shape
distribution is stable across files. What does not happen is any
transfer of knowledge beyond that.

### 2.4 Where the field already does this, and where it does not

the owner's "a benefit that other compression systems dont use across files"
is not quite right — `zstd --train` builds a dictionary from a corpus
and is exactly cross-file sharing. It is in the table, and on text it
is the best method measured: 7.66x without a dictionary, **9.60x with
one**, a 25% gain that IS knowledge transfer, not amortisation.

The interesting row is `photo`, where it reverses:

| photo | ratio |
|---|---|
| zstd -19, no dictionary | 2.27x |
| zstd -19, dictionary trained on 16 sibling tiles | **2.25x** |
| shape codebook, per file | 1.46x |
| shape codebook, shared across 24 | **1.63x** |

**Cross-file sharing helped the shape codebook and hurt the byte
dictionary.** A byte dictionary matches exact substrings, and two
tiles of a photograph share almost no exact substrings; a shape
codebook matches approximate geometry, which they do share. The
direction the owner predicted is visible precisely where the existing
technique fails.

### 2.5 What it does not overturn

The absolute levels. At its best the method reaches 1.67x on photo
tiles against `xz -9` at 2.51x, and 1.15x on text against 9.60x. It
is 1.5x to 8x behind general-purpose compressors on every corpus.

And one caveat that runs the other way, stated because it is large:
**every number here is lossless, which is this codec's worst regime.**
It is built for lossy operation, where the prototype reports 4.17x on
the JWST image. A fair comparison for its intended use is against
JPEG or WebP at matched reconstruction error, which has not been run.

---

## 3. The prototype fixes

the owner: "sure. and we can fix whatever else also."

Three edits to `~/Programming/PUBLIC/ZSpectralCompression/zspectral_compression.py`.

| # | what | where |
|---|---|---|
| 1 | the codebook is now charged per tile, not per channel | the tiled JWST run, ~line 1539 |
| 2 | the reconstruction is saved as PNG, not JPEG, and the comparison figure loads the PNG | ~lines 1555 and 1566 |
| 3 | `calculate_metrics` now also reports `ratio_entropy_coded`, pricing the label stream at its measured entropy instead of a flat byte each | `ZSpectralCompressor.calculate_metrics` |

Fix 1 makes the reported ratio slightly worse and correct. Fix 3 makes
it better and correct: log 002 §2 measured label streams at 1.50–2.04
bits where the old count charged 8, and labels are roughly half the
counted payload.

**All three are unverified by execution**, for two reasons, both worth
recording:

- `torch` is not in the Airlock image, and installing it needs
  `download.pytorch.org` added to the egress allowlist
  (`~/Programming/PUBLIC/Airlock/allow.sh add ...`) — a standing change to a
  security boundary, so not made unilaterally.
- **`jwst_image.jpg` is not in the repository.** Only the output,
  `jwst_final_goldilocks.jpg`, is committed. The headline 4.17x run is
  therefore not reproducible from the repo as it stands, by anyone,
  with or without the fixes.

The edits are small, local, and were verified by reading the diff and
by `ast.parse`. They are not verified by running the codec.

### 3.1 Not fixed, and why

`fast_pytorch_kmeans` (line 1024) is dead code — defined, never
called, while the live path uses `sklearn.cluster.KMeans` on the CPU
once per tile. Wiring it in is plausibly a real speedup and plausibly
a behaviour change; without the ability to run the codec, replacing
the clustering implementation is not an edit to make blind.

---

## 4. Airlock

`numpy`, `scikit-learn`, `pillow` and `zstandard` were installed into
the running `sandbox-runner` container with its own `pip`. That is the
rule — a missing tool is installed into Airlock, never into a host
environment — but it is the *impermanent* form of it: the packages do
not survive a rebuild. The durable form is an entry in
`~/Programming/PUBLIC/Airlock/Containerfile`, which belongs to Airlock's own
repo and is a separate change.

`torch` could not be installed: the proxy returned
`403 Forbidden` for `download.pytorch.org`. See §3.

---

## 5. See also

- `~/Programming/PUBLIC/ZSpectralCompression/DevComms/log_003_roundable_to_exact.md`
  — the round-exact measurements and the three defects fixed here.
- `~/Programming/PUBLIC/ZSpectralCompression/Planning/node_0_3_container/node_0_3_1_vector_quantizer/CORE_0_3_1_vector_quantizer.md`
  — the node this log's §2 is about.
