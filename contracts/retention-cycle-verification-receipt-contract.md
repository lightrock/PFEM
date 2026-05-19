# Retention Cycle Verification Receipts Contract

A PFEM retention cycle verification receipts record should identify:

- `retention_cycle_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_cycle_record_id`
- `retention_schedule_closeout_record_id`
- `verification_state`
- `checked_cycle_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_cycle_ref_digest`
- `actual_cycle_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
