# Custody Verification Receipts

PFEM custody verification receipts record that custody records were checked.

The boundary is:

```text
disposition receipt           = evidence that disposition actions executed
custody record                = where resulting artifacts are held and by whom
custody verification receipt  = evidence that the custody location/held refs were checked
```

## Why custody verification receipts exist

A custody record says:

```text
These artifacts are held here by this custodian.
```

A custody verification receipt says:

```text
We checked that custody location and these held artifacts were present or missing.
```

That keeps ongoing custody responsibility separate from verification evidence.

## Typical verification states

A custody verification receipt can say:

- passed
- failed
- partially_passed
- skipped
- stale
