# Transport Adapters

PFEM transport adapters are named implementation hooks for moving PFEM records.

The boundary is:

```text
routing policy    = where should it go?
delivery channel  = what movement method is allowed?
transport adapter = what implementation hook may move it?
```

## Transport adapters are not evidence adapters

PFEM already has adapters that translate outside systems into PFEM records.

Transport adapters are different. They move PFEM records between PFEM nodes or external handoff destinations.

## Transport adapters still do not move data in this seed

The registry names possible hooks and validates their references.

Actual transport code can come later, such as:

- manual export/import helper
- file-drop writer/reader
- local API client/server
- MQTT bridge
- email handoff generator
- mesh-message bridge
- dashboard sync job

## Why this matters

PFEM should not confuse architecture policy with implementation.

A node may have many possible channels, and a channel may later have different transport implementations. The registry gives AI agents and future developers a place to attach the implementation without rewriting evidence, action, routing, or delivery records.
