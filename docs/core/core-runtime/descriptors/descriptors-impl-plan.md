# Descriptor Implementation Plan

## Scope and authority

This plan records the implementation delta for transient EffectiveDescriptor.
The [runtime descriptor specification](descriptors-design-spec.md#141-effectivedescriptor-canonical-definition)
owns the concept and runtime contract; the
[schema design](../../type-system/schema-design-spec.md#85a-effective-descriptor-result-schema)
owns result structure; the
[kernel rules](../../type-system/descriptor-semantics-rules.md#3-job-two-compute-effective-semantic-inheritance)
remain authoritative for inheritance.

## Implementation status

The implementation is present on `map-holons` branch 838 at `c7a07019`, under
[Issue #838](https://github.com/evomimic/map-holons/issues/838) and
[PR #844](https://github.com/evomimic/map-holons/pull/844). It is awaiting renewed
review and final-head CI; it is not recorded here as merged delivery. The
sequence below records the implemented scope and its verification obligations.

The final design uses allocation-free `ComputedEffectiveSchema` occurrence
metadata, one sealed transient result, no contribution Holons or public
allocation option, policy-normalized direct products, and guest-mediated
construction. Invalid key-rule cardinality remains projectable; singular access
and explicit validation report the corresponding error.

Local verification includes 586 core unit tests, 23 client tests, 369 SDK tests,
58 schema compiler tests, host/WASM/web checks, and formatting. The retained
result integration test passed locally in 105–111 seconds and in CI on
`7cd21408` in 330.853 seconds under the unchanged 600-second limit. Both heavy
jobs passed on that head; its light job exposed a missing test-only trait import,
fixed and locally verified at `c7a07019`. These are observed verification results,
not startup or guest-local construction latency guarantees.

Follow-ups remain separate: [#841](https://github.com/evomimic/map-holons/issues/841)
owns agent-session retention and registry discovery for broader adoption;
[#843](https://github.com/evomimic/map-holons/issues/843) owns consolidated Theme
loading. Neither capability is delivered by this implementation.

## Inspected baseline and dependencies

Original grounding baseline: `map-holons` commit
`c4554f0bb890529776ae9884c684cf100516c467`, the inspected head of
[PR #837](https://github.com/evomimic/map-holons/pull/837) on 2026-10-23.
The PR was open at grounding time. The 838 implementation uses that
post-removal architecture; the original baseline is historical context.

Established components to reuse:

| Component / source under `map-holons` | Established responsibility |
|---|---|
| `shared_crates/holons_core/src/descriptors/inheritance.rs` | `ExtendsIter`, `walk_extends_chain`, policy-aware `effective_relationship_targets`, `EffectiveRelationshipMember` with `member` and `declared_on` |
| `shared_crates/holons_core/src/descriptors/holon_descriptor.rs` | Existing property, relationship, affordance, constraint, binding, and key-rule accessors |
| `shared_crates/holons_core/src/descriptors/effective_relationships.rs` | Declared contract discovery, `SourceOf` inverse discovery, direction classification, identity deduplication, name ambiguity, and staged traversal guards |
| `shared_crates/holons_core/src/reference_layer/definition_identity.rs` | Definition identity without implicit staged-successor substitution |
| `shared_crates/holons_validation/src/commitments.rs` and `descriptor_package.rs` | Existing provenance consumers and evaluation-local products; no wholesale validator migration is required |
| `shared_crates/holons_core/src/core_shared_objects/holon_collection.rs` | Ordinary relationship collections and lifecycle |
| `schema-src/descriptor-runtime/schema.tdl` | Owned descriptor declarations and normal package loading |

PR #837 removes `DescriptorReader`, replacement indexing, and implicit
prospective replacement. Resolve the actual references supplied by the caller.
Do not revive those abstractions for shared products or target deduplication.

The pre-existing `effective_relationships()` obtains inherited declarations and
materialized inverses independently and can raise `UnsupportedStagedTraversal`
for an unsaved endpoint without inverse indexes. That is an established API
behavior, but it conflicts with the new constructor's deliberately tolerant
staged discovery contract. Factor reusable discovery internals rather than
calling this combined accessor unchanged or weakening all existing APIs.

The runtime spec previously deferred transient effective surfaces; this plan
activates that work. Kernel inheritance semantics and authoritative descriptor
meaning remain established semantics. New result types, lightweight contribution metadata,
lineage reuse, and guest construction are the new architectural decisions.

## Implementation sequence

1. **Shared lineage-aware resolution.** Extract policy-aware operations accepting
   an already validated target lineage. Preserve Local, Additive, Override,
   collection normalization, raw local-defect evidence, contribution order,
   and `declared_on`. Existing individual accessors retain lazy or
   short-circuit paths. No competing inheritance algorithm.
2. **Navigation discovery.** Reuse the resolved lineage and declared contract;
   examine existing `SourceOf` on the target and ancestors, admitting both
   directions whose SourceType is eligible. Retain staged declarations and
   available materialized inverses, tolerating absent unmaterialized indexes.
   Deduplicate only the navigation set by definition identity. Preserve other
   structural and graph failures and existing name ambiguity behavior.
3. **Schema definitions.** Define the result/contribution HolonTypes, all their
   relationship pairs, position PropertyType, cardinality constraints, explicit
   collection metadata, and keyless contracts in Descriptor Runtime Schema.
   Depend directly on Core, Dance, and Commands. Declare all eight effective
   collections directly in `EffectiveDescriptor.HolonType.InstanceRelationships`.
   Do not author external `InstanceRelationshipFor` occurrences. Move the
   construction Dance and its request/response/implementation definitions into
   the same package, preserving an acyclic dependency graph.
   `ContributionCollection` targets `RelationshipType.TypeDescriptor`; its accessor
   admits both declared and inverse descriptors but only the seven canonical
   authoritative collection identities. Preserve `AffordsDance`/`AffordsCommand`
   identities and exclude navigation discovery from provenance.
   Regenerate normal schema artifacts and verify bootstrap/package loading in
   `map-holons` when implementing; no generated artifacts belong in DevDocs.
4. **Transient graph construction and wrappers.** Populate direct normalized
   collections from the same lossless computed projection. Retain pre-normalization
   contribution records as lightweight member/origin/collection/local-position
   values. Preserve repeated occurrences and selected key-rule provenance in the
   computed projection. Verify normalized direct membership through ordinary
   HolonCollection/relationship transport; do not transport occurrence metadata
   as contribution Holons.
   Allocate one result Holon and no contribution Holons; remove the public
   allocation option from the service, Commands, SDK, and Dance request. Preserve
   raw occurrence evidence for Commit and diagnostic consumers. Seal completed
   results against consumer mutation. Add typed
   `EffectiveDescriptor` and contribution wrappers over references, with no
   parallel collection cache or lineage reads in accessors. Keep the local
   algorithm in `holons_core` separate from the service-mediated runtime
   construction entry point.
5. **Service-mediated construction and Dance.** Expose construction through
   `TransactionContext`, delegating to `HolonServiceApi`. Implement the client
   service operation in `ClientHolonService` by building the typed request and
   invoking the guest Dance through the existing transport. Implement the guest
   service operation in `GuestHolonService` by calling the local core algorithm
   in the current transaction. The guest Dance handler enters the same
   service-mediated operation; its guest service must execute locally without
   invoking the Dance again. Runtime consumers use this operation rather than
   directly invoking the local algorithm on the host. Keep construction-specific
   routing out of the generic Dance executor.
   Add `ConstructEffectiveDescriptor.DanceType` with
   explicit `SpaceAuthoritative`, and its statically selected guest
   implementation. Descriptor Runtime Schema owns the request/response types. The request
   has a `1..1` `RequestedHolonType` relationship to `HolonType.TypeDescriptor`,
   inverse `RequestedByEffectiveDescriptorRequest` (`0..*`), ordinary Version
   binding, definitional metadata, unordered duplicate-free policy, and Block
   deletion semantics in both directions. It has an explicit keyless contract.
   `ConstructEffectiveDescriptorResponse` extends the normal response type;
   its `ResponseBody` contract names the runtime result type. Author the generic
   `DanceAffordedBy -> HolonSpace` occurrence. Bind request, successful body,
   result graph and failures through existing execution/transport paths.
   Keep semantic descriptor-category endpoints. Validate the runtime request and
   retain constructor invariants, but do not revalidate the generated result
   or response at runtime. Exercise exhaustive generated-output
   conformance separately where appropriate. The existing explicit conformance
   helper defers only the six target checks enumerated in the runtime
   specification, matching canonical subject types and relationship identities.
   The retained-result integration test must not repeat exhaustive remote
   validation for every member. Keep structural safeguards and unrelated
   validation active. Remove
   this accommodation with the separately implemented endpoint-eligibility work;
   do not add generalized eligibility, key-rule normalization, or a ResponseBody
   redesign here.
   Read authoritative Dance/Commands collections through ordinary graph access.
   Register Descriptor Runtime after its dependencies in bootstrap and regenerate
   the packaged bundle. Use shared validation.
6. **DAHN integration.** Route consumers needing multiple collections through
   the existing Rust/public SDK seam to one construction request per required
   schema snapshot. Consume the result in the caller's retained transaction.
   Refresh by reconstruction after relevant schema edits. Keep instance-level
   available relationships, occurrence retrieval, permissions, and visualizer
   selection separate. Follow the
   [Navigator integration plan](../../space-navigator/space-navigator-impl-plan.md#13-effectivedescriptor-consumer-integration).
7. **Semantic and operational validation.** Complete the cases below before
   treating the new path as equivalent to the established descriptor APIs.

## Compatibility and verification

- Compare all seven inherited collections with the corresponding direct
  `HolonDescriptor` products on root, deep, local-only, and Override fixtures;
  compare selected identities, normalization, multiplicity, order where
  meaningful, and `declared_on`. For malformed key-rule selection, verify that
  construction projects zero or multiple distinct selected targets without
  validating the source schema; the singular accessor must still report the
  missing/multiple-target error. Preserve the lossless occurrence sequence for
  Commit validation. Verify that constructing a result allocates no contribution
  Holons and that raw occurrence provenance survives direct-product normalization.
- Exercise additive contributions from several ancestors, repeated constraints
  and bindings, duplicate local occurrences, redundant inherited members,
  semantic-name collisions, Local noninheritance, nearest Override, cycles,
  multiple parents, wrong target kinds, and access failures. Distinguish raw
  contribution evidence from policy-normalized direct relationships.
- For fully indexed saved schema, assert that navigation equals exactly the
  SourceType-based set over the lineage, including declared definitions found
  via SourceOf, inherited inverses, and duplicates reached via both discovery
  paths. Compare existing combined accessors on well-formed complete fixtures;
  do not copy their narrower discovery as the canonical definition.
- Exercise a wholly unsaved type, staged child/saved parent, staged declared
  RelationshipType, absent inverse indexes, and materialized saved inverses.
  Construction must succeed without inventing staged inverses. Unrelated APIs
  retain their existing staged traversal errors. Changing ordinary instance
  occurrences must not change EffectiveDescriptor vocabulary.
- Verify result contracts and lightweight occurrence provenance, correct
  runtime package ownership and its required dependency closure, all nondeferred endpoint
  and cardinality checks, and consistency of direct membership with normalized raw occurrences. Test
  canonical declared and inverse collection identities, reject arbitrary
  collection descriptors, and prove unrelated validation remains unchanged. Missing
  empty authoritative affordances produce empty collections, not invented members.
- Verify actual-reference identity: a saved definition remains the target even
  when a staged successor exists. Round-trip the transient graph through the
  normal host/guest boundary and compare target identities, effective
  membership, duplicate policy, and order. Check local provenance positions on
  the computed projection, not as transported contribution Holons. No descriptor
  state clones.
- Verify the service boundary from both execution contexts: host construction
  delegates through `ClientHolonService` and the normal construction Dance,
  while `GuestHolonService` invokes the local algorithm in the guest transaction
  without further delegation. Assert that eager product population occurs in
  the guest, that the local constructor is not used by the host path, and that
  the returned graph belongs to the caller's retained transaction. Check service
  and Dance failures through the existing error boundaries.
- Verify wrapper reads trigger no target-lineage resolution, results survive
  within the retained transaction as permitted, disposal ends transient access,
  and schema changes require reconstruction. Retained saved-descriptor cache
  behavior and cache-hit/freshness policies must remain unchanged.
- Exercise DAHN property, declared-contract, navigable-relationship, and action
  consumers without TypeScript inheritance reconstruction or permission changes.

## Measurements and remaining implementation checks

Instrument target-lineage resolution calls and `Extends` edge reads separately
from classification of other referenced descriptors. For lineage length `n`,
one construction performs one complete target-lineage walk; all collection
resolvers and wrapper reads perform zero additional target-lineage walks.
Record per-collection resolution counts, SourceOf reads, graph allocation,
normal transport size, and end-to-end duration against sequential existing
accessors on identical deep/wide schema fixtures with warm and cold caches.

The acceptance signal is elimination of redundant target-lineage traversal,
with semantically equivalent results, not an assumed absolute latency or a
fixed speedup. Report Holochain version and invocation overhead separately;
0.7.1 regression findings are not an architectural dependency.

Implementation must confirm that ordinary relationship construction and wire
projection preserve the specified ordered/duplicate-bearing collection shapes,
while the computed projection retains contribution evidence. Repair any gaps within those existing mechanisms;
do not introduce a special transport or Rust-only authoritative representation.
Exact helper signatures and generated descriptor keys are implementation
choices. Registry/session lifetime and broader consumer migration remain
separate follow-up work.


## Package ownership resolution

Descriptor Runtime Schema owns the complete EffectiveDescriptor contract and
construction Dance. It depends directly on Core, Dance, and Commands. All eight
effective collections are directly licensed by the result type. This replaces
the rejected externally authored `InstanceRelationshipFor` approach without
changing Commit validation or the six-target endpoint accommodation. Verify
canonical package ownership, dependency closure, and bootstrap Commit before
running the construction and transport assertions.
