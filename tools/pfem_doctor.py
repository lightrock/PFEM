"""Run PFEM doctor from a source checkout."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pfem.doctor import format_report, run_doctor  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run PFEM repository doctor.")
    parser.add_argument(
        "root",
        nargs="?",
        default=str(ROOT),
        help="PFEM repository root. Defaults to this checkout.",
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        help=(
            "Run doctor plus the historical nested validator pass. "
            "This is intentionally slow; normal pfem_check --full already runs validators separately."
        ),
    )

    args = parser.parse_args(argv)
    report = run_doctor(args.root, deep_validators=args.deep)
    print(format_report(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
