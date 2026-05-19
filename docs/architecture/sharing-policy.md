# Sharing Policy

PFEM separates evidence lineage from sharing permission.

Lineage answers:

```text
Where did this record come from?
```

Sharing policy answers:

```text
Is this kind of sharing named and review-gated?
```

## Rules

- Profiles should reference known review gates.
- Rollup summaries should use known sharing scopes.
- Federation messages should use known sharing scopes.
- A sharing scope does not erase lineage.
- A federation message is still accountable to sender, scope, and lineage.
- Public or external summaries should be review-gated by profile policy.

## Tooling

Run:

```bat
pfem_policy.bat
```

or:

```bat
python tools\pfem_policy.py
```
