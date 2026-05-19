# Merge Decisions

PFEM merge decisions record how imported payloads are resolved against local PFEM records.

The boundary is:

```text
exchange receipt    = exchange-layer acceptance/rejection result
import record       = local repository apply/stage/skip/fail result
merge decision      = local conflict/update decision for incoming records
```

## Why merge decisions exist

Import is not the same thing as conflict resolution.

An import record can say:

```text
This accepted bundle was applied or staged locally.
```

A merge decision can say:

```text
These incoming records were accepted because no local conflict was found.
```

Or:

```text
These incoming records were quarantined/deferred because they conflict with local records.
```

That keeps local update judgment visible on disk instead of hiding it inside import code.

## Typical merge decisions

A merge decision can say:

- accept_incoming
- keep_local
- supersede_local
- create_new_version
- defer_for_review
- reject_incoming
- no_op
