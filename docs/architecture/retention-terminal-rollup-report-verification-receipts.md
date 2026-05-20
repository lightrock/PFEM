# Retention Terminal Rollup Report Verification Receipts

PFEM retention terminal rollup report verification receipts add the next terminal-status retention boundary.

The boundary is:

```text
retention terminal rollup report record = terminal-rollup-report layer terminal rollup report record
retention terminal rollup report verification receipt = evidence that terminal rollup report refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal rollup report record:
terminal-rollup-report layer terminal rollup report record

retention terminal rollup report verification receipt:
evidence that terminal rollup report refs/digest were checked
```
