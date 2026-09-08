---
id: zspectral.algebra.spectral_tensor
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: spectral_tensor
    path: Planning/node_0_0_algebra/node_0_0_1_spectral_tensor/CORE_0_0_1_spectral_tensor.md
super_node:
    name: algebra
    path: ../CORE_0_0_algebra.md
sub_nodes: []
---

# CORE 0_0_1 — spectral_tensor

## metadata

- **id:** zspectral.algebra.spectral_tensor
- **level:** 2
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [algebra](../CORE_0_0_algebra.md)

## sub_nodes

*(none yet)*

## definition

The value: a pair of tensors, `coeffs` and `meta`.

`coeffs` is shaped `[..., Segments, Bounds, Chebyshev]`, where
`Bounds` is 2 — a lower and an upper curve, so that error is part of
the value rather than a separate report — and `Chebyshev` is 4.

The class holds no arithmetic. `__add__`, `__mul__` and `__matmul__`
delegate to [spectral_algebra](../node_0_0_5_spectral_algebra/CORE_0_0_5_spectral_algebra.md);
`shape` and `T` report and transpose only the logical dimensions,
excluding the three physics dimensions on the right.
