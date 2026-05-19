# Source Provenance

PFEM separates adapter identity from source identity.

Adapter:

```text
How was input translated into PFEM shape?
```

Source:

```text
Where did the raw evidence come from?
```

Raw evidence should carry:

- `source_id`
- `provenance.adapter_id`

## Rules

- Every raw evidence `source_id` should be known in the source registry.
- Every source should reference a known adapter.
- Every source should reference a known node.
- Raw evidence provenance should reference a known adapter.
- Raw evidence should not become a finding, alert, or rollup by itself.
