"""PFEM catalog."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pfem.adapter_runtime import load_adapter_registry
from pfem.audit import load_audit_events
from pfem.bundle import load_exchange_bundle
from pfem.capability_runtime import load_capability_manifest
from pfem.doctor import find_repo_root
from pfem.example_runtime import load_example_registry
from pfem.exchange import load_exchange_receipts
from pfem.handling import load_handling_policy
from pfem.integrity import load_integrity_manifest
from pfem.node_runtime import load_node_registry
from pfem.policy import load_sharing_policy
from pfem.profile_runtime import load_profile_registry
from pfem.reconciliation import load_reconciliation_records
from pfem.retention import load_retention_policy
from pfem.review import load_review_records
from pfem.source_runtime import load_source_registry


def _capability_rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((root / "capabilities").rglob("*.capability.yaml")) if (root / "capabilities").exists() else []:
        manifest = load_capability_manifest(path)
        rows.append({"capability_id": manifest.capability_id, "capability_kind": manifest.capability_kind, "path": str(path.relative_to(root))})
    return rows


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
    rows: list[dict[str, Any]] = []
    bundles_dir = root / "bundles"
    if not bundles_dir.exists():
        return rows
    for path in sorted(bundles_dir.glob("**/*.bundle.json")):
        bundle = load_exchange_bundle(path)
        rows.append({"bundle_id": bundle.bundle_id, "bundle_kind": bundle.bundle_kind, "sharing_scope": bundle.sharing_scope, "path": str(path.relative_to(root))})
    return rows


def _exchange_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "exchange" / "exchange-receipts.json"
    if not p.exists():
        return []
    return [{"exchange_receipt_id": r.exchange_receipt_id, "receipt_kind": r.receipt_kind, "bundle_id": r.bundle_id, "decision": r.decision} for r in load_exchange_receipts(p)]


def _reconciliation_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "reconciliation" / "reconciliation-records.json"
    if not p.exists():
        return []
    return [
        {
            "reconciliation_id": r.reconciliation_id,
            "reconciliation_kind": r.reconciliation_kind,
            "decision": r.decision,
            "result_state": r.result_state,
        }
        for r in load_reconciliation_records(p)
    ]


def _handling_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "handling" / "handling-policy.json"
    if not p.exists():
        return []
    policy = load_handling_policy(p)
    return [{"label_id": label.label_id, "allowed_sharing_scopes": ",".join(label.allowed_sharing_scopes), "requires_redaction": label.requires_redaction_before_share} for label in policy.handling_labels]


def _retention_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "retention" / "retention-policy.json"
    if not p.exists():
        return []
    policy = load_retention_policy(p)
    return [{"retention_class": item.retention_class, "default_duration": item.default_duration, "allowed_states": ",".join(item.allowed_disposition_states)} for item in policy.retention_classes]


def _integrity_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "integrity" / "receipt-manifest.json"
    if not p.exists():
        return []
    manifest = load_integrity_manifest(p)
    return [{"path": r.path, "digest_algorithm": r.digest_algorithm, "purpose": r.purpose} for r in manifest.receipts]


def _policy_rows(root: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    p = root / "policy" / "sharing-policy.json"
    if not p.exists():
        return [], []
    policy = load_sharing_policy(p)
    scopes = [{"scope_id": s.scope_id, "display_name": s.display_name, "path": str(p.relative_to(root))} for s in policy.sharing_scopes]
    gates = [{"gate_id": g.gate_id, "display_name": g.display_name, "path": str(p.relative_to(root))} for g in policy.review_gates]
    return scopes, gates


def build_catalog(start: str | Path | None = None) -> dict[str, Any]:
    root = find_repo_root(start)
    capabilities = _capability_rows(root)
    adapters = _adapter_rows(root)
    profiles = _profile_rows(root)
    nodes = _node_rows(root)
    sources = _source_rows(root)
    examples = _example_rows(root)
    reviews = _review_rows(root)
    audit_events = _audit_rows(root)
    bundles = _bundle_rows(root)
    exchange_receipts = _exchange_rows(root)
    reconciliation_records = _reconciliation_rows(root)
    handling_labels = _handling_rows(root)
    retention_classes = _retention_rows(root)
    integrity_receipts = _integrity_rows(root)
    sharing_scopes, review_gates = _policy_rows(root)

    return {
        "root": str(root),
        "counts": {
            "capabilities": len(capabilities), "adapters": len(adapters), "profiles": len(profiles),
            "nodes": len(nodes), "sources": len(sources), "examples": len(examples),
            "reviews": len(reviews), "audit_events": len(audit_events), "bundles": len(bundles),
            "exchange_receipts": len(exchange_receipts),
            "reconciliation_records": len(reconciliation_records),
            "handling_labels": len(handling_labels), "retention_classes": len(retention_classes),
            "integrity_receipts": len(integrity_receipts), "sharing_scopes": len(sharing_scopes),
            "review_gates": len(review_gates),
        },
        "capabilities": capabilities, "adapters": adapters, "profiles": profiles, "nodes": nodes,
        "sources": sources, "examples": examples, "reviews": reviews, "audit_events": audit_events,
        "bundles": bundles, "exchange_receipts": exchange_receipts,
        "reconciliation_records": reconciliation_records,
        "handling_labels": handling_labels, "retention_classes": retention_classes,
        "integrity_receipts": integrity_receipts, "sharing_scopes": sharing_scopes, "review_gates": review_gates,
    }


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
        f"{counts['capabilities']} capabilities, {counts['adapters']} adapters, "
        f"{counts['profiles']} profiles, {counts['nodes']} nodes, {counts['sources']} sources, "
        f"{counts['examples']} examples, {counts['reviews']} reviews, {counts['audit_events']} audit events, "
        f"{counts['bundles']} bundles, {counts['exchange_receipts']} exchange receipts, "
        f"{counts['reconciliation_records']} reconciliation records, "
        f"{counts['handling_labels']} handling labels, {counts['retention_classes']} retention classes, "
        f"{counts['integrity_receipts']} integrity receipts, {counts['sharing_scopes']} sharing scopes, "
        f"{counts['review_gates']} review gates",
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
    lines.extend(_format_table("Handling Labels", catalog["handling_labels"], ["label_id", "allowed_sharing_scopes", "requires_redaction"]))
    lines.extend(_format_table("Retention Classes", catalog["retention_classes"], ["retention_class", "default_duration", "allowed_states"]))
    lines.extend(_format_table("Integrity Receipts", catalog["integrity_receipts"], ["path", "digest_algorithm", "purpose"]))
    lines.extend(_format_table("Sharing Scopes", catalog["sharing_scopes"], ["scope_id", "display_name", "path"]))
    lines.extend(_format_table("Review Gates", catalog["review_gates"], ["gate_id", "display_name", "path"]))
    return "\n".join(lines)
