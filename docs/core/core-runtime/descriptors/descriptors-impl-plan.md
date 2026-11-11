# Descriptor Implementation Plan

## Current consolidation status — November 4

All five consolidation units are implemented on branch
`833-prepare-space-navigators-initial-visualizer-composition-and-eliminate-repeated-selection-reads`:

| Unit | Delivered behavior | Checkpoint |
| --- | --- | --- |
| 1. Commit registry ownership | Transport agent and registry-owner transactions separately; restore them in one guest space; rebuild exact-ID indexes once; ordinary acquisition reuses received results; graph-copying carrier removed | `887f0f3d` |
| 2. Frozen validation reuse | One assessment-owned scope reuses staged/transient products through ordinary acquisition and retires on every exit | `887f0f3d` |
| 3. Consumer adoption | Existing ValueType/PropertyType validation, classification, operator, and eligible compatibility consumers use shared payloads; foundational kernel primitives retain explicit recursion breaks | `887f0f3d` |
| 4. RelationshipType policy | Derived direction-specific policy; exact descriptor/policy association accompanies guest membership retrieval; host policy checks remain local; auxiliary policy/source-type tables removed | `36d72365` |
| 5. HolonType consolidation | EffectiveHolonDescriptor specializes DerivedDescriptor; private typed HolonDescriptor memo; common Session/frozen-scope retirement; prepared lineage/Instance TypeKind; generic command admission guards | `96975f3a` |

