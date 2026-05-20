"""Run PFEM contributor command protocol audit from a source checkout."""

from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.contributor_command_protocol_audit import (  # noqa: E402
    audit_contributor_command_protocol,
    format_contributor_command_protocol_audit_report,
)


def main() -> int:
    report = audit_contributor_command_protocol(ROOT)
    print(format_contributor_command_protocol_audit_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
