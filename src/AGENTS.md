# src/AGENTS.md

Source code must follow PFEM doctrine.

Rules:

- Keep domain objects in `src/pfem/domain/`.
- Keep runtime support code separate from domain definitions.
- Do not let UI/dashboard code become source-of-truth code.
- Do not put source-specific parsing in the core domain model.
- Do not let adapters decide deployment policy.
- Do not let profiles redefine domain objects.
- Prefer small modules with explicit boundaries over generic `utils` dumping grounds.
