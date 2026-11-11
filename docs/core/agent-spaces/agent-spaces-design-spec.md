# MAP Agent Spaces — Reconciled Design Specification

**Version:** 0.4 (sovereign acquisition and complementary space aspects)  
**Date:** 2026-11-11  
**Project:** MAP / Agent Spaces  
**Status:** Design direction with explicit implementation gates; not a claim of implemented behavior

## 1. Purpose, scope, and architectural narrative

MAP is **Person-Centric rather than App-Centric**. Instead of people occupying application-owned environments, BioSocialAgents acquire sovereign digital interiors, within which application-like software Agents—**Dancers**—operate under delegated authority. This arrangement is grounded in Holochain: HolochainAgents provide cryptographic authorship and the computational means to provision and operate MAP HolonSpaces. A HolochainAgent exists before any MAP PersonAgent identity or sovereign AgentSpace has been established.

A **HolonSpace** is a bounded home for holons and an environment for interaction, not an Agent. Agents exercise agency and participate in We-Spaces; spaces provide environments rather than acting as Agents. An initially unclaimed HolonSpace can be provisioned and made operational under constrained bootstrap authority. Identity and authorization evidence for an existing human being is prepared before the PersonAgent is created and acquires that HolonSpace in one atomic MAP transaction. **AgentSpace is the relational role of that HolonSpace after acquisition, not a separate HolonType or a wrapper.** The HolonSpace retains its identity and home-space semantics. After acquisition, the PersonAgent can authorize Dancers within the AgentSpace. Dancers neither create sovereignty nor become independent Agreement parties.

The conceptual progression is:

**HolochainAgent → operational unclaimed HolonSpace → prepared identity and authorization evidence → atomic BioSocialAgent creation and acquisition → sovereign AgentSpace → delegated operational Dancers.**

**Agents are wholes that act and parts that participate. I-Spaces provide their sovereign interiors; We-Spaces provide environments for their participation.** A HolonSpace may support interaction and collective emergence as a We-Space; when a legitimately constituted collective BioSocialAgent acquires it, it becomes that Agent's I-Space without ceasing to function as a We-Space.

This specification reconciles the earlier Agent Spaces design draft (2026-11-04), the Agent Spaces implementation plan (2026-11-09), and the bootstrap/acquisition design (2026-11-10). It supersedes the earlier proposed `AgentSpace extends HolonSpace; ISpace extends AgentSpace; WeSpace extends AgentSpace` inheritance hierarchy. It retains the earlier specifications' Persona, participation, privacy, collective agency, and DAHN ownership requirements.

**Scope:** Agent/space ontology, I-Space and We-Space roles, Holochain grounding, CoreSchema access, onboarding and acquisition, authorization, ownership, contextual identity, Agreement eligibility, Dancers, persistence, and staged delivery boundaries. Detailed authentication protocols, TrustChannel transport, full Promise Weave, collective governance, and multi-AgentSpace runtime infrastructure remain separate design work.

**Normative language:** MUST and MUST NOT state target design invariants. Proposed names and deferred capabilities are not implemented contracts until their owning schema/design decisions are approved. An unclaimed HolonSpace may be provisioned before its sovereign association exists. This does not relax the complete-interior requirement for any BioSocialAgent admitted as committed state.

## 2. Foundational ontology

### 2.1 Holon and HolonSpace

A Holon is MAP's general representational unit at any scale. A Holon does not imply an Agent or AgentSpace. A **HolonSpace** is the foundational bounded container for holons and relationships, and the authoritative home of its locally stewarded holons. Each holon has **exactly one Home Space**. References, remote representations, and permissible immutable runtime caches do not transfer authoritative ownership.

Core HolonSpace capabilities—query, validation, transactions, recognition, navigation, and references—MUST remain usable without an associated BioSocialAgent. A HolonSpace may be provisioned before sovereign acquisition; its identity MUST persist through acquisition and restart.

### 2.2 Agent and kinds of agency

**An Agent is anything capable of sensing and responding to its environment.** Agency alone does not establish sovereignty, moral responsibility, or authority to undertake commitments. Agent is a first-class MAP semantic concept, but the complete taxonomy is not a prerequisite for initial delivery.

**HolochainAgent.** A cryptographically identified Holochain participant, signified by an `AgentPubKey`, with access to computational, storage, and communication resources. HolochainAgents author source-chain actions and provide the technical substrate for MAP operations. They do not thereby become sovereign BioSocialAgents or eligible Agreement parties. Whether HolochainAgents require first-class MAP holon representations is deferred; the runtime concept must not be mistaken for an already-declared MAP HolonType.

A HolochainAgent is identified by its AgentPubKey, not by a physical computing device. Its cryptographic identity is not inherently hardware-bound, although key generation and custody may depend on device-associated cryptographic material. Continuity of identity across execution environments requires preservation or recovery of the relevant key material and compatible Holochain source-chain state. MAP MUST NOT presume that such migration is automatically supported.

