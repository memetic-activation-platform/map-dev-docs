# MAP Agent Spaces — Reconciled Design Specification

**Version:** 0.2 (reconciled design draft)  
**Date:** 2026-11-10  
**Project:** MAP / Agent Spaces  
**Status:** Design direction with explicit implementation gates; not a claim of implemented behavior

## 1. Purpose, scope, and architectural narrative

MAP is **Person-Centric rather than App-Centric**. Instead of people occupying application-owned environments, BioSocialAgents acquire sovereign digital interiors, within which application-like software Agents—**Dancers**—operate under delegated authority. This arrangement is grounded in Holochain: HolochainAgents provide cryptographic authorship and the computational means to provision and operate MAP HolonSpaces. A HolochainAgent exists before any MAP Person identity or sovereign AgentSpace has been established.

A **HolonSpace** is a bounded home for holons, not an Agent. An initially unclaimed HolonSpace can be provisioned and made operational under constrained bootstrap authority. An existing Person then establishes a MAP identity and legitimately acquires that HolonSpace as their sovereign digital interior. **AgentSpace is the relational role of that HolonSpace after acquisition, not a separate HolonType or a wrapper.** The HolonSpace retains its identity and home-space semantics. After acquisition, the Person can authorize Dancers within the AgentSpace. Dancers neither create sovereignty nor become independent Agreement parties.

The conceptual progression is:

**HolochainAgent → provisioned, operational HolonSpace → established Person identity → sovereign acquisition → AgentSpace → delegated Dancers.**

This specification reconciles the earlier Agent Spaces design draft (2026-11-04), the Agent Spaces implementation plan (2026-11-09), and the bootstrap/acquisition design (2026-11-10). It supersedes the earlier proposed `AgentSpace extends HolonSpace; ISpace extends AgentSpace; WeSpace extends AgentSpace` inheritance hierarchy. It retains the earlier specifications' Persona, participation, privacy, collective agency, and DAHN ownership requirements.

**Scope:** Agent/space ontology, I-Space and We-Space roles, Holochain grounding, CoreSchema access, onboarding and acquisition, authorization, ownership, contextual identity, Agreement eligibility, Dancers, persistence, and staged delivery boundaries. Detailed authentication protocols, TrustChannel transport, full Promise Weave, collective governance, and multi-AgentSpace runtime infrastructure remain separate design work.

**Normative language:** MUST and MUST NOT state target design invariants. Proposed names and deferred capabilities are not implemented contracts until their owning schema/design decisions are approved. A relationship's normative meaning does not require it to be populated during provisioning.

## 2. Foundational ontology

### 2.1 Holon and HolonSpace

A Holon is MAP's general representational unit at any scale. A Holon does not imply an Agent or AgentSpace. A **HolonSpace** is the foundational bounded container for holons and relationships, and the authoritative home of its locally stewarded holons. Each holon has **exactly one Home Space**. References, remote representations, and permissible immutable runtime caches do not transfer authoritative ownership.

Core HolonSpace capabilities—query, validation, transactions, recognition, navigation, and references—MUST remain usable without an associated BioSocialAgent. A HolonSpace may be provisioned before sovereign acquisition; its identity MUST persist through acquisition and restart.

### 2.2 Agent and kinds of agency

**An Agent is anything capable of sensing and responding to its environment.** Agency alone does not establish sovereignty, moral responsibility, or authority to undertake commitments. Agent is a first-class MAP semantic concept, but the complete taxonomy is not a prerequisite for initial delivery.

**HolochainAgent.** A cryptographically identified Holochain participant, signified by an `AgentPubKey`, with access to computational, storage, and communication resources. HolochainAgents author source-chain actions and provide the technical substrate for MAP operations. They do not thereby become sovereign BioSocialAgents or eligible Agreement parties. Whether HolochainAgents require first-class MAP holon representations is deferred; the runtime concept must not be mistaken for an already-declared MAP HolonType.

