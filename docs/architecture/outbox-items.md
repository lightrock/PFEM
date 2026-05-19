# Outbox Items

PFEM outbox items are staged payloads ready for transport pickup.

The boundary is:

```text
delivery job        = movement work item
dispatch decision   = allowed/blocked/deferred decision for that job
outbox item         = staged payload/artifact ready to be picked up
transport receipt   = what transport attempted or completed
```

## Why outbox items exist

A delivery job is not the payload.

A dispatch decision is not the payload.

A transport receipt proves an attempt/result, but it should not be the first place the staged payload appears.

An outbox item says:

```text
This bundle/report/message was staged here, for this job, after this dispatch decision.
```

## Outbox items are not transport receipts

Outbox item states can include:

- staged
- ready
- picked_up
- cancelled
- expired
- failed

A transport receipt later records whether a transport adapter actually attempted or completed movement.
