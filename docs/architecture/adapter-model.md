# Adapter Model

Adapters translate source-specific input into PFEM contracts.

Adapters may:

- connect to source systems
- decode source-specific formats
- validate raw payloads
- emit raw evidence records
- emit normalized observations
- report adapter health
- support replay for testing

Adapters must not:

- own policy
- decide final alert severity
- mutate rollup state directly
- silently rewrite source payloads
- hide uncertainty
- depend on UI code to function

## Adapter shape

Each adapter should provide:

- adapter manifest
- decoder
- normalizer
- health check
- sample raw inputs
- sample normalized outputs
- contract tests

The core system should depend on adapter contracts, not source-specific assumptions.