**BioSocialAgent.** An Agent whose agency is grounded in biological and social life, including PersonAgents and appropriately constituted collective Agents (such as communities, organizations, commons, and bioregions). Every committed BioSocialAgent MUST have exactly one sovereign interior through the constitutive relationship; incomplete construction is permitted only in uncommitted state. Positive Agreement-party eligibility, especially for collective representation, requires explicit rules; classification alone does not authorize any particular commitment.

**PersonAgent.** A BioSocialAgent constituting a human being's digital extension in MAP. A PersonAgent is a durable MAP Agent that inherits BioSocialAgent's mandatory sovereign interior; it may participate in We-Spaces and undertake authorized commitments. It is neither the human being nor a digital twin or descriptive profile.

**Person.** An ordinary domain holon containing information about a person. Person is **not** an Agent subtype, sovereign principal, or Agreement party by virtue of that informational role. A Person holon may be associated with a PersonAgent, but no mandatory Person–PersonAgent association is established here. The human being exists independently of MAP; onboarding establishes the PersonAgent's digital presence, not a second human being.

**Dancer.** An application-like software Agent whose operational execution requires an acquired AgentSpace, a valid sovereign principal, appropriate delegated authority, and a ready authorized runtime context. Dancer definitions, descriptors, implementation artifacts, and deployable packages MAY exist before sovereign acquisition and may be loaded into an unclaimed HolonSpace. Their availability confers no operational authority. Operational Dancers cannot acquire AgentSpaces or sign MAP Agreements as accountable parties. They execute within an AgentSpace without another hApp or DHT. The retired term *Organ* is not used.

Other technical agents or computing-node representations may be modeled as needed, without creating a sovereign I-Space for each. No `proto-Agent`, universal `MoralAgent` subtype, or complete Agent inheritance tree is required for the first milestone.

### 2.3 AgentSpace and the sovereign interior

**AgentSpace is the relational role of a HolonSpace serving as the sovereign interior of a BioSocialAgent.** It is not the Agent, does not independently exercise agency, and is neither a new HolonType nor a wrapper. Acquisition preserves the existing HolonSpace's identity, type, and preexisting holons.

The constitutive association is conceptually:

**BioSocialAgent — HasInterior → HolonSpace** (inverse: **IsInteriorOf**).

**Approved relationship direction and definitional status:** `HasInterior` is the declared, definitional relationship from BioSocialAgent to HolonSpace. `IsInteriorOf` is its derived, non-definitional inverse from HolonSpace to BioSocialAgent. The constitutive definition belongs to the BioSocialAgent; a HolonSpace exists independently before acquisition. **Approved target bindings:** `HasInterior` uses `TargetBinding Version`; `IsInteriorOf` uses `TargetBinding Lineage`, matching the existing Core `OwnedBy`/`Owns` binding pattern. The forward definitional relationship identifies an exact HolonSpace version; the inverse identifies the BioSocialAgent lineage. Home Space correspondence requires the same authoritative HolonSpace identity. **Approved collection policy:** both `HasInterior` and `IsInteriorOf` use `IsOrdered false` and `AllowsDuplicates false`. Neither singleton association has meaningful ordering, and duplicate occurrences are disallowed. **Approved deletion policy:** `HasInterior` uses `DeletionSemantic Block`; `IsInteriorOf` uses `DeletionSemantic Allow`. These relationship policies do not replace other applicable deletion constraints or decide explicit association removal, transfer, or decommissioning. The remaining descriptor/enforcement contract is still subject to D1.

Their meaning and validity requirements are settled:

- Every committed BioSocialAgent MUST have exactly one sovereign HolonSpace.
- A HolonSpace MAY have zero or one sovereign BioSocialAgent, never multiple simultaneous sovereign Agents.
- Every BioSocialAgent MUST be homed in the HolonSpace that is its sovereign interior: its Home Space and HasInterior target identify the same HolonSpace.
- These requirements are inherited by PersonAgent and all legitimately constituted collective BioSocialAgent subtypes.
- A BioSocialAgent may be incomplete during uncommitted construction but MUST NOT become valid committed state without its interior association.
- A plain unclaimed HolonSpace is independently valid before any BioSocialAgent exists.
- Technical Agents, HolochainAgents, and Dancers do not inherit this requirement.

Home Space correspondence is a semantic identity invariant, not permission to change Core OwnedBy/Owns binding or to equate sovereignty with home-space stewardship. Exact descriptor bindings, inverse naming, and removal/transfer enforcement remain design gates.

### 2.4 I-Space, We-Space, and holonic participation

**I-Space** denotes a HolonSpace as the sovereign interior of exactly one BioSocialAgent. It supports the Agent's internal organization, information, resources, and operational Dancers; it does not exercise the Agent's agency.

