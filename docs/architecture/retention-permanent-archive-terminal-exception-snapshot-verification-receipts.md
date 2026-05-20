# Retention Permanent Archive Terminal Exception Snapshot Verification Receipts

PFEM retention permanent archive terminal exception snapshot verification receipts add the next permanent-archive finalization boundary.

The boundary is:

```text
retention permanent archive terminal exception snapshot record = permanent-archive-terminal-exception-snapshot layer permanent archive terminal exception snapshot record
retention permanent archive terminal exception snapshot verification receipt = evidence that permanent archive terminal exception snapshot refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive terminal exception snapshot record:
permanent-archive-terminal-exception-snapshot layer permanent archive terminal exception snapshot record

retention permanent archive terminal exception snapshot verification receipt:
evidence that permanent archive terminal exception snapshot refs/digest were checked
```
