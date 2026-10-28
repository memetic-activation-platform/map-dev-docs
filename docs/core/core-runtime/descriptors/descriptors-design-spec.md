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

- the `EffectiveHolonDescriptor` Rust struct wraps one `HolonReference`;
- that self-resolving reference identifies a typed transient holon described by
  `EffectiveHolonDescriptor.HolonType`.

The wrapper carries no separate transaction field, lifecycle state, parallel
schema cache, or `described_instance` field. Its referenced holon carries the
prepared relationships and data. Source references retain their own lifecycle
variants and resolution capabilities. `DescribedHolonType` identifies the
HolonType whose instance schema is represented; `DescribedBy` identifies the
result's own type. Neither replaces an instance's authoritative describing type.

`HolonDescriptor` remains the wrapper around an authoritative definition. Local
reads and metadata delegation belong there; inherited collection computation
belongs on EffectiveHolonDescriptor. The concrete return type preserves generic
`impl ToPropertyName`, `impl ToRelationshipName`, and corresponding Dance and
command name conversions. No trait-object or extension-trait split is required.

Descriptor Runtime Schema depends directly on Core, Dance, and Commands and
owns the result and construction Dance contracts. All eight effective
collections are declared directly on the result type; external
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
| `navigable_relationships()` | `NavigableRelationships`, all outbound RelationshipType references |
| `afforded_dances()` | `EffectiveAffordsDance` |
| `afforded_commands()` | `EffectiveAffordsCommand` |
| `effective_validation_bindings()` | `EffectiveValidationBindings` |
| `effective_constraints()` | `EffectiveConstraints` |
| `effective_key_rule()` | Singular access to `EffectiveInstanceKeyRule` |

Name-based lookup and permission-to-use-contract helpers operate on the same
prepared products. Effective-schema methods move from HolonDescriptor and
ReadableHolon to this concrete wrapper by semantics, not merely by their
`available_*` or `effective_*` prefixes. Public alternate paths that independently
walk inheritance are removed. Explicit local declaration reads, where needed,
are identified as local, for example with a `_local` suffix. Metadata operations
outside the prepared products may delegate to the authoritative descriptor.
Such delegation must not reintroduce migrated inheritance resolution.

An internal type-oriented acquisition operation supports validation and other
schema consumers that already hold a HolonType reference. It interprets that
type's instance contract; it does not mistakenly acquire the effective schema
of the type's own meta-type by treating the definition as an ordinary instance.

The returned handle is lightweight. Returning another wrapper over the same
retained transient reference does not reconstruct or copy the graph. Eager
population is the default. If measured single-aspect flows justify lazy
population later, that choice stays behind this API; callers do not select an
implementation strategy.

### 14.3 NavigableRelationships and instance availability

For HolonType `T`:

