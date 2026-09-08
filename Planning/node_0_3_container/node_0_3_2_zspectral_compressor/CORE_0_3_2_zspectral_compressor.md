---
id: zspectral.container.zspectral_compressor
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: zspectral_compressor
    path: Planning/node_0_3_container/node_0_3_2_zspectral_compressor/CORE_0_3_2_zspectral_compressor.md
super_node:
    name: container
    path: ../CORE_0_3_container.md
sub_nodes: []
---

# CORE 0_3_2 — zspectral_compressor

## metadata

- **id:** zspectral.container.zspectral_compressor
- **level:## definition

Assembles a payload and takes one apart.

`compress` runs the interface, derives each token's pixel count from
its interval, serialises the topology, then separates and quantises
the coefficients. `decompress` reverses it. `calculate_metrics`
counts the parts.

The payload is five keys: `labels`, `c0_quantized`, `codebook`,
`topology_bytes`, `topology_num_bits`. Notably absent: the intervals,
recovered from the topology bitmask, and the `meta` channels, which
are not stored at all.
ng — generated 2026-09-08 from the register in
~/Programming/ZSpectralCompression/Planning/node_0_3_container/CORE_0_3_container.md; the definition and `designation` are the owner's to
write.)*
