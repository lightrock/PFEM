# Manual Observer Report Adapter

The manual observer report adapter is the simplest PFEM input adapter.

It represents a human-entered or human-imported report. It is useful for field
notes, dashboard entry, imported forms, and low-equipment deployment shapes.

## Purpose

The adapter proves the PFEM adapter path without requiring a vendor source.

Flow:

1. A raw manual report is received.
2. The adapter decodes the source payload.
3. The adapter emits a raw evidence candidate.
4. The adapter normalizes the report into a normalized observation candidate.
5. Later PFEM services may turn observations into findings, alerts, packages, or rollups.

## Boundary

The adapter does not decide severity, policy, or final action. It preserves
reported content and marks uncertainty.
