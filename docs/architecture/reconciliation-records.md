# Reconciliation Records

PFEM reconciliation records describe how disagreement, correction, merge, supersession, or unresolved conflict is handled.

In a mesh/federated environment, two nodes may report different things, a later record may correct an earlier record, or an accepted bundle may supersede an older bundle.

A reconciliation record answers:

```text
What records are in tension, what basis was used, and what result state should downstream users understand?
```

## Reconciliation is for

- conflicting observations
- corrected records
- merged records
- superseded bundles/messages
- rejected handoffs
- unresolved disputes

## Reconciliation is not

- truth by decree
- authentication
- transport
- legal adjudication

It is an architecture guardrail so PFEM does not silently flatten disagreement.
