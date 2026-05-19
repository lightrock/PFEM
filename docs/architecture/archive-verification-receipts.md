# Archive Verification Receipts

PFEM archive verification receipts add the next lifecycle/archive boundary.

The boundary is:

```text
archive receipt                = evidence that archive action actually happened
archive verification receipt   = evidence that archived refs/location were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
archive receipt:
evidence that archive action actually happened

archive verification receipt:
evidence that archived refs/location were checked
```
