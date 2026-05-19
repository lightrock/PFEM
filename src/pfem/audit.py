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
    "intake_decision_recorded", "import_recorded", "merge_decision_recorded",
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
        ("merge/merge-decisions.json", "merge_decision_id"),
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
        "inbox", "intake", "imports", "merge", "transport", "topology", "review", "audit", "exchange",
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
