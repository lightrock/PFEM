# Custody Lifecycle Verification Receipts Contract

A PFEM custody lifecycle verification receipts record should identify:

- `custody_lifecycle_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `custody_lifecycle_record_id`
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
