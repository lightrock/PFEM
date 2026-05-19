# Inbox Items

PFEM inbox items are receiver-side staged payloads.

The boundary is:

```text
outbox item         = staged payload on the sending side
transport receipt   = what transport attempted or completed
inbox item          = staged payload on the receiving side
exchange receipt    = exchange-layer acceptance/rejection decision
```

## Why inbox items exist

Transport success is not the same thing as receiver-side intake.

An inbox item says:

```text
The receiving side has this payload staged and ready for validation, exchange processing, review, or rejection.
```

This keeps custody and intake separate from both transport mechanics and exchange decisions.

## Inbox items are not exchange receipts

An inbox item can be:

- received
- quarantined
- ready_for_exchange
- accepted_for_exchange
- rejected
- expired
- failed

An exchange receipt later says whether the exchange layer accepted or rejected the bundle/message.
