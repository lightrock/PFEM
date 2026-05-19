# Retention Ledger Records Contract

A PFEM retention ledger records record should identify:

- `retention_ledger_record_id`
- `ledger_kind`
- `created_time`
- `node_id`
- `retention_lifecycle_closeout_record_id`
- `retention_lifecycle_verification_receipt_id`
- `ledger_state`
- `ledger_sequence`
- `entry_refs`
- `subject_refs`
- `basis_refs`
- `digest_algorithm`
- `entry_ref_digest`
- `recorded_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
