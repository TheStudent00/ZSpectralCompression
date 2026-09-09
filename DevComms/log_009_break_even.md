# log 009 — the break-even bar, and what ZSC is actually for

Repo: `~/Programming/ZSpectralCompression`. Written 2026-09-09 by
Claude. Airlock `sandbox-runner`. Tool: `Tools/test_break_even.py`.

the owner, 2026-09-09:

> i created it to solve the universal input problem for a generalized
> intelligent model (`~/Programming/GraphModel`). the spirit of it
> wasnt compression at all but if we can guarantee that under most (if
> not all) conditions that ZSC at worst breaks even in compression,
> its a massive unexpected victory.

---

## 1. What this changes about everything in logs 001-008

The primary object is the **representation**. Compression is a
constraint to satisfy, not a goal to maximise.

`~/Programming/GraphModel/ComponentDefense/Signal/DesignUpdates_2.md`
carries the same structure as the atomic unit of the Fractal-Aperture
Spectral Transformer:

> **Atomic Unit: The Spectral Token** — Structure: A single segment,
> Order 3 Chebyshev Spline. Heteroscedastic Uncertainty: Modeled via a
> Dual-Curve Interval ([L, U]) to capture skew.

and the ontology those `meta` channels serve:

> The architecture redefines tokens and weights as physical objects
> interacting in a complex-valued field ($M = m_{real} + i \cdot
> m_{virt}$ and $Z = z_{real} + i \cdot z_{virt}$).

Three things this tree had recorded as puzzles are now answered:

| recorded as | actually |
|---|---|
| "nothing in the compression path calls `SpectralAlgebra`" (`node_0_0_algebra`) | correct, and not a defect — it is GraphModel's message passing |
| "the `meta` channels never reach the payload" (`node_0_2_0_4_physics_minter`) | correct, and not a defect — they are the complex neural physics |
| "the dual lower/upper curve collapses to an average at decode" (`node_0_2_1_1_signal_assembler`) | it collapses *for the codec*; for the model it is heteroscedastic uncertainty carried through every operation |

Also worth flagging as a possible divergence to check, not a defect
found: the design document specifies **symmetric** null padding, "to
both ends of the sequence", to keep the centre of mass unskewed.
`_GlobalCanvasFramer.pad_to_pow2` pads only at the high end of each
axis. For compression that is irrelevant; for a centre-of-mass
calculation it may not be.

## 2. The break-even test

Ten inputs at 256-byte random-access granularity, all lossless, four
of them chosen to be hostile — data with no numeric smoothness left in
it at all.

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

### 2.1 As it stands: no, by about 1%

Three inputs fall below 1.0 — random bytes, PNG bytes, JPEG bytes. All
three are already-compressed or structureless data. The shortfall is
1.0% to 1.3%.

### 2.2 With a per-segment escape: yes, and by construction

Let each segment pick the cheapest of degree 0, 1, 2, 3 **or store its
bytes untouched**, with 2 bits of mode flag recording the choice. A
segment can then never cost more than the bytes it holds, so the worst
case over the whole file is bounded by the flag alone:

    2 bits per 256-byte segment = 0.098%

The measured 0.998x is exactly that flag plus the fixed header. **This
is a guarantee rather than an observation** — it holds for adversarial
input because the escape is a per-segment comparison, not a hope about
the data.

The mechanism is standard: deflate has stored blocks, JPEG has an
escape hatch, every production codec carries one. ZSC does not
currently implement it, and it is a small change to the payload format
plus a comparison in the walker.

### 2.3 Two things worth noticing

- **ZSC-as-is is already within 1% on pure random data.** A transform
  codec has no right to that, and it holds because the residual is
  entropy-coded rather than the coefficients being trusted.
- On the two inputs where it beats zstd at matched granularity —
  photo tile 1.478x against 1.247x, smooth signal 22.223x against
  11.674x — it does so **while remaining randomly addressable**, which
  is the property GraphModel actually needs from it.

## 3. The answer to the bar as set

> at worst breaks even in compression

**Met, conditional on adding the per-segment escape**, with a worst
case of 0.998x that shrinks as segments grow. And on the data classes
GraphModel is likely to feed it — images, sampled signals, N-D arrays
— it is not breaking even, it is winning at matched granularity.

## 4. What this asks of the plan

- `Planning/CORE_0.md` now records the purpose, at level 0, from the owner's
  own statement.
- `node_0_0_algebra` had "whether the function-arithmetic half belongs
  in this repo" open. Settled: it is the point.
- New finding node `node_0_5_5_break_even_guarantee`.
- The escape belongs in `node_0_6_open_work` as the next concrete
  build item; it is small, it is bounded, and it converts a measured
  1% loss into a proved guarantee.

## 5. See also

- `~/Programming/GraphModel/ComponentDefense/Signal/DesignUpdates_2.md`
  — the FAST specification quoted in §1.
- `~/Programming/ZSpectralCompression/DevComms/log_008_ratio_versus_usability.md`
  — the matched-granularity comparison this extends.
