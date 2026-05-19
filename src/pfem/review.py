"""PFEM review decision validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.policy import load_sharing_policy, known_review_gate_ids, known_scope_ids
from pfem.topology import load_federation_topology


JsonObject = dict[str, Any]

APPROVED_DECISIONS = {"approved", "approved-with-notes"}


@dataclass(frozen=True)
class ReviewRecord:
    review_id: str
    review_gate: str
    decision: str
    reviewer_role: str
    created_time: str
    subject_refs: list[str]
    sharing_scope: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class ReviewReport:
    source: str
    checked_reviews: int = 0
    checked_gate_requirements: int = 0
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


def load_review_records(path: str | Path) -> list[ReviewRecord]:
    records = _load_records(Path(path))
    return [
        ReviewRecord(
            review_id=str(record.get("review_id", "")),
            review_gate=str(record.get("review_gate", "")),
            decision=str(record.get("decision", "")),
            reviewer_role=str(record.get("reviewer_role", "")),
            created_time=str(record.get("created_time", "")),
            subject_refs=_as_list(record.get("subject_refs", [])),
            sharing_scope=str(record["sharing_scope"]) if "sharing_scope" in record else None,
            notes=str(record["notes"]) if "notes" in record else None,
        )
        for record in records
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
        ("examples/**/raw_evidence.json", "evidence_id"),
        ("examples/**/normalized_observation.json", "observation_id"),
        ("examples/**/finding.json", "finding_id"),
        ("examples/**/alert.json", "alert_id"),
        ("examples/**/evidence_package.json", "package_id"),
        ("examples/**/rollup_summary.json", "rollup_id"),
        ("examples/**/federation_message.json", "message_id"),
    ]

    ids: set[str] = set()
    for pattern, key in patterns:
        for path in root.glob(pattern):
            for record in _load_records(path):
                if record.get(key):
                    ids.add(str(record[key]))
    return ids


def _iter_federation_messages(root: Path) -> list[JsonObject]:
    messages: list[JsonObject] = []
    for path in sorted(root.glob("tests/fixtures/**/federation_message.json")):
        messages.extend(_load_records(path))
    for path in sorted(root.glob("examples/**/federation_message.json")):
        messages.extend(_load_records(path))
    return messages


def _matching_review_exists(
    records: list[ReviewRecord],
    review_gate: str,
    acceptable_refs: set[str],
) -> bool:
    for record in records:
        if record.review_gate != review_gate:
            continue
        if record.decision not in APPROVED_DECISIONS:
            continue
        if acceptable_refs.intersection(record.subject_refs):
            return True
    return False


def _matching_link_gate(
    root: Path,
    sender_node_id: str,
    recipient_node_id: str,
    message_kind: str,
    sharing_scope: str,
) -> str | None:
    topology_path = root / "topology" / "federation-topology.json"
    if not topology_path.exists():
        return None

    topology = load_federation_topology(topology_path)
    for link in topology.links:
        if link.status.startswith("disabled"):
            continue
        if link.from_node_id != sender_node_id:
            continue
        if link.to_node_id != recipient_node_id:
            continue
        if message_kind not in link.allowed_message_kinds:
            continue
        if sharing_scope not in link.allowed_sharing_scopes:
            continue
        return link.review_gate

    return None


def validate_review_repository(root: str | Path) -> ReviewReport:
    root_path = Path(root)
    review_path = root_path / "review" / "review-records.json"
    failures: list[str] = []

    if not review_path.exists():
        return ReviewReport(
            source=str(review_path),
            failures=["missing review records: review/review-records.json"],
        )

    records = load_review_records(review_path)

    policy_path = root_path / "policy" / "sharing-policy.json"
    review_gate_ids: set[str] = set()
    scope_ids: set[str] = set()
    if policy_path.exists():
        policy = load_sharing_policy(policy_path)
        review_gate_ids = known_review_gate_ids(policy)
        scope_ids = known_scope_ids(policy)

    known_record_ids = _collect_known_record_ids(root_path)
    seen_review_ids: set[str] = set()

    for record in records:
        if not record.review_id:
            failures.append("review record missing review_id")
            continue
        if record.review_id in seen_review_ids:
            failures.append(f"duplicate review_id {record.review_id!r}")
        seen_review_ids.add(record.review_id)

        if review_gate_ids and record.review_gate not in review_gate_ids:
            failures.append(f"review {record.review_id!r} references unknown review_gate {record.review_gate!r}")
        if record.sharing_scope and scope_ids and record.sharing_scope not in scope_ids:
            failures.append(f"review {record.review_id!r} references unknown sharing_scope {record.sharing_scope!r}")
        if not record.subject_refs:
            failures.append(f"review {record.review_id!r} has no subject_refs")

        for ref in record.subject_refs:
            if known_record_ids and ref not in known_record_ids:
                failures.append(f"review {record.review_id!r} references missing subject_ref {ref!r}")

    checked_gate_requirements = 0
    for message in _iter_federation_messages(root_path):
        message_id = str(message.get("message_id", ""))
        sender_node_id = str(message.get("sender_node_id", ""))
        message_kind = str(message.get("message_kind", ""))
        sharing_scope = str(message.get("sharing_scope", ""))
        recipient_node_ids = _as_list(message.get("recipient_node_ids", []))

        acceptable_refs = {message_id}
        acceptable_refs.update(_as_list(message.get("lineage_refs", [])))

        for recipient_node_id in recipient_node_ids:
            required_gate = _matching_link_gate(
                root_path,
                sender_node_id=sender_node_id,
                recipient_node_id=recipient_node_id,
                message_kind=message_kind,
                sharing_scope=sharing_scope,
            )
            if not required_gate:
                continue
            checked_gate_requirements += 1
            if not _matching_review_exists(records, required_gate, acceptable_refs):
                failures.append(
                    f"federation message {message_id!r} to {recipient_node_id!r} "
                    f"requires review_gate {required_gate!r} but no approved review covers it"
                )

    return ReviewReport(
        source=str(review_path),
        checked_reviews=len(records),
        checked_gate_requirements=checked_gate_requirements,
        failures=failures,
    )


def format_review_report(report: ReviewReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM review source: {report.source}")
    lines.append(f"Review records checked: {report.checked_reviews}")
    lines.append(f"Gate requirements checked: {report.checked_gate_requirements}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM review validation failed.")
    else:
        lines.append("")
        lines.append("PFEM review validation passed.")

    return "\n".join(lines)
