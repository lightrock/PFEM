"""PFEM smart check runner.

This is the one place that should know how to run PFEM checks.
The root .bat/.sh files are intentionally thin launchers.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from dataclasses import dataclass


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
MANIFEST = ROOT / "tools" / "pfem_check_manifest.json"


@dataclass(frozen=True)
class CheckStep:
    label: str
    args: list[str]


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


def run_steps(steps: list[CheckStep], *, timings: bool) -> int:
    env = _env()
    durations: list[tuple[float, str]] = []
    started = time.perf_counter()

    for index, step in enumerate(steps, start=1):
        print()
        print(f"[{index}/{len(steps)}] {step.label}")
        command = _normalize_args(step.args)
        t0 = time.perf_counter()
        result = subprocess.run(command, cwd=ROOT, env=env)
        elapsed = time.perf_counter() - t0
        durations.append((elapsed, step.label))

        if result.returncode != 0:
            print()
            print(f"PFEM check failed after {elapsed:.3f}s: {step.label}")
            if timings:
                print_timings(durations)
            return result.returncode

    total = time.perf_counter() - started
    print()
    print(f"PFEM checks passed in {total:.3f}s.")

    if timings:
        print_timings(durations)

    return 0


def print_timings(durations: list[tuple[float, str]]) -> None:
    print()
    print("Slowest PFEM checks:")
    for elapsed, label in sorted(durations, reverse=True)[:15]:
        print(f"  {elapsed:8.3f}s  {label}")


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

    args = parser.parse_args(argv)

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

    return run_steps(steps, timings=args.timings)


if __name__ == "__main__":
    raise SystemExit(main())
