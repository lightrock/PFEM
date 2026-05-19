# Dispatch Decisions

PFEM dispatch decisions are per-job decision records.

The boundary is:

```text
dispatch policy    = rulebook for when jobs may run/retry/block
dispatch decision  = what PFEM decided for this specific job
delivery job       = the movement work item
transport receipt  = what movement was attempted or completed
```

## Why dispatch decisions exist

A dispatch policy rule is reusable.

A dispatch decision is specific.

Example:

```text
Policy:
Routine bundle delivery by manual export is allowed.

Decision:
delivery-job-basic-manual-export-001 was allowed by dispatch-manual-export-routine-bundle.
```

## Dispatch decisions are not receipts

A dispatch decision can say:

- allowed
- blocked
- deferred
- requires_review
- rejected
- unknown

That still does not prove that transport happened.

Transport receipts remain the proof/record of attempted or completed movement.
