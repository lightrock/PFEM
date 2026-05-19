"""Run PFEM custody release chain records validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.custody_release_chain_record import format_custody_release_chain_record_report, validate_custody_release_chain_records  # noqa: E402


def main() -> int:
    report = validate_custody_release_chain_records(ROOT)
    print(format_custody_release_chain_record_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
