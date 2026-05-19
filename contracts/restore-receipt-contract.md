# Restore Receipt Contract

A PFEM restore receipt should identify:

- `restore_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `restore_plan_id`
- `restore_approval_id`
- `recovery_point_id`
- optional `state_checkpoint_id`
- optional `snapshot_manifest_id`
- optional `snapshot_verification_receipt_id`
- `restore_state`
- `restore_scope`
- `restored_refs`
- optional `skipped_refs`
- optional `failed_refs`
- `basis_refs`
- `restored_by_ref`
- `summary`

A restore receipt is not a restore approval. It records execution evidence after an approved restore plan runs.
