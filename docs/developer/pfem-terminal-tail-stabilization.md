# PFEM Terminal Tail Stabilization

This is the first post-doodad stabilization check.

The final permanent-archive terminal tail now ends at:

```text
retention permanent archive terminal closure final endcap closeout records
```

This check deliberately does **not** add another record species. It verifies that the terminal tail is closed and that the final terminal verification receipt schemas do not repeat the `missing_refs` contract problem.

## What it checks

```text
- the final endcap closeout record exists
- final terminal closure verification schemas are present
- missing_refs is optional in those schemas
- missing_refs remains available as an array property
- final terminal verification receipt JSON files include missing_refs as a diagnostic array
- passed receipts do not contain non-empty missing_refs
```

## Why this exists

The schema contract gate caught repeated failures where `missing_refs` was present as an empty diagnostic array but also listed as required. In this PFEM pattern, `missing_refs` should be available, but for passed receipts it should not be a required non-empty field.

This audit keeps that rule explicit.
