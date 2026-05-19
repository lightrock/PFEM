# Retention Finalization Verification Receipts Contract

A PFEM retention finalization verification receipts record should identify:

- `retention_finalization_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_finalization_record_id`
- `retention_package_closeout_record_id`
- `verification_state`
- `checked_finalization_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_finalization_ref_digest`
- `actual_finalization_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
