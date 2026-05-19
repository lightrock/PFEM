# State Transition Contract

A PFEM state transition should identify:

- `state_transition_id`
- `transition_kind`
- `created_time`
- `node_id`
- optional/null `from_state_checkpoint_id`
- `to_state_checkpoint_id`
- `apply_receipt_ids`
- optional `merge_decision_ids`
- optional `import_record_ids`
- `transition_state`
- `changed_refs`
- `basis_refs`
- `transitioned_by_ref`
- `summary`

A state transition is not the checkpoint itself. It records how PFEM moved into that checkpointed state.