A HolochainAgent is identified by its AgentPubKey, not by a physical computing device. Its cryptographic identity is not inherently hardware-bound, although key generation and custody may depend on device-associated cryptographic material. Continuity of identity across execution environments requires preservation or recovery of the relevant key material and compatible Holochain source-chain state. MAP MUST NOT presume that such migration is automatically supported.

**BioSocialAgent.** A Person or appropriately constituted collective (including communities, organizations, commons, and bioregions) capable of having a sovereign I-Space. A Person exists independently of MAP; onboarding establishes a digital identity and presence, not a second Person or digital twin. Positive Agreement-party eligibility, especially for collective representation, requires explicit rules; BioSocialAgent classification alone does not automatically authorize any particular commitment.

**Dancer.** An application-like software Agent afforded by an existing AgentSpace and executing under authority delegated by that space's sovereign Agent. Dancers cannot exist independently of an affording AgentSpace and delegated authority, cannot acquire an AgentSpace, and MUST NOT sign MAP Agreements as accountable parties. A Dancer is dynamically provisionable within the AgentSpace and does not require another hApp or DHT. The retired term *Organ* is not used.

Other technical agents or computing-node representations may be modeled as needed, without creating a sovereign I-Space for each. No `proto-Agent`, universal `MoralAgent` subtype, or complete Agent inheritance tree is required for the first milestone.

### 2.3 AgentSpace as a relational role

**AgentSpace is a role of HolonSpace, constituted by a legitimate sovereign association with a BioSocialAgent.** It is not a separate HolonType, a HolonSpace subtype, or an enclosing wrapper. Acquisition MUST NOT require in-place HolonType reclassification or a replacement HolonSpace. The space's identity and existing holons remain stable.

The constitutive association is conceptually:

**BioSocialAgent — HasInterior → HolonSpace** (inverse: **IsInteriorOf**).

`HasInterior` and `IsInteriorOf` are **candidate names**, not approved descriptors. They replace the older `HasISpace`/`ISpace`-type assumption in meaning, pending reconciliation with canonical schema naming and relationship contracts. For a completed sovereign interior, the intended association is one BioSocialAgent to one I-Space and one sovereign BioSocialAgent per I-Space; intermediate unclaimed provisioning is permitted. The exact cardinality, deletion, recovery, and transfer rules require approval before schema enforcement. Technical Agents and Dancers do **not** inherit this correspondence.

### 2.4 I-Space and We-Space

**I-Space** denotes the inward aspect of an AgentSpace as an Agent's sovereign whole containing parts. **We-Space** denotes a shared context for participation and interaction among Agents; an AgentSpace also has an outward aspect as a participant in larger containing wholes. These are holonic roles and contexts, not mandatory subclasses of HolonSpace.

A We-Space is not inherently a sovereign AgentSpace, collective Agent, or social organism. A collective Agent must be constituted explicitly, with its own identity and legitimate authority; its sovereign I-Space may emerge through governance without automatically retyping an existing shared space. Membership in a collective and participation in a We-Space are different relationships: a guest may participate without becoming a constituent member.

The concrete representation of shared We-Spaces, their lifecycle, and their relation to independently stewarded HolonSpaces is **deferred** to multi-space and participation design. This specification MUST NOT be read as requiring a shared We-Space to be provisioned in AS0–AS5.

## 3. Identity, Personas, and accountable agency

### 3.1 Distinct identities

| Identity | Meaning | Not equivalent to |
| --- | --- | --- |
| Holochain `AgentPubKey` | Cryptographic Holochain author | Person, device, sovereign MAP principal |
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

Eligibility for Persons, collective Agents, bioregions, and representatives requires explicit positive rules. Neither a generic Agent type nor possession of an I-Space, Persona, or signing key automatically establishes Agreement-party eligibility.

## 4. Collective identity, Agreements, and participation

