# Retention Terminal Retrieval Certificate Verification Receipts

PFEM retention terminal retrieval certificate verification receipts add the next terminal-status retention boundary.

The boundary is:

```text
retention terminal retrieval certificate record = terminal-retrieval-certificate layer terminal retrieval certificate record
retention terminal retrieval certificate verification receipt = evidence that terminal retrieval certificate refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal retrieval certificate record:
terminal-retrieval-certificate layer terminal retrieval certificate record

retention terminal retrieval certificate verification receipt:
evidence that terminal retrieval certificate refs/digest were checked
```
