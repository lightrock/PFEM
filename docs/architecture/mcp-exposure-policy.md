# MCP Exposure Policy for PFEM Instances

PFEM is the evidence-governance architecture and boundary discipline. MCP is one possible exposure/interface layer.

A PFEM deployment may use local Python services, CLI tools, files, internal APIs, dashboards, queues, or other implementation mechanisms for internal work. It should expose only selected, bounded, earned capabilities through MCP-style tools/resources.

## Rule

Do not make everything MCP by default.

Ask:

```text
Should an AI client, operator workbench, coordinator, or adjacent system be allowed to discover and call this capability across a boundary?
```

If yes, consider MCP.

If no, keep the capability local/internal.

## Keep local/internal when the capability is

- boring implementation plumbing;
- high-frequency runtime work;
- unsafe to expose;
- not useful to AI directly;
- an implementation detail;
- latency-sensitive;
- secret-bearing;
- raw-state mutating;
- likely to confuse the external contract.

Examples:

- evidence normalizer;
- schema validator internals;
- raw file importer;
- cache manager;
- local packet decoder;
- database maintenance script;
- internal scoring routine;
- report renderer internals.

## Consider MCP exposure when the capability is

- useful to an AI/human workflow;
- well-bounded;
- schema-describable;
- auditable;
- policy-checkable;
- meaningful across a system boundary.

Examples:

- `pfem.evidence.lookup`;
- `pfem.package.read`;
- `pfem.package.draft`;
- `pfem.report.draft`;
- `pfem.rollup.read`;
- `pfem.mindgraph.lookup`;
- `pfem.evaluation.run` for non-operational checks.

## Exposure levels

Read-only tools should come first.

Draft/propose tools may come next.

Mutation, publish, send, delete, or operational tools require explicit policy, audit, authority context, and human approval where appropriate.

## One-sentence version

Expose PFEM capabilities through MCP only when crossing an AI/tool boundary is useful, safe, and governable; keep implementation doodads local unless they have earned an external callable contract.
