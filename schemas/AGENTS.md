# schemas/AGENTS.md

Schemas define PFEM contracts.

Rules:

- Keep schemas stable and versionable.
- Prefer additive changes when possible.
- Required fields should represent real contract requirements, not convenience.
- Do not delete or rename contract fields without updating docs, examples, and tests.
- Schema names should match domain object names.
- Derived-object schemas should include lineage references where appropriate.
