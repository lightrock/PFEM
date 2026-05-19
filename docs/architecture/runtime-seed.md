# Runtime Seed

PFEM starts with a dependency-free Python runtime seed.

The runtime seed is intentionally small:

- domain dataclasses
- adapter manifest loader
- node profile loader
- smoke check tool
- unit tests

This is not the full application. It exists to keep the architecture executable and testable before heavy infrastructure appears.

## Rule

Do not add databases, queues, web servers, identity systems, or persistent daemons until the architecture docs justify them.
