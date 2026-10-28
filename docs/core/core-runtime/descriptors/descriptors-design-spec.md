# MAP Runtime Descriptor Subsystem Design Spec (v2.0)

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
7. This specification defines the runtime descriptor subsystem and its
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
they were computed. Any mutation, including descriptor-default
materialization, invalidates affected products. Final validation evaluates the
completed graph snapshot.

The transaction-scoped EffectiveDescriptor defined below consolidates several
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

### 14.1 EffectiveDescriptor — canonical definition

An **EffectiveDescriptor** is a transient Holon representing the effective
schema of one particular HolonType, resolved according to MAP's inheritance
and relationship semantics. Its relationships identify the authoritative
schema Holons contributing to that effective schema. It is derived information,
not an independently persistent schema definition, and construction requires
no instances of the described HolonType.

Descriptor Runtime Schema owns the result/contribution types, all their
relationship pairs, the position property, and the construction Dance and its
request/response contracts. It depends directly on Core, Dance, and Commands.
All eight effective collections are declared directly in
`EffectiveDescriptor.HolonType.InstanceRelationships`; no external inverse
`InstanceRelationshipFor` occurrences extend that contract. These schema ownership
boundaries do not move the shared runtime algorithm out of `holons_core`.

The two typed wrappers have different subjects:

| Wrapper | Wrapped Holon | Responsibility |
|---|---|---|
| `HolonDescriptor` | An authoritative HolonType definition, including a readable staged definition | Local descriptor reads and kernel-backed effective access |
| `EffectiveDescriptor` | A transaction-scoped, typed `TransientHolon` | Read already-resolved effective collections |

Both follow MAP's typed-wrapper pattern. Neither creates a parallel
authoritative data model. `DescribedHolonType` identifies exactly one target
HolonType `T`; `DescribedBy` identifies the result's own type,
`EffectiveDescriptor.HolonType`. These targets are distinct. The result does
not replace `T` or become the `DescribedBy` target of `T`'s instances.

Consolidated schema interpretation, a unified type-level navigation vocabulary,
and elimination of repeated inheritance traversal justify this architecture.
Guest-side construction is useful independently of the unresolved Holochain
0.7.1 invocation-overhead investigation or any measured `call_zome` latency.

### 14.2 Holonic surface and effective collections

