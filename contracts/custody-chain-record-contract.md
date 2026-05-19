# Custody Chain Record Contract

A PFEM custody chain record should identify:

- `custody_chain_record_id`
- `chain_kind`
- `created_time`
- `node_id`
- `source_workflow_kind`
- `source_closeout_ref`
- `chain_state`
- `start_ref`
- `terminal_ref`
- `final_outcome`
- `final_custodian_ref`
- `final_location_ref`
- `final_location_kind`
- `chain_refs`
- `held_refs`
- `basis_refs`
- `digest_algorithm`
- `chain_ref_digest`
- `summarized_by_ref`
- `summary`

A custody chain record is not a custody closeout record. It is a linked summary of the custody chain segment after closeout.
