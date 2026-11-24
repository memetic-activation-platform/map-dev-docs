# Ingestor — Concept Design Specification

**Version:** 0.2  
**Date:** 2026-11-14  
**Status:** Working concept specification; implementation not authorized

## 1. Purpose

Ingestor is a MAP Dancer responsible for securely admitting additional technical Holochain agents into an existing sovereign Agent's I-Space.

Its purpose is specifically **technical-agent admission**, not generalized AgentSpace membership management.

The initial motivating use case is a PersonAgent extending its operational capabilities by admitting additional Holochain agents running on laptops, phones, or headless computing appliances.

Ingestor must reuse MAP's existing Agent Spaces ontology, shared security architecture, and Holochain infrastructure.

## 2. Architectural foundations

### 2.1 Holarchy of agency

MAP distinguishes sovereign BioSocialAgents from technical agents.

A PersonAgent is a BioSocialAgent representing a person's digital extension in MAP. It is distinct from an ordinary Person domain holon.

A PersonAgent has exactly one HolonSpace as its interior, established through `HasInterior`.

The PersonAgent is not itself a member of that interior.

The same HolonSpace is simultaneously:

- The PersonAgent's I-Space, from the perspective of the sovereign whole.
- The shared We-Space of the Holochain subagents participating in its DHT.

These are relational perspectives on the same HolonSpace, not separate DHTs.

A HolochainAgent is a technical agent identified by its Holochain `AgentPubKey`. It is distinct from the sovereign PersonAgent and from the physical device or installation hosting it.

### 2.2 Technical authorship versus sovereign authority

Holochain provides cryptographic authorship and DHT participation.

MAP introduces a holarchy of agency in which technical subagents operate within the interior of higher-level sovereign Agents.

Admitting a HolochainAgent into an AgentSpace:

- Establishes its authorized technical participation.
- Does not create another PersonAgent.
- Does not transfer sovereignty.
- Does not inherently authorize every operation within the space.
- Does not grant authority to enter Agreements on behalf of the sovereign Agent.

Technical authorship, semantic participation, operational authorization, and sovereignty remain distinct.

### 2.3 AgentSpace ontology

The Agent Spaces AS1 work establishes the foundational Agent and AgentSpace ontology.

Our architectural understanding is that Agent participation in spaces is mediated through roles, conceptually expressed through relationships such as `HasRoleIn`.

The exact concrete descriptors, relationship names, inheritance hierarchy, and HolochainAgent representation must be verified against AS1.

**Design constraint:** Ingestor must reuse the existing Agent Spaces ontology. It must not introduce a parallel Membership holon, membership relationship, or role framework unless verification identifies a concrete deficiency.

Do not treat conceptual relationship names as confirmed schema identifiers.

## 3. Scope

### 3.1 Ingestor responsibilities

Ingestor orchestrates the admission of a new technical Holochain agent into an existing AgentSpace.

Its responsibilities are:

1. Initiate a technical-agent enrollment session.
2. Establish the prospective agent's cryptographic identity.
3. Coordinate secure pairing with an authorized existing participant.
4. Support human verification of the pairing.
5. Obtain and verify admission authorization for the specific agent and AgentSpace.
6. Coordinate the Holochain operations required for participation in the existing DHT.
7. Establish the appropriate MAP semantic participation representation using the existing Agent Spaces ontology.
8. Confirm successful admission or report incomplete and failed outcomes.

Ingestor invokes shared security, persistence, and Holochain capabilities rather than independently implementing competing mechanisms.

### 3.2 Explicit exclusions

Ingestor does not own:

- General AgentSpace membership inspection.
- Ongoing role management.
- General membership suspension or removal.
- Revocation or recovery administration.
- BioSocialAgent admission through Promise Weaves and Agreements.
- General AgentSpace governance.
- Persona management.
- Cross-space identity elevation.
- Sovereign constitution of new AgentSpaces.

General participation inspection and management belong to Space Manager or the corresponding shared AgentSpace management capabilities.

Ingestor may display admission results and provide navigation to Space Manager without assuming ownership of ongoing membership management.

## 4. Specialized admission mechanisms

