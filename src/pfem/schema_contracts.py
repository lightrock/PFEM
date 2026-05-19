"""Lightweight PFEM schema contract checks."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


JsonObject = dict[str, Any]


SCHEMA_TO_FIXTURE_FILES = {
    "finding.schema.json": ["tests/fixtures/**/finding.json"],
    "alert.schema.json": ["tests/fixtures/**/alert.json"],
    "evidence_package.schema.json": ["tests/fixtures/**/evidence_package.json"],
    "rollup_summary.schema.json": ["tests/fixtures/**/rollup_summary.json"],
    "federation_message.schema.json": ["tests/fixtures/**/federation_message.json"],
    "review_record.schema.json": ["review/review-records.json"],
    "audit_event.schema.json": ["audit/audit-journal.json"],
    "handling_policy.schema.json": ["handling/handling-policy.json"],
    "retention_policy.schema.json": ["retention/retention-policy.json"],
    "dispatch_policy.schema.json": ["dispatch/dispatch-policy.json"],
    "dispatch_decision.schema.json": ["dispatch/dispatch-decisions.json"],
    "outbox_item.schema.json": ["outbox/outbox-items.json"],
    "inbox_item.schema.json": ["inbox/inbox-items.json"],
    "intake_decision.schema.json": ["intake/intake-decisions.json"],
    "import_record.schema.json": ["imports/import-records.json"],
    "conflict_record.schema.json": ["conflicts/conflict-records.json"],
    "apply_receipt.schema.json": ["apply/apply-receipts.json"],
    "state_checkpoint.schema.json": ["state/state-checkpoints.json"],
    "state_transition.schema.json": ["state/state-transitions.json"],
    "snapshot_manifest.schema.json": ["snapshots/snapshot-manifests.json"],
    "snapshot_verification_receipt.schema.json": ["snapshots/snapshot-verification-receipts.json"],
    "recovery_point.schema.json": ["recovery/recovery-points.json"],
    "restore_plan.schema.json": ["restore/restore-plans.json"],
    "restore_approval.schema.json": ["restore/restore-approvals.json"],
    "restore_receipt.schema.json": ["restore/restore-receipts.json"],
    "restore_verification_receipt.schema.json": ["restore/restore-verification-receipts.json"],
    "restore_closeout_record.schema.json": ["restore/restore-closeout-records.json"],
    "disposition_record.schema.json": ["disposition/disposition-records.json"],
    "disposition_receipt.schema.json": ["disposition/disposition-receipts.json"],
    "custody_record.schema.json": ["custody/custody-records.json"],
    "custody_verification_receipt.schema.json": ["custody/custody-verification-receipts.json"],
    "custody_transfer_record.schema.json": ["custody/custody-transfer-records.json"],
    "custody_transfer_verification_receipt.schema.json": ["custody/custody-transfer-verification-receipts.json"],
    "custody_closeout_record.schema.json": ["custody/custody-closeout-records.json"],
    "custody_chain_record.schema.json": ["custody/custody-chain-records.json"],
    "custody_chain_verification_receipt.schema.json": ["custody/custody-chain-verification-receipts.json"],
    "custody_ledger_record.schema.json": ["custody/custody-ledger-records.json"],
    "custody_ledger_verification_receipt.schema.json": ["custody/custody-ledger-verification-receipts.json"],
    "custody_release_request.schema.json": ["custody/custody-release-requests.json"],
    "custody_release_approval.schema.json": ["custody/custody-release-approvals.json"],
    "custody_release_receipt.schema.json": ["custody/custody-release-receipts.json"],
    "custody_release_verification_receipt.schema.json": ["custody/custody-release-verification-receipts.json"],
    "custody_release_closeout_record.schema.json": ["custody/custody-release-closeout-records.json"],
    "custody_release_chain_record.schema.json": ["custody/custody-release-chain-records.json"],
    "custody_release_chain_verification_receipt.schema.json": ["custody/custody-release-chain-verification-receipts.json"],
    "custody_lifecycle_record.schema.json": ["custody/custody-lifecycle-records.json"],
    "custody_lifecycle_verification_receipt.schema.json": ["custody/custody-lifecycle-verification-receipts.json"],
    "custody_lifecycle_closeout_record.schema.json": ["custody/custody-lifecycle-closeout-records.json"],
    "archive_manifest_record.schema.json": ["archive/archive-manifest-records.json"],
    "archive_receipt.schema.json": ["archive/archive-receipts.json"],
    "archive_verification_receipt.schema.json": ["archive/archive-verification-receipts.json"],
    "archive_closeout_record.schema.json": ["archive/archive-closeout-records.json"],
    "archive_chain_record.schema.json": ["archive/archive-chain-records.json"],
    "archive_chain_verification_receipt.schema.json": ["archive/archive-chain-verification-receipts.json"],
    "archive_index_record.schema.json": ["archive/archive-index-records.json"],
    "archive_index_verification_receipt.schema.json": ["archive/archive-index-verification-receipts.json"],
    "archive_index_closeout_record.schema.json": ["archive/archive-index-closeout-records.json"],
    "archive_lifecycle_record.schema.json": ["archive/archive-lifecycle-records.json"],
    "archive_lifecycle_verification_receipt.schema.json": ["archive/archive-lifecycle-verification-receipts.json"],
    "archive_lifecycle_closeout_record.schema.json": ["archive/archive-lifecycle-closeout-records.json"],
    "preservation_record.schema.json": ["preservation/preservation-records.json"],
    "preservation_verification_receipt.schema.json": ["preservation/preservation-verification-receipts.json"],
    "preservation_closeout_record.schema.json": ["preservation/preservation-closeout-records.json"],
    "preservation_chain_record.schema.json": ["preservation/preservation-chain-records.json"],
    "preservation_chain_verification_receipt.schema.json": ["preservation/preservation-chain-verification-receipts.json"],
    "retention_review_record.schema.json": ["retention/retention-review-records.json"],
    "retention_review_verification_receipt.schema.json": ["retention/retention-review-verification-receipts.json"],
    "retention_decision_record.schema.json": ["retention/retention-decision-records.json"],
    "retention_decision_approval.schema.json": ["retention/retention-decision-approvals.json"],
    "retention_action_receipt.schema.json": ["retention/retention-action-receipts.json"],
    "retention_action_verification_receipt.schema.json": ["retention/retention-action-verification-receipts.json"],
    "retention_action_closeout_record.schema.json": ["retention/retention-action-closeout-records.json"],
    "retention_chain_record.schema.json": ["retention/retention-chain-records.json"],
    "retention_chain_verification_receipt.schema.json": ["retention/retention-chain-verification-receipts.json"],
    "retention_lifecycle_record.schema.json": ["retention/retention-lifecycle-records.json"],
    "retention_lifecycle_verification_receipt.schema.json": ["retention/retention-lifecycle-verification-receipts.json"],
    "retention_lifecycle_closeout_record.schema.json": ["retention/retention-lifecycle-closeout-records.json"],
    "retention_ledger_record.schema.json": ["retention/retention-ledger-records.json"],
    "retention_ledger_verification_receipt.schema.json": ["retention/retention-ledger-verification-receipts.json"],
    "retention_ledger_closeout_record.schema.json": ["retention/retention-ledger-closeout-records.json"],
    "retention_policy_compliance_record.schema.json": ["retention/retention-policy-compliance-records.json"],
    "retention_policy_compliance_verification_receipt.schema.json": ["retention/retention-policy-compliance-verification-receipts.json"],
    "retention_obligation_record.schema.json": ["retention/retention-obligation-records.json"],
    "retention_obligation_verification_receipt.schema.json": ["retention/retention-obligation-verification-receipts.json"],
    "retention_schedule_record.schema.json": ["retention/retention-schedule-records.json"],
    "retention_schedule_verification_receipt.schema.json": ["retention/retention-schedule-verification-receipts.json"],
    "retention_schedule_closeout_record.schema.json": ["retention/retention-schedule-closeout-records.json"],
    "retention_cycle_record.schema.json": ["retention/retention-cycle-records.json"],
    "retention_cycle_verification_receipt.schema.json": ["retention/retention-cycle-verification-receipts.json"],
    "retention_cycle_closeout_record.schema.json": ["retention/retention-cycle-closeout-records.json"],
    "retention_hold_record.schema.json": ["retention/retention-hold-records.json"],
    "retention_hold_verification_receipt.schema.json": ["retention/retention-hold-verification-receipts.json"],
    "retention_hold_closeout_record.schema.json": ["retention/retention-hold-closeout-records.json"],
    "retention_status_snapshot_record.schema.json": ["retention/retention-status-snapshot-records.json"],
    "retention_status_snapshot_verification_receipt.schema.json": ["retention/retention-status-snapshot-verification-receipts.json"],
    "retention_rollup_record.schema.json": ["retention/retention-rollup-records.json"],
    "retention_rollup_verification_receipt.schema.json": ["retention/retention-rollup-verification-receipts.json"],
    "retention_rollup_closeout_record.schema.json": ["retention/retention-rollup-closeout-records.json"],
    "retention_report_record.schema.json": ["retention/retention-report-records.json"],
    "retention_report_verification_receipt.schema.json": ["retention/retention-report-verification-receipts.json"],
    "retention_report_closeout_record.schema.json": ["retention/retention-report-closeout-records.json"],
    "retention_publication_record.schema.json": ["retention/retention-publication-records.json"],
    "retention_publication_verification_receipt.schema.json": ["retention/retention-publication-verification-receipts.json"],
    "retention_publication_closeout_record.schema.json": ["retention/retention-publication-closeout-records.json"],
    "retention_dashboard_snapshot_record.schema.json": ["retention/retention-dashboard-snapshot-records.json"],
    "retention_dashboard_snapshot_verification_receipt.schema.json": ["retention/retention-dashboard-snapshot-verification-receipts.json"],
    "retention_dashboard_snapshot_closeout_record.schema.json": ["retention/retention-dashboard-snapshot-closeout-records.json"],
    "retention_summary_record.schema.json": ["retention/retention-summary-records.json"],
    "retention_summary_verification_receipt.schema.json": ["retention/retention-summary-verification-receipts.json"],
    "retention_summary_closeout_record.schema.json": ["retention/retention-summary-closeout-records.json"],
    "retention_export_record.schema.json": ["retention/retention-export-records.json"],
    "retention_export_verification_receipt.schema.json": ["retention/retention-export-verification-receipts.json"],
    "retention_export_closeout_record.schema.json": ["retention/retention-export-closeout-records.json"],
    "retention_handoff_record.schema.json": ["retention/retention-handoff-records.json"],
    "retention_handoff_verification_receipt.schema.json": ["retention/retention-handoff-verification-receipts.json"],
    "retention_handoff_closeout_record.schema.json": ["retention/retention-handoff-closeout-records.json"],
    "retention_acceptance_record.schema.json": ["retention/retention-acceptance-records.json"],
    "retention_acceptance_verification_receipt.schema.json": ["retention/retention-acceptance-verification-receipts.json"],
    "retention_acceptance_closeout_record.schema.json": ["retention/retention-acceptance-closeout-records.json"],
    "retention_package_record.schema.json": ["retention/retention-package-records.json"],
    "retention_package_verification_receipt.schema.json": ["retention/retention-package-verification-receipts.json"],
    "retention_package_closeout_record.schema.json": ["retention/retention-package-closeout-records.json"],
    "retention_finalization_record.schema.json": ["retention/retention-finalization-records.json"],
    "retention_finalization_verification_receipt.schema.json": ["retention/retention-finalization-verification-receipts.json"],
    "retention_finalization_closeout_record.schema.json": ["retention/retention-finalization-closeout-records.json"],
    "retention_terminal_status_record.schema.json": ["retention/retention-terminal-status-records.json"],
    "retention_terminal_status_verification_receipt.schema.json": ["retention/retention-terminal-status-verification-receipts.json"],
    "retention_terminal_status_closeout_record.schema.json": ["retention/retention-terminal-status-closeout-records.json"],
    "retention_certificate_record.schema.json": ["retention/retention-certificate-records.json"],
    "retention_certificate_verification_receipt.schema.json": ["retention/retention-certificate-verification-receipts.json"],
    "retention_certificate_closeout_record.schema.json": ["retention/retention-certificate-closeout-records.json"],
    "retention_registry_record.schema.json": ["retention/retention-registry-records.json"],
    "retention_registry_verification_receipt.schema.json": ["retention/retention-registry-verification-receipts.json"],
    "retention_registry_closeout_record.schema.json": ["retention/retention-registry-closeout-records.json"],
    "retention_closure_record.schema.json": ["retention/retention-closure-records.json"],
    "retention_closure_verification_receipt.schema.json": ["retention/retention-closure-verification-receipts.json"],
    "retention_closure_closeout_record.schema.json": ["retention/retention-closure-closeout-records.json"],
    "retention_completion_record.schema.json": ["retention/retention-completion-records.json"],
    "retention_completion_verification_receipt.schema.json": ["retention/retention-completion-verification-receipts.json"],
    "retention_completion_closeout_record.schema.json": ["retention/retention-completion-closeout-records.json"],
    "retention_attestation_record.schema.json": ["retention/retention-attestation-records.json"],
    "retention_attestation_verification_receipt.schema.json": ["retention/retention-attestation-verification-receipts.json"],
    "retention_attestation_closeout_record.schema.json": ["retention/retention-attestation-closeout-records.json"],
    "retention_seal_record.schema.json": ["retention/retention-seal-records.json"],
    "retention_seal_verification_receipt.schema.json": ["retention/retention-seal-verification-receipts.json"],
    "retention_seal_closeout_record.schema.json": ["retention/retention-seal-closeout-records.json"],
    "retention_notarization_record.schema.json": ["retention/retention-notarization-records.json"],
    "retention_notarization_verification_receipt.schema.json": ["retention/retention-notarization-verification-receipts.json"],
    "retention_notarization_closeout_record.schema.json": ["retention/retention-notarization-closeout-records.json"],
    "retention_archive_anchor_record.schema.json": ["retention/retention-archive-anchor-records.json"],
    "retention_archive_anchor_verification_receipt.schema.json": ["retention/retention-archive-anchor-verification-receipts.json"],
    "retention_archive_anchor_closeout_record.schema.json": ["retention/retention-archive-anchor-closeout-records.json"],
    "retention_endcap_record.schema.json": ["retention/retention-endcap-records.json"],
    "retention_endcap_verification_receipt.schema.json": ["retention/retention-endcap-verification-receipts.json"],
    "retention_endcap_closeout_record.schema.json": ["retention/retention-endcap-closeout-records.json"],
    "retention_final_index_record.schema.json": ["retention/retention-final-index-records.json"],
    "retention_final_index_verification_receipt.schema.json": ["retention/retention-final-index-verification-receipts.json"],
    "retention_final_index_closeout_record.schema.json": ["retention/retention-final-index-closeout-records.json"],
    "retention_master_ledger_record.schema.json": ["retention/retention-master-ledger-records.json"],
    "retention_master_ledger_verification_receipt.schema.json": ["retention/retention-master-ledger-verification-receipts.json"],
    "retention_master_ledger_closeout_record.schema.json": ["retention/retention-master-ledger-closeout-records.json"],
    "retention_terminal_manifest_record.schema.json": ["retention/retention-terminal-manifest-records.json"],
    "retention_terminal_manifest_verification_receipt.schema.json": ["retention/retention-terminal-manifest-verification-receipts.json"],
    "retention_terminal_manifest_closeout_record.schema.json": ["retention/retention-terminal-manifest-closeout-records.json"],
    "retention_repository_release_record.schema.json": ["retention/retention-repository-release-records.json"],
    "retention_repository_release_verification_receipt.schema.json": ["retention/retention-repository-release-verification-receipts.json"],
    "retention_repository_release_closeout_record.schema.json": ["retention/retention-repository-release-closeout-records.json"],
    "retention_deployment_release_record.schema.json": ["retention/retention-deployment-release-records.json"],
    "retention_deployment_release_verification_receipt.schema.json": ["retention/retention-deployment-release-verification-receipts.json"],
    "retention_deployment_release_closeout_record.schema.json": ["retention/retention-deployment-release-closeout-records.json"],
    "retention_availability_notice_record.schema.json": ["retention/retention-availability-notice-records.json"],
    "retention_availability_notice_verification_receipt.schema.json": ["retention/retention-availability-notice-verification-receipts.json"],
    "retention_availability_notice_closeout_record.schema.json": ["retention/retention-availability-notice-closeout-records.json"],
    "retention_release_acknowledgement_record.schema.json": ["retention/retention-release-acknowledgement-records.json"],
    "retention_release_acknowledgement_verification_receipt.schema.json": ["retention/retention-release-acknowledgement-verification-receipts.json"],
    "retention_release_acknowledgement_closeout_record.schema.json": ["retention/retention-release-acknowledgement-closeout-records.json"],
    "retention_release_confirmation_record.schema.json": ["retention/retention-release-confirmation-records.json"],
    "retention_release_confirmation_verification_receipt.schema.json": ["retention/retention-release-confirmation-verification-receipts.json"],
    "retention_release_confirmation_closeout_record.schema.json": ["retention/retention-release-confirmation-closeout-records.json"],
    "retention_distribution_package_record.schema.json": ["retention/retention-distribution-package-records.json"],
    "retention_distribution_package_verification_receipt.schema.json": ["retention/retention-distribution-package-verification-receipts.json"],
    "retention_distribution_package_closeout_record.schema.json": ["retention/retention-distribution-package-closeout-records.json"],
    "retention_distribution_manifest_record.schema.json": ["retention/retention-distribution-manifest-records.json"],
    "retention_distribution_manifest_verification_receipt.schema.json": ["retention/retention-distribution-manifest-verification-receipts.json"],
    "retention_distribution_manifest_closeout_record.schema.json": ["retention/retention-distribution-manifest-closeout-records.json"],
    "retention_access_publication_record.schema.json": ["retention/retention-access-publication-records.json"],
    "retention_access_publication_verification_receipt.schema.json": ["retention/retention-access-publication-verification-receipts.json"],
    "retention_access_publication_closeout_record.schema.json": ["retention/retention-access-publication-closeout-records.json"],
    "retention_access_grant_record.schema.json": ["retention/retention-access-grant-records.json"],
    "retention_access_grant_verification_receipt.schema.json": ["retention/retention-access-grant-verification-receipts.json"],
    "retention_access_grant_closeout_record.schema.json": ["retention/retention-access-grant-closeout-records.json"],
    "retention_access_ledger_record.schema.json": ["retention/retention-access-ledger-records.json"],
    "retention_access_ledger_verification_receipt.schema.json": ["retention/retention-access-ledger-verification-receipts.json"],
    "retention_access_ledger_closeout_record.schema.json": ["retention/retention-access-ledger-closeout-records.json"],
    "retention_retrieval_catalog_record.schema.json": ["retention/retention-retrieval-catalog-records.json"],
    "retention_retrieval_catalog_verification_receipt.schema.json": ["retention/retention-retrieval-catalog-verification-receipts.json"],
    "retention_retrieval_catalog_closeout_record.schema.json": ["retention/retention-retrieval-catalog-closeout-records.json"],
    "retention_retrieval_endpoint_record.schema.json": ["retention/retention-retrieval-endpoint-records.json"],
    "retention_retrieval_endpoint_verification_receipt.schema.json": ["retention/retention-retrieval-endpoint-verification-receipts.json"],
    "retention_retrieval_endpoint_closeout_record.schema.json": ["retention/retention-retrieval-endpoint-closeout-records.json"],
    "retention_retrieval_token_record.schema.json": ["retention/retention-retrieval-token-records.json"],
    "retention_retrieval_token_verification_receipt.schema.json": ["retention/retention-retrieval-token-verification-receipts.json"],
    "retention_retrieval_token_closeout_record.schema.json": ["retention/retention-retrieval-token-closeout-records.json"],
    "retention_consumer_receipt_record.schema.json": ["retention/retention-consumer-receipt-records.json"],
    "retention_consumer_receipt_verification_receipt.schema.json": ["retention/retention-consumer-receipt-verification-receipts.json"],
    "retention_consumer_receipt_closeout_record.schema.json": ["retention/retention-consumer-receipt-closeout-records.json"],
    "retention_publication_rollup_record.schema.json": ["retention/retention-publication-rollup-records.json"],
    "retention_publication_rollup_verification_receipt.schema.json": ["retention/retention-publication-rollup-verification-receipts.json"],
    "retention_publication_rollup_closeout_record.schema.json": ["retention/retention-publication-rollup-closeout-records.json"],
    "retention_distribution_receipt_record.schema.json": ["retention/retention-distribution-receipt-records.json"],
    "retention_distribution_receipt_verification_receipt.schema.json": ["retention/retention-distribution-receipt-verification-receipts.json"],
    "retention_distribution_receipt_closeout_record.schema.json": ["retention/retention-distribution-receipt-closeout-records.json"],
    "retention_access_audit_snapshot_record.schema.json": ["retention/retention-access-audit-snapshot-records.json"],
    "retention_access_audit_snapshot_verification_receipt.schema.json": ["retention/retention-access-audit-snapshot-verification-receipts.json"],
    "retention_access_audit_snapshot_closeout_record.schema.json": ["retention/retention-access-audit-snapshot-closeout-records.json"],
    "retention_release_health_snapshot_record.schema.json": ["retention/retention-release-health-snapshot-records.json"],
    "retention_release_health_snapshot_verification_receipt.schema.json": ["retention/retention-release-health-snapshot-verification-receipts.json"],
    "retention_release_health_snapshot_closeout_record.schema.json": ["retention/retention-release-health-snapshot-closeout-records.json"],
    "retention_release_usage_summary_record.schema.json": ["retention/retention-release-usage-summary-records.json"],
    "retention_release_usage_summary_verification_receipt.schema.json": ["retention/retention-release-usage-summary-verification-receipts.json"],
    "retention_release_usage_summary_closeout_record.schema.json": ["retention/retention-release-usage-summary-closeout-records.json"],
    "retention_retention_exposure_report_record.schema.json": ["retention/retention-retention-exposure-report-records.json"],
    "retention_retention_exposure_report_verification_receipt.schema.json": ["retention/retention-retention-exposure-report-verification-receipts.json"],
    "retention_retention_exposure_report_closeout_record.schema.json": ["retention/retention-retention-exposure-report-closeout-records.json"],
    "retention_release_closeout_summary_record.schema.json": ["retention/retention-release-closeout-summary-records.json"],
    "retention_release_closeout_summary_verification_receipt.schema.json": ["retention/retention-release-closeout-summary-verification-receipts.json"],
    "retention_release_closeout_summary_closeout_record.schema.json": ["retention/retention-release-closeout-summary-closeout-records.json"],
    "retention_public_record_index_record.schema.json": ["retention/retention-public-record-index-records.json"],
    "retention_public_record_index_verification_receipt.schema.json": ["retention/retention-public-record-index-verification-receipts.json"],
    "retention_public_record_index_closeout_record.schema.json": ["retention/retention-public-record-index-closeout-records.json"],
    "retention_final_release_bundle_record.schema.json": ["retention/retention-final-release-bundle-records.json"],
    "retention_final_release_bundle_verification_receipt.schema.json": ["retention/retention-final-release-bundle-verification-receipts.json"],
    "retention_final_release_bundle_closeout_record.schema.json": ["retention/retention-final-release-bundle-closeout-records.json"],
    "retention_terminal_access_notice_record.schema.json": ["retention/retention-terminal-access-notice-records.json"],
    "retention_terminal_access_notice_verification_receipt.schema.json": ["retention/retention-terminal-access-notice-verification-receipts.json"],
    "retention_terminal_access_notice_closeout_record.schema.json": ["retention/retention-terminal-access-notice-closeout-records.json"],
    "merge_decision.schema.json": ["merge/merge-decisions.json"],
    "delivery_channel_registry.schema.json": ["delivery/delivery-channel-registry.json"],
    "delivery_job.schema.json": ["delivery/delivery-jobs.json"],
    "transport_adapter_registry.schema.json": ["transport/transport-adapter-registry.json"],
    "transport_receipt.schema.json": ["transport/transport-receipts.json"],
    "routing_policy.schema.json": ["routing/routing-policy.json"],
    "exchange_bundle.schema.json": ["bundles/**/*.bundle.json"],
    "exchange_receipt.schema.json": ["exchange/exchange-receipts.json"],
    "reconciliation_record.schema.json": ["reconciliation/reconciliation-records.json"],
    "quality_policy.schema.json": ["quality/quality-policy.json"],
    "quality_assessment.schema.json": ["quality/quality-assessments.json"],
    "action_policy.schema.json": ["action/action-policy.json"],
    "action_record.schema.json": ["action/action-records.json"],
    "playbook.schema.json": ["playbooks/**/*.playbook.json"],
}


@dataclass(frozen=True)
class SchemaContractReport:
    root: Path
    checked_records: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_records(value: Any) -> list[JsonObject]:
    if isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        records: list[JsonObject] = []
        for item in value:
            if not isinstance(item, dict):
                raise ValueError("record arrays must contain JSON objects")
            records.append(item)
        return records
    raise ValueError("expected JSON object or array")


def _required_fields(schema: JsonObject) -> list[str]:
    required = schema.get("required", [])
    if not isinstance(required, list):
        return []
    return [str(item) for item in required]


def validate_records_against_schema(schema_path: Path, record_paths: list[Path], root: Path) -> tuple[int, list[str]]:
    schema = _load_json(schema_path)
    required = _required_fields(schema)
    failures: list[str] = []
    checked = 0

    for record_path in sorted(set(record_paths)):
        records = _as_records(_load_json(record_path))
        for index, record in enumerate(records):
            checked += 1
            record_label = f"{record_path.relative_to(root)}[{index}]"
            for field in required:
                if field not in record or record[field] in (None, "", []):
                    failures.append(f"{record_label} missing required field {field!r} from {schema_path.name}")

    return checked, failures


def validate_schema_contracts(root: str | Path) -> SchemaContractReport:
    root_path = Path(root)
    failures: list[str] = []
    checked_records = 0

    for schema_name, patterns in SCHEMA_TO_FIXTURE_FILES.items():
        schema_path = root_path / "schemas" / schema_name
        if not schema_path.exists():
            failures.append(f"missing schema: schemas/{schema_name}")
            continue

        record_paths: list[Path] = []
        for pattern in patterns:
            record_paths.extend(root_path.glob(pattern))

        checked, schema_failures = validate_records_against_schema(schema_path, record_paths, root_path)
        checked_records += checked
        failures.extend(schema_failures)

    return SchemaContractReport(root=root_path, checked_records=checked_records, failures=failures)


def format_schema_contract_report(report: SchemaContractReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM schema contract root: {report.root}")
    lines.append(f"Records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM schema contract validation failed.")
    else:
        lines.append("")
        lines.append("PFEM schema contract validation passed.")

    return "\n".join(lines)
