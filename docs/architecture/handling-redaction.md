# Handling and Redaction

PFEM separates sharing scope from handling label.

Sharing scope answers:

```text
Where may this record go?
```

Handling label answers:

```text
How carefully must this record be treated before it goes there?
```

## Rules

- Rollup summaries and federation messages should carry a known `handling_label`.
- Rollup summaries and federation messages should carry a `redaction_state`.
- The record's `sharing_scope` should be allowed by the handling label.
- If a handling label requires redaction before sharing, the record's redaction state must be one of that label's allowed redaction states.
- Handling policy is not encryption, authentication, classification law, or legal approval. It is an architecture guardrail.
