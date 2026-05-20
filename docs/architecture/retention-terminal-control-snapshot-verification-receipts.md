# Retention Terminal Control Snapshot Verification Receipts

PFEM retention terminal control snapshot verification receipts add the next terminal-status retention boundary.

The boundary is:

```text
retention terminal control snapshot record = terminal-control-snapshot layer terminal control snapshot record
retention terminal control snapshot verification receipt = evidence that terminal control snapshot refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal control snapshot record:
terminal-control-snapshot layer terminal control snapshot record

retention terminal control snapshot verification receipt:
evidence that terminal control snapshot refs/digest were checked
```