**We-Space** denotes a HolonSpace as a shared environment for interaction and coordination among participating Agents. A HolonSpace can provide this context without a sovereign BioSocialAgent. An unclaimed HolonSpace may therefore function as a We-Space, subject to its applicable bootstrap/admission authority.

**I-Space and We-Space are complementary, potentially simultaneous aspects of the same HolonSpace.** Acquisition adds the I-Space aspect without removing the shared-context capacity. Neither aspect requires a separate HolonType, aspect holon, wrapper, or replacement space merely to distinguish its meaning.

The conceptual participation contract is **Agent — HasRoleIn → We-Space**. An Agent may participate in zero or more We-Spaces. The participating entity is the Agent, not its I-Space. Participation does not move its sovereign interior, merge spaces, or transfer authoritative Home Space ownership.

**Holonic whole/part duality belongs to the Agent:** a BioSocialAgent is a whole with a sovereign interior and may participate as a part in larger holonic structures. Its I-Space provides its interior; We-Spaces provide environments for participation.

A shared We-Space does not automatically constitute a collective Agent. Collective membership, We-Space participation, emergence of organization, legitimate collective constitution, and sovereign acquisition remain distinct. A guest can participate without becoming a constituent member; a collective Agent can itself participate in other We-Spaces.

### 2.5 Collective emergence in an existing We-Space

Agents may interact, coordinate, and self-organize within an unclaimed HolonSpace functioning as a We-Space. If a collective is legitimately constituted as a BioSocialAgent, its creation and authorized acquisition of that same space occur in one atomic MAP transaction. The collective Agent is distinct from the space and is homed in it.

The space becomes the collective's sovereign I-Space **without ceasing to be its participants' We-Space**, preserving its identity and existing holons. Emergence is a developmental process, not a mandatory persistent sovereignty state. No Emergent state is prescribed.

HasRoleIn is a conceptual name, not a finalized simple-edge or Role schema. Qualified participation may be needed for status, roles, Agreements, admission, and authorization. Detailed shared-context representation, collective constitution, and governance remain deferred; the ontology supports this pathway without requiring their implementation for the first personal deployment.

## 3. Identity, Personas, and accountable agency

### 3.1 Distinct identities

| Identity | Meaning | Not equivalent to |
| --- | --- | --- |
| Holochain `AgentPubKey` | Cryptographic Holochain author | PersonAgent, device, sovereign MAP principal |
| MAP Agent identity | Durable semantic identity of a represented Agent | Holochain key or account |
| Persona | Cryptographically backed contextual identity presented by an Agent | Agent, Profile, universally public Agent mapping |
| HolonSpace identity | Persistent identity of a bounded authoritative space | Its sovereign Agent or conductor |
| Installation / conductor / device | Deployment and execution infrastructure | MAP Agent or HolonSpace identity |

The active MAP Agent MUST NOT be inferred solely from a Holochain key, process, host, account, Persona, subject Home Space, or caller-supplied ID. Runtime context must explicitly resolve the authorized principal and applicable space.

### 3.2 Personas and Profiles

A Persona is a cryptographically backed identity through which an Agent presents itself in a participation context; a keypair is the initial working model. An Agent may use multiple Personas, and a Persona may be reused across Agreements and Promise Weaves to expose intended continuity. A new Persona per Agreement is not required. A Profile describes an identity; it is not the Persona or the Agent.

The Agent-to-Persona mapping belongs within its interior context and MUST NOT become universally traversable merely because a Persona is externally visible. Persona reuse makes attribution possible but does not transfer trust or permissions automatically. A durable Persona independent of its current keys, key rotation/revocation, device use, selected proofs, and mapping to Holochain identity remain open design matters. No SSI standard, zero-knowledge system, or credential framework is imposed here.

### 3.3 Operational agency versus moral agency

Software Agents, AI models, and simulation models MUST NOT sign Agreements or be treated as accountable commitment parties. Cryptographic signing capability does not constitute moral authority or assent. Delegated software may execute activities in fulfillment of another Agent's commitments; records must distinguish the accountable principal, its representing Persona, the executing technical/software Agent, and the authority under which execution occurs.

Eligibility for PersonAgents, collective Agents, bioregions, and representatives requires explicit positive rules. Neither a generic Agent type nor possession of an I-Space, Persona, or signing key automatically establishes Agreement-party eligibility.

## 4. Collective identity, Agreements, and participation

A group can have both constituent PersonAgent identities and a distinct collective Agent identity. Recognizing a collective Agent is a constitutive modeling act, not proof that the group already possesses every capacity of a living social organism. A We-Space MUST NOT automatically generate collective identity, collective membership, or a sovereign I-Space.

Agreement participation is contextual. Roles belong to participation within an Agreement, not intrinsically to a Persona. A candidate `AgreementParticipation` holon may associate an Agreement, participating Persona, Roles, commitments, and authorizations; this is **proposed**, not a required type. The accountable Agent remains distinct from the Persona presented to counterparties and from software executing activities.

