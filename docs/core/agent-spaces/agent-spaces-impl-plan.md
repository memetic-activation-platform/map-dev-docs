# Agent Spaces Implementation Plan

## Status and intended outcome

**Version:** 0.2 (reconciled implementation plan)  
**Date:** 2026-11-10  
**Status:** Planned; no increment below is claimed implemented.

Implement the target architecture defined exclusively by [Agent Spaces design specification](agent-spaces-design-spec.md) v0.2 through reviewable increments. The initial delivery establishes a durable first HolonSpace/CoreSchemaSpace, an established Person identity, sovereign acquisition and activation, and Agent-owned VisualizerUsages used by DAHN selection. The first AgentSpace must reopen without reprovisioning. Multi-AgentSpace infrastructure is anticipated in early interfaces but **not implemented or required through AS5**; it is a separate AS6 undertaking. Personas, shared We-Spaces, and governed collectives follow in AS7–AS8.

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

The older [AgentSpace architecture](agent-space-arch.md) says every AgentSpace is
an agentic social organism. The new specification explicitly separates Agent
from AgentSpace and says a We-Space does not automatically constitute an Agent.
Use the new specification for this work; AS0 must reconcile the older wording
rather than importing that conflicting assumption into schema or provisioning.

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
2. Introduce Agent/Person and the approved sovereign **relationship**, not AgentSpace, ISpace, or WeSpace HolonType specializations. Avoid in-place type rewrites during acquisition.
3. Keep Home Space, semantic Agent ownership, and applicable Usage scope distinct. Preserve Core `OwnedBy`/`Owns` semantics.
4. Use ordinary bound references, TransactionContext/Commit, ingress binding, and egress projection; no direct-storage shortcuts.
5. Preserve acyclic packages and direct descriptor dependencies. Do not make Core depend on Agent Spaces or DAHN.
6. Resolve principal, Holochain author, executor, and active space explicitly; do not infer Person from public key, host process, account, Persona, or caller-supplied ID.
7. Keep the bootstrap authority constrained and enforce the transition to sovereign/delegated authorization at trusted boundaries. A development-only initial acquisition path must be labeled and tested as such.
8. Default-only rendering creates no durable personal Usage; background saves must not block foreground usability.
9. Dancers require an affording acquired AgentSpace and delegated authority; adding one does not provision another hApp or DHT.
10. Keep single-home schema stewardship and immutable reference/cache identity explicit, without implementing remote CoreSchema resolution in AS0–AS5.
11. **Do not add multi-AgentSpace provisioning, cross-DHT discovery, remote schema reads, TrustChannels, or shared-space admission to AS0–AS5.** Representing multiple Agents as holons is not multi-AgentSpace operation.

## Sequence and usable milestones

| Unit | Depends on | Reviewable outcome |
| --- | --- | --- |
| AS0 — Resolve first delivery contracts | None | Owning design-spec gates D1–D8 resolved for the affected increments; schema/package and migration contracts reviewed |
| AS1 — Load minimal Agent/Person schema | AS0 decisions needed for AS1 | Minimal non-Core Agent/Person descriptors and sovereign relationship contracts load; plain HolonSpace remains usable |
| AS2 — First sovereign AgentSpace | AS1, applicable AS0 decisions | Initial CoreSchemaSpace provisioned, Person identity established, space acquired/activated; Provision/Open/Upgrade and restart verified |
| AS3 — Persist Agent-owned personal Usages | AS2, Usage design gates | Personal configuration stored and retrievable through authorized Agent/context access |
| AS4 — Agent/context selection | AS3 | Rust selection reuses correctly scoped personal-state index; defaults remain write-free |
| AS5 — Profile and close first milestone | AS4 | Measured selection costs, correct ownership and restart behavior; no multi-space prerequisite |
| AS6 — Multi-AgentSpace infrastructure | AS5 for this delivery sequence; separate infrastructure design gates | Independent spaces, remote authoritative CoreSchema access, reference resolution and required communication; repeat personal provisioning |
| AS7 — Personas and shared We-Space participation | AS6 where cross-space interaction required; identity/admission design gates | Contextual identities and shared interaction without implicit collective identity |
| AS8 — Governed collective and Agreement capabilities | AS7 and governance/eligibility design gates | Accountable participation, collective sovereignty, and delegated execution |

AS1–AS2 deliver the first durable sovereign AgentSpace. AS3–AS5 deliver Agent-owned personalization and selection performance. The former AS2b is retired as a separate pre-AS5 gate; second independent AgentSpace provisioning is verified in AS6. A narrower test representing multiple Agent holons in the first space is allowed but does not count as multi-space support. Unit identifiers are delivery labels, not runtime types. Split units into independently reviewable PRs; create issues once the relevant design gates have been resolved.

