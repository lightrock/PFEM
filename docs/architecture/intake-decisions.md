# Intake Decisions

PFEM intake decisions are receiver-side decisions about inbox items.

The boundary is:

```text
transport receipt   = movement was attempted or completed
inbox item          = receiver-side staged payload
intake decision     = receiver-side decision about that staged payload
exchange receipt    = exchange-layer acceptance/rejection result
```

## Why intake decisions exist

An inbox item is custody/staging.

An intake decision is judgment.

Example:

```text
Inbox:
The received bundle is staged.

Intake decision:
This received bundle may enter exchange processing.
```

That is still not the same as an exchange receipt. Exchange receipts remain the exchange-layer result record.

## Typical intake decisions

An intake decision can say:

- allowed_for_exchange
- quarantined
- rejected
- deferred
- unknown
