"""Run PFEM exchange bundle validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.bundle import format_bundle_report, validate_bundle_repository  # noqa: E402


def main() -> int:
    report = validate_bundle_repository(ROOT)
    print(format_bundle_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
