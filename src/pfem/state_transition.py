"""PFEM state transition validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.apply_receipt import collect_apply_receipt_ids
from pfem.import_record import collect_import_record_ids
from pfem.merge_decision import collect_merge_decision_ids
from pfem.node_runtime import collect_node_ids
from pfem.state_checkpoint import collect_state_checkpoint_ids


JsonObject = dict[str, Any]

KNOWN_TRANSITION_KINDS = {
    "apply_to_checkpoint",
    "checkpoint_superseded",
    "rollback_to_checkpoint",
    "bootstrap_checkpoint",
}

KNOWN_TRANSITION_STATES = {
    "planned",
    "completed",
    "failed",
    "partially_completed",
    "rolled_back",
}


@dataclass(frozen=True)
class StateTransition:
    state_transition_id: str
    transition_kind: str
    created_time: str
    node_id: str
    from_state_checkpoint_id: str | None
    to_state_checkpoint_id: str
    apply_receipt_ids: list[str]
    merge_decision_ids: list[str]
    import_record_ids: list[str]
    transition_state: str
    changed_refs: list[str]
    basis_refs: list[str]
    transitioned_by_ref: str
    summary: str


@dataclass(frozen=True)
class StateTransitionReport:
    source: str
    checked_transitions: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text if text else None


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


def load_state_transitions(path: str | Path) -> list[StateTransition]:
    return [
        StateTransition(
            state_transition_id=str(record.get("state_transition_id", "")),
            transition_kind=str(record.get("transition_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            from_state_checkpoint_id=_optional_str(record.get("from_state_checkpoint_id")),
            to_state_checkpoint_id=str(record.get("to_state_checkpoint_id", "")),
            apply_receipt_ids=_as_list(record.get("apply_receipt_ids", [])),
            merge_decision_ids=_as_list(record.get("merge_decision_ids", [])),
            import_record_ids=_as_list(record.get("import_record_ids", [])),
            transition_state=str(record.get("transition_state", "")),
            changed_refs=_as_list(record.get("changed_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            transitioned_by_ref=str(record.get("transitioned_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_state_transition_ids(root: str | Path) -> set[str]:
    transitions_path = Path(root) / "state" / "state-transitions.json"
    if not transitions_path.exists():
        return set()
    return {
        transition.state_transition_id
        for transition in load_state_transitions(transitions_path)
        if transition.state_transition_id
    }


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
        ("imports/import-records.json", "import_record_id"),
        ("conflicts/conflict-records.json", "conflict_record_id"),
        ("merge/merge-decisions.json", "merge_decision_id"),
        ("apply/apply-receipts.json", "apply_receipt_id"),
        ("state/state-checkpoints.json", "state_checkpoint_id"),
        ("state/state-transitions.json", "state_transition_id"),
        ("reconciliation/reconciliation-records.json", "reconciliation_id"),
        ("quality/quality-assessments.json", "quality_assessment_id"),
        ("action/action-records.json", "action_id"),
        ("playbooks/**/*.playbook.json", "playbook_id"),
        ("delivery/delivery-jobs.json", "delivery_job_id"),
        ("dispatch/dispatch-decisions.json", "dispatch_decision_id"),
        ("outbox/outbox-items.json", "outbox_item_id"),
        ("inbox/inbox-items.json", "inbox_item_id"),
        ("intake/intake-decisions.json", "intake_decision_id"),
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
        "inbox", "intake", "imports", "conflicts", "merge", "apply", "state",
        "transport", "topology", "review", "audit", "exchange", "reconciliation",
        "quality", "action", "playbooks", "integrity", "schemas", "contracts",
        "docs", "bundles", "tests",
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


def _check_id_list(
    failures: list[str],
    label: str,
    owner_id: str,
    refs: list[str],
    known: set[str],
    required: bool,
) -> None:
    if required and not refs:
        failures.append(f"state transition {owner_id!r} has no {label}")
    for ref in refs:
        if known and ref not in known:
            failures.append(f"state transition {owner_id!r} references unknown {label[:-1]} {ref!r}")


def validate_state_transitions(root: str | Path) -> StateTransitionReport:
    root_path = Path(root)
    transitions_path = root_path / "state" / "state-transitions.json"
    failures: list[str] = []

    if not transitions_path.exists():
        return StateTransitionReport(source=str(transitions_path), failures=["missing state transitions: state/state-transitions.json"])

    transitions = load_state_transitions(transitions_path)
    if not transitions:
        failures.append("state transitions file has no transitions")

    node_ids = collect_node_ids(root_path)
    checkpoint_ids = collect_state_checkpoint_ids(root_path)
    apply_receipt_ids = collect_apply_receipt_ids(root_path)
    merge_decision_ids = collect_merge_decision_ids(root_path)
    import_record_ids = collect_import_record_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for transition in transitions:
        if not transition.state_transition_id:
            failures.append("state transition missing state_transition_id")
            continue
        if transition.state_transition_id in seen_ids:
            failures.append(f"duplicate state_transition_id {transition.state_transition_id!r}")
        seen_ids.add(transition.state_transition_id)

        if transition.transition_kind not in KNOWN_TRANSITION_KINDS:
            failures.append(f"state transition {transition.state_transition_id!r} uses unknown transition_kind {transition.transition_kind!r}")
        if not transition.created_time:
            failures.append(f"state transition {transition.state_transition_id!r} missing created_time")
        if node_ids and transition.node_id not in node_ids:
            failures.append(f"state transition {transition.state_transition_id!r} references unknown node_id {transition.node_id!r}")

        if transition.from_state_checkpoint_id and checkpoint_ids and transition.from_state_checkpoint_id not in checkpoint_ids:
            failures.append(
                f"state transition {transition.state_transition_id!r} references unknown from_state_checkpoint_id {transition.from_state_checkpoint_id!r}"
            )
        if checkpoint_ids and transition.to_state_checkpoint_id not in checkpoint_ids:
            failures.append(
                f"state transition {transition.state_transition_id!r} references unknown to_state_checkpoint_id {transition.to_state_checkpoint_id!r}"
            )
        if transition.from_state_checkpoint_id and transition.from_state_checkpoint_id == transition.to_state_checkpoint_id:
            failures.append(f"state transition {transition.state_transition_id!r} cannot transition from and to the same checkpoint")

        _check_id_list(failures, "apply_receipt_ids", transition.state_transition_id, transition.apply_receipt_ids, apply_receipt_ids, True)
        _check_id_list(failures, "merge_decision_ids", transition.state_transition_id, transition.merge_decision_ids, merge_decision_ids, False)
        _check_id_list(failures, "import_record_ids", transition.state_transition_id, transition.import_record_ids, import_record_ids, False)

        if transition.transition_state not in KNOWN_TRANSITION_STATES:
            failures.append(f"state transition {transition.state_transition_id!r} uses unknown transition_state {transition.transition_state!r}")

        if not transition.changed_refs:
            failures.append(f"state transition {transition.state_transition_id!r} has no changed_refs")
        for ref in transition.changed_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"state transition {transition.state_transition_id!r} references unknown changed_ref {ref!r}")

        if not transition.basis_refs:
            failures.append(f"state transition {transition.state_transition_id!r} has no basis_refs")
        for ref in transition.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"state transition {transition.state_transition_id!r} references unknown basis_ref {ref!r}")

        if not transition.transitioned_by_ref:
            failures.append(f"state transition {transition.state_transition_id!r} missing transitioned_by_ref")
        if not transition.summary:
            failures.append(f"state transition {transition.state_transition_id!r} missing summary")

    return StateTransitionReport(source=str(transitions_path), checked_transitions=len(transitions), failures=failures)


def format_state_transition_report(report: StateTransitionReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM state transition source: {report.source}")
    lines.append(f"State transitions checked: {report.checked_transitions}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM state transition validation failed.")
    else:
        lines.append("")
        lines.append("PFEM state transition validation passed.")

    return "\n".join(lines)
