# Custody Ledger Records Contract

A PFEM custody ledger records record should identify:

- `custody_ledger_record_id`
- `ledger_kind`
- `created_time`
- `node_id`
- `source_workflow_kind`
- `source_closeout_ref`
- `custody_chain_verification_receipt_id`
- `custody_chain_record_id`
- `custody_closeout_record_id`
- `ledger_state`
- `ledger_sequence`
- `entry_refs`
- `held_refs`
- `basis_refs`
- `digest_algorithm`
- `entry_ref_digest`
- `recorded_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
