# Preservation Verification Receipts Contract

A PFEM preservation verification receipts record should identify:

- `preservation_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `preservation_record_id`
- `archive_lifecycle_closeout_record_id`
- `verification_state`
- `checked_preserved_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_preserved_ref_digest`
- `actual_preserved_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
