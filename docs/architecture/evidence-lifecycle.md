# Evidence Lifecycle

PFEM keeps evidence and derived objects separate.

A typical lifecycle is:

1. Raw evidence is received.
2. Raw evidence is recorded with source and time information.
3. A normalized observation may be derived from raw evidence.
4. Observations may be associated into entities, tracks, or context.
5. A finding may be produced from observations and context.
6. An alert may be produced from findings and policy.
7. An evidence package may collect relevant records for review.
8. A rollup summary may be produced for another node or dashboard.
9. A report may be generated for human use.

## Rules

- Raw evidence should not be silently rewritten.
- A normalized observation should reference its source evidence.
- A finding should reference the observations and logic that produced it.
- An alert should reference its finding and policy basis.
- A rollup summary should not pretend to be complete local truth.
- A report is an output, not source evidence.
