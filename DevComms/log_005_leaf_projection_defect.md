# log 005 — the leaf projection was transposed, and the merge never ran

Repo: `~/Programming/PUBLIC/ZSpectralCompression`. Written 2026-09-08 by
Claude. Airlock `sandbox-runner`, now carrying `torch 2.14.0+cpu`,
`torchvision`, `numpy`, `scikit-learn`, `pillow`, `zstandard`, `tqdm`
and `matplotlib`. `download.pytorch.org` and `download-r2.pytorch.org`
were added to the egress allowlist with the owner's permission
(`bash ~/Programming/PUBLIC/Airlock/allow.sh add ...`).

---

## 1. What running the prototype showed

First execution of the real pipeline, sweeping the one knob:

```
=== smooth_1d, 32768 bytes ===        (BEFORE the fix)
threshold   tokens  mean len      ratio   round-exact
    0.000     8192       4.0      1.52x        96.6%
    0.002     8192       4.0      1.52x        96.4%
    0.010     8192       4.0      1.52x        96.5%
    0.050     8192       4.0      1.52x        96.6%
```

**The threshold had no effect at any value.** Every run returned 8192
tokens of length 4 — the leaf level, untouched. The pyramid was built
and then entirely discarded. Same on a photo tile and on source code.

## 2. Why: the error at level 0 was impossible

Probing the pyramid directly:

```
pyramid over 32768 smooth samples, min_patch_size=4
 level    nodes      seg len median max_err  max max_err
     0     8192            4       1.2706       1.8039
     1     4096            8       1.7188       2.4402
   ...
    13        1        32768       2.6015       2.6015

signal range: 0.306 .. 0.902
```

A median error of 1.27 on a signal whose entire dynamic range is 0.596.
And level 0 in particular **must** be zero: four Chebyshev coefficients
through four sample points is a square system, so the leaf fit is
exact by construction. It was not.

## 3. The defect

`_BaseLeafMinter._project`, line 669 before the fix:

> ```
> def _project(self, patches):
>     return torch.matmul(patches, self.leaf_basis)
> ```

`self.leaf_basis` is `torch.linalg.pinv(A)` (line 1315) where `A` is
shaped `[points, basis]`. Reconstruction is `coeffs @ A.t()`. For that
round trip to be the identity the projection must be
`patches @ pinv(A).T`, not `patches @ pinv(A)` — the two agree only if
`A` is symmetric, and it is not.

Demonstrated on one patch:

```
A (rows = the 4 sample points, cols = T0..T3):
[[ 1.0000, -1.0000,  1.0000, -1.0000],
 [ 1.0000, -0.3333, -0.7778,  0.8519],
 [ 1.0000,  0.3333, -0.7778, -0.8519],
 [ 1.0000,  1.0000,  1.0000,  1.0000]]
is A symmetric?   False

patch           [0.31 0.42 0.55 0.61]
recon, as-is    [-0.6337  0.4876 -0.2863  0.3100]   max|err| = 0.9437
recon, with .T  [ 0.3100  0.4200  0.5500  0.6100]   max|err| = 0.0000
```

**`_DualCurveFitter.fit` at stage 4 already had it right** —
`coeffs = torch.matmul(stacked_data, A_pinv.T)`. The two stages
disagreed, and the one that was wrong is the one every error estimate
is derived from.

### The consequence, stated plainly

Every node in the pyramid carried a nonsense `max_err` between 1.2 and
2.6. The walker keeps a node only where `max_err <= threshold`, so at
any sane threshold nothing was ever kept above the leaves.

**The adaptive segmentation — the mechanism the codec compresses BY —
has never run.** Every ratio the prototype has ever reported came from
the quantisation stage alone: four samples to two bytes, less the
codebook and topology overhead. That is the 1.52x above.

## 4. After the fix

```
 level    nodes      seg len median max_err  max max_err
     0     8192            4       0.0000       0.0000
     1     4096            8       0.0000       0.0008
     2     2048           16       0.0000       0.0016
     3     1024           32       0.0013       0.0026
     4      512           64       0.0022       0.0034
     5      256          128       0.0030       0.0042
```

Level 0 is exactly zero, as the square system requires, and the error
grows gradually with segment length. The threshold now selects.

| data | threshold | tokens | mean seg | ratio | ratio (entropy-coded) | rounds exact |
|---|---|---|---|---|---|---|
| smooth_1d | 0.000 | 8192 | 4.0 | 1.52x | 1.86x | 96.5% |
| | 0.001 | 2080 | 15.8 | **4.23x** | 4.42x | 70.3% |
| | 0.004 | 135 | 242.7 | **17.03x** | 17.17x | 53.9% |
| | 0.020 | 16 | 2048.0 | **143.72x** | 148.95x | 35.9% |
| | 0.100 | 4 | 8192.0 | 574.88x | 606.81x | 2.5% |
| photo tile | 0.000 | 8192 | 4.0 | 1.52x | 1.66x | 54.6% |
| | 0.020 | 1159 | 28.3 | **5.77x** | 5.87x | 24.4% |
| | 0.100 | 512 | 64.0 | **7.76x** | 7.82x | 18.6% |
| python_source | 0.020 | 7511 | 4.4 | 1.64x | 1.69x | 25.4% |
| | 0.100 | 3537 | 9.3 | 2.97x | 3.01x | 5.6% |

The codec now has a rate-distortion curve instead of a constant.

## 5. What this invalidates

- **The tuned parameters.** `optimal_thresh = 1.1` was chosen by
  `RateDistortionOptimizer` against errors that ran 1.2 to 2.6, so 1.1
  sat inside the noise. Against correct errors, 1.1 merges everything
  into a handful of tokens. **The Pareto sweep must be re-run.**
- **The reported 4.17x on the JWST image**, for the same reason.
- Nothing in logs 001–004. Those measurements used my own fixed-window
  fit, written independently and correctly; they never called the
  prototype. The conclusion that a polynomial basis raises the entropy
  of symbol data stands, and the last row of the table above — source
  code needing threshold 0.1 to reach 2.97x, at which point only 5.6%
  of bytes survive — is the prototype agreeing with it.

## 6. What is still true about lossless

At threshold 0 the codec reaches 1.52x with 96.5% of bytes rounding
exact, not 100%, because `c0` is quantised to a uint8 and the shapes
are replaced by centroids regardless of threshold. Those are payload
stages, not merge stages, so **the merge fix does not by itself give a
lossless mode.** That still needs the correction stream added to the
payload, which the format does not currently carry.

## 7. See also

- `~/Programming/PUBLIC/ZSpectralCompression/zspectral_compression.py` —
  `_BaseLeafMinter._project` carries the fix and the reason.
- `~/Programming/PUBLIC/ZSpectralCompression/Planning/node_0_2_codec/node_0_2_0_encoder/node_0_2_0_0_base_leaf_minter/CORE_0_2_0_0_base_leaf_minter.md`
  — the node for the defective stage. Its claim that "the leaf fit is
  algebraically exact" was true of the design and false of the code.
