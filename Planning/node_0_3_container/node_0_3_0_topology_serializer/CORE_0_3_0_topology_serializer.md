---
id: zspectral.container.topology_serializer
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: topology_serializer
    path: Planning/node_0_3_container/node_0_3_0_topology_serializer/CORE_0_3_0_topology_serializer.md
super_node:
    name: container
    path: ../CORE_0_3_container.md
sub_nodes: []
---

# CORE 0_3_0 — topology_serializer

## metadata

- **id:** zspectral.container.topology_serializer
- **level:*## definition

Encodes the segment lengths as a pre-order bitmask over a binary
subdivision of the total length.

Walking down from the whole stream: emit `1` if the next token
exactly covers the current size, otherwise emit `0` and recurse into
two halves. Decoding replays the same recursion against the bit
stream and reconstructs the lengths.

**This is why intervals are never stored.** The prototype's own
comment records what it replaced: "Our massive 2.8 MB interval array
is now just the length of this byte tensor". The cost is one bit per
segment plus one per internal node of the subdivision tree.
g — generated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_3_container/CORE_0_3_container.md; the definition and `designation` are the owner's to
write.)*
