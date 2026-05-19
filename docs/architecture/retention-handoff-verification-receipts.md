# Retention Handoff Verification Receipts

PFEM retention handoff verification receipts add the next retention handoff/export boundary.

The boundary is:

```text
retention handoff record                = handoff event for verified retention export
retention handoff verification receipt  = evidence that handoff refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention handoff record:
handoff event for verified retention export

retention handoff verification receipt:
evidence that handoff refs/digest were checked
```
