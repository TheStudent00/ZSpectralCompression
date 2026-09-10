# log 001 — ZSpectral on 1D data, measured for the first time

Repo: `~/Programming/PUBLIC/ZSpectralCompression`. Written 2026-09-08 by
Claude. All compute ran in the Airlock `sandbox-runner` container, in
pure Python (no numpy in that image, and nothing was installed into
it).

the owner, 2026-09-08:

> its lossy by config for images in some of the runs that were done.
> however, the algorithm is capable of lossless compression. and in
> N-Dimensions (for all N>=1). granted that the z-curve is just a
> straight line for most files. [...] to be fair, ive never measured
> the compression capabilities on a 1D file like text or a binary.

---

## 1. What was measured, and with what

Not the real codec. A **stand-in** for its leaf behaviour: a degree-3
Chebyshev least-squares fit over fixed 8-sample windows, coefficients
rounded to integers, residual computed exactly. Read §1.1 before
drawing conclusions about the real pipeline.

Columns:

| column | what it is |
|---|---|
| `H0` | order-0 entropy of the raw bytes, bits/byte. What an entropy coder with no model gets. |
| `H1` | entropy of a byte given the previous byte. What a first-order *context* model gets. |
| `cheb` | order-0 entropy of the fit residual alone, bits/byte. Optimistic — ignores the cost of the coefficients. |
| `cheb+c` | the honest lossless cost: residual (8 values) plus coefficients (4 values) per 8-byte window. |
| `paeth` | entropy of a Paeth-predicted residual (left / up / up-left), at the best stride found. |
| `stride` | the stride that minimised `paeth`, searched over 1–64 plus 30 larger candidates. |
| `xz` | `xz -9` output size in bits/byte. A strong general-purpose baseline. |

### 1.1 What this stand-in is not

The real pipeline merges segments up a pyramid wherever the fit error
stays under threshold, so a smooth region becomes **one** segment
covering thousands of samples and the coefficient cost amortises
away. The fixed 8-sample window pays 4 coefficients per 8 bytes
always. So:

- **the `cheb+c` column is a floor on the real design, not a
  ceiling** — the real codec will do better on smooth data;
- **the `cheb` column is a fair reading of whether the basis fits the
  data at all**, because it asks only "does a degree-3 polynomial
  predict these 8 bytes", independent of segment length.

---

## 2. The measurements

```
file                   H0     H1   cheb  cheb+c   paeth   stride     xz
------------------------------------------------------------------------
cpp_source           5.17   3.76   5.88    9.24    6.44        1   1.18
python_source        4.88   3.53   5.87    9.28    6.17        1   2.04
english_prose        4.86   3.53   6.32    9.75    6.48        1   2.65
elf_binary           6.19   4.02   7.48   11.34    6.92        1   2.97
png_image            8.00   7.85   7.72   11.65    7.97        3   7.93
jpeg_image           7.96   7.68   7.69   11.60    7.99        1   8.00
random_control       8.00   7.95   7.75   11.67    8.00        3   8.00
smooth_1d            7.56   0.19   0.32    1.74    0.19        1   0.28
smooth_2d_raw        7.44   1.31   1.03    2.88    1.26     1000   0.32
```

Sources: `cpp_source` = 433 KB of concatenated Blink `.cc` files;
`python_source` = `zspectral_compression.py`; `english_prose` =
`~/Programming/PRIVATE/DevComms/LLM_communication_protocol.md`; `elf_binary` =
first 1 MB of `/usr/bin/restic`; `smooth_1d` = sum of three
low-frequency sines quantised to bytes; `smooth_2d_raw` = a
1000×1000 raw greyscale radial cosine field.

### 2.1 On text, code and binaries the fit makes things worse

`H0` versus `cheb`, i.e. raw bytes versus the fit residual:

| file | raw | after the fit | change |
|---|---|---|---|
| cpp_source | 5.17 | 5.88 | **+0.71** |
| python_source | 4.88 | 5.87 | **+0.99** |
| english_prose | 4.86 | 6.32 | **+1.46** |
| elf_binary | 6.19 | 7.48 | **+1.29** |

The residual carries *more* entropy than the source did. The
transform destroyed structure rather than concentrating it. And that
is before the coefficients: `cheb+c` is 9.24 to 11.34 bits per byte,
against 8 for storing the file untouched. Lossless via this route is
**expansion** on this class of data.

### 2.2 Why — the model class is wrong, not the implementation

- A polynomial basis encodes one assumption: **nearby samples have
  nearby values**. That is a smoothness model.
- The bytes of `the quick` are 116, 104, 101, 32, 113. Nothing about
  a symbol's numeric value predicts its neighbour's numeric value.
  Text is a symbol sequence, not a sampled signal.
- Its structure is **contextual**: which symbol follows which. The
  `H1` column is that model at order 1, and it takes English from
  4.86 to 3.53 bits/byte without any transform at all. `xz` reaches
  2.65 by adding repeat-matching on top.
- A linear transform preserves the entropy of an uncorrelated source.
  It only pays when it diagonalises a correlation the source actually
  has. Smooth signals have that correlation; text does not.

### 2.3 Where it genuinely wins, and this is the real result

`smooth_1d`:

| measure | value |
|---|---|
| `H0` (byte histogram) | **7.56** bits/byte — looks nearly random |
| `cheb` residual | **0.32** bits/byte |

A histogram-based entropy coder sees almost nothing to exploit: 7.56
of 8 bits. The smoothness model extracts a factor of about 25. This
is the case the method was built for, and it is real.

Two honest qualifications:

