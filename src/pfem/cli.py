"""PFEM command line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pfem.action import format_action_report, validate_action_repository
from pfem.audit import format_audit_report, validate_audit_repository
from pfem.bundle import format_bundle_report, validate_bundle_repository
from pfem.catalog import build_catalog, format_catalog
from pfem.doctor import format_report, run_doctor
from pfem.exchange import format_exchange_report, validate_exchange_repository
from pfem.handling import format_handling_report, validate_handling_policy
from pfem.integrity import format_integrity_report, validate_integrity_manifest, write_integrity_manifest
from pfem.lineage import format_lineage_report, validate_lifecycle_dir
from pfem.playbook import format_playbook_report, validate_playbook_repository
from pfem.policy import format_policy_report, validate_policy_repository
from pfem.quality import format_quality_report, validate_quality_repository
from pfem.reconciliation import format_reconciliation_report, validate_reconciliation_repository
from pfem.retention import format_retention_report, validate_retention_policy
from pfem.review import format_review_report, validate_review_repository
from pfem.rollup import format_rollup_report, validate_rollup_dir
from pfem.routing import format_routing_report, validate_routing_policy
from pfem.schema_contracts import format_schema_contract_report, validate_schema_contracts
from pfem.source_runtime.registry import format_source_provenance_report, validate_source_provenance_repository
from pfem.topology import format_topology_report, validate_topology_repository


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pfem", description="PFEM helper commands")
    subparsers = parser.add_subparsers(dest="command")

    for name, help_text in [
        ("doctor", "Run PFEM repository sanity checks"),
        ("catalog", "Print PFEM catalog from disk"),
        ("actions", "Validate PFEM action records"),
        ("playbooks", "Validate PFEM playbooks"),
        ("routing", "Validate PFEM routing policy"),
        ("audit", "Validate PFEM audit journal"),
        ("bundles", "Validate PFEM exchange bundles"),
        ("exchange", "Validate PFEM exchange receipts"),
        ("reconciliation", "Validate PFEM reconciliation records"),
        ("quality", "Validate PFEM confidence/quality records"),
        ("handling", "Validate PFEM handling/redaction policy"),
        ("retention", "Validate PFEM retention/disposition policy"),
        ("policy", "Validate PFEM sharing policy"),
        ("review", "Validate PFEM review records"),
        ("schema-contracts", "Validate PFEM fixture records against minimum schemas"),
        ("topology", "Validate PFEM federation topology"),
        ("sources", "Validate PFEM source provenance"),
        ("integrity", "Validate PFEM integrity receipts"),
        ("integrity-update", "Update PFEM integrity receipts"),
    ]:
        sub = subparsers.add_parser(name, help=help_text)
        sub.add_argument("path", nargs="?", default=".", help="Path inside the PFEM repository.")
        if name == "catalog":
            sub.add_argument("--json", action="store_true", help="Print catalog as JSON.")

    lineage = subparsers.add_parser("lineage", help="Validate PFEM lifecycle lineage records")
    lineage.add_argument("path", nargs="?", default="tests/fixtures/lifecycle/basic")

    rollup = subparsers.add_parser("rollup", help="Validate PFEM rollup and federation records")
    rollup.add_argument("path", nargs="?", default="tests/fixtures/rollup/basic")

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

    if args.command == "actions":
        report = validate_action_repository(Path(args.path))
        print(format_action_report(report))
        return 0 if report.ok else 1

    if args.command == "playbooks":
        report = validate_playbook_repository(Path(args.path))
        print(format_playbook_report(report))
        return 0 if report.ok else 1

    if args.command == "routing":
        report = validate_routing_policy(Path(args.path))
        print(format_routing_report(report))
        return 0 if report.ok else 1

    if args.command == "audit":
        report = validate_audit_repository(Path(args.path))
        print(format_audit_report(report))
        return 0 if report.ok else 1

    if args.command == "bundles":
        report = validate_bundle_repository(Path(args.path))
        print(format_bundle_report(report))
        return 0 if report.ok else 1

    if args.command == "exchange":
        report = validate_exchange_repository(Path(args.path))
        print(format_exchange_report(report))
        return 0 if report.ok else 1

    if args.command == "reconciliation":
        report = validate_reconciliation_repository(Path(args.path))
        print(format_reconciliation_report(report))
        return 0 if report.ok else 1

    if args.command == "quality":
        report = validate_quality_repository(Path(args.path))
        print(format_quality_report(report))
        return 0 if report.ok else 1

    if args.command == "handling":
        report = validate_handling_policy(Path(args.path))
        print(format_handling_report(report))
        return 0 if report.ok else 1

    if args.command == "retention":
        report = validate_retention_policy(Path(args.path))
        print(format_retention_report(report))
        return 0 if report.ok else 1

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

    if args.command == "review":
        report = validate_review_repository(Path(args.path))
        print(format_review_report(report))
        return 0 if report.ok else 1

    if args.command == "schema-contracts":
        report = validate_schema_contracts(Path(args.path))
        print(format_schema_contract_report(report))
        return 0 if report.ok else 1

    if args.command == "topology":
        report = validate_topology_repository(Path(args.path))
        print(format_topology_report(report))
        return 0 if report.ok else 1

    if args.command == "sources":
        report = validate_source_provenance_repository(Path(args.path))
        print(format_source_provenance_report(report))
        return 0 if report.ok else 1

    if args.command == "integrity":
        report = validate_integrity_manifest(Path(args.path))
        print(format_integrity_report(report))
        return 0 if report.ok else 1

    if args.command == "integrity-update":
        path = write_integrity_manifest(Path(args.path))
        print(f"Updated PFEM integrity receipts: {path}")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
