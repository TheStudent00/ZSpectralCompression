---
id: zspectral.algebra.spectral_algebra
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: spectral_algebra
    path: Planning/node_0_0_algebra/node_0_0_5_spectral_algebra/CORE_0_0_5_spectral_algebra.md
super_node:
    name: algebra
    path: ../CORE_0_0_algebra.md
sub_nodes: []
---

# CORE 0_0_5 — spectral_algebra

## metadata

- **id:** zspectral.algebra.spectral_algebra
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

Addition, multiplication, matrix multiplication, composition and
integration over [spectral_tensor](../node_0_0_1_spectral_tensor/CORE_0_0_1_spectral_tensor.md).

Every operation has the same three-step shape: align the two
operands' segment counts upward, do the arithmetic on
`(mean, error)` with the error propagated by its own rule, then
restore the left operand's original segment count.

The error rule is what makes this interval arithmetic rather than
ordinary spline arithmetic. For a product, the error is
`|A|*err_B + |B|*err_A + err_A*err_B`, so the result's bounds enclose
every product of values within the operands' bounds.

**Nothing in the compression path calls this class.** It is a
separate capability that shares the representation.
