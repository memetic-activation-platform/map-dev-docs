# Agent Spaces Architecture

This page explains how the Agent Spaces concepts fit into MAP's shared runtime. The [Agent Spaces design specification](agent-spaces-design-spec.md) owns ontology, invariants, sovereignty and authorization semantics. The [implementation plan](agent-spaces-impl-plan.md) owns delivery sequence, repository integration, validation evidence and remaining work.

An architecture description is not a claim that every capability below is implemented. In particular, independent-space infrastructure, collective governance and inter-space protocols have explicit design and delivery gates in those documents.

## 1. Shared runtime, distinct identities

MAP's AgentSpace architecture uses a shared hApp/DNA implementation rather than requiring a new hApp or DHT for each Dancer. The coordinator/integrity boundary and generic HolonNode/SmartLink storage substrate support descriptor-defined holons, relationships and behavior.

This shared implementation does not collapse the identities it supports:

| Concept | Architectural role |
| --- | --- |
| HolochainAgent | Cryptographic author of Holochain actions; technical authorship does not itself establish sovereign MAP authority. |
| HolonSpace | Bounded authoritative home for holons and environment for interaction; it is not an Agent. |
| BioSocialAgent | Agent with a sovereign interior, exercising agency and participating in other contexts. |
| PersonAgent | A human being's digital extension in MAP; a BioSocialAgent, distinct from an informational Person holon. |
| AgentSpace / I-Space | Relational designation of a HolonSpace as a BioSocialAgent's sovereign interior. |
| We-Space | A HolonSpace's shared interaction-context aspect; potentially simultaneous with its I-Space aspect. |
| Dancer | Software Agent whose operational execution depends on sovereign/delegated authority and runtime readiness. |

### Holochain naming and provisioned spaces

Core ontology names and Holochain implementation names serve different purposes:

| Context | Settled name | Meaning |
| --- | --- | --- |
| Core ontology | `HolonSpace` | The space holon type, including before sovereign acquisition. |
| MAP relational designation | AgentSpace / I-Space | A HolonSpace as a BioSocialAgent's sovereign interior. |
| Holochain hApp | `AgentSpace` | The shared hApp implementation and its packaged artifacts. |
| Holochain coordinator zome | `holon_space` | The coordinator implementing HolonSpace operations. |

Holochain's use of hApp and DNA can refer either to executable artifacts or to a running network and its participants. Here, **AgentSpace hApp** names the shared implementation; **a provisioned AgentSpace** refers to a particular space with its own DHT context and MAP sub-agents. Those MAP Agents are distinct from the Holochain AgentPubKey identities participating in that DHT. Loading another Dancer does not create another DHT. A hApp, DNA, space, sovereign Agent, conductor and device must not be used as interchangeable identities.

