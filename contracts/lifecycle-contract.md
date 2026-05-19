# Lifecycle Contract

The PFEM lifecycle contract is:

```text
raw evidence -> normalized observation -> finding -> alert -> evidence package
```

## Boundaries

- Raw evidence preserves source/provenance.
- Normalized observations derive common fields from evidence.
- Findings are interpretations tied to observations.
- Alerts are actionable surfaces tied to findings.
- Evidence packages collect referenced records for review or sharing.

Each step should preserve ids that allow lineage validation.
