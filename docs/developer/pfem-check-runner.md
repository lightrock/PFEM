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

## Launcher self-check

The Python runner can verify the paired launchers directly:

```bat
pfem_check.bat --check-launchers
```

or:

```sh
sh pfem_check.sh --check-launchers
```

Normal runner modes check the launcher pair before running checks. Use `--skip-launcher-check` only when deliberately testing a broken launcher state.

## Quiet check output and logs

`pfem_check.py` is quiet by default. It shows one progress line per step:

```text
[1/404] Running PFEM catalog ... OK 1.044s
```

Detailed stdout/stderr is written to per-step log files:

```text
build/pfem-check-logs/<timestamp>/
```

Use verbose mode when you want the old firehose in the terminal:

```bat
pfem_check.bat --full --verbose --timings
```

Use `--log-dir` to choose the log location:

```bat
pfem_check.bat --quick --timings --log-dir build/pfem-check-logs/latest
```

On failure, the runner prints the failed step, the log path, and an output tail.
