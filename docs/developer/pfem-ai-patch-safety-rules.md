# PFEM AI Patch Safety Rules

This file exists because PFEM patch scripts must be safe for humans and future AI assistants to run from a normal checkout.

PFEM patches often arrive as temporary folders outside the repository. The operator usually runs a wrapper from the PFEM repo root, for example:

```bat
E:\DRONES\SKYWRONG_PROJECTS\PFEM\PFEM>E:\DRONES\temp\SOME_PATCH\apply_patch.bat
```

The patch wrapper must preserve that caller working directory as the repository root unless the operator explicitly passes another root.

## Required patch-wrapper behavior

Patch wrappers must:

```text
capture %CD% before changing directories
pass that captured repo root explicitly into Python
validate PFEM root by checking multiple PFEM markers
print the repo root being patched
write noisy status output to build/pfem-patch-status/
run only smoke checks whose target files/modules exist
report optional smoke-check skips clearly instead of failing the patch
```

Patch wrappers must not:

```text
cd /d "%~dp0" and then treat the patch folder as the repo root
assume the patch folder is inside the repository
run optional unittest modules before verifying the test file exists
claim the operator is in the wrong directory when the wrapper moved directories itself
silently rewrite broad generated files without a backup/report path
hide failed smoke commands
```

## Safe BAT wrapper pattern

Use this shape for Windows wrappers:

```bat
@echo off
setlocal
set "PFEM_REPO_ROOT=%CD%"
set "PATCH_DIR=%~dp0"

if not exist "%PFEM_REPO_ROOT%\AGENTS.md" goto :bad_root
if not exist "%PFEM_REPO_ROOT%\README.md" goto :bad_root
if not exist "%PFEM_REPO_ROOT%\tools\pfem_check_manifest.json" goto :bad_root

python "%PATCH_DIR%apply_patch.py" "%PFEM_REPO_ROOT%"
exit /b %ERRORLEVEL%

:bad_root
echo This does not look like the PFEM repo root: %PFEM_REPO_ROOT%
echo Run the wrapper from the PFEM checkout root.
exit /b 2
```

Do not use this unsafe shape:

```bat
cd /d "%~dp0"
python apply_patch.py
```

That changes the working directory to the patch folder and can make a correct operator command fail falsely.

## Safe Python patch pattern

Patch Python should accept the repo root as an argument:

```python
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
required = [
    root / "AGENTS.md",
    root / "README.md",
    root / "tools" / "pfem_check_manifest.json",
]
missing = [str(path) for path in required if not path.exists()]
if missing:
    raise SystemExit("PFEM repo-root check failed; missing: " + ", ".join(missing))
```

Optional smoke checks should be conditional:

```python
test_path = root / "tests" / "unit" / "test_boundary_language_standards_audit.py"
if test_path.exists():
    run([sys.executable, "-m", "unittest", "tests.unit.test_boundary_language_standards_audit"], cwd=root)
else:
    print(f"Skipping optional smoke check; missing {test_path.relative_to(root)}")
```

## AI assistant checklist before delivering a PFEM patch

Before handing a PFEM patch to the user, the assistant must check:

```text
1. Did I read AGENTS.md and the current PFEM handoff docs?
2. Does the wrapper preserve the caller repo root?
3. Does Python receive the repo root explicitly?
4. Does the patch validate PFEM root with AGENTS.md, README.md, and tools/pfem_check_manifest.json?
5. Are optional smoke checks conditional on file/module existence?
6. Are backups/reports written under build/ rather than dumped into the terminal?
7. Did I avoid broad blind replacements where PFEM doctrine requires judgment?
8. Did I say exactly what the patch changes and what it does not change?
```

If any answer is no, do not ship the patch yet.

## Why this rule exists

A previous hotfix wrapper changed into the patch directory, then falsely rejected a correct PFEM checkout as the wrong root. This file makes that failure mode explicit so future humans, Codex sessions, and ChatGPT sessions do not repeat it.
