# Retention Permanent Archive Public Digest Verification Receipts

PFEM retention permanent archive public digest verification receipts add the next permanent-archive continuation boundary.

The boundary is:

```text
retention permanent archive public digest record = permanent-archive-public-digest layer permanent archive public digest record
retention permanent archive public digest verification receipt = evidence that permanent archive public digest refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention permanent archive public digest record:
permanent-archive-public-digest layer permanent archive public digest record

retention permanent archive public digest verification receipt:
evidence that permanent archive public digest refs/digest were checked
```
