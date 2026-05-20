"""PFEM audit journal validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


JsonObject = dict[str, Any]

KNOWN_EVENT_KINDS = {
    "review_approved", "review_rejected", "integrity_receipts_generated",
    "policy_changed", "topology_changed", "federation_message_prepared",
    "evidence_package_assembled", "exchange_bundle_exported",
    "exchange_bundle_received", "exchange_bundle_accepted",
    "exchange_bundle_rejected", "reconciliation_recorded",
    "quality_assessment_recorded", "action_recorded", "playbook_registered",
    "routing_policy_registered", "delivery_channel_registered",
    "transport_adapter_registered", "dispatch_policy_registered",
    "dispatch_decision_recorded", "outbox_item_staged", "inbox_item_received",
    "intake_decision_recorded", "import_recorded", "conflict_recorded", "merge_decision_recorded", "apply_receipt_recorded", "state_checkpoint_recorded", "state_transition_recorded", "snapshot_manifest_recorded", "snapshot_verification_recorded", "recovery_point_recorded", "restore_plan_recorded", "restore_approval_recorded", "restore_receipt_recorded", "restore_verification_recorded", "restore_closeout_recorded", "disposition_recorded", "disposition_receipt_recorded", "custody_recorded", "custody_verification_recorded", "custody_transfer_recorded", "custody_transfer_verification_recorded", "custody_closeout_recorded", "custody_chain_recorded", "custody_chain_verification_recorded", "custody_ledger_recorded", "custody_ledger_verification_recorded", "custody_release_request_recorded", "custody_release_approval_recorded", "custody_release_receipt_recorded", "custody_release_verification_recorded", "custody_release_closeout_recorded", "custody_release_chain_recorded", "custody_release_chain_verification_recorded", "custody_lifecycle_recorded", "custody_lifecycle_verification_recorded", "custody_lifecycle_closeout_recorded", "archive_manifest_recorded", "archive_receipt_recorded", "archive_verification_recorded", "archive_closeout_recorded", "archive_chain_recorded", "archive_chain_verification_recorded", "archive_index_recorded", "archive_index_verification_recorded", "archive_index_closeout_recorded", "archive_lifecycle_recorded", "archive_lifecycle_verification_recorded", "archive_lifecycle_closeout_recorded", "preservation_recorded", "preservation_verification_recorded", "preservation_closeout_recorded", "preservation_chain_recorded", "preservation_chain_verification_recorded", "retention_review_recorded", "retention_review_verification_recorded", "retention_decision_recorded", "retention_decision_approval_recorded", "retention_action_receipt_recorded", "retention_action_verification_recorded", "retention_action_closeout_recorded", "retention_chain_recorded", "retention_chain_verification_recorded", "retention_lifecycle_recorded", "retention_lifecycle_verification_recorded", "retention_lifecycle_closeout_recorded", "retention_ledger_recorded", "retention_ledger_verification_recorded", "retention_ledger_closeout_recorded", "retention_policy_compliance_recorded", "retention_policy_compliance_verification_recorded", "retention_obligation_recorded", "retention_obligation_verification_recorded", "retention_schedule_recorded", "retention_schedule_verification_recorded", "retention_schedule_closeout_recorded", "retention_cycle_recorded", "retention_cycle_verification_recorded", "retention_cycle_closeout_recorded", "retention_hold_recorded", "retention_hold_verification_recorded", "retention_hold_closeout_recorded", "retention_status_snapshot_recorded", "retention_status_snapshot_verification_recorded", "retention_rollup_recorded", "retention_rollup_verification_recorded", "retention_rollup_closeout_recorded", "retention_report_recorded", "retention_report_verification_recorded", "retention_report_closeout_recorded", "retention_publication_recorded", "retention_publication_verification_recorded", "retention_publication_closeout_recorded", "retention_dashboard_snapshot_recorded", "retention_dashboard_snapshot_verification_recorded", "retention_dashboard_snapshot_closeout_recorded", "retention_summary_recorded", "retention_summary_verification_recorded", "retention_summary_closeout_recorded", "retention_export_recorded", "retention_export_verification_recorded", "retention_export_closeout_recorded", "retention_handoff_recorded", "retention_handoff_verification_recorded", "retention_handoff_closeout_recorded", "retention_acceptance_recorded", "retention_acceptance_verification_recorded", "retention_acceptance_closeout_recorded", "retention_package_recorded", "retention_package_verification_recorded", "retention_package_closeout_recorded", "retention_finalization_recorded", "retention_finalization_verification_recorded", "retention_finalization_closeout_recorded", "retention_terminal_status_recorded", "retention_terminal_status_verification_recorded", "retention_terminal_status_closeout_recorded", "retention_certificate_recorded", "retention_certificate_verification_recorded", "retention_certificate_closeout_recorded", "retention_registry_recorded", "retention_registry_verification_recorded", "retention_registry_closeout_recorded", "retention_closure_recorded", "retention_closure_verification_recorded", "retention_closure_closeout_recorded", "retention_completion_recorded", "retention_completion_verification_recorded", "retention_completion_closeout_recorded", "retention_attestation_recorded", "retention_attestation_verification_recorded", "retention_attestation_closeout_recorded", "retention_seal_recorded", "retention_seal_verification_recorded", "retention_seal_closeout_recorded", "retention_notarization_recorded", "retention_notarization_verification_recorded", "retention_notarization_closeout_recorded", "retention_archive_anchor_recorded", "retention_archive_anchor_verification_recorded", "retention_archive_anchor_closeout_recorded", "retention_endcap_recorded", "retention_endcap_verification_recorded", "retention_endcap_closeout_recorded", "retention_final_index_recorded", "retention_final_index_verification_recorded", "retention_final_index_closeout_recorded", "retention_master_ledger_recorded", "retention_master_ledger_verification_recorded", "retention_master_ledger_closeout_recorded", "retention_terminal_manifest_recorded", "retention_terminal_manifest_verification_recorded", "retention_terminal_manifest_closeout_recorded", "retention_repository_release_recorded", "retention_repository_release_verification_recorded", "retention_repository_release_closeout_recorded", "retention_deployment_release_recorded", "retention_deployment_release_verification_recorded", "retention_deployment_release_closeout_recorded", "retention_availability_notice_recorded", "retention_availability_notice_verification_recorded", "retention_availability_notice_closeout_recorded", "retention_release_acknowledgement_recorded", "retention_release_acknowledgement_verification_recorded", "retention_release_acknowledgement_closeout_recorded", "retention_release_confirmation_recorded", "retention_release_confirmation_verification_recorded", "retention_release_confirmation_closeout_recorded", "retention_distribution_package_recorded", "retention_distribution_package_verification_recorded", "retention_distribution_package_closeout_recorded", "retention_distribution_manifest_recorded", "retention_distribution_manifest_verification_recorded", "retention_distribution_manifest_closeout_recorded", "retention_access_publication_recorded", "retention_access_publication_verification_recorded", "retention_access_publication_closeout_recorded", "retention_access_grant_recorded", "retention_access_grant_verification_recorded", "retention_access_grant_closeout_recorded", "retention_access_ledger_recorded", "retention_access_ledger_verification_recorded", "retention_access_ledger_closeout_recorded", "retention_retrieval_catalog_recorded", "retention_retrieval_catalog_verification_recorded", "retention_retrieval_catalog_closeout_recorded", "retention_retrieval_endpoint_recorded", "retention_retrieval_endpoint_verification_recorded", "retention_retrieval_endpoint_closeout_recorded", "retention_retrieval_token_recorded", "retention_retrieval_token_verification_recorded", "retention_retrieval_token_closeout_recorded", "retention_consumer_receipt_recorded", "retention_consumer_receipt_verification_recorded", "retention_consumer_receipt_closeout_recorded", "retention_publication_rollup_recorded", "retention_publication_rollup_verification_recorded", "retention_publication_rollup_closeout_recorded", "retention_distribution_receipt_recorded", "retention_distribution_receipt_verification_recorded", "retention_distribution_receipt_closeout_recorded", "retention_access_audit_snapshot_recorded", "retention_access_audit_snapshot_verification_recorded", "retention_access_audit_snapshot_closeout_recorded", "retention_release_health_snapshot_recorded", "retention_release_health_snapshot_verification_recorded", "retention_release_health_snapshot_closeout_recorded", "retention_release_usage_summary_recorded", "retention_release_usage_summary_verification_recorded", "retention_release_usage_summary_closeout_recorded", "retention_retention_exposure_report_recorded", "retention_retention_exposure_report_verification_recorded", "retention_retention_exposure_report_closeout_recorded", "retention_release_closeout_summary_recorded", "retention_release_closeout_summary_verification_recorded", "retention_release_closeout_summary_closeout_recorded", "retention_public_record_index_recorded", "retention_public_record_index_verification_recorded", "retention_public_record_index_closeout_recorded", "retention_final_release_bundle_recorded", "retention_final_release_bundle_verification_recorded", "retention_final_release_bundle_closeout_recorded", "retention_terminal_access_notice_recorded", "retention_terminal_access_notice_verification_recorded", "retention_terminal_access_notice_closeout_recorded", "retention_release_acceptance_recorded", "retention_release_acceptance_verification_recorded", "retention_release_acceptance_closeout_recorded", "retention_access_completion_recorded", "retention_access_completion_verification_recorded", "retention_access_completion_closeout_recorded", "retention_publication_certificate_recorded", "retention_publication_certificate_verification_recorded", "retention_publication_certificate_closeout_recorded", "retention_distribution_closure_notice_recorded", "retention_distribution_closure_notice_verification_recorded", "retention_distribution_closure_notice_closeout_recorded", "retention_public_access_register_recorded", "retention_public_access_register_verification_recorded", "retention_public_access_register_closeout_recorded", "retention_release_access_index_recorded", "retention_release_access_index_verification_recorded", "retention_release_access_index_closeout_recorded", "retention_release_access_verification_summary_recorded", "retention_release_access_verification_summary_verification_recorded", "retention_release_access_verification_summary_closeout_recorded", "retention_release_access_closeout_summary_recorded", "retention_release_access_closeout_summary_verification_recorded", "retention_release_access_closeout_summary_closeout_recorded", "retention_archive_availability_rollup_recorded", "retention_archive_availability_rollup_verification_recorded", "retention_archive_availability_rollup_closeout_recorded", "retention_retrieval_readiness_snapshot_recorded", "retention_retrieval_readiness_snapshot_verification_recorded", "retention_retrieval_readiness_snapshot_closeout_recorded", "retention_consumer_availability_notice_recorded", "retention_consumer_availability_notice_verification_recorded", "retention_consumer_availability_notice_closeout_recorded", "retention_public_release_receipt_recorded", "retention_public_release_receipt_verification_recorded", "retention_public_release_receipt_closeout_recorded", "retention_release_exception_register_recorded", "retention_release_exception_register_verification_recorded", "retention_release_exception_register_closeout_recorded", "retention_release_exception_summary_recorded", "retention_release_exception_summary_verification_recorded", "retention_release_exception_summary_closeout_recorded", "retention_release_metrics_snapshot_recorded", "retention_release_metrics_snapshot_verification_recorded", "retention_release_metrics_snapshot_closeout_recorded", "retention_release_terminal_report_recorded", "retention_release_terminal_report_verification_recorded", "retention_release_terminal_report_closeout_recorded", "retention_final_publication_notice_recorded", "retention_final_publication_notice_verification_recorded",
    "delivery_job_recorded", "transport_receipt_recorded",
}


@dataclass(frozen=True)
class AuditEvent:
    audit_id: str
    event_kind: str
    created_time: str
    actor_ref: str
    subject_refs: list[str]
    summary: str
    source_tool: str | None = None


@dataclass(frozen=True)
class AuditReport:
    source: str
    checked_events: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _load_records(path: Path) -> list[JsonObject]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        return [raw]
    if isinstance(raw, list):
        records: list[JsonObject] = []
        for item in raw:
            if not isinstance(item, dict):
                raise ValueError(f"expected JSON object records in {path}")
            records.append(item)
        return records
    raise ValueError(f"expected JSON object or array in {path}")


def load_audit_events(path: str | Path) -> list[AuditEvent]:
    return [
        AuditEvent(
            audit_id=str(record.get("audit_id", "")),
            event_kind=str(record.get("event_kind", "")),
            created_time=str(record.get("created_time", "")),
            actor_ref=str(record.get("actor_ref", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            summary=str(record.get("summary", "")),
            source_tool=str(record["source_tool"]) if "source_tool" in record else None,
        )
        for record in _load_records(Path(path))
    ]


def _collect_known_record_ids(root: Path) -> set[str]:
    patterns = [
        ("tests/fixtures/**/raw_evidence.json", "evidence_id"),
        ("tests/fixtures/**/normalized_observation.json", "observation_id"),
        ("tests/fixtures/**/finding.json", "finding_id"),
        ("tests/fixtures/**/alert.json", "alert_id"),
        ("tests/fixtures/**/evidence_package.json", "package_id"),
        ("tests/fixtures/**/rollup_summary.json", "rollup_id"),
        ("tests/fixtures/**/federation_message.json", "message_id"),
        ("review/review-records.json", "review_id"),
        ("audit/audit-journal.json", "audit_id"),
        ("bundles/**/*.bundle.json", "bundle_id"),
        ("exchange/exchange-receipts.json", "exchange_receipt_id"),
        ("reconciliation/reconciliation-records.json", "reconciliation_id"),
        ("quality/quality-assessments.json", "quality_assessment_id"),
        ("action/action-records.json", "action_id"),
        ("playbooks/**/*.playbook.json", "playbook_id"),
        ("delivery/delivery-jobs.json", "delivery_job_id"),
        ("dispatch/dispatch-decisions.json", "dispatch_decision_id"),
        ("outbox/outbox-items.json", "outbox_item_id"),
        ("inbox/inbox-items.json", "inbox_item_id"),
        ("intake/intake-decisions.json", "intake_decision_id"),
        ("imports/import-records.json", "import_record_id"),
        ("conflicts/conflict-records.json", "conflict_record_id"),
        ("merge/merge-decisions.json", "merge_decision_id"),
        ("apply/apply-receipts.json", "apply_receipt_id"),
        ("state/state-checkpoints.json", "state_checkpoint_id"),
        ("state/state-transitions.json", "state_transition_id"),
        ("snapshots/snapshot-manifests.json", "snapshot_manifest_id"),
        ("snapshots/snapshot-verification-receipts.json", "snapshot_verification_receipt_id"),
        ("recovery/recovery-points.json", "recovery_point_id"),
        ("restore/restore-plans.json", "restore_plan_id"),
        ("restore/restore-approvals.json", "restore_approval_id"),
        ("restore/restore-receipts.json", "restore_receipt_id"),
        ("restore/restore-verification-receipts.json", "restore_verification_receipt_id"),
        ("restore/restore-closeout-records.json", "restore_closeout_record_id"),
        ("disposition/disposition-records.json", "disposition_record_id"),
        ("disposition/disposition-receipts.json", "disposition_receipt_id"),
        ("custody/custody-records.json", "custody_record_id"),
        ("custody/custody-verification-receipts.json", "custody_verification_receipt_id"),
        ("custody/custody-transfer-records.json", "custody_transfer_record_id"),
        ("custody/custody-transfer-verification-receipts.json", "custody_transfer_verification_receipt_id"),
        ("custody/custody-closeout-records.json", "custody_closeout_record_id"),
        ("custody/custody-chain-records.json", "custody_chain_record_id"),
        ("custody/custody-chain-verification-receipts.json", "custody_chain_verification_receipt_id"),
        ("custody/custody-ledger-records.json", "custody_ledger_record_id"),
        ("custody/custody-ledger-verification-receipts.json", "custody_ledger_verification_receipt_id"),
        ("custody/custody-release-requests.json", "custody_release_request_id"),
        ("custody/custody-release-approvals.json", "custody_release_approval_id"),
        ("custody/custody-release-receipts.json", "custody_release_receipt_id"),
        ("custody/custody-release-verification-receipts.json", "custody_release_verification_receipt_id"),
        ("custody/custody-release-closeout-records.json", "custody_release_closeout_record_id"),
        ("custody/custody-release-chain-records.json", "custody_release_chain_record_id"),
        ("custody/custody-release-chain-verification-receipts.json", "custody_release_chain_verification_receipt_id"),
        ("custody/custody-lifecycle-records.json", "custody_lifecycle_record_id"),
        ("custody/custody-lifecycle-verification-receipts.json", "custody_lifecycle_verification_receipt_id"),
        ("custody/custody-lifecycle-closeout-records.json", "custody_lifecycle_closeout_record_id"),
        ("archive/archive-manifest-records.json", "archive_manifest_record_id"),
        ("archive/archive-receipts.json", "archive_receipt_id"),
        ("archive/archive-verification-receipts.json", "archive_verification_receipt_id"),
        ("archive/archive-closeout-records.json", "archive_closeout_record_id"),
        ("archive/archive-chain-records.json", "archive_chain_record_id"),
        ("archive/archive-chain-verification-receipts.json", "archive_chain_verification_receipt_id"),
        ("archive/archive-index-records.json", "archive_index_record_id"),
        ("archive/archive-index-verification-receipts.json", "archive_index_verification_receipt_id"),
        ("archive/archive-index-closeout-records.json", "archive_index_closeout_record_id"),
        ("archive/archive-lifecycle-records.json", "archive_lifecycle_record_id"),
        ("archive/archive-lifecycle-verification-receipts.json", "archive_lifecycle_verification_receipt_id"),
        ("archive/archive-lifecycle-closeout-records.json", "archive_lifecycle_closeout_record_id"),
        ("preservation/preservation-records.json", "preservation_record_id"),
        ("preservation/preservation-verification-receipts.json", "preservation_verification_receipt_id"),
        ("preservation/preservation-closeout-records.json", "preservation_closeout_record_id"),
        ("preservation/preservation-chain-records.json", "preservation_chain_record_id"),
        ("preservation/preservation-chain-verification-receipts.json", "preservation_chain_verification_receipt_id"),
        ("retention/retention-review-records.json", "retention_review_record_id"),
        ("retention/retention-review-verification-receipts.json", "retention_review_verification_receipt_id"),
        ("retention/retention-decision-records.json", "retention_decision_record_id"),
        ("retention/retention-decision-approvals.json", "retention_decision_approval_id"),
        ("retention/retention-action-receipts.json", "retention_action_receipt_id"),
        ("retention/retention-action-verification-receipts.json", "retention_action_verification_receipt_id"),
        ("retention/retention-action-closeout-records.json", "retention_action_closeout_record_id"),
        ("retention/retention-chain-records.json", "retention_chain_record_id"),
        ("retention/retention-chain-verification-receipts.json", "retention_chain_verification_receipt_id"),
        ("retention/retention-lifecycle-records.json", "retention_lifecycle_record_id"),
        ("retention/retention-lifecycle-verification-receipts.json", "retention_lifecycle_verification_receipt_id"),
        ("retention/retention-lifecycle-closeout-records.json", "retention_lifecycle_closeout_record_id"),
        ("retention/retention-ledger-records.json", "retention_ledger_record_id"),
        ("retention/retention-ledger-verification-receipts.json", "retention_ledger_verification_receipt_id"),
        ("retention/retention-ledger-closeout-records.json", "retention_ledger_closeout_record_id"),
        ("retention/retention-policy-compliance-records.json", "retention_policy_compliance_record_id"),
        ("retention/retention-policy-compliance-verification-receipts.json", "retention_policy_compliance_verification_receipt_id"),
        ("retention/retention-obligation-records.json", "retention_obligation_record_id"),
        ("retention/retention-obligation-verification-receipts.json", "retention_obligation_verification_receipt_id"),
        ("retention/retention-schedule-records.json", "retention_schedule_record_id"),
        ("retention/retention-schedule-verification-receipts.json", "retention_schedule_verification_receipt_id"),
        ("retention/retention-schedule-closeout-records.json", "retention_schedule_closeout_record_id"),
        ("retention/retention-cycle-records.json", "retention_cycle_record_id"),
        ("retention/retention-cycle-verification-receipts.json", "retention_cycle_verification_receipt_id"),
        ("retention/retention-cycle-closeout-records.json", "retention_cycle_closeout_record_id"),
        ("retention/retention-hold-records.json", "retention_hold_record_id"),
        ("retention/retention-hold-verification-receipts.json", "retention_hold_verification_receipt_id"),
        ("retention/retention-hold-closeout-records.json", "retention_hold_closeout_record_id"),
        ("retention/retention-status-snapshot-records.json", "retention_status_snapshot_record_id"),
        ("retention/retention-status-snapshot-verification-receipts.json", "retention_status_snapshot_verification_receipt_id"),
        ("retention/retention-rollup-records.json", "retention_rollup_record_id"),
        ("retention/retention-rollup-verification-receipts.json", "retention_rollup_verification_receipt_id"),
        ("retention/retention-rollup-closeout-records.json", "retention_rollup_closeout_record_id"),
        ("retention/retention-report-records.json", "retention_report_record_id"),
        ("retention/retention-report-verification-receipts.json", "retention_report_verification_receipt_id"),
        ("retention/retention-report-closeout-records.json", "retention_report_closeout_record_id"),
        ("retention/retention-publication-records.json", "retention_publication_record_id"),
        ("retention/retention-publication-verification-receipts.json", "retention_publication_verification_receipt_id"),
        ("retention/retention-publication-closeout-records.json", "retention_publication_closeout_record_id"),
        ("retention/retention-dashboard-snapshot-records.json", "retention_dashboard_snapshot_record_id"),
        ("retention/retention-dashboard-snapshot-verification-receipts.json", "retention_dashboard_snapshot_verification_receipt_id"),
        ("retention/retention-dashboard-snapshot-closeout-records.json", "retention_dashboard_snapshot_closeout_record_id"),
        ("retention/retention-summary-records.json", "retention_summary_record_id"),
        ("retention/retention-summary-verification-receipts.json", "retention_summary_verification_receipt_id"),
        ("retention/retention-summary-closeout-records.json", "retention_summary_closeout_record_id"),
        ("retention/retention-export-records.json", "retention_export_record_id"),
        ("retention/retention-export-verification-receipts.json", "retention_export_verification_receipt_id"),
        ("retention/retention-export-closeout-records.json", "retention_export_closeout_record_id"),
        ("retention/retention-handoff-records.json", "retention_handoff_record_id"),
        ("retention/retention-handoff-verification-receipts.json", "retention_handoff_verification_receipt_id"),
        ("retention/retention-handoff-closeout-records.json", "retention_handoff_closeout_record_id"),
        ("retention/retention-acceptance-records.json", "retention_acceptance_record_id"),
        ("retention/retention-acceptance-verification-receipts.json", "retention_acceptance_verification_receipt_id"),
        ("retention/retention-acceptance-closeout-records.json", "retention_acceptance_closeout_record_id"),
        ("retention/retention-package-records.json", "retention_package_record_id"),
        ("retention/retention-package-verification-receipts.json", "retention_package_verification_receipt_id"),
        ("retention/retention-package-closeout-records.json", "retention_package_closeout_record_id"),
        ("retention/retention-finalization-records.json", "retention_finalization_record_id"),
        ("retention/retention-finalization-verification-receipts.json", "retention_finalization_verification_receipt_id"),
        ("retention/retention-finalization-closeout-records.json", "retention_finalization_closeout_record_id"),
        ("retention/retention-terminal-status-records.json", "retention_terminal_status_record_id"),
        ("retention/retention-terminal-status-verification-receipts.json", "retention_terminal_status_verification_receipt_id"),
        ("retention/retention-terminal-status-closeout-records.json", "retention_terminal_status_closeout_record_id"),
        ("retention/retention-certificate-records.json", "retention_certificate_record_id"),
        ("retention/retention-certificate-verification-receipts.json", "retention_certificate_verification_receipt_id"),
        ("retention/retention-certificate-closeout-records.json", "retention_certificate_closeout_record_id"),
        ("retention/retention-registry-records.json", "retention_registry_record_id"),
        ("retention/retention-registry-verification-receipts.json", "retention_registry_verification_receipt_id"),
        ("retention/retention-registry-closeout-records.json", "retention_registry_closeout_record_id"),
        ("retention/retention-closure-records.json", "retention_closure_record_id"),
        ("retention/retention-closure-verification-receipts.json", "retention_closure_verification_receipt_id"),
        ("retention/retention-closure-closeout-records.json", "retention_closure_closeout_record_id"),
        ("retention/retention-completion-records.json", "retention_completion_record_id"),
        ("retention/retention-completion-verification-receipts.json", "retention_completion_verification_receipt_id"),
        ("retention/retention-completion-closeout-records.json", "retention_completion_closeout_record_id"),
        ("retention/retention-attestation-records.json", "retention_attestation_record_id"),
        ("retention/retention-attestation-verification-receipts.json", "retention_attestation_verification_receipt_id"),
        ("retention/retention-attestation-closeout-records.json", "retention_attestation_closeout_record_id"),
        ("retention/retention-seal-records.json", "retention_seal_record_id"),
        ("retention/retention-seal-verification-receipts.json", "retention_seal_verification_receipt_id"),
        ("retention/retention-seal-closeout-records.json", "retention_seal_closeout_record_id"),
        ("retention/retention-notarization-records.json", "retention_notarization_record_id"),
        ("retention/retention-notarization-verification-receipts.json", "retention_notarization_verification_receipt_id"),
        ("retention/retention-notarization-closeout-records.json", "retention_notarization_closeout_record_id"),
        ("retention/retention-archive-anchor-records.json", "retention_archive_anchor_record_id"),
        ("retention/retention-archive-anchor-verification-receipts.json", "retention_archive_anchor_verification_receipt_id"),
        ("retention/retention-archive-anchor-closeout-records.json", "retention_archive_anchor_closeout_record_id"),
        ("retention/retention-endcap-records.json", "retention_endcap_record_id"),
        ("retention/retention-endcap-verification-receipts.json", "retention_endcap_verification_receipt_id"),
        ("retention/retention-endcap-closeout-records.json", "retention_endcap_closeout_record_id"),
        ("retention/retention-final-index-records.json", "retention_final_index_record_id"),
        ("retention/retention-final-index-verification-receipts.json", "retention_final_index_verification_receipt_id"),
        ("retention/retention-final-index-closeout-records.json", "retention_final_index_closeout_record_id"),
        ("retention/retention-master-ledger-records.json", "retention_master_ledger_record_id"),
        ("retention/retention-master-ledger-verification-receipts.json", "retention_master_ledger_verification_receipt_id"),
        ("retention/retention-master-ledger-closeout-records.json", "retention_master_ledger_closeout_record_id"),
        ("retention/retention-terminal-manifest-records.json", "retention_terminal_manifest_record_id"),
        ("retention/retention-terminal-manifest-verification-receipts.json", "retention_terminal_manifest_verification_receipt_id"),
        ("retention/retention-terminal-manifest-closeout-records.json", "retention_terminal_manifest_closeout_record_id"),
        ("retention/retention-repository-release-records.json", "retention_repository_release_record_id"),
        ("retention/retention-repository-release-verification-receipts.json", "retention_repository_release_verification_receipt_id"),
        ("retention/retention-repository-release-closeout-records.json", "retention_repository_release_closeout_record_id"),
        ("retention/retention-deployment-release-records.json", "retention_deployment_release_record_id"),
        ("retention/retention-deployment-release-verification-receipts.json", "retention_deployment_release_verification_receipt_id"),
        ("retention/retention-deployment-release-closeout-records.json", "retention_deployment_release_closeout_record_id"),
        ("retention/retention-availability-notice-records.json", "retention_availability_notice_record_id"),
        ("retention/retention-availability-notice-verification-receipts.json", "retention_availability_notice_verification_receipt_id"),
        ("retention/retention-availability-notice-closeout-records.json", "retention_availability_notice_closeout_record_id"),
        ("retention/retention-release-acknowledgement-records.json", "retention_release_acknowledgement_record_id"),
        ("retention/retention-release-acknowledgement-verification-receipts.json", "retention_release_acknowledgement_verification_receipt_id"),
        ("retention/retention-release-acknowledgement-closeout-records.json", "retention_release_acknowledgement_closeout_record_id"),
        ("retention/retention-release-confirmation-records.json", "retention_release_confirmation_record_id"),
        ("retention/retention-release-confirmation-verification-receipts.json", "retention_release_confirmation_verification_receipt_id"),
        ("retention/retention-release-confirmation-closeout-records.json", "retention_release_confirmation_closeout_record_id"),
        ("retention/retention-distribution-package-records.json", "retention_distribution_package_record_id"),
        ("retention/retention-distribution-package-verification-receipts.json", "retention_distribution_package_verification_receipt_id"),
        ("retention/retention-distribution-package-closeout-records.json", "retention_distribution_package_closeout_record_id"),
        ("retention/retention-distribution-manifest-records.json", "retention_distribution_manifest_record_id"),
        ("retention/retention-distribution-manifest-verification-receipts.json", "retention_distribution_manifest_verification_receipt_id"),
        ("retention/retention-distribution-manifest-closeout-records.json", "retention_distribution_manifest_closeout_record_id"),
        ("retention/retention-access-publication-records.json", "retention_access_publication_record_id"),
        ("retention/retention-access-publication-verification-receipts.json", "retention_access_publication_verification_receipt_id"),
        ("retention/retention-access-publication-closeout-records.json", "retention_access_publication_closeout_record_id"),
        ("retention/retention-access-grant-records.json", "retention_access_grant_record_id"),
        ("retention/retention-access-grant-verification-receipts.json", "retention_access_grant_verification_receipt_id"),
        ("retention/retention-access-grant-closeout-records.json", "retention_access_grant_closeout_record_id"),
        ("retention/retention-access-ledger-records.json", "retention_access_ledger_record_id"),
        ("retention/retention-access-ledger-verification-receipts.json", "retention_access_ledger_verification_receipt_id"),
        ("retention/retention-access-ledger-closeout-records.json", "retention_access_ledger_closeout_record_id"),
        ("retention/retention-retrieval-catalog-records.json", "retention_retrieval_catalog_record_id"),
        ("retention/retention-retrieval-catalog-verification-receipts.json", "retention_retrieval_catalog_verification_receipt_id"),
        ("retention/retention-retrieval-catalog-closeout-records.json", "retention_retrieval_catalog_closeout_record_id"),
        ("retention/retention-retrieval-endpoint-records.json", "retention_retrieval_endpoint_record_id"),
        ("retention/retention-retrieval-endpoint-verification-receipts.json", "retention_retrieval_endpoint_verification_receipt_id"),
        ("retention/retention-retrieval-endpoint-closeout-records.json", "retention_retrieval_endpoint_closeout_record_id"),
        ("retention/retention-retrieval-token-records.json", "retention_retrieval_token_record_id"),
        ("retention/retention-retrieval-token-verification-receipts.json", "retention_retrieval_token_verification_receipt_id"),
        ("retention/retention-retrieval-token-closeout-records.json", "retention_retrieval_token_closeout_record_id"),
        ("retention/retention-consumer-receipt-records.json", "retention_consumer_receipt_record_id"),
        ("retention/retention-consumer-receipt-verification-receipts.json", "retention_consumer_receipt_verification_receipt_id"),
        ("retention/retention-consumer-receipt-closeout-records.json", "retention_consumer_receipt_closeout_record_id"),
        ("retention/retention-publication-rollup-records.json", "retention_publication_rollup_record_id"),
        ("retention/retention-publication-rollup-verification-receipts.json", "retention_publication_rollup_verification_receipt_id"),
        ("retention/retention-publication-rollup-closeout-records.json", "retention_publication_rollup_closeout_record_id"),
        ("retention/retention-distribution-receipt-records.json", "retention_distribution_receipt_record_id"),
        ("retention/retention-distribution-receipt-verification-receipts.json", "retention_distribution_receipt_verification_receipt_id"),
        ("retention/retention-distribution-receipt-closeout-records.json", "retention_distribution_receipt_closeout_record_id"),
        ("retention/retention-access-audit-snapshot-records.json", "retention_access_audit_snapshot_record_id"),
        ("retention/retention-access-audit-snapshot-verification-receipts.json", "retention_access_audit_snapshot_verification_receipt_id"),
        ("retention/retention-access-audit-snapshot-closeout-records.json", "retention_access_audit_snapshot_closeout_record_id"),
        ("retention/retention-release-health-snapshot-records.json", "retention_release_health_snapshot_record_id"),
        ("retention/retention-release-health-snapshot-verification-receipts.json", "retention_release_health_snapshot_verification_receipt_id"),
        ("retention/retention-release-health-snapshot-closeout-records.json", "retention_release_health_snapshot_closeout_record_id"),
        ("retention/retention-release-usage-summary-records.json", "retention_release_usage_summary_record_id"),
        ("retention/retention-release-usage-summary-verification-receipts.json", "retention_release_usage_summary_verification_receipt_id"),
        ("retention/retention-release-usage-summary-closeout-records.json", "retention_release_usage_summary_closeout_record_id"),
        ("retention/retention-retention-exposure-report-records.json", "retention_retention_exposure_report_record_id"),
        ("retention/retention-retention-exposure-report-verification-receipts.json", "retention_retention_exposure_report_verification_receipt_id"),
        ("retention/retention-retention-exposure-report-closeout-records.json", "retention_retention_exposure_report_closeout_record_id"),
        ("retention/retention-release-closeout-summary-records.json", "retention_release_closeout_summary_record_id"),
        ("retention/retention-release-closeout-summary-verification-receipts.json", "retention_release_closeout_summary_verification_receipt_id"),
        ("retention/retention-release-closeout-summary-closeout-records.json", "retention_release_closeout_summary_closeout_record_id"),
        ("retention/retention-public-record-index-records.json", "retention_public_record_index_record_id"),
        ("retention/retention-public-record-index-verification-receipts.json", "retention_public_record_index_verification_receipt_id"),
        ("retention/retention-public-record-index-closeout-records.json", "retention_public_record_index_closeout_record_id"),
        ("retention/retention-final-release-bundle-records.json", "retention_final_release_bundle_record_id"),
        ("retention/retention-final-release-bundle-verification-receipts.json", "retention_final_release_bundle_verification_receipt_id"),
        ("retention/retention-final-release-bundle-closeout-records.json", "retention_final_release_bundle_closeout_record_id"),
        ("retention/retention-terminal-access-notice-records.json", "retention_terminal_access_notice_record_id"),
        ("retention/retention-terminal-access-notice-verification-receipts.json", "retention_terminal_access_notice_verification_receipt_id"),
        ("retention/retention-terminal-access-notice-closeout-records.json", "retention_terminal_access_notice_closeout_record_id"),
        ("retention/retention-release-acceptance-records.json", "retention_release_acceptance_record_id"),
        ("retention/retention-release-acceptance-verification-receipts.json", "retention_release_acceptance_verification_receipt_id"),
        ("retention/retention-release-acceptance-closeout-records.json", "retention_release_acceptance_closeout_record_id"),
        ("retention/retention-access-completion-records.json", "retention_access_completion_record_id"),
        ("retention/retention-access-completion-verification-receipts.json", "retention_access_completion_verification_receipt_id"),
        ("retention/retention-access-completion-closeout-records.json", "retention_access_completion_closeout_record_id"),
        ("retention/retention-publication-certificate-records.json", "retention_publication_certificate_record_id"),
        ("retention/retention-publication-certificate-verification-receipts.json", "retention_publication_certificate_verification_receipt_id"),
        ("retention/retention-publication-certificate-closeout-records.json", "retention_publication_certificate_closeout_record_id"),
        ("retention/retention-distribution-closure-notice-records.json", "retention_distribution_closure_notice_record_id"),
        ("retention/retention-distribution-closure-notice-verification-receipts.json", "retention_distribution_closure_notice_verification_receipt_id"),
        ("retention/retention-distribution-closure-notice-closeout-records.json", "retention_distribution_closure_notice_closeout_record_id"),
        ("retention/retention-public-access-register-records.json", "retention_public_access_register_record_id"),
        ("retention/retention-public-access-register-verification-receipts.json", "retention_public_access_register_verification_receipt_id"),
        ("retention/retention-public-access-register-closeout-records.json", "retention_public_access_register_closeout_record_id"),
        ("retention/retention-release-access-index-records.json", "retention_release_access_index_record_id"),
        ("retention/retention-release-access-index-verification-receipts.json", "retention_release_access_index_verification_receipt_id"),
        ("retention/retention-release-access-index-closeout-records.json", "retention_release_access_index_closeout_record_id"),
        ("retention/retention-release-access-verification-summary-records.json", "retention_release_access_verification_summary_record_id"),
        ("retention/retention-release-access-verification-summary-verification-receipts.json", "retention_release_access_verification_summary_verification_receipt_id"),
        ("retention/retention-release-access-verification-summary-closeout-records.json", "retention_release_access_verification_summary_closeout_record_id"),
        ("retention/retention-release-access-closeout-summary-records.json", "retention_release_access_closeout_summary_record_id"),
        ("retention/retention-release-access-closeout-summary-verification-receipts.json", "retention_release_access_closeout_summary_verification_receipt_id"),
        ("retention/retention-release-access-closeout-summary-closeout-records.json", "retention_release_access_closeout_summary_closeout_record_id"),
        ("retention/retention-archive-availability-rollup-records.json", "retention_archive_availability_rollup_record_id"),
        ("retention/retention-archive-availability-rollup-verification-receipts.json", "retention_archive_availability_rollup_verification_receipt_id"),
        ("retention/retention-archive-availability-rollup-closeout-records.json", "retention_archive_availability_rollup_closeout_record_id"),
        ("retention/retention-retrieval-readiness-snapshot-records.json", "retention_retrieval_readiness_snapshot_record_id"),
        ("retention/retention-retrieval-readiness-snapshot-verification-receipts.json", "retention_retrieval_readiness_snapshot_verification_receipt_id"),
        ("retention/retention-retrieval-readiness-snapshot-closeout-records.json", "retention_retrieval_readiness_snapshot_closeout_record_id"),
        ("retention/retention-consumer-availability-notice-records.json", "retention_consumer_availability_notice_record_id"),
        ("retention/retention-consumer-availability-notice-verification-receipts.json", "retention_consumer_availability_notice_verification_receipt_id"),
        ("retention/retention-consumer-availability-notice-closeout-records.json", "retention_consumer_availability_notice_closeout_record_id"),
        ("retention/retention-public-release-receipt-records.json", "retention_public_release_receipt_record_id"),
        ("retention/retention-public-release-receipt-verification-receipts.json", "retention_public_release_receipt_verification_receipt_id"),
        ("retention/retention-public-release-receipt-closeout-records.json", "retention_public_release_receipt_closeout_record_id"),
        ("retention/retention-release-exception-register-records.json", "retention_release_exception_register_record_id"),
        ("retention/retention-release-exception-register-verification-receipts.json", "retention_release_exception_register_verification_receipt_id"),
        ("retention/retention-release-exception-register-closeout-records.json", "retention_release_exception_register_closeout_record_id"),
        ("retention/retention-release-exception-summary-records.json", "retention_release_exception_summary_record_id"),
        ("retention/retention-release-exception-summary-verification-receipts.json", "retention_release_exception_summary_verification_receipt_id"),
        ("retention/retention-release-exception-summary-closeout-records.json", "retention_release_exception_summary_closeout_record_id"),
        ("retention/retention-release-metrics-snapshot-records.json", "retention_release_metrics_snapshot_record_id"),
        ("retention/retention-release-metrics-snapshot-verification-receipts.json", "retention_release_metrics_snapshot_verification_receipt_id"),
        ("retention/retention-release-metrics-snapshot-closeout-records.json", "retention_release_metrics_snapshot_closeout_record_id"),
        ("retention/retention-release-terminal-report-records.json", "retention_release_terminal_report_record_id"),
        ("retention/retention-release-terminal-report-verification-receipts.json", "retention_release_terminal_report_verification_receipt_id"),
        ("retention/retention-release-terminal-report-closeout-records.json", "retention_release_terminal_report_closeout_record_id"),
        ("retention/retention-final-publication-notice-records.json", "retention_final_publication_notice_record_id"),
        ("retention/retention-final-publication-notice-verification-receipts.json", "retention_final_publication_notice_verification_receipt_id"),
        ("transport/transport-receipts.json", "transport_receipt_id"),
    ]
    ids: set[str] = set()
    for pattern, key in patterns:
        for path in root.glob(pattern):
            for record in _load_records(path):
                if record.get(key):
                    ids.add(str(record[key]))

    for path, array_key, id_key in [
        (root / "dispatch" / "dispatch-policy.json", "rules", "dispatch_rule_id"),
        (root / "routing" / "routing-policy.json", "routes", "route_id"),
        (root / "delivery" / "delivery-channel-registry.json", "channels", "channel_id"),
        (root / "transport" / "transport-adapter-registry.json", "adapters", "transport_adapter_id"),
    ]:
        if not path.exists():
            continue
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            for item in raw.get(array_key, []):
                if isinstance(item, dict) and item.get(id_key):
                    ids.add(str(item[id_key]))

    return ids


def _collect_known_artifact_paths(root: Path) -> set[str]:
    paths: set[str] = set()
    for folder in [
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "dispatch", "routing", "delivery", "outbox",
        "inbox", "intake", "imports", "conflicts", "merge", "apply", "state", "snapshots", "recovery", "restore", "disposition", "custody", "transport", "topology", "review", "audit", "exchange",
        "reconciliation", "quality", "action", "playbooks", "integrity",
        "schemas", "contracts", "docs", "bundles",
    ]:
        base = root / folder
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                paths.add(str(path.relative_to(root)).replace("\\", "/"))
    return paths


def validate_audit_repository(root: str | Path) -> AuditReport:
    root_path = Path(root)
    audit_path = root_path / "audit" / "audit-journal.json"
    failures: list[str] = []

    if not audit_path.exists():
        return AuditReport(source=str(audit_path), failures=["missing audit journal: audit/audit-journal.json"])

    events = load_audit_events(audit_path)
    known_record_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for event in events:
        if not event.audit_id:
            failures.append("audit event missing audit_id")
            continue
        if event.audit_id in seen_ids:
            failures.append(f"duplicate audit_id {event.audit_id!r}")
        seen_ids.add(event.audit_id)

        if event.event_kind not in KNOWN_EVENT_KINDS:
            failures.append(f"audit event {event.audit_id!r} uses unknown event_kind {event.event_kind!r}")
        if not event.created_time:
            failures.append(f"audit event {event.audit_id!r} missing created_time")
        if not event.actor_ref:
            failures.append(f"audit event {event.audit_id!r} missing actor_ref")
        if not event.summary:
            failures.append(f"audit event {event.audit_id!r} missing summary")
        if not event.subject_refs:
            failures.append(f"audit event {event.audit_id!r} has no subject_refs")

        for ref in event.subject_refs:
            if ref in known_record_ids or ref in known_paths:
                continue
            failures.append(f"audit event {event.audit_id!r} references unknown subject_ref {ref!r}")

    return AuditReport(source=str(audit_path), checked_events=len(events), failures=failures)


def format_audit_report(report: AuditReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM audit source: {report.source}")
    lines.append(f"Audit events checked: {report.checked_events}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM audit validation failed.")
    else:
        lines.append("")
        lines.append("PFEM audit validation passed.")

    return "\n".join(lines)
