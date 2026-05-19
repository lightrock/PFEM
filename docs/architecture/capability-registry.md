# Capability Registry

PFEM profiles are composed from named capabilities.

The registry gives AI assistants and humans a concrete list of reusable
behaviors. This prevents profiles from becoming vague wish lists.

## Rules

- A profile should reference capabilities that exist in `capabilities/`.
- A capability should describe one reusable behavior.
- A capability should not name a private deployment.
- A capability should not redefine a domain object.
- A capability may require or produce contract objects.

The PFEM doctor checks capability manifests and warns when profiles reference
unknown capabilities.
