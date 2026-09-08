---
id: zspectral.codec.decoder.signal_assembler
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: signal_assembler
    path: Planning/node_0_2_codec/node_0_2_1_decoder/node_0_2_1_1_signal_assembler/CORE_0_2_1_1_signal_assembler.md
super_node:
    name: decoder
    path: ../CORE_0_2_1_decoder.md
sub_nodes: []
---

# CORE 0_2_1_1 — signal_assembler

## metadata

- **id:** zspectral.codec.decoder.signal_assembler
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [decoder](../CORE_0_2_1_decoder.md)

## sub_nodes

*(none yet)*

## definition

Evaluates every token and concatenates the pieces back into one
stream, in interval order.

It averages the upper and lower curves into a single output curve.
**That average is where the interval representation collapses to one
value** — the bounds are carried the whole way through encoding and
then discarded at the last step, which is worth stating because it
means the decoder cannot report its own uncertainty.
