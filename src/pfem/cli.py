"""PFEM command line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pfem.catalog import build_catalog, format_catalog
from pfem.doctor import format_report, run_doctor
from pfem.lineage import format_lineage_report, validate_lifecycle_dir
from pfem.policy import format_policy_report, validate_policy_repository
from pfem.rollup import format_rollup_report, validate_rollup_dir
from pfem.schema_contracts import format_schema_contract_report, validate_schema_contracts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pfem", description="PFEM helper commands")
    subparsers = parser.add_subparsers(dest="command")

    doctor = subparsers.add_parser("doctor", help="Run PFEM repository sanity checks")
    doctor.add_argument("path", nargs="?", default=".", help="Path inside the PFEM repository.")

    catalog = subparsers.add_parser("catalog", help="Print PFEM catalog from disk")
    catalog.add_argument("path", nargs="?", default=".", help="Path inside the PFEM repository.")
    catalog.add_argument("--json", action="store_true", help="Print catalog as JSON.")

    lineage = subparsers.add_parser("lineage", help="Validate PFEM lifecycle lineage records")
    lineage.add_argument("path", nargs="?", default="tests/fixtures/lifecycle/basic")

    rollup = subparsers.add_parser("rollup", help="Validate PFEM rollup and federation records")
    rollup.add_argument("path", nargs="?", default="tests/fixtures/rollup/basic")

    policy = subparsers.add_parser("policy", help="Validate PFEM sharing policy")
    policy.add_argument("path", nargs="?", default=".", help="Path inside the PFEM repository.")

    schemas = subparsers.add_parser("schema-contracts", help="Validate PFEM fixture records against minimum schemas")
    schemas.add_argument("path", nargs="?", default=".", help="Path inside the PFEM repository.")

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

    if args.command == "rollup":
        report = validate_rollup_dir(Path(args.path))
        print(format_rollup_report(report))
        return 0 if report.ok else 1

    if args.command == "policy":
        report = validate_policy_repository(Path(args.path))
        print(format_policy_report(report))
        return 0 if report.ok else 1

    if args.command == "schema-contracts":
        report = validate_schema_contracts(Path(args.path))
        print(format_schema_contract_report(report))
        return 0 if report.ok else 1

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
