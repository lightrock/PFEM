# State Checkpoint Contract

A PFEM state checkpoint should identify:

- `state_checkpoint_id`
- `checkpoint_kind`
- `created_time`
- `node_id`
- optional `apply_receipt_id`
- optional `merge_decision_id`
- optional `import_record_id`
- `checkpoint_state`
- `included_refs`
- `basis_refs`
- `digest_algorithm`
- `state_digest`
- `checkpointed_by_ref`
- `summary`

A state checkpoint is not an apply receipt. It marks a point-in-time known-good local PFEM state after apply activity.
