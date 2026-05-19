# Transport Adapters

Transport adapters are named implementation hooks for actually moving PFEM records.

Routing policy says where something should go.

Delivery channels say what movement methods are allowed.

Transport adapters say which concrete implementation hook may perform that movement.

This registry still does not implement transport. It names the hooks and validates that they refer to known delivery channels, nodes, scopes, and handling labels.

Current file:

```text
transport/transport-adapter-registry.json
```
