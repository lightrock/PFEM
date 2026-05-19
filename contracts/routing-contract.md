# Routing Contract

A PFEM routing policy should identify:

- `policy_id`
- `version`
- `routes`

A route should identify:

- `route_id`
- `route_kind`
- `enabled`
- source constraints when needed
- destination nodes/profiles when needed
- applicable action kinds, bundle kinds, priorities, sharing scopes, or handling labels
- `summary`

Routing is policy. It is not transport.
