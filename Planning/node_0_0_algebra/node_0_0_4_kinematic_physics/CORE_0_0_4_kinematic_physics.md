---
id: zspectral.algebra.kinematic_physics
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: kinematic_physics
    path: Planning/node_0_0_algebra/node_0_0_4_kinematic_physics/CORE_0_0_4_kinematic_physics.md
super_node:
    name: algebra
    path: ../CORE_0_0_algebra.md
sub_nodes: []
---

# CORE 0_0_4 — kinematic_physics

## metadata

- **id:** zspectral.algebra.kinematic_physics
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

How the `meta` channels combine when two values interact.

Each operation — add, multiply, compose, matrix-multiply — has its
own rule for propagating real and virtual position, real and virtual
mass, interval length and confidence. Composition additionally takes
the positive and negative stretch from
[chebyshev_math](../node_0_0_2_chebyshev_math/CORE_0_0_2_chebyshev_math.md),
because composing functions rescales the inner function's coordinate.

Unverified: the meta channels play no part in compression. Nothing on
the encode or decode path reads them except `confidence`, which
`integrate` uses as a weight.
