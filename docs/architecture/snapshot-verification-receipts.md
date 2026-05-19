# Snapshot Verification Receipts

PFEM snapshot verification receipts record that a snapshot manifest was checked.

The boundary is:

```text
state checkpoint              = point-in-time known-good local state
snapshot manifest             = itemized materialized contents of that checkpoint
snapshot verification receipt = evidence that the manifest/items/digest were checked
```

## Why snapshot verification receipts exist

A snapshot manifest says:

```text
These records/files make up this checkpoint.
```

A snapshot verification receipt says:

```text
We checked that manifest and the verification passed/failed.
```

That lets PFEM distinguish a declared snapshot from a verified snapshot.

## Typical verification states

A snapshot verification receipt can say:

- passed
- failed
- partially_passed
- skipped
- stale
