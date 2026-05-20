# Retention Terminal Permanent Archive Index Verification Receipts

PFEM retention terminal permanent archive index verification receipts add the next permanent-archive retention boundary.

The boundary is:

```text
retention terminal permanent archive index record = terminal-permanent-archive-index layer terminal permanent archive index record
retention terminal permanent archive index verification receipt = evidence that terminal permanent archive index refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal permanent archive index record:
terminal-permanent-archive-index layer terminal permanent archive index record

retention terminal permanent archive index verification receipt:
evidence that terminal permanent archive index refs/digest were checked
```
