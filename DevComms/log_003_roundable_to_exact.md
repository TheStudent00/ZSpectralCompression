# log 003 — "exact" means roundable, and that changes the lossless answer

Repo: `~/Programming/ZSpectralCompression`. Written 2026-09-08 by
Claude. Airlock `sandbox-runner`, pure Python.

the owner, 2026-09-08:

> to be clear, "exact" means reconstruct. so it needs to be roundable
> to exact, as opposed to exact without rounding.

Correct, and it is the right criterion for byte data. The measurement
below is per-sample: does the fitted value, rounded to the nearest
integer, equal the original byte. The previous logs measured residual
entropy without ever asking how often the residual is simply zero.

---

## 1. Confirming the codebook exists, since it was asserted before it was shown

the owner:

> wait how is k-means being applied? [...] but also you didnt confirm
> the existence of the indexed curves in the prototype.

Fair. `~/Programming/ZSpectralCompression/zspectral_compression.py`
line 17:

> `from sklearn.cluster import KMeans`

and lines 1150–1162, inside `ZSpectralCompressor.compress`:

> ```
> # 3. AC/DC Separation & Vector Quantization
> c0 = mean_coeffs[:, 0]
> shapes = mean_coeffs[:, 1:].cpu().numpy()
>
> c0_clamped = torch.clamp(c0, 0.0, 1.0)
> c0_quantized = (c0_clamped * 255.0).to(torch.uint8)
>
> scaler = StandardScaler()
> scaled_shapes = scaler.fit_transform(shapes)
>
> n_clusters_actual = min(self.k_clusters, shapes.shape[0])
> kmeans = KMeans(n_clusters=n_clusters_actual, random_state=42, n_init='auto')
> labels = kmeans.fit_predict(scaled_shapes)
> shape_centroids = scaler.inverse_transform(kmeans.cluster_centers_)
> ```

So: `mean_coeffs[:, 0]` is `c0`, quantised directly to a uint8;
`mean_coeffs[:, 1:]` is `c1, c2, c3`, standardised and clustered, with
the token storing the cluster index. `k_clusters` defaults to 128
(line 1124) and the final run uses 64 (line 1493, `optimal_k = 64`).

**`fast_pytorch_kmeans` at line 1024 is dead code** — defined, never
called. The sklearn path at 1160 is the live one, and it runs on the
CPU, per tile.

---

## 2. Round-exact by window length

Fraction of samples whose degree-3 fit rounds to the original byte,
and the order-0 entropy of the correction stream for the rest.

| file | window | rounds exact | correction |
|---|---|---|---|
| python_source | 4 | **100.0%** | 0.00 |
| | 8 | 7.8% | 5.87 |
| | 16 | 3.0% | 6.35 |
| | 32 | 1.8% | 6.65 |
| english_prose | 4 | **100.0%** | 0.00 |
| | 8 | 2.6% | 6.32 |
| | 32 | 1.0% | 6.59 |
| elf_binary | 4 | **100.0%** | 0.00 |
| | 8 | 7.5% | 7.40 |
| | 32 | 2.2% | 7.87 |
| smooth_1d | 4, 8, 16 | **100.0%** | 0.00 |
| | 32 | 99.2% | 0.08 |
| smooth_2d_raw | 4, 8 | **100.0%** | 0.00 |
| | 16 | 99.5% | 0.05 |
| | 32 | 98.0% | 0.17 |

Bits per byte in the correction column.

**Window 4 is 100% for every file including the ELF binary**, and that
is not a property of the data. Four coefficients through four points
is a square system, so the leaf fit is algebraically exact — which is
what `VisionGeometryConfig` sets up with `min_patch_size = 4`. It also
buys nothing: four coefficients for four bytes.

Everything after that is the merge, and the merge is where the two
classes of data separate completely. Text falls off a cliff at the
first merge — 100% to 7.8%. Smooth data does not fall off at all.

---

## 3. How far the merge can go on smooth data, and what lossless costs there

Extending the same measurement, with the coefficient cost written
beside it. Coefficient cost assumes four float32 per segment
(128 bits), which is the pessimistic case.

