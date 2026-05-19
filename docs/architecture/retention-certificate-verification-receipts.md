# Retention Certificate Verification Receipts

PFEM retention certificate verification receipts add the next retention closure boundary.

The boundary is:

```text
retention certificate record                = certificate issued for closed terminal retention status
retention certificate verification receipt  = evidence that certificate refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention certificate record:
certificate issued for closed terminal retention status

retention certificate verification receipt:
evidence that certificate refs/digest were checked
```
