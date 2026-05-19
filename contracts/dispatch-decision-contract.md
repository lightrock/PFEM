# Dispatch Decision Contract

A PFEM dispatch decision should identify:

- `dispatch_decision_id`
- `decision_kind`
- `created_time`
- `delivery_job_id`
- `dispatch_rule_id`
- `decision`
- `reason_code`
- `decided_by_ref`
- `basis_refs`
- `summary`

A dispatch decision records what PFEM decided for a specific delivery job.

It is not the policy rule itself, not the job, and not proof of transport.
