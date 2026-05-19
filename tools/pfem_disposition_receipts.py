"""Run PFEM disposition receipt validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.disposition_receipt import format_disposition_receipt_report, validate_disposition_receipts  # noqa: E402


def main() -> int:
    report = validate_disposition_receipts(ROOT)
    print(format_disposition_receipt_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
