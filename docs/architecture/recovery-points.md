# Recovery Points

PFEM recovery points promote verified snapshots into safe restore candidates.

The boundary is:

```text
snapshot manifest             = itemized materialized contents of a checkpoint
snapshot verification receipt = evidence that the snapshot was checked
recovery point                = verified snapshot promoted as restorable
```

## Why recovery points exist

A snapshot verification receipt says:

```text
We checked this snapshot and it passed.
```

A recovery point says:

```text
This verified snapshot is available as a restore candidate.
```

That avoids treating every verified snapshot as automatically approved for recovery workflows.

## Typical recovery states

A recovery point can say:

- available
- superseded
- revoked
- archived
- failed
