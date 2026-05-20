# Retention Permanent Archive Terminal Service Snapshot Verification Receipts

PFEM retention permanent archive terminal service snapshot verification receipts add the next permanent-archive finalization boundary.

The boundary is:

```text
retention permanent archive terminal service snapshot record = permanent-archive-terminal-service-snapshot layer permanent archive terminal service snapshot record
retention permanent archive terminal service snapshot verification receipt = evidence that permanent archive terminal service snapshot refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive terminal service snapshot record:
permanent-archive-terminal-service-snapshot layer permanent archive terminal service snapshot record

retention permanent archive terminal service snapshot verification receipt:
evidence that permanent archive terminal service snapshot refs/digest were checked
```
