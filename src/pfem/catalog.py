"""PFEM catalog."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pfem.action import load_action_policy, load_action_records
from pfem.apply_receipt import load_apply_receipts
from pfem.adapter_runtime import load_adapter_registry
from pfem.audit import load_audit_events
from pfem.conflict_record import load_conflict_records
from pfem.bundle import load_exchange_bundle
from pfem.capability_runtime import load_capability_manifest
from pfem.delivery import load_delivery_channel_registry
from pfem.delivery_job import load_delivery_jobs
from pfem.dispatch import load_dispatch_policy
from pfem.dispatch_decision import load_dispatch_decisions
from pfem.doctor import find_repo_root
from pfem.example_runtime import load_example_registry
from pfem.exchange import load_exchange_receipts
from pfem.handling import load_handling_policy
from pfem.inbox import load_inbox_items
from pfem.import_record import load_import_records
from pfem.intake_decision import load_intake_decisions
from pfem.merge_decision import load_merge_decisions
from pfem.integrity import load_integrity_manifest
from pfem.node_runtime import load_node_registry
from pfem.outbox import load_outbox_items
from pfem.playbook import load_playbooks
from pfem.policy import load_sharing_policy
from pfem.profile_runtime import load_profile_registry
from pfem.quality import load_quality_assessments, load_quality_policy
from pfem.reconciliation import load_reconciliation_records
from pfem.recovery_point import load_recovery_points
from pfem.snapshot_manifest import load_snapshot_manifests
from pfem.snapshot_verification_receipt import load_snapshot_verification_receipts
from pfem.retention import load_retention_policy
from pfem.restore_plan import load_restore_plans
from pfem.restore_approval import load_restore_approvals
from pfem.review import load_review_records
from pfem.routing import load_routing_policy
from pfem.source_runtime import load_source_registry
from pfem.state_checkpoint import load_state_checkpoints
from pfem.state_transition import load_state_transitions
from pfem.transport import load_transport_adapter_registry
from pfem.transport_receipt import load_transport_receipts


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
    return [] if not p.exists() else [{"exchange_receipt_id": r.exchange_receipt_id, "receipt_kind": r.receipt_kind, "bundle_id": r.bundle_id, "decision": r.decision, "intake_decision_id": r.intake_decision_id or ""} for r in load_exchange_receipts(p)]


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


def _dispatch_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "dispatch" / "dispatch-policy.json"
    return [] if not p.exists() else [{"dispatch_rule_id": r.dispatch_rule_id, "enabled": r.enabled, "max_attempts": r.max_attempts, "retry_delay_seconds": r.retry_delay_seconds} for r in load_dispatch_policy(p).rules]


def _dispatch_decision_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "dispatch" / "dispatch-decisions.json"
    return [] if not p.exists() else [{"dispatch_decision_id": d.dispatch_decision_id, "delivery_job_id": d.delivery_job_id, "decision": d.decision, "reason_code": d.reason_code} for d in load_dispatch_decisions(p)]


def _outbox_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "outbox" / "outbox-items.json"
    return [] if not p.exists() else [{"outbox_item_id": o.outbox_item_id, "delivery_job_id": o.delivery_job_id, "outbox_state": o.outbox_state, "item_kind": o.item_kind} for o in load_outbox_items(p)]


def _inbox_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "inbox" / "inbox-items.json"
    return [] if not p.exists() else [{"inbox_item_id": i.inbox_item_id, "transport_receipt_id": i.transport_receipt_id, "inbox_state": i.inbox_state, "item_kind": i.item_kind} for i in load_inbox_items(p)]


def _import_record_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "imports" / "import-records.json"
    return [] if not p.exists() else [{"import_record_id": r.import_record_id, "exchange_receipt_id": r.exchange_receipt_id, "import_state": r.import_state, "import_kind": r.import_kind} for r in load_import_records(p)]


def _conflict_record_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "conflicts" / "conflict-records.json"
    return [] if not p.exists() else [{"conflict_record_id": r.conflict_record_id, "import_record_id": r.import_record_id, "conflict_state": r.conflict_state, "severity": r.severity} for r in load_conflict_records(p)]


def _apply_receipt_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "apply" / "apply-receipts.json"
    return [] if not p.exists() else [{"apply_receipt_id": r.apply_receipt_id, "merge_decision_id": r.merge_decision_id, "apply_state": r.apply_state, "receipt_kind": r.receipt_kind} for r in load_apply_receipts(p)]


def _state_checkpoint_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "state" / "state-checkpoints.json"
    return [] if not p.exists() else [{"state_checkpoint_id": c.state_checkpoint_id, "node_id": c.node_id, "checkpoint_state": c.checkpoint_state, "included_refs": len(c.included_refs)} for c in load_state_checkpoints(p)]


def _state_transition_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "state" / "state-transitions.json"
    return [] if not p.exists() else [{"state_transition_id": t.state_transition_id, "to_state_checkpoint_id": t.to_state_checkpoint_id, "transition_state": t.transition_state, "changed_refs": len(t.changed_refs)} for t in load_state_transitions(p)]


def _snapshot_manifest_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "snapshots" / "snapshot-manifests.json"
    return [] if not p.exists() else [{"snapshot_manifest_id": m.snapshot_manifest_id, "state_checkpoint_id": m.state_checkpoint_id, "snapshot_state": m.snapshot_state, "items": len(m.items)} for m in load_snapshot_manifests(p)]


def _snapshot_verification_receipt_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "snapshots" / "snapshot-verification-receipts.json"
    return [] if not p.exists() else [{"snapshot_verification_receipt_id": r.snapshot_verification_receipt_id, "snapshot_manifest_id": r.snapshot_manifest_id, "verification_state": r.verification_state, "checked_items": len(r.checked_item_refs)} for r in load_snapshot_verification_receipts(p)]


def _recovery_point_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "recovery" / "recovery-points.json"
    return [] if not p.exists() else [{"recovery_point_id": r.recovery_point_id, "snapshot_verification_receipt_id": r.snapshot_verification_receipt_id, "recovery_state": r.recovery_state, "restore_scope": r.restore_scope} for r in load_recovery_points(p)]


def _restore_plan_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "restore" / "restore-plans.json"
    return [] if not p.exists() else [{"restore_plan_id": r.restore_plan_id, "recovery_point_id": r.recovery_point_id, "plan_state": r.plan_state, "restore_scope": r.restore_scope} for r in load_restore_plans(p)]


def _restore_approval_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "restore" / "restore-approvals.json"
    return [] if not p.exists() else [{"restore_approval_id": a.restore_approval_id, "restore_plan_id": a.restore_plan_id, "approval_state": a.approval_state, "approved_scope": a.approved_scope} for a in load_restore_approvals(p)]


def _merge_decision_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "merge" / "merge-decisions.json"
    return [] if not p.exists() else [{"merge_decision_id": d.merge_decision_id, "import_record_id": d.import_record_id, "decision": d.decision, "reason_code": d.reason_code} for d in load_merge_decisions(p)]


def _intake_decision_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "intake" / "intake-decisions.json"
    return [] if not p.exists() else [{"intake_decision_id": d.intake_decision_id, "inbox_item_id": d.inbox_item_id, "decision": d.decision, "reason_code": d.reason_code} for d in load_intake_decisions(p)]


def _routing_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "routing" / "routing-policy.json"
    return [] if not p.exists() else [{"route_id": route.route_id, "route_kind": route.route_kind, "enabled": route.enabled, "channels": len(route.allowed_delivery_channel_ids)} for route in load_routing_policy(p).routes]


def _delivery_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "delivery" / "delivery-channel-registry.json"
    return [] if not p.exists() else [{"channel_id": c.channel_id, "channel_kind": c.channel_kind, "status": c.status, "route_kinds": ",".join(c.supports_route_kinds)} for c in load_delivery_channel_registry(p).channels]


def _delivery_job_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "delivery" / "delivery-jobs.json"
    return [] if not p.exists() else [{"delivery_job_id": j.delivery_job_id, "dispatch_rule_id": j.dispatch_rule_id or "", "job_state": j.job_state, "priority": j.priority} for j in load_delivery_jobs(p)]


def _transport_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "transport" / "transport-adapter-registry.json"
    return [] if not p.exists() else [{"transport_adapter_id": t.transport_adapter_id, "transport_kind": t.transport_kind, "status": t.status, "channels": ",".join(t.delivery_channel_ids)} for t in load_transport_adapter_registry(p).adapters]


def _transport_receipt_rows(root: Path) -> list[dict[str, Any]]:
    p = root / "transport" / "transport-receipts.json"
    return [] if not p.exists() else [{"transport_receipt_id": r.transport_receipt_id, "outbox_item_id": r.outbox_item_id, "transport_adapter_id": r.transport_adapter_id, "transport_state": r.transport_state} for r in load_transport_receipts(p)]


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
        "dispatch_rules": _dispatch_rows(root),
        "dispatch_decisions": _dispatch_decision_rows(root),
        "outbox_items": _outbox_rows(root),
        "inbox_items": _inbox_rows(root),
        "import_records": _import_record_rows(root),
        "conflict_records": _conflict_record_rows(root),
        "apply_receipts": _apply_receipt_rows(root),
        "state_checkpoints": _state_checkpoint_rows(root),
        "state_transitions": _state_transition_rows(root),
        "snapshot_manifests": _snapshot_manifest_rows(root),
        "snapshot_verification_receipts": _snapshot_verification_receipt_rows(root),
        "recovery_points": _recovery_point_rows(root),
        "restore_plans": _restore_plan_rows(root),
        "restore_approvals": _restore_approval_rows(root),
        "merge_decisions": _merge_decision_rows(root),
        "intake_decisions": _intake_decision_rows(root),
        "routes": _routing_rows(root),
        "delivery_channels": _delivery_rows(root),
        "delivery_jobs": _delivery_job_rows(root),
        "transport_adapters": _transport_rows(root),
        "transport_receipts": _transport_receipt_rows(root),
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
        f"{counts.get('sources', 0)} sources, {counts.get('dispatch_rules', 0)} dispatch rules, "
        f"{counts.get('dispatch_decisions', 0)} dispatch decisions, "
        f"{counts.get('outbox_items', 0)} outbox items, "
        f"{counts.get('inbox_items', 0)} inbox items, "
        f"{counts.get('import_records', 0)} import records, "
        f"{counts.get('conflict_records', 0)} conflict records, "
        f"{counts.get('apply_receipts', 0)} apply receipts, "
        f"{counts.get('state_checkpoints', 0)} state checkpoints, "
        f"{counts.get('state_transitions', 0)} state transitions, "
        f"{counts.get('snapshot_manifests', 0)} snapshot manifests, "
        f"{counts.get('snapshot_verification_receipts', 0)} snapshot verification receipts, "
        f"{counts.get('recovery_points', 0)} recovery points, "
        f"{counts.get('restore_plans', 0)} restore plans, "
        f"{counts.get('restore_approvals', 0)} restore approvals, "
        f"{counts.get('merge_decisions', 0)} merge decisions, "
        f"{counts.get('intake_decisions', 0)} intake decisions, "
        f"{counts.get('routes', 0)} routes, {counts.get('delivery_channels', 0)} delivery channels, "
        f"{counts.get('delivery_jobs', 0)} delivery jobs, "
        f"{counts.get('transport_adapters', 0)} transport adapters, "
        f"{counts.get('transport_receipts', 0)} transport receipts",
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
    lines.extend(_format_table("Exchange Receipts", catalog["exchange_receipts"], ["exchange_receipt_id", "receipt_kind", "bundle_id", "decision", "intake_decision_id"]))
    lines.extend(_format_table("Reconciliation Records", catalog["reconciliation_records"], ["reconciliation_id", "reconciliation_kind", "decision", "result_state"]))
    lines.extend(_format_table("Quality Levels", catalog["quality_levels"], ["confidence_level", "rank", "display_name"]))
    lines.extend(_format_table("Quality Assessments", catalog["quality_assessments"], ["quality_assessment_id", "confidence_level", "flags"]))
    lines.extend(_format_table("Action Kinds", catalog["action_kinds"], ["action_kind", "display_name"]))
    lines.extend(_format_table("Action Records", catalog["action_records"], ["action_id", "action_kind", "priority", "action_state"]))
    lines.extend(_format_table("Playbooks", catalog["playbooks"], ["playbook_id", "playbook_kind", "status", "steps"]))
    lines.extend(_format_table("Dispatch Rules", catalog["dispatch_rules"], ["dispatch_rule_id", "enabled", "max_attempts", "retry_delay_seconds"]))
    lines.extend(_format_table("Dispatch Decisions", catalog["dispatch_decisions"], ["dispatch_decision_id", "delivery_job_id", "decision", "reason_code"]))
    lines.extend(_format_table("Outbox Items", catalog["outbox_items"], ["outbox_item_id", "delivery_job_id", "outbox_state", "item_kind"]))
    lines.extend(_format_table("Inbox Items", catalog["inbox_items"], ["inbox_item_id", "transport_receipt_id", "inbox_state", "item_kind"]))
    lines.extend(_format_table("Import Records", catalog["import_records"], ["import_record_id", "exchange_receipt_id", "import_state", "import_kind"]))
    lines.extend(_format_table("Conflict Records", catalog["conflict_records"], ["conflict_record_id", "import_record_id", "conflict_state", "severity"]))
    lines.extend(_format_table("Apply Receipts", catalog["apply_receipts"], ["apply_receipt_id", "merge_decision_id", "apply_state", "receipt_kind"]))
    lines.extend(_format_table("State Checkpoints", catalog["state_checkpoints"], ["state_checkpoint_id", "node_id", "checkpoint_state", "included_refs"]))
    lines.extend(_format_table("State Transitions", catalog["state_transitions"], ["state_transition_id", "to_state_checkpoint_id", "transition_state", "changed_refs"]))
    lines.extend(_format_table("Snapshot Manifests", catalog["snapshot_manifests"], ["snapshot_manifest_id", "state_checkpoint_id", "snapshot_state", "items"]))
    lines.extend(_format_table("Snapshot Verification Receipts", catalog["snapshot_verification_receipts"], ["snapshot_verification_receipt_id", "snapshot_manifest_id", "verification_state", "checked_items"]))
    lines.extend(_format_table("Recovery Points", catalog["recovery_points"], ["recovery_point_id", "snapshot_verification_receipt_id", "recovery_state", "restore_scope"]))
    lines.extend(_format_table("Restore Plans", catalog["restore_plans"], ["restore_plan_id", "recovery_point_id", "plan_state", "restore_scope"]))
    lines.extend(_format_table("Restore Approvals", catalog["restore_approvals"], ["restore_approval_id", "restore_plan_id", "approval_state", "approved_scope"]))
    lines.extend(_format_table("Merge Decisions", catalog["merge_decisions"], ["merge_decision_id", "import_record_id", "decision", "reason_code"]))
    lines.extend(_format_table("Intake Decisions", catalog["intake_decisions"], ["intake_decision_id", "inbox_item_id", "decision", "reason_code"]))
    lines.extend(_format_table("Routes", catalog["routes"], ["route_id", "route_kind", "enabled", "channels"]))
    lines.extend(_format_table("Delivery Channels", catalog["delivery_channels"], ["channel_id", "channel_kind", "status", "route_kinds"]))
    lines.extend(_format_table("Delivery Jobs", catalog["delivery_jobs"], ["delivery_job_id", "dispatch_rule_id", "job_state", "priority"]))
    lines.extend(_format_table("Transport Adapters", catalog["transport_adapters"], ["transport_adapter_id", "transport_kind", "status", "channels"]))
    lines.extend(_format_table("Transport Receipts", catalog["transport_receipts"], ["transport_receipt_id", "outbox_item_id", "transport_adapter_id", "transport_state"]))
    lines.extend(_format_table("Handling Labels", catalog["handling_labels"], ["label_id", "allowed_sharing_scopes", "requires_redaction"]))
    lines.extend(_format_table("Retention Classes", catalog["retention_classes"], ["retention_class", "default_duration", "allowed_states"]))
    lines.extend(_format_table("Integrity Receipts", catalog["integrity_receipts"], ["path", "digest_algorithm", "purpose"]))
    lines.extend(_format_table("Sharing Scopes", catalog["sharing_scopes"], ["scope_id", "display_name", "path"]))
    lines.extend(_format_table("Review Gates", catalog["review_gates"], ["gate_id", "display_name", "path"]))
    return "\n".join(lines)
