# Federation Topology Contract

A PFEM federation topology link should identify:

- `link_id`
- `from_node_id`
- `to_node_id`
- `allowed_message_kinds`
- `allowed_sharing_scopes`
- `status`

Federation messages should carry:

- `sender_node_id`
- `recipient_node_ids`
- `message_kind`
- `sharing_scope`

A message is valid only when its sender, each recipient, message kind, and sharing scope match a known enabled link.