> **Current implementation state (2026-11-11):** The settled names above describe the intended naming. The [hApp manifest](https://github.com/evomimic/map-holons/blob/main/happ/workdir/happ.yaml) still names the hApp `map-holons`; the [DNA manifest](https://github.com/evomimic/map-holons/blob/main/happ/workdir/dna.yaml) names the DNA `map_holons` and registers coordinator zome `holons` and integrity zome `holons_integrity`. Renaming the hApp to `AgentSpace` and coordinator to `holon_space` is deferred implementation work; this documentation update does not rename code or manifests. No new DNA or integrity-zome name is prescribed here. Independent multi-space provisioning remains future delivery work.

## 2. From unclaimed HolonSpace to sovereign interior

A HolonSpace can be provisioned and operational before a sovereign BioSocialAgent exists. Its foundational query, transaction, validation, reference and navigation capabilities do not depend on completed sovereign acquisition.

In the initial deployment, the first HolonSpace also serves as MAP.CoreSchemaSpace. Welcome is foundational onboarding capability available under constrained bootstrap authority, rather than an operational Dancer that would depend circularly on sovereignty.

Onboarding prepares identity and authorization evidence. The existing transaction and validation architecture then establishes BioSocialAgent creation, Home Space, the sovereign interior association and corresponding authorization state together. Acquisition preserves the HolonSpace's identity, type and preexisting holons.

The [design's sovereign-interior contract](agent-spaces-design-spec.md#23-agentspace-and-the-sovereign-interior) governs committed Agent validity and the space's optional sovereign association. Core OwnedBy/Owns continues to express Home Space stewardship; it is not replaced by the sovereign relationship.

Acquisition is the constitutive transition. Runtime opening/readiness is separate: closing a runtime does not remove sovereignty, and reopening an acquired space does not require reacquisition. Exact atomic persistence, conflict and recovery mechanisms belong to the [transaction architecture](../transactions/transactions-design-spec.md), [relationship persistence specification](../transactions/relationship-persistence-design-spec.md), and Agent Spaces implementation plan.

## 3. Complementary I-Space and We-Space aspects

**Agents are wholes that act and parts that participate. I-Spaces provide their sovereign interiors; We-Spaces provide environments for their participation.**

A HolonSpace can provide a shared interaction context before acquisition. After acquisition, that same space can serve both as a BioSocialAgent's sovereign I-Space and as a We-Space for participating Agents.

Participation belongs to the Agent, conceptually through HasRoleIn, not to its I-Space. Participating in another context does not move the Agent's interior, merge spaces, or transfer authoritative Home Space ownership. The exact qualified participation/Role representation remains a design gate.

A collective may emerge through interaction in an existing We-Space. Legitimate constitution and authorized acquisition can establish its collective BioSocialAgent within that same HolonSpace, preserving the continuing We-Space aspect. Participation, constituent membership, emergence, constitution and sovereignty remain distinct; interaction alone does not create a collective Agent.

See the [space aspects and collective-emergence design](agent-spaces-design-spec.md#24-i-space-we-space-and-holonic-participation).

## 4. Descriptor-defined behavior and operational Dancers

Schemas, Dance definitions, Visualizers and implementation artifacts provide affordances through the shared runtime. They do not independently establish a sovereign principal or bypass authorization.

Dancer-related descriptors, definitions and packages may exist or be imported before acquisition. Operational Dancers require an acquired AgentSpace, valid principal/delegation, an initialized runtime and applicable operation-specific authority. Software execution does not make the Dancer an accountable Agreement party.

The [Dances design specification](../dances/dances-design-spec.md) owns invocation and execution contracts. The [DAHN design specification](../hx/dahn-design-spec.md) owns composition and selection. This overview does not prescribe a second dispatch model or imply that all dynamic-loading capabilities are delivered.

For personal configuration, the PersonAgent is the semantic owner of personal VisualizerUsages. Their authoritative Home Space and applicability scope are independent facts. Public Visualizer references do not authorize access to private Agent state.

## 5. Authority, governance and boundary exchange

Runtime execution distinguishes the sovereign principal, delegated executor and Holochain author. Bootstrap authority is restricted to its provisioning/onboarding purpose; ordinary operations after acquisition require sovereign or delegated authority at trusted boundaries.

LifeCodes, Agreements and Roles provide intended governance and participation structures as their owning designs mature. They are not mandatory placeholders for foundational HolonSpace operation, and technical possession of a signing key does not establish Agreement-party eligibility.

TrustChannels are the intended Agreement-governed boundary for inter-space exchange. Permission to invoke a Dance does not automatically authorize disclosure of its returned data. The [Agent Spaces disclosure design](agent-spaces-design-spec.md#73-disclosure-and-trustchannels) and [Trust Channel design specification](trust-channel-design-spec.md) own those requirements.

Envelope composition, protocol policy and transport details belong to the Trust Channel design, not an independently maintained stack on this page. The [Trust Channel entry-point architecture](trust-channel-entry-points.md) addresses host/guest entry-point constraints; it does not replace the sovereign authorization contract.

The former RoutingHolon API sketch and transport/retry algorithms are not established here as accepted interfaces. Routing, endpoint, transport and cross-space coordination details must be reconciled in their owning specifications before implementation. Schema-driven extensibility does not by itself prove that arbitrary protocols or executable implementations can be introduced without runtime work.

## 6. Deployment boundary and further reading

The first personal deployment keeps CoreSchema stewardship, the acquired interior and personal configuration in one authoritative HolonSpace. Multi-AgentSpace provisioning, remote CoreSchema access, inter-space discovery and shared production admission remain separate infrastructure work.

That initial arrangement must preserve unique Home Space identity, immutable reference/cache semantics and explicit execution context so later spaces can reference authoritative schema content without becoming competing authoritative copies. A shared-context aspect inside one HolonSpace is not evidence that independent-space communication is implemented.

For authoritative details:

- [Agent Spaces design specification](agent-spaces-design-spec.md): domain model, sovereignty, acquisition, complementary aspects and open design gates.
- [Agent Spaces implementation plan](agent-spaces-impl-plan.md): milestones, integration points, tests and delivery status.
- [Core Schema bootstrap design](../core-schema-bootstrap/core-schema-bootstrap-design-spec.md): first-space provisioning and readiness.
- [Core runtime overview](../core-runtime/index.md): reference, transaction and execution boundaries.
- [Trust Channel design](trust-channel-design-spec.md): capsules, Agreement-governed exchange and protocol responsibilities.

When this overview and an owning specification differ, reconcile the overview to the governing design rather than treating it as an alternative source of semantics.
