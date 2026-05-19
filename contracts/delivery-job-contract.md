# Delivery Job Contract

A PFEM delivery job should identify:

- `delivery_job_id`
- `job_kind`
- `created_time`
- `requested_by_ref` when applicable
- `route_id`
- `delivery_channel_id`
- `transport_adapter_id`
- `source_node_id`
- `destination_node_id`
- `subject_refs`
- `basis_refs`
- `job_state`
- `priority`
- `summary`

A delivery job is planned or assigned movement work.

It is not routing policy, not a delivery channel definition, not a transport adapter definition, and not proof that delivery happened.
