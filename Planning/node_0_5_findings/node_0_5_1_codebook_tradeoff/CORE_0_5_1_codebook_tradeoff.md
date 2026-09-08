---
id: zspectral.findings.codebook_tradeoff
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: finding
node:
    name: codebook_tradeoff
    path: Planning/node_0_5_findings/node_0_5_1_codebook_tradeoff/CORE_0_5_1_codebook_tradeoff.md
super_node:
    name: findings
    path: ../CORE_0_5_findings.md
sub_nodes: []
---

# CORE 0_5_1 — codebook_tradeoff

## metadata

- **id:** zspectral.findings.codebook_tradeoff
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

What the k-means codebook does to the cost, measured 2026-09-08 at
K = 256 against the same files.

| file | lossless via codebook | lossless with exact coefficients |
|---|---|---|
| Python source | **6.95** | 9.28 |
| English prose | **7.37** | 9.75 |
| smooth 1D | 1.92 | **1.41** |
| smooth 2D raw | 2.85 | **1.79** |

Bits per byte, residual plus the cost of naming the fit.

## what it says

the owner's expectation — that indexing a table of fits rather than storing
a unique fit per segment makes the coefficient cost roughly neutral —
is correct about the coefficients, and the direction it moves the
total depends on the data.

- **The trade is coefficient cost against residual cost.** An index
  costs 1 byte where four exact coefficients cost about 2.3 bits per
  source byte more. But the reconstruction from a centroid is worse
  than the reconstruction from the segment's own fit, so the residual
  grows.
- **On symbol data the codebook wins**, because the fits are near
  random and expensive to store exactly, and the residual was already
  near maximal so it has little room to worsen.
- **On smooth data the codebook loses**, because the exact fit is
  nearly perfect and the residual is where all the remaining cost is.

Neither column reaches the raw `H0` of the symbol files (4.86–4.88),
so the method is still a loss there.
