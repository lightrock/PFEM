# Apply Receipts

PFEM apply receipts record what actually happened after a merge decision.

The boundary is:

```text
conflict record     = local/incoming conflict-check fact
merge decision      = local conflict/update judgment
apply receipt       = actual local apply/skip/fail result
```

## Why apply receipts exist

A merge decision is a judgment.

An apply receipt is evidence of execution.

A merge decision can say:

```text
Accept the incoming records.
```

An apply receipt can say:

```text
These local records were actually created, updated, skipped, or failed.
```

That keeps local repository mutation auditable instead of treating a decision as if it already happened.

## Typical apply states

An apply receipt can say:

- planned
- applied
- skipped
- failed
- partially_applied
- rolled_back
