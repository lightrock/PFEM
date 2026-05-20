# Retention Permanent Archive Terminal Custody Snapshot Verification Receipts

PFEM retention permanent archive terminal custody snapshot verification receipts add the next permanent-archive finalization boundary.

The boundary is:

```text
retention permanent archive terminal custody snapshot record = permanent-archive-terminal-custody-snapshot layer permanent archive terminal custody snapshot record
retention permanent archive terminal custody snapshot verification receipt = evidence that permanent archive terminal custody snapshot refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive terminal custody snapshot record:
permanent-archive-terminal-custody-snapshot layer permanent archive terminal custody snapshot record

retention permanent archive terminal custody snapshot verification receipt:
evidence that permanent archive terminal custody snapshot refs/digest were checked
```