### AS0 — Resolve the first delivery contracts

Review design-spec §§2–3, 5–10, and 13 against canonical TDL and the current repository. Record approved decisions in the **design specification or its owning domain specifications**, not here. AS0 work should settle the subset required for AS1–AS2, and the Agent/Usage contract before AS3–AS4; later gates may remain open.

- Confirm the exact minimal Agent and Person descriptors, source/target contracts and inverse for the sovereign BioSocialAgent–HolonSpace association (design gate D1). Check uniqueness, validation timing, and deletion/transfer constraints without minting AgentSpace/ISpace/WeSpace types.
- Confirm how the initial `MAP.CoreSchemaSpace` is provisioned and later acquired **without replacing its HolonType or identity**; document how ordinary HolonSpace APIs remain valid (D5–D6).
- Resolve initial identity establishment, Welcome bootstrap, acquisition authorization, concurrent attempts, idempotency, failure recovery, and transition to ordinary authority (D2–D4). Mark any constrained local development authorization as non-production.
- Specify durable lifecycle/completion evidence and how Provision, Open, and Upgrade recognize compatible state without replaying schema loads or initial acceptance (D4/D6).
- Specify principal/author/executor resolution and trusted authorization enforcement, without inferring Person from an AgentPubKey or a supplied ID (D3).
- Set schema package ownership, direct dependencies, and relationship inverse declarations. Compare current `OwnedBy`/`Owns` contracts before introducing semantic Agent ownership.
- Approve the Agent–VisualizerUsage ownership, inverse, scope, keys, home placement, reassignment/deletion, and existing-record transition (D7). Evaluate an Agent Spaces–DAHN integration package against a one-way dependency; avoid dependency cycles.
- Reconcile DAHN owner-directed composition, selection precedence, ValueType preferences, background persistence, and derived-index invalidation in its owning design (D8).
- Identify superseded AgentSpace inheritance and social-organism assumptions in dependent documentation; update their design owners rather than copying new normative design into this plan.
- Record multi-space compatibility review (distinct identities, Home Space, explicit context, local CoreSchema stewardship), but do **not** design or implement AS6 protocols as a condition of AS0 exit.

**Exit evidence:** approved first-delivery design contracts and documented deferred gates; package and migration approach reviewed; no multi-space implementation dependency introduced.

### AS1 — Load the minimal Agent Spaces schema

Introduce the approved minimal non-Core Agent/Person descriptors and sovereign relationship contracts in `schema-src/` using the repository's schema tooling. Do **not** create the superseded `AgentSpace extends HolonSpace`, `ISpace extends AgentSpace`, or `WeSpace extends AgentSpace` hierarchy. Defer Persona, AgreementParticipation, Roles, collective governance, and We-Space participation schema unless a settled prerequisite requires them.

Use explicit describing types and valid single `extends` declarations **only for actual types**. Keep both relationship descriptor sides in the appropriate owning package; license declared sides in instance contracts and author direct occurrences on their declared source. Commit materializes inverse occurrences; neither loader nor runtime readers should invent them. Regenerate JSON/import manifests and packaged resources using repository tooling; do not manually edit generated JSON.

**Exit evidence:** schema compilation and kernel validation accept the minimal descriptors and association; imports resolve via direct dependencies; repeated import behavior is established; plain HolonSpace scenarios still work; committed forward and inverse traversals agree. No new AgentSpace/ISpace/WeSpace HolonTypes appear.

### AS2 — Provision, acquire, activate, open, and upgrade the first AgentSpace

Implement the approved first-space path through existing host orchestration, CoreSchema bootstrap, loader, space management, and transaction surfaces. Recheck `host/conductora/src/setup/core_schema_bootstrap.rs`, `setup/space_imports.rs`, `ensure_core_schema_space()`, `enable_bootstrap_provisioning()`, `complete_core_schema_bootstrap()`, `CoreSchemaBootstrapGate::ensure_ready()`, and guest bootstrap guards against the current branch. Preserve/refactor the existing machinery rather than building a parallel bootstrap.

Delivery sequence:

