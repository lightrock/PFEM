# Recovery Point Contract

A PFEM recovery point should identify:

- `recovery_point_id`
- `recovery_point_kind`
- `created_time`
- `node_id`
- `state_checkpoint_id`
- `snapshot_manifest_id`
- `snapshot_verification_receipt_id`
- optional `state_transition_id`
- `recovery_state`
- `restore_scope`
- `restorable_refs`
- `basis_refs`
- `promoted_by_ref`
- `summary`

A recovery point is not a snapshot verification receipt. It promotes a verified snapshot as an available restore candidate.
