# Custody Ledger Verification Receipts

PFEM custody ledger verification receipts add the next custody boundary.

The boundary is:

```text
custody ledger record                = durable ledger entry for the verified chain
custody ledger verification receipt  = evidence that the ledger entry itself was checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
custody ledger record:
durable ledger entry for the verified chain

custody ledger verification receipt:
evidence that the ledger entry itself was checked
```
