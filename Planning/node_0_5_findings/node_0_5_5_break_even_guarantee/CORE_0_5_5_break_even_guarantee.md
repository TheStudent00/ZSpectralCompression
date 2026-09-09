---
id: zspectral.findings.break_even_guarantee
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: finding
node:
    name: break_even_guarantee
    path: Planning/node_0_5_findings/node_0_5_5_break_even_guarantee/CORE_0_5_5_break_even_guarantee.md
super_node:
    name: findings
    path: ../CORE_0_5_findings.md
sub_nodes: []
---

# CORE 0_5_5 — break_even_guarantee

## metadata

- **id:** zspectral.findings.break_even_guarantee
- **level:** 2
- **status:** draft
- **designation:** finding
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [findings](../CORE_0_5_findings.md)

## sub_nodes

*(none yet)*

## definition

Whether ZSC ever costs more than storing the bytes raw. Measured
2026-09-09 against the owner's bar:

> if we can guarantee that under most (if not all) conditions that ZSC
> at worst breaks even in compression, its a massive unexpected
> victory.

## the test

Ten inputs at 256-byte random-access granularity, all lossless,
including four chosen to be hostile: pure random bytes, an already
zstd-compressed stream, PNG file bytes and JPEG file bytes — data with
no numeric smoothness left in it at all.

| input | ZSC as-is | ZSC + raw escape | zstd @256 B |
|---|---|---|---|
| pure random bytes | **0.990x** | 0.998x | 1.000x |
| already zstd-compressed | 1.003x | 1.011x | 1.000x |
| PNG file bytes | **0.987x** | 0.998x | 1.011x |
| JPEG file bytes | **0.992x** | 0.998x | 1.005x |
| alternating 0,255 | 7.642x | 7.642x | 25.600x |
| sawtooth period 7 | 1.995x | 1.995x | 17.067x |
| ELF binary | 1.048x | 1.048x | 1.822x |
| python source | 1.225x | 1.225x | 1.691x |
| photo tile | **1.478x** | 1.478x | 1.247x |
| smooth signal | **22.223x** | 22.223x | 11.674x |

## the answer

**As it stands, no — three inputs fall below 1.0**, and all three are
data with the smoothness already squeezed out. The loss is about 1%.

**With a per-segment raw escape, yes, and by construction.** Each
segment picks the cheapest of degree 0, 1, 2, 3 or *store the bytes
untouched*, and 2 bits of mode flag record the choice. A segment can
then never cost more than the bytes it holds, so the worst case is
bounded by the flag overhead alone:

    2 bits per 256-byte segment = 0.098%

The measured 0.998x is exactly that flag plus the fixed header. **The
bound is a guarantee, not an observation** — it holds for any input,
including adversarial ones, because the escape is checked per segment
rather than hoped for.

This is the standard mechanism: deflate has stored blocks, JPEG has an
escape, every production codec carries one. ZSC does not currently
implement it.

## what this settles

The bar the owner set is met, conditional on adding the escape. Two further
readings:

- **ZSC-as-is is already within 1% on pure random data.** That is
  better than a transform codec has any right to be, and it is because
  the residual is entropy-coded rather than the coefficients being
  trusted.
- On the two inputs where it beats zstd at matched granularity —
  photo tile 1.478x against 1.247x, smooth signal 22.223x against
  11.674x — it does so while remaining randomly addressable, which is
  the property `~/Programming/GraphModel` actually needs.

Record: `~/Programming/ZSpectralCompression/DevComms/log_009_break_even.md`.
