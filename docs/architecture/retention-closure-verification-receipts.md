# Retention Closure Verification Receipts

PFEM retention closure verification receipts add the next retention closure boundary.

The boundary is:

```text
retention closure record                = closure record for the registered retention certificate path
retention closure verification receipt  = evidence that closure refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention closure record:
closure record for the registered retention certificate path

retention closure verification receipt:
evidence that closure refs/digest were checked
```
