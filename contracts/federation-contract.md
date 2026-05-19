# Federation Contract

Federation records carry summaries or requests between nodes.

A federation message should identify:

- `message_id`
- `message_kind`
- `sender_node_id`
- `created_time`
- `lineage_refs`
- `sharing_scope`

A federation message is not raw evidence. It is a shareable message that may carry summary content and references to the records that support it.
