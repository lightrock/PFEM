# Retention Terminal Custody Certificate Verification Receipts

PFEM retention terminal custody certificate verification receipts add the next terminal-status retention boundary.

The boundary is:

```text
retention terminal custody certificate record = terminal-custody-certificate layer terminal custody certificate record
retention terminal custody certificate verification receipt = evidence that terminal custody certificate refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal custody certificate record:
terminal-custody-certificate layer terminal custody certificate record

retention terminal custody certificate verification receipt:
evidence that terminal custody certificate refs/digest were checked
```
