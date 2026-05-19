# Delivery Channels

PFEM delivery channels describe how records may move between nodes.

Routing policy says:

```text
Where should this go?
```

Delivery channels say:

```text
What movement methods are available or allowed?
```

## Delivery channels are not implementations

A delivery channel record does not send data. It does not open a socket, publish MQTT, call an API, send email, or write files.

It is a registry entry that lets routing policy and future transport adapters agree on names and constraints.

## Example delivery channel kinds

- `manual_export`
- `file_drop`
- `api`
- `mqtt`
- `email`
- `mesh_message`
- `dashboard_sync`

## Why this matters

PFEM needs to support different operational realities:

- a local-only workstation
- a ham or volunteer using manual export/import
- a field node with intermittent mesh
- a facility dashboard
- a formal rollup node
- a municipal/civil view
- future API or brokered integration

Delivery channels let PFEM name those movement options without hardcoding one implementation.
