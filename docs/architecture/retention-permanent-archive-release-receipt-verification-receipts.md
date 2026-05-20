# Retention Permanent Archive Release Receipt Verification Receipts

PFEM retention permanent archive release receipt verification receipts add the next permanent-archive continuation boundary.

The boundary is:

```text
retention permanent archive release receipt record = permanent-archive-release-receipt layer permanent archive release receipt record
retention permanent archive release receipt verification receipt = evidence that permanent archive release receipt refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive release receipt record:
permanent-archive-release-receipt layer permanent archive release receipt record

retention permanent archive release receipt verification receipt:
evidence that permanent archive release receipt refs/digest were checked
```
