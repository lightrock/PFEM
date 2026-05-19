# Retention Repository Release Verification Receipts

PFEM retention repository release verification receipts add the next retention release boundary.

The boundary is:

```text
retention repository release record = release-layer repository release record
retention repository release verification receipt = evidence that repository release refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention repository release record:
release-layer repository release record

retention repository release verification receipt:
evidence that repository release refs/digest were checked
```
