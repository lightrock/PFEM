# Federation Topology

Node identity tells PFEM which nodes exist.

Federation topology tells PFEM which node-to-node links are allowed.

A topology link answers:

```text
Can node A send this kind of message to node B under this sharing scope?
```

## Rules

- A topology link should reference known node ids.
- A topology link should use known sharing scopes.
- A topology link may reference a known review gate.
- A federation message should identify sender and recipients.
- A federation message should match an allowed topology link.
- Topology is not authentication. It is an architecture-level routing/permission map.
