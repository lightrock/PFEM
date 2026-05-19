"""PFEM dispatch policy validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path

from pfem.action import load_action_policy
from pfem.delivery import collect_delivery_channel_ids
from pfem.routing import load_routing_policy
from pfem.transport import collect_transport_adapter_ids


KNOWN_JOB_KINDS = {
    "action_delivery",
    "bundle_delivery",
    "summary_delivery",
    "review_delivery",
    "exchange_delivery",
}

KNOWN_JOB_STATES = {
    "proposed",
    "queued",
    "ready",
    "in_progress",
    "completed",
    "failed",
    "cancelled",
    "blocked",
}


@dataclass(frozen=True)
class DispatchRule:
    dispatch_rule_id: str
    enabled: bool
    job_kinds: list[str]
    eligible_job_states: list[str]
    priorities: list[str]
    route_ids: list[str]
    delivery_channel_ids: list[str]
    transport_adapter_ids: list[str]
    requires_review_before_dispatch: bool
    max_attempts: int
    retry_delay_seconds: int
    on_success_job_state: str | None
    on_failure_job_state: str | None
    summary: str


@dataclass(frozen=True)
class DispatchPolicy:
    policy_id: str
    version: str
    rules: list[DispatchRule]


@dataclass(frozen=True)
class DispatchReport:
    source: str
    checked_rules: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _as_int(value: object, default: int = 0) -> int:
    if isinstance(value, int):
        return value
    try:
        return int(str(value))
    except Exception:
        return default


def load_dispatch_policy(path: str | Path) -> DispatchPolicy:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    rules: list[DispatchRule] = []

    for item in raw.get("rules", []):
        if not isinstance(item, dict):
            continue
        rules.append(
            DispatchRule(
                dispatch_rule_id=str(item.get("dispatch_rule_id", "")),
                enabled=bool(item.get("enabled", False)),
                job_kinds=_as_list(item.get("job_kinds", [])),
                eligible_job_states=_as_list(item.get("eligible_job_states", [])),
                priorities=_as_list(item.get("priorities", [])),
                route_ids=_as_list(item.get("route_ids", [])),
                delivery_channel_ids=_as_list(item.get("delivery_channel_ids", [])),
                transport_adapter_ids=_as_list(item.get("transport_adapter_ids", [])),
                requires_review_before_dispatch=bool(item.get("requires_review_before_dispatch", False)),
                max_attempts=_as_int(item.get("max_attempts", 0)),
                retry_delay_seconds=_as_int(item.get("retry_delay_seconds", 0)),
                on_success_job_state=str(item["on_success_job_state"]) if "on_success_job_state" in item else None,
                on_failure_job_state=str(item["on_failure_job_state"]) if "on_failure_job_state" in item else None,
                summary=str(item.get("summary", "")),
            )
        )

    return DispatchPolicy(
        policy_id=str(raw.get("policy_id", "")),
        version=str(raw.get("version", "")),
        rules=rules,
    )


def collect_dispatch_rule_ids(root: str | Path) -> set[str]:
    policy_path = Path(root) / "dispatch" / "dispatch-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_dispatch_policy(policy_path)
    return {rule.dispatch_rule_id for rule in policy.rules if rule.dispatch_rule_id}


def _collect_priorities(root: Path) -> set[str]:
    policy_path = root / "action" / "action-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_action_policy(policy_path)
    return {priority.priority for priority in policy.priority_levels if priority.priority}


def _collect_route_ids(root: Path) -> set[str]:
    policy_path = root / "routing" / "routing-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_routing_policy(policy_path)
    return {route.route_id for route in policy.routes if route.route_id}


def validate_dispatch_policy(root: str | Path) -> DispatchReport:
    root_path = Path(root)
    policy_path = root_path / "dispatch" / "dispatch-policy.json"
    failures: list[str] = []

    if not policy_path.exists():
        return DispatchReport(
            source=str(policy_path),
            failures=["missing dispatch policy: dispatch/dispatch-policy.json"],
        )

    policy = load_dispatch_policy(policy_path)
    if not policy.policy_id:
        failures.append("dispatch policy missing policy_id")
    if not policy.version:
        failures.append("dispatch policy missing version")
    if not policy.rules:
        failures.append("dispatch policy has no rules")

    priorities = _collect_priorities(root_path)
    route_ids = _collect_route_ids(root_path)
    delivery_channel_ids = collect_delivery_channel_ids(root_path)
    transport_adapter_ids = collect_transport_adapter_ids(root_path)
    seen_ids: set[str] = set()

    for rule in policy.rules:
        if not rule.dispatch_rule_id:
            failures.append("dispatch rule missing dispatch_rule_id")
            continue
        if rule.dispatch_rule_id in seen_ids:
            failures.append(f"duplicate dispatch_rule_id {rule.dispatch_rule_id!r}")
        seen_ids.add(rule.dispatch_rule_id)

        if not rule.job_kinds:
            failures.append(f"dispatch rule {rule.dispatch_rule_id!r} has no job_kinds")
        for job_kind in rule.job_kinds:
            if job_kind not in KNOWN_JOB_KINDS:
                failures.append(f"dispatch rule {rule.dispatch_rule_id!r} references unknown job_kind {job_kind!r}")

        if not rule.eligible_job_states:
            failures.append(f"dispatch rule {rule.dispatch_rule_id!r} has no eligible_job_states")
        for state in rule.eligible_job_states:
            if state not in KNOWN_JOB_STATES:
                failures.append(f"dispatch rule {rule.dispatch_rule_id!r} references unknown eligible job state {state!r}")

        if not rule.priorities:
            failures.append(f"dispatch rule {rule.dispatch_rule_id!r} has no priorities")
        for priority in rule.priorities:
            if priorities and priority not in priorities:
                failures.append(f"dispatch rule {rule.dispatch_rule_id!r} references unknown priority {priority!r}")

        for route_id in rule.route_ids:
            if route_ids and route_id not in route_ids:
                failures.append(f"dispatch rule {rule.dispatch_rule_id!r} references unknown route_id {route_id!r}")

        for channel_id in rule.delivery_channel_ids:
            if delivery_channel_ids and channel_id not in delivery_channel_ids:
                failures.append(f"dispatch rule {rule.dispatch_rule_id!r} references unknown delivery_channel_id {channel_id!r}")

        for adapter_id in rule.transport_adapter_ids:
            if transport_adapter_ids and adapter_id not in transport_adapter_ids:
                failures.append(f"dispatch rule {rule.dispatch_rule_id!r} references unknown transport_adapter_id {adapter_id!r}")

        if rule.max_attempts < 1:
            failures.append(f"dispatch rule {rule.dispatch_rule_id!r} max_attempts must be at least 1")
        if rule.retry_delay_seconds < 0:
            failures.append(f"dispatch rule {rule.dispatch_rule_id!r} retry_delay_seconds cannot be negative")
        if rule.on_success_job_state and rule.on_success_job_state not in KNOWN_JOB_STATES:
            failures.append(f"dispatch rule {rule.dispatch_rule_id!r} has unknown on_success_job_state {rule.on_success_job_state!r}")
        if rule.on_failure_job_state and rule.on_failure_job_state not in KNOWN_JOB_STATES:
            failures.append(f"dispatch rule {rule.dispatch_rule_id!r} has unknown on_failure_job_state {rule.on_failure_job_state!r}")
        if not rule.summary:
            failures.append(f"dispatch rule {rule.dispatch_rule_id!r} missing summary")

    return DispatchReport(
        source=str(policy_path),
        checked_rules=len(policy.rules),
        failures=failures,
    )


def format_dispatch_report(report: DispatchReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM dispatch source: {report.source}")
    lines.append(f"Dispatch rules checked: {report.checked_rules}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM dispatch validation failed.")
    else:
        lines.append("")
        lines.append("PFEM dispatch validation passed.")

    return "\n".join(lines)
