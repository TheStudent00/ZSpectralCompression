---
id: zspectral.findings.edit_locality
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: finding
node:
    name: edit_locality
    path: Planning/node_0_5_findings/node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md
super_node:
    name: findings
    path: ../CORE_0_5_findings.md
sub_nodes: []
---

# CORE 0_5_3 — edit_locality

## metadata

- **id:** zspectral.findings.edit_locality
- **level:** 2
- **stat## definition

What the Z-order traversal is worth when data changes. Measured
2026-09-08, with no compression involved at all: a 1024x1024 field cut
into 4096-byte chunks, chunks hashed, an edit applied, changed hashes
counted.

| edit | raster order | Z-order |
|---|---|---|
| 64x64 square, aligned | 16/256 | **1/256** |
| 64x64 square, unaligned | 17/256 | **4/256** |
| 128x128 square | 32/256 | **4/256** |
| one full row | **1/256** | 16/256 |
| one full column | 256/256 | **16/256** |
| four scattered 32x32 squares | 24/256 | **8/256** |

## what it says

- **A compact edit in two dimensions is scattered in one.** Under row
  order a 64x64 square touches 16 separate chunks; under Morton order
  it is one contiguous run.
- **The curve trades the best case for the worst case.** Row order
  wins on row-shaped edits, 1 against 16, and is catastrophic on
  column-shaped ones, 256 against 16 — one changed byte per row
  invalidates every chunk in the image. Z-order is never optimal and
  never pathological.
- For edits whose shape is not known in advance, that trade is the
  right one.

## why this is separable from compression

Nothing above involves a polynomial, a codebook or a threshold. The
result holds for any format whose units are independent and laid along
the curve, which is what
[chunker_framing](../../node_0_6_open_work/node_0_6_2_chunker_framing/CORE_0_6_2_chunker_framing.md)
follows up.
6-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_5_findings/CORE_0_5_findings.md; the definition and `designation` are the owner's to
write.)*
