# Integrity Receipts

PFEM integrity receipts add a simple tamper/drift check for important JSON artifacts.

They do not replace Git, signatures, authentication, or secure storage. They are a local architecture guardrail:

```text
This important JSON file has the same canonical content as when receipts were last generated.
```

## Why canonical JSON?

PFEM uses canonical JSON hashing for JSON files so Windows/Unix line endings and pretty-print spacing do not cause false failures.

## Rules

- Receipts should cover registries, policies, topology, reviews, and example lifecycle/federation fixtures.
- Intentional changes should regenerate receipts.
- Unexpected changes should fail validation.
- Receipts prove local content consistency, not legal authenticity or identity.