A group can have both constituent Person identities and a distinct collective Agent identity. Recognizing a collective Agent is a constitutive modeling act, not proof that the group already possesses every capacity of a living social organism. A We-Space MUST NOT automatically generate collective identity, collective membership, or a sovereign I-Space.

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

**Initial single-space deployment (AS0–AS5):** the first HolonSpace, `MAP.CoreSchemaSpace`, owns the packaged CoreSchema and is subsequently acquired as the first Person's AgentSpace. This is an intentional bootstrap arrangement, **not** a permanent ownership or deployment rule. No remote CoreSchema access is required for AS0–AS5.

The existing implementation mechanisms to preserve and reconcile include:

- `ensure_core_schema_space()` and `CoreSchemaBootstrapGate::ensure_ready()` in `host/conductora/src/setup/core_schema_bootstrap.rs`;
- `enable_bootstrap_provisioning()`;
- `complete_core_schema_bootstrap()` in `happ/crates/holons_guest/src/guest_shared_objects/guest_holon_service.rs`;
- bootstrap guards in `happ/crates/holons_guest/src/dances_guest/dance_adapter.rs`.

These are implementation touchpoints to recheck against the current repository, not a claim that onboarding or sovereign acquisition already exists.

### 5.3 Future multi-AgentSpace CoreSchema access

After AS5, independently provisioned HolonSpaces should resolve an existing authoritative CoreSchemaSpace instead of creating new authoritative CoreSchema graphs. Future bootstrap must address trusted CoreSchemaSpace identity, network/DNA discovery, schema-root reference, compatibility, authentication/trust anchor, read-only descriptor retrieval, and immutable cache/version policy.

The future initial connection cannot depend circularly on an existing Person, ordinary Agreement, or TrustChannel. Concrete transport, authorization, and reference-resolution protocols are **not specified or required for AS0–AS5**.

**Compatibility constraint:** early APIs MUST preserve distinctions between local ownership, authoritative Home Space, references, and cached immutable versions. They MUST NOT assume that all descriptors are necessarily locally homed, but they need not implement remote resolution yet. The first-space bootstrap may be implemented locally without building a speculative multi-space abstraction framework.

## 6. Provisioning, acquisition, and activation lifecycle

### 6.1 Two independent lifecycle dimensions

**Installation lifecycle:**

- **Provision:** establish durable installation/space identity, initial content, and a completion record.
- **Open:** locate completed existing state and reconstruct runtime, indexes, and caches without reprovisioning or replaying initial schema acceptance.
- **Upgrade:** apply explicit versioned application/schema changes with recovery and compatibility checks.

**Sovereignty lifecycle:**

| State | Meaning |
| --- | --- |
| `Provisioning` | HolonSpace identity and CoreSchema access are being established |
| `Unclaimed` | Operational HolonSpace available for authorized onboarding |
| `Acquired` | Legitimate BioSocialAgent–HolonSpace sovereign relationship committed |
| `Active` | Ordinary authorized AgentSpace operations enabled |

These are conceptual lifecycle states, **not new HolonTypes**. Their durable representation and exact transition contracts must be settled in AS0. `Provisioning` may initially be runtime state; completed acquisition must be reconstructible after restart.

### 6.2 Initial single-space flow

1. Initialize HolochainAgent execution and conductor/cell context.
2. Enter explicitly constrained CoreSchema bootstrap authority.
3. Provision `MAP.CoreSchemaSpace`, load and commit the packaged CoreSchema, and bind the space identity.
4. Verify CoreSchema readiness and complete durable provisioning.
5. Expose an operational **unclaimed** HolonSpace and foundational **Welcome to the MAP** onboarding capability.
6. Establish or resolve the existing Person's MAP identity and the necessary initial authentication/authorization evidence.
7. Validate eligibility and authorization for acquisition; commit the Person–HolonSpace sovereign association consistently.
8. Disable acquisition-only bootstrap privileges, establish ordinary sovereign execution context, and activate the AgentSpace.
9. Permit the sovereign Agent to afford/delegate to Dancers, including Space Navigator when available.

