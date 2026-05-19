"""PFEM merge decision validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.exchange import load_exchange_receipts
from pfem.import_record import collect_import_record_ids


JsonObject = dict[str, Any]

KNOWN_DECISION_KINDS = {
    "import_merge",
    "conflict_resolution",
    "operator_override",
}

KNOWN_DECISIONS = {
    "accept_incoming",
    "keep_local",
    "supersede_local",
    "create_new_version",
    "defer_for_review",
    "reject_incoming",
    "no_op",
}

KNOWN_IMPORT_STATES = {
    "staged",
    "imported",
    "skipped",
    "failed",
    "superseded",
    "rejected",
}


@dataclass(frozen=True)
class MergeDecision:
    merge_decision_id: str
    decision_kind: str
    created_time: str
    import_record_id: str
    exchange_receipt_id: str
    bundle_id: str
    decision: str
    reason_code: str
    decided_by_ref: str
    incoming_refs: list[str]
    local_target_refs: list[str]
    basis_refs: list[str]
    resulting_import_state: str | None
    summary: str


@dataclass(frozen=True)
class MergeDecisionReport:
    source: str
    checked_decisions: int = 0
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


def load_merge_decisions(path: str | Path) -> list[MergeDecision]:
    return [
        MergeDecision(
            merge_decision_id=str(record.get("merge_decision_id", "")),
            decision_kind=str(record.get("decision_kind", "")),
            created_time=str(record.get("created_time", "")),
            import_record_id=str(record.get("import_record_id", "")),
            exchange_receipt_id=str(record.get("exchange_receipt_id", "")),
            bundle_id=str(record.get("bundle_id", "")),
            decision=str(record.get("decision", "")),
            reason_code=str(record.get("reason_code", "")),
            decided_by_ref=str(record.get("decided_by_ref", "")),
            incoming_refs=_as_list(record.get("incoming_refs", [])),
            local_target_refs=_as_list(record.get("local_target_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            resulting_import_state=str(record["resulting_import_state"]) if "resulting_import_state" in record else None,
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_merge_decision_ids(root: str | Path) -> set[str]:
    decisions_path = Path(root) / "merge" / "merge-decisions.json"
    if not decisions_path.exists():
        return set()
    return {
        decision.merge_decision_id
        for decision in load_merge_decisions(decisions_path)
        if decision.merge_decision_id
    }


def _collect_exchange_receipt_ids(root: Path) -> set[str]:
    path = root / "exchange" / "exchange-receipts.json"
    if not path.exists():
        return set()
    return {
        receipt.exchange_receipt_id
        for receipt in load_exchange_receipts(path)
        if receipt.exchange_receipt_id
    }


def _collect_bundle_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in root.glob("bundles/**/*.bundle.json"):
        for record in _load_records(path):
            if record.get("bundle_id"):
                ids.add(str(record["bundle_id"]))
    return ids


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
        ("merge/merge-decisions.json", "merge_decision_id"),
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
        "inbox", "intake", "imports", "merge", "transport", "topology", "review",
        "audit", "exchange", "reconciliation", "quality", "action", "playbooks",
        "integrity", "schemas", "contracts", "docs", "bundles", "tests",
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


def validate_merge_decisions(root: str | Path) -> MergeDecisionReport:
    root_path = Path(root)
    decisions_path = root_path / "merge" / "merge-decisions.json"
    failures: list[str] = []

    if not decisions_path.exists():
        return MergeDecisionReport(
            source=str(decisions_path),
            failures=["missing merge decisions: merge/merge-decisions.json"],
        )

    decisions = load_merge_decisions(decisions_path)
    if not decisions:
        failures.append("merge decisions file has no decisions")

    import_record_ids = collect_import_record_ids(root_path)
    exchange_receipt_ids = _collect_exchange_receipt_ids(root_path)
    bundle_ids = _collect_bundle_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for decision in decisions:
        if not decision.merge_decision_id:
            failures.append("merge decision missing merge_decision_id")
            continue
        if decision.merge_decision_id in seen_ids:
            failures.append(f"duplicate merge_decision_id {decision.merge_decision_id!r}")
        seen_ids.add(decision.merge_decision_id)

        if decision.decision_kind not in KNOWN_DECISION_KINDS:
            failures.append(f"merge decision {decision.merge_decision_id!r} uses unknown decision_kind {decision.decision_kind!r}")
        if not decision.created_time:
            failures.append(f"merge decision {decision.merge_decision_id!r} missing created_time")
        if import_record_ids and decision.import_record_id not in import_record_ids:
            failures.append(f"merge decision {decision.merge_decision_id!r} references unknown import_record_id {decision.import_record_id!r}")
        if exchange_receipt_ids and decision.exchange_receipt_id not in exchange_receipt_ids:
            failures.append(f"merge decision {decision.merge_decision_id!r} references unknown exchange_receipt_id {decision.exchange_receipt_id!r}")
        if bundle_ids and decision.bundle_id not in bundle_ids:
            failures.append(f"merge decision {decision.merge_decision_id!r} references unknown bundle_id {decision.bundle_id!r}")
        if decision.decision not in KNOWN_DECISIONS:
            failures.append(f"merge decision {decision.merge_decision_id!r} uses unknown decision {decision.decision!r}")
        if not decision.reason_code:
            failures.append(f"merge decision {decision.merge_decision_id!r} missing reason_code")
        if not decision.decided_by_ref:
            failures.append(f"merge decision {decision.merge_decision_id!r} missing decided_by_ref")

        if not decision.incoming_refs:
            failures.append(f"merge decision {decision.merge_decision_id!r} has no incoming_refs")
        for ref in decision.incoming_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"merge decision {decision.merge_decision_id!r} references unknown incoming_ref {ref!r}")

        for ref in decision.local_target_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"merge decision {decision.merge_decision_id!r} references unknown local_target_ref {ref!r}")

        if not decision.basis_refs:
            failures.append(f"merge decision {decision.merge_decision_id!r} has no basis_refs")
        for ref in decision.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"merge decision {decision.merge_decision_id!r} references unknown basis_ref {ref!r}")

        if decision.resulting_import_state and decision.resulting_import_state not in KNOWN_IMPORT_STATES:
            failures.append(f"merge decision {decision.merge_decision_id!r} has unknown resulting_import_state {decision.resulting_import_state!r}")
        if not decision.summary:
            failures.append(f"merge decision {decision.merge_decision_id!r} missing summary")

    return MergeDecisionReport(
        source=str(decisions_path),
        checked_decisions=len(decisions),
        failures=failures,
    )


def format_merge_decision_report(report: MergeDecisionReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM merge decision source: {report.source}")
    lines.append(f"Merge decisions checked: {report.checked_decisions}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM merge decision validation failed.")
    else:
        lines.append("")
        lines.append("PFEM merge decision validation passed.")

    return "\n".join(lines)