The [runtime payload inventory](descriptors-design-spec.md#1410-derived-payload-inventory-by-descriptor-kind)
is authoritative for HolonType, ValueType, PropertyType, and RelationshipType.
[Space Session](../space-session-design-spec.md) owns lifetime/reset;
[saved-Holon caching](../saved-holon-cache-design-spec.md) owns retrieval and residency.
No SmartReference or StagedHolon lifecycle field was added. Reset retires registered
derived state only; normal cache policies continue to govern relationship inputs.
Plural-only advisory warming, duplicate/provenance preservation, maximum-zero
navigation omission, and exact saved-version identity remain intact.

Verification at the unit-5 checkpoint: 997 unit/schema tests, all three focused
conductor scenarios, guest WASM checking, schema regeneration checks, release
hApp/probe packaging, artifact audit, and formatting passed. The complete `npm test`
sequence and PR review/verification remain outstanding; focused checks do not
substitute for those gates.

The post-clean manual run completed Canvas startup in **94.944 seconds**, compared
with **196.011 seconds** in the preceding slow run. The fresh run had 429 SDK
commands, 299 guest calls, and 169 relationship queries; relationship-name counts
matched the pre-unit-5 profile. This returns to the preceding roughly 89–95-second
baseline and does **not** demonstrate a unit-5 startup speedup. See
[measurements and caveats](../../performance/startup-and-canvas.md) and
[retained evidence](../../performance/evidence/2026-11-04-step5/README.md).
EHD constructor finalization, including SmartLink persistence, remains a separately
measured cost. Visualizer selection redesign remains separately scoped; this
consolidation does not claim to resolve its startup cost.

The dated sections below record intermediate states. Their “pending,” “uncommitted,”
and verification statements apply to those checkpoints, not this current status.
The original issue/PR scope below is historical and does not assert current GitHub
issue disposition or merge status.

## Original scope and authority (historical)

[Issue #838](https://github.com/evomimic/map-holons/issues/838) and
[PR #844](https://github.com/evomimic/map-holons/pull/844) now include the session
ownership and registry work originally recorded in
[#841](https://github.com/evomimic/map-holons/issues/841). These are one delivery
unit before merge. The separate registry implementation commitment is absorbed;
this document does not claim that GitHub issue disposition has already changed.

The [runtime specification](descriptors-design-spec.md#141-effectiveholondescriptor-canonical-definition)
owns EffectiveHolonDescriptor acquisition, preparation, and lifetime. The
[schema specification](../../type-system/schema-design-spec.md#85a-effective-descriptor-result-schema)
owns the result contract; the [kernel rules](../../type-system/descriptor-semantics-rules.md#3-job-two-compute-effective-semantic-inheritance)
own inherited declaration semantics. Implementation code remains in map-holons.

## Original baseline and revised target (historical)

The pre-revision code baseline is `c7a07019`. It implements EffectiveDescriptor,
guest construction, caller-retained results, per-view DAHN acquisition,
read-time direction classification, direct-product normalization, and a cache
that can perform expensive first-use policy discovery. That baseline is not the
revised target and must not be described as completing this plan.

The revised design uses the concrete name EffectiveHolonDescriptor across Rust,
schema, Dance/Commands boundaries, SDK, and docs. Public acquisition is a method
on ReadableHolon exposed by a Holon-scoped Command. Session owns saved-schema
registry entries and their restricted retained transaction. Inherited members
accumulate without duplicate checking or normalization; validation rejects
repeated declarations, and ordinary consumers trust validated uniqueness.
Prepared final cache policies make instance caching strictly local. Public
navigation exposes outbound relationship identities without declared/inverse
classification. The wrapper retains exactly one self-resolving HolonReference;
`described_instance` and a descriptor trait-object API are deferred.

Existing verification of the baseline includes 586 core unit tests, 23 client
tests, 369 SDK tests, 58 schema tests, host/WASM/web checks, and formatting. The
retained-result integration test passed locally in 105–111 seconds and on
`7cd21408` CI in 330.853 seconds with the unchanged 600-second limit. These
results are historical baseline evidence, not verification of this revision or
guarantees about construction/startup latency.

## October 30 navigation partition checkpoint

The follow-up in map-holons [commit 8569d47b](https://github.com/evomimic/map-holons/commit/8569d47b)
implements guest-prepared singular/plural navigation, duplicate-preserving composed
access, maximum-zero omission from navigation, and unchanged declared contracts
and instance lifecycle filtering. Complete structural navigation identities and
provenance retain their original alignment independently of partition order.
TDL, generated imports/bootstrap resources, Commands/wire, SDK, and DAHN consumers
are reconciled. Native, schema, SDK/UI, host/WASM, and real-conductor retained-graph
checks passed locally. This is evidence for this bounded follow-up, not a new
status audit of every historical implementation step below.

See the [DAHN performance record](../../hx/dahn-implementation-plan.md#observed-startup-performance)
for the measured removal of 59 frontend cardinality commands and remaining
selection/materialization costs.

## Plural navigation cache population follow-up

The plural navigation accessor now calls the errors-only `ensure_cached` capability
with distinct saved target IDs. Its output remains the original occurrence list;
staged and transient targets are excluded from warming. Singular-only availability
reads its own partition rather than traversing combined navigation first. A typed
Holon read command carries SDK plural navigation through the Rust accessor.
Consumer regressions cover duplicate preservation, mixed reference phases, cache
reuse, failure/retry behavior, and singular availability isolation. The measured
startup benefit remains to be established by a fresh application profile; the
previous per-target fetch cost is an opportunity estimate, not a claimed saving.

## Implementation sequence

1. **Rename and contract inventory.** Rename EffectiveDescriptor to
   EffectiveHolonDescriptor, including well-known names, result type and paired
   schema identities, construction Dance/request/response/implementation names,
   Rust APIs, Commands/wire binding, SDK handles, tests, and bootstrap assets.
   Generate schema JSON through map-schema. Keep runtime package dependencies
   on Core, Dance, and Commands and all nine directly licensed effective collections, including both navigation partitions.
   Preserve retargetable imports; supply OwnedBy during runtime allocation.

2. **Lossless inherited products.** Reuse the existing target-lineage and
   ComputedEffectiveSchema substrate. Resolve the target lineage once. Accumulate
   all selected additive declarations in ancestor-before-local order; preserve
   each local sequence. Remove normalization and duplicate checking from
   constructor population, public reads, and shared accumulation. Repetition
   must survive staged/candidate projection so validation can reject it. Retain
   Local and nearest-nonempty Override semantics, including singular-access
   errors for malformed key-rule selections. Navigation discovery may still
   union identical references reached through different discovery paths; it must
   not conceal repeated authored declarations in inherited products.

3. **Session ownership and registry (absorbed #841).** Extend RuntimeSession with
   the minimum shared-core/session capability accessible through references and
   services, without upward dependencies from core into host Commands. Strongly
   retain a restricted derived-state transaction and registry. Enforce no stage,
   persistence, Commit, public mutation ingress, undo/redo, or public recovery.
   Key saved entries by exact type identity, isolated by session/space. Exclude
   staged/transient projections. Coordinate concurrent misses without holding
   locks across graph reads or guest execution; publish only completed sealed
   results, release failed reservations, and permit retry.

   Preserve self-resolving owner identity across Commands and host/guest
   transport. Never reinterpret a session temporary ID under a public TxId.
   Public disposal leaves registry results intact; explicit session teardown
   ends access. Avoid ownership cycles and unbounded construction-envelope
   retention. Registry hits allocate no result and make no construction call.

   Commit registry transport is revised by the November 2 consolidation sequence
   below: transport the retained registry-owner transaction separately from the
   agent transaction, restore both in one guest space, and rebuild registry indexes
   once. The earlier cross-transaction graph cloning is transitional implementation,
   not the target. Enforce saved-only dependencies in the Session partition and
   keep frozen candidate products in the validation scope. See runtime §14.8.

4. **Rust-owned public acquisition.** Add
   `ReadableHolon::effective_descriptor() -> Result<EffectiveHolonDescriptor, HolonError>`
   and a Holon-scoped Command. Resolve the source's exact describing type in
   Rust, then route to session find-or-construct or candidate-local acquisition.
   Keep an internal type-oriented operation for consumers already holding a
   HolonType definition; do not accidentally acquire its meta-type's schema.
   Host misses construct through HolonServiceApi and the guest Dance; guest
   execution invokes the local shared algorithm without delegating again.

   Replace the old transaction-construction command as the ordinary public
   acquisition surface. The construction Dance remains internal preparation
   machinery. The SDK forwards and binds an opaque owner-correct handle; remove
   TypeScript type lookup, implementation choice, and per-view schema caching.
   Explicit reconstruction/pull is intentional and distinct from ordinary
   acquisition. It replaces selected registry state without mutating old results.

5. **Move effective-schema methods by semantics.** Migrate inherited properties,
   relationships, constraints, bindings, key-rule selection, affordances, and
   named lookup/helpers from HolonDescriptor and ReadableHolon to
   EffectiveHolonDescriptor. Inventory `instance_*`, `afforded_*`, lookup, and
   contract helpers as well as `effective_*` and `available_*`. Preserve generic
   ToPropertyName/ToRelationshipName/ToDanceName/ToCommandName conveniences on
   the concrete wrapper. Keep authoritative/local reads explicit and delegate
   unrelated metadata reads without triggering migrated inheritance work.

   Remove competing public paths. Internal kernel primitives remain available
   for constructor/bootstrap prerequisites and validation of other descriptor
   categories; they are not another ordinary caller API. Construction and its
   own request validation must not recursively acquire another descriptor to
   satisfy the same acquisition.

   Apply this inventory to query authoring, predicates, ordering, expansion,
   reference availability, and semantic comparison as well as presentation.
   Structural prerequisites (default population, schema cloning, mutation
   classification, and invocation/command-scope binding) may reuse an already
   published product without initiating construction; their bootstrap fallback
   remains internal. Candidate validation shares assessment-local computed
   products and already-diagnosed lineages. Commit graph-only overlap checks
   consume those prepared products; persistence retains one projection per
   committed source and can restore it from the shipped snapshot.

6. **Relationship-owned cache policy.** Establish the RelationshipType derived
   payload and embed acquisition in RelationshipDescriptor's policy accessor.
   Resolve the exact outbound descriptor when establishing a membership entry,
   retain its small final policy value, and remove the auxiliary authoritative
   policy table. A usable hit must remain a direct policy check. Preserve
   foundational bootstrap policies, direction-specific semantics, lock/reentrancy
   boundaries, freshness hints, and existing membership lifetimes. See the
   November 2 sequence below for delivery status and measurement gates.

7. **Navigation and availability.** Make navigable_relationships a read of
   prepared outbound references. Remove eager per-member direction classification
   and public QualifiedRelationship direction flags from Commands/SDK results.
   Replace UI `direction + name` keys and comparisons with exact/opaque
   relationship identity. Rust exposes navigability and updateability separately;
   the UI does not derive them from declared/inverse status.

   Preserve the existing uncommitted-instance availability restriction in Rust
   using prepared/local metadata, without a second target-lineage traversal or
   wholesale relationship classification. Determine the replacement internal
   availability operation from its actual consumers. Do not add
   `described_instance` to the wrapper or runtime schema and do not retain the
   old effective-resolution entry points merely to keep this filtering helper.

8. **Above-PVL validation adoption.** Reuse effective products for semantic
   validation rather than walking Extends independently per rule. Keep candidate
   schema and evidence local to the assessment; saved entries cannot replace
   staged edits or implicitly select successors. Repeated target declarations
   remain present for validation and diagnostics. Lightweight declaring-origin
   information comes from the same computation, without contribution holons or
   another target-lineage walk. Do not validate source schemas or generated
   result/response bodies during construction. Preserve the bounded explicit
   endpoint accommodation and minimal structural prerequisites.

## Verification gates

- Accumulation: inherited/local duplicate targets remain repeated; validators
  reject local repetition and ancestor redeclaration for additive schema members.
  Valid schemas produce unique products without read-time deduplication. Preserve
  distinct-identity/name-conflict evidence and Override behavior.
- Equivalence: all seven inherited products, semantic local order, declaring
  origins, exact saved references, structural errors, and navigation SourceType
  identity set. Staged discovery tolerates absent indexes without inventing them.
- Acquisition: one Holon-scoped request from the SDK, no TS schema coordination,
  no retired public bypasses, and preserved ergonomic name arguments. Reads of
  prepared products do not rewalk the target lineage or classify navigation
  members through their own ancestry.
- Registry: two independent callers/public transactions share one construction;
  public disposal preserves active-session results; successful saved-state Commit
  resets the Session while detached Commit copies remain execution-local; staged
  projections stay local; concurrent requests, failures/retry, reset, obsolete handles, session
  isolation, transport ownership, teardown, and bounded pool growth are tested.
- Cache: every instance-cache policy resolution is local, including first use,
  TTL expiry, RequireFresh, batching, empty results, and other instances of the
  same type. Count descriptor lookups and guest calls at this seam, not merely
  later cache hits. Test bootstrap without recursive preparation and adoption
  changes without incoherent cached membership.
- Navigation: no declared/inverse flag reaches presentation; identities preserve
  state across rebinds; committed/uncommitted behavior remains correct. Normal
  traversal and authorization continue through the reference layer.
- Validation: above-PVL consumers share products, preserve candidate defects,
  and do not recursively invoke construction. No contribution or policy-entry
  holons are allocated. Minimal structural safeguards remain active.
- Lifecycle: keyless result is sealed; wrapper has one self-resolving reference;
  correct owner disposal ends access. No persistent derived artifact or source
  descriptor clone is introduced.

Run focused core/runtime/boundary/SDK/UI/schema tests, host/WASM checks,
formatting, and guest-backed integration after implementation. Record cold and
retained acquisition, guest calls, policy lookups, lineage reads, construction
allocations, response size, and session-pool footprint. Compare full-flow costs,
not just constructor time. Do not raise timeouts to conceal repeated work.

## Separate work

[#843 LoadTheme](https://github.com/evomimic/map-holons/issues/843), Visualizer
Selection redesign, Theme validation delivery, Module-governed adoption, and
persistent effective artifacts remain outside this unit. This revision enables
shared schema use in those consumers without claiming their implementation.

## Space Session reset and derived-payload reconciliation

The [space Session specification](../space-session-design-spec.md) owns the
lifecycle contract. The [payload inventory](descriptors-design-spec.md#1410-derived-payload-inventory-by-descriptor-kind)
owns category-specific prepared state.

Implemented in the current working changes:

- HolonSpaceManager owns a shared retirement token and coordinates reset of
  registry selections. Relationship memberships, policies, and source-type
  resolutions retain their independent lifetimes and normal read semantics.
  Saved-node residency, exact version bindings, public transactions,
  staged edits, and Undo/Redo are preserved. Rebuilding is lazy.
- DerivedDescriptor results share their Session token; cloned/independent holders
  observe retirement. ValueDescriptor and PropertyDescriptor replace obsolete
  memoized handles and retry only that condition. Backing-holon access is
  crate-internal. Staged/transient sources do not enter wrapper/session caches,
  and candidate dependencies prevent admission even for a saved source.
- ValueType/PropertyType prepare effective Instance TypeKind anchor metadata,
  native value kind, lineage, constraints, bindings, operators, and declaring
  origins from one resolved lineage. Instance TypeKind is an optional index into
  the reference-backed lineage, not authored classification state. Operational
  read failures abort; readable semantic defects remain product-specific errors.
- Registered derived-result publication is guarded against retirement. Ordinary
  relationship fetches and their cache publications are not coupled to that token. Snapshot
  capture retries across reset; Commit-local copies remain detached, and response
  pools do not republish older results into the active registry. Guest validation
  can restore generic prepared lineage/constraints/bindings through its existing
  assessment preparation, without pretending the result is a HolonType projection.
  Missing assessment products retain request-local kernel computation. Foundational
  bootstrap classification remains independent of derived-schema availability.
- Host Commit completion resets after persistence acknowledgment. Rejected and
  demonstrably empty attempts preserve the Session; Incomplete attempts reset
  conservatively because persistence may already have occurred. Loading and direct
  DeleteHolon persistence also reset. Reset failure after persistence is reported
  distinctly and leaves stale Session state retired.

At this pre-consolidation checkpoint, EffectiveHolonDescriptor migration remained
deferred (superseded by unit 5 below). Reset cleared its selected
registry entries, while policy resolutions remain governed by their existing
lifetime. Previously returned HolonType handles retain their
existing readable lifetime. The shared carrier remains allocated rather than
being disposed underneath capture/construction. Retained old HolonType products
remain admitted until registry teardown under this interim contract. Migration
must replace that retention policy with the shared retirement contract rather
than making it a permanent exception.

Verification covers refreshed fake persistence inputs, exact anchor identities,
one lineage traversal, staged preservation, direct obsolete reads, wrapper
recovery, captured-graph survival, late derived-publication rejection,
reset-overlapping capture, and successful/empty/rejected/partial Commit behavior.
Real-conductor verification and native/WASM/schema gates are recorded with the
implementation report; these changes do not establish an application performance
improvement. Measure reset frequency and reconstruction cost, particularly for
background Usage persistence, before considering exceptions to the blanket rule.

### November 2 verification checkpoint

The affected native/core/validation/selection/type-name suites and schema gates
passed 1,039 unit/inventory tests. Both conductor-backed descriptor scenarios
passed; the ValueType/PropertyType scenario additionally exercises an actual
HolonSpace candidate rejected for missing required properties, correction in the
same transaction, successful guest persistence, automatic host Session reset,
wrapper reacquisition, and retained readability of a detached captured graph.
WASM workspace checking and release hApp build/packing passed. Changed Rust
sources were formatted and both repository whitespace checks passed. The full
npm test sequence and manual UI/startup profiling have not been run for this
checkpoint; no runtime responsiveness improvement is claimed from these checks.

### Derived-only reset correction

The earlier input-cache clearing and membership-publication token guards have
been removed. Reset retires only registered derived state. Reacquisition trusts
existing Reuse, Fresh, bounded-age, and explicit freshness-hint behavior; it does
not force a different membership observation. Tests cover cached Reuse membership
surviving reset, Fresh reads fetching again, bounded entries surviving until expiry,
in-flight reads completing normally, and policy/source-resolution generations
remaining unchanged. The earlier verification checkpoint predates this correction;
its test counts are historical, not the final verification of this narrower change.

The narrower implementation passed 783 affected core/client/runtime unit tests,
WASM workspace checking, release hApp build/packing, and the focused real-conductor
ValueType/PropertyType rejection/correction/Commit-reset scenario (107.83 seconds).
Whitespace checks passed in both repositories. Relationship-cache implementation
files match their pre-Session baseline; no application performance gain is claimed.


## November 2 consolidation design and delivery sequence

The design below defines the agreed delivery sequence; dated checkpoints below
record implementation progress. It supersedes the earlier
Commit graph-copying carrier and fresh-on-every-access policy for frozen mutable
inputs. Historical verification above establishes neither completion nor performance
of this revision. The normative contracts are runtime §§14.6–14.10 and the
[space Session specification](../space-session-design-spec.md).

### Gaps observed on November 2 (historical)

- ValueType and PropertyType have DerivedDescriptor-backed accessors; HolonType
  retains its separate reusable EffectiveHolonDescriptor. RelationshipType has no
  migrated derived payload. HolonType is not wholly without prepared-state reuse.
- Some consumers still bypass prepared products. In particular Commit value
  assessment/binding compatibility classify native kinds independently, query
  compatibility walks ancestry, and structural diagnosis repeats across phases.
- Staged/transient derived access currently reconstructs on every acquisition;
  the frozen validation reuse scope is not implemented. Broadly switching validation
  to those accessors first could increase full-payload construction during bootstrap.
- Host Commit currently clones registered results into the agent pool. Explicit
  guest validation lookup finds them, but ordinary saved accessor acquisition
  chooses a new construction context: guest ingress has not attached the received
  registry to the guest space. Transport works; discovery/ownership is disconnected.
- Background successful Usage commits intentionally retire the saved-derived
  Session under the agreed blanket rule. That is distinct from a lookup defect;
  retain the rule unless later measurement warrants reconsideration.
- November 2 UI startup: 83.497 s versus a comparable 82.934 s prior run, with 425
  SDK commands in both. DescribedBy/close/repeat: 74.120 s then 8.746 s; accumulated
  selection durations fall from 56.593 s to 0.017 s for 23 calls in each.
- Correlated Rust foreground request spans show 313 guest calls on first navigation
  and 32 on repeat. The repeat includes nine ValueType queries reporting unresolved
  `policy: None`, nine key lookups and three canonical calls. None is not an absent
  required policy property: omitted optional maximum age resolves to Fresh. A
  background Commit completed between navigations, but the log does not directly
  record retirement. Accumulated command/transport durations are not additive
  portions of wall time; these observations do not prove a causal DD speedup.

### Ordered implementation units

1. **Restore registry ownership/discovery on Commit.** Transport the agent and
   registry-owner transaction states distinctly, with the registry root identity.
   Restore them in one guest space, attach the registry with its retained owner,
   and reconstruct descriptor-ID indexes once from transported transient results.
   Require no storage/Extends reads for indexing. Retire cross-transaction cloning
   and preserve ordinary accessor acquisition. Ordinary requests do not ship/rebuild
   this extra state. Test EHD/DD saved-accessor hits, exact source/owner identity,
   capture across host reset, and no stale registry republishing on response.
2. **Enable frozen validation reuse.** Enter the TransactionContext-owned scope
   before preparation; retire on success, rejection, and operational error. Register
   staged/transient products by exact transaction-local identity. Share completed
   results across independent wrappers, while allowing derived output construction.
   Preserve fresh behavior outside validation, obsolete-handle recovery, saved vs
   predecessor distinctions, and fresh edited retries. No new SmartReference or
   StagedHolon fields or generic per-mutation invalidation machinery.
3. **Complete existing consumer adoption.** Convert native ValueType classification,
   constraints/bindings and eligible query compatibility to normal descriptor
   accessors. Reuse diagnosed lineages and assessment-local structural evidence;
   do not remove malformed-graph diagnostics or foundational recursion breaks.
   Validation packages retain diagnostics/projections, not a second acquisition API.
   Prove units 1–2 with a small real-Commit consumer conversion before expanding.
4. **Add RelationshipType derived policy and consumers.** Acquire final policy through
   RelationshipDescriptor. Resolve the exact declaration at cache-entry establishment,
   keep direct scalar policy checks for hot hits, and retire the auxiliary table.
   Prove repeat ValueType reads have a resolved policy and retain/fetch memberships
   according to it; do not force Reuse or flush existing caches. Preserve recursion
   breaks, explicit freshness, and declared/inverse differences.
5. **Migrate EffectiveHolonDescriptor.** Consolidate HolonType acquisition/lifetime into
   the proved design without changing navigation partitions, maximum-zero exclusion,
   duplicate/provenance behavior, key-rule identity, or ordinary consumer semantics.
   Implemented on the branch in the November 4 consolidation below; it was not
   a prerequisite for units 1–4.

Keep units reviewable as separate commits. Use focused native/WASM and real-Commit
checks during development, then full manual verification at meaningful checkpoints.
Measure after unit 3 (bootstrap/Commit validation) and after unit 4 (cold/repeat
navigation). Record index rebuilding, acquisition/construction counts, scope reuse,
session resets, guest calls, policy misses and wall time separately. Unit 5 is
architectural consolidation, not an assumed performance improvement. Bootstrap
editing-time memoization and new Operator/KeyRule payloads remain separate work.

### November 3 frozen-validation implementation checkpoint

Consolidation units 1 and 2 are implemented in the branch working tree; the
pre-consolidation gaps above describe the prior foundation. Unit 2 enters a
TransactionContext-owned frozen scope before assessment preparation. Ordinary
ValueType/PropertyType acquisition shares completed mutable-source products by
staged/transient identity within that owner, independently of saved predecessor
identity and the saved-space Session. The shared scope token retires on every
assessment exit, including rejection and operational error; selected entries are
released, retained direct results report obsolescence, and corrected retries start
a new scope. Mutable access outside assessment still constructs fresh products.
Transient output construction remains permitted. No fields were added to
SmartReference or StagedHolon, and the scope is not transported or serialized.

Focused tests cover independent-wrapper reuse without new result allocations,
staged and transient inputs, retained-result retirement, edited retries, failed
construction, and actual assessment entry/exit on acceptance, rejection and error.
All 652 core and 137 validation unit tests pass, as do the hApp WASM workspace
check and normal release build/packing. The focused conductor-backed
`value_and_property_wrappers_reuse_guest_derived_products` scenario passed
(124.910 s), including real guest Commit rejection, correction, success and
saved-registry lifecycle behavior. Unit 3 consumer conversion, RelationshipType
payloads and EHD migration remain pending; these checks establish no performance
gain. Changes remain uncommitted.

### November 3 consumer-adoption implementation checkpoint

Consolidation unit 3 is implemented in the branch working tree. Commit value-kind
assessment and native binding compatibility now use ValueDescriptor accessors.
Preparation acquires complete ValueType/PropertyType products through the same
accessor path used during consumption, and retains only validation projections
and structural evidence in assessment packages. Saved-product eligibility is
per reference rather than an assessment-wide affected-Schema bypass.

Structural diagnosis is shared by exact definition across subjects, governors,
package preparation, role checks and declaration assessment. Valid mutable
lineages supply inputs to ordinary derived construction through the existing
frozen scope; they do not establish another acquisition authority. Malformed
lineages retain prerequisite findings and existing kernel error behavior.
Universal contract preparation and saved authored-surface checks consume the
already computed validation projection instead of rediscovering inheritance.

ValueType query compatibility uses the acquired lineage. Transient-contract
native classification uses ValueDescriptor and reuses an existing EHD when
available, while retaining non-constructing fallback during infrastructure setup.
Cold guest requests retain an empty ordinary saved-product registry when none was
transported; its owner/results are created on demand, remain request-local, and
are not republished to the host. Loader enum/default materialization remains a
low-level pre-validation path because it mutates inputs before the frozen phase.
Other descriptor kinds retain their kernel paths until their planned migration.

All 653 core and 138 validation unit tests pass. Regression checks prove no
Extends reread after diagnosed mutable-lineage retention, no further derived
allocations during frozen consumption, and no schema backend reads during saved
consumption. Construction may resolve the derived-result and registry carrier
types; native classification does not rediscover kind anchors. The WASM workspace
check and normal release hApp build/packing pass. Both conductor-backed descriptor
scenarios passed: retained sealed EHD graph (229.557 s) and ValueType/PropertyType
products with real Commit rejection, correction and success (109.258 s). These
are test durations, not application startup measurements. Manual startup/Commit
measurements now include a completed 76.957-second Canvas profile after consumer
adoption, compared with 96.870 s after unit 2 and 88.899 s before it. These single
runs do not isolate causality; see the November 3 observations in
[Startup and Canvas performance](../../performance/startup-and-canvas.md).
Units 1–3 were checkpointed in map-holons commit `887f0f3d`. RelationshipType policy
adoption (unit 4) is the next implementation unit; EHD migration (unit 5) remains
pending.

### November 3 relationship-policy implementation checkpoint

Consolidation unit 4 adds a private DerivedFields handle to RelationshipDescriptor
and a DerivedRelationshipPolicy product to the existing transient carrier. One
resolved lineage supplies relationship direction and the final Reuse, Fresh or
bounded-age policy. Declared-definitional membership reuses; omitted/zero age on
other membership resolves Fresh, and positive age resolves bounded reuse.
Semantic product errors remain explicit and operational read failures prevent
publication. Relationship construction leaves unused value/property collections
empty instead of fetching those unsupported products.

Guest-prepared policy projections use RelationshipDescriptor acquisition and
include complete declared instance contracts, including explicit meta-type
members omitted by endpoint-filtered navigation. Client policy binding combines
that contract with the descriptor source's own SourceOf indexes along its Extends
lineage; existing derived lineages are reused when available, with kernel paths
retained for unmigrated kinds. The two-hierarchy regression exposed both SourceType
and ValueType omissions in the first conductor pass. No navigation partitions
were changed. Distinct matching identities fail as ambiguous.

The auxiliary source-type/name policy table and source-type resolution map are
retired. Relationship-cache entries continue to retain a small scalar policy for
hot hits, expiry and explicit freshness. Session retirement does not flush those
entries. Foundational policies and active-construction recursion breaks remain;
an empty registry alone does not excuse an ordinary unresolved policy. Policy
binding can perform additional cold schema/index reads, so reduced guest-call
counts or startup latency require measurement rather than inference.

Verification: 657 core, 138 validation and 18 client unit tests pass, together
with 58 schema-tool tests, schema compile/check, the hApp WASM check and normal
release build/packing. The retained sealed EHD graph / Commit transport / pull
conductor scenario passed (310.712 s). Its duration is not a startup benchmark.
The targeted ValueType cache-hit / ValueTypeFor freshness / real-Commit scenario
remains unverified: after correcting the initial policy-binding omissions, three
attempts stopped in Holochain initialization with “agent info didn't make it to
the peer store,” before reaching descriptor assertions. No test-only capability
was exposed and no harness timeout/retry behavior was changed. An extra Cargo
retry was stopped during redundant dependency compilation and the existing
current test binary was used for the final two initialization attempts.

Manual startup and cold/repeat navigation measurements, the targeted conductor
scenario, and the full npm verification sequence remain pending. EHD migration
(unit 5) remains separate. Unit 4 changes are uncommitted.

### November 3 startup composition follow-up

Manual startup exposed a HasSlot declaration error after unit 4 tightened policy
resolution. The composition walker continued past Visualizer.HolonType into
generic HolonType/TypeDescriptor ancestors whose meta-type does not declare
HasSlot. Previously unresolved policy served those empty reads fresh and hid the
invalid request. Composition now processes the Visualizer family root inclusively
and stops there; inheritance within that family, role overrides and resolution
errors remain unchanged. No cache-policy fallback was added.

A saved-reference regression reproduced the HasSlot error on a generic parent
before the fix. Both the family-boundary regression and a control proving that
in-family resolution errors still propagate now pass, together with all 31
selection scenarios and 18 client unit tests. The hApp WASM check and normal
release build/packing pass. A focused conductor scenario loaded the real Core
Schema and discovered all eight HolonInspector slots and the PathInspector slot
without error (110.51 s including bootstrap; not a startup benchmark). DAHN design
now states the inclusive family boundary explicitly. A separate retry of the
previous ValueType cache/Commit scenario again stopped during conductor peer-store
initialization (11.65 s), before its assertions; that outstanding verification gap
remains. Full manual app startup remains to be rerun; changes are uncommitted.


### November 3 local policy-boundary correction

Manual verification of unit 4 recorded Canvas startup at 160.407 seconds versus
76.957 seconds after unit 3, first DescribedBy navigation at 98.747 seconds and
repeat navigation at 7.291 seconds. The client policy callback incorrectly acquired
EHDs and walked descriptor ancestry/SourceOf, introducing guest calls at what must
be a local lookup boundary. This was an implementation defect, not an accepted
first-use tradeoff.

The correction carries an exact relationship-version identity and its
RelationshipDescriptor-derived scalar with the existing membership response.
Guest retrieval binds the describing contract plus descriptor endpoint ancestry;
no host policy table or host schema walk is introduced. RelationshipCache retains
the association with its scalar, including for empty membership and Fresh policies.
Expiry and explicit freshness fetch targets without requesting descriptor rebinding.
Foundational and construction-internal reads retain their bounded local behavior.

A failing client regression reproduced schema discovery on a ValueType policy
lookup before the correction. Tests cover a single membership request through the
real client and wire JSON/binding path, zero guest calls on reuse, membership-only
explicit fresh reads, Reuse/Fresh/TTL retention, complete meta-type declaration
binding, an inherited inverse and ambiguity errors. Application latency after the
correction remains to be measured; passing these tests does not establish speedup.
Unit 5 remains pending.


Verification of the local policy-boundary correction: 658 shared-core tests,
138 validation tests, 21 client tests, 3 selection unit tests and 31 selection
integration tests passed (851 total). WASM workspace checking, release hApp
build/packing, explicit-file formatting and whitespace checks passed. The focused
real-conductor `value_and_property_wrappers_reuse_guest_derived_products` test
also passed (104.22 seconds including bootstrap). Its assertions cover ValueType
membership reuse, inverse freshness, derived-product acquisition/transport and
Commit rejection/correction/reset. That duration is a test-suite observation,
not an application startup measurement. Manual npm start timing remains user-run.
Changes remain uncommitted.


### November 4 HolonType consolidation (unit 5)

Implementation now specializes the common DerivedDescriptor handle for
EffectiveHolonDescriptor. HolonDescriptor has a private, nonserialized typed
DerivedFields memo; saved results share the registry Session token and frozen
staged/transient results share the transaction assessment token. The two result
partitions retain their existing payload and transport identities, while generic
private memo/scope helpers share acquisition and retirement behavior.

EffectiveHolonDescriptor.HolonType now extends DerivedDescriptor.HolonType.
Construction retains its already resolved lineage and prepares effective Instance
TypeKind without another Extends walk. Navigation partitions, maximum-zero
exclusion, duplicates, effective key-rule identity, prepared relationship policies,
and declaring provenance remain unchanged. Unrelated generic carrier collections
are empty. An explicit pull resets the whole Session and reacquires the exact
version; old direct semantic handles report ObsoleteSession and ordinary wrappers
replace their memo lazily. Command narrowing recovers the selected result's token.

Verification completed: 660 holons_core, 138 holons_validation, 117 command-runtime,
21 client, three selection-unit, and 58 schema-compiler tests pass (997 total).
The guest WASM workspace check, regenerated-schema check, release hApp/probe builds,
artifact audit, formatting and whitespace checks pass. All three focused conductor
tests pass: retained EHD construction/transport and exact-version pull; saved
visualizer composition boundaries; and ValueType/PropertyType plus HolonType reuse
across rejected and successful Commits. Those tests include generic command reads
of retired EHD carriers and independent guest snapshot lifetime. The full npm test
sequence remains outstanding. Subsequent manual app/performance verification is
recorded in the current-status section and linked performance evidence above;
it establishes no unit-5 speedup. The preceding guest profile located 1.203 s of a 1.364 s EHD constructor
in finalization (175 link queries); this consolidation does not claim to resolve
that separate measured cost.

The SDK's generic collection reads also pass through a local command-boundary
admission check for the registry owner. This closes a retirement bypass without
schema discovery or storage reads. Reset clears the admission set for all results
of the retired Session, including superseded publications, rather than walking
only currently selected results. The same shared Session token guards the whole
read operation. Trusted typed narrowing recovers its selected token; arbitrary
narrowing retains its existing type validation. An unpublished construction
carrier is not a public read capability.


## Selective Commit retention follow-up — November 6

[map-holons #853](https://github.com/evomimic/map-holons/issues/853) follows the
consolidation delivered in PR #846. It replaces the blanket successful-Commit
reset trigger with the guest's conservative persistence-effect verdict. Preserve
existing host EHD/DD results across proven descriptor-independent Complete
Commits; retain whole-Session reset for affecting, partial, or uncertain effects.
The Space Session specification and descriptor input inventory define the revised
target contract; earlier blanket-reset checkpoints above remain historical.

Implementation uses the existing CommitResponse carrier, a descriptor-owned
in-memory effect accumulator, and both directions of existing semantic SmartLink
persistence. Track newly published exact identities separately from graph-only
SavedHolons. Cover the full Nursery retry scope and conservative response failures.
No classifier storage reads, registry scans, or extra lineage walks are permitted.

Verify retained EHD/DD identity after instance creation/versioning and ordinary
relationships; input-family and inverse SourceOf reset; fresh-vs-retry identity;
missing/malformed verdict and uncertain outcomes; current-Session retirement
across overlapping reset/acquisition; unchanged relationship-cache policies; and
native/WASM/schema plus targeted real-conductor execution. Record matched reset,
construction, and guest-call evidence rather than infer a timing improvement.

This is independent of #822's preparation-demand narrowing. Guest-to-host registry
return is addressed by the bounded follow-up below. Frozen validation-only product
promotion remains deferred. No new numbered roadmap PR unit is inferred. Implementation is checkpointed in [map-holons commit 0f19ac39](https://github.com/evomimic/map-holons/commit/0f19ac39) on the existing 852 branch;
verification evidence follows. No merge or issue-completion claim is made.


### Selective-retention verification checkpoint

The implementation carries DescriptorResetRequired on the existing CommitResponse
holon. It defaults to true and is finalized from the descriptor-owned effect
accumulator only after Complete persistence. The host preserves proven safe
results and retires the current Session for affecting, partial, malformed, or
uncertain outcomes. Failed transport retains its original error; acknowledged
persistence retains the distinct CacheResetAfterCommit failure contract.

Verification: 704 existing core tests, 21 client tests, two additional constructor
inventory tests, and 58 schema compiler tests passed. The hApp WASM check,
production/probe artifact audit, TDL validation/generated-import roundtrip,
bootstrap import/digest/package consistency, and repository formatting passed.

The real-conductor value/property scenario passed in 159.01 seconds including
bootstrap. It proves EHD/DD retention through instance creation, instance version
publication, and an instance graph-only AvailableSchemas update with a saved Schema
inverse. Independent reacquisition preserves the EHD result identity and adds no
registry-owner transient allocations; subsequent schema version publication retires
both partitions. That scenario duration is not application latency or evidence of
a measured overall speedup. Guest-created validation-only products remain local;
no reduction of all reported forty validation builds is claimed.

The existing probe-backed incomplete_commit_repeats_error_then_completes_relationship_retry
scenario also passed (405.82 seconds including bootstrap and both injected-conflict
sequences), preserving repeated error recording and relationship-only recovery.
Full npm test and a matched application performance capture have not been run for
this checkpoint. A subsequent [41-fixture dance capture](../../performance/test-performance/dance-timings-selective-retention-comparison.md) passed before the bespoke inventory step was removed in
[commit b6f2cd23](https://github.com/evomimic/map-holons/commit/b6f2cd23). Those timings reflect cumulative branch changes and do not isolate selective retention.


### Delivered retention and test-execution follow-ups

Selective Session retention was delivered through merged map-holons PR 855.
PRs 854 and 858 subsequently merged; the combined state passed the maintainer's
hApp/host builds, npm start and full npm test, plus required CI, before PR 858
merged. Earlier checkpoint statements above describe their original evidence.
The [Issue 852 delivery summary](../../performance/test-performance/issue-852-delivery-summary.md)
records the later bounded-verification and test-setup consolidation results.
Guest-to-host registry return and the declarative required-binding-retention gap
remain separate follow-ups; closing Issue 852 does not establish either capability.


## Commit registry return follow-up — November 9

[map-holons #863](https://github.com/evomimic/map-holons/issues/863) extends the
selective-retention substrate with a full selected snapshot on internal Commit
responses, separate from agent pools. Transport binding produces unpublished
runtime products; client reconciliation adopts them only after its reset verdict
and only into the originating current active Session.

The merge validates the complete snapshot before publication and atomically
updates owner-pool membership, root and EHD/DD indexes against retirement. Imported
results receive live-owner temporary identities; existing host selections win
conflicts for the same exact identity. Malformed return data is discarded without changing the
authoritative persistence outcome. Preserve concurrent host publications and
in-flight owner allocations when updating or pruning the pool.

Validate cold host/guest construction, retained Complete and no-persistence
Rejected/correction paths, second-Commit transport/reuse, both partitions, exact
versions, duplicate/conflicting snapshots, unsaved dependencies and malformed
ownership/metadata. Exercise reset, uncertain outcomes and overlapping retirement.
Record matched cold/warm construction counts, snapshot bytes, capture/binding/
adoption and end-to-end timings; fewer constructions alone do not establish net
speedup. Delta transport and frozen-candidate promotion remain outside this unit.
Verification results follow in the working-tree checkpoint below.


### Working-tree verification — November 9

The #863 implementation is verified locally; this checkpoint does not claim a
commit, PR, merge or issue closure. Core unit tests (715), boundary tests (23),
native client tests (21), the native workspace check, the hApp WASM workspace
check and repository formatting passed. Boundary tests include actual Holochain
MessagePack encoding, unpublished binding, both partitions, exact saved versions,
owner-ID collisions, host-wins conflicts, idempotence, malformed/volatile/unsealed
products, current-Session checks and failure cleanup. The internal pool update
also has a late-failure rollback regression.

The production-conductor `effective_descriptor_tests` target passed in 221.31 s,
including bootstrap and its existing EHD/Session/retention scenarios. New coverage
starts with an empty host registry, adopts saved DDs from a Rejected Commit,
repeats that same unchanged candidate, corrects it to Complete, then exercises
cold/warm nonempty Complete Commits. It checks the exact saved ValueType reached
from the exercised PropertyType, all actually returned EHD sources, and unchanged
selected product transport identities/payloads on the subsequent Commit. It does
not demand additional schema products merely to populate a partition. Both EHD/DD
partitions are covered by boundary tests and the existing EHD conductor coverage;
this cold Commit workload exercises five saved DD constructions. Owner-pool
bookkeeping may be pruned without changing selected products.

Execution used the existing `MAP_SWEET_STARTUP_TIMEOUT_SECS=60` harness override
after upstream peer-store readiness timed out during startup. Successful readiness
for this run took 2.153 s; this does not establish a timeout root cause. Startup
and bootstrap are outside the measured Commit intervals. The final test was built
and run under Nix with an isolated `CARGO_TARGET_DIR` to avoid interference from
concurrent IDE builds. The relevant reproducible commands are:

```sh
nix develop --command npm run check -w map-host
nix develop --command npm run check -w map-happ
npm run fmt:check
nix develop --command npm run build:commit-perf -w map-happ
nix develop --command env MAP_SWEET_STARTUP_TIMEOUT_SECS=60 \
  RUST_LOG=warn,wasm=info,holons_trust_channel=info,holons_client::client_shared_objects::client_holon_service=info,holons_test::harness::helpers::mock_conductor=info \
  WASM_LOG=info cargo test --manifest-path tests/sweetests/Cargo.toml \
  --test effective_descriptor_tests -- --nocapture
```

Single-trial matched measurements from the in-process real-conductor backend:

| Workload | Assessment DD builds | Assessment EHD builds | Preparation/construction ms | Conductor ms | Commit end-to-end ms | Full response bytes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| rejected-cold | 5 | 1 | 380.250 | 616.441 | 616.930 | 12240 |
| rejected-warm | 0 | 1 | 313.067 | 502.302 | 502.808 | 12844 |
| complete-cold | 5 | 1 | 296.522 | 463.152 | 463.702 | 11639 |
| complete-warm | 0 | 1 | 262.050 | 416.750 | 417.448 | 20490 |

| Workload | Registry payload bytes | Host request capture us | Guest return capture us | Host return binding us | Host adoption us |
| --- | ---: | ---: | ---: | ---: | ---: |
| rejected-cold | 9031 | 2 | 394 | 292 | 26 |
| rejected-warm | 9090 | 27 | 366 | 304 | 28 |
| complete-cold | 9037 | 1 | 383 | 360 | 30 |
| complete-warm | 17896 | 48 | 661 | 377 | 33 |

The unchanged-candidate Rejected pair reduced observed Commit latency by 114.122 ms
(18.5%); the Complete pair by 46.254 ms (10.0%). Five assessment DD constructions
became zero in both warm attempts; one assessment EHD construction remained in
each attempt. Frozen validation work remains local and is not promoted. Both warm
guest ingress snapshots contained five DDs, with no registry hydration storage reads
or cache misses. The corrected Rejected candidate completed with zero new DD
constructions as well.

These are workload-specific observations, not a general speedup estimate. Cold
means an empty descriptor registry after Session reset, not cold persisted storage
or a cold process. The Rejected pair uses the same staged candidate; Complete
uses equivalent separately staged candidates, with staging outside the Commit
interval. Full snapshots include owner state beyond selected products, so their
size can differ while selected identities/payloads remain unchanged. Timings
include profiling overhead and are not a production websocket or UI benchmark.
Capture, binding and adoption together cost about 0.7–1.1 ms in these samples;
conductor and end-to-end measurements include the wider transport/execution cost.
Full snapshots remain the selected transport; these samples do not justify a
separate delta protocol. The agent-run checkpoint did not include the full
Sweettest suite; subsequent user-reported validation is recorded below.

### User-reported build and startup verification — November 9

The user reported successful hApp and host builds and a passing full `npm test`
run lasting 47 minutes 41 seconds. These results supplement the agent-run checks
above; the agent did not rerun this full suite.

The user also reported that `npm start` opened the application window approximately
65 seconds into the Starting Canvas stage. The supplied startup screenshot showed
these completed stages:

| Stage | Elapsed ms |
| --- | ---: |
| Initializing host | 260 |
| Installing Holochain application, including WASM compilation (dev mode on) | 249 |
| Executing Core Schema LoadHolons dance | 86681 |
| Activating base packages | 4284 |
| Realizing Canvas | 756 |
| Selecting home Dancer | 14481 |

At screenshot capture, Starting Canvas was still in progress at 60506 ms. The
approximately 65-second figure refers to that stage, not total startup. Assuming
the displayed stages execute sequentially, their completed durations plus the
reported window-open time imply approximately 172 seconds (2 minutes 52 seconds)
overall. The user subsequently confirmed that `npm start` behavior was nominal.
These observations provide a user-reported startup baseline.
