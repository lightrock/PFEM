# Exchange Receipt Intake Linkage Contract

A PFEM exchange receipt may identify receiver-side provenance fields when applicable:

- `transport_receipt_id`
- `outbox_item_id`
- `inbox_item_id`
- `intake_decision_id`
- `basis_refs`

For accepted or rejected inbound exchange receipts, these fields should point back to the received/staged payload path whenever known.

This does not replace inbox items or intake decisions. It lets the exchange receipt cite them.
