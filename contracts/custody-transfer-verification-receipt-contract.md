# Custody Transfer Verification Receipt Contract

A PFEM custody transfer verification receipt should identify:

- `custody_transfer_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `custody_transfer_record_id`
- `custody_verification_receipt_id`
- `custody_record_id`
- `disposition_receipt_id`
- `source_workflow_kind`
- `source_closeout_ref`
- `verification_state`
- `verified_custodian_ref`
- `verified_location_ref`
- `verified_location_kind`
- `checked_refs`
- optional `missing_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_checked_ref_digest`
- `actual_checked_ref_digest`
- `verified_by_ref`
- `summary`

A custody transfer verification receipt is not a custody transfer record. It records the post-transfer custody check.