Promise Weave supports richer Agreement formation but is not a prerequisite for the first persistent AgentSpace. Detailed admission rules, representative authority, governance, and positive Agreement eligibility are later-stage design gates.

## 5. CoreSchema and Holochain foundation

### 5.1 Runtime boundaries

MAP retains its single **AgentSpace hApp architecture**, with the existing MAP DNA, coordinator zome `AgentSpace`, integrity zome `holons_integrity`, Holochain EntryType `HolonNode`, and LinkType `SmartLink`. Semantic HolonTypes are descriptors, not additional Holochain EntryTypes. Independently provisioned spaces will correspond to distinct space/DHT contexts when multi-AgentSpace infrastructure is implemented. Dancers execute inside an AgentSpace without additional hApps/DHTs.

Every operation affecting authoritative distributed MAP state ultimately requires authorized HolochainAgent execution. The implementation MUST distinguish:

- **Principal:** MAP Agent whose authority governs an operation.
- **Executor:** component/Dancer performing the operation.
- **Author:** HolochainAgent whose key authors the Holochain action.

During bootstrap no sovereign BioSocialAgent principal has yet acquired the space; only narrowly scoped bootstrap authority is available. After acquisition, ordinary operations require authority traceable to the sovereign principal or a valid delegation. Holochain cryptographic authorship is not, by itself, MAP sovereign authorization.

### 5.2 CoreSchema availability and ownership

Every operational HolonSpace requires access to a compatible authoritative CoreSchema, but does not necessarily own its descriptors. All CoreSchema holons retain one authoritative Home Space. Locally cached immutable versions and external references do not constitute new authoritative copies.

**Initial single-space deployment:** the first HolonSpace, `MAP.CoreSchemaSpace`, owns the packaged CoreSchema and is subsequently acquired as the first PersonAgent's AgentSpace. This is an intentional bootstrap arrangement, **not** a permanent ownership or deployment rule. No remote CoreSchema access is required for the first personal deployment.

The existing CoreSchema bootstrap and readiness behavior MUST be preserved through the transition to sovereign acquisition. Concrete functions, repository touchpoints, and migration tasks belong in `agent-spaces-impl-plan.md`; this specification does not claim onboarding or acquisition is already implemented.

### 5.3 Future multi-AgentSpace CoreSchema access

Future independently provisioned HolonSpaces should resolve an existing authoritative CoreSchemaSpace instead of creating new authoritative CoreSchema graphs. Future bootstrap must address trusted CoreSchemaSpace identity, network/DNA discovery, schema-root reference, compatibility, authentication/trust anchor, read-only descriptor retrieval, and immutable cache/version policy.

The future initial connection cannot depend circularly on an existing PersonAgent, ordinary Agreement, or TrustChannel. Concrete transport, authorization, and reference-resolution protocols are **deferred and not required for the first personal deployment**.

**Compatibility constraint:** early APIs MUST preserve distinctions between local ownership, authoritative Home Space, references, and cached immutable versions. They MUST NOT assume that all descriptors are necessarily locally homed, but they need not implement remote resolution yet. The first-space bootstrap may be implemented locally without building a speculative multi-space abstraction framework.

## 6. Provisioning, acquisition, and runtime readiness

### 6.1 Independent lifecycle dimensions

The installation lifecycle distinguishes **Provision** (durable installation/space identity, initial content and completion evidence), **Open** (reuse completed state and rebuild runtime/caches without reprovisioning), and **Upgrade** (explicit versioned changes with compatibility and recovery).

The sovereignty lifecycle is:

| State | Meaning |
| --- | --- |
| Provisioning | Foundational HolonSpace identity and infrastructure are being established |
| Unclaimed | An operational HolonSpace exists without a sovereign BioSocialAgent |
| Acquired | A valid BioSocialAgent has acquired the HolonSpace as its sovereign interior |

Acquisition is the constitutive transition establishing AgentSpace. There is no separate persistent Active sovereignty state. Runtime conditions such as **Closed, Opening, Ready, and Closing** are independent: an acquired space remains acquired while closed, and reopening it does not authorize or require reacquisition. These conceptual states do not imply new HolonTypes.

### 6.2 Atomic creation and acquisition

Initial BioSocialAgent creation and sovereign acquisition MUST constitute one atomic MAP transaction establishing the Agent, its authoritative Home Space, its required interior association, and the corresponding sovereign authorization state.

For personal onboarding, identity and acquisition evidence is prepared for the existing human being before persistence. The PersonAgent is staged in the already operational unclaimed HolonSpace it will acquire. No separately committed, interior-less PersonAgent is required or permitted.

Acquisition MUST:

