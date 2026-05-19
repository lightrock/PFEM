# Handling and Redaction Contract

A shared PFEM record should identify:

- `sharing_scope`
- `handling_label`
- `redaction_state`

The handling policy maps labels to allowed sharing scopes and redaction states.

A federation message or rollup summary is valid only when its handling label permits its sharing scope and redaction state.
