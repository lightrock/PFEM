# Retention Handoff Verification Receipts Contract

A PFEM retention handoff verification receipts record should identify:

- `retention_handoff_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_handoff_record_id`
- `retention_export_closeout_record_id`
- `verification_state`
- `checked_handoff_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_handoff_ref_digest`
- `actual_handoff_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
