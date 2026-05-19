# Restore Verification Receipts

PFEM restore verification receipts record that restored state was checked after restore execution.

The boundary is:

```text
restore approval              = authorization to execute a restore plan
restore receipt               = evidence that restore execution happened
restore verification receipt  = evidence that restored state was checked afterward
```

## Why restore verification receipts exist

A restore receipt says:

```text
The restore ran.
```

A restore verification receipt says:

```text
After the restore ran, we checked the restored state and it passed/failed.
```

That keeps execution evidence separate from post-execution verification.

## Typical verification states

A restore verification receipt can say:

- passed
- failed
- partially_passed
- skipped
- stale
