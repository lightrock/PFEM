# Outbox Items

Outbox items are staged payloads waiting for transport pickup.

A delivery job says movement work exists.
A dispatch decision says PFEM allowed or blocked that job.
An outbox item says the payload/artifact has been staged for movement.
A transport receipt later says what happened during transport.
