# Agent Spaces Implementation Plan

## Status and intended outcome

**Version:** 0.16 (supported first-space choices; Upgrade deferred)

**Date:** 2026-11-25

**Status:** AS1 merged and verified; AS2-P has bounded foundation evidence, and PR #880 adds constitution/Open engineering integration. Complete constitution and authorized acquired-space Open retain their shared validation and Client Security handoffs. AS2 now covers the supported first-space lifecycle and currently valid choices; Upgrade, DHT migration and rehabilitation are separate future design work, not AS2 completion gates. See the dated delivery records below.

Implement the target architecture defined exclusively by [Agent Spaces design specification](agent-spaces-design-spec.md) v0.12 through reviewable increments. The initial delivery establishes a durable first personal HolonSpace hosting local CoreSchema, an established PersonAgent identity, atomic PersonAgent creation/acquisition and authorized runtime opening, and Agent-owned VisualizerUsages used by DAHN selection. The first AgentSpace must reopen without reprovisioning. Multi-AgentSpace infrastructure is anticipated in early interfaces but **not implemented or required through AS5**; it is a separate AS6 undertaking. Personas, shared We-Spaces, and governed collectives follow in AS7–AS8.

**Document boundary:** The design specification alone defines target semantics, invariants, and unresolved design gates. This implementation plan contains only delivery sequence, dependencies, repository touchpoints, implementation tasks, migration steps, and verification evidence. Where a design gate remains open, the step is to resolve it **in the design specification first**, then implement it; this plan does not settle it by implication. Candidate names below are references to design-spec proposals, not approvals.

## Scope and delivery reconciliation — 2026-11-25

