# Retention Terminal Permanent Integrity Receipt Verification Receipts

PFEM retention terminal permanent integrity receipt verification receipts add the next permanent-archive retention boundary.

The boundary is:

```text
retention terminal permanent integrity receipt record = terminal-permanent-integrity-receipt layer terminal permanent integrity receipt record
retention terminal permanent integrity receipt verification receipt = evidence that terminal permanent integrity receipt refs/digest were checked
```

## Why this exists

This keeps one PFEM responsibility separate from the next.

Plain English:

```text
retention terminal permanent integrity receipt record:
terminal-permanent-integrity-receipt layer terminal permanent integrity receipt record

retention terminal permanent integrity receipt verification receipt:
evidence that terminal permanent integrity receipt refs/digest were checked
```
