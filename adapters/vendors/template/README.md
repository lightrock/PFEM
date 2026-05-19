# Template Adapter

This is the starter shape for a PFEM adapter.

An adapter translates source-specific input into PFEM contracts.

Expected files:

- `adapter.yaml`
- `decoder.py`
- `normalizer.py`
- `health.py`
- `replay.py`
- `samples/raw/`
- `samples/normalized/`

The template code is intentionally small. Real adapters should add source-specific parsing, tests, and sample records.