[#870](https://github.com/evomimic/map-holons/issues/870) now scopes AS2 to supported first-space provisioning, constitution and compatible Open. Upgrade/rehabilitation are deferred under design §6.7/D14. This supersedes the older AS2-U sequence and Upgrade checklist requirements, while preserving constitution, sovereignty and authorized-Open guarantees and their shared handoffs.

[PR #880](https://github.com/evomimic/map-holons/pull/880), reviewed head `0e26cd97`, merged as `4c24ab5ccf85fc77fc2a8d895879853cfe96b8c2`, extends existing constitution and packaged Navigator mechanisms: root packaged startup, named Space-successor continuity, broader real-conductor restart evidence and explicit separate-environment selection on incompatibility. Its engineering profile is not complete CS-L1 or historical-sovereignty acceptance. The issue records source/test evidence and the outstanding name-key/package-policy reconciliation; those policies are not changed by this scope update. Older dated observations below remain historical checkpoints rather than current completion claims.

Validation enhancements belong to Rashaan's [Commit Validation implementation plan](../validation/commit-validation-impl-plan.md). Client Security owns #872 and its security handoffs. Agent Spaces consumes those outputs. Baselined Complete/Rejected/Incomplete, partial persistence, retained identities/work and supported remediation/resubmission are unchanged; this plan adds no shared validator, rollback or transaction redesign.

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

## HolonSpace wrapper alignment

The legacy receptor discovery/routing DTO is named `DeprecatedHolonSpace` in
Rust and TypeScript. This is a source-level rename: its serialized fields,
legacy command registrations and discovery behavior remain unchanged.

The [HolonSpace wrapper design](../architecture/holon-layered-representation-design-spec.md#holonspace-domain-wrapper)
remains provisional. HolonSpace and possible I-Space/We-Space aspect wrappers,
including their APIs and responsibility boundaries, require further design
before implementation. The rename implements none of those wrappers and does
not change Commit remediation/resubmission semantics. Retirement
of obsolete receptor discovery APIs is separate work, not part of this rename
or a prerequisite for documenting the wrapper.

## Constitution implementation boundaries

The current refactor separates Agent Spaces behavior from the Tauri container:

- `shared_crates/holons_core/src/agent_spaces.rs` owns fresh sovereign-membership
  observation and PersonAgent staging through bound references. These are domain
  operations, not HolonSpace or aspect wrapper implementations.
- `shared_crates/type_system/type_names/src/agent_space_names.rs` owns typed names
  for the separately packaged Agent Spaces schema. Descriptor lookup for creation
  uses that vocabulary; no schema package/version literal is used as a status gate.
- `host/crates/map_commands_runtime/src/personal_constitution.rs` owns the short
  observation transaction and constitution transaction orchestration, including
  ordinary Commit outcomes and retention for remediation/resubmission.
- Conductora owns packaged Welcome ingress, window/origin enforcement, presentation
  state and wire projection. Its `welcome_lifecycle.rs` maps observations to display
  state and assurance blockers; it does not perform domain reads or mutations.

Status observations reuse adopted Space identity and read sovereign membership
fresh. They do not separately look up and discard the Agent Spaces schema root
or PersonAgent descriptor. Provision and compatible Open retain their compatibility
responsibilities; PersonAgent creation resolves its descriptor when needed. Upgrade
and incompatible-Space rehabilitation are separate future design work.
Membership classification preserves the existing zero/one/ambiguous behavior;
this refactor does not add historical lineage enforcement or new acquisition
arbitration. The shared operations can later be exposed by domain wrappers once
that design is resolved. The legacy APIs and current persistent store are unchanged.

## Local packaged coordinator maintenance

The explicit local engineering command
`npm run welcome:start -w map-host -- --upgrade-coordinators` updates only the
coordinator code of an already installed packaged application, through the
native Holochain administration boundary. It is limited to the packaged debug
`local-constitution` profile, accepts no caller-selected application, cell or
package path, and opens no administration or application WebSocket. Ordinary
Welcome launches continue to verify the installed package and refuse silent
coordinator replacement.

The operation checks the existing role, DNA, author, integrity definitions,
coordinator names and dependencies before updating changed coordinator WASM.
It verifies the installed definition and cell/author identities afterward;
reapplying the same code is a no-op. It does not reinstall the hApp, replace the
Space, recreate the PersonAgent, replay imports, rotate credentials or modify
ordinary Commit outcomes. An interrupted attempt is reconciled by inspecting
the installed definition and explicitly retrying the same approved package.
This is coordinator-code maintenance, not delivery of general schema migration,
credential recovery or a supported semantic Agent Spaces Upgrade. That broader capability is future design work outside AS2.

`npm run welcome:build -w map-host` builds the hApp and packaged Welcome bundle;
`npm run welcome:start -w map-host` launches that existing bundle without rebuilding.
PR #880 changed root `npm start` to build and launch the packaged Welcome flow. The earlier development-mode/root-entrypoint distinction is historical; ordinary host Cargo builds still do not refresh the packaged macOS app bundle. Reusing a retained compatible environment is Open evidence, not incompatible-Space recovery.

## Local Welcome-to-Navigator handoff

The packaged debug `local-constitution` flow starts with Welcome on every launch.
After an ordinary Complete constitution and a fresh saved-association read, or
a successful Open of an already acquired Space, Welcome requests the native
`open_space_navigator` handoff once. This request accepts no Agent or Space IDs.
Pending or retained constitution transactions prevent handoff and remain available
for ordinary remediation/resubmission. A handoff failure leaves Welcome available
with a Navigator retry action, never a repeated constitution request.

The host runtime's `application_launch` service reuses the adopted Space and the
existing RuntimeSession, obtains its saved sovereign Agent through the shared
relationship operation, and runs the existing Canvas/home-Dancer selection.
It passes that Agent to the selector and projects the selected identities into
the runtime-only application session. It neither provisions a second Space,
replays imports, creates another PersonAgent nor restarts the conductor. The
same selector is used by development startup; no parallel Navigator UI or
selection policy is introduced.

Conductora creates the packaged Navigator window only after that selection
succeeds, then closes Welcome. The Navigator consumes the existing application
session and MAP Commands runtime. Its separate capability grants session reads,
command dispatch, native source selection, window sizing and read-only access
to the packaged import-schema file; it grants neither
constitution commands nor conductor administration. Backend admission also
checks the exact packaged Navigator origin/window and the backend-established
acquired local session. Welcome retains only status, constitution and handoff
permissions. The native-only conductor remains without external app/admin
listeners. The packaged Angular production build keeps script/style minification
but disables critical-CSS inlining: its generated inline stylesheet-load handler
is incompatible with the packaged script CSP and can leave the Canvas display
at zero height. Blocking external CSS avoids that handler without weakening CSP. This local engineering handoff does not claim completion of Client
Security's production authorization/delegation assurance work or generalized
multi-space runtime selection.

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
| AS2 — First sovereign AgentSpace | AS1, applicable AS0 decisions | Initial personal HolonSpace with local CoreSchema, PersonAgent constituted with its interior, runtime ready; Provision/constitution/compatible Open and restart verified; valid choices reflect current compatibility and authority |
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
- Verify acquisition integration with the existing Commit, relationship-persistence and zome-call boundaries. Preserve Complete/Rejected/Incomplete outcomes, partial-result diagnostics, remediation and resubmission. Document conflict handling and recovery without introducing an all-or-nothing rollback prerequisite. A shared transaction ID or transport success is not sufficient evidence.
- Inspect the existing bootstrap/import path to distinguish loadable Dancer definitions/packages from operational Dancer execution; preserve pre-acquisition imports while gating operation at trusted boundaries.
- Resolve D7/D8 before AS3/AS4: Agent-owned Usage direction/inverse, key isolation, scope, Home Space, migration, background authority and derived-index validity. Evaluate a separate Agent Spaces–DAHN integration package versus one-way dependency without cycles.
- Reconcile older organism, AgentSpace subtype, I-Space participation and exclusivity wording in its owning documents. Use PersonAgent for the sovereign personal Agent; do not require an ordinary Person record.
- Review compatibility for future spaces without designing or implementing AS6 transport/discovery/reference protocols.

**Exit evidence:** the schema-affecting subset is approved for AS1; D2's authority model is approved; implementation-security, lifecycle and atomicity contracts are approved before enabling the corresponding privileged paths; later gates remain named. Settled decisions stay in the design specification and no multi-space dependency is introduced.

### AS1 — Load the minimal Agent Spaces schema

**Design-ready scope:** implement the approved schema/package, not onboarding or shared key/relationship infrastructure. See design §§2.2.2–2.3 and the explicit transitional dependencies below.

- Author `schema-src/agent-spaces/schema.tdl` for **MAP Agent Spaces Schema v0.1.0**, directly dependent on CoreSchema only. Use abstract Agent, abstract BioSocialAgent and concrete PersonAgent with single inheritance and existing MetaHolonType conventions. No new TypeKind anchor, ordinary Person type, complete taxonomy, Dancer reparenting or AgentSpace/ISpace/WeSpace types.
- License optional FirstName/MiddleName and required LastName on PersonAgent. The current NoneRule decision supersedes the original configured name FormatRule for instance keys. Do not introduce extra Agent/BioSocialAgent scalar properties.
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

#### Historical AS1 key authoring — superseded for current PersonAgent instances

**Historical delivery contract, superseded by the approved 2026-11-16 NoneRule decision.** The following records the merged AS1 approach and is not a current implementation gate. The former design-spec §2.2.2 contract was `LastName.FirstName.MiddleName`, with parameters `[LastName, FirstName, MiddleName]` and target template `{0}.[1].[2]`. [map-holons #868](https://github.com/evomimic/map-holons/issues/868) owns the shared positional-template capability and optional components; [map-dev-docs #87](https://github.com/memetic-activation-platform/map-dev-docs/issues/87) and the Commit Validation Implementation Plan own the remaining shared composition, producer and enforcement contracts. Those implementations are queued behind validation work. AS1 MUST NOT duplicate them or silently treat them as delivered.

**Interim path for schema work.** Author the target configured rule in canonical TDL and use explicit, precomputed `Key` values in AS1 schema-level fixture/loader inputs. This uses the existing authored-key path; it is not a substitute runtime KeyRule, custom renderer, or product onboarding API. Preserve optional property absence in the subject data. For example:

| LastName | FirstName | MiddleName | Explicit interim Key |
| --- | --- | --- | --- |
| Smith | Jane | Marie | `Smith.Jane.Marie` |
| Smith | Jane | absent | `Smith.Jane.` |
| Smith | absent | absent | `Smith..` |

Do not populate missing optional names with empty-string defaults, require those properties, switch to LastName-only/UUID/NoneRule, or introduce a second key-producing algorithm. Fixtures should state expected keys directly. Keys remain explicit state, subject to all currently active property, key-shape and uniqueness validation; no rule or validation failure may be bypassed to make this path work.

**Evidence and compatibility gate.** Recheck the implementation baseline when AS1 starts. Demonstrate that the current schema compiler, loader and active validator accept the target rule declaration and explicit-key fixtures through ordinary paths. Report separately (a) descriptor/package loading and relationship/name-property behavior demonstrated now, and (b) target synthesis, compose-and-set, and stored-key mismatch rejection awaiting shared infrastructure. Explicit-key fixture success does not prove automatic synthesis or enforcement. If newly active validation requires an unavailable renderer, or the target declaration cannot pass the ordinary path, the affected AS1 slice is blocked on the owning dependency; do not weaken the target schema or disable validation. Record any deferred key acceptance evidence in the AS1 delivery record rather than claiming the complete target key capability is verified.

**Removal of the workaround.** Once #868 and the applicable shared composition/producer/Commit-validation increments land, use their ordinary compose-and-set path in producers and exercise optional inputs and key mismatch rejection through the integrated implementation. Reuse the same declared rule and expected key strings. No rekeying is intended solely because explicit authoring is replaced by shared composition; any actual output mismatch requires explicit reconciliation rather than rewriting historical keys. Preserve ordinary lineage identity, historical key claims and exact references. Product/runtime producer behavior belongs to its delivery milestone; AS1 adds no onboarding implementation.

### AS2 — Supported first-space provisioning, constitution, and Open

**Lifecycle delivery:** provision one eligible unclaimed HolonSpace with its local semantic foundation; support human-initiated Local Sovereign Constitution through Client Security; establish PersonAgent and sovereign association using shared commitment/validation; Open/restart compatible state without replacing identities or repeating acquisition; present only currently valid supported choices. Upgrade and rehabilitation are outside this milestone. Apply design v0.12 §§5–6 and 11–13. AS1 is merged via [PR #871](https://github.com/evomimic/map-holons/pull/871), merge `36a577c2fa5b6c78419897ecdfcca4e56b32b79b`, reviewed head `70de9d6f`; its fixtures do not establish acquisition guarantees.

<a id="reconciled-implementation-units--proposal-for-review-2026-11-16"></a>

#### Reconciled implementation units — updated scope, 2026-11-25

AS2 remains the lifecycle milestone tracked by [#870](https://github.com/evomimic/map-holons/issues/870). [CS-L1 #872](https://github.com/evomimic/map-holons/issues/872) supplies its bounded security mechanisms. Their completion criteria are not interchangeable with checkpoints, preparatory code slices or PR boundaries. The following decomposition now follows the revised supported-first-space boundary in #870 and design v0.12. The earlier AS2-U delivery requirement is superseded by separate future design work; AS2-P/C/O remain the lifecycle outcomes. Existing engineering-profile evidence does not establish complete shared guarantees.

**Next Agent Spaces increment: currently valid first-space choices.** Reuse the existing startup, constitution and Welcome paths to expose supported Provision, admitted constitution, compatible authorized Open or explicit fresh-environment creation. Do not make expanded diagnostic messages the feature. Work on choice derivation/presentation can proceed now; actions requiring undelivered validation/security guarantees remain unavailable in the supported flow. Full AS2-C acceptance still requires its handoffs. Neither parent issue closes merely because this increment merges.

| Unit | Owned outcome and dependencies | Review/merge exit |
| --- | --- | --- |
| AS2-P — Durable first-space foundation | AS2 owns Provision versus Open classification, fixed local foundation and retained Space identity; consumes CS-L1.1's supported packaged execution boundary. This is a prerequisite contract, not personal constitution. | The supported packaged path provisions exactly once, reopens the same unclaimed Space/content without create-import replay, and refuses or explicitly remediates incomplete/incompatible state without replacement. Live startup must reach a terminal verified state, not only a responsive Welcome window. |
| AS2-C — First personal constitution | Consumes AS2-P, CS-L1.1/2, shared key/relationship/validation/Commit handoffs; integrates CS-L1.3 principal binding and durable retirement in the constitution transaction. | Explicit Welcome initiation produces the complete supported personal constitution, preserves the existing Space, exposes its actual committed outcome and passes the detailed contract below. Acquired-state recognition and retired acquisition authority survive restart; operational authorized Open/Navigator may remain unavailable. |
| AS2-O — Authorized Open and Navigator handoff | AS2 owns runtime reconstruction/presentation; consumes CS-L1.4 retained-credential authorization and a reconciled finite Navigator operation inventory. | Valid credentials open the same acquired Agent/Space after process/conductor restart without schema replay, reacquisition or bootstrap reopening; the authorized built-in Navigator experience appears. Missing/inconsistent credentials deny operation while preserving sovereignty. Only explicitly inventoried operations are exposed. |

**Former AS2-U:** removed from AS2 delivery and closure criteria. Upgrade, DHT migration and rehabilitation require the separate future design described below.

CS-L1.1–4 are delivery labels defined in the [Client Security plan](../security/map-client-security-impl-plan.md#reconciled-cs-l1-implementation-units--proposal-for-review-2026-11-16), not new issues or a new security framework. CS5 assurance accompanies every exposed path; it is not a final permission to defer necessary security checks. AS2-C requires the security properties it exercises, not all future security capabilities. AS2-O remains required to finish the supported lifecycle. AS2-U is no longer a milestone requirement. Consume the applicable CS-L1 contracts; do not implement Client Security mechanisms or validation enhancements inside the Agent Spaces increment.

##### Current-work allocation

This is an implementation/evidence inventory, not a declaration that a unit is complete.

| Current work | Allocated unit | Evidence and remaining gap |
| --- | --- | --- |
| Merged AS1 schema and conforming fixtures (`36a577c2`) | Existing dependency of every unit | Schema/import baseline only. Retain AS1 TDL while prerequisite work is reconciled; the separately approved Lineage/Lineage target is not implemented by the current Version/Lineage declaration. Do not enable real constitution under a silently weakened relationship contract. |
| Saved local-Space discovery/adoption and skipping configured imports on Open (`e3bf588f`) | AS2-P; reused by AS2-O | Real native-conductor tests preserve Space identity after restart. This is not sovereign authorization, and does not by itself prove the complete packaged lifecycle. |
| Restricted packaged Welcome, native-only conductor access and narrow command/capability boundary (`c9316ce3`) | CS-L1.1; consumed by AS2-P/C | Mechanism tests and basic packaged-page evidence exist. Required actual-interface/local-caller/content security checks remain bounded gates; the checkpoint is not complete CS-L1. |
| Ordinary `npm start`, early development window and dev orphan-cache backup (`c9316ce3`) | Engineering startup support; relevant evidence for AS2-P | A real conductor/visible Navigator was observed. Development still selects a fresh temporary conductor store on every normal launch; full bootstrap repeats. Reusing an isolated development store is a correctness/tooling follow-up, not a reason to restore the test-key/cache-reset optimization. Development is not the supported constitution security profile. |
| State-aware Welcome and deny-only target/admission projection (working tree) | AS2-P/C presentation and CS-L1.2 preparation | 35 host and 3 shipped-page-script tests passed in the final AS2-P verification; all constitution requests remain denied. No usable credential, principal or acquired Space has been created by this work. An empty observed inverse is deliberately not classified as authoritative unclaimed eligibility. |
| Extended native test: foundation checks/current inverse, fresh-runtime adoption and restart (working tree) | AS2-P evidence; later reused by AS2-C/O | The final 35-test host suite passes, including fresh provisioning, explicit missing-definition/incompatible-version refusal and retained Space/content identity after restart with no import replay. Does not prove historical absence, actual acquisition, protected custody, retirement or authorized acquired-space Open. |
| Native conductor startup and packaged retained foundation | Shared native startup prerequisite consumed by AS2-P | The pinned native DHT dependency now range-searches gossip sectors instead of repeatedly scanning the store. The rebuilt packaged app reached terminal foundation-present and checked 31 configured definitions without import replay or resetting the retained store. The additive index migration and future migration-history compatibility are documented in `host/patches/README.md`; this is not an AgentSpace transaction/authorization mechanism. |

##### Prerequisite handoffs for AS2-C

The handoff is a concrete supported contract plus evidence on a named revision. Existing machinery must be reused; listing a gate is not a claim that all its mechanisms are absent. Shared negative-case coverage must be verified before real constitution, rather than inferred from descriptor declarations or valid fixtures.

| Gate / owner | Minimum handoff to AS2-C | Current disposition and first action |
| --- | --- | --- |
| Foundation / AS2-P | Stable supported packaged installation and Space; required local foundation; terminal startup and repeated-launch identity/content evidence; deterministic refusal or supported reconciliation of partial provisioning | Delivered by map-holons `c2d3d105`; see the AS2-P delivery record below. The real-conductor provision/restart test preserves Space/content identity without import replay, and the packaged retained-store run reaches foundation-present. The fixed dependency checks do not claim the separately owned full-Core readiness predicate or sovereign authorization. Isolated development-store reuse remains a bounded tooling follow-up. |
| PersonAgent instance key policy | Explicit NoneRule, absent Key, required/optional names preserved; discovery by committed association and IDs | The 2026-11-16 keyless decision removes #868/#87 from the creation critical path. Those issues remain shared composer work; no private renderer or fixture-key substitution is needed. |
| Relationships/references / shared owner | Authoritative saved association/absence lookup, source-version carry-forward, successor/inverse traversal and same-lineage accounting for the approved sovereign pair; explicit ambiguity policy | Not established by current Welcome observation tests. Supply the bounded shared contract/evidence, then integrate the approved canonical binding delta through ordinary tooling. Retain AS1 TDL until that integration is ready; no TDL edit is part of this reconciliation. |
| Constraints / shared descriptor-driven Commit validation | Required endpoints/cardinality/inverse effects, Home Space correspondence, both historical continuity invariants and affected saved endpoints, using approved shared constraint declarations/evaluation | Current schema declarations and declaration validation are not evidence of these acquisition rejections. Confirm the smallest missing configured/shared evaluation capability in its owning workplan; no AS2-local validator or new semantics property by convenience. |
| Commit/retry / shared transactions and persistence | Acquisition-specific use of accepted Complete/Rejected/Incomplete outcomes; retained identities, staged/saved work and diagnostics; paired effects, local conflict handling, authoritative unknown-outcome query and deterministic resubmission | Existing Commit semantics are accepted. Deliver bounded acquisition/fault/conflict evidence and any demonstrated missing shared capability. No all-or-nothing rollback redesign, completion artifact, general journal or cross-cell transaction prerequisite. |
| Admission/custody / CS-L1.1/2 | Verified packaged request boundary, backend credential custody, exact installation/Space/operation scope and enforcement against reachable alternate paths | Partial boundary and deny-only code exist. Resolve and verify custody and scoped allowed admission in the owning Client Security contract. An empty-passphrase Lair instance, localhost, author key or supplied flag is not the required handoff. |
| Binding/retirement / CS-L1.3 integrated with AS2-C | Durable meaning and binding of principal/author/executor authority, retirement and retry/consumption behavior tied to committed constitutive state | Not delivered. Settle the minimal representation/lookup contract in the owning security/persistence architecture, then integrate and test with real constitution. Do not require CS-L1's complete AS2 integration to be finished before building this integration; that would be circular. |

Minimum compatible schema/security evidence interpretation is required for AS2-C; Upgrade, migration and rehabilitation implementation are not prerequisites. Mechanism design choices still open in the owning specifications must be settled there before enabling the corresponding path. Local Sovereign Constitution and the trusted packaged-Welcome boundary remain approved; no external identity proofing or independent native confirmation is reopened.

##### Proposed first-personal-constitution PR acceptance contract

**PR objective:** an eligible installation with one existing unclaimed HolonSpace lets its human explicitly constitute their PersonAgent through packaged Welcome, with a real saved sovereign association, required authorization effects and durable retirement of acquisition authority. A successful feature demonstration ends in an evidence-backed constitution result in Welcome. Navigator handoff and full operational Open belong to AS2-O; a disabled button or schema fixture does not satisfy this PR.

1. **Supported first-space lifecycle.** On the supported packaged profile, first launch provisions one Space/foundation before the PersonAgent exists. A second launch before constitution preserves its exact Space identity/content and skips original create imports. Partial/incompatible/unreadable provisioning is explicitly blocked or follows an approved reconciliation path, never silently replaced.
2. **Explicit trusted initiation.** Welcome accepts only the required personal name data (LastName required; optional FirstName/MiddleName under the retained schema). Those values are data, not authority. Backend resolution selects the eligible installation/Space; supplied Agent/Space/author IDs, keys and bootstrap flags cannot confer authority. Approved packaged initiation works without external identity proofing or independent OS confirmation.
3. **Scoped protected admission.** Relevant CS-L1.1/2 controls are demonstrated on the supported configuration: credential custody, origin/content isolation, caller admission, operation/Space binding and protection/closure of alternate reachable IPC, management, signing and zome paths. The frontend receives no reusable constitution authority. Required security properties are verified before the action is enabled; an unsigned bundle or passing unit test alone does not establish them.
4. **One logical constitution transaction.** Using ordinary bound references and TransactionContext, stage the PersonAgent in the intended Home Space, declared HasInterior and all required authorization effects as one complete logical operation. Create a keyless PersonAgent under NoneRule; do not write Key. Preserve the Space's lineage/type/content and existing schemas; do not independently author IsInteriorOf or intentionally commit Agent creation as a separate completed transaction.
5. **Correct acquired-state and onboarding reporting.** Read committed IsInteriorOf through the approved authoritative lineage-aware lookup as the settled acquisition predicate. No completion record or Recognized stage is introduced. A committed association remains acquired if other onboarding effects need remediation; report those effects as incomplete rather than reporting full onboarding success or calling the Space unclaimed again. Full success requires the complete supported outcome, not transport success or process-local readiness.
6. **Shared semantic enforcement.** Required shared tests reject missing/multiple interiors, wrong endpoints/Home Space, removal/replacement and another Agent lineage acquiring the Space, including graph-only changes and affected saved endpoints. Initial valid constitution succeeds. Shared evidence demonstrates ordinary endpoint evolution and same-lineage accounting without changing the established pair or unintended Agent propagation; it does not expand packaged mutation permissions.
7. **Accepted Commit outcomes preserved.** Complete/Rejected/Incomplete remain distinct. Rejected leaves remediable staged work/diagnostics; Incomplete retains saved work, staged work, identities and diagnostics for remediation/resubmission of the same acquisition. Fault injection demonstrates applicable failures and retries. No new rollback prerequisite or intentionally split constitution is introduced.
8. **Duplicates, concurrency and ambiguous responses.** Repeated clicks, competing local attempts and response loss recover the original allowed outcome or an explicit conflict/incomplete/unknown result. They cannot create a second PersonAgent lineage/association as a retry strategy. An unavailable or ambiguous authoritative query cannot trigger fresh acquisition; committed historical association remains authoritative even if a current prospective inverse appears empty.
9. **Durable retirement and minimal restart recognition.** After completed constitution, restart rediscovers the same Agent/Space association and cannot reissue acquisition-only authority, even when the technical author retains invocation rights. Missing credentials deny privileged execution without erasing sovereignty or offering reacquisition. This is the minimum restart/retirement proof for AS2-C, not a claim that full authorized Open or Navigator is delivered.
10. **Currently valid choices.** Through explicitly inventoried lifecycle/identity reads, Welcome offers only supported actions under current compatibility, evidence and authority. Show completed constitution or an unavailable continuation accurately; internal findings do not require a detailed diagnostic experience. Offer retry/remediation only when the existing contract actually supports it, and never imply that retaining an incompatible Space makes it recoverable. Unsupported operational Dancers, mutations, generic dispatch and Navigator actions remain unavailable or protected. No standing bootstrap/admin bypass results from successful constitution.
11. **Real-boundary evidence.** Proposed AS2-C scenario labels are ConstitutionHappyPath, RejectedRemediation, IncompleteResubmission, DuplicateAndConflict, LostResponse, RestartRetirement and UnauthorizedConstitution; these are planned acceptance cases, not existing test identifiers. Before enablement, map them to actual IPC/runtime/zome entrypoints and real tests. Use fresh references and process/conductor restart where claimed; reference shared mechanism suites without duplicating them or treating mocks as proof of actual admission.
12. **Review scope and closure.** Record exact source/dependency revisions, supported configuration, security assumptions, passed checks and limitations. All first-constitution requirements above must pass or the PR remains draft/not merge-ready. The PR references #870/#872 as partial delivery; it does not close either milestone or claim complete CS-L1, production readiness, authorized Navigator, Upgrade or AS3 personalization.

##### Execution and review sequence

1. Deliver the currently-valid-choices increment described below using existing lifecycle paths. Keep baselined Commit outcomes, retention and supported remediation/resubmission intact.
2. Consume Rashaan's [Commit Validation track](../validation/commit-validation-impl-plan.md) for reusable semantic enforcement and the [Client Security plan](../security/map-client-security-impl-plan.md) for admission, custody, authority binding, retirement and authorized Open. Resolve missing contracts in their owning tracks; do not turn them into Agent Spaces implementation scope.
3. Integrate available handoffs and verify AS2-C, then AS2-O with its finite authorized operation inventory. Keep engineering evidence distinct from completed supported security/sovereignty acceptance. No additional acquisition authority is enabled by choice/presentation work alone.
4. Close #870 only when its revised supported-first-space requirements are met. Upgrade, DHT migration and rehabilitation are not closure gates; #872 retains its own security completion criteria.

**Tracking alignment:** #870 was updated on 2026-11-25 to record PR #880, preserve baselined Commit behavior and focus on valid first-space choices. Its former Upgrade requirement is superseded. Any older Client Security tracking language about physical atomicity or Upgrade must be reconciled in that owning track; it does not expand this Agent Spaces increment. No new shared issue identifiers or delivered guarantees are implied.

##### Currently-valid-choices increment

| Current condition | Available behavior |
| --- | --- |
| No provisioned Space and provisioning is permitted | Provision one first Space/foundation, then offer constitution only when eligible and admitted. |
| Compatible provisioned unclaimed Space with required handoffs | Continue constitution in that existing Space. An empty current inverse alone does not prove eligibility. |
| Compatible acquired AgentSpace with valid authority/readiness | Open the same Agent/Space/content without import replay or reacquisition. |
| Incomplete, unknown, ambiguous or unauthorized state | Offer only continuation established by existing contracts; otherwise withhold the unavailable action. Do not infer a fresh acquisition or invent a repair/retry. |
| Incompatible Space | Refuse Open/constitution. Offer a separate fresh environment only where supported and explicitly selected; this does not recover or transfer the old Space. |

Implement through existing startup/Welcome/orchestration paths; no general environment manager, detailed-diagnostics project, new persistence protocol or cross-process recovery engine is included. Verify that available choices match the evidence, existing compatible restart preserves identities/content, unavailable actions do not execute, and incompatible-store retention/listing/selection is never presented as rehabilitation. Reuse existing tests and engineering-profile evidence where applicable; record the configuration and missing handoffs.

##### Separate future design: Upgrade, migration and rehabilitation

Design §6.7/D14 owns this deferred capability boundary. Before planning implementation, identify code/schema component compatibility and consider prior-code selection/rebuild, older-schema updates and migration to a new DHT for integrity-zome changes. Define authorization, identity/content treatment and interruption behavior for any actual supported transition. Retaining a prior Space directory does not supply any of these operations. Neither fresh-environment creation, initial import, coordinator-only maintenance nor no-op Open demonstrates rehabilitation or a semantic Upgrade. No new future-work issue, transition protocol or migration implementation is created by this plan update.

#### AS2-owned implementation

1. Integrate the existing bootstrap/import lifecycle as supported Provision, constitution and compatible Open, exposing only currently valid choices. Preserve existing TransactionContext, Reference Layer and transport binding paths. Recheck `core_schema_bootstrap.rs`, `space_imports.rs`, `ensure_core_schema_space()` and guest completion/index handling on the implementation baseline; do not create a competing bootstrap.
2. Provision one unclaimed ordinary HolonSpace with packaged local CoreSchema and Agent Spaces. Reconcile `MAP.CoreSchemaSpace` naming/key assumptions without replacing/retyping the space, duplicating content or requiring a descriptive-property rewrite. Display identity may be presentation-only.
3. Provide foundational Welcome and scoped definition imports. Request constitution authorization through the CS-L1 contract; do not implement credential issuance/custody or a capability framework in AS2.
4. Deliver the canonical HasInterior Lineage-binding schema delta, retaining definitional status and derived IsInteriorOf. Declare Home Space and historical continuity requirements using the approved shared mechanisms. General evaluators and binding-aware traversal are prerequisites, not AS2 implementations.
5. Orchestrate one complete constitution: stage PersonAgent in its intended Home Space, declared HasInterior and required authorization/completion effects using ordinary bound references and transaction APIs. Consume shared admission, validation and commitment results. Do not intentionally split Agent creation and acquisition into separate completed transactions or author the inverse independently. Preserve partially saved work and diagnostics on Incomplete; remediate and resubmit the same acquisition with retained identities.
6. Use committed IsInteriorOf as completed constitution, preserving authored HasInterior and the owning lineage lookup contract. Integrate conflict/interruption/retry outcomes through existing persisted-state queries; no completion artifact, Recognized state or read-time acquisition revalidation. Keep current authorization/compatibility and legitimate provisioning/loading checks distinct.
7. Integrate durable acquisition-privilege retirement and authorized runtime reconstruction through CS-L1. Admit the built-in House Troupe under the approved containing-space policy, not a supplied identity or author key. Enumerate required supported operations in the CS-L1 integration inventory; no general membership/role engine, negotiated Agreements or TrustChannels. All exposed privileged operations require authorization; unsupported paths remain unavailable/protected.
8. Implement compatible valid-credential Open/restart and safe incompatible-state refusal. Preserve Agent/Space/content identity on Open. Where supported, fresh-environment creation is a separate explicit choice; retained incompatible state is not recovery. Upgrade, DHT migration and rehabilitation remain separate future design work.

There is no persistent Active sovereignty transition. Closed/Opening/Ready/Closing remains runtime state.

#### Explicit minimum dependencies

These labels identify bounded work, not newly created GitHub issues. Owners must link delivery issues and verified revisions before the corresponding path is enabled.

| Dependency | Owner and minimum handoff | Broader work outside the dependency |
| --- | --- | --- |
| [CS-L1 #872](https://github.com/evomimic/map-holons/issues/872) | [Client Security plan](../security/map-client-security-impl-plan.md#minimum-operation-inventory): approved local trust contract, scoped constitution, credential custody, durable retirement, opening/restarting the same acquired AgentSpace and only the finite operations mapped to AS2-Local-Lifecycle, with security evidence for one supported configuration | General Dancer authorization, arbitrary delegation, WeSpace roles, universal policy engine, adaptive risk, rotation/revocation, credential recovery and TrustChannels |
| Local acquisition commitment | Existing shared Commit contract: preserve Complete/Rejected/Incomplete, saved work and diagnostics; verify acquisition remediation/resubmission, paired inverse completion, conflicts and committed-state retry queries without duplicate identities or associations | Rollback redesign, new transaction subsystem, completion artifact, general journal or cross-cell coordination |
| Relevant relationship/constraint enforcement | Rashaan's [shared Commit Validation track](../validation/commit-validation-impl-plan.md): required endpoints/cardinalities/inverses, Home Space correspondence, both historical invariants and affected saved endpoints through reusable assessment | Unrelated constraint coverage or general dynamic rule loading |
| Lineage/reference behavior | Shared relationship/reference infrastructure: binding-aware comparisons, successor/inverse traversal and same-lineage accounting needed by the sovereign pair | General cache or version-adoption redesign |
| Approved type key policy | Consume the approved schema policy; keyless PersonAgent under NoneRule does not depend on #868 / DevDocs #87. Reconcile the shipped name-key policy separately. | Shared key composition remains independently owned, not an AS2 implementation task |
| Compatibility contracts | Each owner defines supported current code/schema/evidence/security interpretations; AS2 selects valid first-space actions and refuses incompatible Open | Upgrade, code/schema reversion or repair, DHT migration and rehabilitation |

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
| Baselined Commit outcomes, concurrency, stale reads, caught failures and lost-response retry | Shared transactions/persistence | Consume existing outcomes and supported remediation/resubmission |
| Authorization evidence meaning / reliable storage / domain completion | Client Security / shared persistence / Agent Spaces respectively | Integrate without prescribing a record type |
| Supported Provision/constitution/Open choices and incompatible-state refusal | Agent Spaces, consuming each owner's compatibility contract | Offer only currently valid actions; retention does not imply recovery |
| Mechanism-level tests and assurance | Corresponding shared owner | Selected real-lifecycle acceptance scenarios |

#### Acceptance and evidence

AS2 acceptance demonstrates one durable Space with local schemas; explicit human constitution through approved admission; PersonAgent Home Space and declared/derived association; independent Agent/Space version evolution; rejection of removal, replacement and conflicting acquirers; deterministic duplicate/interruption/lost-response outcomes; valid-credential restart without reload/reacquisition/bootstrap reopening; missing-credential denial; scoped imports with unauthorized Dancer denial; and currently valid first-space choices with incompatible-state refusal. Upgrade, migration and rehabilitation are not AS2 acceptance requirements. Include non-root references, affected saved endpoints and historically acquired Spaces with prospectively empty inverses.

Shared owners supply mechanism-level security tests, reusable validator tests and persistence fault/conflict evidence. AS2 repeats selected end-to-end scenarios through the real conductor and published contracts; it does not own every attack/fault test or certify the entire security roadmap. Required security assurance for the supported deployment cannot be waived. Map the finite CS-L1 operation inventory to actual AS2-Local-Lifecycle entrypoints and test identifiers before enabling them; shared versioning/validation tests do not implicitly expand it. Record exact dependency revisions, configuration and unverified guarantees.

Lifecycle discovery/classification, compatibility analysis, Space-identity preservation and Welcome presentation/request contracts can proceed independently. Acquisition and privileged execution remain disabled until their bounded dependencies are delivered. No second Space/DHT, remote CoreSchema, shared admission, general Declaration/Agreement implementation or recovery framework is required.

### AS2 delivery increment — state-aware packaged Welcome (2026-11-16)

The packaged startup path now observes saved Space/foundation/sovereign-association evidence and projects it through restricted Welcome. Initial loading, foundation-present, recorded sovereign association and unavailable/ambiguous evidence remain distinct. A recorded association hides the constitution action; neither a saved Space nor an empty current inverse collection establishes acquisition eligibility or authorizes reopening. Missing foundation or lookup failure blocks without replaying imports or replacing identities. Packaged startup failures retain the Welcome window with admission closed.

The [CS2/CS3 initial admission contract](../security/map-client-security-impl-plan.md#state-aware-welcome-and-initial-admission-contract--2026-11-16) resolves the target internally through the configured runtime and accepts no caller-selected IDs, keys or bootstrap flags. No usable constitution credential is issued and the action remains disabled pending protected custody, shared acquisition prerequisites and durable authorization/retirement. State-aware presentation is delivered independently of those prerequisites; no new constitution-completion artifact, validator or Commit semantics is introduced.

The current engineering `npm start` path uses ordinary conductor startup rather than the cache-reset/test-key optimization. Its main window is created after provider/runtime initialization and before schema loading, so its existing UI can display startup progress. It continues to be a development configuration and is not evidence of packaged sovereign authorization. The supported packaged flow will converge on Welcome for initial constitution and Navigator after authorized Open; general navigation/mutation authority is not implied by CS-L1's existing finite lifecycle inventory.

**Increment evidence:** 34 host tests and 3 actual-page-script tests passed; web typecheck, Rust formatting and unsigned packaged app build passed. The native-conductor test verifies missing-foundation denial and saved Space/current-inverse observation across restart without import replay. Live packaged inspection verified initial Welcome status and disabled constitution; retained-state opening was stopped before conductor initialization finished, without resetting data. Historical eligibility, credential custody, acquired-space authorization and terminal packaged Open remain explicit enablement/evidence gates. See the Client Security plan for the detailed limits.

### AS2-P delivery — bounded first-space foundation (2026-11-16)

The supported packaged path preserves the existing provisioning mechanism. The guest writes `LocalHolonSpace` only after a Complete bootstrap Commit. Host startup now also requires the actual LoadHolons `LoadCommitStatus` to be Complete before advancing. Rejected, Incomplete and transport/error outcomes retain ordinary transaction/result state for diagnostics and supported remediation/resubmission; no rollback or new completion artifact is introduced.

Provision loads the fixed configured definition imports through the existing loader and verifies the newly loaded packages once. Normal Open adopts the existing local Space, checks the supported Core identity, resolves the sovereign association and reuses committed definitions. It does not reread the package import JSON or repeat the 31-definition type/relationship audit. This supersedes the earlier retained-Open audit recorded in the historical evidence below. It does not replay imports, activate a Dancer, create a replacement Space or interpret an empty sovereign inverse as acquisition eligibility. Missing or incompatible dependencies are reported when required by the requested operation; incompatible CoreSchema identity blocks Open. Retaining the store is not remediation or Upgrade; a fresh environment, where supported, is a separate explicit choice. Existing Commit remediation and retained identities remain authoritative.

This is a bounded AS2 dependency check under D4, not a new full-Core manifest audit or a claim that every Dance is ready. The separately owned bootstrap manifest-readiness gap remains recorded below and in the Core bootstrap plan. No generalized resolver, persistent readiness marker, acquisition privilege or change to AS1 TDL was added.

**Packaged evidence:** the unsigned Apple Silicon `custom-protocol` bundle reached terminal `foundation-present` on the retained installation. Native accessibility inspection confirmed the backend-provided foundation message and disabled constitution action at `tauri://localhost/welcome.html`. Backend logs confirmed adoption without bootstrap replay and verification of all 31 configured definitions. The existing store was backed up before the additive native index migration; no Space, Agent or content reset occurred. Constitution and authorized acquired-space Open/Navigator remain gated.

**Native startup diagnosis:** the earlier delay was in Holochain/Kitsune gossip-sector queries before MAP schema loading. A disposable copied-store probe changed from 209.94 seconds to 0.732 seconds for 512 sectors with identical timestamp/count aggregates. A single-connection comparison with SQLite lock waiting disabled returned identical eight-sector results in 2.578 seconds with the original predicate and 0.014 seconds with concrete range predicates. The native patch adds location indexes and changes only those two queries; no hApp/WASM or MAP Commit semantics changed. This measurement is separate from the expected 60–180 second initial schema load. A proposed full-manifest startup scan was removed from this increment to preserve the bounded D4 scope.

**Verification:** all 35 host library tests passed, including the real-conductor provision/restart test (206.90 seconds for the suite). The test exercises the same startup helpers as the packaged host, counts loader invocations, preserves Space/descriptor IDs and rejects missing configured definitions and an unsupported Core identity without import replay or replacement. All 146 dependency library tests, 3 shipped Welcome-script tests, scoped formatting/diff checks and the unsigned packaged build passed. No full CS-L1 or production-security assurance is claimed.

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
5. Make PersonAgent onboarding, logical creation/acquisition, runtime readiness and compatible Provision/Open repeatable for the second independent space without hardcoded founder IDs or development filesystem paths. Upgrade and rehabilitation require their separate design; provisioning a second Space does not establish recovery of the first.
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
- [ ] Valid-credential compatible Open/restart reopens the same Agent, Space and saved holons without reprovisioning; missing credentials fail closed.
- [ ] Welcome offers only currently valid supported first-space choices. Incompatible Open is refused; a supported explicit fresh-environment choice is not reported as recovery.
- [ ] Retention/listing/selection of an incompatible Space makes no reconnect/rehabilitation claim. Upgrade, DHT migration and rehabilitation are separate future design work, not completion gates.
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

AS2 owns AgentSpace behavior and integration. Client Security owns shared authorization/assurance; transaction, relationship, key and validation mechanisms remain separately delivered dependencies. The ownership ledger and minimum dependency table above replace accumulating general mechanism design in the lifecycle issue. At this reconciliation, constitutive evidence representation remained open; design v0.9 subsequently settles it as committed IsInteriorOf, with no dedicated record type.

## AS2 first implementation slice — 2026-11-15

Independent first work: read-only discovery of the executing cell's existing local-space index through ordinary runtime/reference/Dance layers; adopt that identity before choosing Provision versus Open; avoid replaying configured create imports on Open. Missing designation permits initial provisioning only when no authored application footprint exists; ambiguous, broken or unreadable designation must fail closed rather than create a replacement. Finding a Space does not establish acquisition or grant authority. Preserve AS1 TDL and the type-free name key; the separately approved HasInterior Lineage delta remains pending shared validation/traversal.

Implemented evidence covers discovery before provisioning (no state created), adoption by a fresh host runtime, retained Space/content identity and error-versus-absence handling. The startup Core-key compatibility check and Provision-only fixed definition checks do not claim the full bootstrap manifest graph predicate; retain that separately owned bootstrap work as an explicit readiness gap. AS2-P reuses the existing guest-side rule that publishes the local designation only after a Complete bootstrap Commit, without adding a full-manifest audit to ordinary Open. Loader recovery must distinguish successful loading from interrupted packages without a general resolver or a global schema-readiness marker. Existing-package presence alone is not proof of complete loading. Future readiness is dependency-driven/per-Dance; no speculative distributed registry is implemented.

The existing two-pass Commit deliberately retains successful persistence and returns Incomplete with diagnostics when other writes fail. This accepted behavior supports remediation and resubmission; it is not a defect or a shared rollback prerequisite. Verify acquisition using those semantics: preserve saved identities and associations, retain correctable work, complete missing effects on resubmission and avoid duplicate constitution. A persisted IsInteriorOf remains sovereign evidence; incomplete onboarding does not supply missing operational authorization. Reuse existing Dance execution placement and verify the executing cell/Space; do not introduce another ExecutionContext framework.

CS-L1 authorization and historical/lineage enforcement remain dependencies. Acquisition must integrate and verify existing conflict/retry behavior; no general Commit redesign is implied. Independent lifecycle work may proceed; do not enable acquisition or new privileged operations. Retrospective recognition, TransactionWarrant infrastructure, global activation markers, general roles, additional cells/DHTs and speculative Upgrade frameworks remain deferred. AS2 owns lifecycle integration; shared owners supply their mechanisms and evidence.


### Earlier next-step note — superseded by the reconciled implementation units

The earlier sequence prioritized the [Client Security implementation contract](../security/map-client-security-impl-plan.md#repository-grounding-and-implementation): map the finite lifecycle inventory to actual Tauri IPC, Rust runtime and conductor/zome entrypoints; establish backend admission, credential custody, eligible-Space scope, retirement and restart checks under the approved packaged-Welcome boundary. Verify denial through alternate callers, untrusted content and supplied identity/bootstrap flags. Independent native confirmation and a new credential framework are not prerequisites. This remains a shared security handoff consumed by AS2; it does not broaden AS2 or replace existing Commit semantics. The revised AS2-P/C/O units and prerequisite matrix above govern sequencing; the former AS2-U requirement is deferred: CS-L1 is not one opaque prerequisite that must finish before AS2 begins. Required key, relationship/lineage, validation and acquisition-retry evidence remain explicit parallel handoffs.


## Keyless PersonAgent creation increment — 2026-11-16

The approved current instance key rule is NoneRule; this supersedes the earlier instructions to retain the type-free name key. Canonical TDL and generated/packaged imports now select it. The inactive PersonAgentName FormatRule remains ordinary unused schema content. Existing local test stores with the previous FormatRule are not automatically upgraded or reset; the creation executor verifies the selected instance policy and refuses incompatible state.

The native creation executor accepts naming data and a caller-owned ordinary empty transaction, stages a PersonAgent in its existing Home Space, adds declared HasInterior and invokes existing Commit once. It returns the existing MapResult and retains the transaction and ordinary diagnostics for remediation/resubmission. It never independently authors IsInteriorOf, creates a replacement Space, supplies a key, enables bootstrap or implements a private validator. A recorded current association blocks a repeated create; empty inverse membership does not grant authority or establish historical absence. Production Welcome remains unconnected pending its admission, binding and shared enforcement work.

The existing disposable-conductor test is extended to execute this real transaction, inspect saved names, absent Key, Home Space and the derived inverse, and refuse a second create. The AS1 name-version fixture now traverses saved IDs and preserves keylessness rather than manually assigning keys. Signing and the key composer are not prerequisites to this isolated implementation/evidence path. Verification results follow after execution; no retained user store is modified.


The real creation test exposed two existing key assumptions, now corrected generically: HolonPool allocates keyless staged candidates without a key-index entry, using phase-distinct temporary IDs; Commit builds a saved ID-bound response reference when the saved holon has no key. Neither fix manufactures a semantic key or changes Commit outcomes. The failing keyless staging regression passed after the fix, together with all 745 shared-core unit tests. The compiler's 58 library tests and three Agent Spaces schema tests pass; the full corpus reports no diagnostics. The hApp/WASM and native host rebuild successfully. Real-conductor checks are rerun after both keyless fixes.


### Verified keyless creation result

All 37 host tests passed, including `native_only_keyless_personal_constitution_preserves_space` (190.96 seconds for the suite). The new native executor returned a Complete Commit on a real disposable conductor. Fresh reads verified LastName/FirstName, absent MiddleName and Key, the existing PersonAgent descriptor, HasInterior, OwnedBy and derived IsInteriorOf. A repeated create was refused without staging another PersonAgent. After conductor shutdown and reconstruction of host caches, the same PersonAgent and HolonSpace IDs and absent Key were observed, with no bootstrap import replay.

Both Agent Spaces integration tests passed with the existing 60-second peer-store startup setting (196.02 seconds): missing required LastName is Rejected and remediated in the same transaction; the committed PersonAgent and name-update successors remain keyless and retain the sovereign pair. All 745 shared-core tests, 58 compiler library tests and three schema/package tests passed; the full corpus check reports no diagnostics, and the hApp/WASM and host builds succeeded. Earlier runs reproduced the staged-key and post-save-key assumptions before their fixes; one initial fixture run hit the upstream ten-second readiness timeout before schema execution. No validation assertion was removed.

This is real PersonAgent creation/persistence, not an enabled production Welcome flow or complete AS2-C authorization/retirement/concurrency acceptance. No live user store or Keychain was modified. The queued observer follow-up is preserved separately in a stash. Keyless code, generated imports and documentation changes remain uncommitted pending checkpoint.


## Local Welcome constitution and retained Open — 2026-11-16

The explicit `local-constitution` packaged debug build connects Welcome's names-only request to the native creation executor. Exact packaged WebView/origin admission and existing command permissions remain in force; Rust resolves the local Space, checks the current association again, and serializes creation requests. One successful ordinary Commit creates the keyless PersonAgent and declared HasInterior. Complete archives the finished transaction; Rejected, Incomplete and errors with staged work retain the existing RuntimeSession transaction for ordinary remediation/resubmission. Welcome cannot restage another candidate while that work is retained. This increment does not add a diagnostics/remediation editor to Welcome.

All ordinary application launches retain a stable conductor store. The local constitution build uses the application-data `holochain/local-constitution` directory, separate from older foundation-only state; ordinary Tauri development uses `holochain/development`. Neither ordinary startup path deletes its store. The explicit legacy cache-reset optimization remains a separate mode. Current development state need not be preserved, but identity/content continuity across subsequent launches is required; no automatic schema migration or reset is introduced.

Build with `npm run welcome:build -w map-host` and launch with `npm run welcome:start -w map-host`. The latter runs packaged assets and clears the three unsupported development overrides; it does not launch a localhost frontend server or reset data. On the first launch, provisioning loads the foundation once and Welcome offers creation. Subsequent launches adopt the existing cell/author, Space and PersonAgent, verify configured imports without replay, and present Welcome back without another constitution action. Navigator handoff is separate from this bounded reopening behavior.

Apple enrollment/signing is not required to exercise this local workflow. Its existing unsigned engineering custody is not the app-restricted Keychain assurance claim. The feature requires a packaged debug build and cannot be combined with protected-custody; default/signed profiles retain their admission gates. Current-association checks and the installation lease do not claim shared historical/distributed acquisition enforcement or completed production principal authorization. AS2 scope, Local Sovereign Constitution and existing Commit semantics remain unchanged.


**Verified:** all 38 host tests passed (268.06 seconds), including the real persistent-conductor test using the same `WelcomeConstitution::submit` backend called by IPC. Concurrent and sequential repeat requests were refused; after shutdown and reconstruction, the Holochain author, PersonAgent ID, Space ID, names and keylessness were retained. Core and configured-package Open returned existing state with no additional LoadHolons calls; the newly constructed backend also refused another constitution. All 506 web tests passed with one skipped, including nine tests of the shipped Welcome HTML/JavaScript covering creation, returning-installation presentation, duplicate suppression and retained Rejected/Incomplete outcomes. Type checking, formatting and scoped diff checks passed. The matching hApp and debug packaged app built successfully, including the executable target. This is real backend restart evidence plus shipped-page tests; a live human-initiated packaged constitution has not been performed by the agent. Existing user data and Keychain were untouched. Changes remain on the current AS2/docs branches without a new commit.


## Welcome post-Commit observation correction — 2026-11-17

The live first-launch flow exposed a presentation defect: after constitution the creation action could become available again while a fresh guard already observed the saved sovereign association. Lifecycle inspection now explicitly requests fresh IsInteriorOf membership, and status requests refresh saved evidence after startup has established the runtime. Welcome displays creation progress immediately, keeps creation disabled after a Complete response while confirming the association, and then hides the form/action for the acquired installation. This is presentation and observation correctness, not a new completion marker or authorization grant. Rejected/Incomplete transactions and ordinary remediation/resubmission are unchanged. The initial window is enlarged to 720 by 760 logical pixels to accommodate the name fields and action.

The regression fixture now creates in the same runtime that provisioned the foundation, asserts immediate post-Commit association visibility, and retains its existing identity, duplicate-request and restart checks. Earlier native coverage created only after an unclaimed-store restart and did not reproduce the first-launch observation problem. The shipped-page regression failed on re-enabling creation after Complete and passes with the correction.

Live diagnosis also found authored application state without a local Space designation in the earlier disposable store. After the user stopped MAP, that store was moved aside without deletion. An unchanged fresh bootstrap then completed CoreSchema loading in 234 seconds and enabled the form. The initial event that left the old designation absent was not captured; do not infer rollback defects or weaken the no-replacement guard from that observation. The newly constituted personal store is retained; this correction does not reset, migrate, replace or reacquire it.


### Diagnostic step timers and lean Open — 2026-11-17

The user clarified that committed definitions must not be reverified on each retrieval/Open. The package preparation function now returns immediately for OpenedExisting, before reading import JSON, beginning definition-check transactions or traversing definition graphs. Provision retains its load/verification path; shared mutation/Commit validation and the current CoreSchema compatibility lookup are unchanged. Missing dependencies are resolved and reported by their consumers, not by a blanket startup graph audit. No cache, readiness marker or weaker integrity rule is introduced.

Welcome reports the actual backend startup stage with an animated activity indicator, elapsed time on that step and total elapsed time. Loading required packages and verifying newly loaded definitions are separate stages. These are temporary diagnostic affordances; elapsed time is not a completion percentage or proof of backend progress. Detailed native log timings separate storage/configuration, saved-interface preflight, Lair startup, device-seed access and conductor construction; retained Open separately times transaction setup, Space discovery/cleanup and the supported-Core identity lookup. These measurements do not change credentials or transaction semantics.


**Verification of the final correction:** all 39 native tests passed (223.63 seconds), including the no-import-I/O/no-graph-audit Open regression, first-runtime creation, immediate post-Commit observation, duplicate refusal, retained author/Agent/Space identity and restart. All 508 web tests passed with one skipped; the eleven shipped-Welcome tests cover live per-step/total clocks, stage transitions, timer shutdown, progress feedback and keeping creation disabled after Complete. Type checking and the packaged hApp/app build passed.

A subsequent live restart ran after our builds/tests had completed. The same current store directory and the exact saved PersonAgent/Space IDs matched the preceding successful reopen. Logs explicitly report retained Open and committed-definition reuse, with no bootstrap/package import replay or repeated 31-definition audit. Native accessibility inspection confirmed the active-step timer during startup and terminal Welcome back with the creation form/action absent. This preserved the user's constituted store; the only quarantined store was the earlier disposable partial bootstrap, before personal constitution.

Measured live launch components: storage/configuration preparation 0 ms; saved-interface preflight 787 ms; Lair startup 675 ms; existing device-seed access 0 ms; conductor construction 2183 ms; embedded-runtime total 3.6 seconds. Retained Space discovery took 353 ms, transaction setup/cleanup rounded to 0 ms, and the supported CoreSchema key lookup took 189 ms (542 ms for the whole retained-Space preparation function). Backend startup completed in about seven seconds, including subsequent saved-association observation. The earlier 11-second runtime/76-second audit sample overlapped our integration workload and is not a controlled before/after benchmark; the audit's removal is established independently by code, regression and the absence of audit execution in the final log. No reduced password-hash strength, credential changes, interface relaxation or persistence reset was used to obtain this result.


### Adopted Space resolution on host — 2026-11-17

The host client resolver now reuses the existing HolonSpaceManager adopted identity before requesting persisted-designation discovery. It returns a reference bound to the caller's transaction; it adds no second content cache or application-side guest-fetch loop. On an identity miss, the existing guest discovery path and its missing/error distinctions remain unchanged. Discovery does not itself adopt or provision; trusted startup retains ownership of adoption and rejects a conflicting adoption during an in-flight cold discovery. Absence and errors are not cached as an identity.

Welcome status reads the adopted Space directly with get_space_holon; it does not rediscover or adopt one. Its IsInteriorOf read still explicitly requires freshness. Content-cache misses continue through the normal Reference Layer/cache-manager mechanism. This separates stable runtime Space identity from sovereign-membership freshness and from authorization.

The client regressions reproduce the old unconditional guest calls and verify transport-free warm resolution, guest fallback on a miss, adoption reuse across transactions and no negative/error identity caching. Native transport counters verify one discovery per cold host runtime and no extra discovery during warm status or post-Commit membership observations. The same native case retains its fresh zero-to-one association, duplicate refusal, author/Agent/Space restart identity and no-import-replay assertions. An earlier startup unit assumed forced rediscovery on an adopted identity; its replacement tests warm reuse plus the retained conflict guard during an in-flight cold discovery.


**Cache-resolution verification:** all 23 holons_client library tests pass, including the two regressions that failed before the cache-first identity correction. The real persistent-conductor case passes its transport counters (one initial discovery per cold host runtime; no additional discovery for warm status/post-Commit observations), fresh association, duplicate refusal and retained-identity assertions. After updating the superseded forced-rediscovery startup unit to cover warm reuse and a cold-discovery/adoption conflict, the remaining 39 native unit checks pass. No production behavior changed after the successful conductor case; the follow-up unit change corrected that obsolete expectation.

The packaged local application was rebuilt and reopened the user's same store directory. The exact Space and PersonAgent IDs match the previously captured successful reopen; accessibility inspection shows Welcome back with no creation form/action. Logs show retained Open with no bootstrap/import replay or definition audit. This run measured 3.4 seconds for embedded-runtime launch, 283 ms for initial cold Space discovery and 131 ms for the supported-Core identity lookup. These are cold-start measurements, not warm-cache benchmarks; warm host reuse is established by zero-discovery-call tests. Credentials, current stored content and guest discovery implementation were not changed.
