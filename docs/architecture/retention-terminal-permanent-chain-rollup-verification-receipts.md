# Retention Terminal Permanent Chain Rollup Verification Receipts

PFEM retention terminal permanent chain rollup verification receipts add the next permanent-archive retention boundary.

The boundary is:

```text
retention terminal permanent chain rollup record = terminal-permanent-chain-rollup layer terminal permanent chain rollup record
retention terminal permanent chain rollup verification receipt = evidence that terminal permanent chain rollup refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal permanent chain rollup record:
terminal-permanent-chain-rollup layer terminal permanent chain rollup record

retention terminal permanent chain rollup verification receipt:
evidence that terminal permanent chain rollup refs/digest were checked
```
