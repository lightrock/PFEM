# Retention Ledger Records

PFEM retention ledger records add the next retention boundary.

The boundary is:

```text
retention lifecycle closeout record = formal closure of the retention lifecycle
retention ledger record             = durable ledger entry for that closed retention lifecycle
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention lifecycle closeout record:
formal closure of the retention lifecycle

retention ledger record:
durable ledger entry for that closed retention lifecycle
```
