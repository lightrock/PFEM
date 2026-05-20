# Retention Terminal Final Digest Verification Receipts

PFEM retention terminal final digest verification receipts add the next terminal-status retention boundary.

The boundary is:

```text
retention terminal final digest record = terminal-final-digest layer terminal final digest record
retention terminal final digest verification receipt = evidence that terminal final digest refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal final digest record:
terminal-final-digest layer terminal final digest record

retention terminal final digest verification receipt:
evidence that terminal final digest refs/digest were checked
```
