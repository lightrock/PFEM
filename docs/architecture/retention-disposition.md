# Retention and Disposition

PFEM retention policy names how records should be kept and what should happen next.

Retention answers:

```text
How long should this record class normally be kept?
```

Disposition answers:

```text
What state is this record in now: active, review-due, archived, legal-hold, purge-eligible, or purged?
```

## Rules

- Shared packages, rollups, and federation messages should carry `retention_class`.
- Shared packages, rollups, and federation messages should carry `disposition_state`.
- The `retention_class` must be known.
- The `disposition_state` must be allowed for that retention class.
- Legal hold should override normal purge.
- Retention policy is not deletion, law, or secure storage by itself. It is an architecture guardrail.
