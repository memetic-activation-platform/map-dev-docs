# MAP Runtime Descriptor Subsystem Design Spec (v2.1)

## 1. Purpose

This specification defines the runtime descriptor subsystem within the MAP core
holonic runtime. It explains how runtime code reaches descriptor data, invokes
descriptor semantics, and exposes descriptor-backed capabilities without
creating another descriptor representation or semantic authority.

The descriptor subsystem makes self-description operational. A holon's
`DescribedBy` relationship connects its runtime representation to the effective specification
defined by its type, including its instance contract, key rule, validation commitments, and
behavior affordances.

This is a master design document. It establishes responsibilities and
boundaries, then delegates schema structure, semantic algorithms, construction
flow, and component execution to focused specifications.

## 2. Authority

Authority is divided by concern:

1. The [schema design specification](../../type-system/schema-design-spec.md)
   defines descriptor structure and schema invariants.
2. The
   [descriptor-kernel semantic rules](../../type-system/descriptor-semantics-rules.md)
   define representation-neutral computation and validation.
3. The [layered descriptor architecture](../../descriptors/layered-desc-arch.md)
   defines creation, graph construction, descriptor-default materialization,
   and validation ordering.
4. The [MAP Validation Architecture](../../validation/validation-arch.md)
   owns the shared descriptor-aware validation framework. The
   [PVL Design Specification](../../validation/pvl-design-spec.md) separately
   owns descriptor-independent Integrity Zome validation.
5. The [holon layered representation design](../../architecture/holon-layered-representation-design-spec.md)
   defines the general integrity, shared-object, reference, and typed-wrapper
   layers.
6. The TDL corpus in `map-holons/schema-src` defines exact descriptor
   identities and member declarations.
7. The [space Session specification](../space-session-design-spec.md) owns
   Session lifetime, shared retirement, reset triggers, and Commit capture.
8. This specification defines the runtime descriptor subsystem and its
   integration boundaries.

Generated loader JSON, Rust enums, wrapper fields, and source-language
declaration forms are not independent sources of descriptor meaning.

## 3. Runtime Role

The descriptor subsystem connects four runtime concerns:

```text
HolonReference and Reference Layer
        |
        | resolve and read
        v
Descriptor Holons in the Explicit Holon Graph
        |
        | invoke through HolonDescriptor
        v
Descriptor Kernel
        |
        | computed specifications, classification, and violations
        v
Runtime Callers and Component Subsystems
```

Its responsibilities are to:

- resolve a holon's describing type;
- interpret descriptor holons through schema-backed runtime operations;
- provide graph access to the descriptor kernel;
- expose local descriptor state and kernel-computed effective results;
- support descriptor-backed validation and mutation decisions;
- expose behavior affordances to their owning component runtimes; and
- map graph and semantic failures into runtime error contracts without hiding
  their causes.

The descriptor subsystem is not a separate runtime beside the holonic runtime.
It is the part of the holonic runtime that makes descriptor relationships and
semantics usable by callers.

## 4. Representation Contract

### 4.1 Descriptors are ordinary holons

Every descriptor is an ordinary holon in the explicit MAP holon graph. Its
properties, relationships, identity, and lifecycle are represented by the same
shared-object and reference-layer facilities used for other holons.

The subsystem does not copy descriptors into an authoritative Rust object
model. A runtime descriptor operation reads the descriptor holon through a
`HolonReference` or a typed core wrapper over that reference.

### 4.2 One holonic representation

The explicit graph formed by `Holon`, `TransientHolon`, `StagedHolon`,
`SavedHolon`, their relationships, and their reference-layer handles is the
runtime representation on which descriptor semantics operate.

Source ASTs, loader references, source indexes, generated JSON, and comparison
snapshots may exist at their respective boundaries. They do not become a
second representation on which descriptor semantics independently execute.

### 4.3 Lifecycle transparency

Descriptor operations apply to readable transient, staged, and saved holons.
Callers should not need different descriptor semantics for each lifecycle
state.

The reference layer remains responsible for phase-aware resolution and access.
The descriptor kernel receives stable graph identities and local graph facts;
it does not own lifecycle management.

## 5. Descriptor Resolution

For a holon `H`, runtime descriptor resolution follows the authored graph:

```text
H --DescribedBy--> D
```

Resolution must:

1. read the local `DescribedBy` relationship from `H`;
2. require exactly one target;
3. require an admissible, non-abstract describing type as defined by the
   descriptor kernel; and
4. return descriptor-backed runtime access to `D`.

Resolution must not infer the descriptor from:

- a Rust type;
- `TypeKind`;
- a TDL declaration form;
- a key suffix or type name;
- a persisted entry type; or
- a source-format field after that field has been lowered.

The reference layer is the natural caller-facing home for this operation
because it already abstracts transient, staged, and saved representations.

Resolving `DescribedBy` does not produce a combined lineage. Schema 2.0 keeps
these operations distinct:

- `L(D(H))` determines the effective specification to which the holon must conform;
- a descriptor's own `Extends` lineage determines classification and the effective specification
  it imposes on described instances; and
- the kernel's `InheritanceRules` table governs semantic inheritance of values
  populated through each member.

## 6. Descriptor Classification

When runtime code requires a descriptor category, classification follows the
descriptor's identity and transitive `Extends` relationship to the applicable
abstract category.

Examples of category anchors include:

- `HolonType.TypeDescriptor`;
- `PropertyType.TypeDescriptor`;
- `ValueType.TypeDescriptor`;
- `RelationshipType.TypeDescriptor`;
- `DeclaredRelationshipType.RelationshipType`; and
- `InverseRelationshipType.RelationshipType`.

A descriptor's Instance TypeKind is a separate, graph-derived classification: the nearest
descriptor in its self-first lineage with a local explicit `DefinesInstanceTypeKind = true`
value. `TypeDescriptor` is the sole descriptor root without an Instance TypeKind. Runtime code may
project the resolved anchor identity into a legacy `TypeKind` API, but must not read authored
`TypeKind` or `InstanceTypeKind` state.

Type names, declaration forms, key formats, and derived category projections may support
diagnostics or optimization after classification. They are not proof that a descriptor belongs to
a wrapper category.

Typed narrowing must fail when the descriptor does not extend the required
category. It must not silently construct a typed view over an incompatible
reference.

## 7. HolonDescriptor Integration

`HolonDescriptor` is the existing runtime façade for descriptor semantics. An
ordinary readable holon reaches its describing type through
`ReadableHolon::holon_descriptor()`. Descriptor-specific runtime code works
through `HolonDescriptor` and the typed descriptor wrappers it returns.

