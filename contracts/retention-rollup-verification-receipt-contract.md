# Retention Rollup Verification Receipts Contract

A PFEM retention rollup verification receipts record should identify:

- `retention_rollup_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_rollup_record_id`
- `retention_status_snapshot_verification_receipt_id`
- `verification_state`
- `checked_rollup_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_rollup_ref_digest`
- `actual_rollup_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
