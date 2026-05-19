# Custody Ledger Verification Receipts Contract

A PFEM custody ledger verification receipts record should identify:

- `custody_ledger_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `custody_ledger_record_id`
- `custody_chain_verification_receipt_id`
- `verification_state`
- `checked_entry_refs`
- `checked_held_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_entry_ref_digest`
- `actual_entry_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
