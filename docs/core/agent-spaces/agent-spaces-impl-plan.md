# Agent Spaces Implementation Plan

## Status and intended outcome

**Version:** 0.13 (AS2/CS-L1 implementation units and AS2-P retained-startup evidence)

**Date:** 2026-11-16

**Status:** AS1 merged and verified; AS2-P is implemented and verified within its bounded D4 contract. Constitution, authorized acquired-space Open and Upgrade remain gated. See the dated delivery records below.

Implement the target architecture defined exclusively by [Agent Spaces design specification](agent-spaces-design-spec.md) v0.10 through reviewable increments. The initial delivery establishes a durable first personal HolonSpace hosting local CoreSchema, an established PersonAgent identity, atomic PersonAgent creation/acquisition and authorized runtime opening, and Agent-owned VisualizerUsages used by DAHN selection. The first AgentSpace must reopen without reprovisioning. Multi-AgentSpace infrastructure is anticipated in early interfaces but **not implemented or required through AS5**; it is a separate AS6 undertaking. Personas, shared We-Spaces, and governed collectives follow in AS7–AS8.

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
- Verify acquisition integration with the existing Commit, relationship-persistence and zome-call boundaries. Preserve Complete/Rejected/Incomplete outcomes, partial-result diagnostics, remediation and resubmission. Document conflict handling and recovery without introducing an all-or-nothing rollback prerequisite. A shared transaction ID or transport success is not sufficient evidence.
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

