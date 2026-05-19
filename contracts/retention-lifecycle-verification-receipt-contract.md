# Retention Lifecycle Verification Receipts Contract

A PFEM retention lifecycle verification receipts record should identify:

- `retention_lifecycle_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_lifecycle_record_id`
- `retention_chain_verification_receipt_id`
- `verification_state`
- `checked_lifecycle_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_lifecycle_ref_digest`
- `actual_lifecycle_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
