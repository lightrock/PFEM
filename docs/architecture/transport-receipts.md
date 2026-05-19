# Transport Receipts

PFEM transport receipts record actual or attempted movement.

The boundary is:

```text
routing policy     = where should it go?
delivery channel   = what movement method is allowed?
transport adapter  = what implementation hook may move it?
transport receipt  = what movement was attempted or completed?
```

## Why separate transport receipts?

Do not bury delivery outcomes inside the evidence, bundle, route, or transport adapter definition.

A transport receipt is an event-like record saying:

```text
This subject was attempted/sent/received/failed through this adapter/channel/route at this time.
```

## Transport receipts are not exchange receipts

Exchange receipts describe handoff acceptance/rejection at the PFEM exchange layer.

Transport receipts describe movement mechanics:

- attempted
- queued
- sent
- received
- succeeded
- failed
- cancelled
- unknown

A transport can succeed while the exchange decision later rejects the bundle. Those are different facts.
