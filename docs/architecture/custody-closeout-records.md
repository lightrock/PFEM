# Custody Closeout Records

PFEM custody closeout records close a custody chain segment after transfer and destination verification.

The boundary is:

```text
custody transfer record                = custody moved or was formally re-asserted
custody transfer verification receipt  = evidence that destination custody was checked afterward
custody closeout record                = final closure of that custody chain segment
```

## Why custody closeout records exist

A custody transfer verification receipt says:

```text
After transfer/re-assertion, we checked destination custody.
```

A custody closeout record says:

```text
That custody chain segment is now closed with this final outcome.
```

That keeps the post-transfer check separate from formal custody-chain closure.

## Typical closeout states

A custody closeout record can say:

- closed
- closed_with_exceptions
- deferred
- escalated
- cancelled
- superseded