**Welcome is a foundational bootstrap/onboarding capability, not a Dancer.** A Dancer cannot be the actor that creates the sovereignty on which its own existence depends.

### 6.3 Acquisition contract

Acquisition MUST:

- Confirm that the Person's semantic identity is established independently of the Holochain author key.
- Confirm that the HolonSpace is operational, unclaimed, and eligible.
- Verify authorized acquisition under an explicitly defined bootstrap/admission rule.
- Establish the constitutive `HasInterior` relationship (or approved equivalent) and applicable authorization state.
- Commit without permitting conflicting sovereign associations or duplicate successful acquisitions.
- Support deterministic recovery after interruption and preserve the space's identity and preexisting holons.
- Prevent normal operations from reverting an acquired space to `Unclaimed` to bypass authorization.

Transfer, succession, recovery of lost credentials, and decommissioning require separate authorized procedures and are not implicitly solved by the initial acquisition mechanism.

### 6.4 First-milestone authentication boundary

AS2 MUST establish a persistent Person identity, sovereign association, and enforceable separation between bootstrap and ordinary authority. It **need not implement the complete future authentication architecture**. A constrained local development bootstrap may establish the initial principal, provided its limitations are documented and it is not represented as production-grade proof of sovereignty. A caller-supplied Person ID or Holochain AgentPubKey alone is not adequate authorization evidence.

### 6.5 Authorization matrix

| Capability | Provisioning | Unclaimed | Acquired / Active |
| --- | --- | --- | --- |
| Initialize local HolonSpace | Bootstrap only | Denied | Denied |
| Establish/read CoreSchema | Bootstrap only | Scoped reads | Authorized access |
| Welcome/onboarding | Not yet | Scoped | Optional, separately authorized |
| Establish initial Person identity | Denied | Scoped | Governed normal operation |
| Acquire this HolonSpace | Denied | Authorized once | Denied |
| Ordinary holon mutation | Provisioning-only | Onboarding-only | Sovereign/delegated authority |
| Provision or invoke Dancers | Denied | Denied | Authorized delegation |
| Undertake MAP Agreements | Denied | Denied | Only eligible accountable Agents |

The matrix states required policy boundaries, not necessarily distinct APIs. Authorization MUST be enforced at trusted runtime/zome boundaries, not solely in the UI. Coordinator checks and integrity validation must have an explicit division of responsibility; no blanket authorization bypass may persist after acquisition.

## 7. Stewardship, semantic ownership, and contextual disclosure

### 7.1 Distinct ownership facts

The implementation MUST preserve three independent facts:

1. **Home Space:** where the holon's authoritative state is stewarded; existing Core `OwnedBy`/`Owns` relationships have HolonSpace semantics.
2. **Semantic Agent owner:** the Agent whose personal configuration or responsibility the holon expresses.
3. **Applicable context/scope:** the circumstances in which that configuration or authority applies.

For example, a VisualizerUsage may be homed in a HolonSpace, owned by a Person Agent, and scoped to a subject type, Slot, or composition context. Agent ownership MUST NOT retarget or replace Core Home Space ownership.

### 7.2 Agent-owned VisualizerUsages

The first AgentSpace must provide an explicit, authorized path to its sovereign Agent so that DAHN can discover personal VisualizerUsages from that Agent rather than treating public Visualizers or subject ancestry as authoritative personal ownership indexes.

The integration contract must define Agent-to-Usage relationship direction/inverse, multiplicity, context scope, home-space placement, reassignment/deletion, keys, and existing-record migration. Shared Visualizers and subject types MUST NOT cause different Agents' configurations to collide or leak. Default-only rendering MUST NOT create durable personal Usages. Background saves must retain the correct principal/context and must not block foreground usability.

