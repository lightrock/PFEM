# Retention Terminal Storage Receipt Verification Receipts

PFEM retention terminal storage receipt verification receipts add the next terminal-status retention boundary.

The boundary is:

```text
retention terminal storage receipt record = terminal-storage-receipt layer terminal storage receipt record
retention terminal storage receipt verification receipt = evidence that terminal storage receipt refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal storage receipt record:
terminal-storage-receipt layer terminal storage receipt record

retention terminal storage receipt verification receipt:
evidence that terminal storage receipt refs/digest were checked
```
