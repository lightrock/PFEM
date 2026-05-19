# Merge Decision Contract

A PFEM merge decision should identify:

- `merge_decision_id`
- `decision_kind`
- `created_time`
- `import_record_id`
- `exchange_receipt_id`
- `bundle_id`
- `decision`
- `reason_code`
- `decided_by_ref`
- `incoming_refs`
- optional `local_target_refs`
- `basis_refs`
- optional `resulting_import_state`
- `summary`

A merge decision is not an import record. It records the local conflict/update judgment for imported records.
