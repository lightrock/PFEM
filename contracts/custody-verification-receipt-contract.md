# Custody Verification Receipt Contract

A PFEM custody verification receipt should identify:

- `custody_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `custody_record_id`
- `disposition_receipt_id`
- optional `disposition_record_id`
- `source_workflow_kind`
- `source_closeout_ref`
- `verification_state`
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

A custody verification receipt is not a custody record. It records that the custody location and held refs were checked.
