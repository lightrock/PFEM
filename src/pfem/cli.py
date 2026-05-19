"""PFEM command line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from pfem.doctor import format_report, run_doctor


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pfem", description="PFEM helper commands")
    subparsers = parser.add_subparsers(dest="command")

    doctor = subparsers.add_parser("doctor", help="Run PFEM repository sanity checks")
    doctor.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path inside the PFEM repository. Defaults to current directory.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        report = run_doctor(Path(args.path))
        print(format_report(report))
        return 0 if report.ok else 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
