# Restore Plans

PFEM restore plans describe intended restore activity from a recovery point.

The boundary is:

```text
recovery point = verified snapshot promoted as restorable
restore plan   = intended restore scope and preconditions
restore receipt = future evidence that a restore actually happened
```

## Why restore plans exist

A recovery point says:

```text
This verified snapshot is available as a restore candidate.
```

A restore plan says:

```text
Here is what we intend to restore from that recovery point.
```

That keeps "safe to restore from" separate from "we are about to restore" and separate again from "we actually restored."

## Typical plan states

A restore plan can say:

- draft
- ready
- approved
- superseded
- cancelled
- executed
- failed
