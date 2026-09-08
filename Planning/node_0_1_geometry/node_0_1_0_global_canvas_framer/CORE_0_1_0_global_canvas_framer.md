---
id: zspectral.geometry.global_canvas_framer
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: global_canvas_framer
    path: Planning/node_0_1_geometry/node_0_1_0_global_canvas_framer/CORE_0_1_0_global_canvas_framer.md
super_node:
    name: geometry
    path: ../CORE_0_1_geometry.md
sub_nodes: []
---

# CORE 0_1_0 — global_canvas_framer

## metadata

- **id:** zspectral.geometry.global_canvas_framer
- **level:*## definition

Pads every axis up to the next power of two with zeros, and crops
back afterwards.

It exists for one reason: a Morton code is an interleave of the
coordinates' bits, and an interleave tiles a region exactly only when
the region's sides are powers of two. Without the padding the
Z-order traversal would not partition the data.

The padding value is a constant zero, which for image data means the
codec fits polynomials across a hard edge at the boundary. Unverified
whether that costs anything measurable.
g — generated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_1_geometry/CORE_0_1_geometry.md; the definition and `designation` are the owner's to
write.)*
