# Retention Terminal Permanent Archive Package Verification Receipts

PFEM retention terminal permanent archive package verification receipts add the next permanent-archive retention boundary.

The boundary is:

```text
retention terminal permanent archive package record = terminal-permanent-archive-package layer terminal permanent archive package record
retention terminal permanent archive package verification receipt = evidence that terminal permanent archive package refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal permanent archive package record:
terminal-permanent-archive-package layer terminal permanent archive package record

retention terminal permanent archive package verification receipt:
evidence that terminal permanent archive package refs/digest were checked
```
