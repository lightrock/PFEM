# Profile Registry

PFEM keeps a profile registry at:

```text
profiles/profile-registry.json
```

The registry is a simple index of known node profiles and their manifest paths.

## Purpose

The registry makes profile discovery explicit.

It helps humans and AI assistants answer:

- what deployment shapes exist?
- where is each profile?
- which profile ids are already taken?
- is this profile an example, template, or configured profile?

## Rules

- Every reusable profile should have an entry in the registry.
- The `profile_id` in the registry must match the profile file.
- Registry paths should point to `*.profile.yaml` files.
- The registry does not replace profile files.
- The registry is an index, not policy.
