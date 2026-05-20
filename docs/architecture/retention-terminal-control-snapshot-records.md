# Retention Terminal Control Snapshot Records

PFEM retention terminal control snapshot records add the next terminal-status retention boundary.

The boundary is:

```text
retention terminal policy attestation closeout record = formal closure of retention terminal policy attestation workflow
retention terminal control snapshot record = terminal-control-snapshot layer terminal control snapshot record
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal policy attestation closeout record:
formal closure of retention terminal policy attestation workflow

retention terminal control snapshot record:
terminal-control-snapshot layer terminal control snapshot record
```
