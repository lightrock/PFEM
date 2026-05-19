"""PFEM state checkpoint validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from pfem.apply_receipt import collect_apply_receipt_ids
from pfem.import_record import collect_import_record_ids
from pfem.merge_decision import collect_merge_decision_ids
from pfem.node_runtime import collect_node_ids


JsonObject = dict[str, Any]

KNOWN_CHECKPOINT_KINDS = {
    "local_repository_state",
    "rollup_state",
    "node_state",
}

KNOWN_CHECKPOINT_STATES = {
    "current",
    "superseded",
    "archived",
    "failed",
}

KNOWN_DIGEST_ALGORITHMS = {
    "sha256-sorted-ref-list",
}


@dataclass(frozen=True)
class StateCheckpoint:
    state_checkpoint_id: str
    checkpoint_kind: str
    created_time: str
    node_id: str
    apply_receipt_id: str | None
    merge_decision_id: str | None
    import_record_id: str | None
    checkpoint_state: str
    included_refs: list[str]
    basis_refs: list[str]
    digest_algorithm: str
    state_digest: str
    checkpointed_by_ref: str
    summary: str


@dataclass(frozen=True)
class StateCheckpointReport:
    source: str
    checked_checkpoints: int = 0
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


def compute_ref_digest(refs: list[str]) -> str:
    payload = json.dumps(sorted(refs), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_state_checkpoints(path: str | Path) -> list[StateCheckpoint]:
    return [
        StateCheckpoint(
            state_checkpoint_id=str(record.get("state_checkpoint_id", "")),
            checkpoint_kind=str(record.get("checkpoint_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            apply_receipt_id=str(record["apply_receipt_id"]) if "apply_receipt_id" in record else None,
            merge_decision_id=str(record["merge_decision_id"]) if "merge_decision_id" in record else None,
            import_record_id=str(record["import_record_id"]) if "import_record_id" in record else None,
            checkpoint_state=str(record.get("checkpoint_state", "")),
            included_refs=_as_list(record.get("included_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            digest_algorithm=str(record.get("digest_algorithm", "")),
            state_digest=str(record.get("state_digest", "")),
            checkpointed_by_ref=str(record.get("checkpointed_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_state_checkpoint_ids(root: str | Path) -> set[str]:
    checkpoints_path = Path(root) / "state" / "state-checkpoints.json"
    if not checkpoints_path.exists():
        return set()
    return {
        checkpoint.state_checkpoint_id
        for checkpoint in load_state_checkpoints(checkpoints_path)
        if checkpoint.state_checkpoint_id
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


def validate_state_checkpoints(root: str | Path) -> StateCheckpointReport:
    root_path = Path(root)
    checkpoints_path = root_path / "state" / "state-checkpoints.json"
    failures: list[str] = []

    if not checkpoints_path.exists():
        return StateCheckpointReport(source=str(checkpoints_path), failures=["missing state checkpoints: state/state-checkpoints.json"])

    checkpoints = load_state_checkpoints(checkpoints_path)
    if not checkpoints:
        failures.append("state checkpoints file has no checkpoints")

    node_ids = collect_node_ids(root_path)
    apply_receipt_ids = collect_apply_receipt_ids(root_path)
    merge_decision_ids = collect_merge_decision_ids(root_path)
    import_record_ids = collect_import_record_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for checkpoint in checkpoints:
        if not checkpoint.state_checkpoint_id:
            failures.append("state checkpoint missing state_checkpoint_id")
            continue
        if checkpoint.state_checkpoint_id in seen_ids:
            failures.append(f"duplicate state_checkpoint_id {checkpoint.state_checkpoint_id!r}")
        seen_ids.add(checkpoint.state_checkpoint_id)

        if checkpoint.checkpoint_kind not in KNOWN_CHECKPOINT_KINDS:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} uses unknown checkpoint_kind {checkpoint.checkpoint_kind!r}")
        if not checkpoint.created_time:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} missing created_time")
        if node_ids and checkpoint.node_id not in node_ids:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} references unknown node_id {checkpoint.node_id!r}")
        if checkpoint.apply_receipt_id and apply_receipt_ids and checkpoint.apply_receipt_id not in apply_receipt_ids:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} references unknown apply_receipt_id {checkpoint.apply_receipt_id!r}")
        if checkpoint.merge_decision_id and merge_decision_ids and checkpoint.merge_decision_id not in merge_decision_ids:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} references unknown merge_decision_id {checkpoint.merge_decision_id!r}")
        if checkpoint.import_record_id and import_record_ids and checkpoint.import_record_id not in import_record_ids:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} references unknown import_record_id {checkpoint.import_record_id!r}")
        if checkpoint.checkpoint_state not in KNOWN_CHECKPOINT_STATES:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} uses unknown checkpoint_state {checkpoint.checkpoint_state!r}")

        if not checkpoint.included_refs:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} has no included_refs")
        for ref in checkpoint.included_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} references unknown included_ref {ref!r}")

        if not checkpoint.basis_refs:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} has no basis_refs")
        for ref in checkpoint.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} references unknown basis_ref {ref!r}")

        if checkpoint.digest_algorithm not in KNOWN_DIGEST_ALGORITHMS:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} uses unknown digest_algorithm {checkpoint.digest_algorithm!r}")
        elif checkpoint.state_digest != compute_ref_digest(checkpoint.included_refs):
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} has state_digest mismatch")
        if not checkpoint.checkpointed_by_ref:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} missing checkpointed_by_ref")
        if not checkpoint.summary:
            failures.append(f"state checkpoint {checkpoint.state_checkpoint_id!r} missing summary")

    return StateCheckpointReport(source=str(checkpoints_path), checked_checkpoints=len(checkpoints), failures=failures)


def format_state_checkpoint_report(report: StateCheckpointReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM state checkpoint source: {report.source}")
    lines.append(f"State checkpoints checked: {report.checked_checkpoints}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM state checkpoint validation failed.")
    else:
        lines.append("")
        lines.append("PFEM state checkpoint validation passed.")

    return "\n".join(lines)
