# Audit Journal

PFEM audit records describe important architecture events.

They answer:

```text
What important action happened, when, by what actor/tool, and what records did it affect?
```

## What audit is

Audit is a lightweight event journal for the pattern:

- review approved
- integrity receipts generated
- policy changed
- topology changed
- federation message prepared
- evidence package assembled

## What audit is not

Audit is not authentication. It is not a legal signature. It is not a secure append-only log by itself.

It is an architecture hook that lets PFEM keep important events tied back to records.
