"""PFEM command line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pfem.catalog import build_catalog, format_catalog
from pfem.doctor import format_report, run_doctor
from pfem.lineage import format_lineage_report, validate_lifecycle_dir


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

    catalog = subparsers.add_parser("catalog", help="Print PFEM catalog from disk")
    catalog.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path inside the PFEM repository. Defaults to current directory.",
    )
    catalog.add_argument(
        "--json",
        action="store_true",
        help="Print catalog as JSON.",
    )

    lineage = subparsers.add_parser("lineage", help="Validate PFEM lifecycle lineage records")
    lineage.add_argument(
        "path",
        nargs="?",
        default="tests/fixtures/lifecycle/basic",
        help="Lifecycle fixture directory. Defaults to tests/fixtures/lifecycle/basic.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "doctor":
        report = run_doctor(Path(args.path))
        print(format_report(report))
        return 0 if report.ok else 1

    if args.command == "catalog":
        catalog = build_catalog(Path(args.path))
        if args.json:
            print(json.dumps(catalog, indent=2))
        else:
            print(format_catalog(catalog))
        return 0

    if args.command == "lineage":
        report = validate_lifecycle_dir(Path(args.path))
        print(format_lineage_report(report))
        return 0 if report.ok else 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
