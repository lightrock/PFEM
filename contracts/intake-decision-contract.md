# Intake Decision Contract

A PFEM intake decision should identify:

- `intake_decision_id`
- `decision_kind`
- `created_time`
- `inbox_item_id`
- `decision`
- `reason_code`
- `decided_by_ref`
- `basis_refs`
- optional `resulting_inbox_state`
- `summary`

An intake decision is not the inbox item itself and not the exchange receipt. It is the receiver-side decision about whether a received/staged payload may move into exchange processing.
