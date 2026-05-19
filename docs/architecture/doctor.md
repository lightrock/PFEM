# PFEM Doctor

`pfem doctor` is a dependency-free repository sanity check.

It checks:

- required architecture anchors
- JSON syntax in schemas, fixtures, and adapter samples
- adapter manifest loading
- node profile loading
- obvious neutral-language warnings

From a source checkout, run:

```bat
pfem_doctor.bat
```

or:

```bat
python tools\pfem_doctor.py
```

The doctor is intentionally boring. It should catch drift early without adding package dependencies.
