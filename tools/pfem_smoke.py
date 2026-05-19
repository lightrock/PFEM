"""PFEM smoke check.

Runs dependency-free checks that are safe for a fresh clone.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def check_json_files() -> list[str]:
    failures: list[str] = []
    for base in [ROOT / "schemas", ROOT / "tests" / "fixtures", ROOT / "adapters"]:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.json")):
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{path.relative_to(ROOT)}: {exc}")
    return failures


def check_expected_paths() -> list[str]:
    expected = [
        "README.md",
        "AGENTS.md",
        "docs/AI_START_HERE.md",
        "docs/architecture/architecture-stack.md",
        "ai/review-checklist.md",
        "contracts/adapter-contract.md",
        "schemas/adapter_manifest.schema.json",
        "src/pfem/__init__.py",
    ]
    return [path for path in expected if not (ROOT / path).exists()]


def main() -> int:
    failures: list[str] = []

    failures.extend(check_json_files())
    missing = check_expected_paths()
    failures.extend([f"missing expected path: {path}" for path in missing])

    if failures:
        print("PFEM smoke check failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("PFEM smoke check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
