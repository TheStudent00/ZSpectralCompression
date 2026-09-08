---
id: zspectral.algebra.chebyshev_math
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: chebyshev_math
    path: Planning/node_0_0_algebra/node_0_0_2_chebyshev_math/CORE_0_0_2_chebyshev_math.md
super_node:
    name: algebra
    path: ../CORE_0_0_algebra.md
sub_nodes: []
---

# CORE 0_0_2 — chebyshev_math

## metadata

- **id:** zspectral.algebra.chebyshev_math
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

The degree-3 Chebyshev operations that do not depend on the tensor
layout.

- the 4x4x4 multiplication tensor, from the identity
  `T_i * T_j = (T_{i+j} + T_{|i-j|}) / 2`;
- the four Chebyshev nodes and the pseudo-inverse of the basis
  evaluated at them, for interpolation;
- conversion between `(lower, upper)` and `(mean, error)`, in both
  directions;
- evaluation at arbitrary points;
- `get_stretch_partitions` — a Hahn decomposition that splits a
  segment's total variation into its increasing and decreasing parts
  by solving the derivative quadratic, used only by composition.
