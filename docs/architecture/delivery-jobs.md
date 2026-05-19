# Delivery Jobs

PFEM delivery jobs are planned movement work.

The boundary is:

```text
routing policy     = where should it go?
delivery channel   = what movement method is allowed?
transport adapter  = what implementation hook may move it?
delivery job       = what movement work is queued/planned/assigned?
transport receipt  = what movement was attempted or completed?
```

## Why add delivery jobs?

A routing rule is not a job.

A transport adapter definition is not a job.

A transport receipt records what happened, but it should not be the only place where planned movement exists.

Delivery jobs let PFEM represent work such as:

```text
Export this bundle through this route/channel/adapter.
```

without pretending the work has already happened.

## Delivery jobs are not transport receipts

A delivery job may be:

- proposed
- queued
- ready
- in_progress
- completed
- failed
- cancelled
- blocked

A transport receipt records a specific attempt/result. One delivery job may eventually have multiple transport receipts if retries happen.
