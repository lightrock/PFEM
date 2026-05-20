# PFEM New Chat Handoff

Use this file when starting a new ChatGPT tab, Codex session, or human review.

## First instruction to the new chat

```text
We are working in the PFEM repository: lightrock/PFEM.
Before proposing or generating changes, inspect the current repo state on main and read:
- AGENTS.md
- docs/developer/pfem-boundary-language-generation-standard.md
- docs/developer/pfem-terminal-tail-stabilization.md
- docs/developer/pfem-new-chat-handoff.md
- tools/pfem_check_manifest.json

Do not rely only on conversation memory.
```

## Current state

The permanent-archive terminal record-species chain has reached its semantic endcap:

```text
retention permanent archive terminal closure final endcap closeout records
```

The terminal tail stabilization audit guards that endcap and the `missing_refs` schema rule.

## Do not blindly continue 50-batches

More record species are allowed only when one of these is true:

```text
a gate exposes a real missing boundary
a documented PFEM domain workflow is incomplete
a previous batch stopped halfway through a record / verification / closeout triple
a human deliberately opens a new chain
```

If none of those are true, the next work is:

```text
stabilization
speed
cleanup
catalog readability
developer documentation
full gate
release/tag
```

## Current operating pattern

During focused patch work:

```text
apply patch
run focused validators
run audit/schema/integrity/catalog/doctor/quick
write git status to build/pfem-patch-status/
commit
push
verify main
```

During release work:

```text
pfem_check.bat --full --timings
inspect slowest checks
fix real failures
do not generate fake refs just to satisfy a schema
```

## Known gotcha: missing_refs

`missing_refs` must not be required for passed verification receipt schemas.

Correct pattern:

```json
{
  "verification_state": "passed",
  "missing_refs": []
}
```

Schema pattern:

```json
"properties": {
  "missing_refs": { "type": "array" }
}
```

but:

```text
missing_refs is not in required
```

## Human sanity rule

If the assistant starts inventing more terminal/endcap/final/final-final/final-final-final record species without a concrete reason, stop it and make it run the gate.
- `docs/developer/pfem-architecture-theory-notes.md`
- docs/developer/pfem-ai-patch-safety-rules.md
