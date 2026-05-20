# Retention Permanent Archive Terminal Monitoring Snapshot Verification Receipts

PFEM retention permanent archive terminal monitoring snapshot verification receipts add the next permanent-archive assurance boundary.

The boundary is:

```text
retention permanent archive terminal monitoring snapshot record = permanent-archive-terminal-monitoring-snapshot layer permanent archive terminal monitoring snapshot record
retention permanent archive terminal monitoring snapshot verification receipt = evidence that permanent archive terminal monitoring snapshot refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive terminal monitoring snapshot record:
permanent-archive-terminal-monitoring-snapshot layer permanent archive terminal monitoring snapshot record

retention permanent archive terminal monitoring snapshot verification receipt:
evidence that permanent archive terminal monitoring snapshot refs/digest were checked
```
