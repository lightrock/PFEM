# Retention Availability Notice Verification Receipts

PFEM retention availability notice verification receipts add the next retention release-continuation boundary.

The boundary is:

```text
retention availability notice record = release-continuation availability notice record
retention availability notice verification receipt = evidence that availability notice refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention availability notice record:
release-continuation availability notice record

retention availability notice verification receipt:
evidence that availability notice refs/digest were checked
```
