"""PFEM catalog."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pfem.action import load_action_policy, load_action_records
from pfem.adapter_runtime import load_adapter_registry
from pfem.audit import load_audit_events
from pfem.bundle import load_exchange_bundle
from pfem.capability_runtime import load_capability_manifest
from pfem.delivery import load_delivery_channel_registry
from pfem.doctor import find_repo_root
from pfem.example_runtime import load_example_registry
from pfem.exchange import load_exchange_receipts
from pfem.handling import load_handling_policy
from pfem.integrity import load_integrity_manifest
from pfem.node_runtime import load_node_registry
from pfem.playbook import load_playbooks
from pfem.policy import load_sharing_policy
from pfem.profile_runtime import load_profile_registry
from pfem.quality import load_quality_assessments, load_quality_policy
from pfem.reconciliation import load_reconciliation_records
from pfem.retention import load_retention_policy
from pfem.review import load_review_records
from pfem.routing import load_routing_policy
from pfem.source_runtime import load_source_registry
from pfem.transport import load_transport_adapter_registry


def _capability_rows(root: Path) -> list[dict[str, Any]]:
    return [{"capability_id": m.capability_id, "capability_kind": m.capability_kind, "path": str(p.relative_to(root))} for p in sorted((root / "capabilities").rglob("*.capability.yaml")) for m in [load_capability_manifest(p)]] if (root / "capabilities").exists() else []


def _adapter_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "adapters" / "adapter-registry.json"
    return [] if not p.exists() else [{"adapter_id": e.adapter_id, "adapter_kind": e.adapter_kind, "status": e.status, "path": e.path} for e in load_adapter_registry(p).adapters]


def _profile_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "profiles" / "profile-registry.json"
    return [] if not p.exists() else [{"profile_id": e.profile_id, "profile_kind": e.profile_kind, "status": e.status, "path": e.path} for e in load_profile_registry(p).profiles]


def _node_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "nodes" / "node-registry.json"
    return [] if not p.exists() else [{"node_id": e.node_id, "profile_id": e.profile_id, "status": e.status, "path": e.path} for e in load_node_registry(p).nodes]


def _source_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "sources" / "source-registry.json"
    return [] if not p.exists() else [{"source_id": e.source_id, "source_kind": e.source_kind, "adapter_id": e.adapter_id, "node_id": e.node_id, "status": e.status} for e in load_source_registry(p).sources]


def _example_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "examples" / "example-registry.json"
    return [] if not p.exists() else [{"example_id": e.example_id, "profile_id": e.profile_id, "runnable": e.runnable, "status": e.status, "path": e.path} for e in load_example_registry(p).examples]


def _review_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "review" / "review-records.json"
    return [] if not p.exists() else [{"review_id": r.review_id, "review_gate": r.review_gate, "decision": r.decision, "sharing_scope": r.sharing_scope or ""} for r in load_review_records(p)]


def _audit_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "audit" / "audit-journal.json"
    return [] if not p.exists() else [{"audit_id": e.audit_id, "event_kind": e.event_kind, "actor_ref": e.actor_ref} for e in load_audit_events(p)]


def _bundle_rows(root: Path) -> list[dict[str, Any]]:
    return [{"bundle_id": b.bundle_id, "bundle_kind": b.bundle_kind, "sharing_scope": b.sharing_scope, "path": str(p.relative_to(root))} for p in sorted((root / "bundles").glob("**/*.bundle.json")) for b in [load_exchange_bundle(p)]] if (root / "bundles").exists() else []


def _exchange_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "exchange" / "exchange-receipts.json"
    return [] if not p.exists() else [{"exchange_receipt_id": r.exchange_receipt_id, "receipt_kind": r.receipt_kind, "bundle_id": r.bundle_id, "decision": r.decision} for r in load_exchange_receipts(p)]


def _reconciliation_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "reconciliation" / "reconciliation-records.json"
    return [] if not p.exists() else [{"reconciliation_id": r.reconciliation_id, "reconciliation_kind": r.reconciliation_kind, "decision": r.decision, "result_state": r.result_state} for r in load_reconciliation_records(p)]


def _quality_assessment_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "quality" / "quality-assessments.json"
    return [] if not p.exists() else [{"quality_assessment_id": q.quality_assessment_id, "confidence_level": q.confidence_level, "flags": ",".join(q.quality_flags)} for q in load_quality_assessments(p)]


def _quality_policy_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "quality" / "quality-policy.json"
    return [] if not p.exists() else [{"confidence_level": level.confidence_level, "rank": level.rank, "display_name": level.display_name} for level in load_quality_policy(p).confidence_levels]


def _action_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "action" / "action-records.json"
    return [] if not p.exists() else [{"action_id": a.action_id, "action_kind": a.action_kind, "priority": a.priority, "action_state": a.action_state} for a in load_action_records(p)]


def _action_policy_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "action" / "action-policy.json"
    return [] if not p.exists() else [{"action_kind": kind.action_kind, "display_name": kind.display_name} for kind in load_action_policy(p).action_kinds]


def _playbook_rows(root: Path) -> list[dict[str, Any]]:
    return [{"playbook_id": playbook.playbook_id, "playbook_kind": playbook.playbook_kind, "status": playbook.status, "steps": len(playbook.steps)} for _, playbook in load_playbooks(root)]


def _routing_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "routing" / "routing-policy.json"
    return [] if not p.exists() else [{"route_id": route.route_id, "route_kind": route.route_kind, "enabled": route.enabled, "channels": len(route.allowed_delivery_channel_ids)} for route in load_routing_policy(p).routes]


def _delivery_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "delivery" / "delivery-channel-registry.json"
    return [] if not p.exists() else [{"channel_id": c.channel_id, "channel_kind": c.channel_kind, "status": c.status, "route_kinds": ",".join(c.supports_route_kinds)} for c in load_delivery_channel_registry(p).channels]


def _transport_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "transport" / "transport-adapter-registry.json"
    return [] if not p.exists() else [{"transport_adapter_id": t.transport_adapter_id, "transport_kind": t.transport_kind, "status": t.status, "channels": ",".join(t.delivery_channel_ids)} for t in load_transport_adapter_registry(p).adapters]


def _handling_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "handling" / "handling-policy.json"
    return [] if not p.exists() else [{"label_id": label.label_id, "allowed_sharing_scopes": ",".join(label.allowed_sharing_scopes), "requires_redaction": label.requires_redaction_before_share} for label in load_handling_policy(p).handling_labels]


def _retention_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "retention" / "retention-policy.json"
    return [] if not p.exists() else [{"retention_class": item.retention_class, "default_duration": item.default_duration, "allowed_states": ",".join(item.allowed_disposition_states)} for item in load_retention_policy(p).retention_classes]


def _integrity_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "integrity" / "receipt-manifest.json"
    return [] if not p.exists() else [{"path": r.path, "digest_algorithm": r.digest_algorithm, "purpose": r.purpose} for r in load_integrity_manifest(p).receipts]


def _policy_rows(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    p = root / "policy" / "sharing-policy.json"
    if not p.exists():
        return [], []
    policy = load_sharing_policy(p)
    return ([{"scope_id": s.scope_id, "display_name": s.display_name, "path": str(p.relative_to(root))} for s in policy.sharing_scopes],
            [{"gate_id": g.gate_id, "display_name": g.display_name, "path": str(p.relative_to(root))} for g in policy.review_gates])


def build_catalog(start: str | Path | None = None) -> dict[str, Any]:
    root = find_repo_root(start)
    sharing_scopes, review_gates = _policy_rows(root)
    catalog = {
        "root": str(root),
        "capabilities": _capability_rows(root),
        "adapters": _adapter_rows(root),
        "profiles": _profile_rows(root),
        "nodes": _node_rows(root),
        "sources": _source_rows(root),
        "examples": _example_rows(root),
        "reviews": _review_rows(root),
        "audit_events": _audit_rows(root),
        "bundles": _bundle_rows(root),
        "exchange_receipts": _exchange_rows(root),
        "reconciliation_records": _reconciliation_rows(root),
        "quality_levels": _quality_policy_rows(root),
        "quality_assessments": _quality_assessment_rows(root),
        "action_kinds": _action_policy_rows(root),
        "action_records": _action_rows(root),
        "playbooks": _playbook_rows(root),
        "routes": _routing_rows(root),
        "delivery_channels": _delivery_rows(root),
        "transport_adapters": _transport_rows(root),
        "handling_labels": _handling_rows(root),
        "retention_classes": _retention_rows(root),
        "integrity_receipts": _integrity_rows(root),
        "sharing_scopes": sharing_scopes,
        "review_gates": review_gates,
    }
    catalog["counts"] = {key: len(value) for key, value in catalog.items() if isinstance(value, list)}
    return catalog


def _format_table(title: str, rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["", title, "-" * len(title)]
    if not rows:
        lines.append("(none)")
        return lines
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in columns}
    lines.append("  ".join(c.ljust(widths[c]) for c in columns))
    lines.append("  ".join("-" * widths[c] for c in columns))
    for row in rows:
        lines.append("  ".join(str(row.get(c, "")).ljust(widths[c]) for c in columns))
    return lines


def format_catalog(catalog: dict[str, Any]) -> str:
    counts = catalog["counts"]
    lines = [
        f"PFEM catalog root: {catalog['root']}",
        "Counts: "
        f"{counts.get('capabilities', 0)} capabilities, {counts.get('adapters', 0)} adapters, "
        f"{counts.get('profiles', 0)} profiles, {counts.get('nodes', 0)} nodes, "
        f"{counts.get('sources', 0)} sources, {counts.get('routes', 0)} routes, "
        f"{counts.get('delivery_channels', 0)} delivery channels, "
        f"{counts.get('transport_adapters', 0)} transport adapters",
    ]
    lines.extend(_format_table("Capabilities", catalog["capabilities"], ["capability_id", "capability_kind", "path"]))
    lines.extend(_format_table("Adapters", catalog["adapters"], ["adapter_id", "adapter_kind", "status", "path"]))
    lines.extend(_format_table("Profiles", catalog["profiles"], ["profile_id", "profile_kind", "status", "path"]))
    lines.extend(_format_table("Nodes", catalog["nodes"], ["node_id", "profile_id", "status", "path"]))
    lines.extend(_format_table("Sources", catalog["sources"], ["source_id", "source_kind", "adapter_id", "node_id", "status"]))
    lines.extend(_format_table("Examples", catalog["examples"], ["example_id", "profile_id", "runnable", "status", "path"]))
    lines.extend(_format_table("Reviews", catalog["reviews"], ["review_id", "review_gate", "decision", "sharing_scope"]))
    lines.extend(_format_table("Audit Events", catalog["audit_events"], ["audit_id", "event_kind", "actor_ref"]))
    lines.extend(_format_table("Bundles", catalog["bundles"], ["bundle_id", "bundle_kind", "sharing_scope", "path"]))
    lines.extend(_format_table("Exchange Receipts", catalog["exchange_receipts"], ["exchange_receipt_id", "receipt_kind", "bundle_id", "decision"]))
    lines.extend(_format_table("Reconciliation Records", catalog["reconciliation_records"], ["reconciliation_id", "reconciliation_kind", "decision", "result_state"]))
    lines.extend(_format_table("Quality Levels", catalog["quality_levels"], ["confidence_level", "rank", "display_name"]))
    lines.extend(_format_table("Quality Assessments", catalog["quality_assessments"], ["quality_assessment_id", "confidence_level", "flags"]))
    lines.extend(_format_table("Action Kinds", catalog["action_kinds"], ["action_kind", "display_name"]))
    lines.extend(_format_table("Action Records", catalog["action_records"], ["action_id", "action_kind", "priority", "action_state"]))
    lines.extend(_format_table("Playbooks", catalog["playbooks"], ["playbook_id", "playbook_kind", "status", "steps"]))
    lines.extend(_format_table("Routes", catalog["routes"], ["route_id", "route_kind", "enabled", "channels"]))
    lines.extend(_format_table("Delivery Channels", catalog["delivery_channels"], ["channel_id", "channel_kind", "status", "route_kinds"]))
    lines.extend(_format_table("Transport Adapters", catalog["transport_adapters"], ["transport_adapter_id", "transport_kind", "status", "channels"]))
    lines.extend(_format_table("Handling Labels", catalog["handling_labels"], ["label_id", "allowed_sharing_scopes", "requires_redaction"]))
    lines.extend(_format_table("Retention Classes", catalog["retention_classes"], ["retention_class", "default_duration", "allowed_states"]))
    lines.extend(_format_table("Integrity Receipts", catalog["integrity_receipts"], ["path", "digest_algorithm", "purpose"]))
    lines.extend(_format_table("Sharing Scopes", catalog["sharing_scopes"], ["scope_id", "display_name", "path"]))
    lines.extend(_format_table("Review Gates", catalog["review_gates"], ["gate_id", "display_name", "path"]))
    return "\n".join(lines)
