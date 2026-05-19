# Routing Policy

PFEM routing policy describes where records, actions, bundles, and summaries should go.

Routing answers:

```text
Given this kind of thing, with this scope, priority, and handling label, which node or profile should receive it?
```

## Routing is not transport

A routing policy does not send messages, open sockets, call APIs, publish MQTT, or create tickets.

It is the architecture map that tells an adapter, operator, agent, bridge, or future transport layer where something belongs.

## Why this matters

PFEM is pluralistic. It should support:

- local-only operation
- ad hoc mesh operation
- formal rollup paths
- civil or municipal dashboards
- site-specific dashboards
- independent review nodes
- research/test nodes

Routing policy prevents the design from hardcoding one central destination.

## Routing should stay separate from

- evidence
- actions
- playbooks
- exchange receipts
- federation messages
- transport adapters

A routing rule can guide where an action or bundle should go without rewriting the record itself.
