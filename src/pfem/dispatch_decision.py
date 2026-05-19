"""PFEM dispatch decision validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.delivery_job import collect_delivery_job_ids
from pfem.dispatch import collect_dispatch_rule_ids


JsonObject = dict[str, Any]

KNOWN_DECISION_KINDS = {
    "eligibility_check",
    "review_gate",
    "retry_check",
    "operator_override",
}

KNOWN_DECISIONS = {
    "allowed",
    "blocked",
    "deferred",
    "requires_review",
    "rejected",
    "unknown",
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
class DispatchDecision:
    dispatch_decision_id: str
    decision_kind: str
    created_time: str
    delivery_job_id: str
    dispatch_rule_id: str
    decision: str
    reason_code: str
    decided_by_ref: str
    basis_refs: list[str]
    resulting_job_state: str | None
    summary: str


@dataclass(frozen=True)
class DispatchDecisionReport:
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


def load_dispatch_decisions(path: str | Path) -> list[DispatchDecision]:
    return [
        DispatchDecision(
            dispatch_decision_id=str(record.get("dispatch_decision_id", "")),
            decision_kind=str(record.get("decision_kind", "")),
            created_time=str(record.get("created_time", "")),
            delivery_job_id=str(record.get("delivery_job_id", "")),
            dispatch_rule_id=str(record.get("dispatch_rule_id", "")),
            decision=str(record.get("decision", "")),
            reason_code=str(record.get("reason_code", "")),
            decided_by_ref=str(record.get("decided_by_ref", "")),
            basis_refs=_as_list(record.get("basis_refs", [])),
            resulting_job_state=str(record["resulting_job_state"]) if "resulting_job_state" in record else None,
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_dispatch_decision_ids(root: str | Path) -> set[str]:
    decisions_path = Path(root) / "dispatch" / "dispatch-decisions.json"
    if not decisions_path.exists():
        return set()
    return {
        decision.dispatch_decision_id
        for decision in load_dispatch_decisions(decisions_path)
        if decision.dispatch_decision_id
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
        ("reconciliation/reconciliation-records.json", "reconciliation_id"),
        ("quality/quality-assessments.json", "quality_assessment_id"),
        ("action/action-records.json", "action_id"),
        ("playbooks/**/*.playbook.json", "playbook_id"),
        ("delivery/delivery-jobs.json", "delivery_job_id"),
        ("dispatch/dispatch-decisions.json", "dispatch_decision_id"),
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
        "handling", "retention", "dispatch", "routing", "delivery", "transport", "topology",
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


def validate_dispatch_decisions(root: str | Path) -> DispatchDecisionReport:
    root_path = Path(root)
    decisions_path = root_path / "dispatch" / "dispatch-decisions.json"
    failures: list[str] = []

    if not decisions_path.exists():
        return DispatchDecisionReport(
            source=str(decisions_path),
            failures=["missing dispatch decisions: dispatch/dispatch-decisions.json"],
        )

    decisions = load_dispatch_decisions(decisions_path)
    if not decisions:
        failures.append("dispatch decisions file has no decisions")

    delivery_job_ids = collect_delivery_job_ids(root_path)
    dispatch_rule_ids = collect_dispatch_rule_ids(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for decision in decisions:
        if not decision.dispatch_decision_id:
            failures.append("dispatch decision missing dispatch_decision_id")
            continue
        if decision.dispatch_decision_id in seen_ids:
            failures.append(f"duplicate dispatch_decision_id {decision.dispatch_decision_id!r}")
        seen_ids.add(decision.dispatch_decision_id)

        if decision.decision_kind not in KNOWN_DECISION_KINDS:
            failures.append(
                f"dispatch decision {decision.dispatch_decision_id!r} uses unknown decision_kind {decision.decision_kind!r}"
            )
        if not decision.created_time:
            failures.append(f"dispatch decision {decision.dispatch_decision_id!r} missing created_time")

        if delivery_job_ids and decision.delivery_job_id not in delivery_job_ids:
            failures.append(
                f"dispatch decision {decision.dispatch_decision_id!r} references unknown delivery_job_id {decision.delivery_job_id!r}"
            )

        if dispatch_rule_ids and decision.dispatch_rule_id not in dispatch_rule_ids:
            failures.append(
                f"dispatch decision {decision.dispatch_decision_id!r} references unknown dispatch_rule_id {decision.dispatch_rule_id!r}"
            )

        if decision.decision not in KNOWN_DECISIONS:
            failures.append(
                f"dispatch decision {decision.dispatch_decision_id!r} uses unknown decision {decision.decision!r}"
            )

        if not decision.reason_code:
            failures.append(f"dispatch decision {decision.dispatch_decision_id!r} missing reason_code")
        if not decision.decided_by_ref:
            failures.append(f"dispatch decision {decision.dispatch_decision_id!r} missing decided_by_ref")
        if not decision.basis_refs:
            failures.append(f"dispatch decision {decision.dispatch_decision_id!r} has no basis_refs")
        for ref in decision.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(
                    f"dispatch decision {decision.dispatch_decision_id!r} references unknown basis_ref {ref!r}"
                )

        if decision.resulting_job_state and decision.resulting_job_state not in KNOWN_JOB_STATES:
            failures.append(
                f"dispatch decision {decision.dispatch_decision_id!r} has unknown resulting_job_state {decision.resulting_job_state!r}"
            )

        if not decision.summary:
            failures.append(f"dispatch decision {decision.dispatch_decision_id!r} missing summary")

    return DispatchDecisionReport(
        source=str(decisions_path),
        checked_decisions=len(decisions),
        failures=failures,
    )


def format_dispatch_decision_report(report: DispatchDecisionReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM dispatch decision source: {report.source}")
    lines.append(f"Dispatch decisions checked: {report.checked_decisions}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM dispatch decision validation failed.")
    else:
        lines.append("")
        lines.append("PFEM dispatch decision validation passed.")

    return "\n".join(lines)
