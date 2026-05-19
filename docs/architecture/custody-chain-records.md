# Custody Chain Records

PFEM custody chain records summarize a linked custody chain segment after it has been checked, transferred or re-asserted, destination-verified, and closed.

The boundary is:

```text
custody closeout record = final closure of one custody chain segment
custody chain record    = linked summary of the closed custody chain segment
```

## Why custody chain records exist

A custody closeout record says:

```text
This custody chain segment is closed.
```

A custody chain record says:

```text
Here are the linked custody records, verification receipts, transfer records, and closeout records that form the closed custody chain segment.
```

That keeps the individual chain events separate from the summarized chain view.

## Typical chain states

A custody chain record can say:

- open
- closed
- closed_with_exceptions
- broken
- superseded
