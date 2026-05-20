# Retention Permanent Archive Terminal Health Snapshot Verification Receipts

PFEM retention permanent archive terminal health snapshot verification receipts add the next permanent-archive finalization boundary.

The boundary is:

```text
retention permanent archive terminal health snapshot record = permanent-archive-terminal-health-snapshot layer permanent archive terminal health snapshot record
retention permanent archive terminal health snapshot verification receipt = evidence that permanent archive terminal health snapshot refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive terminal health snapshot record:
permanent-archive-terminal-health-snapshot layer permanent archive terminal health snapshot record

retention permanent archive terminal health snapshot verification receipt:
evidence that permanent archive terminal health snapshot refs/digest were checked
```
