# Agent Spaces Implementation Plan

## Status and intended outcome

**Version:** 0.8 (finite CS-L1 lifecycle authorization dependency)

**Date:** 2026-11-14

**Status:** AS1 merged and verified; AS2 remains planned and gated. See the dated delivery records below.

Implement the target architecture defined exclusively by [Agent Spaces design specification](agent-spaces-design-spec.md) v0.8 through reviewable increments. The initial delivery establishes a durable first personal HolonSpace hosting local CoreSchema, an established PersonAgent identity, atomic PersonAgent creation/acquisition and authorized runtime opening, and Agent-owned VisualizerUsages used by DAHN selection. The first AgentSpace must reopen without reprovisioning. Multi-AgentSpace infrastructure is anticipated in early interfaces but **not implemented or required through AS5**; it is a separate AS6 undertaking. Personas, shared We-Spaces, and governed collectives follow in AS7–AS8.

**Document boundary:** The design specification alone defines target semantics, invariants, and unresolved design gates. This implementation plan contains only delivery sequence, dependencies, repository touchpoints, implementation tasks, migration steps, and verification evidence. Where a design gate remains open, the step is to resolve it **in the design specification first**, then implement it; this plan does not settle it by implication. Candidate names below are references to design-spec proposals, not approvals.

## Authority and boundaries

- [Agent Spaces specification](agent-spaces-design-spec.md): Agent versus I-Space,
  relational AgentSpace, BioSocialAgent sovereignty, operational versus moral agency, Persona privacy, and collective identity.
