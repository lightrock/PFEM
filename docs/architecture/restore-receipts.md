# Restore Receipts

PFEM restore receipts record that an approved restore actually executed.

The boundary is:

```text
restore plan     = intended restore scope and preconditions
restore approval = authorization to execute that plan
restore receipt  = evidence that restore execution happened
```

## Why restore receipts exist

A restore approval says:

```text
This restore plan is authorized.
```

A restore receipt says:

```text
This approved restore actually ran, and these records were restored, skipped, or failed.
```

That keeps authorization separate from execution evidence.

## Typical restore states

A restore receipt can say:

- completed
- partially_completed
- failed
- skipped
- rolled_back
