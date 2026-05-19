# Transport Receipt Contract

A PFEM transport receipt should identify:

- `transport_receipt_id`
- `receipt_kind`
- `created_time`
- `transport_adapter_id`
- `delivery_channel_id`
- `route_id`
- `source_node_id`
- `destination_node_id`
- `subject_refs`
- `basis_refs`
- `transport_state`
- `outcome_summary`

Transport receipts may include artifact references, such as a bundle file path or exported artifact path.

A transport receipt records movement attempt/result. It is not evidence, not routing policy, and not an exchange decision.
