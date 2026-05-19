# Node Profile Model

A node profile describes a deployment shape.

Profiles configure the same core architecture instead of creating separate products.

A profile may define:

- profile id
- profile kind
- enabled capabilities
- disabled capabilities
- default adapters
- required schemas
- sharing behavior
- dashboard mode
- review gates
- storage assumptions
- disconnected operation behavior

## Neutral profile names

Use deployment-shape terms:

- field-radio-node
- community-mesh-node
- infrastructure-site-node
- civil-dashboard-node
- research-testbed-node
- formal-authority-rollup-node
- disconnected-edge-node

Avoid naming specific customers, sponsors, agencies, or programs in public profile names.

## Rule

A profile may configure behavior. It must not redefine core domain objects.
