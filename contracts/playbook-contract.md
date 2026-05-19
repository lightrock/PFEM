# Playbook Contract

A PFEM playbook should identify:

- `playbook_id`
- `playbook_kind`
- `version`
- `status`
- `owner_ref`
- `applies_to_action_kinds`
- `required_inputs`
- `summary`
- `steps`

Each step should identify:

- `step_id`
- `title`
- `instruction`
- `expected_output`

Actions may reference playbooks with `playbook_refs`.
