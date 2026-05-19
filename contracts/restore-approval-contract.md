# Restore Approval Contract

A PFEM restore approval should identify:

- `restore_approval_id`
- `approval_kind`
- `created_time`
- `node_id`
- `restore_plan_id`
- `recovery_point_id`
- `approval_state`
- `approved_scope`
- `approved_refs`
- `approver_ref`
- `approval_basis_refs`
- optional `approval_constraints`
- `summary`

A restore approval is not a restore receipt. It authorizes a restore plan before execution.
