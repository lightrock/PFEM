# Import Records

PFEM import records describe what happened after a received exchange payload was accepted.

The boundary is:

```text
inbox item          = receiver-side staged payload
intake decision     = receiver-side intake judgment
exchange receipt    = exchange-layer acceptance/rejection result
import record       = local repository apply/stage/skip/fail result
```

## Why import records exist

Acceptance is not the same thing as local application.

An exchange receipt can say:

```text
This bundle is accepted by the exchange layer.
```

An import record can say:

```text
This accepted bundle was applied into the receiver-side PFEM repository,
and these local records were created or updated.
```

That keeps exchange validation separate from local repository mutation.

## Typical import states

An import record can say:

- staged
- imported
- skipped
- failed
- superseded
- rejected
