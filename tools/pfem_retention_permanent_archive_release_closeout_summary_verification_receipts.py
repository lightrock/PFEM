"""Run PFEM retention permanent archive release closeout summary verification receipts validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.retention_permanent_archive_release_closeout_summary_verification_receipt import format_retention_permanent_archive_release_closeout_summary_verification_receipt_report, validate_retention_permanent_archive_release_closeout_summary_verification_receipts  # noqa: E402


def main() -> int:
    report = validate_retention_permanent_archive_release_closeout_summary_verification_receipts(ROOT)
    print(format_retention_permanent_archive_release_closeout_summary_verification_receipt_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
