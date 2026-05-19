# Retention Status Snapshot Records Contract

A PFEM retention status snapshot records record should identify:

- `retention_status_snapshot_record_id`
- `snapshot_kind`
- `created_time`
- `node_id`
- `retention_hold_closeout_record_id`
- `retention_cycle_closeout_record_id`
- `snapshot_state`
- `retention_status`
- `snapshot_refs`
- `subject_refs`
- `basis_refs`
- `digest_algorithm`
- `snapshot_ref_digest`
- `recorded_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
