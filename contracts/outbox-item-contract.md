# Outbox Item Contract

A PFEM outbox item should identify:

- `outbox_item_id`
- `item_kind`
- `created_time`
- `delivery_job_id`
- `dispatch_decision_id`
- `route_id`
- `delivery_channel_id`
- `transport_adapter_id`
- `source_node_id`
- `destination_node_id`
- `subject_refs`
- `artifact_refs`
- `basis_refs`
- `outbox_state`
- `staged_by_ref`
- `summary`

An outbox item is the staged payload boundary. It is not the delivery job, not the dispatch decision, and not the transport result.