- Establish semantic Agent identity independently of Holochain author identity.
- Confirm that the target HolonSpace is operational, unclaimed, eligible, and legitimately acquirable by this principal.
- Validate the complete prospective Agent, Home Space, interior relationship, inverse uniqueness, and authorization state.
- Prevent conflicting sovereign associations and duplicate successful acquisitions.
- Preserve the existing space's identity, type, and preexisting content.
- Provide durable evidence allowing interrupted or retried acquisition to be resolved deterministically.
- Never expose a partial result as valid completed acquisition or allow ordinary operations to reset sovereignty to Unclaimed.

Atomicity is the required semantic outcome, not an assumption that an arbitrary sequence of Holochain actions or a successful transport response provides database-style all-or-nothing persistence. The owning transaction and relationship-persistence specifications govern physical commitment, write authority, conflicts, and recovery. No competing transaction mechanism is authorized.

Ordinary relationship mutation MUST NOT leave a committed BioSocialAgent without its interior or violate Home Space correspondence. Unrestricted removal or reassignment is not permitted. Transfer, succession, lost-credential recovery, and decommissioning require separately authorized procedures; no normal path may reopen bootstrap authority to perform them.

### 6.3 Bootstrap and Welcome

The first HolonSpace is MAP.CoreSchemaSpace, provisioned before a PersonAgent exists. It remains an ordinary HolonSpace under narrowly scoped bootstrap authority until atomic PersonAgent creation/acquisition establishes its sovereign association.

**Welcome to the MAP is a foundational onboarding capability, not an operational Dancer.** It may prepare identity/authorization evidence and initiate acquisition in an unclaimed space. Operational Dancers cannot supply the sovereignty on which their own authorization depends.

### 6.4 Identity and authorization boundary

Persistent PersonAgent identity, its sovereign association, and enforceable separation between bootstrap and ordinary authority are required. Complete future authentication protocols are not prerequisites for the first personal deployment. A constrained local development acquisition rule may be used if explicitly defined and labeled non-production; a supplied PersonAgent ID or Holochain AgentPubKey alone is insufficient authorization evidence.

After acquisition, ordinary operations require the acquired association, an appropriately initialized runtime context, a valid sovereign principal or authorized delegation, and operation-specific authorization. Acquisition does not grant every operation automatically.

### 6.5 Authorization matrix

| Capability | Provisioning | Unclaimed | Acquired |
| --- | --- | --- | --- |
| Initialize local HolonSpace | Bootstrap only | Denied | Denied |
| Establish/read CoreSchema | Bootstrap only | Scoped reads | Authorized access |
| Welcome/onboarding | Not yet | Scoped | Optional, separately authorized |
| Prepare initial PersonAgent identity evidence | Denied | Scoped, without an interior-less committed Agent | Governed operation; no duplicate initial acquisition |
| Create initial PersonAgent and acquire this space | Denied | Authorized once, atomically | Denied |
| Ordinary holon mutation | Provisioning-only | Onboarding/admitted-context scope only | Sovereign/delegated authority |
| Load Dancer definitions/packages | Bootstrap-content scope | Scoped schema/package imports | Authorized imports |
| Provision or invoke operational Dancers | Denied | Denied | Authorized delegation and runtime readiness |
| Undertake MAP Agreements | Denied | Denied | Eligible accountable Agents under applicable authority |

The acquired column is conditional on runtime readiness and applicable authorization. Loading Dancer content confers no execution authority. An unclaimed We-Space is not an unrestricted mutation environment.

Authorization must be enforced at trusted runtime/zome boundaries, not solely in the UI. Coordinator checks and integrity validation need an explicit division of responsibility. No blanket bootstrap bypass may persist after acquisition.

## 7. Stewardship, semantic ownership, and contextual disclosure

### 7.1 Distinct ownership facts

The implementation MUST preserve three independent facts:

1. **Home Space:** where the holon's authoritative state is stewarded; existing Core `OwnedBy`/`Owns` relationships have HolonSpace semantics.
2. **Semantic Agent owner:** the Agent whose personal configuration or responsibility the holon expresses.
3. **Applicable context/scope:** the circumstances in which that configuration or authority applies.

For example, a VisualizerUsage may be homed in a HolonSpace, owned by a PersonAgent, and scoped to a subject type, Slot, or composition context. Agent ownership MUST NOT retarget or replace Core Home Space ownership.

### 7.2 Agent-owned VisualizerUsages

The first AgentSpace must provide an explicit, authorized path to its sovereign PersonAgent so that DAHN can discover personal VisualizerUsages from that Agent rather than treating public Visualizers or subject ancestry as authoritative personal ownership indexes.

The integration contract must define Agent-to-Usage relationship direction/inverse, multiplicity, context scope, home-space placement, reassignment/deletion, keys, and existing-record migration. Shared Visualizers and subject types MUST NOT cause different Agents' configurations to collide or leak. Default-only rendering MUST NOT create durable personal Usages. Background saves must retain the correct principal/context and must not block foreground usability.

