# log 011 — the upgraded codec, built and round-trip verified

Repo: `~/Programming/PUBLIC/ZSpectralCompression`. Written 2026-09-09 by
Claude. Airlock `sandbox-runner` (torch, numpy, sklearn installed).
New module: `src/zsc_lossless.py`. Tests:
`Tools/test_codec_roundtrip.py`, `Tools/test_game_data.py`.

the owner: *"youve made some awesome realizations/discoveries. please
upgrade the system accordingly."*

---

## 1. What was built, and what it deliberately did not touch

`src/zsc_lossless.py` is **additive**. `zspectral_compression.py` keeps
its tokenization unchanged except for the log 005 transpose fix,
because that file is GraphModel's atomic unit and shifting its
segmentation would shift the model's input.

Four measured findings, implemented:

| # | change | from | measured payoff |
|---|---|---|---|
| 1 | rate criterion — keep a node when that costs fewer bits than splitting, not when its error is under a constant | log 006 | 2.51x -> 25.89x on smooth data |
| 2 | per-segment mode: degree 0/1/2/3 **or raw** | log 007 §8, log 009 | degree 0 wins on text/binary/photo, degree 3 on smooth; raw bounds the worst case |
| 3 | traversal chosen per volume — each axis-fastest, plus Morton | log 010 | up to 16.8x on video |
| 4 | a real correction stream, so output is lossless and round-trips | log 006 | makes any of the above usable |

Plus two things the build itself forced:

- **A whole-file stored escape.** The format may never cost more than
  the bytes plus a short header. Break-even is now structural.
- **A container choice.** Packed alone, every segment is
  independently decodable. Wrapped in lzma the ratio improves —
  often a lot, because lzma catches the repetition a polynomial model
  structurally cannot see — but decoding becomes sequential. This is
  log 008's trade, made explicit as a parameter rather than assumed.

## 2. Verification

**Every round-trip is byte-exact.** `Tools/test_codec_roundtrip.py`:

| input | addressable | sequential | `xz -9` | order chosen | round-trip |
|---|---|---|---|---|---|
| python source | 1.13x | 1.86x | 3.80x | axis0 | EXACT |
| english prose | 1.03x | 1.68x | 2.72x | axis0 | EXACT |
| elf binary | 1.00x | 3.15x | 3.31x | axis0 | EXACT |
| pure random | 1.00x | 1.00x | 1.00x | **stored** | EXACT |
| photo tile 2-D | 1.23x | **1.91x** | 1.81x | morton | EXACT |
| smooth signal 1-D | 5.24x | 14.54x | 26.09x | axis0 | EXACT |
| video: static scene 3-D | 3.53x | 29.65x | 35.16x | **axis2** | EXACT |
| video: moving disc 3-D | 3.08x | 38.06x | 44.04x | **morton** | EXACT |
| game: static 3-D field x time | 1.77x | **27.48x** | 25.72x | **axis3** | EXACT |
| game: voxel terrain x time | 1.77x | **40.03x** | 31.51x | **axis3** | EXACT |

Three things to read off it:

- **Nothing is below 1.00x, on any input, including pure random** —
  the stored escape fires and the format reports it.
- **The traversal chooser works unsupervised**: time-major for static
  video, Morton for the moving disc, axis3 for the 4D volumes, and
  it was never told which.
- **The sequential container beats `xz -9` on three inputs** — photo
  tile, static 3-D field, voxel terrain — which no configuration in
  logs 001-010 managed.

### The honest cost of addressability

The addressable column is much lower than the sequential one because
its residuals are bit-packed per segment (constant stride, so a
segment decodes without walking its predecessors) rather than
entropy-coded across the file. That gap **is** log 008's theorem in
practice: buying random access costs redundancy above the entropy.

## 3. Game-shaped data

`Tools/test_game_data.py`:

| data | addressable | sequential | `xz -9` | order |
|---|---|---|---|---|
| terrain heightmap 256x256 | 1.17x | **3.46x** | 2.99x | axis0 |
| light field 32^3, values 0..15 | 3.06x | 8.90x | **30.57x** | morton |
| minecraft-ish chunk 32^3 (block IDs) | 1.83x | 17.84x | **24.60x** | axis0 |
| chunk x 16 ticks, edits only | 5.38x | 108.93x | **172.92x** | **axis3** |
| entity positions 64x3x256 | 1.72x | 4.47x | **5.11x** | axis2 |

**ZSC wins the heightmap** — a genuinely sampled continuous function —
and loses everything whose redundancy is runs or repeats.

### The categorical problem, stated plainly

Block IDs are **categorical, not numeric.** Block 5 is not "between"
block 4 and block 6, so fitting a polynomial through them models a
relationship that does not exist. Only degree 0 — a constant run — is
semantically meaningful for them, and degree-0 segmentation is
run-length encoding, which every voxel format already does better.

This is not a tuning problem and no basis fixes it (log 007 §9.1). It
is a statement about what the data *is*.

## 4. Still open

- **Per-region traversal**, rather than per-volume. A static
  background and a moving foreground want different orders. That is
  what motion compensation buys a conventional codec, reached another
  way. Unmeasured.
- **Entropy-coded residuals inside the addressable container**, with a
  per-segment offset table instead of constant stride. Would close
  part of the gap in §2 at the cost of an index — exactly the
  redundancy-versus-access trade, made explicit.
- The rate criterion is currently applied at a uniform segment length
  chosen globally, not descended per node through the pyramid.

## 5. See also

- `~/Programming/PUBLIC/ZSpectralCompression/src/zsc_lossless.py` — the module.
- `~/Programming/PUBLIC/ZSpectralCompression/DevComms/log_010_time_and_higher_dimensions.md`
  — where the traversal finding came from.
