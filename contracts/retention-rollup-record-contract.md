# Retention Rollup Records Contract

A PFEM retention rollup records record should identify:

- `retention_rollup_record_id`
- `rollup_kind`
- `created_time`
- `node_id`
- `retention_status_snapshot_verification_receipt_id`
- `retention_status_snapshot_record_id`
- `rollup_state`
- `rollup_scope`
- `rollup_refs`
- `subject_refs`
- `basis_refs`
- `digest_algorithm`
- `rollup_ref_digest`
- `rolled_up_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
