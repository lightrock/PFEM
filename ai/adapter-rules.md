# Adapter Rules

Adapters translate source-specific inputs into PFEM contracts.

Adapters may:

- connect to external or local input sources
- parse source-specific formats
- validate incoming payloads
- preserve raw input where configured
- emit normalized observations
- report health and freshness
- support replay for tests and demonstrations

Adapters must not:

- own deployment policy
- decide final severity
- mutate rollup state directly
- bypass boundary rules
- depend on dashboard code
- hide uncertainty
- silently discard source records

When adding an adapter, include samples and contract tests.
