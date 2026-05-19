# Retention Terminal Manifest Verification Receipts

PFEM retention terminal manifest verification receipts add the next retention release boundary.

The boundary is:

```text
retention terminal manifest record = release-layer terminal manifest record
retention terminal manifest verification receipt = evidence that terminal manifest refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal manifest record:
release-layer terminal manifest record

retention terminal manifest verification receipt:
evidence that terminal manifest refs/digest were checked
```