Selection may bulk-acquire authorized personal state and build a reusable Rust-derived index. It must preserve specialization, applicable Visualizers, explicit pins, ValueType preferences, composition-local overrides, Slot contracts, Themes, runtime compatibility, and authorization. Index validity must respond to Agent/context changes, edits, background persistence, schema/policy changes, and Space Session reset. TypeScript consumes Rust-authorized results; no parallel ownership mechanism should be introduced in the host adapter.

### 7.3 Disclosure and TrustChannels

Persona identity does not define a global permission set. Effective disclosure depends on Agreement and participation context. Proposed reusable disclosure selections may group permissions, but editing a reused selection MUST NOT silently enlarge an existing Agreement's grant.

TrustChannels are the intended Agreement-governed boundary for inter-space exchange; Declared External Commitments may govern relevant Exosphere interactions. Their detailed endpoints, routing, and transport are deferred. Permission to invoke a Dance does **not** automatically authorize every returned datum. Type/property/relationship checks are necessary but cannot prove arbitrary values contain no sensitive derivations. These detailed boundary capabilities are deferred beyond the initial local personal-configuration delivery.

## 8. Candidate schema and relationship inventory

This inventory preserves the earlier design's useful associations while reflecting the relational AgentSpace model. **Except for explicitly approved decisions below, names and concrete descriptors remain provisional** until reconciled with canonical TDL, single inheritance, direct dependencies, inverse materialization, and existing contracts.

| Source | Candidate association | Target | Meaning / status |
| --- | --- | --- | --- |
| BioSocialAgent | `HasInterior` | HolonSpace | Approved declared, definitional relationship; exactly one for committed Agents; target equals authoritative Home Space |
| HolonSpace | `IsInteriorOf` | BioSocialAgent | Approved derived, non-definitional inverse; zero or one sovereign Agent |
| Agent | `HasRoleIn` | HolonSpace in We-Space role | Agent participation in a shared context; exact qualified representation deferred |
| Agent | `HasPersona` | Persona | Contextual identities; mapping visibility restricted |
| Persona | `HasProfile` | Profile | Contextual description; proposed |
| Agent | `HasLifeCode` | LifeCode | Optional values/goals/governance |
| We-Space context | `HasLifeCode` | LifeCode | Optional shared contextual commitments |
| CollectiveAgent | `HasMember` | Agent | Constituent membership, not venue participation |
| We-Space context | `HasCollectiveIdentity` | CollectiveAgent | Optional association; semantics (emergence, governance, or venue) deferred |
| AgreementParticipation | `InAgreement` | Agreement | Proposed qualified participation |
| AgreementParticipation | `UsesPersona` | Persona | Proposed participating identity |
| AgreementParticipation | `AssignedRole` | Role | Proposed Agreement-scoped Role |
| HolonSpace in AgentSpace role | `GovernedBy` | Agreement | Candidate governance association, not signing eligibility |
| Sovereign interior | `HasTrustChannel` | TrustChannel | Governed boundary exchange |
| TrustChannel | `GovernedBy` | Agreement | Agreement-governed exchange |
| TrustChannel | `BoundByExternalCommitment` | DeclaredExternalCommitment | Candidate Exosphere boundary |
| HolonSpace in AgentSpace role | `HostsDancer` | Operational Dancer | Hosting under delegated authority; not mere definition/package availability |
| Agent | `DelegatesTo` | Agent | Proposed delegation; scope and authority required |
| Agent | `OwnsPersonalUsage` | VisualizerUsage | Candidate semantic ownership, distinct from Home Space |

The table's role-qualified sources and targets are semantic descriptions, **not proposed new HolonTypes**. Exact descriptor identities, inverse names, bindings, and enforcement placement remain design gates; the mandatory BioSocialAgent interior and zero-or-one space sovereign cardinalities are settled. Additional associations to Enquiries, Offers, Promises, Promise Weaves, Modules, descriptors, and DAHN preferences belong to their respective owning designs. Association does not imply authorization to traverse or disclose private identity mappings.

## 9. Deployment compatibility and deferred multi-AgentSpace infrastructure

The first personal deployment operates one authoritative HolonSpace that also serves as MAP.CoreSchemaSpace. Independent-space provisioning, remote CoreSchema resolution, cross-DHT discovery, inter-space TrustChannels, and cross-space admission are a separately designed infrastructure undertaking, not prerequisites for initial sovereignty or Agent-owned personal configuration.

Early interfaces MUST preserve distinct Agent, HolonSpace, HolochainAgent, Persona, conductor and device identities; one authoritative Home Space; explicit sovereign context; local stewardship versus remote references/caches; and acyclic schema dependencies. They must not assume all future descriptors are locally homed or conflate technical keys with sovereign principals.

