---
id: zspectral.codec
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: codec
    path: Planning/node_0_2_codec/CORE_0_2_codec.md
super_node:
    name: zspectral
    path: ../CORE_0.md
sub_nodes:
    - name: encoder
      path: node_0_2_0_encoder/CORE_0_2_0_encoder.md
    - name: decoder
      path: node_0_2_1_decoder/CORE_0_2_1_decoder.md
    - name: interface
      path: node_0_2_2_interface/CORE_0_2_2_interface.md
---

# CORE 0_2 — codec

## metadata

- **id:** zspectral.codec
- **level:** 1
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [zspectral](../CORE_0.md)

## sub_nodes

- [encoder](node_0_2_0_encoder/CORE_0_2_0_encoder.md)
- [decoder](node_0_2_1_decoder/CORE_0_2_1_decoder.md)
- [interface](node_0_2_2_interface/CORE_0_2_2_interface.md)

## definition

The conversion between a one-dimensional stream of samples and a set
of variable-length tokens, each token one Chebyshev polynomial over
one interval.

## design

The token lengths are not fixed and not chosen in advance. They fall
out of a build-then-descend procedure:

- fit every fixed-size leaf patch, and record each patch's fit error;
- merge the whole sequence upward in pairs to a single root, inflating
  the error estimate at each merge;
- descend from the root, keeping a node whole where its error is under
  the threshold and splitting it where it is not;
- re-fit the segments that survived, at their real lengths.

The re-fit at the end is not redundant. The merged coefficients are a
projection of a projection, so they drift; the final fit is against
the raw data at the segment's true length.

**The threshold is the only knob that decides lossy versus lossless.**
At a positive threshold, merging is what produces compression. At zero
the procedure still runs, but merges only where the data is exactly a
degree-3 polynomial, which for measured data is nearly nowhere — see
[lossless_mode](../node_0_6_open_work/node_0_6_0_lossless_mode/CORE_0_6_0_lossless_mode.md).
