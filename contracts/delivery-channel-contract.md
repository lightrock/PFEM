# Delivery Channel Contract

A PFEM delivery channel should identify:

- `channel_id`
- `channel_kind`
- `status`
- `supports_route_kinds`
- source constraints when needed
- destination constraints when needed
- allowed sharing scopes when needed
- allowed handling labels when needed
- `summary`

A delivery channel is not a transport implementation. It is a named delivery option that routes may reference.
