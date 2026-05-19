# Custody Records

PFEM custody records say where retained/exported/archived artifacts are held and who is responsible for them.

The boundary is:

```text
disposition record   = retain/archive/export/remove/hold decision
disposition receipt  = evidence that disposition actions executed
custody record       = where the resulting artifacts are held and by whom
```

## Why custody records exist

A disposition receipt says:

```text
These disposition actions actually happened.
```

A custody record says:

```text
These retained/exported/archived artifacts are now held here by this custodian.
```

That keeps action execution separate from ongoing responsibility and location.

## Typical custody states

A custody record can say:

- active
- transferred
- released
- archived
- revoked
- missing
- superseded
