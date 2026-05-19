# Retention Retrieval Endpoint Verification Receipts

PFEM retention retrieval endpoint verification receipts add the next retention access/release boundary.

The boundary is:

```text
retention retrieval endpoint record = retrieval-endpoint layer retrieval endpoint record
retention retrieval endpoint verification receipt = evidence that retrieval endpoint refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention retrieval endpoint record:
retrieval-endpoint layer retrieval endpoint record

retention retrieval endpoint verification receipt:
evidence that retrieval endpoint refs/digest were checked
```
