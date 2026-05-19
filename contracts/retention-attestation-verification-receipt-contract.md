# Retention Attestation Verification Receipts Contract

A PFEM retention attestation verification receipts record should identify:

- `retention_attestation_verification_receipt_id`
- `receipt_kind`
- `created_time`
- `node_id`
- `retention_attestation_record_id`
- `retention_completion_closeout_record_id`
- `verification_state`
- `checked_attestation_refs`
- `checked_subject_refs`
- `basis_refs`
- `digest_algorithm`
- `expected_attestation_ref_digest`
- `actual_attestation_ref_digest`
- `verified_by_ref`
- `summary`

This record keeps its boundary separate from the preceding PFEM artifact.
