"""Run PFEM restore closeout record validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.restore_closeout_record import (  # noqa: E402
    format_restore_closeout_record_report,
    validate_restore_closeout_records,
)


def main() -> int:
    report = validate_restore_closeout_records(ROOT)
    print(format_restore_closeout_record_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