- `xz` reached 0.28 on the same file, slightly better than 0.32, by
  finding the periodicity through repeat-matching. The method is not
  beating the general-purpose baseline here.
- But per §1.1, the 8-sample window is the crudest possible version
  of the design. Adaptive segment merging is precisely what would
  close that gap, and it is untested.

### 2.4 Already-compressed data is a floor for everything

`png_image`, `jpeg_image`, `random_control`: every method sits at
7.7–8.0 bits/byte. Nothing works, as expected — the entropy is
already extracted.

---

## 3. The N-dimensional claim, inverted

the owner:

> granted that the z-curve is just a straight line for most files

True in the direction stated, and the more interesting statement is
the converse: **many 1D files are secretly N-dimensional, and the
dimension is discoverable.**

The `stride` column is an automatic search: for each candidate stride
`s`, predict each byte from its left and upper neighbours at that
stride, and take the stride minimising residual entropy.

| file | stride found | reading |
|---|---|---|
| `smooth_2d_raw` | **1000** | the true row width, recovered with no metadata |
| cpp_source, python_source, english_prose, elf_binary | 1 | correctly reports "this is 1D" |
| png, jpeg, random | 1–3 | no structure to find |

At stride 1000, `smooth_2d_raw` drops from 7.44 to 1.26 bits/byte
under a 2D predictor. General-purpose compressors have the machinery
for this — `xz --delta=dist=N` — but the stride must be supplied by
hand. **Discovering it is the underexploited part**, and it is where
an N-D method has an edge that is not available to a 1D one.

---

## 4. The surgical-edit claim, measured

the owner:

> if i had a compressed image and i added a square in the middle of
> the image, i could surgically insert the square and truncate the
> curves it overlaps with. and even re-run the curving on the changed
> sections.

This is the strongest idea in the design, and it is measurable
independently of compression. Setup: a 1024×1024 greyscale field,
cut into 4096-byte chunks, chunks hashed. Apply an edit; count how
many chunk hashes changed. Two traversal orders: raster (row by row)
and Z-order (Morton interleave).

```
image 1024x1024, 4096-byte chunks, 256 chunks total

edit                                   raster    z-order
--------------------------------------------------------
64x64 square, aligned                  16/256      1/256
64x64 square, unaligned                17/256      4/256
128x128 square                         32/256      4/256
one full row                            1/256     16/256
one full column                       256/256     16/256
4 scattered 32x32 squares              24/256      8/256
```

### 4.1 What the table says

- **Compact 2D edits: Z-order is 4× to 16× better.** A 64×64 aligned
  square is *one* chunk under Morton order and 16 under raster.
- **Row-shaped edits: raster wins**, 1 against 16. A row is
  contiguous in raster order by definition.
- **Column-shaped edits: raster is catastrophic**, 256 of 256 — every
  chunk in the image changed because one byte per row moved. Z-order
  holds at 16.

So the precise statement is: **the space-filling curve trades the
best case for the worst case.** Raster order is optimal for edits
shaped like its traversal and pathological for edits shaped across
it. Z-order is never optimal and never pathological. For edits whose
shape is not known in advance, that is the better bet.

### 4.2 What the property is called, and who else has it

The property is **local decodability**: a segment can be decoded, and
replaced, without touching the rest.

Most compressors do not have it. LZMA, zstd with long-range matching,
and any adaptive arithmetic coder are *causal and adaptive* — the
decoder's state at position *i* depends on every byte before *i*, so
an edit at the front invalidates everything after it.

Formats that do have it, all by the same means (independent
segments): FLAC frames, JPEG2000 tiles and precincts, squashfs
blocks, and the content-defined chunking used by `restic` and `borg`.

### 4.3 Where this design differs from those

Those are all **1D** chunkers. Two things follow:

- A local 2D edit is *scattered* in 1D. The table quantifies it: the
  same 64×64 square costs 16 chunks in raster order and 1 in Morton
  order.
- The pyramid adds a **hierarchy** those formats lack. If each
  pyramid node carries a hash of its subtree, the structure is a
  Merkle tree over a space-filling curve, and "what changed between
  version A and B" is answerable in time proportional to the changed
  region rather than to the file.

That combination — geometry-aware chunk boundaries plus a hash
hierarchy — is not what the standard tools do.

---

## 5. Three axes, and which one this design is actually strong on

Compression research optimises mostly one axis. There are three:

| axis | question | who optimises it |
|---|---|---|
| **ratio** | how few bits | xz, zstd, brotli, PPM/CM |
| **model class** | what structure is assumed | transform codecs assume smoothness; context models assume symbol context; LZ assumes repeats |
| **locality** | can a piece be read or replaced without the rest | FLAC, JPEG2000, squashfs, content-defined chunkers |

The measurements say this design is **weak on ratio for 1D symbol
data** (§2.1), **strong on ratio for sampled signals** (§2.3), and
**strong on locality in N dimensions** (§4), which is the axis almost
nothing else covers in more than one dimension.

That suggests the sharper framing is not "a better compressor" but
**a geometry-aware chunker with a hash hierarchy** — where the
Chebyshev fit is one available per-chunk codec rather than the point
of the system.

---

## 6. See also

- `~/Programming/PUBLIC/ZSpectralCompression/zspectral_compression.py` — the
  codec; `_ZCurveRouter`, `_TopologicalPyramid` and `_PyramidWalker`
  are the parts §4 is about.
- `~/Programming/PRIVATE/GitSpaceTime/DevComms/log_002_compression_and_storage_layer.md`
  §2.1 — the chunk-level dedup measurement this log's §4 extends into
  two dimensions.
