# Exchange Receipts

Exchange receipts record what happened to a PFEM bundle.

A bundle says:

```text
This is what should travel together.
```

An exchange receipt says:

```text
This bundle was exported, transmitted, received, accepted, rejected, or superseded.
```

## Rules

- A receipt should reference a known bundle id.
- A receipt should reference known sender and recipient node ids.
- A receipt should reference known record ids or artifact paths.
- A receipt should use a known receipt kind.
- A receipt is not a transport protocol, authentication method, or legal signature.
- It is a handoff/audit hook for the architecture.
