"""Run PFEM state transition validation from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.state_transition import format_state_transition_report, validate_state_transitions  # noqa: E402


def main() -> int:
    report = validate_state_transitions(ROOT)
    print(format_state_transition_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
