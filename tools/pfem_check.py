"""PFEM smart check runner.

This is the one place that should know how to run PFEM checks.
The root .bat/.sh files are intentionally thin launchers.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
MANIFEST = ROOT / "tools" / "pfem_check_manifest.json"
LOG_ROOT = ROOT / "build" / "pfem-check-logs"
LAUNCHER_VERSION = "1"


@dataclass(frozen=True)
class CheckStep:
    label: str
    args: list[str]


@dataclass(frozen=True)
class StepResult:
    label: str
    elapsed: float
    returncode: int
    log_path: Path


def check_launchers(*, quiet: bool = False) -> int:
    """Verify pfem_check.bat and pfem_check.sh stay paired."""

    launcher_paths = [
        ROOT / "pfem_check.bat",
        ROOT / "pfem_check.sh",
    ]
    failures: list[str] = []
    versions: dict[str, str] = {}

    for path in launcher_paths:
        if not path.exists():
            failures.append(f"missing launcher: {path.name}")
            continue

        text = path.read_text(encoding="utf-8")
        match = re.search(r"PFEM_CHECK_LAUNCHER_VERSION=([0-9]+)", text)
        if not match:
            failures.append(f"{path.name} missing PFEM_CHECK_LAUNCHER_VERSION marker")
        else:
            versions[path.name] = match.group(1)

        if "tools/pfem_check.py" not in text.replace("\\", "/"):
            failures.append(f"{path.name} does not call tools/pfem_check.py")

    if versions and any(version != LAUNCHER_VERSION for version in versions.values()):
        failures.append(
            "launcher version does not match tools/pfem_check.py "
            f"LAUNCHER_VERSION={LAUNCHER_VERSION}: {versions}"
        )

    if len(set(versions.values())) > 1:
        failures.append(f"launcher versions differ: {versions}")

    if failures:
        print("PFEM launcher check failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    if not quiet:
        print(f"PFEM launcher check passed. Version: {LAUNCHER_VERSION}")

    return 0


def _env() -> dict[str, str]:
    env = os.environ.copy()
    old = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(SRC) if not old else str(SRC) + os.pathsep + old
    return env


def _load_manifest() -> list[CheckStep]:
    if not MANIFEST.exists():
        raise SystemExit(f"missing PFEM check manifest: {MANIFEST}")

    raw = json.loads(MANIFEST.read_text(encoding="utf-8"))
    steps: list[CheckStep] = []

    for item in raw.get("steps", []):
        label = str(item.get("label", "")).strip() or "PFEM check"
        args = [str(part) for part in item.get("args", [])]
        if args:
            steps.append(CheckStep(label=label, args=args))

    if not steps:
        raise SystemExit(f"PFEM check manifest has no runnable steps: {MANIFEST}")

    return steps


def _default_unit_step() -> CheckStep:
    return CheckStep(
        label="PFEM unit tests",
        args=["-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
    )


def _normalize_args(args: list[str]) -> list[str]:
    if not args:
        raise ValueError("empty command args")

    first = args[0].replace("\\", "/")

    if first.startswith("tools/") and first.endswith(".py"):
        return [sys.executable, str(ROOT / first), *args[1:]]

    return [sys.executable, *args]


def _step_key(step: CheckStep) -> str:
    if step.args and step.args[0].replace("\\", "/").startswith("tools/"):
        return Path(step.args[0].replace("\\", "/")).name
    return " ".join(step.args)


def _select_steps(steps: list[CheckStep], mode: str) -> list[CheckStep]:
    if mode == "full":
        return steps

    if mode == "unit":
        selected = [s for s in steps if "-m" in s.args and "unittest" in s.args]
        return selected or [_default_unit_step()]

    if mode == "doctor":
        return [s for s in steps if _step_key(s) == "pfem_doctor.py"]

    if mode == "validators":
        return [s for s in steps if _step_key(s).startswith("pfem_") and _step_key(s).endswith(".py")]

    if mode == "quick":
        wanted = {
            "pfem_catalog.py",
            "pfem_audit.py",
            "pfem_schema_contracts.py",
            "pfem_integrity.py",
            "pfem_doctor.py",
            "pfem_smoke.py",
        }
        selected = [s for s in steps if _step_key(s) in wanted]
        if selected:
            return selected
        return [s for s in steps if _step_key(s) in {"pfem_catalog.py", "pfem_doctor.py"}]

    raise ValueError(f"unknown mode: {mode}")


def _apply_start_at(steps: list[CheckStep], needle: str | None) -> list[CheckStep]:
    if not needle:
        return steps

    n = needle.lower()
    for i, step in enumerate(steps):
        hay = (step.label + " " + " ".join(step.args)).lower()
        if n in hay:
            return steps[i:]

    raise SystemExit(f"--start-at did not match any step: {needle!r}")


def _slug(text: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", text.strip().lower()).strip("-")
    return value[:90] or "pfem-check"


def _prepare_log_dir(path: str | None) -> Path:
    if path:
        log_dir = Path(path)
        if not log_dir.is_absolute():
            log_dir = ROOT / log_dir
    else:
        log_dir = LOG_ROOT / time.strftime("%Y%m%d-%H%M%S")

    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def _write_log(
    *,
    log_path: Path,
    step: CheckStep,
    command: list[str],
    returncode: int,
    elapsed: float,
    stdout: str,
    stderr: str,
) -> None:
    log_path.write_text(
        "\n".join(
            [
                f"label: {step.label}",
                f"command: {' '.join(command)}",
                f"returncode: {returncode}",
                f"elapsed_seconds: {elapsed:.3f}",
                "",
                "--- stdout ---",
                stdout.rstrip(),
                "",
                "--- stderr ---",
                stderr.rstrip(),
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _tail(text: str, *, lines: int = 200) -> str:
    split = text.splitlines()
    if len(split) <= lines:
        return text.rstrip()
    return "\n".join(["... output truncated ...", *split[-lines:]]).rstrip()


def run_steps(steps: list[CheckStep], *, timings: bool, verbose: bool, log_dir: Path) -> int:
    env = _env()
    results: list[StepResult] = []
    started = time.perf_counter()

    print(f"PFEM check logs: {log_dir}")

    for index, step in enumerate(steps, start=1):
        command = _normalize_args(step.args)
        log_path = log_dir / f"{index:03d}-{_slug(step.label)}.log"

        print(f"[{index}/{len(steps)}] {step.label} ... ", end="", flush=True)
        t0 = time.perf_counter()
        completed = subprocess.run(
            command,
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
        )
        elapsed = time.perf_counter() - t0

        _write_log(
            log_path=log_path,
            step=step,
            command=command,
            returncode=completed.returncode,
            elapsed=elapsed,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

        results.append(
            StepResult(
                label=step.label,
                elapsed=elapsed,
                returncode=completed.returncode,
                log_path=log_path,
            )
        )

        if completed.returncode != 0:
            print(f"FAILED {elapsed:.3f}s")
            print()
            print(f"PFEM check failed: {step.label}")
            print(f"Log: {log_path}")

            output = "\n".join(part for part in [completed.stdout, completed.stderr] if part)
            if output.strip():
                print()
                print("--- output tail ---")
                print(_tail(output))

            if timings:
                print_timings(results)
            return completed.returncode

        print(f"OK {elapsed:.3f}s")

        if verbose:
            if completed.stdout.strip():
                print()
                print(completed.stdout.rstrip())
            if completed.stderr.strip():
                print()
                print(completed.stderr.rstrip(), file=sys.stderr)

    total = time.perf_counter() - started
    print()
    print(f"PFEM checks passed in {total:.3f}s.")
    print(f"Logs: {log_dir}")

    if timings:
        print_timings(results)

    return 0


def print_timings(results: list[StepResult]) -> None:
    print()
    print("Slowest PFEM checks:")
    for result in sorted(results, key=lambda item: item.elapsed, reverse=True)[:15]:
        print(f"  {result.elapsed:8.3f}s  {result.label}")
        print(f"             log: {result.log_path}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run PFEM checks from one Python runner.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--full", action="store_true", help="Run every check in tools/pfem_check_manifest.json.")
    mode.add_argument("--quick", action="store_true", help="Run the high-value fast checks.")
    mode.add_argument("--validators", action="store_true", help="Run Python tool validators from the manifest.")
    mode.add_argument("--doctor", action="store_true", help="Run only PFEM doctor.")
    mode.add_argument("--unit", action="store_true", help="Run only unit tests.")
    parser.add_argument("--list", action="store_true", help="List selected checks instead of running them.")
    parser.add_argument("--start-at", help="Start at the first selected step whose label/command contains this text.")
    parser.add_argument("--timings", action="store_true", help="Print slowest checks at the end.")
    parser.add_argument("--verbose", action="store_true", help="Echo each check's stdout/stderr to the terminal.")
    parser.add_argument("--log-dir", help="Directory for per-step logs. Defaults to build/pfem-check-logs/<timestamp>.")
    parser.add_argument("--check-launchers", action="store_true", help="Verify pfem_check.bat and pfem_check.sh stay paired, then exit.")
    parser.add_argument("--skip-launcher-check", action="store_true", help="Skip launcher pair validation before running checks.")

    args = parser.parse_args(argv)

    if args.check_launchers:
        return check_launchers()

    if not args.skip_launcher_check:
        launcher_result = check_launchers(quiet=True)
        if launcher_result != 0:
            return launcher_result

    selected_mode = "full"
    if args.quick:
        selected_mode = "quick"
    elif args.validators:
        selected_mode = "validators"
    elif args.doctor:
        selected_mode = "doctor"
    elif args.unit:
        selected_mode = "unit"

    steps = _select_steps(_load_manifest(), selected_mode)
    steps = _apply_start_at(steps, args.start_at)

    if args.list:
        for index, step in enumerate(steps, start=1):
            print(f"{index:4d}. {step.label} :: python {' '.join(step.args)}")
        return 0

    return run_steps(
        steps,
        timings=args.timings,
        verbose=args.verbose,
        log_dir=_prepare_log_dir(args.log_dir),
    )


if __name__ == "__main__":
    raise SystemExit(main())
