"""PFEM transport adapter registry validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from pfem.delivery import collect_delivery_channel_ids
from pfem.handling import load_handling_policy
from pfem.node_runtime import collect_node_ids
from pfem.policy import load_sharing_policy, known_scope_ids


KNOWN_TRANSPORT_KINDS = {
    "manual_export",
    "file_drop",
    "api",
    "mqtt",
    "email",
    "mesh_message",
    "dashboard_sync",
}

KNOWN_TRANSPORT_STATUSES = {
    "available",
    "planned",
    "disabled",
    "deprecated",
}

KNOWN_ROUTE_KINDS = {
    "action",
    "bundle",
    "summary",
    "review",
    "exchange",
}


@dataclass(frozen=True)
class TransportAdapter:
    transport_adapter_id: str
    transport_kind: str
    status: str
    delivery_channel_ids: list[str]
    implementation_ref: str
    source_node_ids: list[str]
    destination_node_ids: list[str]
    supported_route_kinds: list[str]
    allowed_sharing_scopes: list[str]
    allowed_handling_labels: list[str]
    summary: str


@dataclass(frozen=True)
class TransportAdapterRegistry:
    registry_id: str
    version: str
    adapters: list[TransportAdapter]


@dataclass(frozen=True)
class TransportReport:
    source: str
    checked_adapters: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def load_transport_adapter_registry(path: str | Path) -> TransportAdapterRegistry:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    adapters: list[TransportAdapter] = []

    for item in raw.get("adapters", []):
        if not isinstance(item, dict):
            continue
        adapters.append(
            TransportAdapter(
                transport_adapter_id=str(item.get("transport_adapter_id", "")),
                transport_kind=str(item.get("transport_kind", "")),
                status=str(item.get("status", "")),
                delivery_channel_ids=_as_list(item.get("delivery_channel_ids", [])),
                implementation_ref=str(item.get("implementation_ref", "")),
                source_node_ids=_as_list(item.get("source_node_ids", [])),
                destination_node_ids=_as_list(item.get("destination_node_ids", [])),
                supported_route_kinds=_as_list(item.get("supported_route_kinds", [])),
                allowed_sharing_scopes=_as_list(item.get("allowed_sharing_scopes", [])),
                allowed_handling_labels=_as_list(item.get("allowed_handling_labels", [])),
                summary=str(item.get("summary", "")),
            )
        )

    return TransportAdapterRegistry(
        registry_id=str(raw.get("registry_id", "")),
        version=str(raw.get("version", "")),
        adapters=adapters,
    )


def collect_transport_adapter_ids(root: str | Path) -> set[str]:
    registry_path = Path(root) / "transport" / "transport-adapter-registry.json"
    if not registry_path.exists():
        return set()
    registry = load_transport_adapter_registry(registry_path)
    return {adapter.transport_adapter_id for adapter in registry.adapters if adapter.transport_adapter_id}


def _collect_sharing_scopes(root: Path) -> set[str]:
    policy_path = root / "policy" / "sharing-policy.json"
    if not policy_path.exists():
        return set()
    return known_scope_ids(load_sharing_policy(policy_path))


def _collect_handling_labels(root: Path) -> set[str]:
    policy_path = root / "handling" / "handling-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_handling_policy(policy_path)
    return {label.label_id for label in policy.handling_labels if label.label_id}


def validate_transport_adapter_registry(root: str | Path) -> TransportReport:
    root_path = Path(root)
    registry_path = root_path / "transport" / "transport-adapter-registry.json"
    failures: list[str] = []

    if not registry_path.exists():
        return TransportReport(
            source=str(registry_path),
            failures=["missing transport adapter registry: transport/transport-adapter-registry.json"],
        )

    registry = load_transport_adapter_registry(registry_path)

    if not registry.registry_id:
        failures.append("transport adapter registry missing registry_id")
    if not registry.version:
        failures.append("transport adapter registry missing version")
    if not registry.adapters:
        failures.append("transport adapter registry has no adapters")

    node_ids = collect_node_ids(root_path)
    delivery_channel_ids = collect_delivery_channel_ids(root_path)
    sharing_scopes = _collect_sharing_scopes(root_path)
    handling_labels = _collect_handling_labels(root_path)
    seen_ids: set[str] = set()

    for adapter in registry.adapters:
        if not adapter.transport_adapter_id:
            failures.append("transport adapter missing transport_adapter_id")
            continue
        if adapter.transport_adapter_id in seen_ids:
            failures.append(f"duplicate transport_adapter_id {adapter.transport_adapter_id!r}")
        seen_ids.add(adapter.transport_adapter_id)

        if adapter.transport_kind not in KNOWN_TRANSPORT_KINDS:
            failures.append(
                f"transport adapter {adapter.transport_adapter_id!r} uses unknown transport_kind {adapter.transport_kind!r}"
            )
        if adapter.status not in KNOWN_TRANSPORT_STATUSES:
            failures.append(
                f"transport adapter {adapter.transport_adapter_id!r} uses unknown status {adapter.status!r}"
            )
        if not adapter.delivery_channel_ids:
            failures.append(f"transport adapter {adapter.transport_adapter_id!r} has no delivery_channel_ids")
        for channel_id in adapter.delivery_channel_ids:
            if delivery_channel_ids and channel_id not in delivery_channel_ids:
                failures.append(
                    f"transport adapter {adapter.transport_adapter_id!r} references unknown delivery_channel_id {channel_id!r}"
                )

        if not adapter.implementation_ref:
            failures.append(f"transport adapter {adapter.transport_adapter_id!r} missing implementation_ref")

        if not adapter.supported_route_kinds:
            failures.append(f"transport adapter {adapter.transport_adapter_id!r} has no supported_route_kinds")
        for route_kind in adapter.supported_route_kinds:
            if route_kind not in KNOWN_ROUTE_KINDS:
                failures.append(
                    f"transport adapter {adapter.transport_adapter_id!r} references unknown route_kind {route_kind!r}"
                )

        for node_id in adapter.source_node_ids:
            if node_ids and node_id not in node_ids:
                failures.append(
                    f"transport adapter {adapter.transport_adapter_id!r} references unknown source_node_id {node_id!r}"
                )
        for node_id in adapter.destination_node_ids:
            if node_ids and node_id not in node_ids:
                failures.append(
                    f"transport adapter {adapter.transport_adapter_id!r} references unknown destination_node_id {node_id!r}"
                )

        for scope in adapter.allowed_sharing_scopes:
            if sharing_scopes and scope not in sharing_scopes:
                failures.append(
                    f"transport adapter {adapter.transport_adapter_id!r} references unknown sharing_scope {scope!r}"
                )
        for label in adapter.allowed_handling_labels:
            if handling_labels and label not in handling_labels:
                failures.append(
                    f"transport adapter {adapter.transport_adapter_id!r} references unknown handling_label {label!r}"
                )

        if not adapter.summary:
            failures.append(f"transport adapter {adapter.transport_adapter_id!r} missing summary")

    return TransportReport(
        source=str(registry_path),
        checked_adapters=len(registry.adapters),
        failures=failures,
    )


def format_transport_report(report: TransportReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM transport source: {report.source}")
    lines.append(f"Transport adapters checked: {report.checked_adapters}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM transport validation failed.")
    else:
        lines.append("")
        lines.append("PFEM transport validation passed.")

    return "\n".join(lines)
