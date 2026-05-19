"""PFEM transport receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.delivery import collect_delivery_channel_ids
from pfem.delivery_job import collect_delivery_job_ids
from pfem.node_runtime import collect_node_ids
from pfem.outbox import collect_outbox_item_ids
from pfem.routing import load_routing_policy
from pfem.transport import collect_transport_adapter_ids


JsonObject = dict[str, Any]

KNOWN_RECEIPT_KINDS = {
    "delivery_attempt",
    "delivery_result",
    "delivery_acknowledgement",
}

KNOWN_TRANSPORT_STATES = {
    "queued",
    "attempted",
    "sent",
    "received",
    "succeeded",
    "failed",
    "cancelled",
    "unknown",
}


@dataclass(frozen=True)
class TransportReceipt:
    transport_receipt_id: str
    receipt_kind: str
    created_time: str
    delivery_job_id: str
    outbox_item_id: str
    transport_adapter_id: str
    delivery_channel_id: str
    route_id: str
    source_node_id: str
    destination_node_id: str
    subject_refs: list[str]
    basis_refs: list[str]
    transport_state: str
    artifact_refs: list[str]
    outcome_summary: str


@dataclass(frozen=True)
class TransportReceiptReport:
    source: str
    checked_receipts: int = 0
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


def load_transport_receipts(path: str | Path) -> list[TransportReceipt]:
    return [
        TransportReceipt(
            transport_receipt_id=str(record.get("transport_receipt_id", "")),
            receipt_kind=str(record.get("receipt_kind", "")),
            created_time=str(record.get("created_time", "")),
            delivery_job_id=str(record.get("delivery_job_id", "")),
            outbox_item_id=str(record.get("outbox_item_id", "")),
            transport_adapter_id=str(record.get("transport_adapter_id", "")),
            delivery_channel_id=str(record.get("delivery_channel_id", "")),
            route_id=str(record.get("route_id", "")),
            source_node_id=str(record.get("source_node_id", "")),
            destination_node_id=str(record.get("destination_node_id", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            transport_state=str(record.get("transport_state", "")),
            artifact_refs=_as_list(record.get("artifact_refs", [])),
            outcome_summary=str(record.get("outcome_summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_transport_receipt_ids(root: str | Path) -> set[str]:
    receipts_path = Path(root) / "transport" / "transport-receipts.json"
    if not receipts_path.exists():
        return set()
    return {
        receipt.transport_receipt_id
        for receipt in load_transport_receipts(receipts_path)
        if receipt.transport_receipt_id
    }


def _collect_route_ids(root: Path) -> set[str]:
    policy_path = root / "routing" / "routing-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_routing_policy(policy_path)
    return {route.route_id for route in policy.routes if route.route_id}


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


def validate_transport_receipts(root: str | Path) -> TransportReceiptReport:
    root_path = Path(root)
    receipts_path = root_path / "transport" / "transport-receipts.json"
    failures: list[str] = []

    if not receipts_path.exists():
        return TransportReceiptReport(
            source=str(receipts_path),
            failures=["missing transport receipts: transport/transport-receipts.json"],
        )

    receipts = load_transport_receipts(receipts_path)
    if not receipts:
        failures.append("transport receipts file has no receipts")

    delivery_job_ids = collect_delivery_job_ids(root_path)
    outbox_item_ids = collect_outbox_item_ids(root_path)
    transport_adapter_ids = collect_transport_adapter_ids(root_path)
    delivery_channel_ids = collect_delivery_channel_ids(root_path)
    route_ids = _collect_route_ids(root_path)
    node_ids = collect_node_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for receipt in receipts:
        if not receipt.transport_receipt_id:
            failures.append("transport receipt missing transport_receipt_id")
            continue
        if receipt.transport_receipt_id in seen_ids:
            failures.append(f"duplicate transport_receipt_id {receipt.transport_receipt_id!r}")
        seen_ids.add(receipt.transport_receipt_id)

        if receipt.receipt_kind not in KNOWN_RECEIPT_KINDS:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}")
        if not receipt.created_time:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} missing created_time")
        if delivery_job_ids and receipt.delivery_job_id not in delivery_job_ids:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown delivery_job_id {receipt.delivery_job_id!r}")
        if outbox_item_ids and receipt.outbox_item_id not in outbox_item_ids:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown outbox_item_id {receipt.outbox_item_id!r}")
        if transport_adapter_ids and receipt.transport_adapter_id not in transport_adapter_ids:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown transport_adapter_id {receipt.transport_adapter_id!r}")
        if delivery_channel_ids and receipt.delivery_channel_id not in delivery_channel_ids:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown delivery_channel_id {receipt.delivery_channel_id!r}")
        if route_ids and receipt.route_id not in route_ids:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown route_id {receipt.route_id!r}")
        if node_ids and receipt.source_node_id not in node_ids:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown source_node_id {receipt.source_node_id!r}")
        if node_ids and receipt.destination_node_id not in node_ids:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown destination_node_id {receipt.destination_node_id!r}")
        if not receipt.subject_refs:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} has no subject_refs")
        for ref in receipt.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown subject_ref {ref!r}")
        if not receipt.basis_refs:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} has no basis_refs")
        for ref in receipt.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown basis_ref {ref!r}")
        if receipt.transport_state not in KNOWN_TRANSPORT_STATES:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} uses unknown transport_state {receipt.transport_state!r}")
        for ref in receipt.artifact_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"transport receipt {receipt.transport_receipt_id!r} references unknown artifact_ref {ref!r}")
        if not receipt.outcome_summary:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} missing outcome_summary")

    return TransportReceiptReport(source=str(receipts_path), checked_receipts=len(receipts), failures=failures)


def format_transport_receipt_report(report: TransportReceiptReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM transport receipt source: {report.source}")
    lines.append(f"Transport receipts checked: {report.checked_receipts}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM transport receipt validation failed.")
    else:
        lines.append("")
        lines.append("PFEM transport receipt validation passed.")

    return "\n".join(lines)
