# Review Decisions

PFEM separates named policy gates from review records.

Policy says:

```text
This kind of sharing requires review.
```

Review records say:

```text
This specific thing was reviewed under this gate.
```

## Rules

- A review record should reference a known review gate.
- A review record should reference existing lifecycle, rollup, or federation records.
- A reviewed federation message should match the gate required by its topology link.
- A review record is not authentication.
- A review record is not legal approval by itself.
- It is an architecture-level audit hook.
