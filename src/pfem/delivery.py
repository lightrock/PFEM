"""PFEM delivery channel registry validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.handling import load_handling_policy
from pfem.node_runtime import collect_node_ids
from pfem.policy import load_sharing_policy, known_scope_ids


JsonObject = dict[str, Any]

KNOWN_CHANNEL_KINDS = {
    "manual_export",
    "file_drop",
    "api",
    "mqtt",
    "email",
    "mesh_message",
    "dashboard_sync",
}

KNOWN_CHANNEL_STATUSES = {
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
class DeliveryChannel:
    channel_id: str
    channel_kind: str
    status: str
    supports_route_kinds: list[str]
    source_node_ids: list[str]
    destination_node_ids: list[str]
    allowed_sharing_scopes: list[str]
    allowed_handling_labels: list[str]
    summary: str


@dataclass(frozen=True)
class DeliveryChannelRegistry:
    registry_id: str
    version: str
    channels: list[DeliveryChannel]


@dataclass(frozen=True)
class DeliveryReport:
    source: str
    checked_channels: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def load_delivery_channel_registry(path: str | Path) -> DeliveryChannelRegistry:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    channels: list[DeliveryChannel] = []
    for item in raw.get("channels", []):
        if not isinstance(item, dict):
            continue
        channels.append(
            DeliveryChannel(
                channel_id=str(item.get("channel_id", "")),
                channel_kind=str(item.get("channel_kind", "")),
                status=str(item.get("status", "")),
                supports_route_kinds=_as_list(item.get("supports_route_kinds", [])),
                source_node_ids=_as_list(item.get("source_node_ids", [])),
                destination_node_ids=_as_list(item.get("destination_node_ids", [])),
                allowed_sharing_scopes=_as_list(item.get("allowed_sharing_scopes", [])),
                allowed_handling_labels=_as_list(item.get("allowed_handling_labels", [])),
                summary=str(item.get("summary", "")),
            )
        )
    return DeliveryChannelRegistry(
        registry_id=str(raw.get("registry_id", "")),
        version=str(raw.get("version", "")),
        channels=channels,
    )


def collect_delivery_channel_ids(root: str | Path) -> set[str]:
    registry_path = Path(root) / "delivery" / "delivery-channel-registry.json"
    if not registry_path.exists():
        return set()
    registry = load_delivery_channel_registry(registry_path)
    return {channel.channel_id for channel in registry.channels if channel.channel_id}


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


def validate_delivery_channel_registry(root: str | Path) -> DeliveryReport:
    root_path = Path(root)
    registry_path = root_path / "delivery" / "delivery-channel-registry.json"
    failures: list[str] = []

    if not registry_path.exists():
        return DeliveryReport(
            source=str(registry_path),
            failures=["missing delivery channel registry: delivery/delivery-channel-registry.json"],
        )

    registry = load_delivery_channel_registry(registry_path)

    if not registry.registry_id:
        failures.append("delivery channel registry missing registry_id")
    if not registry.version:
        failures.append("delivery channel registry missing version")
    if not registry.channels:
        failures.append("delivery channel registry has no channels")

    node_ids = collect_node_ids(root_path)
    sharing_scopes = _collect_sharing_scopes(root_path)
    handling_labels = _collect_handling_labels(root_path)
    seen_channel_ids: set[str] = set()

    for channel in registry.channels:
        if not channel.channel_id:
            failures.append("delivery channel missing channel_id")
            continue
        if channel.channel_id in seen_channel_ids:
            failures.append(f"duplicate delivery channel_id {channel.channel_id!r}")
        seen_channel_ids.add(channel.channel_id)

        if channel.channel_kind not in KNOWN_CHANNEL_KINDS:
            failures.append(f"delivery channel {channel.channel_id!r} uses unknown channel_kind {channel.channel_kind!r}")
        if channel.status not in KNOWN_CHANNEL_STATUSES:
            failures.append(f"delivery channel {channel.channel_id!r} uses unknown status {channel.status!r}")
        if not channel.supports_route_kinds:
            failures.append(f"delivery channel {channel.channel_id!r} has no supports_route_kinds")
        for route_kind in channel.supports_route_kinds:
            if route_kind not in KNOWN_ROUTE_KINDS:
                failures.append(f"delivery channel {channel.channel_id!r} references unknown route_kind {route_kind!r}")

        for node_id in channel.source_node_ids:
            if node_ids and node_id not in node_ids:
                failures.append(f"delivery channel {channel.channel_id!r} references unknown source_node_id {node_id!r}")
        for node_id in channel.destination_node_ids:
            if node_ids and node_id not in node_ids:
                failures.append(f"delivery channel {channel.channel_id!r} references unknown destination_node_id {node_id!r}")

        for scope in channel.allowed_sharing_scopes:
            if sharing_scopes and scope not in sharing_scopes:
                failures.append(f"delivery channel {channel.channel_id!r} references unknown sharing_scope {scope!r}")
        for label in channel.allowed_handling_labels:
            if handling_labels and label not in handling_labels:
                failures.append(f"delivery channel {channel.channel_id!r} references unknown handling_label {label!r}")

        if not channel.summary:
            failures.append(f"delivery channel {channel.channel_id!r} missing summary")

    return DeliveryReport(
        source=str(registry_path),
        checked_channels=len(registry.channels),
        failures=failures,
    )


def format_delivery_report(report: DeliveryReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM delivery source: {report.source}")
    lines.append(f"Delivery channels checked: {report.checked_channels}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM delivery validation failed.")
    else:
        lines.append("")
        lines.append("PFEM delivery validation passed.")

    return "\n".join(lines)