Supporting these distinctions does not require speculative transport, remote resolution, full Agreements, or a multi-space framework in the first deployment. Representing several Agents within one space, or recognizing its complementary I-Space/We-Space aspects, does not prove independently operating spaces or production shared admission.

## 10. Persistence and runtime requirements

Provisioning MUST record durable completion independently of incidental schema presence. Opening MUST reconstruct the same installation, HolonSpace, Agent association, and saved holons without reprovisioning. Upgrades MUST be explicit, versioned, and recoverable. Interrupted provisioning/acquisition, duplicate calls, conflicting associations, incompatible versions, and partial durable state require defined detection and recovery; neither an in-memory space ID nor a successful transport response alone proves readiness.

Existing Reference Layer binding, TransactionContext mutation/Commit, and wire projection boundaries must be preserved. No direct-storage shortcut or competing mutation API should be introduced. Descriptor recognition and validation follow their owning specifications; opening is not permission to replay initial content acceptance on every startup.

Schema descriptors should be introduced through non-Core packages and ordinary configured imports, with direct dependencies, single `extends` declarations where applicable, and both relationship directions declared consistently with the TDL/descriptor rules. Generated JSON/manifests are produced by repository tooling, not manually edited. The relational AgentSpace model removes the earlier requirement to create an AgentSpace/ISpace/WeSpace inheritance hierarchy.

## 11. Constraint enforcement responsibilities

The existing descriptor-aware validator and transaction machinery own enforcement; no parallel semantic validation system is introduced.

- Descriptor contracts express actual type lineage, declared/inverse endpoint compatibility, committed BioSocialAgent interior requiredness, and the space-side zero-or-one sovereign constraint.
- Prospective Commit assessment includes affected local declared and derived inverse occurrences, Home Space correspondence, and the effect of removal or replacement. Incomplete staged construction is not admitted as valid committed state.
- Acquisition authorization determines legitimate authority to create the sovereign association; structural validity alone is not authorization.
- Commit orchestration and its owning persistence contracts establish the required all-or-nothing acquisition outcome, conflict handling, completion evidence, and retry/recovery behavior.
- Runtime authorization resolves sovereign principal, Holochain author, executor and delegation; operational readiness does not change persistent sovereignty.
- Holochain integrity validation remains within its owning architectural boundary; descriptor-dependent semantics must not be silently moved into integrity validation.

The exact representation and responsibility split for cross-field consistency, affected saved endpoints, durable acquisition evidence, and concurrent attempts remain explicit design gates. Complete collective, transfer and remote-coordination protocols are deferred, but ordinary local mutation cannot admit an invalid committed BioSocialAgent.

## 12. Architectural invariants

1. **Technical grounding:** authoritative distributed MAP state changes require authorized HolochainAgent execution.
2. **Single Home Space:** each holon has one authoritative Home Space; references/caches do not transfer ownership.
3. **Space/Agent separation:** a HolonSpace is not an Agent.
4. **Relational AgentSpace:** AgentSpace is a HolonSpace role established through legitimate sovereign association, not a HolonType.
5. **BioSocial sovereignty:** every committed BioSocialAgent has exactly one interior and is homed there; each HolonSpace has at most one sovereign Agent. Technical Agents and Dancers do not inherit the requirement.
6. **Unclaimed operation:** constrained bootstrap may provision an operational HolonSpace before atomic PersonAgent creation/acquisition.
7. **Authorization separation:** Holochain authorship, bootstrap capability, sovereign principal, and delegated execution are distinct.
8. **No software moral agency:** Dancers, AI models, and simulations cannot become accountable Agreement parties by delegation or possession of keys.
9. **Dancer authority:** definitions/packages may preexist acquisition; operational Dancers require acquired sovereignty, delegated authority and runtime readiness, without another hApp/DHT.
10. **Persistent identity:** acquisition and restart preserve HolonSpace identity; MAP PersonAgent identity is not a device or AgentPubKey.
11. **No bootstrap escalation:** unclaimed-space privileges cannot authorize ordinary sovereign operations after acquisition.
12. **Collective distinction:** We-Space participation does not automatically constitute a collective Agent, membership, or I-Space.
13. **Agent participation:** Agents, not their I-Spaces, participate in We-Spaces through contextual roles; participation does not transfer Home Space ownership or sovereign interiors.
14. **Holonic duality:** the Agent is a whole with an interior and may be a part through participation; an AgentSpace does not independently exercise agency.
15. **PersonAgent/Person distinction:** PersonAgent is a BioSocialAgent and digital extension; Person is an ordinary informational domain holon, not a sovereign Agent.
16. **Contextual privacy:** public Persona or Visualizer references do not expose private Agent identity mappings or configuration.
17. **Independent ownership:** Home Space, semantic Agent owner, and applicable configuration scope remain separate.
18. **Deployment independence:** initial sovereignty and personal configuration do not depend on independent-space infrastructure, while preserving future compatibility.
19. **Complementary aspects:** a HolonSpace may simultaneously be a sovereign I-Space and a shared We-Space; collective acquisition preserves its existing shared-context capacity.
20. **Atomic acquisition:** BioSocialAgent creation, Home Space, sovereign association and authorization state form one atomic MAP transaction.
21. **Sovereignty continuity:** acquisition persists independently of runtime readiness; there is no separate persistent Active sovereignty state.

