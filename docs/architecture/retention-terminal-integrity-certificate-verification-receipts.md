# Retention Terminal Integrity Certificate Verification Receipts

PFEM retention terminal integrity certificate verification receipts add the next terminal-status retention boundary.

The boundary is:

```text
retention terminal integrity certificate record = terminal-integrity-certificate layer terminal integrity certificate record
retention terminal integrity certificate verification receipt = evidence that terminal integrity certificate refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal integrity certificate record:
terminal-integrity-certificate layer terminal integrity certificate record

retention terminal integrity certificate verification receipt:
evidence that terminal integrity certificate refs/digest were checked
```
