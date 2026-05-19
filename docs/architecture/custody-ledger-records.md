# Custody Ledger Records

PFEM custody ledger records add the next custody boundary.

The boundary is:

```text
custody chain verification receipt = evidence that the chain summary/digest was checked
custody ledger record              = durable ledger entry for that verified chain segment
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
custody chain verification receipt:
evidence that the chain summary/digest was checked

custody ledger record:
durable ledger entry for that verified chain segment
```
