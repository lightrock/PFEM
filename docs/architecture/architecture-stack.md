# PFEM Architecture Stack

PFEM uses several models together. No single model owns the whole project.

## Domain model

The domain model names the real things the system handles: evidence, observation, source, adapter, capability, node profile, finding, alert, evidence package, dashboard action, federation message, rollup summary, trust, and policy.

## Polycentric mesh model

PFEM assumes many valid centers of control. A deployment may be local, mesh-like, dashboard-only, field-oriented, site-oriented, research-oriented, or rollup-oriented.

## Node anatomy model

A node is described by functional parts: boundary, input transducer, decoder, associator, memory, decider, encoder, output transducer, timer, and channel/net.

## Recursive coordination model

Nodes can participate in larger systems. The architecture distinguishes local operation, coordination, control, adaptation, and policy.

## Evidence lineage model

Raw evidence, normalized observations, findings, alerts, packages, reports, and rollups are separate objects. Derived objects should preserve links to what produced them.

## AI collaboration model

AI assistants may help write, review, summarize, and test. They must follow the architecture rules and must not collapse domain boundaries for convenience.
