# log 010 — video, 3D and 3+1D: the traversal order is the whole game

Repo: `~/Programming/PUBLIC/ZSpectralCompression`. Written 2026-09-09 by
Claude. Airlock `sandbox-runner`. Tools: `Tools/test_axis_order.py`,
`Tools/compare_curves.py`.

the owner, 2026-09-09:

> what im super curious about is video files since ZSC could actually
> compress through time, not just each image. also curious about 3D
> and even 3+1D such as gaming.

---

## 1. The headline

**It works, and the prototype's fixed Morton interleave is the worst
possible choice for the content it works best on.**

32x32 frames x 32 frames, lossless, only the traversal order changes:

| content | per-frame (2-D) | frame-major (x fastest) | **time-major (t fastest)** | morton 3-D |
|---|---|---|---|---|
| static scene, no change | 3.26x | 3.61x | **24.98x** | 1.49x |
| static scene, slow fade | 3.44x | 3.61x | 3.21x | 1.49x |
| moving disc | 3.58x | 3.32x | 3.39x | **4.78x** |
| real photo, panning 1 px/frame | 1.69x | 1.72x | 1.66x | **1.93x** |

On a static scene, time-major reaches **24.98x where Morton reaches
1.49x — a factor of 16.8.** On content with real motion, Morton is the
best of the four, but only by 1.4x.

### Why

Order the volume time-fastest and each pixel's own time series becomes
one contiguous run. For static content that run is *constant*, which a
degree-0 segment fits exactly — one coefficient for thirty-two
samples. Morton interleaves the bits of x, y and t, so a token covers
a small cube in all three axes at once and never sees a pure time run.

## 2. The same thing in 3+1D

16x16x16 volumes over 16 timesteps — the shape a game's light-probe
grid, fog volume or voxel chunk actually has:

| content | per-frame (3-D) | **time-major** | morton 4-D |
|---|---|---|---|
| static 3-D field over time | 2.62x | **12.72x** | 1.48x |
| moving light through volume | 1.62x | 1.42x | **1.81x** |
| blocky voxel terrain, static | 1.48x | **12.72x** | 1.39x |

The third row is the one worth stopping on. **Blocky voxel terrain —
discrete, hard-edged, exactly the content this codec is supposed to be
bad at — reaches 12.72x.** Because it does not change over time, and
time-major makes every voxel a constant run.

## 3. What that corrects about this project's own framing

Logs 001-007 kept saying "smooth data versus symbol data". That is the
wrong axis. The right statement:

> **What matters is whether there exists an axis along which the values
> vary slowly. Not whether the data as a whole is smooth.**

Blocky terrain is not smooth in x, y or z. It is perfectly constant in
t. One good axis is enough, and the traversal has to be chosen to walk
along it.

## 4. Design consequence

The traversal order is currently fixed — `_ZCurveRouter` always
interleaves every axis. It should be **chosen per volume**, the same
way segment length and (per log 007 §8) degree should be:

- try the handful of candidate orders — each axis fastest, plus the
  Morton interleave;
- price each with the existing machinery;
- keep the cheapest, and store the choice in a few bits of header.

For an N-dimensional volume that is N+1 trials, and the measurements
above say the payoff is up to 16.8x on the content video actually
consists of.

A stronger version, not measured: choose the order **per region**, so
a static background and a moving foreground get different traversals.
That is what motion compensation buys a conventional codec, reached by
a different route.

## 5. A hypothesis tested and rejected: Hilbert instead of Morton

Morton order jumps. Measured on a 32x32 grid: **50.0% of consecutive
Morton steps move more than one cell, with a maximum step of 32** —
the full width. A Hilbert curve never jumps; every step is exactly 1.
Since a polynomial models continuity, Hilbert looked like it should
fit much better.

It does not:

| image (128x128, lossless) | raster | morton | hilbert |
|---|---|---|---|
| photo tile | 1.50x | 1.86x | **1.86x** |
| smooth 2-D field | **11.21x** | 1.98x | 1.99x |
| random noise | 1.00x | 1.00x | 1.00x |

Hilbert buys **+0% to +1%**. The jumps were not the problem.

And edit locality — the property the curve exists for — is identical
on both:

| edit (1024x1024, 4096-byte chunks) | morton | hilbert |
|---|---|---|
| 64x64 square | 1/256 | 1/256 |
| 128x128 square | 4/256 | 4/256 |
| one full row | 16/256 | 16/256 |
| one full column | 16/256 | 16/256 |

**So there is no reason to switch curves.** Recorded because the
hypothesis was reasonable and is now closed.

### What the curve does cost

The middle row above is the real finding: on a smooth 2-D field,
**raster order reaches 11.21x where both space-filling curves reach
about 1.98x.** A space-filling curve preserves locality but not
*direction* — it turns constantly, so a smooth gradient becomes a
wandering path rather than a monotone sweep, and a polynomial cannot
follow it.

On a real photo the curve wins instead (1.86x against 1.50x), because
photographic texture has no consistent gradient direction and locality
is what pays. So the curve is the right default for images and the
wrong one for fields with global structure — which is §4's argument
again, one dimension lower.

## 6. See also

- `~/Programming/PUBLIC/ZSpectralCompression/Planning/node_0_1_geometry/node_0_1_1_z_curve_router/CORE_0_1_1_z_curve_router.md`
  — the node this concerns.
- `~/Programming/PUBLIC/ZSpectralCompression/DevComms/log_008_ratio_versus_usability.md`
  — the granularity trade this extends into N dimensions.
