# Restore Approvals

PFEM restore approvals authorize a restore plan before restore execution.

The boundary is:

```text
restore plan     = intended restore scope and preconditions
restore approval = authorization to execute that plan
restore receipt  = future evidence that a restore actually happened
```

## Why restore approvals exist

A restore plan says:

```text
Here is what we intend to restore.
```

A restore approval says:

```text
This restore plan is approved for execution under these constraints.
```

That keeps "we planned it" separate from "we authorized it" and separate again from "we executed it."

## Typical approval states

A restore approval can say:

- approved
- rejected
- deferred
- revoked
- superseded
