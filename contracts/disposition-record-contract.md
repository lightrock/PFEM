# Disposition Record Contract

A PFEM disposition record should identify:

- `disposition_record_id`
- `disposition_kind`
- `created_time`
- `node_id`
- `source_workflow_kind`
- `source_closeout_ref`
- `disposition_state`
- optional `retention_basis`
- optional `retention_policy_ref`
- `subject_refs`
- `actions`
- `basis_refs`
- `disposed_by_ref`
- `summary`

A disposition record is not a closeout record. It records what should happen to closed workflow artifacts.
