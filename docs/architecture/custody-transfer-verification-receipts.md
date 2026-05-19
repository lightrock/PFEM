# Custody Transfer Verification Receipts

PFEM custody transfer verification receipts record that destination custody was checked after a custody transfer or formal custody re-assertion.

The boundary is:

```text
custody verification receipt           = evidence that current custody was checked
custody transfer record                = custody moved or was formally re-asserted
custody transfer verification receipt  = evidence that destination custody was checked afterward
```

## Why custody transfer verification receipts exist

A custody transfer record says:

```text
Custody moved from here to there, or was formally re-asserted in the same place.
```

A custody transfer verification receipt says:

```text
After that transfer/re-assertion, we checked the destination custodian/location and the artifacts were present or missing.
```

That gives PFEM a closed chain-of-custody edge: checked before transfer, recorded transfer, checked after transfer.

## Typical verification states

A custody transfer verification receipt can say:

- passed
- failed
- partially_passed
- skipped
- stale
