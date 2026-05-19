# Retention Release Acknowledgement Verification Receipts

PFEM retention release acknowledgement verification receipts add the next retention release-continuation boundary.

The boundary is:

```text
retention release acknowledgement record = release-continuation release acknowledgement record
retention release acknowledgement verification receipt = evidence that release acknowledgement refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention release acknowledgement record:
release-continuation release acknowledgement record

retention release acknowledgement verification receipt:
evidence that release acknowledgement refs/digest were checked
```
