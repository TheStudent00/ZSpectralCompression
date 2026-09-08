---
id: zspectral.geometry
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: geometry
    path: Planning/node_0_1_geometry/CORE_0_1_geometry.md
super_node:
    name: zspectral
    path: ../CORE_0.md
sub_nodes:
    - name: global_canvas_framer
      path: node_0_1_0_global_canvas_framer/CORE_0_1_0_global_canvas_framer.md
    - name: z_curve_router
      path: node_0_1_1_z_curve_router/CORE_0_1_1_z_curve_router.md
    - name: geometry_interpreter
      path: node_0_1_2_geometry_interpreter/CORE_0_1_2_geometry_interpreter.md
---

# CORE 0_1 — geometry

## metadata

- **id:** zspectral.geometry
- **level:** 1
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [zspectral](../CORE_0.md)

## sub_nodes

- [global_canvas_framer](node_0_1_0_global_canvas_framer/CORE_0_1_0_global_canvas_framer.md)
- [z_curve_router](node_0_1_1_z_curve_router/CORE_0_1_1_z_curve_router.md)
- [geometry_interpreter](node_0_1_2_geometry_interpreter/CORE_0_1_2_geometry_interpreter.md)

## definition

The boundary between data of any dimension and the one-dimensional
sequence everything downstream operates on, together with the inverse.

## design

Two steps forward, two back, in this order:

- **pad**, so every axis length is a power of two. The Z-order code
  is a bit interleave, and a bit interleave only tiles a region
  exactly when the region's sides are powers of two. Padding is what
  buys that, and it is why the framer exists as its own step.
- **sequence**, by sorting every cell by its Morton code — the
  interleave of its coordinates' bits. The output is the flat
  sequence plus, per group of `min_token_size` cells, the bounding
  box in the original coordinates.

The bounding boxes are the part that is easy to miss: the 1D stream
alone would lose where each token came from, and the intervals are
what let a token be placed back in N dimensions, and what
[edit_locality](../node_0_5_findings/node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md)
measures.

## why a space-filling curve rather than raster order

Measured 2026-09-08, and it is a trade rather than a win:

- a compact 2D edit costs 1 to 4 chunks under Z-order against 16 to
  32 under raster order;
- a full-row edit costs 16 under Z-order against 1 under raster;
- a full-column edit costs 16 under Z-order against **all 256** under
  raster.

Z-order is never the best ordering and never the worst. Raster order
is optimal for edits shaped along its traversal and pathological for
edits shaped across it.
