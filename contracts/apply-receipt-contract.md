# Apply Receipt Contract

A PFEM apply receipt should identify:

- `apply_receipt_id`
- `receipt_kind`
- `created_time`
- `merge_decision_id`
- optional `conflict_record_id`
- `import_record_id`
- optional `exchange_receipt_id`
- `bundle_id`
- `apply_state`
- `applied_by_ref`
- optional `created_refs`
- optional `updated_refs`
- optional `skipped_refs`
- optional `failed_refs`
- `basis_refs`
- `summary`

An apply receipt is not the merge decision. It records the actual local apply/skip/fail result after the decision.
