# Capabilities

Capabilities are reusable PFEM behaviors.

A node profile enables or disables capabilities. Profiles should reference named
capabilities rather than inventing behavior inline.

Capability manifests live under this folder as `*.capability.yaml`.

A capability manifest should include:

- `capability_id`
- `display_name`
- `capability_kind`
- optional `description`
- optional `requires`
- optional `produces`

Capabilities are not products. They are building blocks used by deployment
profiles.
