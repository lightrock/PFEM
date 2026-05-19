# Dispatch Policy Contract

A PFEM dispatch policy should identify:

- `policy_id`
- `version`
- `rules`

A dispatch rule should identify:

- `dispatch_rule_id`
- `enabled`
- applicable `job_kinds`
- eligible job states
- applicable priorities
- route, channel, or transport adapter constraints when needed
- whether review is required before dispatch
- maximum attempts
- retry delay
- success/failure job-state outcomes
- `summary`

Dispatch policy controls job eligibility and retry behavior. It does not perform transport and it does not prove delivery happened.
