"""Validate that PFEM JSON files parse.

This is intentionally dependency-free. It checks JSON syntax only.
Schema semantic validation can be added later with a JSON Schema library.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CHECK_DIRS = [
    ROOT / "schemas",
    ROOT / "tests" / "fixtures",
    ROOT / "adapters",
]


def iter_json_files() -> list[Path]:
    files: list[Path] = []
    for directory in CHECK_DIRS:
        if directory.exists():
            files.extend(sorted(directory.rglob("*.json")))
    return files


def main() -> int:
    failures: list[str] = []
    for path in iter_json_files():
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - validation tool should report all parse failures
            failures.append(f"{path.relative_to(ROOT)}: {exc}")

    if failures:
        print("JSON validation failed:")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print(f"Validated {len(iter_json_files())} JSON files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
