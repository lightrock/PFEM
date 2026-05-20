# Retention Permanent Archive Terminal Policy Lock Record Verification Receipts

PFEM retention permanent archive terminal policy lock record verification receipts add the next permanent-archive assurance boundary.

The boundary is:

```text
retention permanent archive terminal policy lock record record = permanent-archive-terminal-policy-lock-record layer permanent archive terminal policy lock record record
retention permanent archive terminal policy lock record verification receipt = evidence that permanent archive terminal policy lock record refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive terminal policy lock record record:
permanent-archive-terminal-policy-lock-record layer permanent archive terminal policy lock record record

retention permanent archive terminal policy lock record verification receipt:
evidence that permanent archive terminal policy lock record refs/digest were checked
```
