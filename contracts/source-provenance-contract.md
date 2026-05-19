# Source Provenance Contract

A PFEM source registry entry should identify:

- `source_id`
- `display_name`
- `source_kind`
- `adapter_id`
- `node_id`
- `status`

A raw evidence record should identify:

- `evidence_id`
- `evidence_kind`
- `source_id`
- `provenance.adapter_id`

Source validation checks that raw evidence came from known source and adapter names.
