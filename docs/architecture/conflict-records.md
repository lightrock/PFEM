# Conflict Records

PFEM conflict records capture local/incoming conflict-check facts.

The boundary is:

```text
import record       = local repository apply/stage/skip/fail result
conflict record     = local/incoming conflict-check fact
merge decision      = local conflict/update judgment
```

## Why conflict records exist

A merge decision should not hide its evidence.

A conflict record can say:

```text
No local conflict was found for these incoming records.
```

Or:

```text
Incoming record A conflicts with local record B.
```

Then a merge decision can cite that conflict record when it accepts, keeps, supersedes, rejects, or defers an incoming record.

## Typical conflict states

A conflict record can say:

- none_detected
- observed
- under_review
- resolved
- waived
- superseded
