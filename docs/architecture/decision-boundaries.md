# Decision Boundaries

PFEM separates source input, evidence preservation, analysis, alerting, dashboard action, and rollup.

## Boundary rules

- An adapter may translate input, but it does not own deployment policy.
- A normalized observation may describe what was seen, but it is not a finding by itself.
- A finding may describe interpreted significance, but it is not automatically an action.
- An alert may request attention, but it is not an evidence package.
- A dashboard action may guide a human, but it is not source evidence.
- A rollup may summarize local state, but it is not complete local truth.
- A report is an output, not a source record.

If a change makes these boundaries weaker, it needs an architecture note.
