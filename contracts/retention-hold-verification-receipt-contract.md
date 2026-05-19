# Retention Hold Verification Receipts Contract

A PFEM retention hold verification receipts record should identify:

- `retention_hold_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_hold_record_id`
- `retention_cycle_closeout_record_id`
- `verification_state`
- `checked_hold_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_hold_ref_digest`
- `actual_hold_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
