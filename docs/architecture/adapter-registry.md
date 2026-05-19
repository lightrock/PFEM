# Adapter Registry

PFEM keeps an adapter registry at:

```text
adapters/adapter-registry.json
```

The registry is a simple index of known adapters and their manifest paths.

## Purpose

The registry makes adapter discovery explicit.

It helps humans and AI assistants answer:

- what adapters exist?
- where is each manifest?
- is this adapter a template, example, or real configured adapter?
- which adapter ids are already taken?

## Rules

- Every non-temporary adapter should have an entry in the registry.
- The `adapter_id` in the registry must match the adapter manifest.
- Registry paths should point to `adapter.yaml` files.
- The registry does not replace adapter manifests.
- The registry is an index, not a policy engine.
