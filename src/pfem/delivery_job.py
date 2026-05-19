"""PFEM delivery job validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.action import load_action_policy
from pfem.delivery import collect_delivery_channel_ids
from pfem.dispatch import collect_dispatch_rule_ids
from pfem.node_runtime import collect_node_ids
from pfem.routing import load_routing_policy
from pfem.transport import collect_transport_adapter_ids


JsonObject = dict[str, Any]

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
class DeliveryJob:
    delivery_job_id: str
    job_kind: str
    created_time: str
    requested_by_ref: str | None
    dispatch_rule_id: str | None
    route_id: str
    delivery_channel_id: str
    transport_adapter_id: str
    source_node_id: str
    destination_node_id: str
    subject_refs: list[str]
    basis_refs: list[str]
    job_state: str
    priority: str
    not_before_time: str | None
    summary: str


@dataclass(frozen=True)
class DeliveryJobReport:
    source: str
    checked_jobs: int = 0
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


def load_delivery_jobs(path: str | Path) -> list[DeliveryJob]:
    return [
        DeliveryJob(
            delivery_job_id=str(record.get("delivery_job_id", "")),
            job_kind=str(record.get("job_kind", "")),
            created_time=str(record.get("created_time", "")),
            requested_by_ref=str(record["requested_by_ref"]) if "requested_by_ref" in record else None,
            dispatch_rule_id=str(record["dispatch_rule_id"]) if "dispatch_rule_id" in record else None,
            route_id=str(record.get("route_id", "")),
            delivery_channel_id=str(record.get("delivery_channel_id", "")),
            transport_adapter_id=str(record.get("transport_adapter_id", "")),
            source_node_id=str(record.get("source_node_id", "")),
            destination_node_id=str(record.get("destination_node_id", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            basis_refs=_as_list(record.get("basis_refs", [])),
            job_state=str(record.get("job_state", "")),
            priority=str(record.get("priority", "")),
            not_before_time=str(record["not_before_time"]) if "not_before_time" in record else None,
            summary=str(record.get("summary", "")),
        )
        for record in _load_records(Path(path))
    ]


def collect_delivery_job_ids(root: str | Path) -> set[str]:
    jobs_path = Path(root) / "delivery" / "delivery-jobs.json"
    if not jobs_path.exists():
        return set()
    return {job.delivery_job_id for job in load_delivery_jobs(jobs_path) if job.delivery_job_id}


def _collect_route_ids(root: Path) -> set[str]:
    policy_path = root / "routing" / "routing-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_routing_policy(policy_path)
    return {route.route_id for route in policy.routes if route.route_id}


def _collect_priorities(root: Path) -> set[str]:
    policy_path = root / "action" / "action-policy.json"
    if not policy_path.exists():
        return set()
    policy = load_action_policy(policy_path)
    return {priority.priority for priority in policy.priority_levels if priority.priority}


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


def validate_delivery_jobs(root: str | Path) -> DeliveryJobReport:
    root_path = Path(root)
    jobs_path = root_path / "delivery" / "delivery-jobs.json"
    failures: list[str] = []

    if not jobs_path.exists():
        return DeliveryJobReport(
            source=str(jobs_path),
            failures=["missing delivery jobs: delivery/delivery-jobs.json"],
        )

    jobs = load_delivery_jobs(jobs_path)
    if not jobs:
        failures.append("delivery jobs file has no jobs")

    dispatch_rule_ids = collect_dispatch_rule_ids(root_path)
    route_ids = _collect_route_ids(root_path)
    delivery_channel_ids = collect_delivery_channel_ids(root_path)
    transport_adapter_ids = collect_transport_adapter_ids(root_path)
    node_ids = collect_node_ids(root_path)
    priorities = _collect_priorities(root_path)
    known_ids = _collect_known_record_ids(root_path)
    known_paths = _collect_known_artifact_paths(root_path)
    seen_ids: set[str] = set()

    for job in jobs:
        if not job.delivery_job_id:
            failures.append("delivery job missing delivery_job_id")
            continue
        if job.delivery_job_id in seen_ids:
            failures.append(f"duplicate delivery_job_id {job.delivery_job_id!r}")
        seen_ids.add(job.delivery_job_id)

        if job.job_kind not in KNOWN_JOB_KINDS:
            failures.append(f"delivery job {job.delivery_job_id!r} uses unknown job_kind {job.job_kind!r}")
        if not job.created_time:
            failures.append(f"delivery job {job.delivery_job_id!r} missing created_time")
        if job.requested_by_ref and not _known_ref(job.requested_by_ref, known_ids, known_paths):
            failures.append(f"delivery job {job.delivery_job_id!r} references unknown requested_by_ref {job.requested_by_ref!r}")
        if job.dispatch_rule_id and dispatch_rule_ids and job.dispatch_rule_id not in dispatch_rule_ids:
            failures.append(f"delivery job {job.delivery_job_id!r} references unknown dispatch_rule_id {job.dispatch_rule_id!r}")
        if route_ids and job.route_id not in route_ids:
            failures.append(f"delivery job {job.delivery_job_id!r} references unknown route_id {job.route_id!r}")
        if delivery_channel_ids and job.delivery_channel_id not in delivery_channel_ids:
            failures.append(f"delivery job {job.delivery_job_id!r} references unknown delivery_channel_id {job.delivery_channel_id!r}")
        if transport_adapter_ids and job.transport_adapter_id not in transport_adapter_ids:
            failures.append(f"delivery job {job.delivery_job_id!r} references unknown transport_adapter_id {job.transport_adapter_id!r}")
        if node_ids and job.source_node_id not in node_ids:
            failures.append(f"delivery job {job.delivery_job_id!r} references unknown source_node_id {job.source_node_id!r}")
        if node_ids and job.destination_node_id not in node_ids:
            failures.append(f"delivery job {job.delivery_job_id!r} references unknown destination_node_id {job.destination_node_id!r}")

        if not job.subject_refs:
            failures.append(f"delivery job {job.delivery_job_id!r} has no subject_refs")
        for ref in job.subject_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"delivery job {job.delivery_job_id!r} references unknown subject_ref {ref!r}")

        if not job.basis_refs:
            failures.append(f"delivery job {job.delivery_job_id!r} has no basis_refs")
        for ref in job.basis_refs:
            if not _known_ref(ref, known_ids, known_paths):
                failures.append(f"delivery job {job.delivery_job_id!r} references unknown basis_ref {ref!r}")

        if job.job_state not in KNOWN_JOB_STATES:
            failures.append(f"delivery job {job.delivery_job_id!r} uses unknown job_state {job.job_state!r}")
        if priorities and job.priority not in priorities:
            failures.append(f"delivery job {job.delivery_job_id!r} references unknown priority {job.priority!r}")
        if not job.summary:
            failures.append(f"delivery job {job.delivery_job_id!r} missing summary")

    return DeliveryJobReport(source=str(jobs_path), checked_jobs=len(jobs), failures=failures)


def format_delivery_job_report(report: DeliveryJobReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM delivery job source: {report.source}")
    lines.append(f"Delivery jobs checked: {report.checked_jobs}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM delivery job validation failed.")
    else:
        lines.append("")
        lines.append("PFEM delivery job validation passed.")

    return "\n".join(lines)
