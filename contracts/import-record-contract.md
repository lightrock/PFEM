# Import Record Contract

A PFEM import record should identify:

- `import_record_id`
- `import_kind`
- `created_time`
- `exchange_receipt_id`
- `bundle_id`
- optional `inbox_item_id`
- optional `intake_decision_id`
- `source_node_id`
- `destination_node_id`
- `subject_refs`
- `artifact_refs`
- `basis_refs`
- optional `created_or_updated_refs`
- `import_state`
- `imported_by_ref`
- `summary`

An import record is not an exchange receipt. It records local receiver-side staging/application after exchange acceptance.