Selection may bulk-acquire authorized personal state and build a reusable Rust-derived index. It must preserve specialization, applicable Visualizers, explicit pins, ValueType preferences, composition-local overrides, Slot contracts, Themes, runtime compatibility, and authorization. Index validity must respond to Agent/context changes, edits, background persistence, schema/policy changes, and Space Session reset. TypeScript consumes Rust-authorized results; no parallel ownership mechanism should be introduced in the host adapter.

### 7.3 Disclosure and TrustChannels

Persona identity does not define a global permission set. Effective disclosure depends on Agreement and participation context. Proposed reusable disclosure selections may group permissions, but editing a reused selection MUST NOT silently enlarge an existing Agreement's grant.

TrustChannels are the intended Agreement-governed boundary for inter-space exchange; Declared External Commitments may govern relevant Exosphere interactions. Their detailed endpoints, routing, and transport are deferred. Permission to invoke a Dance does **not** automatically authorize every returned datum. Type/property/relationship checks are necessary but cannot prove arbitrary values contain no sensitive derivations. None of these capabilities is mandatory for AS0–AS5.

## 8. Candidate schema and relationship inventory

This inventory preserves the earlier design's useful associations while reflecting the relational AgentSpace model. **Names and concrete descriptors remain provisional** until reconciled with canonical TDL, single inheritance, direct dependencies, inverse materialization, and existing contracts.

| Source | Candidate association | Target | Meaning / status |
| --- | --- | --- | --- |
| BioSocialAgent | `HasInterior` | HolonSpace | Constitutive sovereign association; candidate replacement for `HasISpace` |
| HolonSpace | `IsInteriorOf` | BioSocialAgent | Inverse of sovereign association |
| Agent | `HasPersona` | Persona | Contextual identities; mapping visibility restricted |
| Persona | `HasProfile` | Profile | Contextual description; proposed |
| Agent | `HasLifeCode` | LifeCode | Optional values/goals/governance |
| We-Space context | `HasLifeCode` | LifeCode | Optional shared contextual commitments |
| CollectiveAgent | `HasMember` | Agent | Constituent membership, not venue participation |
| We-Space context | `HasCollectiveIdentity` | CollectiveAgent | Only where explicitly constituted |
| AgreementParticipation | `InAgreement` | Agreement | Proposed qualified participation |
| AgreementParticipation | `UsesPersona` | Persona | Proposed participating identity |
| AgreementParticipation | `AssignedRole` | Role | Proposed Agreement-scoped Role |
| HolonSpace in AgentSpace role | `GovernedBy` | Agreement | Candidate governance association, not signing eligibility |
| Sovereign interior | `HasTrustChannel` | TrustChannel | Governed boundary exchange |
| TrustChannel | `GovernedBy` | Agreement | Agreement-governed exchange |
| TrustChannel | `BoundByExternalCommitment` | DeclaredExternalCommitment | Candidate Exosphere boundary |
| HolonSpace in AgentSpace role | `HostsDancer` | Dancer | Delegated execution within interior |
| Agent | `DelegatesTo` | Agent | Proposed delegation; scope and authority required |
| Agent | `OwnsPersonalUsage` | VisualizerUsage | Candidate semantic ownership, distinct from Home Space |

The table's role-qualified sources are semantic descriptions, **not proposed new HolonTypes**. Exact source/target descriptors, inverse names, constraints, and optionality require AS0 review. Additional associations to Enquiries, Offers, Promises, Promise Weaves, Modules, descriptors, and DAHN preferences belong to their respective owning designs. Association does not imply authorization to traverse or disclose private identity mappings.

## 9. Multi-AgentSpace strategy and compatibility boundary

**Multi-AgentSpace capability is a substantial, separate undertaking and MUST NOT be a dependency of AS0–AS5.** The first delivery operates one authoritative HolonSpace/AgentSpace, which also serves as `MAP.CoreSchemaSpace`.

Early work MUST nevertheless avoid structural assumptions that preclude later independent spaces:

