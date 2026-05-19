# Restore Closeout Records

PFEM restore closeout records close a restore workflow after post-restore verification.

The boundary is:

```text
restore receipt              = evidence that restore execution happened
restore verification receipt = evidence that restored state was checked afterward
restore closeout record      = final operational closure of the restore workflow
```

## Why restore closeout records exist

A restore verification receipt says:

```text
After the restore ran, we checked the restored state and it passed/failed.
```

A restore closeout record says:

```text
The restore workflow is now closed with this final outcome.
```

That keeps post-restore verification separate from final operational closure.

## Typical closeout states

A restore closeout record can say:

- closed
- closed_with_exceptions
- deferred
- escalated
- cancelled
- superseded
