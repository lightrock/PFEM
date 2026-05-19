# Dispatch Policy

PFEM dispatch policy controls when delivery jobs are allowed to run, retry, block, or require review.

The boundary is:

```text
routing policy     = where should it go?
delivery channel   = what movement method is allowed?
transport adapter  = what implementation hook could move it?
delivery job       = what movement work is queued/planned/assigned?
dispatch policy    = when is that job allowed to run/retry/block?
transport receipt  = what movement was attempted or completed?
```

## Dispatch is not transport

Dispatch policy does not send data.

It answers questions like:

- Is this job eligible to run?
- Does this priority allow dispatch?
- Does this route/channel/adapter combination match a rule?
- Does this job require review before dispatch?
- How many attempts are allowed?
- What state should the job move to on success or failure?

## Why this matters

Without dispatch policy, retry behavior and manual-review behavior get hidden in scripts.

PFEM should keep those rules visible on disk so operators, reviewers, and AI agents can inspect them before movement happens.
