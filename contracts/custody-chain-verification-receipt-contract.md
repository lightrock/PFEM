# Custody Chain Verification Receipt Contract

A PFEM custody chain verification receipt should identify:

- `custody_chain_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `custody_chain_record_id`
- `terminal_ref`
- `source_workflow_kind`
- `source_closeout_ref`
- `verification_state`
- `checked_chain_refs`
- `checked_held_refs`
- optional `missing_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_chain_ref_digest`
- `actual_chain_ref_digest`
- `verified_by_ref`
- `summary`

A custody chain verification receipt is not a custody chain record. It records that the chain summary and digest were checked.
