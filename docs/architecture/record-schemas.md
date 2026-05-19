# Record Schemas

PFEM record schemas define the minimum expected shape of lifecycle and sharing records.

Current record schemas include:

- `raw_evidence.schema.json`
- `normalized_observation.schema.json`
- `finding.schema.json`
- `alert.schema.json`
- `evidence_package.schema.json`
- `rollup_summary.schema.json`
- `federation_message.schema.json`

These schemas are deliberately minimal. They define required identity and linkage fields without trying to model every deployment-specific detail.

## Rule

Schemas define shape. Validators define cross-record truth.

Examples:

- schema validation can say a finding has `source_observation_ids`
- lineage validation can say those observation ids actually exist
- rollup validation can say a rollup points back to known lifecycle records
- policy validation can say a sharing scope is known
