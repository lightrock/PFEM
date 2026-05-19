# Restore Verification Receipt Contract

A PFEM restore verification receipt should identify:

- `restore_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `restore_receipt_id`
- `restore_approval_id`
- `restore_plan_id`
- `recovery_point_id`
- optional `state_checkpoint_id`
- optional `snapshot_manifest_id`
- `verification_state`
- `checked_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_restored_ref_digest`
- `actual_restored_ref_digest`
- `verified_by_ref`
- `summary`

A restore verification receipt is not a restore receipt. It records the post-restore check result.
