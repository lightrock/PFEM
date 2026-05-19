"""PFEM catalog."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pfem.adapter_runtime import load_adapter_registry
from pfem.capability_runtime import load_capability_manifest
from pfem.doctor import find_repo_root
from pfem.example_runtime import load_example_registry
from pfem.node_runtime import load_node_registry
from pfem.policy import load_sharing_policy
from pfem.profile_runtime import load_profile_registry
from pfem.source_runtime import load_source_registry


def _capability_rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted((root / "capabilities").rglob("*.capability.yaml")) if (root / "capabilities").exists() else []:
        manifest = load_capability_manifest(path)
        rows.append({"capability_id": manifest.capability_id, "capability_kind": manifest.capability_kind, "path": str(path.relative_to(root))})
    return rows


def _adapter_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "adapters" / "adapter-registry.json"
    if not p.exists():
        return []
    return [{"adapter_id": e.adapter_id, "adapter_kind": e.adapter_kind, "status": e.status, "path": e.path} for e in load_adapter_registry(p).adapters]


def _profile_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "profiles" / "profile-registry.json"
    if not p.exists():
        return []
    return [{"profile_id": e.profile_id, "profile_kind": e.profile_kind, "status": e.status, "path": e.path} for e in load_profile_registry(p).profiles]


def _node_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "nodes" / "node-registry.json"
    if not p.exists():
        return []
    return [{"node_id": e.node_id, "profile_id": e.profile_id, "status": e.status, "path": e.path} for e in load_node_registry(p).nodes]


def _source_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "sources" / "source-registry.json"
    if not p.exists():
        return []
    return [
        {
            "source_id": e.source_id,
            "source_kind": e.source_kind,
            "adapter_id": e.adapter_id,
            "node_id": e.node_id,
            "status": e.status,
        }
        for e in load_source_registry(p).sources
    ]


def _example_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "examples" / "example-registry.json"
    if not p.exists():
        return []
    return [{"example_id": e.example_id, "profile_id": e.profile_id, "runnable": e.runnable, "status": e.status, "path": e.path} for e in load_example_registry(p).examples]


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
    sharing_scopes, review_gates = _policy_rows(root)

    return {
        "root": str(root),
        "counts": {
            "capabilities": len(capabilities),
            "adapters": len(adapters),
            "profiles": len(profiles),
            "nodes": len(nodes),
            "sources": len(sources),
            "examples": len(examples),
            "sharing_scopes": len(sharing_scopes),
            "review_gates": len(review_gates),
        },
        "capabilities": capabilities,
        "adapters": adapters,
        "profiles": profiles,
        "nodes": nodes,
        "sources": sources,
        "examples": examples,
        "sharing_scopes": sharing_scopes,
        "review_gates": review_gates,
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
        f"{counts['capabilities']} capabilities, "
        f"{counts['adapters']} adapters, "
        f"{counts['profiles']} profiles, "
        f"{counts['nodes']} nodes, "
        f"{counts['sources']} sources, "
        f"{counts['examples']} examples, "
        f"{counts['sharing_scopes']} sharing scopes, "
        f"{counts['review_gates']} review gates",
    ]
    lines.extend(_format_table("Capabilities", catalog["capabilities"], ["capability_id", "capability_kind", "path"]))
    lines.extend(_format_table("Adapters", catalog["adapters"], ["adapter_id", "adapter_kind", "status", "path"]))
    lines.extend(_format_table("Profiles", catalog["profiles"], ["profile_id", "profile_kind", "status", "path"]))
    lines.extend(_format_table("Nodes", catalog["nodes"], ["node_id", "profile_id", "status", "path"]))
    lines.extend(_format_table("Sources", catalog["sources"], ["source_id", "source_kind", "adapter_id", "node_id", "status"]))
    lines.extend(_format_table("Examples", catalog["examples"], ["example_id", "profile_id", "runnable", "status", "path"]))
    lines.extend(_format_table("Sharing Scopes", catalog["sharing_scopes"], ["scope_id", "display_name", "path"]))
    lines.extend(_format_table("Review Gates", catalog["review_gates"], ["gate_id", "display_name", "path"]))
    return "\n".join(lines)
