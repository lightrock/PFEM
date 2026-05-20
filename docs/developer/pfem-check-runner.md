# PFEM Check Runner

PFEM uses one real check runner:

```text
tools/pfem_check.py
```

The repository root keeps only thin launchers:

```text
pfem_check.bat
pfem_check.sh
run_tests.bat
```

Do not add new root `pfem_*.bat` validator wrappers. Put check logic in Python and register checks through:

```text
tools/pfem_check_manifest.json
```

## Common commands

Windows:

```bat
pfem_check.bat --quick --timings
pfem_check.bat --doctor
pfem_check.bat --unit --timings
pfem_check.bat --full --timings
```

Linux/macOS:

```sh
sh pfem_check.sh --quick --timings
sh pfem_check.sh --doctor
sh pfem_check.sh --unit --timings
sh pfem_check.sh --full --timings
```

## Launcher binding rule

`pfem_check.bat` and `pfem_check.sh` both carry:

```text
PFEM_CHECK_LAUNCHER_VERSION=1
```

If one launcher changes, update the other launcher and keep the launcher-pair test passing.

## Why this exists

PFEM used to generate many root BAT files. That made the root directory noisy and caused constant launcher churn. The root launchers are now dumb wrappers; `tools/pfem_check.py` owns the test/check behavior.
