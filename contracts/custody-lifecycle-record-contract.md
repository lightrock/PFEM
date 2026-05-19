# Custody Lifecycle Records Contract

A PFEM custody lifecycle records record should identify:

- `custody_lifecycle_record_id`
- `lifecycle_kind`
- `created_time`
- `node_id`
- `custody_chain_verification_receipt_id`
- `custody_ledger_verification_receipt_id`
- `custody_release_chain_verification_receipt_id`
- `lifecycle_state`
- `final_outcome`
- `lifecycle_refs`
- `subject_refs`
- `basis_refs`
- `digest_algorithm`
- `lifecycle_ref_digest`
- `summarized_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
