# Retention Registry Verification Receipts

PFEM retention registry verification receipts add the next retention closure boundary.

The boundary is:

```text
retention registry record                = registry entry for the closed retention certificate
retention registry verification receipt  = evidence that registry refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention registry record:
registry entry for the closed retention certificate

retention registry verification receipt:
evidence that registry refs/digest were checked
```
