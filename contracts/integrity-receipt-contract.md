# Integrity Receipt Contract

A PFEM integrity receipt should identify:

- `path`
- `digest_algorithm`
- `digest`
- `purpose`

Current algorithm:

```text
sha256-canonical-json
```

For JSON files, the digest is computed from parsed JSON serialized with sorted keys and compact separators.
