# Custody Transfer Records

PFEM custody transfer records document movement of custody from one custodian/location to another.

The boundary is:

```text
custody record                = where artifacts are held and by whom
custody verification receipt  = evidence that the custody location/held refs were checked
custody transfer record       = evidence that custody moved, or was formally re-asserted
```

## Why custody transfer records exist

A custody verification receipt says:

```text
We checked that these artifacts are held here.
```

A custody transfer record says:

```text
Custody moved from this custodian/location to that custodian/location.
```

For local-only workflows, the source and destination can be the same. That still matters because it gives PFEM a uniform chain-of-custody edge.

## Typical transfer states

A custody transfer record can say:

- completed
- partially_completed
- failed
- skipped
- pending
- cancelled
