# State Transitions

PFEM state transitions record how a node moved into a new checkpointed state.

The boundary is:

```text
apply receipt       = actual local apply/skip/fail result
state transition    = before/after bridge caused by one or more apply receipts
state checkpoint    = point-in-time known-good local state
```

## Why state transitions exist

A state checkpoint says:

```text
This is the known-good state.
```

A state transition says:

```text
This is how we got there.
```

That matters because a later operator or automation may need to answer:

- Which apply receipts created this checkpoint?
- Which records changed?
- Was this an initial/bootstrap transition or a transition from a prior checkpoint?
- Did the transition complete, fail, partially apply, or roll back?

## Initial transitions

The first checkpoint for a node may not have a previous checkpoint.

In that case, `from_state_checkpoint_id` may be null, while `to_state_checkpoint_id` points to the new known-good checkpoint.