- Keep Agent, HolonSpace, HolochainAgent, Persona, conductor, and device identities distinct.
- Preserve unique authoritative Home Space and external-reference semantics.
- Separate CoreSchema availability from ownership, even when initially local.
- Keep the active sovereign Agent/context explicit rather than relying on global singletons or implicit key-to-Person equivalence.
- Separate bootstrap, acquisition, and ordinary authorization concerns.
- Maintain package boundaries and direct schema dependencies without introducing Core → Agent Spaces/DAHN dependency cycles.
- Do not require Agreements, TrustChannels, or remote discovery for initial personal configuration.

**AS0–AS5 do not implement:** multiple independently operating AgentSpaces, remote CoreSchema resolution, cross-DHT discovery, inter-space TrustChannels, shared We-Space admission, or cross-space governance. Future multi-AgentSpace infrastructure should receive its own milestone **after AS5**, before delivery features that actually require inter-space interaction.

Representing multiple Agents as holons within the first AgentSpace does **not** imply multi-AgentSpace capability.

## 10. Persistence and runtime requirements

Provisioning MUST record durable completion independently of incidental schema presence. Opening MUST reconstruct the same installation, HolonSpace, Agent association, and saved holons without reprovisioning. Upgrades MUST be explicit, versioned, and recoverable. Interrupted provisioning/acquisition, duplicate calls, conflicting associations, incompatible versions, and partial durable state require defined detection and recovery; neither an in-memory space ID nor a successful transport response alone proves readiness.

Existing Reference Layer binding, TransactionContext mutation/Commit, and wire projection boundaries must be preserved. No direct-storage shortcut or competing mutation API should be introduced. Descriptor recognition and validation follow their owning specifications; opening is not permission to replay initial content acceptance on every startup.

Schema descriptors should be introduced through non-Core packages and ordinary configured imports, with direct dependencies, single `extends` declarations where applicable, and both relationship directions declared consistently with the TDL/descriptor rules. Generated JSON/manifests are produced by repository tooling, not manually edited. The relational AgentSpace model removes the earlier requirement to create an AgentSpace/ISpace/WeSpace inheritance hierarchy.

## 11. Incremental delivery contract

This section sets **scope boundaries**; detailed work breakdown, repository baselines, tests, and PR sequencing belong in `agent-spaces-impl-plan.md`.

| Unit | Outcome | Multi-space requirement |
| --- | --- | --- |
| **AS0** | Approve ontology, relationship contracts, local bootstrap/acquisition, authorization, package ownership, and Agent/Usage integration | Compatibility only |
| **AS1** | Load minimal non-Core Agent/Person and required relationship schema; plain HolonSpace still works | None |
| **AS2** | Provision first HolonSpace/CoreSchemaSpace, establish Person identity, acquire/activate it, and prove Provision/Open/Upgrade and restart continuity | None |
| **AS3** | Persist and retrieve Agent-owned personal VisualizerUsages with proper scope and isolation | None |
| **AS4** | Use authorized Agent/context personal-state access in Rust selection with valid derived indexing | None |
| **AS5** | Profile and verify first-AgentSpace and DAHN selection outcomes | None |
| **AS6** | Separately scoped multi-AgentSpace infrastructure: independent provisioning, discovery, CoreSchema access, references, and necessary communication | Required here |
| **AS7** | Personas and shared We-Space participation, with relevant admission/privacy design | Where cross-space interaction is needed |
| **AS8** | Governed collective Agents, Agreements, and accountable participation | As required by feature |

The former **AS2b** repeat-personal-provisioning milestone is **not an AS0–AS5 prerequisite**. Repeatable provisioning of a second independent AgentSpace belongs with AS6 unless a narrower single-space demonstration can be performed without claiming multi-space support. No new second-space requirement should be hidden in AS2.

