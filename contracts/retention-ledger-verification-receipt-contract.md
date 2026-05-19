# Retention Ledger Verification Receipts Contract

A PFEM retention ledger verification receipts record should identify:

- `retention_ledger_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_ledger_record_id`
- `retention_lifecycle_closeout_record_id`
- `verification_state`
- `checked_entry_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_entry_ref_digest`
- `actual_entry_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