```text
Lineage(T) = {T} union Ancestors(T)
NavigableRelationships(T) = { R | SourceType(R) in Lineage(T) }
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

`navigable_relationships()` reads the populated references. It does not traverse
the target lineage or classify every referenced RelationshipType by walking
that member's ancestry. It does not return a public declared/inverse direction
flag. Presentation state uses relationship identity, not `direction + name`.

Instance availability remains a Rust reference-layer concern applied after
acquisition. In particular, the existing exclusion of inverse navigation for
uncommitted instances must be preserved without reclassifying the complete
vocabulary on every read. Any classification needed for that internal rule is
prepared or locally available. The wrapper remains type-level and has no
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
Its access and transport must preserve the wrapper's single-reference shape and
must not add another target-lineage computation. SourceOf discovery contributes
navigation identities without inventing authored declaration provenance.

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

Guest construction also gathers the metadata needed to compute the final cache
policy for each applicable relationship. It derives final `Reuse`, `Fresh`, or
bounded-age values once, reusing metadata and the already resolved target
lineage. The prepared projection carries exact source-type identity,
relationship identity, the name-to-identity association used by named instance
reads, and final policy values with any age parameter. Compact policy data uses
normal owner-aware result transport; it must not require one auxiliary holon or
one host/guest read per policy entry. Concrete encoding belongs to schema/API
implementation, while completeness and identity are part of this contract.

Before the descriptor becomes the registry's selected entry, the host installs
its policy data into a session-local index. Rust acquisition also establishes
the local source-instance-to-describing-type association needed by policy
lookup; instance caching must not fetch that association. At the point of instance caching,
policy resolution is strictly local: no DescribedBy fetch, relationship lookup,
Extends traversal, declared/inverse classification walk, or guest call is
permitted. The cache consumes final policy, not the schema reasoning behind it.
A missing prepared policy is handled by acquisition/preparation before entering
instance caching; it must not start recursive discovery inside the cache or be
silently promoted to an authoritative fallback policy.

Foundational policies required by construction's own reads are locally
available before preparation. Bootstrap traversal exemptions must not permanently
exclude structural collections such as Constraints from policy preparation:
after Descriptor Runtime is available, ordinary reads use their prepared final
policies too. Guest request-local membership reuse remains
independent of host descriptor discovery. Construction may use relationship
classification internally to derive policy; public navigation reads do not
repeat it. Explicit freshness changes membership retrieval, not schema-policy
preparation.

The runtime retains normal request binding and structural safeguards. It does
not run semantic source validation or a second conformance pass over its own
result or response. The existing bounded explicit-conformance accommodation for
descriptor-valued endpoints remains: the five effective vocabulary endpoints
and ContributionCollection retain their semantic category targets until general
endpoint eligibility can express them. The accommodation is not eager validation
and does not widen endpoints. Guest-local construction below 200 ms remains a
design target, distinct from host transport time and observed benchmark results.

### 14.7 Session ownership, registry, and explicit pull

A Session is one agent's adopted runtime context within a HolonSpace, spanning
public transactions. Session owns the registry and strongly retains a restricted
derived-state transaction containing saved-schema projections. HolonSpaceManager
remains a runtime proxy for the persistent space, which may be shared by agents.
Ownership is not assigned to the persistent HolonSpace itself.

Registry entries are keyed by exact saved HolonType identity and isolated by
session and space. Independent callers and public transactions obtain wrappers
over the same completed transient result. The self-resolving references retain
their actual owner; temporary IDs are not rebound into the caller's transaction.
Public completion, archival, undo/redo, and disposal do not dispose the retained
derived transaction. Session teardown explicitly disposes it.

The derived transaction permits reads, transient construction and sealing. It
prohibits staging, persistence, and Commit and is not exposed as user-mutable or
recoverable public work. Private cache-read frames retain their operation-bounded
semantics; public acquisition must not leave its result owned by such a frame.
Guest WASM state remains request-local; host session ownership retains the
returned graph across requests.

Coordinate concurrent acquisition of the same type. Registry locks are released
before graph reads and Dance invocation. Publish only a complete sealed result
with its prepared policies; failures leave no successful partial entry and may
be retried. Repeated hits add neither new result holons nor construction
transport. Retention must not create ownership cycles or accumulate unrelated
public transaction pools. Construction envelopes must have a managed lifetime.

The registry represents an adopted construction-time view. A saved HolonId is
version-specific, but incoming SourceOf vocabulary can change independently.
There are no TTL checks, push invalidations, background refreshes, or implicit
latest-version selection for schema adoption. Explicit pull/reconstruction
creates a new sealed result and updates selected descriptor/policy associations.
Existing handles remain bound to their prior result and owner; no published
result is mutated. Policy associations must remain coherent with the selected
adopted view when membership caches are reused. No common database snapshot
across independently prepared descriptors is implied.

Schema containing staged or transient definitions remains transaction/assessment
local and outside the saved-schema registry. Edits invalidate affected local
products. Reconstruct against the exact changed graph before assessing it again.
General Module-governed adoption and persistent effective artifacts remain outside
this design.

### 14.8 Commit-local registry snapshot

Before a host Commit invocation, shallow-clone the Session registry holon and
all of its selected EffectiveHolonDescriptor holons into the Commit transaction's
TransientHolonPool. Replace the cloned registry's entries with references to the
Commit-local descriptor clones. Each descriptor clone retains its original saved
schema references; those targets are neither cloned nor rebound. The existing
Dance pool projection carries the resulting graph. Pass the cloned registry root
as Commit input; this requires no additional pool transport protocol.

Admission to the Session registry requires every descriptor relationship target
to be a SmartReference. Check reference variants locally before publication, and
check again before making a Commit snapshot. A saved HolonType alone does not
establish this invariant: staged references, including committed staged handles,
and transient dependencies are excluded. Third-context unsaved references are
admission or cloning errors, rather than a reason to ship additional contexts.

Descriptor Runtime Schema defines the keyless
EffectiveHolonDescriptorRegistry.HolonType and its PreparedDescriptors
relationship to EffectiveHolonDescriptor.HolonType. Its paired inverse is
DescriptorRegistryFor; transient construction populates only the declared side.
PreparedSchema is a compact string-valued property of EffectiveHolonDescriptor.
It carries prepared relationship policies and lightweight declaring-origin data
as identity/value metadata, with no bound references, contribution holons, policy
entry holons, or validation outcomes.

Guest assessment may restore the seven inherited products and their original
occurrence positions from this prepared input without following Extends again.
Candidate schema edits require candidate-local computation; they cannot inherit
an accepted assessment or replace their candidate graph with a saved snapshot.
An assessment containing schema edits may conservatively decline the snapshot.
Validation outcomes remain specific to that assessment.

Ordinary Commands preserve the actual Session owner of a published descriptor
handle. Owner-aware binding permits that narrow read capability across public
transactions; it does not reinterpret Session temporary IDs in a caller pool or
expose the registry root and construction envelopes through public mutation
commands. Explicit pull replaces the selected descriptor and policy view,
invalidating retained membership/policy entries together. Previously returned
descriptor holons remain immutable and readable until Session teardown.

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