**Lifecycle delivery:** provision one eligible unclaimed HolonSpace with its local semantic foundation; support human-initiated Local Sovereign Constitution through Client Security; establish PersonAgent and sovereign association using shared commitment/validation; Open/restart and perform supported Upgrade without replacing identities or repeating acquisition. Apply design v0.10 §§5–6 and 11–13. AS1 is merged via [PR #871](https://github.com/evomimic/map-holons/pull/871), merge `36a577c2fa5b6c78419897ecdfcca4e56b32b79b`, reviewed head `70de9d6f`; its fixtures do not establish acquisition guarantees.

#### Reconciled implementation units — proposal for review, 2026-11-16

AS2 remains the lifecycle milestone tracked by [#870](https://github.com/evomimic/map-holons/issues/870). [CS-L1 #872](https://github.com/evomimic/map-holons/issues/872) supplies its bounded security mechanisms. Their completion criteria are not interchangeable with checkpoints, preparatory code slices or PR boundaries. The following decomposition makes those boundaries explicit without changing the design specification. The first-personal-constitution PR contract below is proposed for review before further implementation; no additional implementation is authorized by labelling a prerequisite complete.

**Recommended next feature PR: AS2-C — First personal constitution.** Its result is an actual constituted PersonAgent/AgentSpace, not another unavailable Welcome action. Preparatory mechanisms may have prerequisite PRs only with their own independently useful, tested contract and named consumer. A combined integration PR may contain AS2 behavior and necessary CS-L1 integration without transferring shared security ownership to AS2. Neither parent issue closes merely because that PR merges.

| Unit | Owned outcome and dependencies | Review/merge exit |
| --- | --- | --- |
| AS2-P — Durable first-space foundation | AS2 owns Provision versus Open classification, fixed local foundation and retained Space identity; consumes CS-L1.1's supported packaged execution boundary. This is a prerequisite contract, not personal constitution. | The supported packaged path provisions exactly once, reopens the same unclaimed Space/content without create-import replay, and refuses or explicitly remediates incomplete/incompatible state without replacement. Live startup must reach a terminal verified state, not only a responsive Welcome window. |
| AS2-C — First personal constitution | Consumes AS2-P, CS-L1.1/2, shared key/relationship/validation/Commit handoffs; integrates CS-L1.3 principal binding and durable retirement in the constitution transaction. | Explicit Welcome initiation produces the complete supported personal constitution, preserves the existing Space, exposes its actual committed outcome and passes the detailed contract below. Acquired-state recognition and retired acquisition authority survive restart; operational authorized Open/Navigator may remain unavailable. |
| AS2-O — Authorized Open and Navigator handoff | AS2 owns runtime reconstruction/presentation; consumes CS-L1.4 retained-credential authorization and a reconciled finite Navigator operation inventory. | Valid credentials open the same acquired Agent/Space after process/conductor restart without schema replay, reacquisition or bootstrap reopening; the authorized built-in Navigator experience appears. Missing/inconsistent credentials deny operation while preserving sovereignty. Only explicitly inventoried operations are exposed. |
| AS2-U — Supported Upgrade | AS2 integrates one declared version transition with the owning schema/security/persistence compatibility contracts and CS-L1.4's bounded Upgrade scope. | A real supported transition, including interruption/remediation and incompatible-state rejection, preserves Agent/Space lineages and acquired authority. Initial import and no-op reopening do not count as Upgrade. |

CS-L1.1–4 are delivery labels defined in the [Client Security plan](../security/map-client-security-impl-plan.md#reconciled-cs-l1-implementation-units--proposal-for-review-2026-11-16), not new issues or a new security framework. CS5 assurance accompanies every exposed path; it is not a final permission to defer necessary security checks. AS2-C requires the security properties it exercises, not all future security capabilities. AS2-O and AS2-U remain required to finish AS2, even though they are separate reviewable outcomes.

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
| Foundation / AS2-P | Stable supported packaged installation and Space; required local foundation; terminal startup and repeated-launch identity/content evidence; deterministic refusal or supported reconciliation of partial provisioning | Partial. Diagnose the retained-store startup and finish packaged Provision/Open evidence. Do not make development Navigator success a substitute. Isolated development-store reuse may be delivered as an explicitly bounded tooling change; it is not a separate sovereignty model. |
| Keys / shared key composition and validation | Producer compose/set and conformance for the retained PersonAgent name/key rule, including optional values; ordinary uniqueness behavior | [#868](https://github.com/evomimic/map-holons/issues/868) remains open; explicit AS1 fixture keys do not supply producer support. Link the owning key-composition/enforcement delivery and evidence; no Welcome-specific renderer or manual fixture-key shortcut. |
| Relationships/references / shared owner | Authoritative saved association/absence lookup, source-version carry-forward, successor/inverse traversal and same-lineage accounting for the approved sovereign pair; explicit ambiguity policy | Not established by current Welcome observation tests. Supply the bounded shared contract/evidence, then integrate the approved canonical binding delta through ordinary tooling. Retain AS1 TDL until that integration is ready; no TDL edit is part of this reconciliation. |
| Constraints / shared descriptor-driven Commit validation | Required endpoints/cardinality/inverse effects, Home Space correspondence, both historical continuity invariants and affected saved endpoints, using approved shared constraint declarations/evaluation | Current schema declarations and declaration validation are not evidence of these acquisition rejections. Confirm the smallest missing configured/shared evaluation capability in its owning workplan; no AS2-local validator or new semantics property by convenience. |
| Commit/retry / shared transactions and persistence | Acquisition-specific use of accepted Complete/Rejected/Incomplete outcomes; retained identities, staged/saved work and diagnostics; paired effects, local conflict handling, authoritative unknown-outcome query and deterministic resubmission | Existing Commit semantics are accepted. Deliver bounded acquisition/fault/conflict evidence and any demonstrated missing shared capability. No all-or-nothing rollback redesign, completion artifact, general journal or cross-cell transaction prerequisite. |
| Admission/custody / CS-L1.1/2 | Verified packaged request boundary, backend credential custody, exact installation/Space/operation scope and enforcement against reachable alternate paths | Partial boundary and deny-only code exist. Resolve and verify custody and scoped allowed admission in the owning Client Security contract. An empty-passphrase Lair instance, localhost, author key or supplied flag is not the required handoff. |
| Binding/retirement / CS-L1.3 integrated with AS2-C | Durable meaning and binding of principal/author/executor authority, retirement and retry/consumption behavior tied to committed constitutive state | Not delivered. Settle the minimal representation/lookup contract in the owning security/persistence architecture, then integrate and test with real constitution. Do not require CS-L1's complete AS2 integration to be finished before building this integration; that would be circular. |

Minimum compatible schema/security evidence interpretation is required for AS2-C; a generalized Upgrade/migration implementation is not. Mechanism design choices still open in the owning specifications must be settled there before enabling the corresponding path. Local Sovereign Constitution and the trusted packaged-Welcome boundary remain approved; no external identity proofing or independent native confirmation is reopened.

##### Proposed first-personal-constitution PR acceptance contract

**PR objective:** an eligible installation with one existing unclaimed HolonSpace lets its human explicitly constitute their PersonAgent through packaged Welcome, with a real saved sovereign association, required authorization effects and durable retirement of acquisition authority. A successful feature demonstration ends in an evidence-backed constitution result in Welcome. Navigator handoff and full operational Open belong to AS2-O; a disabled button or schema fixture does not satisfy this PR.

1. **Supported first-space lifecycle.** On the supported packaged profile, first launch provisions one Space/foundation before the PersonAgent exists. A second launch before constitution preserves its exact Space identity/content and skips original create imports. Partial/incompatible/unreadable provisioning is explicitly blocked or follows an approved reconciliation path, never silently replaced.
2. **Explicit trusted initiation.** Welcome accepts only the required personal name data (LastName required; optional FirstName/MiddleName under the retained schema). Those values are data, not authority. Backend resolution selects the eligible installation/Space; supplied Agent/Space/author IDs, keys and bootstrap flags cannot confer authority. Approved packaged initiation works without external identity proofing or independent OS confirmation.
3. **Scoped protected admission.** Relevant CS-L1.1/2 controls are demonstrated on the supported configuration: credential custody, origin/content isolation, caller admission, operation/Space binding and protection/closure of alternate reachable IPC, management, signing and zome paths. The frontend receives no reusable constitution authority. Required security properties are verified before the action is enabled; an unsigned bundle or passing unit test alone does not establish them.
4. **One logical constitution transaction.** Using ordinary bound references and TransactionContext, stage the PersonAgent in the intended Home Space, declared HasInterior and all required authorization effects as one complete logical operation. Use the shared key producer/validation. Preserve the Space's lineage/type/content and existing schemas; do not independently author IsInteriorOf or intentionally commit Agent creation as a separate completed transaction.
5. **Correct acquired-state and onboarding reporting.** Read committed IsInteriorOf through the approved authoritative lineage-aware lookup as the settled acquisition predicate. No completion record or Recognized stage is introduced. A committed association remains acquired if other onboarding effects need remediation; report those effects as incomplete rather than reporting full onboarding success or calling the Space unclaimed again. Full success requires the complete supported outcome, not transport success or process-local readiness.
6. **Shared semantic enforcement.** Required shared tests reject missing/multiple interiors, wrong endpoints/Home Space, removal/replacement and another Agent lineage acquiring the Space, including graph-only changes and affected saved endpoints. Initial valid constitution succeeds. Shared evidence demonstrates ordinary endpoint evolution and same-lineage accounting without changing the established pair or unintended Agent propagation; it does not expand packaged mutation permissions.
7. **Accepted Commit outcomes preserved.** Complete/Rejected/Incomplete remain distinct. Rejected leaves remediable staged work/diagnostics; Incomplete retains saved work, staged work, identities and diagnostics for remediation/resubmission of the same acquisition. Fault injection demonstrates applicable failures and retries. No new rollback prerequisite or intentionally split constitution is introduced.
8. **Duplicates, concurrency and ambiguous responses.** Repeated clicks, competing local attempts and response loss recover the original allowed outcome or an explicit conflict/incomplete/unknown result. They cannot create a second PersonAgent lineage/association as a retry strategy. An unavailable or ambiguous authoritative query cannot trigger fresh acquisition; committed historical association remains authoritative even if a current prospective inverse appears empty.
9. **Durable retirement and minimal restart recognition.** After completed constitution, restart rediscovers the same Agent/Space association and cannot reissue acquisition-only authority, even when the technical author retains invocation rights. Missing credentials deny privileged execution without erasing sovereignty or offering reacquisition. This is the minimum restart/retirement proof for AS2-C, not a claim that full authorized Open or Navigator is delivered.
10. **Bounded user-visible result.** Through explicitly inventoried constitution-result/identity reads, Welcome can show that constitution completed or explain the supported blocked/remediation outcome. Unsupported operational Dancers, mutations, generic dispatch and Navigator actions remain unavailable or protected. No standing bootstrap/admin bypass results from successful constitution.
11. **Real-boundary evidence.** Proposed AS2-C scenario labels are ConstitutionHappyPath, RejectedRemediation, IncompleteResubmission, DuplicateAndConflict, LostResponse, RestartRetirement and UnauthorizedConstitution; these are planned acceptance cases, not existing test identifiers. Before enablement, map them to actual IPC/runtime/zome entrypoints and real tests. Use fresh references and process/conductor restart where claimed; reference shared mechanism suites without duplicating them or treating mocks as proof of actual admission.
12. **Review scope and closure.** Record exact source/dependency revisions, supported configuration, security assumptions, passed checks and limitations. All first-constitution requirements above must pass or the PR remains draft/not merge-ready. The PR references #870/#872 as partial delivery; it does not close either milestone or claim complete CS-L1, production readiness, authorized Navigator, Upgrade or AS3 personalization.

##### Execution and review sequence

1. Review this decomposition/AS2-C acceptance contract and resolve only the remaining concrete custody, authority-binding and shared history/enforcement handoffs in their owning specifications. Publish exact dependency/test mappings; do not reopen approved authority/ontology decisions.
2. Finish AS2-P and the bounded shared key/relationship/validation and CS-L1.1/2 prerequisites. They may proceed independently where dependencies permit. A prerequisite PR must state its contract, consumer, negative evidence and remaining feature limitations explicitly; no requirement to merge an arbitrary checkpoint.
3. Deliver AS2-C together with the necessary CS-L1.3 integration and acquisition-specific Commit/retry evidence. This is the next feature PR target; judge it by actual constitution rather than preparation volume.
4. Deliver AS2-O with CS-L1.4 and a closed list of authorized Navigator operations, then AS2-U with its actual compatibility transition. These complete the broader AS2 lifecycle and bounded CS-L1 integration. Only then close the parent issues if all their requirements are satisfied.

**Tracking reconciliation still required:** #870 and #872 contain older commitment wording about full-write-set/physical atomicity that must be aligned with the accepted Complete/Rejected/Incomplete remediation/resubmission contract. #870 also retains the superseded candidate completion-record/unfinished-predicate language and stale pinned document versions. Propose targeted issue edits after this workplan/PR contract is reviewed; this pass changes neither issue body. No new shared issue identifiers, guarantees or delivered revisions are invented here.

#### AS2-owned implementation

1. Refactor the existing bootstrap/import lifecycle into explicit Provision/Open/Upgrade. Preserve existing TransactionContext, Reference Layer and transport binding paths. Recheck `core_schema_bootstrap.rs`, `space_imports.rs`, `ensure_core_schema_space()` and guest completion/index handling on the implementation baseline; do not create a competing bootstrap.
2. Provision one unclaimed ordinary HolonSpace with packaged local CoreSchema and Agent Spaces. Reconcile `MAP.CoreSchemaSpace` naming/key assumptions without replacing/retyping the space, duplicating content or requiring a descriptive-property rewrite. Display identity may be presentation-only.
3. Provide foundational Welcome and scoped definition imports. Request constitution authorization through the CS-L1 contract; do not implement credential issuance/custody or a capability framework in AS2.
4. Deliver the canonical HasInterior Lineage-binding schema delta, retaining definitional status and derived IsInteriorOf. Declare Home Space and historical continuity requirements using the approved shared mechanisms. General evaluators and binding-aware traversal are prerequisites, not AS2 implementations.
5. Orchestrate one complete constitution: stage PersonAgent in its intended Home Space, declared HasInterior and required authorization/completion effects using ordinary bound references and transaction APIs. Consume shared admission, validation and commitment results. Do not intentionally split Agent creation and acquisition into separate completed transactions or author the inverse independently. Preserve partially saved work and diagnostics on Incomplete; remediate and resubmit the same acquisition with retained identities.
6. Use committed IsInteriorOf as completed constitution, preserving authored HasInterior and the owning lineage lookup contract. Integrate conflict/interruption/retry outcomes through existing persisted-state queries; no completion artifact, Recognized state or read-time acquisition revalidation. Keep current authorization/compatibility and legitimate provisioning/loading checks distinct.
7. Integrate durable acquisition-privilege retirement and authorized runtime reconstruction through CS-L1. Admit the built-in House Troupe under the approved containing-space policy, not a supplied identity or author key. Enumerate required supported operations in the CS-L1 integration inventory; no general membership/role engine, negotiated Agreements or TrustChannels. All exposed privileged operations require authorization; unsupported paths remain unavailable/protected.
8. Implement valid-credential Open/restart and explicit supported Upgrade transitions. Preserve Agent/Space/content identity; reject unsupported or incompatible transitions safely. Do not claim an upgrade protocol from an initial import or no-op. No general migration framework or credential recovery is required.

There is no persistent Active sovereignty transition. Closed/Opening/Ready/Closing remains runtime state.

#### Explicit minimum dependencies

These labels identify bounded work, not newly created GitHub issues. Owners must link delivery issues and verified revisions before the corresponding path is enabled.

| Dependency | Owner and minimum handoff | Broader work outside the dependency |
| --- | --- | --- |
| [CS-L1 #872](https://github.com/evomimic/map-holons/issues/872) | [Client Security plan](../security/map-client-security-impl-plan.md#minimum-operation-inventory): approved local trust contract, scoped constitution, credential custody, durable retirement, opening/restarting the same acquired AgentSpace and only the finite operations mapped to AS2-Local-Lifecycle, with security evidence for one supported configuration | General Dancer authorization, arbitrary delegation, WeSpace roles, universal policy engine, adaptive risk, rotation/revocation, credential recovery and TrustChannels |
| Local acquisition commitment | Existing shared Commit contract: preserve Complete/Rejected/Incomplete, saved work and diagnostics; verify acquisition remediation/resubmission, paired inverse completion, conflicts and committed-state retry queries without duplicate identities or associations | Rollback redesign, new transaction subsystem, completion artifact, general journal or cross-cell coordination |
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

### AS2 delivery increment — state-aware packaged Welcome (2026-11-16)

The packaged startup path now observes saved Space/foundation/sovereign-association evidence and projects it through restricted Welcome. Initial loading, foundation-present, recorded sovereign association and unavailable/ambiguous evidence remain distinct. A recorded association hides the constitution action; neither a saved Space nor an empty current inverse collection establishes acquisition eligibility or authorizes reopening. Missing foundation or lookup failure blocks without replaying imports or replacing identities. Packaged startup failures retain the Welcome window with admission closed.

The [CS2/CS3 initial admission contract](../security/map-client-security-impl-plan.md#state-aware-welcome-and-initial-admission-contract--2026-11-16) resolves the target internally through the configured runtime and accepts no caller-selected IDs, keys or bootstrap flags. No usable constitution credential is issued and the action remains disabled pending protected custody, shared acquisition prerequisites and durable authorization/retirement. State-aware presentation is delivered independently of those prerequisites; no new constitution-completion artifact, validator or Commit semantics is introduced.

The current engineering `npm start` path uses ordinary conductor startup rather than the cache-reset/test-key optimization. Its main window is created after provider/runtime initialization and before schema loading, so its existing UI can display startup progress. It continues to be a development configuration and is not evidence of packaged sovereign authorization. The supported packaged flow will converge on Welcome for initial constitution and Navigator after authorized Open; general navigation/mutation authority is not implied by CS-L1's existing finite lifecycle inventory.

**Increment evidence:** 34 host tests and 3 actual-page-script tests passed; web typecheck, Rust formatting and unsigned packaged app build passed. The native-conductor test verifies missing-foundation denial and saved Space/current-inverse observation across restart without import replay. Live packaged inspection verified initial Welcome status and disabled constitution; retained-state opening was stopped before conductor initialization finished, without resetting data. Historical eligibility, credential custody, acquired-space authorization and terminal packaged Open remain explicit enablement/evidence gates. See the Client Security plan for the detailed limits.

### AS2-P delivery — bounded first-space foundation (2026-11-16)

The supported packaged path preserves the existing provisioning mechanism. The guest writes `LocalHolonSpace` only after a Complete bootstrap Commit. Host startup now also requires the actual LoadHolons `LoadCommitStatus` to be Complete before advancing. Rejected, Incomplete and transport/error outcomes retain ordinary transaction/result state for diagnostics and supported remediation/resubmission; no rollback or new completion artifact is introduced.

Provision loads the fixed configured definition imports through the existing loader. Open adopts the existing local Space, checks the expected Core identity and reads the 31 packaged Agent Spaces/Navigator definitions and their required type/declared memberships through ordinary references. It does not replay imports, activate a Dancer, create a replacement Space or interpret an empty sovereign inverse as acquisition eligibility. Missing/incompatible definitions block for explicit remediation/Upgrade. Existing Commit remediation and retained identities remain authoritative.

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

AS2 owns AgentSpace behavior and integration. Client Security owns shared authorization/assurance; transaction, relationship, key and validation mechanisms remain separately delivered dependencies. The ownership ledger and minimum dependency table above replace accumulating general mechanism design in the lifecycle issue. At this reconciliation, constitutive evidence representation remained open; design v0.9 subsequently settles it as committed IsInteriorOf, with no dedicated record type.

## AS2 first implementation slice — 2026-11-15

Independent first work: read-only discovery of the executing cell's existing local-space index through ordinary runtime/reference/Dance layers; adopt that identity before choosing Provision versus Open; avoid replaying configured create imports on Open. Missing designation permits initial provisioning only when no authored application footprint exists; ambiguous, broken or unreadable designation must fail closed rather than create a replacement. Finding a Space does not establish acquisition or grant authority. Preserve AS1 TDL and the type-free name key; the separately approved HasInterior Lineage delta remains pending shared validation/traversal.

Implemented evidence covers discovery before provisioning (no state created), adoption by a fresh host runtime, retained Space/content identity and error-versus-absence handling. The startup Core-key check and AS2-P fixed definition checks do not claim the full bootstrap manifest graph predicate; retain that separately owned bootstrap work as an explicit readiness gap. AS2-P reuses the existing guest-side rule that publishes the local designation only after a Complete bootstrap Commit, without adding a full-manifest audit to ordinary Open. Loader recovery must distinguish successful loading from interrupted packages without a general resolver or a global schema-readiness marker. Existing-package presence alone is not proof of complete loading. Future readiness is dependency-driven/per-Dance; no speculative distributed registry is implemented.

The existing two-pass Commit deliberately retains successful persistence and returns Incomplete with diagnostics when other writes fail. This accepted behavior supports remediation and resubmission; it is not a defect or a shared rollback prerequisite. Verify acquisition using those semantics: preserve saved identities and associations, retain correctable work, complete missing effects on resubmission and avoid duplicate constitution. A persisted IsInteriorOf remains sovereign evidence; incomplete onboarding does not supply missing operational authorization. Reuse existing Dance execution placement and verify the executing cell/Space; do not introduce another ExecutionContext framework.

CS-L1 authorization and historical/lineage enforcement remain dependencies. Acquisition must integrate and verify existing conflict/retry behavior; no general Commit redesign is implied. Independent lifecycle work may proceed; do not enable acquisition or new privileged operations. Retrospective recognition, TransactionWarrant infrastructure, global activation markers, general roles, additional cells/DHTs and speculative Upgrade frameworks remain deferred. AS2 owns lifecycle integration; shared owners supply their mechanisms and evidence.


### Earlier next-step note — superseded by the reconciled implementation units

The earlier sequence prioritized the [Client Security implementation contract](../security/map-client-security-impl-plan.md#repository-grounding-and-implementation): map the finite lifecycle inventory to actual Tauri IPC, Rust runtime and conductor/zome entrypoints; establish backend admission, credential custody, eligible-Space scope, retirement and restart checks under the approved packaged-Welcome boundary. Verify denial through alternate callers, untrusted content and supplied identity/bootstrap flags. Independent native confirmation and a new credential framework are not prerequisites. This remains a shared security handoff consumed by AS2; it does not broaden AS2 or replace existing Commit semantics. The reconciled AS2-P/C/O/U units and prerequisite matrix above now govern sequencing: CS-L1 is not one opaque prerequisite that must finish before AS2 begins. Required key, relationship/lineage, validation and acquisition-retry evidence remain explicit parallel handoffs.