- [DAHN §11.1](../hx/dahn-design-spec.md#111-visualizerusage): personal Usage,
  authorized agent/context access, applicable scope, default rendering without
  personal records, and selection authority.
- [Core runtime](../core-runtime/index.md),
  [Space Session](../core-runtime/space-session-design-spec.md), and
  [runtime shared types](../core-runtime/runtime-shared-types.md): execution,
  lifetime, and Focal Space boundaries.
- [Core Schema bootstrap](../core-schema-bootstrap/core-schema-bootstrap-design-spec.md)
  and its [implementation alignment](../core-schema-bootstrap/core-schema-bootstrap-implementation-plan.md):
  Core readiness and post-Core provisioning boundaries.
- [TDL specification](../type-system/tdl/tdl-spec.md) and
  [descriptor semantics](../type-system/descriptor-semantics-rules.md): exact
  schema dependencies, single inheritance, relationship contracts, and validation.
- [DAHN roadmap](../hx/dahn-implementation-plan.md) and
  [integrated plan](../space-navigator/space-navigator-impl-plan.md): surrounding
  selection, composition, and personalization work.

The [AgentSpace architecture](agent-space-arch.md) is an overview subordinate to the design specification. Agent, HolonSpace, Holochain author and provisioned runtime remain distinct; the target hApp/coordinator names do not imply that implementation renaming has landed.

## Repository baseline

Read-only inspection used map-holons `main` at `b35a4745` and profiling branch
`codex/profile-visualizer-selection` at `fba06a71`. These are local checkpoints,
not claims about remote merge status. Recheck them before implementation.

| Area | Observed implementation | Delivery implication |
| --- | --- | --- |
| Core ownership | `schema-src/core/relationship-types.tdl` targets `OwnedBy` at `HolonSpace.HolonType`; `Owns` is its inverse | Agent ownership is a distinct domain association. Do not retarget Core ownership to Agent. |
| Agent types | No Agent, AgentSpace, ISpace, or WeSpace declarations found in the inspected canonical TDL | Introduce a non-Core schema package rather than treating existing UI space interfaces as domain descriptors. |
| Usage schema | `schema-src/dahn/schema.tdl` declares VisualizerUsage, Visualizer/subject/Slot associations, preferences, and override types | Preserve these meanings while adding explicit Agent access and context semantics. |
| Usage lookup | `shared_crates/holons_core/src/dahn/usage.rs` and `dances/visualizer_usage_resolution.rs` reach Usages from the selected Visualizer; resolution also examines subject lineage | Agent-owned bulk access and applicability evaluation must replace this as the authoritative personal discovery path. |
| Usage keys | `record_key` derives local keys from Visualizer and subject-type IDs | Revisit owner/context isolation and specialization; adding Agent ownership without revisiting keys can collide. |
| Host adapter | `host/crates/dahn_selection/src/usage.rs` re-exports the shared Usage implementation | Do not add an independent host-only ownership model alongside the shared path. |
| Provisioning | Conductora has `setup/core_schema_bootstrap.rs` and `setup/space_imports.rs` | Reuse ordinary loader and transaction boundaries. Existing bootstrap readiness gaps remain explicit. |
| Profiling branch | Selector spans, correlated backend fetches, IPC timings, and `scripts/summarize-selector-profile.py` exist on the branch | Retain the measurement work, reconcile with current main, and use it to evaluate AS4/AS5. It does not itself supply Agent ownership. |

## Delivery guardrails

Follow design-spec §§2, 5–10 and 12 for authoritative constraints. For implementation, maintain these guardrails:

1. Keep Core HolonSpace query, transaction, validation, and navigation paths usable before acquisition and without an Agent association.
2. Introduce Agent/PersonAgent and the approved sovereign **relationship**, not AgentSpace, ISpace, or WeSpace HolonType specializations. Avoid in-place type rewrites during acquisition.
3. Keep Home Space, semantic Agent ownership, and applicable Usage scope distinct. Preserve Core `OwnedBy`/`Owns` semantics.
4. Use ordinary bound references, TransactionContext/Commit, ingress binding, and egress projection; no direct-storage shortcuts.
5. Preserve acyclic packages and direct descriptor dependencies. Do not make Core depend on Agent Spaces or DAHN.
6. Resolve principal, Holochain author, executor, and active space explicitly; do not infer PersonAgent from public key, host process, account, Persona, or caller-supplied ID.
7. Keep the bootstrap authority constrained and enforce the transition to sovereign/delegated authorization at trusted boundaries. Consume the approved Client Security local contract; distinguish unverified implementation assurance from the production authority model.
8. Default-only rendering creates no durable personal Usage; background saves must not block foreground usability.
9. Operational Dancers require the acquired-space authority and runtime readiness defined in design §2.2/§6. Definitions/packages may load before acquisition; do not add an acquisition prerequisite to schema import.
10. Keep single-home schema stewardship and immutable reference/cache identity explicit, without implementing remote CoreSchema resolution in AS0–AS5.
11. **Do not add multi-AgentSpace provisioning, cross-DHT discovery, remote schema reads, TrustChannels, or shared-space admission to AS0–AS5.** Representing multiple Agents as holons is not multi-AgentSpace operation.

## Sequence and usable milestones

| Unit | Depends on | Reviewable outcome |
| --- | --- | --- |
| AS0 — Resolve first delivery contracts | None | Owning design-spec gates D1–D8 resolved for the affected increments; schema/package and migration contracts reviewed |
| AS1 — Load minimal Agent/PersonAgent schema | AS0 decisions needed for AS1 | Minimal non-Core Agent/PersonAgent descriptors and sovereign relationship contracts load; plain HolonSpace remains usable |
| AS2 — First sovereign AgentSpace | AS1, applicable AS0 decisions | Initial personal HolonSpace with local CoreSchema, PersonAgent constituted with its interior, runtime ready; Provision/Open/Upgrade and restart verified |
| AS3 — Persist Agent-owned personal Usages | AS2, Usage design gates | Personal configuration stored and retrievable through authorized Agent/context access |
| AS4 — Agent/context selection | AS3 | Rust selection reuses correctly scoped personal-state index; defaults remain write-free |
| AS5 — Profile and close first milestone | AS4 | Measured selection costs, correct ownership and restart behavior; no multi-space prerequisite |
| AS6 — Multi-AgentSpace infrastructure | AS5 for this delivery sequence; separate infrastructure design gates | Independent spaces, remote authoritative CoreSchema access, reference resolution and required communication; repeat personal provisioning |
| AS7 — Personas and shared We-Space participation | AS6 where cross-space interaction required; identity/admission design gates | Contextual identities and shared interaction without implicit collective identity |
| AS8 — Governed collective and Agreement capabilities | AS7 and governance/eligibility design gates | Accountable participation, collective sovereignty, and delegated execution |

AS1–AS2 deliver the first durable sovereign AgentSpace. AS3–AS5 deliver Agent-owned personalization and selection performance. The former AS2b is retired as a separate pre-AS5 gate; second independent AgentSpace provisioning is verified in AS6. A narrower test representing multiple Agent holons in the first space is allowed but does not count as multi-space support. Unit identifiers are delivery labels, not runtime types. Split units into independently reviewable PRs; create issues once the relevant design gates have been resolved.

### AS0 — Close implementation-relevant design contracts

Use design-spec §§2–3, 5–6, 10–13 as authority. The latest reconciliation settles the core ontology and cardinality; do not reopen those decisions as implementation preferences. Record additional semantic decisions in their owning specification: Agent Spaces domain, Client Security, or shared transaction/validation infrastructure, not this plan.

- Reconcile D1/D5 with canonical TDL: exact Agent/BioSocialAgent/PersonAgent descriptors, abstractness, properties/keys, package identity and direct dependencies; declared/inverse names, endpoints, bindings, duplicates/order policy and enforcement boundaries.
- Map the settled interior requiredness, space-side optionality, Home Space correspondence and staged/committed boundary to existing descriptor-aware assessment and ordinary Commit. Identify how inverse-side conflicts and removal/reassignment on saved sources are detected; no parallel validator.
- Apply resolved D2 Local Sovereign Constitution. Route local authority and assurance decisions to Client Security CS-L1, commitment/history mechanisms to shared transaction/validation owners, and lifecycle completion/compatibility predicates to Agent Spaces D4/D6. Preserve the same first personal HolonSpace and its local CoreSchema without retyping or a second space; the display name is independent of CoreSchema hosting.
- Have the shared transaction/persistence workstream inspect Commit, relationship-persistence and zome-call boundaries and supply the bounded atomic create/acquire contract. Document confirmed guarantees, gaps, partial-result detection, conflict handling and idempotent recovery. A shared transaction ID or transport success is not sufficient evidence.
- Inspect the existing bootstrap/import path to distinguish loadable Dancer definitions/packages from operational Dancer execution; preserve pre-acquisition imports while gating operation at trusted boundaries.
- Resolve D7/D8 before AS3/AS4: Agent-owned Usage direction/inverse, key isolation, scope, Home Space, migration, background authority and derived-index validity. Evaluate a separate Agent Spaces–DAHN integration package versus one-way dependency without cycles.
- Reconcile older organism, AgentSpace subtype, I-Space participation and exclusivity wording in its owning documents. Use PersonAgent for the sovereign personal Agent; do not require an ordinary Person record.
- Review compatibility for future spaces without designing or implementing AS6 transport/discovery/reference protocols.

**Exit evidence:** the schema-affecting subset is approved for AS1; D2's authority model is approved; implementation-security, lifecycle and atomicity contracts are approved before enabling the corresponding privileged paths; later gates remain named. Settled decisions stay in the design specification and no multi-space dependency is introduced.

### AS1 — Load the minimal Agent Spaces schema

**Design-ready scope:** implement the approved schema/package, not onboarding or shared key/relationship infrastructure. See design §§2.2.2–2.3 and the explicit transitional dependencies below.

- Author `schema-src/agent-spaces/schema.tdl` for **MAP Agent Spaces Schema v0.1.0**, directly dependent on CoreSchema only. Use abstract Agent, abstract BioSocialAgent and concrete PersonAgent with single inheritance and existing MetaHolonType conventions. No new TypeKind anchor, ordinary Person type, complete taxonomy, Dancer reparenting or AgentSpace/ISpace/WeSpace types.
- License optional FirstName/MiddleName and required LastName on PersonAgent. Select its configured target FormatRule `{0}.[1].[2]`, with ordered name-property parameters; both literal dots survive absence. Do not introduce extra Agent/BioSocialAgent scalar properties.
- Declare HasInterior and IsInteriorOf together. License the declared HasInterior on BioSocialAgent and use ordinary inverse discovery/materialization. Preserve Core independence. AS1 delivered the then-approved Version/Lineage bindings, ExactlyOne/ZeroOrOne cardinalities, unordered/no-duplicates policy, Block/Allow deletion values and absent/24-hour membership TTL. Design v0.6 changes the target forward binding to Lineage; the AS2 delta and shared binding/traversal evidence must not be reported as already delivered by AS1.
- Compile and regenerate imports/resources using existing tooling. AS1 generalized `ensure_configured_space_imports` to a resource-root `imports` set containing direct generated-JSON paths, replacing the package `schema_imports` manifests and their resource-sync assumptions. Reuse that delivered ordinary loader route; add no second loader and do not model this package as a Dancer.
- Load after Core and before dependent consumers, without requiring sovereign acquisition. Check actual descriptor references to establish the exact direct Core version and avoid accidental DAHN/Dancer dependencies.
- Verify ordinary first import and repeat-import outcome. Identical-version identity reuse is the target; current create-based repeat import may reject through ordinary uniqueness validation. Document rejection and absence of duplicate publication as an interim limitation, not idempotent reuse. Do not implement a loader upgrade protocol in AS1 or claim that a transport success proves completion.
- Use conforming fixtures whose PersonAgent Home Space matches HasInterior. **Defer enforcement of Home Space correspondence and the general cross-version sovereign-replacement prohibition mechanism to AS2**, before constitution/acquisition. Do not add special-case validators here.

**Shared enforcement dependencies and evidence:**

General relationship pairing, endpoint compatibility, binding-aware directional cardinality, collection policy, and prospective affected declared/inverse buckets are already specified, with complete Commit enforcement assigned to shared Capability 4. AS1 does not deliver Capability 4. Existing discovery, mutation classification, binding materialization and inverse traversal are distinct from complete Commit rejection. Where the implementation baseline supplies an active rule, exercise it; otherwise record the exact missing enforcement and its shared owner. Neither schema declarations nor valid fixture success demonstrate a negative-case rejection that has not been implemented. AS2 is gated on required enforcement before real constitution/acquisition.

**Exit evidence:**

- Approved TDL compiles and package declarations/dependencies pass available schema/kernel checks; generated resources are reproducible.
- Missing required LastName and optional-name omissions are checked through delivered ordinary property validation. Key synthesis/mismatch checks follow the temporary-key boundary below.
- Plain HolonSpace works before and after import with no sovereign association. The package does not retype, replace or rename the existing space as a side effect of import.
- A complete, conforming PersonAgent fixture commits using ordinary bound references; fresh-transaction forward/inverse traversal preserves the original space and content.
- Record which of missing/multiple interiors, inverse conflicts, endpoint mismatches, duplicate/order violations and graph-only removal/replacement are rejected by the active shared validator, and which await Capability 4. Do not implement a general relationship validator or deletion engine in this issue.
- Repeat import has explicit identity/version/rejection evidence. No silently duplicated logical schema definitions are accepted.
- Delivery evidence distinguishes schema completion, pending shared key/relationship enforcement, and the two explicitly deferred AS2 enforcement mechanisms.

Fixture success proves the delivered schema/validation surface, not legitimate acquisition, race-free sovereignty or physical persistence atomicity.

#### Temporary PersonAgent key authoring before #868

**Target and ownership.** The design-spec §2.2.2 contract remains `LastName.FirstName.MiddleName`, with parameters `[LastName, FirstName, MiddleName]` and target template `{0}.[1].[2]`. [map-holons #868](https://github.com/evomimic/map-holons/issues/868) owns the shared positional-template capability and optional components; [map-dev-docs #87](https://github.com/memetic-activation-platform/map-dev-docs/issues/87) and the Commit Validation Implementation Plan own the remaining shared composition, producer and enforcement contracts. Those implementations are queued behind validation work. AS1 MUST NOT duplicate them or silently treat them as delivered.

**Interim path for schema work.** Author the target configured rule in canonical TDL and use explicit, precomputed `Key` values in AS1 schema-level fixture/loader inputs. This uses the existing authored-key path; it is not a substitute runtime KeyRule, custom renderer, or product onboarding API. Preserve optional property absence in the subject data. For example:

| LastName | FirstName | MiddleName | Explicit interim Key |
| --- | --- | --- | --- |
| Smith | Jane | Marie | `Smith.Jane.Marie` |
| Smith | Jane | absent | `Smith.Jane.` |
| Smith | absent | absent | `Smith..` |

Do not populate missing optional names with empty-string defaults, require those properties, switch to LastName-only/UUID/NoneRule, or introduce a second key-producing algorithm. Fixtures should state expected keys directly. Keys remain explicit state, subject to all currently active property, key-shape and uniqueness validation; no rule or validation failure may be bypassed to make this path work.

**Evidence and compatibility gate.** Recheck the implementation baseline when AS1 starts. Demonstrate that the current schema compiler, loader and active validator accept the target rule declaration and explicit-key fixtures through ordinary paths. Report separately (a) descriptor/package loading and relationship/name-property behavior demonstrated now, and (b) target synthesis, compose-and-set, and stored-key mismatch rejection awaiting shared infrastructure. Explicit-key fixture success does not prove automatic synthesis or enforcement. If newly active validation requires an unavailable renderer, or the target declaration cannot pass the ordinary path, the affected AS1 slice is blocked on the owning dependency; do not weaken the target schema or disable validation. Record any deferred key acceptance evidence in the AS1 delivery record rather than claiming the complete target key capability is verified.

**Removal of the workaround.** Once #868 and the applicable shared composition/producer/Commit-validation increments land, use their ordinary compose-and-set path in producers and exercise optional inputs and key mismatch rejection through the integrated implementation. Reuse the same declared rule and expected key strings. No rekeying is intended solely because explicit authoring is replaced by shared composition; any actual output mismatch requires explicit reconciliation rather than rewriting historical keys. Preserve ordinary lineage identity, historical key claims and exact references. Product/runtime producer behavior belongs to its delivery milestone; AS1 adds no onboarding implementation.

### AS2 — Provision, acquire, open, and upgrade the first AgentSpace

**Lifecycle delivery:** provision one eligible unclaimed HolonSpace with its local semantic foundation; support human-initiated Local Sovereign Constitution through Client Security; establish PersonAgent and sovereign association using shared commitment/validation; Open/restart and perform supported Upgrade without replacing identities or repeating acquisition. Apply design v0.8 §§5–6 and 11–13. AS1 is merged via [PR #871](https://github.com/evomimic/map-holons/pull/871), merge `36a577c2fa5b6c78419897ecdfcca4e56b32b79b`, reviewed head `70de9d6f`; its fixtures do not establish acquisition guarantees.

#### AS2-owned implementation

1. Refactor the existing bootstrap/import lifecycle into explicit Provision/Open/Upgrade. Preserve existing TransactionContext, Reference Layer and transport binding paths. Recheck `core_schema_bootstrap.rs`, `space_imports.rs`, `ensure_core_schema_space()` and guest completion/index handling on the implementation baseline; do not create a competing bootstrap.
2. Provision one unclaimed ordinary HolonSpace with packaged local CoreSchema and Agent Spaces. Reconcile `MAP.CoreSchemaSpace` naming/key assumptions without replacing/retyping the space, duplicating content or requiring a descriptive-property rewrite. Display identity may be presentation-only.
3. Provide foundational Welcome and scoped definition imports. Request constitution authorization through the CS-L1 contract; do not implement credential issuance/custody or a capability framework in AS2.
4. Deliver the canonical HasInterior Lineage-binding schema delta, retaining definitional status and derived IsInteriorOf. Declare Home Space and historical continuity requirements using the approved shared mechanisms. General evaluators and binding-aware traversal are prerequisites, not AS2 implementations.
5. Orchestrate one complete constitution: stage PersonAgent in its intended Home Space, declared HasInterior and required authorization/completion effects using ordinary bound references and transaction APIs. Consume shared admission, validation and commitment results. Never separately commit an incomplete Agent or author the inverse independently.
6. Define the domain completion predicate and evidence-based lifecycle classification. Integrate shared conflict/interruption/retry outcomes without treating transport success, a marker or process readiness as completed sovereignty.
7. Integrate durable acquisition-privilege retirement and authorized runtime reconstruction through CS-L1 for its finite lifecycle operation inventory. All exposed privileged operations require appropriate authorization; unsupported paths remain unavailable or otherwise protected. Definitions may preexist, but general Dancer authorization and arbitrary delegation are later capabilities, not CS-L1 delivery requirements.
8. Implement valid-credential Open/restart and explicit supported Upgrade transitions. Preserve Agent/Space/content identity; reject unsupported or incompatible transitions safely. Do not claim an upgrade protocol from an initial import or no-op. No general migration framework or credential recovery is required.

There is no persistent Active sovereignty transition. Closed/Opening/Ready/Closing remains runtime state.

#### Explicit minimum dependencies

These labels identify bounded work, not newly created GitHub issues. Owners must link delivery issues and verified revisions before the corresponding path is enabled.

| Dependency | Owner and minimum handoff | Broader work outside the dependency |
| --- | --- | --- |
| CS-L1 | [Client Security plan v0.2](../security/map-client-security-impl-plan.md#minimum-operation-inventory): approved local trust contract, scoped constitution, credential custody, durable retirement, opening/restarting the same acquired AgentSpace and only the finite operations mapped to AS2-Local-Lifecycle, with security evidence for one supported configuration | General Dancer authorization, arbitrary delegation, WeSpace roles, universal policy engine, adaptive risk, rotation/revocation, credential recovery and TrustChannels |
| Local acquisition commitment | Shared transactions/persistence: demonstrated complete-write-set boundary, durable outcome, conflict revalidation and deterministic interruption/lost-response handling | New transaction subsystem, general journal or cross-cell coordination |
| Relevant relationship/constraint enforcement | Shared Commit validation: required endpoints/cardinalities/inverses, Home Space correspondence, both historical invariants and affected saved endpoints through reusable assessment | Unrelated constraint coverage or general dynamic rule loading |
| Lineage/reference behavior | Shared relationship/reference infrastructure: binding-aware comparisons, successor/inverse traversal and same-lineage accounting needed by the sovereign pair | General cache or version-adoption redesign |
| Required key composition | Shared key infrastructure, including #868 / DevDocs #87: compose/set and conformance for constitution types | Unrelated key features |
| Compatibility contracts | Each owner defines supported schema/evidence/security formats; AS2 integrates explicit transitions and rejection | General schema migration |

No missing prerequisite may be replaced by UI gating, an AS2-local validator, a bootstrap flag or incomplete persistence presented as successful acquisition. Completing every future security/transaction capability is not required.

#### Requirement ownership ledger

| Requirement group | Authoritative owner | AS2 integration |
| --- | --- | --- |
| Self-constitution, eligible unclaimed target, provisioning before Agent | Agent Spaces | Welcome and first-space flow |
| Agent/Space identity, contents, names and CoreSchema-hosting distinction | Agent Spaces | Preserve existing Space and content |
| Human/principal/author/executor distinctions | Agent Spaces semantic identities; Client Security execution authority | Pass resolved authority through lifecycle operations |
| Issuance, custody, trusted initiation, caller admission, scope and replay | Client Security | Consume CS-L1; supply domain operation/Space scope |
| Tauri/webview/native/conductor/zome enforcement | Client Security | Use supported ingress |
| Durable privilege retirement, operation/Dancer authority, restart credentials | Client Security architecture | Consume only the CS-L1 lifecycle inventory for AS2; defer general Dancer/delegation authorization without allowing unsupported privileged paths |
| Home Space, HasInterior, cardinality and historical sovereign continuity declarations | Agent Spaces | Declare and construct conforming domain state |
| General cardinality/inverse/history assessment and affected-endpoint scheduling | Shared validation/descriptors | Consume required enforcement |
| Binding normalization, source versions, inverse accounting and authoritative lookup | Shared relationships/references/persistence | Verify endpoint evolution and historical continuity |
| Key composition/conformance | Shared key infrastructure | Use for PersonAgent production |
| Required acquisition effects and completed-constitution predicate | Agent Spaces | Identify full domain effects and classify outcomes |
| Atomic persistence, concurrency, stale reads, caught failures and lost-response retry | Shared transactions/persistence | Consume approved complete outcome and recovery |
| Authorization evidence meaning / reliable storage / domain completion | Client Security / shared persistence / Agent Spaces respectively | Integrate without prescribing a record type |
| Provision/Open/Upgrade classification and supported transitions | Agent Spaces, consuming each owner's compatibility contract | Implement lifecycle outcomes |
| Mechanism-level tests and assurance | Corresponding shared owner | Selected real-lifecycle acceptance scenarios |

#### Acceptance and evidence

AS2 acceptance demonstrates one durable Space with local schemas; explicit human constitution through approved admission; PersonAgent Home Space and declared/derived association; independent Agent/Space version evolution; rejection of removal, replacement and conflicting acquirers; deterministic duplicate/interruption/lost-response outcomes; valid-credential restart without reload/reacquisition/bootstrap reopening; missing-credential denial; scoped imports with unauthorized Dancer denial; and supported Upgrade/incompatible-state handling. Include non-root references, affected saved endpoints and historically acquired Spaces with prospectively empty inverses.

Shared owners supply mechanism-level security tests, reusable validator tests and persistence fault/conflict evidence. AS2 repeats selected end-to-end scenarios through the real conductor and published contracts; it does not own every attack/fault test or certify the entire security roadmap. Required security assurance for the supported deployment cannot be waived. Map the finite CS-L1 operation inventory to actual AS2-Local-Lifecycle entrypoints and test identifiers before enabling them; shared versioning/validation tests do not implicitly expand it. Record exact dependency revisions, configuration and unverified guarantees.

Lifecycle discovery/classification, compatibility analysis, Space-identity preservation and Welcome presentation/request contracts can proceed independently. Acquisition and privileged execution remain disabled until their bounded dependencies are delivered. No second Space/DHT, remote CoreSchema, shared admission, general Declaration/Agreement implementation or recovery framework is required.

### AS3 — Persist Agent-owned personal Usages

Implement the integration relationship and context contract approved in AS0.
Persist the PersonAgent ownership association for the initial personal flow as part of admitting new personal state, preserving
Core home-space ownership and the shared Visualizer's independent identity.
Ensure the actual background persistence transaction retains the correct Agent
and authorized context, not merely the foreground transient object.

Make Agent-to-Usage traversal usable through the existing Reference Layer and
appropriate command/Dance boundary. Project only the records authorized for the
consumer. A public Visualizer or externally visible Persona must not become a
back door to private Agent configuration.

Update identity/key construction, preference references, specialization, and
configuration-copy behavior where needed to prevent collisions across Agents,
contexts, or explicit scopes. Implement the approved existing-record transition
and test it before enabling the new discovery path; keep unresolved records out
of another Agent's personal results.

**Exit evidence:** accepted personal configuration survives restart and is
retrievable from its owning PersonAgent. Two Agents using the same Visualizer and
subject type cannot see, overwrite, or inherit each other's configuration merely
because those inputs match. Declared and inverse ownership traverse correctly.
Persistence failure/retry preserves the current usable configuration and subject
transaction isolation. Default-only rendering produces no durable personal Usage.

### AS4 — Use Agent/context access in selection

Bulk-acquire relevant personal state through authorized Agent/context access and
construct a derived Rust index. Reuse it for compatible selections instead of
rediscovering all Usages from each Visualizer or subject ancestor. Scope keys
must reflect the approved personal policy, not every occurrence identity.

Honor DAHN precedence, explicit choices/pins, cross-cutting preferences,
composition-local overrides, subject applicability, Slot contracts, Theme,
runtime compatibility, and current authorization. Evaluate ancestry against
available metadata; an ownership index is not permission to ignore eligibility
or silently flatten distinct scopes. TypeScript consumes Rust-authorized results.

Specify validity and refresh triggers for personal edits, background-save
completion/failure, context/Agent changes, relevant schema or policy changes,
and Space Session reset. Retire derived state with its owning lifecycle. Cache
a successful absence only within that validity context; an error or incomplete
read must not become a personal-state miss. This increment does not invent a
cross-context registry for uncommitted personal state.

**Exit evidence:** repeat compatible requests reuse personal state without
per-slot ownership discovery; switching Agent/context cannot reuse another
Agent's results; committed changes and Session reset refresh the index. A
preferred date interactor applies across compatible compositions, a local
override stays local, and absence renders defaults without creating a Usage.
Ambiguity and unauthorized access remain visible errors rather than defaults.

### AS5 — Resume profiling and close the first milestone

Reconcile `codex/profile-visualizer-selection` with the implementation baseline;
retain useful selector/IPC spans and the summarizer without adopting unrelated
branch differences automatically. Record the exact tested revisions and data
transition before collecting a new baseline.

Compare the same application/data workload before and after AS4: fresh process,
repeat navigation within a Session, no-personalization startup, accepted personal
configuration, and an Agent/context switch. Separate first acquisition and index
construction from repeated applicability checks, metadata reads, candidate
discovery, realization, and background persistence.

Record usable-content time, selector requests, backend fetches, conductor calls,
personal-state loads/index reuse, and required Usage writes. Preserve correlation
IDs and raw logs with the summary. The branch's metadata-fetch counts describe
host-service calls, not SQL queries; nested inclusive spans must not be summed
as independent wall time.

**Exit evidence:** controlled before/after results establish whether personal
lookup duplication was removed and identify remaining costs. Default-only startup
has zero durable personal Usage creations; required personal saves do not gate
foreground usability. Report residual discovery/materialization costs explicitly.
No percentage improvement or absolute startup target is presumed.

### AS6 — Introduce multi-AgentSpace infrastructure

Treat multi-AgentSpace support as a separately estimated, designed, and reviewed infrastructure undertaking. Before implementation, resolve the design-spec deferred D9 gate in the authoritative design documentation (and any relevant CoreSchema, reference, Holochain, or TrustChannel specifications). Do not interpret compatibility accommodations from AS0–AS5 as proof that remote operations already work.

Implementation slices, to be separately scoped and ordered after design review:

1. Provision a second independent HolonSpace/AgentSpace context without changing the first space's identity, data, or stewardship. Establish the required DHT/cell lifecycle and durable installation registry or equivalent approved discovery mechanism.
2. Obtain and verify a trusted reference to the existing authoritative `MAP.CoreSchemaSpace` using approved bootstrap information. Resolve schema identity, compatible versions, and authentication without assuming a preexisting PersonAgent, Agreement, or TrustChannel.
3. Read and reference authorized remote CoreSchema descriptors through the approved reference layer. Preserve Home Space/version identity and use permitted immutable caching; do not load a second authoritative CoreSchema graph.
4. Add necessary inter-space transport, routing, request authorization, and failure handling through the appropriate owning runtime design. Do not bypass reference, validation, or projection boundaries.
5. Make PersonAgent onboarding, atomic creation/acquisition, runtime readiness, Provision/Open/Upgrade, and recovery repeatable for the second independent space without hardcoded founder IDs or development filesystem paths.
6. Verify isolation between distinct Agents and spaces, including personal Usages and configuration. Document what is and is not supported for multi-device Persona/key continuity; do not claim it implicitly.

**Exit evidence:** two independently provisioned spaces reopen with distinct identities and authoritative holons; the second accesses the existing CoreSchema without creating a competing authoritative copy; remote references and caches preserve identity/version; failures, unauthorized reads, and partial provisioning are handled under approved contracts; the first space's personal state remains isolated. Any capabilities not yet supplied (e.g., complete TrustChannel governance) are explicitly recorded as later gates.

### AS7 — Add Personas and shared We-Space participation

Implement the approved qualified Agent-side HasRoleIn participation contract, not ISpace BelongsTo. Preserve complementary I-Space/We-Space aspects, constituent membership and sovereignty as distinct concerns. Do not add aspect wrappers merely to represent these roles.

After AS6 supplies the necessary independent-space infrastructure and the corresponding design decisions are settled, provision contextual
Personas and We-Spaces through the same durable lifecycle. Keep the Agent's
private Persona mapping in its interior context; verify externally visible
identity does not imply universally traversable Agent identity. Decide key
lifecycle and Holochain identity mapping before binding them in runtime code.

Introduce contextual participation without conflating it with collective
membership. A venue can exist and accept guests without creating a collective
Agent or becoming an I-Space. Resolve We-Space personal/shared configuration
policy before extending AS4's index to those contexts. Specify the first shared
We-Space's invitation/admission behavior and its relationship to eventual
Agreement governance before implementation, following design §§2.4–2.5 and D11; the complementary We-Space aspect does not authorize an unenforced membership mechanism.

Reconcile reusable disclosure selections under design §7.3. Identity continuity does
not itself authorize access or transfer trust. Editing a reused disclosure policy
must not silently expand an existing Agreement's grant. Apply data-access limits
to returned values and derivations across retrieval paths, not only to invocation
permission or graph shape. Detailed TrustChannel endpoints and We-Space routing
remain separately gated design work.

**Exit evidence:** supported Persona reuse/separation and participation scenarios
preserve privacy and identity distinctions. No Persona, key, Role, or software
Agent automatically gains Agreement-party eligibility. Admission rejects
unsupported participation; disclosure-policy changes do not silently enlarge
previous grants or expose a participant's private identity graph.

### AS8 — Add governed collective and Agreement capabilities

Deliver the collective-emergence pathway from design §2.5: an existing We-Space can support organization before a sovereign collective exists; legitimately constitute, create and acquire the collective Agent in one transaction within that same space, preserving continuing shared participation. Verify Home Space correspondence, distinct membership/participation, and the collective Agent's participation in other We-Spaces. Do not introduce a mandatory Emergent state. No part of this later delivery becomes an AS0–AS5 prerequisite.

Deliver further vertical slices after positive accountable-party eligibility,
representation, delegation, and governance rules are settled. Candidate
AgreementParticipation and Role models remain design work until approved.
Model accountable party, representing Persona, executing software Agent, and
execution authority as distinct facts. Apply software-agent Agreement
restrictions at the relevant admission boundary, not merely in the UI.

Recognize collective Agents explicitly and give them distinct I-Spaces when
appropriate; do not infer either from a We-Space's existence. Integrate LifeCodes,
Agreements, TrustChannels, and Promise Weave incrementally as their contracts
mature. Full Promise Weave execution and cryptographic protocol implementation
are not gates for AS1–AS5.

**Exit evidence:** allowed and forbidden commitment/delegation cases are tested,
collective membership differs from venue participation, and records preserve who
executed an activity versus who undertook its commitment.

## Validation and delivery records

For schema increments, run the applicable schema compilation/check commands,
regeneration consistency checks, and descriptor-kernel tests. For shared runtime
changes, validate host consumers and the hApp WASM boundary. For loader,
provisioning, relationship persistence, and restart behavior, use real-conductor
integration scenarios in addition to unit tests. Consult the sweettest-framework
skill before authoring tests under `tests/sweetests/`.

Use focused SDK/UI tests for changed transport/projection behavior and selection
consumers; no UI dependency is required for Core-only verification. Complete the
repository's applicable checks for each implementation PR. This documentation
change does not claim any runtime checks or performance experiments were run.

For each delivered unit, append its actual status, issue/PR links when created,
verified revision, test evidence, transitional limitations, and remaining gates.
Keep design intent in the owning specifications; completion of an intermediate
unit does not silently narrow their target state.

## Milestone acceptance checklist

### AS0–AS2: first sovereign AgentSpace

- [ ] Plain HolonSpace operations remain usable without a PersonAgent/AgentSpace association.
- [ ] HolochainAgent initialization and CoreSchema provisioning do not require an existing MAP PersonAgent.
- [ ] The first personal HolonSpace retains identity/content through constitution; its display name is independent of CoreSchema hosting and current MAP.CoreSchemaSpace implementation assumptions are reconciled.
- [ ] Welcome/onboarding is available under constrained bootstrap authority without an independently authorized Dancer; explicit human initiation and backend authorization implement Local Sovereign Constitution without external identity recognition.
- [ ] PersonAgent identity is distinct from Holochain AgentPubKey and device identity; ordinary Person domain holons are not acquiring Agents.
- [ ] Creation/acquisition commits PersonAgent, Home Space, required interior relationship and authorization/completion evidence together, preserving the HolonSpace's identity/type.
- [ ] Commit rejects incomplete Agents, Home Space mismatch, invalid local inverse cardinality and ordinary removal/reassignment that violates the settled contract.
- [ ] Repeated, interrupted, or conflicting acquisition attempts cannot produce conflicting sovereign owners.
- [ ] Constitution issuance/custody, scope, trusted invocation and replay/conflict prevention are verified; acquisition-only privileges are durably retired and cannot bypass ordinary authorization after acquisition or restart.
- [ ] Closed/reopening runtime does not remove acquired sovereignty; no persistent Active state or reacquisition is introduced.
- [ ] Dancer definitions/packages can load before acquisition; exposed operational execution requires appropriate acquired authority and readiness. Unsupported privileged paths are denied; general Dancer/delegation authorization is not a CS-L1 milestone requirement.
- [ ] Provision, Open, and Upgrade are distinct; valid-credential restart reopens the same Agent, space, and saved holons without reprovisioning. Missing credentials fail closed; loss/compromise recovery is not claimed.
- [ ] No multi-AgentSpace infrastructure is required to pass the first milestone.

### AS3–AS5: Agent-owned DAHN state

- [ ] Personal VisualizerUsage is semantically owned by a PersonAgent independently of its Home Space and applicability scope.
- [ ] Two Agents cannot read, overwrite, or inherit each other's personal Usages merely by sharing Visualizer/subject identifiers.
- [ ] Personal Usage can be discovered through authorized Agent/context access, and its persistence survives restart.
- [ ] Default-only rendering creates no durable personal Usage; required background saves do not gate foreground usability.
- [ ] Derived selection state is invalidated correctly on context, policy, schema, and session changes.
- [ ] Profiling reports first-load and repeated-selection costs without assuming an arbitrary performance target.

### Future multi-AgentSpace acceptance (not AS0–AS5)

- [ ] A new independent HolonSpace can access an existing authoritative CoreSchemaSpace without creating another authoritative CoreSchema copy.
- [ ] Inter-space references and permitted caches preserve Home Space and version identity.
- [ ] Shared We-Space participation does not implicitly create a collective Agent or disclose private Persona mappings.

## Reconciliation and change-control record

- **Design authority:** `agent-spaces-design-spec.md` v0.6. This plan must not become a second source for ontology, lifecycle semantics, authorization rules, or acceptance policy. If a conflict appears, update the design specification first and then align the affected implementation step.
- **Delivery changes:** former AS2b is folded into AS6; former AS6/AS7 become AS7/AS8; AS1 no longer creates an AgentSpace/ISpace/WeSpace type hierarchy; AS2 explicitly separates unclaimed provisioning, PersonAgent establishment, atomic creation/acquisition, runtime readiness, and restart; AS6 is a separately scoped multi-space undertaking.
- **Retained detail:** repository baseline, direct schema dependencies and inverse handling, DAHN Usage persistence/indexing, migration safeguards, profiling instrumentation, integration-test expectations, and evidence tracking remain part of this implementation plan.
- **Earlier reconciliation (2026-11-11):** settled cardinality and Home Space correspondence, atomic create/acquire, sovereignty without persistent Active, complementary space aspects and Dancer definition/operation distinction follow design v0.5. Milestone checklists formerly in the design spec are maintained above; AS0–AS8 dependencies and downstream profiling/migration details are retained.
- **Status:** AS1 is delivered as recorded below; AS2 and later units remain planned. Older repository observations and verification entries are dated historical checkpoints, not current completion claims.

## AS1 readiness record — 2026-11-12

The AS1-relevant AS0 semantic choices are approved in design v0.5. General relationship rules are not open Agent Spaces design questions. Home Space correspondence enforcement and the cross-version sovereign-replacement mechanism are explicitly AS2 gates. AS1 schema delivery may use authored target-compatible keys while #868/shared composition is pending. Non-Dancer packaging and repeat-import behavior remain bounded implementation checks; current create-import rejection must not be reported as identical-version identity reuse.

Read-only grounding at map-holons c9ae0ad2: 25 effective-relationship discovery unit tests and 9 key-uniqueness unit tests passed during this reconciliation. They establish discovery/lineage-key behaviors, not complete Capability 4 enforcement, authorized acquisition or restart guarantees. No conductor integration suite or AS1 implementation was run. Relationship checks follow the existing Commit Validation Implementation Plan Capability 4; shared template implementation belongs to #868 and its dependencies. Pairwise holon-deletion semantics remain outside this increment.

## AS1 implementation evidence — 2026-11-12 (historical pre-merge checkpoint)

**Status:** local implementation on `860-agent-spaces-as1-load-the-agent-spaces-schema-including-as0-delivery-contract`, based on map-holons `2457f77e`; code changes are not yet committed/merged. This record does not close AS1 or claim conductor acceptance. DevDocs PR #93 remains open.

Implemented surfaces:

- Canonical `schema-src/agent-spaces/schema.tdl` and package manifest, generated JSON and matching Conductora resources. Agent/BioSocialAgent/PersonAgent lineage, optional/required name properties, the target optional-component template and approved directional relationship policies are authored without changing Core or Dancer.
- The configured import set moves from the House Troupe directory to `resources/space-imports.json`, selecting the ordinary Agent Spaces package before Space Navigator. The existing import path and transaction loader are reused; a rejected/incomplete load response is not treated as success.
- Build/resource synchronization and focused schema/package regression tests are wired into existing npm commands.
- `tests/sweetests/tests/agent_spaces_tests.rs` adds an isolated ordinary-conductor scenario for unclaimed-space preservation, configured-rule shape, repeat-create rejection/identity preservation, missing-LastName rejection/correction, optional-name absence, fresh persisted forward/inverse traversal and name updates within one Agent lineage. Keys are explicit fixtures; this is not a custom composer or acquisition flow.

Verified:

| Check | Result |
| --- | --- |
| TDL check over schema-src | Passed; no diagnostics |
| Generated imports and JSON/TDL round trip | Passed |
| map-schema library tests | 58 passed |
| Schema inventory and Agent Spaces package tests | 8 + 3 passed |
| Conductora native cargo check | Passed with installed complete Rust 1.95 |
| hApp production WASM build | Passed with installed complete Rust 1.94 |
| Repacked DNA/hApp surface audit | Passed with hc 0.7.1; no production test-only exports |
| Focused agent_spaces_tests compilation | Passed with Rust 1.95 |
| Focused agent_spaces_tests execution | Blocked at conductor startup before Core bootstrap: iroh netmon initialization returned Operation not permitted |
| Formatting / diff whitespace | Passed |

The runtime failure is a managed-environment restriction, not a successful schema test or a demonstrated schema rejection. Execute the preserved integration test in CI or a permitted development environment before claiming package loading, required-property correction, persisted traversal or repeat-import runtime acceptance. Do not bypass the monitor by changing production transport.

Pending ownership remains unchanged: #868/#87 supply shared synthesis and mismatch enforcement; Capability 4 supplies complete relationship conformance; AS2 supplies Home Space correspondence enforcement, the cross-version sovereign-replacement restriction and real constitution/acquisition. Pairwise holon-deletion execution and loader upgrade/reconciliation remain separately owned. No onboarding, authorization or second-space implementation is included.

## AS1 merged delivery and AS2 handoff — 2026-11-13

**AS1 delivered:** Issue [#860](https://github.com/evomimic/map-holons/issues/860) closed with [PR #871](https://github.com/evomimic/map-holons/pull/871), merged as `36a577c2fa5b6c78419897ecdfcca4e56b32b79b` (reviewed head `70de9d6f0781d4060456b042621b5e4a8b8c39e1`). DevDocs PR #93 remains the documentation branch; its open state does not mean AS1 code is unmerged.

- The delivered configured import set names generated JSON paths directly under `resources`, loading Agent Spaces before Space Navigator. Package manifests are not part of the delivered loader/catalog contract. Canonical TDL and generated resources remain the source pipeline.
- CI run [43480997948](https://github.com/evomimic/map-holons/actions/runs/43480997948) passed on that head: light, heavy storage/commit/rest, formatting and aggregate gate. The isolated `agent_schema_preserves_space_and_name_versions_and_rejects_reimport` test passed in heavy rest (about 367 seconds). This supersedes the local netmon-blocked execution entry above and supplies schema-load, required-name correction, optional-name absence, repeat-create rejection, fresh traversal and Agent-lineage evolution evidence.
- The result-rendering follow-up restores ordinary selection/composition of the actual Load Holons response through HolonInspector. The maintainer confirmed it live. Reported hApp/host builds, `npm test` and `npm start` were nominal. Focused frontend verification: 497 tests passed, one skipped, plus typecheck; schema checks: 58 library + 8 inventory + 3 package tests, generated comparison and round trip passed.
- These results establish AS1's bounded schema/import behavior. Explicit fixture keys do not prove shared key synthesis. Version/Lineage sovereign binding was delivered; the v0.6 Lineage/Lineage target is AS2 work. Neither Space-version evolution nor historical association enforcement, acquisition authority, physical acquisition atomicity or restart recovery is established by this evidence.
- Shared Capability 4/key prerequisites and the Home Space/historical-continuity gates remain. No onboarding, second space, remote schema access or personalization implementation is claimed.

**AS2 resolution order:** resolve CS-L1 in Client Security and bounded commitment/history gaps in their shared owners; link dependency delivery and evidence; implement the lifecycle and schema integration; verify selected end-to-end acquisition/evolution/recovery scenarios. D2 sovereignty remains resolved. Optional presentation naming is independent.

## D2 architectural authority resolution — 2026-11-13

Local Sovereign Constitution is approved as the intended production model. This corrects the earlier non-production-local-rule versus production-proof framing; no external identity authority is required. The initial implementation uses constrained local authorization, subject to demonstrated security guarantees rather than a replacement sovereignty model.

Lifecycle discovery/classification, compatibility work, space-identity preservation, Welcome presentation/request contracts and shared relationship enforcement can proceed without enabling acquisition. Usable constitution credential issuance, acquisition, post-acquisition privileged execution and authorized restart remain gated on their security contracts and the relevant D1/D4/D6 prerequisites. Production readiness is an assurance conclusion, not implied by this architectural decision. Complete credential recovery, external proofing and general Declaration/Agreement infrastructure remain outside AS2.

## Scope reconciliation — 2026-11-14

AS2 owns AgentSpace behavior and integration. Client Security owns shared authorization/assurance; transaction, relationship, key and validation mechanisms remain separately delivered dependencies. The ownership ledger and minimum dependency table above replace accumulating general mechanism design in the lifecycle issue. Constitutive evidence representation is still open and no dedicated record type is approved.
