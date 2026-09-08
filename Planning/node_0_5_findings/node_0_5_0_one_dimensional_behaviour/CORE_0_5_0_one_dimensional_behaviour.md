---
id: zspectral.findings.one_dimensional_behaviour
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: finding
node:
    name: one_dimensional_behaviour
    path: Planning/node_0_5_findings/node_0_5_0_one_dimensional_behaviour/CORE_0_5_0_one_dimensional_behaviour.md
super_node:
    name: findings
    path: ../CORE_0_5_findings.md
sub_nodes: []
---

# CORE 0_5_0 — one_dimensional_behaviour

## metadata

- **id:** zspectral.findings.one_dimensional_behaviour
- **level:*## definition

What the polynomial basis does to one-dimensional data that is not a
sampled signal. Measured 2026-09-08; the prototype had never been run
on 1D input.

| file | raw H0 | after the fit | change |
|---|---|---|---|
| C++ source | 5.17 | 5.88 | +0.71 |
| Python source | 4.88 | 5.87 | +0.99 |
| English prose | 4.86 | 6.32 | +1.46 |
| ELF binary | 6.19 | 7.48 | +1.29 |
| smooth 1D signal | 7.56 | **0.32** | **-7.24** |

Bits per byte. `H0` is the order-0 entropy of the raw bytes; the
third column is the order-0 entropy of the fit residual.

## what it says

- **On symbol data the transform raises entropy.** A degree-3
  polynomial through eight arbitrary byte values predicts nothing, and
  the residual is more uniform than the source was. The structure that
  was there — letter and opcode frequency — is destroyed by the fit.
- **On a sampled signal it wins by a factor of about 25**, and it wins
  precisely where a histogram-based coder cannot: that file's byte
  histogram carries 7.56 of 8 bits.
- The dividing line is the model, not the dimension. Smoothness is an
  assumption about the data; text does not satisfy it and no amount of
  tuning will make it.

## what it does not say

The harness is a fixed 8-sample window, not the adaptive pyramid — see
[findings](../CORE_0_5_findings.md). These residual figures are a fair
test of whether the basis fits; the totals derived from them are not a
fair test of the prototype's ratio.
enerated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_5_findings/CORE_0_5_findings.md; the definition and `designation` are the owner's to
write.)*
