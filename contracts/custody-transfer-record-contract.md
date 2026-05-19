# Custody Transfer Record Contract

A PFEM custody transfer record should identify:

- `custody_transfer_record_id`
- `transfer_kind`
- `created_time`
- `node_id`
- `custody_record_id`
- `custody_verification_receipt_id`
- `disposition_receipt_id`
- `source_workflow_kind`
- `source_closeout_ref`
- `transfer_state`
- `from_custodian_ref`
- `to_custodian_ref`
- `from_location_ref`
- `to_location_ref`
- `from_location_kind`
- `to_location_kind`
- `transferred_refs`
- optional `skipped_refs`
- optional `failed_refs`
- `basis_refs`
- `transferred_by_ref`
- `summary`

A custody transfer record is not a custody verification receipt. It records a chain-of-custody movement or formal re-assertion after custody was checked.
