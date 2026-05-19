"""Run PFEM intake decision validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.intake_decision import format_intake_decision_report, validate_intake_decisions  # noqa: E402


def main() -> int:
    report = validate_intake_decisions(ROOT)
    print(format_intake_decision_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
