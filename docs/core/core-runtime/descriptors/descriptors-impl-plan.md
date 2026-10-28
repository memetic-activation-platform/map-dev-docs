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

## Implementation sequence

1. **Rename and contract inventory.** Rename EffectiveDescriptor to
   EffectiveHolonDescriptor, including well-known names, result type and paired
   schema identities, construction Dance/request/response/implementation names,
   Rust APIs, Commands/wire binding, SDK handles, tests, and bootstrap assets.
   Generate schema JSON through map-schema. Keep runtime package dependencies
   on Core, Dance, and Commands and all eight directly licensed collections.
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

6. **Prepare cache policy in the guest.** Alongside navigation discovery, gather
   the metadata needed to derive final policies for applicable relationships.
   Include exact type and relationship identities, name mapping, final policy,
   and bounded-age parameters in a compact self-contained prepared projection.
   Choose the concrete property/transport encoding within existing holonic
   machinery; do not create one policy holon per entry or fetch fields one by
   one on the host. Install the host session-local policy index before marking
   preparation complete. Leave the wrapper's one-reference structure intact.

   Instance cache reads use only local final policies. Remove first-use
   descriptor lookup, DescribedBy/Extends traversal, and direction discovery
   from cache-policy resolution. Missing preparation routes through the
   acquisition layer before instance caching, never recursively from inside
   it. Provide foundational local policies for preparation's own reads. Keep
   guest request-local reuse and membership TTL/freshness semantics unchanged.
   Pull must keep selected descriptor/policy associations and reused membership
   entries coherent; old handles must not silently acquire another adopted view.

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
  public commit/disposal leaves results readable; staged projections stay local;
  concurrent requests, failures/retry, explicit pull, old handles, session
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