AS1–AS2 establish the durable first-AgentSpace foundation; AS3–AS5 deliver personal configuration and DAHN selection performance. Full Promise Weave, LifeCodes, TrustChannels, complete Persona lifecycle, and collective governance are not gates for those early units.

## 12. Architectural invariants

1. **Technical grounding:** authoritative distributed MAP state changes require authorized HolochainAgent execution.
2. **Single Home Space:** each holon has one authoritative Home Space; references/caches do not transfer ownership.
3. **Space/Agent separation:** a HolonSpace is not an Agent.
4. **Relational AgentSpace:** AgentSpace is a HolonSpace role established through legitimate sovereign association, not a HolonType.
5. **BioSocial sovereignty:** sovereign I-Space correspondence applies to BioSocialAgents, not automatically to Dancers or HolochainAgents.
6. **Unclaimed operation:** constrained bootstrap may provision an operational HolonSpace before Person acquisition.
7. **Authorization separation:** Holochain authorship, bootstrap capability, sovereign principal, and delegated execution are distinct.
8. **No software moral agency:** Dancers, AI models, and simulations cannot become accountable Agreement parties by delegation or possession of keys.
9. **Dancer dependency:** Dancers require an affording AgentSpace and delegated authority; no extra hApp/DHT.
10. **Persistent identity:** acquisition and restart preserve HolonSpace identity; MAP Person identity is not a device or AgentPubKey.
11. **No bootstrap escalation:** unclaimed-space privileges cannot authorize ordinary sovereign operations after acquisition.
12. **Collective distinction:** We-Space participation does not automatically constitute a collective Agent, membership, or I-Space.
13. **Contextual privacy:** public Persona or Visualizer references do not expose private Agent identity mappings or configuration.
14. **Independent ownership:** Home Space, semantic Agent owner, and applicable configuration scope remain separate.
15. **Incremental delivery:** AS0–AS5 MUST remain independent of multi-AgentSpace infrastructure while preserving future compatibility.

## 13. Open design decisions and gates

### Required for AS0–AS2

- **D1 — Relationship contract:** approve `HasInterior`/inverse or existing canonical equivalents, cardinality, source/target bindings, uniqueness, deletion/transfer behavior, and validation gates for unclaimed versus acquired spaces.
- **D2 — Acquisition authorization:** define the narrowly scoped first-person acquisition proof, conflict resolution, idempotency, and atomicity/recovery behavior; distinguish development bootstrap from production authorization.
- **D3 — Sovereign execution:** define how runtime context resolves principal, Holochain author, and delegated executor; enforce lifecycle constraints at trusted boundaries.
- **D4 — Lifecycle persistence:** choose durable representation of provisioning, unclaimed, acquired, active, completion records, and recovery after restart.
- **D5 — Minimal schema/package:** choose first concrete Agent kind, TDL ownership, direct dependencies, and exact schema contracts without new AgentSpace subtypes.
- **D6 — Existing CoreSchema integration:** ensure first HolonSpace is `MAP.CoreSchemaSpace`, and ordinary Open/Upgrade does not reload or duplicate canonical content.

### Required for AS3–AS5

- **D7 — Personal Usage semantics:** approve Agent ownership, inverse, multiplicity, home placement, applicable scopes, key isolation, deletion/reassignment, and migration of existing Usage records.
- **D8 — DAHN integration:** resolve personal-state index validity, selection precedence, background persistence, context switches, and relationship to owner-directed composition.

### Deferred beyond AS5

- **D9 — Multi-AgentSpace infrastructure:** space/DHT provisioning, network discovery, remote CoreSchema authentication/retrieval, reference resolution, cache policy, and space identity continuity.
- **D10 — Persona lifecycle:** durable Persona/key relationship, rotation, revocation, Holochain identity mapping, and private identity disclosure.
- **D11 — Shared We-Spaces:** participation/admission, routing, distinction from collective membership, and shared/personal configuration policies.
- **D12 — Agreements and governance:** accountable-party eligibility, representative authority, AgreementParticipation, Roles, TrustChannels, external commitments, and disclosure enforcement.
- **D13 — Sovereignty succession:** transfer, recovery, and decommissioning without reopening bootstrap authority.