`HolonDescriptor` wraps a resolved `HolonReference` and uses existing
reference-layer reads and descriptor helpers to provide local and effective
access. Its effective operations implement or delegate to the Schema 2.0
descriptor-kernel algorithms. No graph-adapter layer or copied graph
representation is required.

The wrapped reference remains encapsulated. Consumers use descriptor accessors
rather than extracting the reference and independently traversing descriptor
state. Internal helpers must preserve multiplicity, order, target identity,
and local-versus-inherited provenance until the governing semantic operation
has evaluated them.

Descriptor-kernel operations exposed through `HolonDescriptor` compute and
validate; they do not mutate holons or materialize defaults in authored
representations.

## 8. Local and Effective Access

The runtime must distinguish local structural reads from effective semantic
queries.

### 8.1 Local access

Local access reads state explicitly populated on a descriptor holon. Examples
include:

- its direct `Extends` target;
- shared descriptor metadata;
- a property descriptor's selected value type and local default metadata;
- a relationship descriptor's local endpoints and directional properties; and
- locally populated affordance relationships.

Local access does not traverse `Extends`, apply kernel inheritance rules, or materialize
missing values.

### 8.2 Effective access

Effective access delegates to the descriptor kernel. Examples include:

- effective instance properties and relationships;
- effective populated values under `Local`, `Additive`, or `Override`;
- subtype and endpoint compatibility;
- the effective instance key rule;
- effective value constraints; and
- effective behavior affordances.

Caller-facing names must make the distinction clear. An operation documented
as effective must not substitute an ad hoc local read, and a local operation
must not conceal graph traversal.

Effective values are computed views. They are not copied into authoritative
local descriptor state.

## 9. Runtime API and Encapsulation

Typed Rust wrappers are part of the general MAP core-struct pattern. Descriptor
wrappers may provide category-specific operations when those operations make a
meaningful runtime contract easier and safer to use.

The following rules apply:

- a wrapper retains the holon as its semantic subject;
- schema-backed state is read through reference-layer operations;
- copied Rust fields do not become an alternate source of truth;
- typed construction or narrowing validates the required descriptor category;
- effective operations delegate to the descriptor kernel; and
- wrappers preserve reference-layer lifecycle behavior.

Wrapper proliferation is not a goal. A specialized wrapper is justified when
it adds a coherent typed contract or behavior, not merely because a descriptor
has a distinct derived category projection or concrete schema identity.

The subsystem does not define a universal public trait whose purpose is to
expose every wrapper's private `HolonReference`. Such an escape hatch defeats
the encapsulation supplied by typed wrappers. A specific API may deliberately
accept or return a `HolonReference` when reference transfer is part of that
API's contract, but that conversion is explicit and purpose-specific.

Accessors are schema-backed conveniences. They must preserve requiredness,
optionality, cardinality, and lifecycle errors. They must not synthesize
defaults during reads or encode independent inheritance rules.

## 10. Affordance Discovery

Descriptors make active-holon behavior discoverable. Holon and value types may
declare commands, dances, operators, and other affordances through ordinary
schema relationships.

The descriptor subsystem owns:

- resolving the relevant descriptor;
- computing the effective affordance declarations through kernel semantics;
- looking up an affordance by schema identity or stable semantic name; and
- returning descriptor-backed information required by the owning runtime.

The subsystem does not own execution of every discovered affordance:

- Commands owns command ingress and command execution;
- Dances owns dance invocation, implementation binding, and execution;
- Queries owns query planning and execution;
- Validation owns validation orchestration beyond descriptor-kernel
  conformance; and
- operator execution belongs to the value/query execution design that consumes
  operator descriptors.

Descriptor-backed discovery must not require a second global semantic registry.
An owning component may maintain implementation bindings or optimized indexes,
but those structures consume descriptor identity rather than replace the
schema declarations.

## 11. Creation, Default Materialization, and Validation

The runtime descriptor subsystem consumes and evaluates explicit holon graphs.
It collaborates with creation paths but does not absorb their mutation
responsibilities.

Host-side TDL and MAP JSON translation operates over `LoaderRefRep` and does
not invoke this runtime pipeline. The pipeline begins when `LoaderRefRep` is
submitted to the guest loader or when a runtime creation path constructs
application holons directly.

The loader's final sequence is:

```text
construct and resolve explicit graph
  -> compute effective contract
  -> normalize enum defaults
  -> attempt descriptor-defined defaults
  -> materialize enum properties
  -> commit
       -> invoke shared Holon Validator
            -> invoke descriptor-kernel semantics
       -> persist only when valid
```

Shared writable-reference operations provide best-effort default population during construction,
staging, cloning, and descriptor attachment. Holon Loading retains its final pass after assembly.
The descriptor kernel owns semantic computation and
validation. Commit must invoke the reusable Holon Validator for persisted graphs and
refuse persistence when blocking violations remain. The Holon Validator remains
independently callable outside commit and Holon Loading. Commit does not invoke
default materialization; it validates the actual explicit graph supplied
by creation/load orchestration. The descriptor runtime provides
`HolonDescriptor`, typed descriptor wrappers, and existing reference-layer
helpers through which those services operate.

The Validation document set owns validator scopes, contexts, rule delegation,
error accumulation, and result reporting. Descriptor-independent PVL is
invoked separately through Holochain Integrity callbacks and does not resolve
descriptors or invoke the descriptor kernel.

The reusable Holon Validator performs descriptor-driven validation of ordinary
holons and descriptor holons against their effective descriptor contracts. It
accumulates independently discoverable descriptor
violations across the transaction and persists nothing if any blocking
violation exists. Fatal graph-access or infrastructure failures may stop
validation when further results would be unreliable.

The Holon Validator is the reusable validation entry point. It owns scope,
context, rule coordination, and result accumulation, while delegating Schema
2.0 semantic predicates and conformance algorithms to the pure descriptor
kernel. It must not duplicate those algorithms.

