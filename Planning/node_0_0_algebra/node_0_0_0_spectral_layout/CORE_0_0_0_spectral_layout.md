---
id: zspectral.algebra.spectral_layout
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: spectral_layout
    path: Planning/node_0_0_algebra/node_0_0_0_spectral_layout/CORE_0_0_0_spectral_layout.md
super_node:
    name: algebra
    path: ../CORE_0_0_algebra.md
sub_nodes: []
---

# CORE 0_0_0 — spectral_layout

## metadata

- **id:** zspectral.algebra.spectral_layout
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

Every axis index, key list and slice map the algebra uses, computed
once at class-definition time from four key lists.

`COEFF_DIM_KEYS = ["Segments","Bounds","Chebyshev"]` and
`META_KEYS = ["z_real","z_virt","m_real","m_virt","L","confidence"]`
are the two that decide every shape. The axis indices, the slicing
maps and the transpose axes are all derived from them, so changing
the representation is one edit here rather than a search across the
module. Its own docstring states the intent: "eliminate magic numbers
across the architecture".
