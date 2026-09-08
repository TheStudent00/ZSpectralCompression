---
id: zspectral.geometry.geometry_interpreter
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: geometry_interpreter
    path: Planning/node_0_1_geometry/node_0_1_2_geometry_interpreter/CORE_0_1_2_geometry_interpreter.md
super_node:
    name: geometry
    path: ../CORE_0_1_geometry.md
sub_nodes: []
---

# CORE 0_1_2 — geometry_interpreter

## metadata

- **id:** zspectral.geometry.geometry_interpreter
- **level:*## definition

Composes the framer and the router into one boundary:
`flatten_to_1d` and `unflatten_to_nd`.

It is the only place downstream code learns that the data had a
shape. Everything after it operates on a flat stream plus a table of
intervals, which is why the codec is dimension-agnostic without
containing any dimension-handling code.
g — generated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_1_geometry/CORE_0_1_geometry.md; the definition and `designation` are the owner's to
write.)*
