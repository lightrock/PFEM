# Node Identity

Profiles define node shape. Nodes identify configured participants.

A federation system cannot rely only on profile names. It needs stable node ids.

Example:

```text
profile_id = field-radio-node
node_id    = field-radio-node-example
```

## Rules

- A node manifest should reference a known profile.
- A node registry entry should point to a real node manifest.
- The `node_id` in the registry should match the manifest.
- Rollup summaries should use known `producer_node_id` values.
- Federation messages should use known `sender_node_id` values.
- A node id is not a person name, legal identity, or authentication credential.
