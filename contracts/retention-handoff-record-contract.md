# Retention Handoff Records Contract

A PFEM retention handoff records record should identify:

- `retention_handoff_record_id`
- `handoff_kind`
- `created_time`
- `node_id`
- `retention_export_closeout_record_id`
- `retention_export_verification_receipt_id`
- `handoff_state`
- `handoff_scope`
- `handoff_refs`
- `subject_refs`
- `basis_refs`
- `digest_algorithm`
- `handoff_ref_digest`
- `handed_off_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
