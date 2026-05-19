# Federation Model

PFEM federation is the exchange of attributable information between nodes.

A federation message may carry:

- evidence references
- observation summaries
- alert summaries
- evidence package references
- dashboard requests
- rollup summaries
- health or freshness information

Federation does not mean every node shares everything with every other node.

## Rules

- A node should know what it is sending.
- A node should know why it is allowed to send it.
- A receiving node should know where the message came from.
- Federation messages should preserve lineage references when possible.
- Sharing scope should be explicit.
- Rollup summaries should not replace local source records.

## Topologies

PFEM should support multiple topology styles:

- local-only
- peer mesh
- hub-and-spoke
- ad hoc group
- formal rollup chain
- disconnected edge with later sync

The architecture should not assume one topology is always present.