`with_descriptor()` attempts defaults after successful attachment; available descriptor
information may still be incomplete. Construction, staging, and clone paths retain their own
attempts. Holon Loading's final default-population and enum-materialization pass remains
authoritative after relationship assembly, including for values copied by early attempts.
See [best-effort default population](../../descriptors/layered-desc-arch.md#6-best-effort-default-population)
for triggers, direct attachment without population, idempotence, and the error contract.

Once written, a materialized default is ordinary explicit property state. The
loader may retain ephemeral provenance for diagnostics, but commit persists no
authored-versus-default marker. Later descriptor-default changes do not replace
already populated values; validation assesses their conformance.

`HolonDescriptor::instance_properties()` supplies the effective property
declarations. `PropertyDescriptor` exposes the schema-backed effective member
definition, including the effective `default_value()` for each declaration. It
does not treat locally populated descriptor fields as the complete definition.
No separate kernel-level default helper is required.

A mutation-capable default-materialization service exposes
`WritableHolon::populate_defaults()`. It detects omissions on the receiver,
reads defaults from effective `PropertyDescriptor`s, and writes applicable
values through the receiver's mutation API. Loader orchestration selects the
staged-holon scope; descriptor wrappers, the Holon Validator, and commit do
not receive mutation capabilities.

Population is fail-fast per holon for errors other than `MissingDescribedBy`; partial
writes are not rolled back. The loader collects errors across holons and skips Commit
if any are reported. A skipped default is not a validation finding or readiness obligation;
the Holon Validator assesses any resulting required-property omission.

Runtime reads must not treat a missing required property as a request to apply
its default. A missing required value after default materialization is invalid explicit
state.

Transient or staged graphs may be temporarily incomplete during controlled
construction. Such graphs must not be committed or published as valid merely
because the reference layer can represent them.

## 12. Descriptor-Backed Mutation Decisions

Other runtime layers may consult descriptor metadata before accepting or
classifying a mutation. Examples include:

- whether a property or relationship is permitted by the effective contract;
- whether a relationship target satisfies its endpoint constraint;
- whether a relationship mutation is definitional; and
- whether a value satisfies its selected value type and constraints.

The descriptor subsystem supplies the authoritative descriptor-backed answer.
The consuming subsystem owns the resulting action. For example, the shared
objects and transaction layers decide whether a mutation creates a new version
or graph-only work after obtaining the relationship's effective
`IsDefinitional` value.

Failure to resolve required descriptor metadata is an error. Consumers must
not silently substitute permissive, restrictive, graph-only, or
version-producing defaults.

## 13. Error Contract

Runtime descriptor operations must distinguish failures that callers can act
on or diagnose independently, including:

- graph-access or lifecycle failure;
- missing or multiple `DescribedBy` targets;
- invalid or abstract describing type;
- invalid typed narrowing;
- missing or multiple `Extends` parents;
- cyclic inheritance;
- unresolved relationship target;
- missing or malformed required descriptor state;
- `RedundantInheritedMemberDeclaration` for a repeated inherited member identity;
- `DuplicateSemanticMemberDeclaration` for a property or relationship name collision within its
  namespace;
- invalid endpoint category;
- invalid cardinality or value constraint; and
- descriptor-kernel conformance violations.

`HolonDescriptor` operations report `HolonError` without discarding descriptor,
member, target, or contribution provenance. Higher-level validation boundaries
map those failures into their result vocabulary where required.

Source adapters may enrich these errors with filenames and source locations.
Source provenance remains boundary metadata and does not alter semantic
identity.

## 14. Derived Results and Caching

Within a descriptor-kernel evaluation, implementations must memoize effective
semantic products by product kind and resolved descriptor identity. A product
whose meaning depends on multiple identities uses the complete identity tuple
as its cache key. Effective-product computation is separate from conformance validation: the
kernel computes products from an immutable graph snapshot, then validates holons against those
products. It never computes an effective specification by recursively validating the descriptor
that supplies it.

An in-progress cache entry is also a recursion guard. Re-entering the same
product dependency is a semantic evaluation cycle unless the semantic rules
explicitly define that fixed point. `DescribedBy` is not followed transitively during product
computation. A self-describing descriptor selects its already computed effective specification; it
does not request a nested conformance result.

Memoized results are valid only for the graph identity and version from which
they were computed. Mutable inputs, including descriptor-default materialization,
are not retained across editing operations. Once preparation and validation freeze
those inputs, a validation-owned scope permits reuse until that assessment exits.
Editing after rejection and subsequent validation use a new scope; no per-mutation
generation or dependency invalidation graph is required. Final validation evaluates
the completed graph snapshot.

The session-retained or candidate-local EffectiveHolonDescriptor below consolidates several
effective products into an ordinary transient holon. It preserves direct
kernel evaluation semantics without requiring every individual accessor to
construct the full surface.

The subsystem does not currently depend on:

- a persisted effective-descriptor artifact;
- DAG-CBOR encoding of effective surfaces;
- descriptor-dependent PVL validation; or
- a second mutable cache that can disagree with descriptor holons.

Cached or derived results are replaceable implementation products. Descriptor
holons interpreted by the descriptor kernel remain authoritative.

### 14.1 EffectiveHolonDescriptor — canonical definition

An **EffectiveHolonDescriptor** is the effective schema surface for one
HolonType. It consolidates inherited declarations and outbound navigation
vocabulary while retaining references to authoritative definitions. It does
not represent effective PropertyType, RelationshipType, or ValueType
specifications. The generic descriptor kernel continues to interpret those
categories under their own contracts.

The Holonic Wrapper Pattern distinguishes two objects:

- the `EffectiveHolonDescriptor` Rust struct specializes the shared `DerivedDescriptor` handle around one `HolonReference`;
- that self-resolving reference identifies a typed transient holon described by
  `EffectiveHolonDescriptor.HolonType`.

The wrapper carries no separate transaction field, parallel schema cache, or
`described_instance` field. Its referenced holon carries the prepared relationships
and data; private runtime retirement metadata enforces the space Session contract. Source references retain their own lifecycle
variants and resolution capabilities. `DescribedHolonType` identifies the
HolonType whose instance schema is represented; `DescribedBy` identifies the
result's own type. Neither replaces an instance's authoritative describing type.

`HolonDescriptor` remains the wrapper around an authoritative definition. Its private,
nonserialized derived-fields handle acquires the complete specialized result on demand.
It uses the same memoization and retirement contract as the other descriptor wrappers.
Local reads and metadata delegation belong there; inherited collection computation
belongs on EffectiveHolonDescriptor. The concrete return type preserves generic
`impl ToPropertyName`, `impl ToRelationshipName`, and corresponding Dance and
command name conversions. No trait-object or extension-trait split is required.

Descriptor Runtime Schema depends directly on Core, Dance, and Commands and
owns the result and construction Dance contracts. The result type extends
`DerivedDescriptor.HolonType`, inheriting its lineage/kind carrier contract; the
HolonType-specific effective collections remain declared directly on the result type. External
`InstanceRelationshipFor` occurrences do not extend that contract.

### 14.2 Public acquisition and schema surface

`ReadableHolon::effective_descriptor()` returns
`Result<EffectiveHolonDescriptor, HolonError>`. Rust resolves the source holon's
unique `DescribedBy` reference and acquires the projection of that exact
HolonType through the session/context service. A Holon-scoped Command exposes
this operation. The SDK performs boundary projection and binding; TypeScript
must not resolve the describing type, choose construction versus reuse, or own
per-view schema memoization.

The result supplies:

| Accessor | Populated relationship / meaning |
|---|---|
| `instance_properties()` | `EffectiveInstanceProperties` |
| `instance_relationships()` | `EffectiveInstanceRelationships`, the declared contract |
| `singular_navigable_relationships()` | `SingularNavigableRelationships`, effective maximum one |
| `plural_navigable_relationships()` | `PluralNavigableRelationships`, effective maximum greater than one or unbounded |
| `navigable_relationships()` | Singular then plural composition, preserving every occurrence |
| `afforded_dances()` | `EffectiveAffordsDance` |
| `afforded_commands()` | `EffectiveAffordsCommand` |
| `effective_validation_bindings()` | `EffectiveValidationBindings` |
| `effective_constraints()` | `EffectiveConstraints` |
| `effective_key_rule()` | Singular access to `EffectiveInstanceKeyRule` |
| `instance_type_kind()` | Optional nearest defining anchor, prepared from the same lineage |

Name-based lookup and permission-to-use-contract helpers operate on the same
prepared products. Effective-schema methods move from HolonDescriptor and
ReadableHolon to this concrete wrapper by semantics, not merely by their
`available_*` or `effective_*` prefixes. Public alternate paths that independently
walk inheritance are removed. Explicit local declaration reads, where needed,
are identified as local, for example with a `_local` suffix. Metadata operations
outside the prepared products may delegate to the authoritative descriptor.
Such delegation must not reintroduce migrated inheritance resolution.

`HolonDescriptor::effective_descriptor()` provides ordinary type-oriented
acquisition for consumers already holding an authoritative HolonType. It acquires
that exact type's instance contract through its private derived-fields memo.
In contrast, `ReadableHolon::effective_descriptor()` first resolves the source's
`DescribedBy`. Both use shared acquisition; the type-oriented accessor must not
mistakenly project the type's own meta-type. `HolonDescriptor::instance_type_kind()`
reads the same prepared result rather than walking Extends independently.

The returned handle is lightweight. Returning another wrapper over the same
retained transient reference does not reconstruct or copy the graph. Eager
population is the default. If measured single-aspect flows justify lazy
population later, that choice stays behind this API; callers do not select an
implementation strategy.

Plural navigation warms its referenced saved holons immediately before returning.
The helper snapshots the relationship occurrences, extracts and deduplicates exact
`HolonId`s from saved references only, and passes those IDs to `ensure_cached`.
Staged and transient references are excluded. Warming neither changes returned
references, occurrence order, nor duplicates. It is advisory: population failures
are logged without turning a successful navigation read into a failure; later
ordinary target reads retain their normal error behavior. Ordinary cache eviction
still applies. Construction and singular-only navigation do not initiate this
warming. An instance availability request for one partition reads that partition
directly, so singular-only availability does not traverse the plural collection.
The SDK's typed plural accessor reaches the same Rust operation.

### 14.3 NavigableRelationships and instance availability

For HolonType `T`:

```text
Lineage(T) = {T} union Ancestors(T)
OutboundVocabulary(T) = relationship occurrences with SourceType in Lineage(T)
Singular(T) = occurrences from OutboundVocabulary(T) with effective maximum = 1
Plural(T) = occurrences from OutboundVocabulary(T) with effective maximum > 1 or unbounded
NavigableRelationships(T) = concatenate(Singular(T), Plural(T))
```

All relationships are outbound from their SourceType to their TargetType.
Declared/inverse classification is an internal schema/storage distinction, not
a UI traversal direction. Navigability and updateability are separate
capabilities. Navigation grants no mutation or authorization permission.

Construction reads effective `InstanceRelationships` and existing `SourceOf`
indexes on the target and its ancestors. Both declared and inverse descriptors
whose SourceType is eligible participate. Source identity uses exact definition
identity, without implicit staged-successor substitution. Reaching the same
RelationshipType through several discovery paths contributes one navigation
identity; this discovery union is distinct from inherited declaration
accumulation, which must preserve invalid repeated declarations.

For staged schema, retain available forward declarations and materialized
SourceOf entries, including saved ancestor indexes. Missing unmaterialized
indexes on an unsaved type are expected. Do not synthesize inverses from pair
metadata. Actual access, malformed structure, and inheritance errors propagate.
Ordinary instance occurrences are not inspected to discover the type vocabulary.

Construction resolves the directly attached directional CardinalityConstraints
and populates `SingularNavigableRelationships` and `PluralNavigableRelationships`.
Both optional and required maximum-one relationships are singular. An omitted
maximum is unbounded and plural; an explicit maximum of zero belongs to neither
partition. Maximum-zero declarations remain in the effective instance contract,
so defining a relationship does not require permitting its instantiation. Missing
or malformed cardinality is an explicit construction error, not a guessed default.

These are presentation conveniences holding authoritative descriptor references,
without materializing their targets or allocating an entry holon per relationship.
The `navigable_relationships()` accessor concatenates singular then plural
membership without deduplication. It reads only populated references; it does not
traverse the target lineage or classify every referenced RelationshipType by walking
that member's ancestry. Consumers needing a presentation region read the relevant
partition without another per-member cardinality-resolution operation. The accessor
does not return a public declared/inverse direction
flag. Presentation state uses relationship identity, not `direction + name`.

Instance availability remains a Rust reference-layer concern applied after
acquisition. In particular, the existing exclusion of inverse navigation for
uncommitted instances must be preserved without reclassifying the complete
vocabulary on every read. Any classification needed for that internal rule is
prepared or locally available. Partition requests preserve those lifecycle rules
and maximum-zero omission. Structural preparation retains the complete source
navigation identities and aligned declaring origins, including maximum-zero
members and original occurrence order, separately from presentation partition
order. Rehydrating a prepared schema must not zip reordered presentation members
against the original provenance sequence. The wrapper remains type-level and has no
instance field or instance-sourced schema relationship. The precise replacement
API for instance-only availability is determined by its migrated call sites;
this does not preserve the old competing effective-resolution APIs.

### 14.4 One lineage and lossless accumulation

Construction resolves the complete target `Extends` lineage once and reuses it
for all collections, navigation discovery, and related preparation. Existing
kernel Local, Additive, and Override semantics remain authoritative. Additive
schema collections concatenate ancestor contributions before local ones;
authoritative local order is preserved. Override selects the nearest nonempty
local declaration, excluding shadowed ancestors from the selected product.

For additive schema declarations, validation prohibits repeating a target
locally or redeclaring a target already declared by an ancestor. This applies
to properties, declared relationships, constraints, validation bindings, Dance
and command affordances. Validated collections are therefore already unique.
Construction accumulates without duplicate checking, deduplication, or policy
normalization. Candidate-schema duplicates remain present for validation to
reject; post-validation reads trust the invariant. No separate normalized
membership surface is needed to conceal those occurrences.

Construction is a read-time projection, not a semantic-validation boundary.
It preserves zero or multiple selected key-rule targets when encountered;
singular access reports the cardinality error, while explicit validation
retains the `1..1` commitment. Cycles, multiple Extends parents, inaccessible
references, and an ineligible construction target remain operational or
structural failures because safe projection cannot proceed.

Minimal structural and bootstrap operations use internal kernel primitives.
They do not acquire the public effective descriptor recursively. Ordinary
callers use the prepared surface, rather than choosing those primitives as a
second public path.

### 14.5 Lightweight provenance and validation

The same accumulation can retain lightweight records identifying `member`,
`declared_on`, authoritative `source_collection`, and local position. For a valid
schema, each selected additive target has one declaring origin. During
assessment of invalid candidates, repeated occurrences and their origins remain
observable. Validation can diagnose local repetition, inherited redeclaration,
placement, and name conflicts without reconstructing the target lineage.

Above-PVL validation is a primary consumer of shared effective-schema products.
It must not independently chase Extends for every rule or product. Source-schema
assessment uses the exact candidate graph and assessment-local products;
saved-schema registry entries must not substitute for staged edits. Validation
must not infer declaration evidence from a deduplicated result. A validation
finding does not become part of ordinary read-time construction.

Construction allocates one result holon and no contribution holons. There is no
public contribution-allocation option. The retained contribution schema
vocabulary does not require instances; `EffectiveContributions` remains empty.
Provenance stays lightweight in the shared computation/preparation machinery.
Its access and transport preserve one reference-backed result with private runtime
retirement metadata and must not add another target-lineage computation. SourceOf
discovery contributes navigation identities without inventing authored declaration provenance.

### 14.6 Guest preparation and local cache policy

The context/service acquisition operation chooses reuse or construction in Rust.
On a saved-schema registry miss, ClientHolonService delegates the ordinary
Space-authoritative `ConstructEffectiveHolonDescriptor` Dance to the guest.
GuestHolonService runs the shared algorithm in `holons_core`; it does not invoke
another construction Dance. The construction request, response, implementation,
and well-known names use EffectiveHolonDescriptor consistently across schema,
Rust, Commands, SDK, and documentation.

The request identifies exactly one `RequestedHolonType`. The affording holon is
the current persisted HolonSpace. Request, invocation, result, and response use
ordinary inherited OwnedBy links supplied at runtime, not a hard-coded Space in
retargetable schema imports. Source definitions are referenced rather than
cloned or eagerly transported merely to populate the result.

RelationshipDescriptor owns acquisition of its derived membership cache policy.
Its accessor acquires the RelationshipType derived result through the same
find-or-construct path as other descriptor semantics. The result contains the
final Reuse, Fresh, or bounded-age policy and any age parameter. Declared
and definitional membership resolves to Reuse; otherwise an omitted or zero
MembershipCacheMaxAgeMillis resolves to Fresh, and a positive value resolves to
bounded-age membership. Omission of that optional schema property is a resolved
Fresh policy, not an unresolved runtime policy.

Saved membership retrieval supplies the cache with the exact declared or inverse
relationship version and its already-derived final policy. Existing Session-owned
EffectiveHolonDescriptor preparation may supply the association locally: PreparedSchema
provides the name and scalar policy, paired with the exact saved ID from retained
relationship references. This projection uses guarded accessors, does not hydrate
descriptor targets, and never reconstructs IDs from display identity strings.
The existing guest membership request performs any still-necessary descriptor binding
and obtains policy through RelationshipDescriptor; it returns both with the targets,
including for empty membership. This must not require a separate host-to-guest schema discovery
sequence. The host retains that association and a small scalar policy in the same
cache entry. Policy lookup itself is local: no descriptor acquisition, ancestry
traversal, reference resolution, or guest calls, including on the first read.
Membership expiry and explicit freshness reuse the retained association and policy;
they do not repeat descriptor binding.

For a descriptor source H, guest binding includes the complete declared contract
of D(H) and outbound relationship definitions indexed by SourceOf along L(H).
An endpoint-filtered navigation projection of D(H) alone is insufficient: an
explicit meta-type declaration can govern H even when its SourceType is in L(H)
rather than L(D(H)). Descriptor-specific outbound inverses such as ValueTypeFor
retain their own direction-specific policy. Distinct applicable identities sharing
a name remain ambiguous. This does not change the navigation partition contract.

There is no separately authoritative source-type/name-to-policy table, and a local
policy miss must not start schema discovery. Ordinary client membership responses
must supply an authoritative descriptor association for names not already resolved
by retained or applicable prepared associations; binding or acquisition failures
remain explicit errors. A descriptor source whose declared instance contract includes Extends continues
to use guest binding for unresolved policies, preserving the additional candidates
from its own ancestry. Prepared name enumeration can still be reused. Named reads
consult preparation using only resident, unexpired DescribedBy membership; a policy
miss does not initiate source-type discovery. Release relationship-cache locks before retrieval. The
cache consumes the supplied scalar without deriving policy again.

Foundational policies required by construction's own reads remain locally
available before preparation and break recursive policy dependencies. Bootstrap
exemptions are explicit and bounded; ordinary post-bootstrap reads use their
resolved descriptor policies. Guest request-local membership reuse remains
independent of host descriptor discovery. Explicit freshness changes membership
retrieval, not schema-policy preparation. HolonType prepared navigation may carry
compact final policy projections for its relationship identities; those values
come from RelationshipDescriptor acquisition rather than a second derivation
algorithm or policy authority.

The runtime retains normal request binding and structural safeguards. It does
not run semantic source validation or a second conformance pass over its own
result or response. The existing bounded explicit-conformance accommodation for
descriptor-valued endpoints remains: the five effective vocabulary endpoints
and ContributionCollection retain their semantic category targets until general
endpoint eligibility can express them. The accommodation is not eager validation
and does not widen endpoints. Guest-local construction below 200 ms remains a
design target, distinct from host transport time and observed benchmark results.

### 14.7 Participation in the space Session

The [space Session specification](../space-session-design-spec.md) owns Session
identity, lifetime, reset, local-commit adoption, and concurrency boundaries.
HolonSpaceManager coordinates that lifecycle. The descriptor subsystem owns
registry contents and acquired result handles, not a separate Session definition.

Registry entries are keyed by exact saved descriptor identity and isolated by
Session and runtime space. Independent wrappers and public transactions share
completed results in that registry. A restricted retained derived-state
transaction owns the transient products. References retain their actual owner;
temporary IDs are not rebound into the caller's public transaction.

The retained owner permits reads, transient construction, and sealing, but not
staging, persistence, Commit, public mutation, or recoverable public work.
Private cache-read frames remain operation-bounded and cannot own results after
public acquisition returns. Host retention spans guest requests; guest WASM
state remains request-local. Registry lifetime must not create ownership cycles
or retain unrelated public pools, and construction envelopes require cleanup.

Reacquisition performs ordinary reference reads under existing relationship cache
policies; retiring a derived result does not invalidate or override its inputs.
Coordinate acquisition and publication with the space Session boundary. Publish
only complete sealed results and coherent prepared policies. Release registry
locks before graph reads or Dance invocation. Retired-session work cannot publish
into the active Session. Hits require neither reconstruction nor new transport.

Registered results reference the Session's shared retirement token. Every
semantic accessor checks it. Direct reads of retired results report the specific
obsolete condition. Ordinary descriptor wrappers discard an obsolete private
handle, reacquire through the same mechanism, and retry; other errors propagate.
The private memo must support replacement rather than permanently pinning an
obsolete result. Runtime validity metadata is not serialized into schema state.
Raw backing-holon access is internal to construction, registry, and transport
responsibilities; ordinary consumers cannot bypass retirement through it.

Staged/transient sources, and derivations whose dependency references include
volatile state, do not enter the saved Session partition. A saved source ID alone
does not establish eligibility. Frozen candidate inputs may reuse results in the
validation scope below, without replacing candidate edits with saved projections.
Explicit pull follows whole-session reset; there is no independent per-descriptor
adoption path retaining old registered results.

#### Prepared-product input changes

Local Commit may preserve the space Session when its completed effects are proven
independent of prepared descriptor inputs. Space Session owns the verdict's
lifecycle and failure semantics; descriptor construction owns the input inventory.
The watched relationship collections are Extends; InstanceProperties,
InstanceRelationships, AffordsDance, AffordsCommand, InstanceKeyRule; Constraints,
ValidationBindings, AffordsOperator; SourceType, SourceOf; and DescribedBy.
This includes navigation discovery, direct cardinality interpretation, inherited
commitments, native-kind/error projections, and prepared relationship policies.
Changes to the shared constructors' input surface require corresponding inventory
and invalidation-policy reconciliation.

Ordinary Instances, OwnedBy/Owns, and Predecessor/Successor memberships do not
by themselves change these prepared products. Exact saved property content does
not change when a new version is published. The narrow DescribedBy initialization
exception is specified by Space Session; it does not exempt other watched writes
on freshly published sources. Effect accounting observes actual forward and
inverse persistence names, including SourceOf writes onto unstaged saved types.
Registry membership and IsDefinitional alone are not sufficient predicates.

### 14.8 Commit registry transport and guest acquisition

A host Commit transports two transaction-state snapshots: the agent transaction
containing the subjects to commit, and the Session's restricted registry-owning
transaction containing prepared result graphs. Transport the registry root
identity explicitly with its owner's state. Project runtime references to the
existing wire representations and bind them at guest ingress; do not serialize
live transaction objects, locks, or bound handles. Do not clone the Session's
registry/results into the agent transaction's transient pool as a transport carrier.

Restore both transaction states within the same request-local guest space while
preserving their distinct transaction identities and pools. The received registry
retains its restored owner, and the guest space exposes it through the ordinary
space-bound acquisition capability. Ordinary saved-reference EHD and DD accessors
therefore consult the received registry through their existing acquisition path;
validation does not require a second context-specific acquisition API. The agent
transaction remains the transaction against which Commit executes.

Reconstruct the registry's descriptor-ID indexes once at guest Commit ingress from
the transported root's selected results. Each EHD supplies its exact described
type; each DD supplies its source through its self-first lineage. Index rebuilding
uses only transported transient state and saved reference identities, with no
storage retrieval, Extends walk, semantic acquisition, or source hydration.
Duplicate/conflicting entries and missing result references are explicit ingress
errors. Do not transmit a redundant descriptor-ID index or rebuild one per accessor.
Registry-owner transport and ingress index reconstruction are specific to Commit;
ordinary guest reads do not incur them.

Admission to the saved Session registry requires saved references for all actual
schema dependencies, including each result's describing type. Recheck that
invariant at capture. Staged references, including committed staged handles, and
transient dependencies cannot be smuggled into the saved partition by transporting
another owner. Frozen candidate results use their separate validation scope.

Descriptor Runtime Schema defines the keyless registry and its selected EHD/DD
collections. HolonType PreparedSchema retains lightweight declaring-origin and
navigation metadata and may project final relationship policies acquired from
RelationshipType results. Prepared products are reference-backed and contain
neither validation outcomes nor eagerly hydrated source/target graphs.

Guests are stateless across requests. The received graphs belong to that guest
execution; subsequent host reset cannot retire them. Capture must observe one
coherent selected host registry and owner state or retry across retirement.
Returning the agent transaction's pools must not rebind or republish the received
registry-owner state into the active host Session. Ordinary Commands preserve
actual owner identity and do not expose registry infrastructure for public mutation.

#### Per-reference reuse and validation acquisition

**Saved-product reuse is decided per reference, not per assessment.** Registry lookups apply only to
exact saved identities; staged candidates compute candidate-local products. An affected-Schema workset does not disable saved-product reuse. Saved-schema registry entries
never substitute for staged edits (§14.5). The per-reference rule is
sufficient because:

- registry entries are keyed by exact saved identity and admit only saved dependencies;
- staged candidates have their own identities and cannot match a saved entry;
- no-op and graph-only candidates share their saved source's identity, but graph-only changes affect
  only non-definitional collections, and every effective-schema input (`InstanceProperties`,
  `InstanceRelationships`, `AffordsDance`, `AffordsCommand`, `InstanceKeyRule`, `Constraints`,
  `ValidationBindings`, `Extends`, and `ValueType`) is definitional;
- registered products are lossless, retaining repeated contributions and declaring origins.

**HolonType acquisition level.** Validation consumes the shared effective-schema computation for
HolonType: restoration from registered EffectiveHolonDescriptor results for saved definitions, and
the same kernel computation that EffectiveHolonDescriptor construction runs before materialization
for candidates. Materialization adds navigation partitions, which validation does not consume, and
reads every navigable relationship's cardinality to build them; malformed cardinality there remains
a construction error under descriptor specification §14.3. Validation therefore does not materialize
candidate EffectiveHolonDescriptor results, and Commit gains no exposure to that error. This is the
same computation, not a second derivation path. Saved entries were materialized successfully at
publication.
The shared runtime retains an unmaterialized computation entry point for validation.

### 14.8.1 Frozen validation scope

TransactionContext marks entry into validation before descriptor preparation and
owns a request-local reuse scope for frozen staged/transient descriptor inputs.
Preparation and validation do not mutate those inputs. Construction of derived
output holons remains permitted; frozen inputs do not imply a blanket prohibition
on transient-pool writes. There is no universal Session synchronization barrier.

The single accessor-embedded acquisition path consults this scope before
constructing a candidate-derived result. Independently created wrappers reuse a
completed result by exact transaction-local source identity. Do not collapse a
staged candidate into its saved predecessor or reuse a result built for a different
candidate graph. All supported products share the same construction algorithm and
one resolved lineage; an already diagnosed lineage can supply construction without
another walk. Structural diagnosis of malformed input retains its own evidence
and error semantics and is not replaced with a successful cached classification.

Outside the frozen validation phase, mutable-source acquisition constructs fresh
results. Validation exit on success, rejection, or operational error retires its
shared scope token and releases its selected entries. Wrapper-private memos cannot
serve results after retirement; ordinary acquisition uses the current scope or
fresh behavior. Direct holders report the obsolete condition. A corrected retry
starts a new scope. These rules require neither per-holon mutation generations nor
new fields on SmartReference or StagedHolon.

Saved-derived results are acquired through the installed guest-space registry;
frozen candidate results retain the agent transaction as their owner. Validation
packages may retain diagnostics and projections, but do not become a competing
acquisition authority. Saved products never override staged candidates, and
validation outcomes remain specific to the assessment.

### 14.9 Lazy derived acquisition and shared carriers

ValueDescriptor, PropertyDescriptor, RelationshipDescriptor, and HolonDescriptor
retain their authoritative HolonReference and privately memoize a typed derived
handle. HolonDescriptor uses EffectiveHolonDescriptor, which specializes the common
DerivedDescriptor handle; the other supported categories use DerivedDescriptor.
The memo is runtime-only and is never serialized. Ordinary inherited accessors acquire the handle on first
use; callers do not separately construct a derived object. The common acquisition
and Session-participation contract applies across descriptor categories; their
prepared payloads are listed below.

DerivedDescriptor is a sealed transaction-bound transient holon. It records a
self-first DerivedLineage and ancestor-first DerivedConstraints,
DerivedValidationBindings, and DerivedOperators collections. PropertyType consumers
use constraints and validation bindings; ValueType consumers additionally use
operator affordances. DerivedValueKind holds the native-kind projection computed
from the nearest local Instance TypeKind anchor in that same lineage. The
construction algorithm resolves Extends once and uses the same lineage and
kernel additive rules for all products. Duplicates and order
remain observable. DerivedOrigins stores collection-aligned indexes into
DerivedLineage, retaining declaring provenance without allocating contribution
holons or serializing bound runtime references as property values.

A separate identity-indexed partition of the existing session registry retains
saved-derived results. It shares the retained transaction, reference admission,
construction serialization, envelope cleanup, and disposal rules of the HolonType
partition. Independent wrappers for one exact saved descriptor reuse the completed
result. Failed acquisition leaves the wrapper unpopulated and is retryable. An
acquired handle checks Session retirement and owner disposal; ordinary wrappers
recover from retirement through replacement acquisition.

ClientHolonService delegates ConstructDerivedDescriptor as an ordinary typed,
Space-authoritative Dance. GuestHolonService executes the shared algorithm locally.
The request identifies RequestedDescriptor, whose endpoint is TypeDescriptor; the
response carries DerivedDescriptor through existing transient-pool transport.
Saved Session publication requires every schema dependency, including lineage
and result describing type, to be saved. Commit transports that registry's owning
transaction and installs the received registry as specified in §14.8.

Staged/transient source descriptors acquire through the same path. During frozen
validation, results can populate the validation-owned lookup and wrapper-private
memo with the scope's retirement token. Outside that phase they construct fresh
transaction-local products. This provides bootstrap/Commit reuse without stale
editing-time memoization, per-holon mutation generations, or a separate validator
acquisition path. Local metadata accessors and defaults preserve their kernel
semantics independently of derived-state acquisition.

All ordinary ValueDescriptor inherited semantic accessors acquire the derived
handle: constraints, validation bindings, operator enumeration, exact operator
membership, name lookup, native value-kind classification, and array
classification. Membership compares exact afforded identities; it never grants
an operator implicitly through its ancestry. Subtype affordance helpers delegate
to those same accessors. ValueDescriptor does not retain a competing Extends walk.

Preparation computes value kind using the already resolved lineage. A semantic
classification error is retained as that product's error without preventing
other structurally readable products from being consumed. Operational read errors
abort construction and remain retryable; they are not published as classification
results. Subsequent kind reads use the prepared property, not ancestor metadata.

Foundational construction/validation may use the explicitly named kernel primitive
classify_value_kind_for_validation before the derived result schema is available.
That primitive and derived preparation share one classification implementation;
construction must not recursively acquire itself to classify its inputs. Once
preparation is available, ordinary validation consumes derived kind, constraints,
bindings, and eligible lineage-based compatibility through the normal descriptor
accessors. Reuse diagnosed structural evidence within an assessment without
suppressing malformed-graph diagnostics. The frozen scope in §14.8.1 governs
mutable-source reuse; foundation-only primitives are not a competing ordinary API.


### 14.10 Derived payload inventory by descriptor kind

This inventory owns the payload contract. Rust doc comments on the corresponding
wrappers/results mirror it. All products of one acquisition share one resolved
self-first Extends lineage; each product retains its kernel inheritance policy,
precedence, duplicate occurrences, ordering, and errors. Fully populated means all
supported products are prepared, not that their referenced targets are hydrated
or that validation has succeeded. Product-specific semantic errors may be retained;
operational failures abort preparation without publishing a successful partial entry.

| Descriptor kind | Prepared semantic payload | Supporting payload / exclusions |
| --- | --- | --- |
| HolonType | Instance properties; declared instance relationships; singular and plural navigable relationships (combined accessor preserves occurrences); afforded Dances; afforded Commands; constraints; validation bindings; effective instance key rule; effective Instance TypeKind | Exact described type, prepared relationship policies and declaring origins. Navigation excludes maximum-zero occurrences. The two navigation partitions are projections, not separate inherited vocabularies. |
| ValueType | Effective Instance TypeKind; native value-kind classification (including array classification); afforded operators; constraints; validation bindings | Self-first lineage and per-occurrence declaring origins. Native value kind is distinct from the general TypeKind projection. Enum variants and array element declarations retain their local kernel semantics. |
| PropertyType | Effective Instance TypeKind; constraints; validation bindings | Self-first lineage and per-occurrence declaring origins. Property name, requiredness, and ValueType are fixed concrete declarations, not inherited override products. Abstract property families can contribute constraints and bindings; concrete properties cannot be extended. |
| RelationshipType (declared and inverse) | Final membership cache policy: Reuse, Fresh, or bounded age with its age parameter | Exact relationship identity; direction and definitional inputs; inherited MembershipCacheMaxAgeMillis resolved from one lineage. Declared/inverse policies remain distinct. Omitted maximum age resolves to Fresh unless declared-definitional Reuse applies. Local source/target declarations remain references; this contract does not imply eager target hydration or inheritance of every relationship field. |

Effective Instance TypeKind uses the nearest self-first lineage descriptor with
local explicit DefinesInstanceTypeKind=true, according to the kernel rules.
TypeDescriptor itself has no Instance TypeKind. Retain enough anchor identity for
the established TypeKind projection; do not conflate it with DerivedValueKind or
introduce authored TypeKind state.

For HolonType, EffectiveHolonDescriptor specializes the shared derived-result handle.
The same resolved lineage populates DerivedLineage and DerivedInstanceTypeKind;
its specialized effective collections and PreparedSchema remain authoritative for
HolonType semantics. The inherited carrier's unused category collections are empty;
this does not add operator, native-value, or relationship-policy semantics to HolonType.
Both registry partitions attach the shared space Session retirement token. Mutable
HolonType products use the same frozen-validation scope, with a typed result slot;
independent wrappers reuse one complete result during that scope. Explicit pull resets
the whole Session and reacquires the same exact described version. Command narrowing
recovers the selected result's token and cannot revive an old Session-owned result.
Generic SDK relationship reads on a registry-owned carrier also check current
admission and Session retirement at the command boundary. Reset revokes all
admitted result identities from the old Session, including superseded publications;
unpublished construction carriers remain internal. These checks perform no schema
discovery or storage reads.

For ValueType and PropertyType, the reference-backed result carries DerivedLineage,
DerivedConstraints, DerivedValidationBindings, and collection-aligned DerivedOrigins.
DerivedInstanceTypeKind stores the optional anchor index into DerivedLineage or
its semantic resolution error. ValueType also consumes DerivedOperators and
DerivedValueKind. The shared carrier
can contain unused products for another category; that does not make them additional
PropertyType semantics. Session validity is private runtime metadata, not a property
on the transient result holon. Validation-scope validity is likewise runtime-only.

The runtime carrier's DerivedRelationshipPolicy property encodes an optional
product containing direction and final membership policy (including bounded age),
or its product-specific semantic error. Non-relationship categories carry no
relationship-policy product. RelationshipType construction leaves the carrier's
unused value/property collections empty; it does not read those collections to
prepare policy. Failed storage/reference reads abort construction as usual.

RelationshipType cache policy is acquired through its wrapper and retained in the
derived result. Exact wire/schema encoding of this additional product is an
implementation decision; its semantic ownership and the hot membership-hit policy
check are defined in §14.6.

Other descriptor categories have no payload contract established here. Adding a
category requires an explicit inventory rather than assuming all of its fields
inherit or treating a generic carrier's fields as category semantics.

### Key composition boundary

Descriptor Runtime gathers semantic key inputs through the existing descriptor facades and shared
descriptor kernel. Composition formatting is pure and WASM-safe over typed, already-resolved
inputs. Loader assembly, runtime composition, and Commit assessment share this semantic resolution
path; they do not introduce a separate key resolver or semantic IR. In particular, semantic key
resolution does not belong in `map_schema_semantic`.

## 15. Definition and Extension Governance

Runtime recognition of a descriptor category does not decide who may define or
extend that category.

Schema ownership, Extension Schema compatibility, authorization, and
core-controlled descriptor branches are governance concerns. They must not be
inferred from:

- the availability of a Rust wrapper;
- a cached or projected `TypeKind` value;
- a hard-coded facade inventory; or
- whether runtime code can technically construct a descriptor holon.

The type-system Extension Schema design owns structural extension rules. The
relevant authorization boundary owns permission to create or activate a
definition.

## 16. Ownership Summary

| Concern | Owner |
|---|---|
| Descriptor structure and schema invariants | Type system schema design |
| Exact descriptor declarations | Core and component TDL schemas |
| Effective-specification, contract, inheritance, key-rule, and conformance algorithms | Descriptor kernel |
| Descriptor-driven holon-validation orchestration | Validation framework |
| Descriptor-independent Integrity validation | PVL |
| Holon lifecycle and shared in-memory state | Shared objects layer |
| Uniform transient, staged, and saved access | Reference layer |
| Descriptor resolution and typed runtime interpretation | Runtime descriptor subsystem |
| Kernel invocation through `HolonDescriptor` and reference-layer access | Runtime descriptor subsystem |
| Default materialization | Descriptor-default materialization service |
| Commit, rollback, and version production | Transactions |
| Relationship occurrence storage | Transactions and storage |
| Command execution | Commands |
| Dance execution | Dances |
| Query execution | MAP Queries |
| Validation orchestration outside kernel conformance | Validation |
| Source syntax and source diagnostics | TDL, JSON, or other source adapters |

## 17. Explicit Non-Responsibilities

The runtime descriptor subsystem does not own:

- schema structure or exact descriptor inventories;
- TDL or JSON parsing;
- source-level shorthand;
- graph construction or reference authoring;
- default materialization;
- transaction lifecycle or persistence;
- relationship occurrence encoding or inverse repair;
- command, dance, query, or operator execution;
- PVL rules or integrity-layer validation;
- schema migration sequencing;
- domain authorization policy;
- code-generation workflow; or
- implementation-plan sequencing.

Its focused responsibility is to make descriptor holons and kernel-defined
semantics available through the core holonic runtime without creating a second
semantic model or weakening reference-layer encapsulation.

## 18. Related Documents

- [MAP Schema Design Spec](../../type-system/schema-design-spec.md)
- [Descriptor-Kernel Semantic Rules](../../type-system/descriptor-semantics-rules.md)
- [Layered Descriptor Architecture](../../descriptors/layered-desc-arch.md)
- [Holon Layered Representation Design](../../architecture/holon-layered-representation-design-spec.md)
- [Holons Shared Objects Layer Design](../../architecture/holons-shared-objects-layer-design-spec.md)
- [MAP Runtime Shared Types](../runtime-shared-types.md)
- [MAP Commands](../../commands-and-runtime/commands.md)
- [MAP Dances](../../dances/dances-design-spec.md)
- [MAP Validation Architecture](../../validation/validation-arch.md)
- [MAP Core Document Role Manifest](../../document-role-manifest.md)

The prior facade-oriented draft remains at
`docs/core/descriptors/descriptors-design-spec.md` for comparison during the
documentation refactor. It is not authoritative for this target design.
