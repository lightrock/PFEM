# Retention Release Exception Register Verification Receipts

PFEM retention release exception register verification receipts add the next retention post-access boundary.

The boundary is:

```text
retention release exception register record = release-exception-register layer release exception register record
retention release exception register verification receipt = evidence that release exception register refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention release exception register record:
release-exception-register layer release exception register record

retention release exception register verification receipt:
evidence that release exception register refs/digest were checked
```
