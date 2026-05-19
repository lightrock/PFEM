"""PFEM transport receipt validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.delivery import collect_delivery_channel_ids
from pfem.node_runtime import collect_node_ids
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
        ("transport/transport-receipts.json", "transport_receipt_id"),
    ]
    ids: set[str] = set()
    for pattern, key in patterns:
        for path in root.glob(pattern):
            for record in _load_records(path):
                if record.get(key):
                    ids.add(str(record[key]))

    routing_path = root / "routing" / "routing-policy.json"
    if routing_path.exists():
        raw = json.loads(routing_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            for route in raw.get("routes", []):
                if isinstance(route, dict) and route.get("route_id"):
                    ids.add(str(route["route_id"]))

    delivery_path = root / "delivery" / "delivery-channel-registry.json"
    if delivery_path.exists():
        raw = json.loads(delivery_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            for channel in raw.get("channels", []):
                if isinstance(channel, dict) and channel.get("channel_id"):
                    ids.add(str(channel["channel_id"]))

    transport_path = root / "transport" / "transport-adapter-registry.json"
    if transport_path.exists():
        raw = json.loads(transport_path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            for adapter in raw.get("adapters", []):
                if isinstance(adapter, dict) and adapter.get("transport_adapter_id"):
                    ids.add(str(adapter["transport_adapter_id"]))

    return ids


def _collect_known_artifact_paths(root: Path) -> set[str]:
    folders = [
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "routing", "delivery", "transport", "topology",
        "review", "audit", "exchange", "reconciliation", "quality", "action",
        "playbooks", "integrity", "schemas", "contracts", "docs", "bundles",
        "tests",
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
            failures.append(
                f"transport receipt {receipt.transport_receipt_id!r} uses unknown receipt_kind {receipt.receipt_kind!r}"
            )
        if not receipt.created_time:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} missing created_time")
        if transport_adapter_ids and receipt.transport_adapter_id not in transport_adapter_ids:
            failures.append(
                f"transport receipt {receipt.transport_receipt_id!r} references unknown transport_adapter_id {receipt.transport_adapter_id!r}"
            )
        if delivery_channel_ids and receipt.delivery_channel_id not in delivery_channel_ids:
            failures.append(
                f"transport receipt {receipt.transport_receipt_id!r} references unknown delivery_channel_id {receipt.delivery_channel_id!r}"
            )
        if route_ids and receipt.route_id not in route_ids:
            failures.append(
                f"transport receipt {receipt.transport_receipt_id!r} references unknown route_id {receipt.route_id!r}"
            )
        if node_ids and receipt.source_node_id not in node_ids:
            failures.append(
                f"transport receipt {receipt.transport_receipt_id!r} references unknown source_node_id {receipt.source_node_id!r}"
            )
        if node_ids and receipt.destination_node_id not in node_ids:
            failures.append(
                f"transport receipt {receipt.transport_receipt_id!r} references unknown destination_node_id {receipt.destination_node_id!r}"
            )
        if not receipt.subject_refs:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} has no subject_refs")
        for ref in receipt.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(
                    f"transport receipt {receipt.transport_receipt_id!r} references unknown subject_ref {ref!r}"
                )
        if not receipt.basis_refs:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} has no basis_refs")
        for ref in receipt.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(
                    f"transport receipt {receipt.transport_receipt_id!r} references unknown basis_ref {ref!r}"
                )
        if receipt.transport_state not in KNOWN_TRANSPORT_STATES:
            failures.append(
                f"transport receipt {receipt.transport_receipt_id!r} uses unknown transport_state {receipt.transport_state!r}"
            )
        for ref in receipt.artifact_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(
                    f"transport receipt {receipt.transport_receipt_id!r} references unknown artifact_ref {ref!r}"
                )
        if not receipt.outcome_summary:
            failures.append(f"transport receipt {receipt.transport_receipt_id!r} missing outcome_summary")

    return TransportReceiptReport(
        source=str(receipts_path),
        checked_receipts=len(receipts),
        failures=failures,
    )


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
