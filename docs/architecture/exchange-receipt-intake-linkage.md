# Exchange Receipt Intake Linkage

PFEM exchange receipts should be able to point back to the receiver-side intake path when the receipt is about a received/accepted payload.

The boundary is:

```text
transport receipt   = movement was attempted or completed
inbox item          = receiver-side staged payload
intake decision     = receiver-side allow/quarantine/reject/defer decision
exchange receipt    = exchange-layer result
```

## Why this matters

Before this linkage, an exchange receipt could say a bundle was accepted, but the accepted receipt did not necessarily point to the receiving-side custody trail.

With this linkage, an accepted exchange receipt can reference:

- the transport receipt
- the inbox item
- the intake decision
- the bundle artifact

That makes the exchange acceptance easier to audit.
