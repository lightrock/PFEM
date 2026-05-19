"""PFEM federation topology validation."""

from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any

from pfem.node_runtime import collect_node_ids
from pfem.policy import load_sharing_policy, known_review_gate_ids, known_scope_ids


JsonObject = dict[str, Any]


@dataclass(frozen=True)
class FederationLink:
    link_id: str
    from_node_id: str
    to_node_id: str
    allowed_message_kinds: list[str]
    allowed_sharing_scopes: list[str]
    status: str
    review_gate: str | None = None


@dataclass(frozen=True)
class FederationTopology:
    topology_id: str
    version: str
    links: list[FederationLink]


@dataclass(frozen=True)
class TopologyReport:
    source: str
    checked_links: int = 0
    checked_messages: int = 0
    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.failures


def _as_list(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def load_federation_topology(path: str | Path) -> FederationTopology:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))

    links = [
        FederationLink(
            link_id=str(item.get("link_id", "")),
            from_node_id=str(item.get("from_node_id", "")),
            to_node_id=str(item.get("to_node_id", "")),
            allowed_message_kinds=_as_list(item.get("allowed_message_kinds", [])),
            allowed_sharing_scopes=_as_list(item.get("allowed_sharing_scopes", [])),
            status=str(item.get("status", "")),
            review_gate=str(item["review_gate"]) if "review_gate" in item else None,
        )
        for item in raw.get("links", [])
    ]

    return FederationTopology(
        topology_id=str(raw.get("topology_id", "")),
        version=str(raw.get("version", "")),
        links=links,
    )


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


def _iter_federation_messages(root: Path) -> list[tuple[Path, JsonObject]]:
    candidates = [
        *root.glob("tests/fixtures/**/federation_message.json"),
        *root.glob("examples/**/federation_message.json"),
    ]
    records: list[tuple[Path, JsonObject]] = []
    for path in sorted(set(candidates)):
        for record in _load_records(path):
            records.append((path, record))
    return records


def _matching_link_exists(
    links: list[FederationLink],
    sender_node_id: str,
    recipient_node_id: str,
    message_kind: str,
    sharing_scope: str,
) -> bool:
    for link in links:
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
        return True
    return False


def validate_topology_repository(root: str | Path) -> TopologyReport:
    root_path = Path(root)
    topology_path = root_path / "topology" / "federation-topology.json"
    failures: list[str] = []

    if not topology_path.exists():
        return TopologyReport(
            source=str(topology_path),
            failures=["missing federation topology: topology/federation-topology.json"],
        )

    topology = load_federation_topology(topology_path)
    node_ids = collect_node_ids(root_path)

    policy_path = root_path / "policy" / "sharing-policy.json"
    scope_ids: set[str] = set()
    review_gate_ids: set[str] = set()
    if policy_path.exists():
        policy = load_sharing_policy(policy_path)
        scope_ids = known_scope_ids(policy)
        review_gate_ids = known_review_gate_ids(policy)

    if not topology.topology_id:
        failures.append("federation topology missing topology_id")
    if not topology.version:
        failures.append("federation topology missing version")

    seen_links: set[str] = set()
    for link in topology.links:
        if not link.link_id:
            failures.append("topology link missing link_id")
            continue
        if link.link_id in seen_links:
            failures.append(f"duplicate topology link_id {link.link_id!r}")
        seen_links.add(link.link_id)

        if node_ids and link.from_node_id not in node_ids:
            failures.append(f"topology link {link.link_id!r} references unknown from_node_id {link.from_node_id!r}")
        if node_ids and link.to_node_id not in node_ids:
            failures.append(f"topology link {link.link_id!r} references unknown to_node_id {link.to_node_id!r}")
        if not link.allowed_message_kinds:
            failures.append(f"topology link {link.link_id!r} has no allowed_message_kinds")
        if not link.allowed_sharing_scopes:
            failures.append(f"topology link {link.link_id!r} has no allowed_sharing_scopes")

        for scope in link.allowed_sharing_scopes:
            if scope_ids and scope not in scope_ids:
                failures.append(f"topology link {link.link_id!r} uses unknown sharing scope {scope!r}")

        if link.review_gate and review_gate_ids and link.review_gate not in review_gate_ids:
            failures.append(f"topology link {link.link_id!r} uses unknown review gate {link.review_gate!r}")

    messages = _iter_federation_messages(root_path)
    for path, message in messages:
        message_id = message.get("message_id", "<missing message_id>")
        sender_node_id = str(message.get("sender_node_id", ""))
        message_kind = str(message.get("message_kind", ""))
        sharing_scope = str(message.get("sharing_scope", ""))
        recipient_node_ids = _as_list(message.get("recipient_node_ids", []))

        if not recipient_node_ids:
            failures.append(f"federation message {message_id!r} has no recipient_node_ids: {path.relative_to(root_path)}")
            continue

        for recipient_node_id in recipient_node_ids:
            if node_ids and recipient_node_id not in node_ids:
                failures.append(f"federation message {message_id!r} references unknown recipient_node_id {recipient_node_id!r}")
                continue
            if not _matching_link_exists(
                topology.links,
                sender_node_id=sender_node_id,
                recipient_node_id=recipient_node_id,
                message_kind=message_kind,
                sharing_scope=sharing_scope,
            ):
                failures.append(
                    f"federation message {message_id!r} has no allowed topology link "
                    f"{sender_node_id!r}->{recipient_node_id!r} kind={message_kind!r} scope={sharing_scope!r}"
                )

    return TopologyReport(
        source=str(topology_path),
        checked_links=len(topology.links),
        checked_messages=len(messages),
        failures=failures,
    )


def format_topology_report(report: TopologyReport) -> str:
    lines: list[str] = []
    lines.append(f"PFEM topology source: {report.source}")
    lines.append(f"Links checked: {report.checked_links}")
    lines.append(f"Federation messages checked: {report.checked_messages}")

    if report.failures:
        lines.append("")
        lines.append("Failures:")
        for failure in report.failures:
            lines.append(f"  - {failure}")
        lines.append("")
        lines.append("PFEM topology validation failed.")
    else:
        lines.append("")
        lines.append("PFEM topology validation passed.")

    return "\n".join(lines)
