# Disposition Receipt Contract

A PFEM disposition receipt should identify:

- `disposition_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `disposition_record_id`
- `source_workflow_kind`
- `source_closeout_ref`
- `receipt_state`
- `executed_actions`
- optional `completed_refs`
- optional `skipped_refs`
- optional `failed_refs`
- `basis_refs`
- `executed_by_ref`
- `summary`

A disposition receipt is not a disposition record. It records evidence that the disposition actions actually executed.
