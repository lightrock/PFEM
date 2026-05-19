# Evidence Rules

PFEM treats evidence as a first-class domain object.

Rules:

- Keep raw evidence separate from derived objects.
- Preserve source, time, and provenance metadata.
- Make transformations explicit.
- Link normalized observations back to source evidence.
- Link findings back to observations and reasoning.
- Link alerts back to findings and policy basis.
- Treat rollups as summaries, not complete local truth.
- Treat reports as human-facing outputs, not source records.
- Mark uncertainty instead of hiding it.

If a change makes evidence easier to read but harder to trace, it is probably wrong.
