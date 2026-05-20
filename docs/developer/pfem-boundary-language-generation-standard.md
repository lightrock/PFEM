# PFEM Boundary-Language Generation Standard

This file exists so a new chat, Codex session, or human contributor does not have to recover PFEM's generated-boundary rules from conversation history.

PFEM uses three related terms:

```text
record species       the formal PFEM record type or semantic niche
generated boundary  the complete implementation bundle for that species
boundary language   the formal vocabulary and rules for these boundaries
```

A PFEM record species is not just a JSON file. A valid generated boundary includes data, schema, validation code, tool wiring, audit/catalog/doctor integration, docs, contracts, tests, and gate coverage.

## Naming

Use a real domain noun phrase as the stem.

Examples:

```text
permanent_archive_terminal_closure_final_endcap
permanent_archive_terminal_closure_final_summary
retention_public_access_register
```

Use these two projections consistently:

```text
snake_case: permanent_archive_terminal_closure_final_endcap
hyphen-case: permanent-archive-terminal-closure-final-endcap
```

## Standard generated boundary types

Most PFEM generated boundaries are one of these:

```text
record
verification_receipt
closeout_record
```

The normal three-step boundary is:

```text
retention <stem> records
retention <stem> verification receipts
retention <stem> closeout records
```

If a batch stops halfway through a three-step boundary, the next batch must resume that exact boundary before inventing a new stem.

## Required files for a generated boundary

For a `record` boundary:

```text
retention/retention-<stem-hyphen>-records.json
schemas/retention_<stem>_record.schema.json
src/pfem/retention_<stem>_record.py
tools/pfem_retention_<stem>_records.py
tests/unit/test_retention_<stem>_records.py
docs/architecture/retention-<stem-hyphen>-records.md
contracts/retention-<stem-hyphen>-record-contract.md
```

For a `verification_receipt` boundary:

```text
retention/retention-<stem-hyphen>-verification-receipts.json
schemas/retention_<stem>_verification_receipt.schema.json
src/pfem/retention_<stem>_verification_receipt.py
tools/pfem_retention_<stem>_verification_receipts.py
tests/unit/test_retention_<stem>_verification_receipts.py
docs/architecture/retention-<stem-hyphen>-verification-receipts.md
contracts/retention-<stem-hyphen>-verification-receipt-contract.md
```

For a `closeout_record` boundary:

```text
retention/retention-<stem-hyphen>-closeout-records.json
schemas/retention_<stem>_closeout_record.schema.json
src/pfem/retention_<stem>_closeout_record.py
tools/pfem_retention_<stem>_closeout_records.py
tests/unit/test_retention_<stem>_closeout_records.py
docs/architecture/retention-<stem-hyphen>-closeout-records.md
contracts/retention-<stem-hyphen>-closeout-record-contract.md
```

## Required cross-file updates

Every generated boundary must be wired into:

```text
audit/audit-journal.json
src/pfem/audit.py
src/pfem/schema_contracts.py
src/pfem/integrity.py
src/pfem/catalog.py
src/pfem/doctor.py
tools/pfem_check_manifest.json
```

Do not leave a validator as an orphan tool. If the boundary matters, it must be visible to the PFEM check manifest.

## Verification receipt rule

`missing_refs` is a diagnostic field.

For passed verification receipts:

```json
"verification_state": "passed",
"missing_refs": []
```

Schema rule:

```text
missing_refs should be present as an optional array property.
missing_refs should not be listed in required for passed verification receipt schemas.
```

Why: the schema-contract checker treats empty required arrays as missing. PFEM has already hit this failure mode during terminal closure/endcap work. Do not repeat it.

## Runtime and launcher rule

Do not add root-level `pfem_*.bat` wrapper churn.

Allowed root PFEM launcher:

```text
pfem_check.bat
```

Linux launcher:

```text
pfem_check.sh
```

New checks belong in:

```text
tools/<tool>.py
tools/pfem_check_manifest.json
```

The launcher pair should remain bound by tests. If one launcher changes, update the other intentionally.

## Patch-output rule

Do not dump giant `git status --short` output into the operator's terminal at the end of a patch.

Write status files under:

```text
build/pfem-patch-status/
```

Then print the status-file path.

## Normal focused check sequence

For a generated-boundary patch, run focused checks first:

```text
new generated validators
new unit tests
tools/pfem_audit.py
tools/pfem_schema_contracts.py
tools/pfem_integrity_update.py
tools/pfem_integrity.py
tools/pfem_catalog.py
tools/pfem_doctor.py
pfem_check.bat --quick --timings
```

Do not demand a full gate after every generated-boundary batch. Use focused gates during generation and a full gate at stabilization/release boundaries.

## Full gate timing

Run the full gate when:

```text
a chain is semantically closed
a release/tag is being prepared
a generator/standard changes
a broad refactor changes check plumbing
```

## Stop condition

Do not keep generating record species just because generation is easy.

Stop adding record species when the chain reaches a real semantic endcap.

For the current permanent-archive terminal tail, the endcap is:

```text
retention permanent archive terminal closure final endcap closeout records
```

After an endcap, the next work should be stabilization, speed, cleanup, docs, and full-gate/release work unless a gate exposes a real missing boundary.
