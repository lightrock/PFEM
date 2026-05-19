# Disposition Receipts

PFEM disposition receipts record that disposition actions actually happened.

The boundary is:

```text
disposition record   = retain/archive/export/remove/hold decision for closed artifacts
disposition receipt  = evidence that disposition actions were executed
retention policy     = standing rule basis for disposition decisions
```

## Why disposition receipts exist

A disposition record says:

```text
These closed workflow artifacts should be retained, archived, exported, removed, or held.
```

A disposition receipt says:

```text
Those disposition actions actually happened, with completed/skipped/failed results.
```

That keeps records-management decisions separate from execution evidence.

## Typical receipt states

A disposition receipt can say:

- completed
- partially_completed
- failed
- skipped
- pending
