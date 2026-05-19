# Archive Index Verification Receipts

PFEM archive index verification receipts add the next archive boundary.

The boundary is:

```text
archive index record                = lookup/index entry for the verified archive chain
archive index verification receipt  = evidence that archive index refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
archive index record:
lookup/index entry for the verified archive chain

archive index verification receipt:
evidence that archive index refs/digest were checked
```
