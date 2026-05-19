# Example Registry

PFEM keeps an example registry at:

```text
examples/example-registry.json
```

The registry is a simple index of known examples and their manifest paths.

## Purpose

The registry makes examples discoverable.

It helps humans and AI assistants answer:

- what examples exist?
- which profile does an example use?
- is the example runnable?
- where is the example manifest?
- which examples are shape-only examples?

## Rules

- Every reusable example should have an entry in the registry.
- The `example_id` in the registry must match the example manifest.
- Registry paths should point to `example.json` files.
- The registry does not replace example manifests.
- Runnable examples should be covered by tests.
