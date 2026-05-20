# Retention Terminal Permanent Storage Receipt Verification Receipts

PFEM retention terminal permanent storage receipt verification receipts add the next permanent-archive retention boundary.

The boundary is:

```text
retention terminal permanent storage receipt record = terminal-permanent-storage-receipt layer terminal permanent storage receipt record
retention terminal permanent storage receipt verification receipt = evidence that terminal permanent storage receipt refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal permanent storage receipt record:
terminal-permanent-storage-receipt layer terminal permanent storage receipt record

retention terminal permanent storage receipt verification receipt:
evidence that terminal permanent storage receipt refs/digest were checked
```
