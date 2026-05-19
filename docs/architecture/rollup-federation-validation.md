# Rollup and Federation Validation

Lineage validation checks local evidence chains.

Rollup and federation validation checks derived sharing objects:

```text
local lifecycle records -> rollup summary -> federation message
```

## Rules

- A rollup summary should reference records that exist in the lifecycle chain.
- A rollup summary should identify the node that produced it.
- A federation message should identify the sending node.
- A federation message should preserve lineage references when it carries a summary.
- A federation message is not raw evidence.
- A rollup is not complete local truth.

## Tooling

Run:

```bat
pfem_rollup.bat
```

or:

```bat
python tools\pfem_rollup.py
```

The first validation target is:

```text
tests/fixtures/rollup/basic/
```
