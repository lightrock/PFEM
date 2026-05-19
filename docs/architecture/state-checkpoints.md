# State Checkpoints

PFEM state checkpoints mark a local known-good state after apply receipts.

The boundary is:

```text
merge decision      = local conflict/update judgment
apply receipt       = actual local apply/skip/fail result
state checkpoint    = point-in-time known-good local state
```

## Why state checkpoints exist

An apply receipt says an action happened.

A state checkpoint says:

```text
After those apply receipts, this is the local known-good set of records.
```

That gives PFEM a stable recovery/audit marker without pretending that every state query must replay the whole chain every time.

## State checkpoints are not integrity receipts

Integrity receipts prove file/artifact bytes or canonical JSON digests.

State checkpoints prove a domain-level state marker:

```text
This node considers these PFEM record IDs the current known-good state.
```
