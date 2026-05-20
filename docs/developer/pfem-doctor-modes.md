# PFEM Doctor Modes

PFEM doctor is intentionally shallow by default.

The doctor checks repository-level health:

```text
expected paths
JSON syntax
adapter manifests
capability manifests
node profiles
neutral public-language scan
```

It no longer re-runs the full generated validator chain by default. The full check runner already owns that work step-by-step through:

```text
pfem_check.bat --full
```

Use deep mode only when deliberately debugging the historical nested doctor behavior:

```bat
python tools\pfem_doctor.py --deep
```

Normal use:

```bat
python tools\pfem_doctor.py
pfem_check.bat --doctor --timings
```

This keeps doctor useful without turning it into another full-suite run hidden inside a single step.
