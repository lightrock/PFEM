# Transport Adapter Contract

A PFEM transport adapter should identify:

- `transport_adapter_id`
- `transport_kind`
- `status`
- `delivery_channel_ids`
- `implementation_ref`
- source constraints when needed
- destination constraints when needed
- `supported_route_kinds`
- allowed sharing scopes when needed
- allowed handling labels when needed
- `summary`

A transport adapter is an implementation hook. It is not a routing rule and it is not evidence.
