---
id: zspectral.container.vector_quantizer
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: vector_quantizer
    path: Planning/node_0_3_container/node_0_3_1_vector_quantizer/CORE_0_3_1_vector_quantizer.md
super_node:
    name: container
    path: ../CORE_0_3_container.md
sub_nodes: []
---

# CORE 0_3_1 — vector_quantizer

## metadata

- **id:** zspectral.container.vector_quantizer
- **level:** 2
- **status:** draft
- **designation:** code (function)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [container](../CORE_0_3_container.md)

## sub_nodes

*(none yet)*

## definition

Replaces each token's three shape coefficients with an index into a
learned codebook.

The mean level `c0` is separated out first and quantised directly to
a uint8; the remaining `c1, c2, c3` are standardised across all
tokens and clustered by k-means into at most 256 centroids.

The split is the design decision: a segment's mean level varies over
the whole range and does not repeat, while a segment's *shape*
repeats across a data set and is therefore worth a codebook.

**Currently not a class.** It exists as inline calls to
`StandardScaler` and `KMeans` inside `ZSpectralCompressor.compress`.
Stated as a node because it is a distinct stage with its own measured
behaviour; whether it is extracted is a refactor question, not a
design one.
