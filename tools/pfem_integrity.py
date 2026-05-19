"""Run PFEM integrity receipt validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.integrity import format_integrity_report, validate_integrity_manifest  # noqa: E402


def main() -> int:
    report = validate_integrity_manifest(ROOT)
    print(format_integrity_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
