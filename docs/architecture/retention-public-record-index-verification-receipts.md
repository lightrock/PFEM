# Retention Public Record Index Verification Receipts

PFEM retention public record index verification receipts add the next retention access/release boundary.

The boundary is:

```text
retention public record index record = public-record-index layer public record index record
retention public record index verification receipt = evidence that public record index refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention public record index record:
public-record-index layer public record index record

retention public record index verification receipt:
evidence that public record index refs/digest were checked
```