## 13. Open design decisions and gates

### Initial schema and sovereign acquisition

- **D1 — Exact relationship contract and enforcement:** HasInterior (BioSocialAgent → HolonSpace, declared and definitional) and IsInteriorOf (HolonSpace → BioSocialAgent, derived inverse and non-definitional) are approved. Target bindings are approved: HasInterior uses Version; IsInteriorOf uses Lineage. Collection policy is approved: both directions use IsOrdered false and AllowsDuplicates false. Deletion policy is approved: HasInterior uses Block; IsInteriorOf uses Allow. Resolve membership cache policy, committed-state and affected-endpoint validation, and removal/transfer restrictions. Exactly one interior per committed BioSocialAgent, zero-or-one sovereign per HolonSpace, and Home Space correspondence are settled, not open cardinality alternatives.
- **D2 — Acquisition authorization and commitment:** define the narrowly scoped initial proof, conflict resolution, physical atomicity boundary, durable completion evidence and idempotent failure/recovery behavior for the required atomic create-and-acquire outcome; distinguish development-only from production authorization.
- **D3 — Sovereign execution:** resolve principal, Holochain author, executor and delegation at trusted boundaries; distinguish runtime readiness from acquired sovereignty.
- **D4 — Lifecycle persistence:** choose durable provisioning/acquisition evidence and restart/recovery representation without introducing a separate persistent Active state.
- **D5 — Minimal schema/package:** approve exact Agent, BioSocialAgent and concrete PersonAgent descriptors, abstractness, properties/keys, package identity and direct dependencies; no AgentSpace/ISpace/WeSpace type hierarchy or complete technical/collective taxonomy is required.
- **D6 — Existing CoreSchema integration:** preserve the same MAP.CoreSchemaSpace through acquisition; define compatible Open/Upgrade without reloading or duplicating canonical content.

### Personal state and DAHN integration

- **D7 — Personal Usage semantics:** approve ownership/inverse, multiplicity, Home Space, applicable scopes, key isolation, deletion/reassignment and migration of existing records.
- **D8 — DAHN integration:** resolve index validity, selection precedence, background persistence and context changes consistently with owner-directed composition.

### Deferred capabilities

- **D9 — Independent-space infrastructure:** space/DHT provisioning, discovery, authoritative remote CoreSchema access, references, caches and continuity.
- **D10 — Persona lifecycle:** durable Persona/key relation, rotation, revocation, Holochain identity mapping and private disclosure.
- **D11 — We-Space participation:** qualified roles, admission, routing and shared/personal configuration; complementary space aspects and Agent-side participation are settled.
- **D12 — Agreements and collective governance:** accountable-party eligibility, constitution and representative authority, AgreementParticipation, Roles, TrustChannels and external commitments. Collective emergence and acquisition of an existing We-Space are supported architecturally; exact governance remains open.
- **D13 — Sovereignty succession:** authorized transfer, recovery and decommissioning without reopening bootstrap privileges.



## 14. Design provenance

Conformance requires evidence that the stated invariants hold, including persistent identity, authorization separation, acquisition uniqueness, restart continuity, and Agent-owned DAHN isolation. The concrete validation procedures, test suites, profiling, and implementation sequencing are defined only in `agent-spaces-impl-plan.md`.

**Reconciliation sources:**

- `agent-spaces-design-spec.md`, initial discussion draft dated 2026-11-04: foundational Agent/space separation; Personas; Agreements; collectives; disclosure; candidate relationships; persistence.
- `agent-spaces-impl-plan.md`, initial delivery plan dated 2026-11-09: initial implementation slices; schema and DAHN integration; Agent-owned VisualizerUsages; restart and profiling evidence.
- `agent-space-bootstrap-and-acquisition-spec.md`, design dated 2026-11-10: HolochainAgent grounding; relational AgentSpace; constrained bootstrap; PersonAgent acquisition; CoreSchema bootstrap pathways.
- Reconciliation decision, 2026-11-10: **anticipate independent-space capability architecturally while keeping it separate from the initial personal deployment**.

**Governing principle:** Agents are wholes that act and parts that participate. I-Spaces provide their sovereign interiors; We-Spaces provide environments for their participation. A HolonSpace may become a collective BioSocialAgent's interior without ceasing to serve as a We-Space. The Agent is distinct from and homed in that space, has exactly one sovereign interior, and may participate in other We-Spaces. Operational Dancers extend authorized sovereign agency through delegation.