MAP supports different participation-establishment mechanisms for different kinds of agents.

### Technical agents

Ingestor establishes technical Holochain-agent participation through secure pairing, admission authorization, and DHT provisioning.

### BioSocialAgents

BioSocialAgent participation is established through Promise Weaves, Agreements, and applicable governance processes.

These mechanisms are distinct and must not be conflated.

Once participation is established, however, the resulting relationships should be discoverable through the shared AgentSpace ontology.

**Architectural principle: Admission mechanisms may be specialized by agent kind, while ongoing participation management is generalized across agent kinds.**

## 5. Secure pairing model

### 5.1 Candidate identity

The prospective Holochain agent generates or selects its cryptographic keypair.

The identity being admitted is its Holochain `AgentPubKey`, not merely a device name, installation identifier, or network address.

The candidate must demonstrate possession of the corresponding private key.

### 5.2 Pairing protocol

The preferred conceptual approach is interactive, cryptographically key-bound pairing rather than reliance on transferable bearer invitations.

The proposed sequence is:

1. The prospective Holochain agent initiates enrollment.
2. An existing authorized installation establishes a pairing session with the candidate.
3. The endpoints perform a vetted cryptographic key exchange and appropriate key-possession verification.
4. Both independently derive a Short Authentication String (SAS) bound to the pairing transcript.
5. The human operator compares the SAS values through trusted interfaces.
6. Pairing is confirmed only when the values match.
7. Admission authorization is evaluated for the specific candidate public key and target AgentSpace.
8. Authorized DHT provisioning and semantic participation establishment proceed.

The SAS mechanism is a proposed design direction, not a finalized cryptographic protocol.

The eventual protocol must address mutual authentication, transcript binding, freshness, replay resistance, verification strength, and attempt limiting.

Successful pairing establishes confidence in the intended cryptographic endpoint. It does not independently grant admission authority.

### 5.3 Admission authorization

Before admission is committed, the trusted authorization mechanism must verify:

- Candidate Holochain identity.
- Target AgentSpace.
- Authority of the approving participant.
- Scope of the requested admission.
- Freshness and validity of the pairing session.

A supplied `AgentPubKey`, Space identifier, or approval flag is not sufficient authorization evidence.

Authorization must be enforced at the appropriate trusted backend boundaries, including relevant conductor and coordinator entrypoints.

## 6. Graphical and headless interfaces

The pairing protocol must be independent of its user interface.

### Graphical experience

An authorized MAP installation presents the candidate identity, pairing verification information, admission approval, and completion outcome.

### Headless experience

A headless appliance must support admission through a command-line interface, including operation over SSH.

The interface can display the same SAS as the graphical client.

Illustrative output:

    Verification code: 482 917

    Compare this code with Ingestor
    on your authorized MAP installation.

SSH authentication protects access to the appliance but does not substitute for the pairing protocol.

No camera, QR code, browser, or graphical desktop is required.

QR codes may be offered as an optional discovery or information-transfer mechanism, not as independent admission authority.

## 7. Admission completion

Admission involves distinct but related outcomes.

### 7.1 Holochain participation

The candidate becomes a participating Holochain agent in the intended existing DHT.

The precise provisioning operations must be verified against the deployed Holochain version.

### 7.2 MAP semantic participation

The candidate's participation is represented through the established Agent Spaces ontology.

The representation must preserve the distinction between:

- Cryptographic Holochain identity.
- Technical-agent identity, where modeled.
- Hosting device or installation.
- Role-mediated participation in the AgentSpace.
- Operation-specific authorization.

### 7.3 Completion and failure

The design must define when admission is complete and how to handle:

- Interrupted pairing.
- Failed authorization.
- Partial DHT provisioning.
- Failed semantic participation persistence.
- Duplicate or replayed admission requests.
- Divergence between technical DHT participation and MAP semantic participation.

The system must not report successful authorized admission when required completion conditions have not been satisfied.

Recovery and consistency mechanisms should reuse shared infrastructure.

## 8. Ownership boundaries

