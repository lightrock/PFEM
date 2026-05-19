# Custody Closeout Record Contract

A PFEM custody closeout record should identify:

- `custody_closeout_record_id`
- `closeout_kind`
- `created_time`
- `node_id`
- `custody_transfer_verification_receipt_id`
- `custody_transfer_record_id`
- `custody_verification_receipt_id`
- `custody_record_id`
- `disposition_receipt_id`
- `source_workflow_kind`
- `source_closeout_ref`
- `closeout_state`
- `outcome`
- `closed_refs`
- `basis_refs`
- `closed_by_ref`
- `summary`

A custody closeout record is not a custody transfer verification receipt. It records final closure of the custody chain segment.
