# Inbox Item Contract

A PFEM inbox item should identify:

- `inbox_item_id`
- `item_kind`
- `created_time`
- `transport_receipt_id`
- `outbox_item_id` when known
- `source_node_id`
- `destination_node_id`
- `subject_refs`
- `artifact_refs`
- `basis_refs`
- `inbox_state`
- `received_by_ref`
- `summary`

An inbox item is the receiver-side staged payload boundary. It is not the transport receipt and not the exchange-layer acceptance/rejection result.
