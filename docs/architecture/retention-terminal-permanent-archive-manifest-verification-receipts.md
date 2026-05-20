# Retention Terminal Permanent Archive Manifest Verification Receipts

PFEM retention terminal permanent archive manifest verification receipts add the next permanent-archive retention boundary.

The boundary is:

```text
retention terminal permanent archive manifest record = terminal-permanent-archive-manifest layer terminal permanent archive manifest record
retention terminal permanent archive manifest verification receipt = evidence that terminal permanent archive manifest refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal permanent archive manifest record:
terminal-permanent-archive-manifest layer terminal permanent archive manifest record

retention terminal permanent archive manifest verification receipt:
evidence that terminal permanent archive manifest refs/digest were checked
```
