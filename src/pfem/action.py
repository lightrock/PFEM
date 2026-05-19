"""PFEM action record validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class ActionKind:
    action_kind: str
    display_name: str
    description: str


@dataclass(frozen=True)
class PriorityLevel:
    priority: str
    rank: int
    description: str


@dataclass(frozen=True)
class ActionPolicy:
    policy_id: str
    version: str
    action_kinds: list[ActionKind]
    priority_levels: list[PriorityLevel]
    action_states: list[str]


@dataclass(frozen=True)
class ActionRecord:
    action_id: str
    action_kind: str
    created_time: str
    owner_ref: str
    subject_refs: list[str]
    basis_refs: list[str]
    priority: str
    action_state: str
    summary: str
    next_step: str
    completion_refs: list[str]


@dataclass(frozen=True)
class ActionReport:
    source: str
    checked_policy_kinds: int = 0
    checked_policy_priorities: int = 0
    checked_records: int = 0
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


def load_action_policy(path: str | Path) -> ActionPolicy:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    kinds = [
        ActionKind(
            action_kind=str(item.get("action_kind", "")),
            display_name=str(item.get("display_name", "")),
            description=str(item.get("description", "")),
        )
        for item in raw.get("action_kinds", [])
    ]
    priorities = [
        PriorityLevel(
            priority=str(item.get("priority", "")),
            rank=int(item.get("rank", 0)),
            description=str(item.get("description", "")),
        )
        for item in raw.get("priority_levels", [])
    ]
    return ActionPolicy(
        policy_id=str(raw.get("policy_id", "")),
        version=str(raw.get("version", "")),
        action_kinds=kinds,
        priority_levels=priorities,
        action_states=_as_list(raw.get("action_states", [])),
    )


def load_action_records(path: str | Path) -> list[ActionRecord]:
    return [
        ActionRecord(
            action_id=str(record.get("action_id", "")),
            action_kind=str(record.get("action_kind", "")),
            created_time=str(record.get("created_time", "")),
            owner_ref=str(record.get("owner_ref", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            priority=str(record.get("priority", "")),
            action_state=str(record.get("action_state", "")),
            summary=str(record.get("summary", "")),
            next_step=str(record.get("next_step", "")),
            completion_refs=_as_list(record.get("completion_refs", [])),
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
    ]
    ids: set[str] = set()
    for pattern, key in patterns:
        for path in root.glob(pattern):
            for record in _load_records(path):
                if record.get(key):
                    ids.add(str(record[key]))
    return ids


def _collect_known_artifact_paths(root: Path) -> set[str]:
    folders = [
        "adapters", "profiles", "nodes", "sources", "examples", "policy",
        "handling", "retention", "topology", "review", "audit", "exchange",
        "reconciliation", "quality", "action", "integrity", "schemas",
        "contracts", "docs", "tests", "bundles",
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


def validate_action_repository(root: str | Path) -> ActionReport:
    root_path = Path(root)
    policy_path = root_path / "action" / "action-policy.json"
    records_path = root_path / "action" / "action-records.json"
    failures: list[str] = []

    if not policy_path.exists():
        return ActionReport(
            source=str(policy_path),
            failures=["missing action policy: action/action-policy.json"],
        )

    if not records_path.exists():
        return ActionReport(
            source=str(records_path),
            failures=["missing action records: action/action-records.json"],
        )

    policy = load_action_policy(policy_path)
    records = load_action_records(records_path)

    if not policy.policy_id:
        failures.append("action policy missing policy_id")
    if not policy.version:
        failures.append("action policy missing version")
    if not policy.action_kinds:
        failures.append("action policy has no action_kinds")
    if not policy.priority_levels:
        failures.append("action policy has no priority_levels")
    if not policy.action_states:
        failures.append("action policy has no action_states")

    action_kinds = [item.action_kind for item in policy.action_kinds]
    priorities = [item.priority for item in policy.priority_levels]
    if len(action_kinds) != len(set(action_kinds)):
        failures.append("action policy has duplicate action_kind values")
    if len(priorities) != len(set(priorities)):
        failures.append("action policy has duplicate priority values")
    if len(policy.action_states) != len(set(policy.action_states)):
        failures.append("action policy has duplicate action_state values")

    known_kinds = {item.action_kind for item in policy.action_kinds if item.action_kind}
    known_priorities = {item.priority for item in policy.priority_levels if item.priority}
    known_states = {state for state in policy.action_states if state}

    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    node_ids = collect_node_ids(root_path)
    seen_ids: set[str] = set()

    for record in records:
        if not record.action_id:
            failures.append("action record missing action_id")
            continue
        if record.action_id in seen_ids:
            failures.append(f"duplicate action_id {record.action_id!r}")
        seen_ids.add(record.action_id)

        if record.action_kind not in known_kinds:
            failures.append(f"action {record.action_id!r} uses unknown action_kind {record.action_kind!r}")
        if record.priority not in known_priorities:
            failures.append(f"action {record.action_id!r} uses unknown priority {record.priority!r}")
        if record.action_state not in known_states:
            failures.append(f"action {record.action_id!r} uses unknown action_state {record.action_state!r}")

        if not record.created_time:
            failures.append(f"action {record.action_id!r} missing created_time")
        if not record.owner_ref:
            failures.append(f"action {record.action_id!r} missing owner_ref")
        elif node_ids and record.owner_ref not in node_ids and not _known_ref(record.owner_ref, known_ids, known_paths):
            failures.append(f"action {record.action_id!r} references unknown owner_ref {record.owner_ref!r}")

        if not record.subject_refs:
            failures.append(f"action {record.action_id!r} has no subject_refs")
        for ref in record.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"action {record.action_id!r} references unknown subject_ref {ref!r}")

        if not record.basis_refs:
            failures.append(f"action {record.action_id!r} has no basis_refs")
        for ref in record.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"action {record.action_id!r} references unknown basis_ref {ref!r}")

        for ref in record.completion_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"action {record.action_id!r} references unknown completion_ref {ref!r}")

        if not record.summary:
            failures.append(f"action {record.action_id!r} missing summary")
        if not record.next_step:
            failures.append(f"action {record.action_id!r} missing next_step")

    return ActionReport(
        source=str(root_path / "action"),
        checked_policy_kinds=len(policy.action_kinds),
        checked_policy_priorities=len(policy.priority_levels),
        checked_records=len(records),
        failures=failures,
    )


def format_action_report(report: ActionReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM action source: {report.source}")
    lines.append(f"Action kinds checked: {report.checked_policy_kinds}")
    lines.append(f"Priority levels checked: {report.checked_policy_priorities}")
    lines.append(f"Action records checked: {report.checked_records}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM action validation failed.")
    else:
        lines.append("")
        lines.append("PFEM action validation passed.")

    return "\n".join(lines)