1. Initialize HolochainAgent/conductor execution and enter explicitly constrained CoreSchema bootstrap.
2. Provision and durably complete the first HolonSpace, `MAP.CoreSchemaSpace`, using the packaged CoreSchema. Do not provision a second space for the first Person.
3. Make the operational **Unclaimed** HolonSpace available with a foundational Welcome/onboarding path, **not** a Dancer.
4. Establish or resolve the existing Person's MAP identity separately from the Holochain author and device. Use only the acquisition authorization mechanism approved in the design specification; document development-only limitations.
5. Acquire the same HolonSpace through the approved sovereign association and persist the authorization/lifecycle transition. Reject duplicate or conflicting acquisition and handle interrupted commits deterministically.
6. Activate ordinary sovereign execution, disable acquisition-only authority, and permit authorized Dancers. Verify principal/author/executor provenance at the trusted boundary.
7. Prove that the space, Person, association, saved holons, and lifecycle can be reopened and upgraded without reprovisioning.

Implement the three installation operations independently:

| Operation | Delivery work |
| --- | --- |
| Provision | Persist installation/space identity, initial CoreSchema content, readiness, and completion evidence; support incomplete-state recovery. |
| Open | Find completed state, rebuild runtime/index/cache, validate compatibility, and reuse existing Agent/space/holons without initial loading or acceptance. |
| Upgrade | Apply explicit versioned changes with documented failure, retry, and compatibility behavior. |

Use ordinary TransactionContext/Commit and reference binding; read back durable relationship and expected types before declaring acquisition/activation complete. Do not equate partial schema presence, an in-memory ID, or a successful transport response with readiness. Test concurrent provisioning/acquisition attempts and interrupted phases. A normal Open must not reactivate bootstrap privileges. Keep ordinary HolonSpace-only operation independent of social readiness.

**Exit evidence:** first launch yields one operational CoreSchemaSpace, then one acquired and active Person interior with persistent saved holons; Welcome is available before acquisition without a Dancer; Holochain author differs conceptually from sovereign principal; restart reopens identical space/Agent/holons without reload; retries are idempotent or fail explicitly; conflicting acquisitions are rejected; unauthorized or ambiguous contexts cannot resolve personal state; upgrades and failure recovery follow the approved contract. No remote CoreSchema, second DHT, shared We-Space, or TrustChannel is required.

### AS3 — Persist Agent-owned personal Usages

Implement the integration relationship and context contract approved in AS0.
Persist the Agent association as part of admitting new personal state, preserving
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
retrievable from its owning Agent. Two Agents using the same Visualizer and
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
2. Obtain and verify a trusted reference to the existing authoritative `MAP.CoreSchemaSpace` using approved bootstrap information. Resolve schema identity, compatible versions, and authentication without assuming a preexisting Person, Agreement, or TrustChannel.
3. Read and reference authorized remote CoreSchema descriptors through the approved reference layer. Preserve Home Space/version identity and use permitted immutable caching; do not load a second authoritative CoreSchema graph.
4. Add necessary inter-space transport, routing, request authorization, and failure handling through the appropriate owning runtime design. Do not bypass reference, validation, or projection boundaries.
5. Make Person onboarding, acquisition, activation, Provision/Open/Upgrade, and recovery repeatable for the second independent space without hardcoded founder IDs or development filesystem paths.
6. Verify isolation between distinct Agents and spaces, including personal Usages and configuration. Document what is and is not supported for multi-device Persona/key continuity; do not claim it implicitly.

**Exit evidence:** two independently provisioned spaces reopen with distinct identities and authoritative holons; the second accesses the existing CoreSchema without creating a competing authoritative copy; remote references and caches preserve identity/version; failures, unauthorized reads, and partial provisioning are handled under approved contracts; the first space's personal state remains isolated. Any capabilities not yet supplied (e.g., complete TrustChannel governance) are explicitly recorded as later gates.

### AS7 — Add Personas and shared We-Space participation

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
Agreement governance before implementation; §11.3 does not approve an unenforced
membership mechanism.

Reconcile any reusable disclosure selections under §9. Identity continuity does
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

## Reconciliation and change-control record

- **Design authority:** `agent-spaces-design-spec.md` v0.2. This plan must not become a second source for ontology, lifecycle semantics, authorization rules, or acceptance policy. If a conflict appears, update the design specification first and then align the affected implementation step.
- **Delivery changes:** former AS2b is folded into AS6; former AS6/AS7 become AS7/AS8; AS1 no longer creates an AgentSpace/ISpace/WeSpace type hierarchy; AS2 explicitly separates unclaimed provisioning, Person establishment, acquisition, activation, and restart; AS6 is a separately scoped multi-space undertaking.
- **Retained detail:** repository baseline, direct schema dependencies and inverse handling, DAHN Usage persistence/indexing, migration safeguards, profiling instrumentation, integration-test expectations, and evidence tracking remain part of this implementation plan.
- **Status:** planning reconciliation only. Repository observations and branch revisions above are historical inspection checkpoints, not freshly verified implementation facts.
