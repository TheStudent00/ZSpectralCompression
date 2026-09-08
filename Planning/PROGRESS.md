---
id: zspectral.progress
status: in-progress
---

# PROGRESS — ZSpectralCompression

## metadata

- **id:** zspectral.progress
- **status:** in-progress

## where the implementation stands

| item | status | evidence |
|---|---|---|
| prototype exists and runs on images | done, undated (predates this plan) | `~/Programming/ZSpectralCompression/zspectral_compression.py`, `ZSpectral_Compression.ipynb` |
| plan reverse-engineered from the prototype | in-progress, opened 2026-09-08 | this tree |
| 1D behaviour measured | done 2026-09-08 | `DevComms/log_001_one_dimensional_measurements.md` §2 |
| codebook cost/residual trade measured | done 2026-09-08 | log_001 §2, follow-up run |
| index-stream residual entropy measured | done 2026-09-08 | log_001, follow-up run |
| Z-order edit locality measured | done 2026-09-08 | log_001 §4 |
| lossless mode | planned | see node_0_6_open_work |
| stride discovery | planned | see node_0_6_open_work |

## notes

- No node below level 0 has been settled. The whole tree is `draft`.
- The prototype has no test suite. Every CHECK in this tree is
  currently a by-hand `.md` question, not an executable check.
