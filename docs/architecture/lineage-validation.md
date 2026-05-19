# Lineage Validation

PFEM keeps derived objects linked to the records that produced them.

The minimum lifecycle chain is:

```text
raw evidence -> normalized observation -> finding -> alert
```

Evidence packages may include references to any records in that chain.

## Rules

- A normalized observation should reference existing raw evidence ids.
- A finding should reference existing normalized observation ids.
- An alert should reference an existing finding id.
- An evidence package should reference existing lifecycle record ids.
- A report is not source evidence.
- A rollup is a summary, not complete local truth.

## Tooling

Run:

```bat
pfem_lineage.bat
```

or:

```bat
python tools\pfem_lineage.py
```

The first validation target is the small lifecycle fixture in:

```text
tests/fixtures/lifecycle/basic/
```
