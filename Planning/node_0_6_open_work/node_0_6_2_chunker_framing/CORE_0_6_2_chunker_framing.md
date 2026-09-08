---
id: zspectral.open_work.chunker_framing
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: work
node:
    name: chunker_framing
    path: Planning/node_0_6_open_work/node_0_6_2_chunker_framing/CORE_0_6_2_chunker_framing.md
super_node:
    name: open_work
    path: ../CORE_0_6_open_work.md
sub_nodes: []
---

# CORE 0_6_2 — chunker_framing

## metadata

- **id:** zspectral.open_work.chunker_framing
- **level:** 2
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [open_work](../CORE_0_6_open_work.md)

## sub_nodes

*(none yet)*

## definition

Decide whether the project's centre is the codec or the addressing
scheme.

## the case for the change

[edit_locality](../../node_0_5_findings/node_0_5_3_edit_locality/CORE_0_5_3_edit_locality.md)
holds with no compression involved. Independent units laid along a
space-filling curve, with a hash per unit, give a structure whose
useful property is that a local change in N dimensions costs a small
number of units — measured at 1 against 16 for a compact 2D edit.

Adding a hash to each level of the existing merge pyramid makes that
structure a hash hierarchy over a space-filling curve. "What changed
between version A and B" then costs the size of the change rather
than the size of the data.

The formats that already have local decodability — FLAC frames,
JPEG2000 tiles, squashfs blocks, and the content-defined chunking in
`restic` and `borg` — are all one-dimensional, and none has the
hierarchy.

## what this would make the Chebyshev fit

One available per-unit codec rather than the point of the system. It
would be applied where the data is smooth and skipped where it is
not, which is what
[one_dimensional_behaviour](../../node_0_5_findings/node_0_5_0_one_dimensional_behaviour/CORE_0_5_0_one_dimensional_behaviour.md)
says the alternative should be.

## why it is the owner's to settle

It is a question about what the project is for, not about what is
true. PROTOCOL §2 puts that at level 0.
