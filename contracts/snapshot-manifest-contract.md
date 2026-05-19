# Snapshot Manifest Contract

A PFEM snapshot manifest should identify:

- `snapshot_manifest_id`
- `manifest_kind`
- `created_time`
- `node_id`
- `state_checkpoint_id`
- optional `state_transition_id`
- `snapshot_state`
- `items`
- `basis_refs`
- `digest_algorithm`
- `snapshot_digest`
- `manifested_by_ref`
- `summary`

A snapshot manifest is not the checkpoint itself. It lists the materialized records/files behind that checkpoint.
