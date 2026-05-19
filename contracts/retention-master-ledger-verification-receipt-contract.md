# Retention Master Ledger Verification Receipts Contract

A PFEM retention master ledger verification receipts record should identify:

- `retention_master_ledger_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_master_ledger_record_id`
- `retention_final_index_closeout_record_id`
- `verification_state`
- `checked_master_ledger_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_master_ledger_ref_digest`
- `actual_master_ledger_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
