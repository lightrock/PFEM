# Snapshot Manifests

PFEM snapshot manifests list the materialized records behind a state checkpoint.

The boundary is:

```text
state transition    = how PFEM reached a checkpoint
state checkpoint    = point-in-time known-good local state
snapshot manifest   = itemized materialized contents of that checkpoint
```

## Why snapshot manifests exist

A state checkpoint is a compact marker.

A snapshot manifest answers:

```text
What records/files make up this checkpoint?
```

That gives PFEM a practical recovery and inspection target without requiring a full replay of every previous receipt, decision, transition, and checkpoint.

## Snapshot manifests are not integrity manifests

Integrity receipts verify file/artifact digests.

Snapshot manifests identify the domain records that compose a state checkpoint and can carry their own manifest digest.
