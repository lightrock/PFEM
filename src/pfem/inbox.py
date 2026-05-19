"""PFEM inbox item validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.outbox import collect_outbox_item_ids
from pfem.transport_receipt import collect_transport_receipt_ids


JsonObject = dict[str, Any]

KNOWN_ITEM_KINDS = {
    "exchange_bundle",
    "evidence_package",
    "rollup_summary",
    "federation_message",
    "report",
    "operator_message",
}

KNOWN_INBOX_STATES = {
    "received",
    "quarantined",
    "ready_for_exchange",
    "accepted_for_exchange",
    "rejected",
    "expired",
    "failed",
}


@dataclass(frozen=True)
class InboxItem:
    inbox_item_id: str
    item_kind: str
    created_time: str
    transport_receipt_id: str
    outbox_item_id: str | None
    source_node_id: str
    destination_node_id: str
    subject_refs: list[str]
    artifact_refs: list[str]
    basis_refs: list[str]
    inbox_state: str
    received_by_ref: str
    summary: str


@dataclass(frozen=True)
class InboxReport:
    source: str
    checked_items: int = 0
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


def load_inbox_items(path: str | Path) -> list[InboxItem]:
    return [
        InboxItem(
            inbox_item_id=str(record.get("inbox_item_id", "")),
            item_kind=str(record.get("item_kind", "")),
            created_time=str(record.get("created_time", "")),
            transport_receipt_id=str(record.get("transport_receipt_id", "")),
            outbox_item_id=str(record["outbox_item_id"]) if "outbox_item_id" in record else None,
            source_node_id=str(record.get("source_node_id", "")),
            destination_node_id=str(record.get("destination_node_id", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            artifact_refs=_as_list(record.get("artifact_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            inbox_state=str(record.get("inbox_state", "")),
            received_by_ref=str(record.get("received_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_inbox_item_ids(root: str | Path) -> set[str]:
    inbox_path = Path(root) / "inbox" / "inbox-items.json"
    if not inbox_path.exists():
        return set()
    return {item.inbox_item_id for item in load_inbox_items(inbox_path) if item.inbox_item_id}


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
    folders = [
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "dispatch", "routing", "delivery", "outbox",
        "inbox", "transport", "topology", "review", "audit", "exchange",
        "reconciliation", "quality", "action", "playbooks", "integrity",
        "schemas", "contracts", "docs", "bundles", "tests",
    ]
    paths: set[str] = set()
    for folder in folders:
        base = root / folder
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file():
                paths.add(str(path.relative_to(root)).replace("\\", "/"))
    return paths


def _known_ref(ref: str, known_ids: set[str], known_paths: set[str]) -> bool:
    return ref in known_ids or ref.replace("\\", "/") in known_paths


def validate_inbox_items(root: str | Path) -> InboxReport:
    root_path = Path(root)
    inbox_path = root_path / "inbox" / "inbox-items.json"
    failures: list[str] = []

    if not inbox_path.exists():
        return InboxReport(source=str(inbox_path), failures=["missing inbox items: inbox/inbox-items.json"])

    items = load_inbox_items(inbox_path)
    if not items:
        failures.append("inbox items file has no items")

    transport_receipt_ids = collect_transport_receipt_ids(root_path)
    outbox_item_ids = collect_outbox_item_ids(root_path)
    node_ids = collect_node_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for item in items:
        if not item.inbox_item_id:
            failures.append("inbox item missing inbox_item_id")
            continue
        if item.inbox_item_id in seen_ids:
            failures.append(f"duplicate inbox_item_id {item.inbox_item_id!r}")
        seen_ids.add(item.inbox_item_id)

        if item.item_kind not in KNOWN_ITEM_KINDS:
            failures.append(f"inbox item {item.inbox_item_id!r} uses unknown item_kind {item.item_kind!r}")
        if not item.created_time:
            failures.append(f"inbox item {item.inbox_item_id!r} missing created_time")
        if transport_receipt_ids and item.transport_receipt_id not in transport_receipt_ids:
            failures.append(f"inbox item {item.inbox_item_id!r} references unknown transport_receipt_id {item.transport_receipt_id!r}")
        if item.outbox_item_id and outbox_item_ids and item.outbox_item_id not in outbox_item_ids:
            failures.append(f"inbox item {item.inbox_item_id!r} references unknown outbox_item_id {item.outbox_item_id!r}")
        if node_ids and item.source_node_id not in node_ids:
            failures.append(f"inbox item {item.inbox_item_id!r} references unknown source_node_id {item.source_node_id!r}")
        if node_ids and item.destination_node_id not in node_ids:
            failures.append(f"inbox item {item.inbox_item_id!r} references unknown destination_node_id {item.destination_node_id!r}")
        if item.inbox_state not in KNOWN_INBOX_STATES:
            failures.append(f"inbox item {item.inbox_item_id!r} uses unknown inbox_state {item.inbox_state!r}")
        if not item.received_by_ref:
            failures.append(f"inbox item {item.inbox_item_id!r} missing received_by_ref")
        if not item.subject_refs:
            failures.append(f"inbox item {item.inbox_item_id!r} has no subject_refs")
        for ref in item.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"inbox item {item.inbox_item_id!r} references unknown subject_ref {ref!r}")
        if not item.artifact_refs:
            failures.append(f"inbox item {item.inbox_item_id!r} has no artifact_refs")
        for ref in item.artifact_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"inbox item {item.inbox_item_id!r} references unknown artifact_ref {ref!r}")
        if not item.basis_refs:
            failures.append(f"inbox item {item.inbox_item_id!r} has no basis_refs")
        for ref in item.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"inbox item {item.inbox_item_id!r} references unknown basis_ref {ref!r}")
        if not item.summary:
            failures.append(f"inbox item {item.inbox_item_id!r} missing summary")

    return InboxReport(source=str(inbox_path), checked_items=len(items), failures=failures)


def format_inbox_report(report: InboxReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM inbox source: {report.source}")
    lines.append(f"Inbox items checked: {report.checked_items}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM inbox validation failed.")
    else:
        lines.append("")
        lines.append("PFEM inbox validation passed.")

    return "\n".join(lines)
