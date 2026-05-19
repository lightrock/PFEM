# Action Records

PFEM action records describe recommended, assigned, blocked, completed, or cancelled next steps.

An action record answers:

```text
Given these records and this basis, what should happen next?
Who owns the next step?
What state is that action in?
```

## Why separate action records?

Evidence should not become a task manager.

Rollups should not secretly contain operational task state.

Action records are separate so PFEM can attach a next step without corrupting evidence, findings, rollups, exchanges, reconciliation, or quality assessments.

## Action records are for

- review this
- notify someone/something
- investigate a discrepancy
- escalate under a profile/workflow
- monitor without escalation
- correct or supersede a record
- prepare a handoff
- archive/disposition work

## Action records are not

- dispatch software
- incident command
- case management
- legal authority
- proof that the action was actually performed

They are the architecture hook that keeps “what next?” tied to the records that justified it.
