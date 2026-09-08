---
id: zspectral.algebra
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: algebra
    path: Planning/node_0_0_algebra/CORE_0_0_algebra.md
super_node:
    name: zspectral
    path: ../CORE_0.md
sub_nodes:
    - name: spectral_layout
      path: node_0_0_0_spectral_layout/CORE_0_0_0_spectral_layout.md
    - name: spectral_tensor
      path: node_0_0_1_spectral_tensor/CORE_0_0_1_spectral_tensor.md
    - name: chebyshev_math
      path: node_0_0_2_chebyshev_math/CORE_0_0_2_chebyshev_math.md
    - name: spectral_topology
      path: node_0_0_3_spectral_topology/CORE_0_0_3_spectral_topology.md
    - name: kinematic_physics
      path: node_0_0_4_kinematic_physics/CORE_0_0_4_kinematic_physics.md
    - name: spectral_algebra
      path: node_0_0_5_spectral_algebra/CORE_0_0_5_spectral_algebra.md
---

# CORE 0_0 — algebra

## metadata

- **id:** zspectral.algebra
- **level:** 1
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [zspectral](../CORE_0.md)

## sub_nodes

*(rebuilt by the generator)*

## definition

The value type the whole project operates on — a piecewise Chebyshev
spline carrying an upper and a lower bound at every point — and the
arithmetic closed over it.

## design

A value is a pair of tensors, and both are needed to say what it is:

- `coeffs`, shaped `[... , Segments, Bounds, Chebyshev]`. `Bounds` is
  2, holding a lower and an upper curve; `Chebyshev` is 4, holding
  the degree-3 coefficients. Carrying two curves rather than one is
  what makes error a first-class part of the value instead of a
  separate report.
- `meta`, shaped `[... , Channels]`, holding
  `z_real, z_virt, m_real, m_virt, L, confidence`.

Two facts about this module that matter for the rest of the tree:

- **It is larger than the codec needs.** The codec uses only
  `upsample_to_match` and `enforce_left_complexity` from
  [spectral_topology](node_0_0_3_spectral_topology/CORE_0_0_3_spectral_topology.md).
  Addition, multiplication, matrix multiplication, composition and
  integration are a separate capability: interval arithmetic on
  functions represented as splines. Nothing in the compression path
  calls them.
- **`spectral_layout` is the reason there are no magic numbers.**
  Every axis index in the module is derived from the key lists in one
  class, so a change to the representation is one edit.

## open

- Whether the function-arithmetic half belongs in this repo at all,
  or is its own project, is unsettled. It is recorded here because it
  exists in the prototype, not because the placement is decided.
