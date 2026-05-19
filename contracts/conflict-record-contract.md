# Conflict Record Contract

A PFEM conflict record should identify:

- `conflict_record_id`
- `conflict_kind`
- `created_time`
- `import_record_id`
- `exchange_receipt_id`
- `bundle_id`
- `incoming_refs`
- optional `local_target_refs`
- `basis_refs`
- `severity`
- `conflict_state`
- `detected_by_ref`
- `summary`

A conflict record is not the merge decision. It records the facts the merge decision can cite.
