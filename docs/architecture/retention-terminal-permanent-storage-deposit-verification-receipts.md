# Retention Terminal Permanent Storage Deposit Verification Receipts

PFEM retention terminal permanent storage deposit verification receipts add the next permanent-archive retention boundary.

The boundary is:

```text
retention terminal permanent storage deposit record = terminal-permanent-storage-deposit layer terminal permanent storage deposit record
retention terminal permanent storage deposit verification receipt = evidence that terminal permanent storage deposit refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal permanent storage deposit record:
terminal-permanent-storage-deposit layer terminal permanent storage deposit record

retention terminal permanent storage deposit verification receipt:
evidence that terminal permanent storage deposit refs/digest were checked
```
