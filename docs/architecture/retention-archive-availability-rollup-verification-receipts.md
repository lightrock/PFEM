# Retention Archive Availability Rollup Verification Receipts

PFEM retention archive availability rollup verification receipts add the next retention post-access boundary.

The boundary is:

```text
retention archive availability rollup record = archive-availability-rollup layer archive availability rollup record
retention archive availability rollup verification receipt = evidence that archive availability rollup refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention archive availability rollup record:
archive-availability-rollup layer archive availability rollup record

retention archive availability rollup verification receipt:
evidence that archive availability rollup refs/digest were checked
```