## 14. Acceptance criteria

### AS0–AS2: first sovereign AgentSpace

- [ ] Plain HolonSpace operations remain usable without a Person/AgentSpace association.
- [ ] HolochainAgent initialization and CoreSchema provisioning do not require an existing MAP Person.
- [ ] The initial `MAP.CoreSchemaSpace` is the same HolonSpace subsequently acquired by the first Person.
- [ ] Welcome/onboarding is available under constrained bootstrap authority without an independently authorized Dancer.
- [ ] Person identity is distinct from Holochain AgentPubKey and device identity.
- [ ] Acquisition commits a unique sovereign relationship without changing the HolonSpace's HolonType or identity.
- [ ] Repeated, interrupted, or conflicting acquisition attempts cannot produce conflicting sovereign owners.
- [ ] Bootstrap authority cannot bypass ordinary authorization after acquisition.
- [ ] Provision, Open, and Upgrade are distinct; restart reopens the same Agent, space, and saved holons without reprovisioning.
- [ ] No multi-AgentSpace infrastructure is required to pass the first milestone.

### AS3–AS5: Agent-owned DAHN state

- [ ] Personal VisualizerUsage is semantically owned by an Agent independently of its Home Space and applicability scope.
- [ ] Two Agents cannot read, overwrite, or inherit each other's personal Usages merely by sharing Visualizer/subject identifiers.
- [ ] Personal Usage can be discovered through authorized Agent/context access, and its persistence survives restart.
- [ ] Default-only rendering creates no durable personal Usage; required background saves do not gate foreground usability.
- [ ] Derived selection state is invalidated correctly on context, policy, schema, and session changes.
- [ ] Profiling reports first-load and repeated-selection costs without assuming an arbitrary performance target.

### Future multi-AgentSpace acceptance (not AS0–AS5)

- [ ] A new independent HolonSpace can access an existing authoritative CoreSchemaSpace without creating another authoritative CoreSchema copy.
- [ ] Inter-space references and permitted caches preserve Home Space and version identity.
- [ ] Shared We-Space participation does not implicitly create a collective Agent or disclose private Persona mappings.

## 15. Validation and design provenance

Implementation work must use the repository's applicable TDL/schema compilation, regeneration, descriptor-kernel, host/WASM, transaction, and real-conductor integration tests. Restart, failure/retry, relationship persistence, and acquisition concurrency need end-to-end evidence. DAHN selection changes require focused Rust/SDK/UI tests and controlled profiling; the existing implementation plan contains the detailed measurement contract. Do not claim tests or repository audits that have not been run.

**Reconciliation sources:**

- `agent-spaces-design-spec.md`, initial discussion draft dated 2026-11-04: foundational Agent/space separation; Personas; Agreements; collectives; disclosure; candidate relationships; persistence.
- `agent-spaces-impl-plan.md`, initial delivery plan dated 2026-11-09: AS0–AS7 implementation slices; schema and DAHN integration; Agent-owned VisualizerUsages; restart and profiling evidence.
- `agent-space-bootstrap-and-acquisition-spec.md`, design dated 2026-11-10: HolochainAgent grounding; relational AgentSpace; constrained bootstrap; Person acquisition; CoreSchema bootstrap pathways.
- Reconciliation decision, 2026-11-10: **anticipate multi-AgentSpace capability architecturally but defer implementation and dependencies until after AS5**.

**Governing principle:** HolochainAgents provide the technical foundation; HolonSpaces provide bounded digital interiors; BioSocialAgents acquire those interiors as sovereign AgentSpaces; Dancers extend sovereign agency through delegation. Shared We-Spaces support interaction and the possible emergence of collective agency without automatically becoming Agents themselves.
