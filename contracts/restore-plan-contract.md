# Restore Plan Contract

A PFEM restore plan should identify:

- `restore_plan_id`
- `plan_kind`
- `created_time`
- `node_id`
- `recovery_point_id`
- optional `state_checkpoint_id`
- optional `snapshot_manifest_id`
- optional `snapshot_verification_receipt_id`
- `restore_scope`
- `plan_state`
- `planned_restore_refs`
- `preconditions`
- `basis_refs`
- `planned_by_ref`
- `summary`

A restore plan is not a restore receipt. It describes intended restore activity before execution.