| Concern | Owning capability |
|---|---|
| Technical-agent admission orchestration | Ingestor |
| Agent hierarchy and participation ontology | Agent Spaces |
| Authentication, authorization, credentials | Client Security |
| Cryptographic authorship and DHT participation | Holochain infrastructure |
| General membership inspection and management | Space Manager |
| BioSocialAgent participation and commitments | Promise Weaves / Agreements |
| Durable state changes and recovery | Shared Transactions / Persistence |
| Cross-space sovereign identity transitions | TrustChannel and Persona architecture |

Ingestor must not create competing implementations of these responsibilities.

## 9. Relationship to Client Security

Client Security owns the shared security mechanisms that Ingestor consumes.

Ingestor requires secure admission authorization but does not define an independent authentication framework or general policy engine.

The existing CS-L1 delivery is narrowly scoped to initial local constitution and the bounded AS2 lifecycle.

General Dancer authorization, multi-device continuity, and broader delegation capabilities remain separately scoped.

**Ingestor must not silently expand CS-L1 or AS2.**

Its eventual implementation requires an explicitly defined security capability sufficient to authorize and enforce technical-agent admission.

Holochain technical invocation rights must not be confused with MAP semantic authority.

## 10. Open design decisions

### D1 — AS1 ontology reconciliation

Inspect the actual AS1 schema and descriptors.

Determine:

- The concrete Agent hierarchy.
- Whether TechnicalAgent is an existing subtype of Agent.
- Whether HolochainAgent is represented as a first-class holon.
- The actual role and participation relationship descriptors.
- The relationship between role assignment and recognized participation.
- The required semantic records produced by successful admission.

Do not invent missing descriptors or relationships without identifying and documenting an actual gap.

### D2 — Holochain identity binding

Determine how the candidate `AgentPubKey` is associated with its MAP representation.

Preserve the distinction between technical identity, device or installation, and sovereign Agent.

### D3 — Admission authority

Determine which existing participants may authorize admission and how their authority is established and verified.

### D4 — Cryptographic pairing

Select a vetted pairing protocol with appropriate mutual authentication, SAS verification, key binding, replay protection, and freshness guarantees.

### D5 — Discovery

Determine how a prospective agent locates an authorized enrollment endpoint, including local-network and remote scenarios.

### D6 — Holochain provisioning

Verify the precise Holochain operations required to add a new agent to the existing DHT.

Identify version-specific constraints and security implications.

### D7 — Durable completion and recovery

Define admission completion predicates, persistence sequencing, idempotency, and recovery from partial outcomes.

### D8 — Initial implementation increment

Define the smallest useful implementation that demonstrates secure technical-agent admission without introducing generalized membership management or expanding existing milestone scopes.

## 11. Target acceptance outcomes

A future implementation should demonstrate that:

1. An authorized participant can initiate technical-agent admission into an existing acquired AgentSpace.
2. A prospective Holochain agent can complete cryptographically authenticated pairing.
3. Both graphical and headless interfaces use the same admission protocol.
4. Unauthorized candidates cannot obtain valid admission.
5. Admission authorization is bound to the candidate's public key and the target AgentSpace.
6. The candidate participates in the intended existing Holochain DHT.
7. Semantic participation is established using the existing Agent Spaces ontology.
8. Admission does not confer sovereignty or unrestricted operational authority.
9. Interrupted or failed admission does not silently produce an unauthorized successful participant.
10. The admitted agent is subsequently discoverable through general AgentSpace management capabilities.

These are conceptual acceptance outcomes, not claims of implemented functionality.

## 12. Governing principle

**Ingestor is the specialized technical-agent admission Dancer for MAP AgentSpaces.**

It securely establishes the participation of additional Holochain agents within an existing sovereign Agent's interior.

It reuses the Agent Spaces ontology, MAP Client Security, Holochain infrastructure, and shared persistence capabilities.

It does not own generalized membership management.

## 13. Next design activity

Before implementation planning:

1. Reconcile the exact AS1 Agent hierarchy and role descriptors.
2. Verify Holochain multi-agent DHT provisioning mechanisms.
3. Identify the security capabilities required beyond CS-L1.
4. Select the cryptographic pairing protocol.
5. Define the minimum admission completion and recovery contract.

Do not begin implementation or introduce new ontology solely on the basis of this concept specification.