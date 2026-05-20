# Retention Permanent Archive Retention Lock Verification Receipts

PFEM retention permanent archive retention lock verification receipts add the next permanent-archive continuation boundary.

The boundary is:

```text
retention permanent archive retention lock record = permanent-archive-retention-lock layer permanent archive retention lock record
retention permanent archive retention lock verification receipt = evidence that permanent archive retention lock refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive retention lock record:
permanent-archive-retention-lock layer permanent archive retention lock record

retention permanent archive retention lock verification receipt:
evidence that permanent archive retention lock refs/digest were checked
```
