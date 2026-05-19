# Retention Publication Rollup Verification Receipts

PFEM retention publication rollup verification receipts add the next retention access/release boundary.

The boundary is:

```text
retention publication rollup record = publication-rollup layer publication rollup record
retention publication rollup verification receipt = evidence that publication rollup refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention publication rollup record:
publication-rollup layer publication rollup record

retention publication rollup verification receipt:
evidence that publication rollup refs/digest were checked
```
