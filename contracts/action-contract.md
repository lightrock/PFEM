# Action Contract

A PFEM action record should identify:

- `action_id`
- `action_kind`
- `created_time`
- `owner_ref`
- `subject_refs`
- `basis_refs`
- `priority`
- `action_state`
- `summary`
- `next_step`

Action kinds, priorities, and states must come from `action/action-policy.json`.

Action records should reference known records or artifact paths.
