# Retention Release Health Snapshot Verification Receipts

PFEM retention release health snapshot verification receipts add the next retention access/release boundary.

The boundary is:

```text
retention release health snapshot record = release-health layer release health snapshot record
retention release health snapshot verification receipt = evidence that release health snapshot refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention release health snapshot record:
release-health layer release health snapshot record

retention release health snapshot verification receipt:
evidence that release health snapshot refs/digest were checked
```
