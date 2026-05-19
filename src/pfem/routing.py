"""PFEM routing policy validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.action import load_action_policy
from pfem.bundle import load_exchange_bundle
from pfem.delivery import collect_delivery_channel_ids
from pfem.handling import load_handling_policy
from pfem.node_runtime import collect_node_ids
from pfem.policy import load_sharing_policy, known_scope_ids
from pfem.profile_runtime import load_profile_registry


JsonObject = dict[str, Any]

KNOWN_ROUTE_KINDS = {"action", "bundle", "summary", "review", "exchange"}


@dataclass(frozen=True)
class Route:
    route_id: str
    route_kind: str
    enabled: bool
    source_node_ids: list[str]
    source_profile_ids: list[str]
    destination_node_ids: list[str]
    destination_profile_ids: list[str]
    applies_to_action_kinds: list[str]
    applies_to_bundle_kinds: list[str]
    applies_to_priorities: list[str]
    applies_to_sharing_scopes: list[str]
    allowed_handling_labels: list[str]
    allowed_delivery_channel_ids: list[str]
    summary: str


@dataclass(frozen=True)
class RoutingPolicy:
    policy_id: str
    version: str
    routes: list[Route]


@dataclass(frozen=True)
class RoutingReport:
    source: str
    checked_routes: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def load_routing_policy(path: str | Path) -> RoutingPolicy:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    routes: list[Route] = []
    for item in raw.get("routes", []):
        if not isinstance(item, dict):
            continue
        routes.append(
            Route(
                route_id=str(item.get("route_id", "")),
                route_kind=str(item.get("route_kind", "")),
                enabled=bool(item.get("enabled", False)),
                source_node_ids=_as_list(item.get("source_node_ids", [])),
                source_profile_ids=_as_list(item.get("source_profile_ids", [])),
                destination_node_ids=_as_list(item.get("destination_node_ids", [])),
                destination_profile_ids=_as_list(item.get("destination_profile_ids", [])),
                applies_to_action_kinds=_as_list(item.get("applies_to_action_kinds", [])),
                applies_to_bundle_kinds=_as_list(item.get("applies_to_bundle_kinds", [])),
                applies_to_priorities=_as_list(item.get("applies_to_priorities", [])),
                applies_to_sharing_scopes=_as_list(item.get("applies_to_sharing_scopes", [])),
                allowed_handling_labels=_as_list(item.get("allowed_handling_labels", [])),
                allowed_delivery_channel_ids=_as_list(item.get("allowed_delivery_channel_ids", [])),
                summary=str(item.get("summary", "")),
            )
        )
    return RoutingPolicy(
        policy_id=str(raw.get("policy_id", "")),
        version=str(raw.get("version", "")),
        routes=routes,
    )


def _collect_profile_ids(root: Path) -> set[str]:
    registry_path = root / "profiles" / "profile-registry.json"
    if not registry_path.exists():
        return set()
    registry = load_profile_registry(registry_path)
    return {profile.profile_id for profile in registry.profiles if profile.profile_id}


def _collect_action_kinds(root: Path) -> set[str]:
    policy_path = root / "action" / "action-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_action_policy(policy_path)
    return {kind.action_kind for kind in policy.action_kinds if kind.action_kind}


def _collect_priorities(root: Path) -> set[str]:
    policy_path = root / "action" / "action-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_action_policy(policy_path)
    return {priority.priority for priority in policy.priority_levels if priority.priority}


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


def _collect_bundle_kinds(root: Path) -> set[str]:
    kinds: set[str] = set()
    for path in root.glob("bundles/**/*.bundle.json"):
        try:
            bundle = load_exchange_bundle(path)
        except Exception:
            continue
        if bundle.bundle_kind:
            kinds.add(bundle.bundle_kind)
    return kinds


def validate_routing_policy(root: str | Path) -> RoutingReport:
    root_path = Path(root)
    policy_path = root_path / "routing" / "routing-policy.json"
    failures: list[str] = []

    if not policy_path.exists():
        return RoutingReport(
            source=str(policy_path),
            failures=["missing routing policy: routing/routing-policy.json"],
        )

    policy = load_routing_policy(policy_path)

    if not policy.policy_id:
        failures.append("routing policy missing policy_id")
    if not policy.version:
        failures.append("routing policy missing version")
    if not policy.routes:
        failures.append("routing policy has no routes")

    node_ids = collect_node_ids(root_path)
    profile_ids = _collect_profile_ids(root_path)
    action_kinds = _collect_action_kinds(root_path)
    priorities = _collect_priorities(root_path)
    sharing_scopes = _collect_sharing_scopes(root_path)
    handling_labels = _collect_handling_labels(root_path)
    bundle_kinds = _collect_bundle_kinds(root_path)
    delivery_channel_ids = collect_delivery_channel_ids(root_path)

    seen_route_ids: set[str] = set()

    for route in policy.routes:
        if not route.route_id:
            failures.append("route missing route_id")
            continue
        if route.route_id in seen_route_ids:
            failures.append(f"duplicate route_id {route.route_id!r}")
        seen_route_ids.add(route.route_id)

        if route.route_kind not in KNOWN_ROUTE_KINDS:
            failures.append(f"route {route.route_id!r} uses unknown route_kind {route.route_kind!r}")
        if not route.summary:
            failures.append(f"route {route.route_id!r} missing summary")

        if not route.destination_node_ids and not route.destination_profile_ids:
            failures.append(f"route {route.route_id!r} has no destination_node_ids or destination_profile_ids")

        for node_id in route.source_node_ids:
            if node_ids and node_id not in node_ids:
                failures.append(f"route {route.route_id!r} references unknown source_node_id {node_id!r}")
        for node_id in route.destination_node_ids:
            if node_ids and node_id not in node_ids:
                failures.append(f"route {route.route_id!r} references unknown destination_node_id {node_id!r}")

        for profile_id in route.source_profile_ids:
            if profile_ids and profile_id not in profile_ids:
                failures.append(f"route {route.route_id!r} references unknown source_profile_id {profile_id!r}")
        for profile_id in route.destination_profile_ids:
            if profile_ids and profile_id not in profile_ids:
                failures.append(f"route {route.route_id!r} references unknown destination_profile_id {profile_id!r}")

        for action_kind in route.applies_to_action_kinds:
            if action_kinds and action_kind not in action_kinds:
                failures.append(f"route {route.route_id!r} references unknown action_kind {action_kind!r}")

        for priority in route.applies_to_priorities:
            if priorities and priority not in priorities:
                failures.append(f"route {route.route_id!r} references unknown priority {priority!r}")

        for scope in route.applies_to_sharing_scopes:
            if sharing_scopes and scope not in sharing_scopes:
                failures.append(f"route {route.route_id!r} references unknown sharing_scope {scope!r}")

        for label in route.allowed_handling_labels:
            if handling_labels and label not in handling_labels:
                failures.append(f"route {route.route_id!r} references unknown handling_label {label!r}")

        for bundle_kind in route.applies_to_bundle_kinds:
            if bundle_kinds and bundle_kind not in bundle_kinds:
                failures.append(f"route {route.route_id!r} references unknown bundle_kind {bundle_kind!r}")

        for channel_id in route.allowed_delivery_channel_ids:
            if delivery_channel_ids and channel_id not in delivery_channel_ids:
                failures.append(f"route {route.route_id!r} references unknown delivery channel {channel_id!r}")

    return RoutingReport(
        source=str(policy_path),
        checked_routes=len(policy.routes),
        failures=failures,
    )


def format_routing_report(report: RoutingReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM routing source: {report.source}")
    lines.append(f"Routes checked: {report.checked_routes}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM routing validation failed.")
    else:
        lines.append("")
        lines.append("PFEM routing validation passed.")

    return "\n".join(lines)
