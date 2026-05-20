# Retention Public Release Receipt Verification Receipts

PFEM retention public release receipt verification receipts add the next retention post-access boundary.

The boundary is:

```text
retention public release receipt record = public-release-receipt layer public release receipt record
retention public release receipt verification receipt = evidence that public release receipt refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention public release receipt record:
public-release-receipt layer public release receipt record

retention public release receipt verification receipt:
evidence that public release receipt refs/digest were checked
```
