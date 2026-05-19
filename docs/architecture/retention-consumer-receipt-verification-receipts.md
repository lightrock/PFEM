# Retention Consumer Receipt Verification Receipts

PFEM retention consumer receipt verification receipts add the next retention access/release boundary.

The boundary is:

```text
retention consumer receipt record = consumer-receipt layer consumer receipt record
retention consumer receipt verification receipt = evidence that consumer receipt refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention consumer receipt record:
consumer-receipt layer consumer receipt record

retention consumer receipt verification receipt:
evidence that consumer receipt refs/digest were checked
```