| file | window | rounds exact | correction | coefficients | **lossless total** |
|---|---|---|---|---|---|
| smooth_1d | 32 | 99.2% | 0.08 | 4.00 | 4.08 |
| | 64 | 97.8% | 0.17 | 2.00 | 2.17 |
| | 128 | 97.6% | 0.19 | 1.00 | 1.19 |
| | 256 | 97.8% | 0.18 | 0.50 | 0.68 |
| | 512 | 97.8% | 0.18 | 0.25 | **0.43** |
| smooth_2d_raw | 32 | 98.0% | 0.17 | 4.00 | 4.17 |
| | 128 | 89.2% | 0.82 | 1.00 | 1.82 |
| | 512 | 16.1% | 4.60 | 0.25 | 4.85 |
| python_source | 32 | 1.8% | 6.65 | 4.00 | 10.65 |
| | 512 | 0.3% | 6.54 | 0.25 | 6.79 |

Bits per byte.

### What this settles

- **Lossless via this route is viable on smooth data, and it needs
  long segments.** At 512 samples per segment, `smooth_1d` costs
  0.43 bits per byte against `xz -9` at 0.28. Quantising the
  coefficients to 16 bits each instead of 32 would put it at about
  0.31 — level with `xz`, on data whose byte histogram carries
  7.56 of 8 bits and where a histogram coder gets nothing.
- **The correction stream plateaus at 0.18 bits per byte** and stops
  improving past window 128. That is the floor from the source signal
  having been quantised to bytes in the first place, not a limit of
  the fit.
- **Text does not become viable at any window length.** 0.3% round
  exact at 512, correction 6.54 bits per byte. This is now measured
  across five window lengths and is not an artifact of one choice.

### A limitation of this harness that runs the other way

`smooth_2d_raw` degrades badly as the window grows — 98.0% at 32 down
to 16.1% at 512. **That is my harness, not the method.** I read the
file as a flat 1D stream in raster order, so a 512-sample window is a
512-long strip spanning half a row of a 1000-wide field, and a
degree-3 polynomial cannot follow that.

Under the prototype's Z-order traversal a 512-sample window is a
compact tile of roughly 23x23, over which the field is far flatter.
So the 2D row is a floor for the real pipeline, and the gap between
these numbers and the prototype's is a measurement of what the
space-filling curve is worth for compression — separate from what
[edit_locality](../Planning/node_0_5_findings/node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md)
measured it to be worth for addressing.

---

## 4. Two things in the final showcase cell, found while checking §1

Lines 1480–1568 of the prototype, the tiled JWST run.

### 4.1 The codebook is counted once per channel but built once per tile

> ```
> total_compressed_bytes += (metrics['breakdown']['labels'] +
>                          metrics['breakdown']['c0'] +
>                          metrics['breakdown']['topology'])
> if not codebook_paid[i]:
>     total_compressed_bytes += metrics['breakdown']['codebook']
>     codebook_paid[i] = True
> ```

`compress` runs KMeans per call, so each of the tiles in a channel
produces its own codebook, and a decoder needs all of them. The
accounting charges one.

**Magnitude: negligible.** At `optimal_k = 64` a codebook is
`64 * 3 * 4 = 768` bytes; an 84 MB three-channel image at
`tile_size = 1024` is roughly 36 tiles per channel, so the
undercount is about 27 KB against a reported 20.13 MB — 0.13%. Worth
fixing for correctness, not a threat to the reported 4.17x.

### 4.2 The displayed reconstruction is a JPEG of the reconstruction

> ```
> TF.to_pil_image(color_canvas.cpu()).save("jwst_final_goldilocks.jpg", quality=100)
> ...
> reconstructed_img = Image.open("jwst_final_goldilocks.jpg")
> ```

The side-by-side figure compares one JPEG against another JPEG. Both
sides carry JPEG artifacts that are not attributable to this codec,
in both directions — it can hide the codec's errors and add errors
the codec did not make. A PNG round-trip would make the figure say
what it claims to say.

### 4.3 The reported ratio is pessimistic, by the amount in log 002

`calculate_metrics` counts labels at one byte each.
`~/Programming/ZSpectralCompression/DevComms/log_002_codebook_indices_and_plan.md`
§2 measured label streams compressing to 1.50–2.04 bits under `xz`.
Labels and `c0` are one byte per token each, so labels are roughly
half the counted payload. Entropy-coding them would move the reported
4.17x upward materially. **Unverified on the JWST run itself** — that
estimate is from the label streams of a different data set, and the
honest way to state it is that the number is a floor.

---

## 5. See also

- `~/Programming/ZSpectralCompression/DevComms/log_002_codebook_indices_and_plan.md`
  — the codebook and index-stream measurements this continues.
- `~/Programming/ZSpectralCompression/Planning/node_0_6_open_work/node_0_6_0_lossless_mode/CORE_0_6_0_lossless_mode.md`
  — the node this partly answers.
