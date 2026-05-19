"""PFEM command line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pfem.action import format_action_report, validate_action_repository
from pfem.apply_receipt import format_apply_receipt_report, validate_apply_receipts
from pfem.audit import format_audit_report, validate_audit_repository
from pfem.conflict_record import format_conflict_record_report, validate_conflict_records
from pfem.bundle import format_bundle_report, validate_bundle_repository
from pfem.catalog import build_catalog, format_catalog
from pfem.delivery import format_delivery_report, validate_delivery_channel_registry
from pfem.delivery_job import format_delivery_job_report, validate_delivery_jobs
from pfem.dispatch import format_dispatch_report, validate_dispatch_policy
from pfem.dispatch_decision import format_dispatch_decision_report, validate_dispatch_decisions
from pfem.disposition_record import format_disposition_record_report, validate_disposition_records
from pfem.disposition_receipt import format_disposition_receipt_report, validate_disposition_receipts
from pfem.custody_record import format_custody_record_report, validate_custody_records
from pfem.custody_verification_receipt import format_custody_verification_receipt_report, validate_custody_verification_receipts
from pfem.custody_transfer_record import format_custody_transfer_record_report, validate_custody_transfer_records
from pfem.custody_transfer_verification_receipt import format_custody_transfer_verification_receipt_report, validate_custody_transfer_verification_receipts
from pfem.custody_closeout_record import format_custody_closeout_record_report, validate_custody_closeout_records
from pfem.custody_chain_record import format_custody_chain_record_report, validate_custody_chain_records
from pfem.custody_chain_verification_receipt import format_custody_chain_verification_receipt_report, validate_custody_chain_verification_receipts
from pfem.custody_ledger_record import format_custody_ledger_record_report, validate_custody_ledger_records
from pfem.custody_ledger_verification_receipt import format_custody_ledger_verification_receipt_report, validate_custody_ledger_verification_receipts
from pfem.custody_release_request import format_custody_release_request_report, validate_custody_release_requests
from pfem.custody_release_approval import format_custody_release_approval_report, validate_custody_release_approvals
from pfem.custody_release_receipt import format_custody_release_receipt_report, validate_custody_release_receipts
from pfem.custody_release_verification_receipt import format_custody_release_verification_receipt_report, validate_custody_release_verification_receipts
from pfem.custody_release_closeout_record import format_custody_release_closeout_record_report, validate_custody_release_closeout_records
from pfem.custody_release_chain_record import format_custody_release_chain_record_report, validate_custody_release_chain_records
from pfem.custody_release_chain_verification_receipt import format_custody_release_chain_verification_receipt_report, validate_custody_release_chain_verification_receipts
from pfem.custody_lifecycle_record import format_custody_lifecycle_record_report, validate_custody_lifecycle_records
from pfem.custody_lifecycle_verification_receipt import format_custody_lifecycle_verification_receipt_report, validate_custody_lifecycle_verification_receipts
from pfem.custody_lifecycle_closeout_record import format_custody_lifecycle_closeout_record_report, validate_custody_lifecycle_closeout_records
from pfem.archive_manifest_record import format_archive_manifest_record_report, validate_archive_manifest_records
from pfem.archive_receipt import format_archive_receipt_report, validate_archive_receipts
from pfem.archive_verification_receipt import format_archive_verification_receipt_report, validate_archive_verification_receipts
from pfem.archive_closeout_record import format_archive_closeout_record_report, validate_archive_closeout_records
from pfem.archive_chain_record import format_archive_chain_record_report, validate_archive_chain_records
from pfem.archive_chain_verification_receipt import format_archive_chain_verification_receipt_report, validate_archive_chain_verification_receipts
from pfem.archive_index_record import format_archive_index_record_report, validate_archive_index_records
from pfem.archive_index_verification_receipt import format_archive_index_verification_receipt_report, validate_archive_index_verification_receipts
from pfem.archive_index_closeout_record import format_archive_index_closeout_record_report, validate_archive_index_closeout_records
from pfem.archive_lifecycle_record import format_archive_lifecycle_record_report, validate_archive_lifecycle_records
from pfem.archive_lifecycle_verification_receipt import format_archive_lifecycle_verification_receipt_report, validate_archive_lifecycle_verification_receipts
from pfem.archive_lifecycle_closeout_record import format_archive_lifecycle_closeout_record_report, validate_archive_lifecycle_closeout_records
from pfem.preservation_record import format_preservation_record_report, validate_preservation_records
from pfem.preservation_verification_receipt import format_preservation_verification_receipt_report, validate_preservation_verification_receipts
from pfem.doctor import format_report, run_doctor
from pfem.exchange import format_exchange_report, validate_exchange_repository
from pfem.handling import format_handling_report, validate_handling_policy
from pfem.inbox import format_inbox_report, validate_inbox_items
from pfem.import_record import format_import_record_report, validate_import_records
from pfem.merge_decision import format_merge_decision_report, validate_merge_decisions
from pfem.intake_decision import format_intake_decision_report, validate_intake_decisions
from pfem.integrity import format_integrity_report, validate_integrity_manifest, write_integrity_manifest
from pfem.lineage import format_lineage_report, validate_lifecycle_dir
from pfem.outbox import format_outbox_report, validate_outbox_items
from pfem.playbook import format_playbook_report, validate_playbook_repository
from pfem.policy import format_policy_report, validate_policy_repository
from pfem.quality import format_quality_report, validate_quality_repository
from pfem.reconciliation import format_reconciliation_report, validate_reconciliation_repository
from pfem.recovery_point import format_recovery_point_report, validate_recovery_points
from pfem.retention import format_retention_report, validate_retention_policy
from pfem.restore_plan import format_restore_plan_report, validate_restore_plans
from pfem.restore_approval import format_restore_approval_report, validate_restore_approvals
from pfem.restore_receipt import format_restore_receipt_report, validate_restore_receipts
from pfem.restore_verification_receipt import format_restore_verification_receipt_report, validate_restore_verification_receipts
from pfem.restore_closeout_record import format_restore_closeout_record_report, validate_restore_closeout_records
from pfem.review import format_review_report, validate_review_repository
from pfem.rollup import format_rollup_report, validate_rollup_dir
from pfem.routing import format_routing_report, validate_routing_policy
from pfem.schema_contracts import format_schema_contract_report, validate_schema_contracts
from pfem.snapshot_manifest import format_snapshot_manifest_report, validate_snapshot_manifests
from pfem.snapshot_verification_receipt import format_snapshot_verification_receipt_report, validate_snapshot_verification_receipts
from pfem.source_runtime.registry import format_source_provenance_report, validate_source_provenance_repository
from pfem.state_checkpoint import format_state_checkpoint_report, validate_state_checkpoints
from pfem.state_transition import format_state_transition_report, validate_state_transitions
from pfem.topology import format_topology_report, validate_topology_repository
from pfem.transport import format_transport_report, validate_transport_adapter_registry
from pfem.transport_receipt import format_transport_receipt_report, validate_transport_receipts


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pfem", description="PFEM helper commands")
    subparsers = parser.add_subparsers(dest="command")

    for name, help_text in [
        ("doctor", "Run PFEM repository sanity checks"),
        ("catalog", "Print PFEM catalog from disk"),
        ("actions", "Validate PFEM action records"),
        ("playbooks", "Validate PFEM playbooks"),
        ("dispatch", "Validate PFEM dispatch policy"),
        ("dispatch-decisions", "Validate PFEM dispatch decisions"),
        ("outbox", "Validate PFEM outbox items"),
        ("inbox", "Validate PFEM inbox items"),
        ("intake-decisions", "Validate PFEM intake decisions"),
        ("import-records", "Validate PFEM import records"),
        ("apply-receipts", "Validate PFEM apply receipts"),
        ("state-checkpoints", "Validate PFEM state checkpoints"),
        ("state-transitions", "Validate PFEM state transitions"),
        ("snapshot-manifests", "Validate PFEM snapshot manifests"),
        ("snapshot-verification-receipts", "Validate PFEM snapshot verification receipts"),
        ("recovery-points", "Validate PFEM recovery points"),
        ("restore-plans", "Validate PFEM restore plans"),
        ("restore-approvals", "Validate PFEM restore approvals"),
        ("restore-receipts", "Validate PFEM restore receipts"),
        ("restore-verification-receipts", "Validate PFEM restore verification receipts"),
        ("restore-closeout-records", "Validate PFEM restore closeout records"),
        ("disposition-records", "Validate PFEM disposition records"),
        ("disposition-receipts", "Validate PFEM disposition receipts"),
        ("custody-records", "Validate PFEM custody records"),
        ("custody-verification-receipts", "Validate PFEM custody verification receipts"),
        ("custody-transfer-records", "Validate PFEM custody transfer records"),
        ("custody-transfer-verification-receipts", "Validate PFEM custody transfer verification receipts"),
        ("custody-closeout-records", "Validate PFEM custody closeout records"),
        ("custody-chain-records", "Validate PFEM custody chain records"),
        ("custody-chain-verification-receipts", "Validate PFEM custody chain verification receipts"),
        ("custody-ledger-records", "Validate PFEM custody ledger records"),
        ("custody-ledger-verification-receipts", "Validate PFEM custody ledger verification receipts"),
        ("custody-release-requests", "Validate PFEM custody release requests"),
        ("custody-release-approvals", "Validate PFEM custody release approvals"),
        ("custody-release-receipts", "Validate PFEM custody release receipts"),
        ("custody-release-verification-receipts", "Validate PFEM custody release verification receipts"),
        ("custody-release-closeout-records", "Validate PFEM custody release closeout records"),
        ("custody-release-chain-records", "Validate PFEM custody release chain records"),
        ("custody-release-chain-verification-receipts", "Validate PFEM custody release chain verification receipts"),
        ("custody-lifecycle-records", "Validate PFEM custody lifecycle records"),
        ("custody-lifecycle-verification-receipts", "Validate PFEM custody lifecycle verification receipts"),
        ("custody-lifecycle-closeout-records", "Validate PFEM custody lifecycle closeout records"),
        ("archive-manifest-records", "Validate PFEM archive manifest records"),
        ("archive-receipts", "Validate PFEM archive receipts"),
        ("archive-verification-receipts", "Validate PFEM archive verification receipts"),
        ("archive-closeout-records", "Validate PFEM archive closeout records"),
        ("archive-chain-records", "Validate PFEM archive chain records"),
        ("archive-chain-verification-receipts", "Validate PFEM archive chain verification receipts"),
        ("archive-index-records", "Validate PFEM archive index records"),
        ("archive-index-verification-receipts", "Validate PFEM archive index verification receipts"),
        ("archive-index-closeout-records", "Validate PFEM archive index closeout records"),
        ("archive-lifecycle-records", "Validate PFEM archive lifecycle records"),
        ("archive-lifecycle-verification-receipts", "Validate PFEM archive lifecycle verification receipts"),
        ("archive-lifecycle-closeout-records", "Validate PFEM archive lifecycle closeout records"),
        ("preservation-records", "Validate PFEM preservation records"),
        ("preservation-verification-receipts", "Validate PFEM preservation verification receipts"),
        ("conflict-records", "Validate PFEM conflict records"),
        ("merge-decisions", "Validate PFEM merge decisions"),
        ("routing", "Validate PFEM routing policy"),
        ("delivery", "Validate PFEM delivery channel registry"),
        ("delivery-jobs", "Validate PFEM delivery jobs"),
        ("transport", "Validate PFEM transport adapter registry"),
        ("transport-receipts", "Validate PFEM transport receipts"),
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
        print(json.dumps(catalog, indent=2) if args.json else format_catalog(catalog))
        return 0

    command_map = {
        "actions": (validate_action_repository, format_action_report),
        "playbooks": (validate_playbook_repository, format_playbook_report),
        "dispatch": (validate_dispatch_policy, format_dispatch_report),
        "dispatch-decisions": (validate_dispatch_decisions, format_dispatch_decision_report),
        "outbox": (validate_outbox_items, format_outbox_report),
        "inbox": (validate_inbox_items, format_inbox_report),
        "intake-decisions": (validate_intake_decisions, format_intake_decision_report),
        "import-records": (validate_import_records, format_import_record_report),
        "apply-receipts": (validate_apply_receipts, format_apply_receipt_report),
        "state-checkpoints": (validate_state_checkpoints, format_state_checkpoint_report),
        "state-transitions": (validate_state_transitions, format_state_transition_report),
        "snapshot-manifests": (validate_snapshot_manifests, format_snapshot_manifest_report),
        "snapshot-verification-receipts": (validate_snapshot_verification_receipts, format_snapshot_verification_receipt_report),
        "recovery-points": (validate_recovery_points, format_recovery_point_report),
        "restore-plans": (validate_restore_plans, format_restore_plan_report),
        "restore-approvals": (validate_restore_approvals, format_restore_approval_report),
        "restore-receipts": (validate_restore_receipts, format_restore_receipt_report),
        "restore-verification-receipts": (validate_restore_verification_receipts, format_restore_verification_receipt_report),
        "restore-closeout-records": (validate_restore_closeout_records, format_restore_closeout_record_report),
        "disposition-records": (validate_disposition_records, format_disposition_record_report),
        "disposition-receipts": (validate_disposition_receipts, format_disposition_receipt_report),
        "custody-records": (validate_custody_records, format_custody_record_report),
        "custody-verification-receipts": (validate_custody_verification_receipts, format_custody_verification_receipt_report),
        "custody-transfer-records": (validate_custody_transfer_records, format_custody_transfer_record_report),
        "custody-transfer-verification-receipts": (validate_custody_transfer_verification_receipts, format_custody_transfer_verification_receipt_report),
        "custody-closeout-records": (validate_custody_closeout_records, format_custody_closeout_record_report),
        "custody-chain-records": (validate_custody_chain_records, format_custody_chain_record_report),
        "custody-chain-verification-receipts": (validate_custody_chain_verification_receipts, format_custody_chain_verification_receipt_report),
        "custody-ledger-records": (validate_custody_ledger_records, format_custody_ledger_record_report),
        "custody-ledger-verification-receipts": (validate_custody_ledger_verification_receipts, format_custody_ledger_verification_receipt_report),
        "custody-release-requests": (validate_custody_release_requests, format_custody_release_request_report),
        "custody-release-approvals": (validate_custody_release_approvals, format_custody_release_approval_report),
        "custody-release-receipts": (validate_custody_release_receipts, format_custody_release_receipt_report),
        "custody-release-verification-receipts": (validate_custody_release_verification_receipts, format_custody_release_verification_receipt_report),
        "custody-release-closeout-records": (validate_custody_release_closeout_records, format_custody_release_closeout_record_report),
        "custody-release-chain-records": (validate_custody_release_chain_records, format_custody_release_chain_record_report),
        "custody-release-chain-verification-receipts": (validate_custody_release_chain_verification_receipts, format_custody_release_chain_verification_receipt_report),
        "custody-lifecycle-records": (validate_custody_lifecycle_records, format_custody_lifecycle_record_report),
        "custody-lifecycle-verification-receipts": (validate_custody_lifecycle_verification_receipts, format_custody_lifecycle_verification_receipt_report),
        "custody-lifecycle-closeout-records": (validate_custody_lifecycle_closeout_records, format_custody_lifecycle_closeout_record_report),
        "archive-manifest-records": (validate_archive_manifest_records, format_archive_manifest_record_report),
        "archive-receipts": (validate_archive_receipts, format_archive_receipt_report),
        "archive-verification-receipts": (validate_archive_verification_receipts, format_archive_verification_receipt_report),
        "archive-closeout-records": (validate_archive_closeout_records, format_archive_closeout_record_report),
        "archive-chain-records": (validate_archive_chain_records, format_archive_chain_record_report),
        "archive-chain-verification-receipts": (validate_archive_chain_verification_receipts, format_archive_chain_verification_receipt_report),
        "archive-index-records": (validate_archive_index_records, format_archive_index_record_report),
        "archive-index-verification-receipts": (validate_archive_index_verification_receipts, format_archive_index_verification_receipt_report),
        "archive-index-closeout-records": (validate_archive_index_closeout_records, format_archive_index_closeout_record_report),
        "archive-lifecycle-records": (validate_archive_lifecycle_records, format_archive_lifecycle_record_report),
        "archive-lifecycle-verification-receipts": (validate_archive_lifecycle_verification_receipts, format_archive_lifecycle_verification_receipt_report),
        "archive-lifecycle-closeout-records": (validate_archive_lifecycle_closeout_records, format_archive_lifecycle_closeout_record_report),
        "preservation-records": (validate_preservation_records, format_preservation_record_report),
        "preservation-verification-receipts": (validate_preservation_verification_receipts, format_preservation_verification_receipt_report),
        "conflict-records": (validate_conflict_records, format_conflict_record_report),
        "merge-decisions": (validate_merge_decisions, format_merge_decision_report),
        "routing": (validate_routing_policy, format_routing_report),
        "delivery": (validate_delivery_channel_registry, format_delivery_report),
        "delivery-jobs": (validate_delivery_jobs, format_delivery_job_report),
        "transport": (validate_transport_adapter_registry, format_transport_report),
        "transport-receipts": (validate_transport_receipts, format_transport_receipt_report),
        "audit": (validate_audit_repository, format_audit_report),
        "bundles": (validate_bundle_repository, format_bundle_report),
        "exchange": (validate_exchange_repository, format_exchange_report),
        "reconciliation": (validate_reconciliation_repository, format_reconciliation_report),
        "quality": (validate_quality_repository, format_quality_report),
        "handling": (validate_handling_policy, format_handling_report),
        "retention": (validate_retention_policy, format_retention_report),
        "policy": (validate_policy_repository, format_policy_report),
        "review": (validate_review_repository, format_review_report),
        "schema-contracts": (validate_schema_contracts, format_schema_contract_report),
        "topology": (validate_topology_repository, format_topology_report),
        "sources": (validate_source_provenance_repository, format_source_provenance_report),
        "integrity": (validate_integrity_manifest, format_integrity_report),
    }
    if args.command in command_map:
        validator, formatter = command_map[args.command]
        report = validator(Path(args.path))
        print(formatter(report))
        return 0 if report.ok else 1

    if args.command == "lineage":
        report = validate_lifecycle_dir(Path(args.path))
        print(format_lineage_report(report))
        return 0 if report.ok else 1

    if args.command == "rollup":
        report = validate_rollup_dir(Path(args.path))
        print(format_rollup_report(report))
        return 0 if report.ok else 1

    if args.command == "integrity-update":
        path = write_integrity_manifest(Path(args.path))
        print(f"Updated PFEM integrity receipts: {path}")
        return 0

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
