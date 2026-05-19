# Custody Chain Verification Receipts

PFEM custody chain verification receipts prove that a custody chain record was checked after it was summarized.

The boundary is:

```text
custody chain record                 = linked summary of the closed custody chain segment
custody chain verification receipt   = evidence that the chain summary and digest were checked
```

## Why custody chain verification receipts exist

A custody chain record says:

```text
Here is the full linked custody chain segment.
```

A custody chain verification receipt says:

```text
We checked that chain summary, its refs, and its digest.
```

That keeps the summary artifact separate from the verification of that summary.

## Typical verification states

A custody chain verification receipt can say:

- passed
- failed
- partially_passed
- skipped
- stale
