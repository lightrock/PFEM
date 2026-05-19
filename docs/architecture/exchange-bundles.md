# Exchange Bundles

Exchange bundles define portable PFEM handoff manifests.

A bundle answers:

```text
What records and artifacts are traveling together, from which node, to which node, under what handling and retention rules?
```

## Bundle role

A bundle is not raw evidence, not a federation message, and not an archive format by itself.

It is a manifest that ties together:

- evidence package references
- rollup summary references
- federation message references
- review records
- audit records
- artifact paths

## Rules

- A bundle should reference known producer and recipient nodes.
- A bundle should use known sharing, handling, redaction, retention, and disposition values.
- A bundle should include known record refs or known artifact paths.
- A bundle should not erase lineage; it should carry lineage-supporting refs together.
