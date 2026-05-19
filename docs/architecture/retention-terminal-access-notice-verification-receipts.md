# Retention Terminal Access Notice Verification Receipts

PFEM retention terminal access notice verification receipts add the next retention access/release boundary.

The boundary is:

```text
retention terminal access notice record = terminal-access-notice layer terminal access notice record
retention terminal access notice verification receipt = evidence that terminal access notice refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal access notice record:
terminal-access-notice layer terminal access notice record

retention terminal access notice verification receipt:
evidence that terminal access notice refs/digest were checked
```
