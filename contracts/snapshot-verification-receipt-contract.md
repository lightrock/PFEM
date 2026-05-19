# Snapshot Verification Receipt Contract

A PFEM snapshot verification receipt should identify:

- `snapshot_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `snapshot_manifest_id`
- `state_checkpoint_id`
- optional `state_transition_id`
- `verification_state`
- `checked_item_refs`
- optional `checked_source_paths`
- `basis_refs`
- `digest_algorithm`
- `expected_snapshot_digest`
- `actual_snapshot_digest`
- `verified_by_ref`
- `summary`

A snapshot verification receipt is not the snapshot manifest. It records that the manifest/items/digest were checked.
