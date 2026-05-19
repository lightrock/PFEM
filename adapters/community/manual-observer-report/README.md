# Manual Observer Report Adapter

This adapter converts a human-entered or imported report into PFEM records.

It is intentionally simple:

- `decoder.py` preserves the raw report as a raw evidence candidate.
- `normalizer.py` derives a normalized observation candidate.
- `samples/raw/example.json` shows a source payload.
- `samples/normalized/example.json` shows the expected observation shape.

This adapter does not decide severity, policy, or actions.