The [result schema contract](../../type-system/schema-design-spec.md#85a-effective-descriptor-result-schema)
defines the result type and its distinct relationship types. Conceptually:

```text
EffectiveDescriptor (TransientHolon)
  DescribedBy                 -> EffectiveDescriptor.HolonType
  DescribedHolonType           -> Person.HolonType
  EffectiveInstanceProperties  -> Name.PropertyType, BirthDate.PropertyType
  EffectiveInstanceRelationships -> LivesAt.DeclaredRelationshipType
  NavigableRelationships      -> LivesAt.DeclaredRelationshipType,
                                 ResidentOf.InverseRelationshipType
  EffectiveAffordsDance        -> SomeDance.DanceType
  EffectiveAffordsCommand      -> command descriptors
  EffectiveValidationBindings  -> ValidationRule holons
  EffectiveConstraints         -> Constraint holons
  EffectiveInstanceKeyRule     -> the selected KeyRule target
  EffectiveContributions      -> empty; provenance remains in computed occurrence records
```

The initial surface includes all eight requested collections:

| Collection / wrapper accessor | Result relationship | Meaning |
|---|---|---|
| `instance_properties()` | `EffectiveInstanceProperties` | Effective property declarations |
| `instance_relationships()` | `EffectiveInstanceRelationships` | Effective declared instance relationship contract |
| `navigable_relationships()` | `NavigableRelationships` | Outbound declared and inverse RelationshipType vocabulary |
| `afforded_dances()` | `EffectiveAffordsDance` | Effective Dance affordances |
| `afforded_commands()` | `EffectiveAffordsCommand` | Effective command affordances |
| `effective_validation_bindings()` | `EffectiveValidationBindings` | Effective validation commitments, distinct from constraints |
| `effective_constraints()` | `EffectiveConstraints` | Effective adopted constraints |
| `effective_key_rule()` | `EffectiveInstanceKeyRule` | Nearest populated key-rule declaration under Override |

No collection in this table is deferred. Operator affordances, deletion-policy
aggregation, and resolved property values or member-definition products beyond
these collections are outside the initial surface. Consumers continue to use
existing descriptor accessors for them. Referenced descriptors' metadata,
endpoint declarations, cardinalities, defaults, and property values are read
from their authoritative Holons; they are not flattened or copied into the
result. `EffectiveAffordsDance`, for example, records the described type's
resolved affordances; it does not afford those Dances to the result Holon.

### 14.3 NavigableRelationships

For HolonType `T`, the normative definition is:

```text
Lineage(T) = {T} union Ancestors(T)
NavigableRelationships(T) = { R | SourceType(R) in Lineage(T) }
```

Thus both declared and inverse RelationshipTypes participate. `SourceType`
comparison uses descriptor definition identity, not type name, key equality,
or implicit replacement by a staged successor.

Five concerns remain distinct:

- **Navigability:** the schema-defined RelationshipTypes that may be followed
  outbound from instances of `T`.
- **Declaration:** the effective `InstanceRelationships` contract contains
  declared RelationshipTypes only.
- **Direction:** a RelationshipType is declared or inverse; an inverse is a
  first-class outbound vocabulary item from its own source type.
- **Updateability:** direction and the applicable mutation and authorization
  rules determine whether authors may modify a relationship. Navigability
  grants no update authority.
- **Instance realization:** actual occurrences on an individual Holon are
  outside EffectiveDescriptor. Construction never inspects such instances.

For committed, fully indexed schema, discover RelationshipTypes using the
existing `SourceOf` inverse of `RelationshipType.SourceType`, at `T` and each
ancestor. No new index is introduced. Both directions found there participate;
effective declared RelationshipTypes also come through the inherited
`InstanceRelationships` contract. Union these discovery paths by descriptor
identity for the navigable set, checking source eligibility. Equal names do
not merge distinct definitions or excuse existing declaration/ambiguity errors.
Canonical membership is SourceType-based, not defined by the discovery path.

For staged schema, retain declared RelationshipTypes available through the
effective `InstanceRelationships` contract, including staged declarations.
Include materialized inverse RelationshipTypes available through `SourceOf`.
Inverses of staged declarations that have not been materialized are absent;
do not synthesize them from `HasInverse`, `InverseOf`, or endpoint swapping.
An unsaved descriptor with no materialized inverse-index entries is a valid
construction input and does not cause `UnsupportedStagedTraversal`. Available
saved-ancestor indexes must still be examined. This lifecycle-aware discovery
rule is intentionally incomplete relative to the fully indexed committed
vocabulary. It does not relax malformed endpoints, graph-access failures, or
inheritance errors into empty results.

These staged rules concern RelationshipType definitions. They establish no
instance-level staging, availability, cardinality, or mutation rule. Existing
instance-level `available_relationships()` and relationship realization remain
separate operations.

### 14.4 One lineage, existing inheritance semantics

Construction must resolve and structurally validate the complete `Extends`
lineage of `T` exactly once, then reuse it across all collections and
`SourceOf` discovery. It must reuse the descriptor kernel's inheritance rules,
not introduce another inheritance engine:

```text
lineage = resolve complete Extends lineage(T)
for each effective member:
    resolve using existing policy and already-resolved lineage
navigable = discover using lineage and resolved declared contract
populate one typed transient result; retain lightweight occurrence provenance
```

Single inheritance, cycle detection, multiple-parent detection, Local,
Additive, Override, authoritative local order, ancestor-before-local additive
order, collection normalization, duplicate policies, and structural errors
remain governed by the
[descriptor-kernel rules](../../type-system/descriptor-semantics-rules.md#3-job-two-compute-effective-semantic-inheritance).
Construction is a read-time projection, not a schema-validation boundary.
It preserves raw inherited occurrence evidence for validation and diagnostics;
normalizing direct products must not erase that evidence. Override retains the
nearest nonempty declaration. Construction does not reject a missing or
multiply populated effective key-rule selection: the projected relationship
retains its normalized membership, and the singular `effective_key_rule()`
accessor reports missing/multiple-target errors when consumed. The `1..1`
schema contract remains a validation commitment. Cycles, multiple Extends
parents, inaccessible references, and an ineligible target remain construction
errors because projection cannot safely proceed.

Factor shared inheritance logic into internal operations that accept an
already-resolved lineage. Existing `HolonDescriptor` accessors remain available
and delegate to that same semantic logic. Individual Local reads and
short-circuiting Override or classification queries need not eagerly walk the
whole lineage. The once-only requirement applies to the target lineage during
EffectiveDescriptor construction; validating other referenced descriptors may
require their own lineages.

Construction reads a coherent graph snapshot. Mutating a contributing definition,
lineage, or applicable source index makes the derived result stale; construct a
new result before consuming changed schema. Transaction scope alone does not
make a result fresh. No mutable automatic refresh cache is implied.

### 14.5 Contributions and provenance

The computed effective schema retains provenance as lightweight reference-valued
occurrence records. Each selected declaration occurrence must retain:

| Field | Meaning |
|---|---|
| `member` | Exact bound reference to the contributed definition or configured instance |
| `declared_on` | Exact bound reference to the declaring type in the resolved lineage |
| `source_collection` | Identity of the authoritative collection, not its derived result counterpart |
| `local_position` | Zero-based position within that declaring type's selected local sequence |

Positions are local to their declaration source, not a global sequence number on
the effective result. Existing constraint and validation-binding consumers can
project `EffectiveRelationshipMember` values from those records without
allocating transient Holons.

Raw occurrence sequences preserve repeated targets, ancestor/local origins,
conflicts, and local defects for validation and diagnostics. They are captured
before normalizing direct result membership. Source collection ordering and
duplicate policy govern the direct product: duplicate-free products retain the
first occurrence by exact definition identity, while duplicate-allowing products
retain the corresponding multiplicity. Normalization must not erase the raw
occurrence evidence supplied to validation.

Construction must allocate exactly one EffectiveDescriptor result Holon and must
not allocate EffectiveSchemaContribution Holons. Ordinary Dance request,
invocation, and response Holons are separate transport machinery. There is no
public provenance-allocation option at the Dance, service, Commands, or SDK
boundary. `EffectiveContributions` must remain empty; its existing schema
vocabulary does not require constructing instances. Consumers needing declaring-origin
evidence use the computed projection's occurrence records. Neither result
accessors nor provenance consumers reconstruct that evidence by traversing the
target's Extends chain again. The records remain bound to their computed
projection and transaction lifetime. Materializing or transporting an
EffectiveDescriptor does not transport these records or promise public provenance
access through the result handle. Consumers requiring provenance retain and use
the computed projection.

A navigation-only RelationshipType found through SourceOf contributes to the
navigable identity set, not to the inherited occurrence sequence. Index discovery
must not invent a declaring-origin contribution.

### 14.6 Typed wrapper and guest construction Dance

The typed `EffectiveDescriptor` wrapper holds one encapsulated
`HolonReference`. Narrowing checks the result's describing type and readable
transient lifecycle. Typed collection accessors read already-populated result
relationships and narrow their targets to the appropriate wrappers. They do
not traverse `T`'s lineage or keep parallel cached vectors or maps. Ordinary
requiredness, cardinality, narrowing, and reference-access errors remain
observable. A successfully constructed result is read-only to consumers.

Descriptor-valued endpoints express descriptor-category membership (future
`SubtypeOf` eligibility), while configured-instance endpoints express `InstanceOf`
eligibility. The existing describing-type-only endpoint validator cannot express
all descriptor-category contracts. Until generalized endpoint eligibility is
implemented, explicit descriptor-backed conformance defers only the target
checks for:

- `EffectiveInstanceProperties`;
- `EffectiveInstanceRelationships`;
- `NavigableRelationships`;
- `EffectiveAffordsDance`;
- `EffectiveAffordsCommand`; and
- `ContributionCollection`.

The accommodation matches the canonical result/contribution describing type and
canonical relationship identity. It applies only when explicit descriptor-backed
conformance is requested; it does not add validation to construction or ordinary
result reads. Other endpoint, cardinality, property, and lifecycle contracts
remain enforceable by explicit validation. The bounded accommodation does not
widen schema endpoints or introduce generalized endpoint eligibility.

Construction is a performance aid with a target below 200 ms for guest-local
construction, distinct from end-to-end host/Dance/transport time. This is a design
target, not a guaranteed or demonstrated bound. The runtime validates its request
and retains structural traversal and target-eligibility safeguards. It does not
run source-schema semantic validation or a second conformance pass over its
internally generated result or response. Schema conformance and semantic
validation remain separate operations, including enforcement of the effective
key-rule cardinality. Construction allocates no contribution Holons. Neither
key-rule representation conversion nor response-body contract redesign belongs
to this construction operation.

EffectiveDescriptor construction is a transaction-scoped operation mediated by
`HolonServiceApi`. The caller uses the construction operation exposed through
`TransactionContext`; its environment-specific service supplies execution:

- **Host:** `ClientHolonService` constructs the typed request and invokes the
  `ConstructEffectiveDescriptor` Dance through the existing Dance transport.
  The host does not populate products locally or issue a separate construction
  request for each product.
- **Guest:** `GuestHolonService` invokes the shared construction algorithm
  directly, using the current guest transaction. Lineage resolution, effective
  product population, and lightweight occurrence capture all execute in the
  guest before the result is returned.

The guest Dance handler enters the same service-mediated construction operation
through its guest-bound `TransactionContext`. Its `GuestHolonService` executes
locally rather than invoking the Dance again. Context-specific delegation
belongs in the service implementations; the generic Dance executor does not
own construction-specific routing.

The construction algorithm belongs in `holons_core`, which is shared by host
and guest. That placement does not determine where a call executes. Public
runtime callers use the service-mediated operation rather than calling the
local algorithm as an alternative construction path. The service boundary
keeps guest-side population independent of the caller's execution context.

`ConstructEffectiveDescriptor` is the name-addressed, guest-executed Dance used
by the client service, with `RequiredExecutionContext = SpaceAuthoritative`.
Its schema integration uses the
[ordinary Dance contract](../../dances/dances-design-spec.md):

- `HolonSpace` affords the Dance through the generic `AffordsDance` pair.
- A typed transient `ConstructEffectiveDescriptorRequest` carries exactly one
  `RequestedHolonType` reference to `T`. The affording space and request are
  distinct; no instance of `T` is required. There is no contribution-allocation option.
- The Dance's `RequestType` names that request type; `Response` names
  `ConstructEffectiveDescriptorResponse`, whose `ResponseBody` contract is
  `EffectiveDescriptor.HolonType`.
- Its implementation binds through `ForDance` and enters the transaction's
  service-mediated construction operation. The guest service uses that same
  transaction to resolve the target lineage, compute collections, and allocate
  and populate one typed transient EffectiveDescriptor result.
- The typed request, invocation, result, and response
  explicitly identify the current persisted HolonSpace through inherited `OwnedBy`
  before publication. This satisfies the existing required ownership cardinality;
  transient assembly does not materialize persistent inverse `Owns` occurrences.
- The successful response carries the result through normal Dance response
  binding and transaction-state projection. No partial result is published as
  success; failures use the existing Dance error boundary.

The client service returns reference-backed access to the guest-produced
transient graph through the existing host/guest transport. Host-side invocation
preparation and later descriptor reads may still use normal reference services;
they do not relocate effective-product population to the host. A retained consumer result
must belong to the caller's retained transaction, not a private cache-read
frame that is disposed at the end of one read. Ordinary Dance request binding
and contract checks remain in the shared execution path; the generated result
and response are not subjected to another conformance pass.

### 14.7 Lifetime, identity, caching, and limits

The result is transaction-scoped, held by the
normal transient manager and unavailable after its disposal. Transaction scope
follows the [transaction lifecycle](../../transactions/transactions-design-spec.md#7-lifecycle-and-operation-policy),
including retained transient-pool access where supported after Commit.
Results are not staged or committed as authoritative schema definitions.

Relationships retain the authoritative targets' normal reference identities.
Saved descriptors may already be held in the Space's cross-transaction Holon
cache; staged definitions remain bound to their transaction. Descriptor state
is not cloned into transient descriptor copies. Existing reference binding,
cache retention/freshness, and transaction-state transport suffice; this
feature introduces no cache synchronization, special host hydration, cache
deltas, or cache lifecycle rules.

The boundary excludes persistent EffectiveDescriptor materialization,
general-purpose materialized views, a replacement inheritance engine, changes
to authoritative descriptor meaning or mutation authorization, instance-level
relationship realization, query planning or traversal optimization beyond
descriptor resolution, and transaction transport redesign.

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
