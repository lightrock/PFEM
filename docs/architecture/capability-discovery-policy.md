# PFEM Capability Discovery Policy

PFEM instances may support a voluntary capability discovery / offers channel.

This is not consumer advertising and not automatic trust.

It is a policy-controlled metadata exchange where a PFEM node can disclose selected information about what it is, what it can consume, what it can expose, what it needs, and what terms or approvals are required for deeper integration.

## Rule

A PFEM capability advertisement is not evidence, not a finding, not a rollup, not an approval, and not a trust relationship.

It is metadata that may begin a review/onboarding workflow.

## Possible PFEM discovery records

- Capability Advertisement;
- Need Advertisement;
- Integration Offer;
- Partner Inquiry;
- Trust Requirement;
- Disclosure Level;
- Research Invitation;
- Connector Match;
- Onboarding Request;
- Revocation Notice;
- Expiration Notice;
- Abuse Report.

## PFEM responsibilities

PFEM should preserve provenance and boundaries for:

- who published an advertisement;
- when it was published;
- what capability or need was described;
- what schemas/contracts were referenced;
- what MCP tools/resources were advertised;
- what disclosure level was selected;
- what trust or regulatory gates are required;
- what offer was accepted, rejected, expired, or revoked;
- what abuse was detected or reported.

## Safety rules

- No sensitive operational data by default.
- No automatic trust from advertisements.
- No automatic sharing of raw evidence.
- No automatic MCP tool exposure.
- No bypass of inter-node authentication policy.
- No bypass of regulatory readiness gates.
- Offers expire and can be revoked.
- Discovery traffic should be rate-limited, abuse-gated, and auditable.

## MCP candidates

Possible future read/draft tools:

- `pfem.discovery.profile.read`;
- `pfem.discovery.capabilities.list`;
- `pfem.discovery.needs.list`;
- `pfem.discovery.offers.search`;
- `pfem.discovery.offer.draft`;
- `pfem.discovery.offer.submit_for_review`.

Do not expose high-risk integration actions without policy, audit, authority context, and human approval.

## One-sentence version

PFEM capability discovery is voluntary, policy-controlled metadata exchange for finding compatible connectors, partners, rollup paths, research opportunities, and services without treating advertisements as trust, evidence, authority, or approved integration.
