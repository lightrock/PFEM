"""PFEM snapshot manifest validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.state_checkpoint import collect_state_checkpoint_ids
from pfem.state_transition import collect_state_transition_ids


JsonObject = dict[str, Any]

KNOWN_MANIFEST_KINDS = {
    "state_checkpoint_snapshot",
    "node_snapshot",
    "rollup_snapshot",
}

KNOWN_SNAPSHOT_STATES = {
    "current",
    "superseded",
    "archived",
    "failed",
}

KNOWN_DIGEST_ALGORITHMS = {
    "sha256-canonical-snapshot-items",
}


@dataclass(frozen=True)
class SnapshotManifest:
    snapshot_manifest_id: str
    manifest_kind: str
    created_time: str
    node_id: str
    state_checkpoint_id: str
    state_transition_id: str | None
    snapshot_state: str
    items: list[JsonObject]
    basis_refs: list[str]
    digest_algorithm: str
    snapshot_digest: str
    manifested_by_ref: str
    summary: str


@dataclass(frozen=True)
class SnapshotManifestReport:
    source: str
    checked_manifests: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def _as_object_list(value: object) -> list[JsonObject]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


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


def compute_snapshot_digest(items: list[JsonObject]) -> str:
    payload = json.dumps(items, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_snapshot_manifests(path: str | Path) -> list[SnapshotManifest]:
    return [
        SnapshotManifest(
            snapshot_manifest_id=str(record.get("snapshot_manifest_id", "")),
            manifest_kind=str(record.get("manifest_kind", "")),
            created_time=str(record.get("created_time", "")),
            node_id=str(record.get("node_id", "")),
            state_checkpoint_id=str(record.get("state_checkpoint_id", "")),
            state_transition_id=_optional_str(record.get("state_transition_id")),
            snapshot_state=str(record.get("snapshot_state", "")),
            items=_as_object_list(record.get("items", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            digest_algorithm=str(record.get("digest_algorithm", "")),
            snapshot_digest=str(record.get("snapshot_digest", "")),
            manifested_by_ref=str(record.get("manifested_by_ref", "")),
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_snapshot_manifest_ids(root: str | Path) -> set[str]:
    manifests_path = Path(root) / "snapshots" / "snapshot-manifests.json"
    if not manifests_path.exists():
        return set()
    return {
        manifest.snapshot_manifest_id
        for manifest in load_snapshot_manifests(manifests_path)
        if manifest.snapshot_manifest_id
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
        ("snapshots/snapshot-manifests.json", "snapshot_manifest_id"),
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
        "snapshots", "transport", "topology", "review", "audit", "exchange",
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


def validate_snapshot_manifests(root: str | Path) -> SnapshotManifestReport:
    root_path = Path(root)
    manifests_path = root_path / "snapshots" / "snapshot-manifests.json"
    failures: list[str] = []

    if not manifests_path.exists():
        return SnapshotManifestReport(source=str(manifests_path), failures=["missing snapshot manifests: snapshots/snapshot-manifests.json"])

    manifests = load_snapshot_manifests(manifests_path)
    if not manifests:
        failures.append("snapshot manifests file has no manifests")

    node_ids = collect_node_ids(root_path)
    checkpoint_ids = collect_state_checkpoint_ids(root_path)
    transition_ids = collect_state_transition_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for manifest in manifests:
        if not manifest.snapshot_manifest_id:
            failures.append("snapshot manifest missing snapshot_manifest_id")
            continue
        if manifest.snapshot_manifest_id in seen_ids:
            failures.append(f"duplicate snapshot_manifest_id {manifest.snapshot_manifest_id!r}")
        seen_ids.add(manifest.snapshot_manifest_id)

        if manifest.manifest_kind not in KNOWN_MANIFEST_KINDS:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} uses unknown manifest_kind {manifest.manifest_kind!r}")
        if not manifest.created_time:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} missing created_time")
        if node_ids and manifest.node_id not in node_ids:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} references unknown node_id {manifest.node_id!r}")
        if checkpoint_ids and manifest.state_checkpoint_id not in checkpoint_ids:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} references unknown state_checkpoint_id {manifest.state_checkpoint_id!r}")
        if manifest.state_transition_id and transition_ids and manifest.state_transition_id not in transition_ids:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} references unknown state_transition_id {manifest.state_transition_id!r}")
        if manifest.snapshot_state not in KNOWN_SNAPSHOT_STATES:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} uses unknown snapshot_state {manifest.snapshot_state!r}")

        if not manifest.items:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} has no items")
        for item in manifest.items:
            ref = str(item.get("ref", ""))
            source_path = str(item.get("source_path", ""))
            if not ref:
                failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} has item without ref")
            elif not _known_ref(ref, known_ids, known_paths):
                failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} references unknown item ref {ref!r}")
            if source_path and source_path.replace("\\", "/") not in known_paths:
                failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} references missing item source_path {source_path!r}")

        if not manifest.basis_refs:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} has no basis_refs")
        for ref in manifest.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} references unknown basis_ref {ref!r}")

        if manifest.digest_algorithm not in KNOWN_DIGEST_ALGORITHMS:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} uses unknown digest_algorithm {manifest.digest_algorithm!r}")
        elif manifest.snapshot_digest != compute_snapshot_digest(manifest.items):
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} has snapshot_digest mismatch")
        if not manifest.manifested_by_ref:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} missing manifested_by_ref")
        if not manifest.summary:
            failures.append(f"snapshot manifest {manifest.snapshot_manifest_id!r} missing summary")

    return SnapshotManifestReport(source=str(manifests_path), checked_manifests=len(manifests), failures=failures)


def format_snapshot_manifest_report(report: SnapshotManifestReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM snapshot manifest source: {report.source}")
    lines.append(f"Snapshot manifests checked: {report.checked_manifests}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM snapshot manifest validation failed.")
    else:
        lines.append("")
        lines.append("PFEM snapshot manifest validation passed.")

    return "\n".join(lines)
