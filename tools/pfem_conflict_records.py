"""Run PFEM conflict record validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.conflict_record import format_conflict_record_report, validate_conflict_records  # noqa: E402


def main() -> int:
    report = validate_conflict_records(ROOT)
    print(format_conflict_record_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
