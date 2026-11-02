# Descriptor Implementation Plan

## Scope and authority

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

## Baseline and revised target

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

EffectiveHolonDescriptor migration remains deferred. Reset clears its selected
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

The design below is agreed but not yet implemented. It supersedes the earlier
Commit graph-copying carrier and fresh-on-every-access policy for frozen mutable
inputs. Historical verification above establishes neither completion nor performance
of this revision. The normative contracts are runtime §§14.6–14.10 and the
[space Session specification](../space-session-design-spec.md).

### Current gaps and observed evidence

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
   This remains pending and is not a prerequisite for units 1–4.

Keep units reviewable as separate commits. Use focused native/WASM and real-Commit
checks during development, then full manual verification at meaningful checkpoints.
Measure after unit 3 (bootstrap/Commit validation) and after unit 4 (cold/repeat
navigation). Record index rebuilding, acquisition/construction counts, scope reuse,
session resets, guest calls, policy misses and wall time separately. Unit 5 is
architectural consolidation, not an assumed performance improvement. Bootstrap
editing-time memoization and new Operator/KeyRule payloads remain separate work.
