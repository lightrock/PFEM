# Retention Rollup Verification Receipts

PFEM retention rollup verification receipts add the next retention reporting/publication boundary.

The boundary is:

```text
retention rollup record                = published rollup of verified retention status
retention rollup verification receipt  = evidence that retention rollup refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention rollup record:
published rollup of verified retention status

retention rollup verification receipt:
evidence that retention rollup refs/digest were checked
```
