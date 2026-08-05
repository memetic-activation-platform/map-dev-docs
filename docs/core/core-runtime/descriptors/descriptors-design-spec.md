# MAP Runtime Descriptor Subsystem Design Spec (v2.0)

## 1. Purpose

This specification defines the runtime descriptor subsystem within the MAP core
holonic runtime. It explains how runtime code reaches descriptor data, invokes
descriptor semantics, and exposes descriptor-backed capabilities without
creating another descriptor representation or semantic authority.

The descriptor subsystem makes self-description operational. A holon's
`DescribedBy` relationship connects its runtime representation to the schema
contract, key rule, relationship permissions, validation commitments, and
behavior affordances declared by its type.

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
        | adapt graph access
        v
Descriptor Kernel
        |
        | computed contracts, classification, and violations
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

- the describing type determines the holon's conformance contract;
- a descriptor's own `Extends` lineage determines classification and the
  contract it passes to described instances; and
- a member's `InheritanceMode` governs semantic inheritance of values
  populated through that member.

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

`TypeKind`, type names, declaration forms, and key formats may support
diagnostics or optimization after classification. They are not proof that a
descriptor belongs to a category.

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

Local access does not traverse `Extends`, apply `InheritanceMode`, or materialize
missing values.

### 8.2 Effective access

Effective access delegates to the descriptor kernel. Examples include:

- effective instance properties and relationships;
- effective populated values under `None`, `Additive`, or `Override`;
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
has a distinct `TypeKind` or concrete schema identity.

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

The required order is:

```text
construct and resolve explicit graph
  -> compute effective contract
  -> materialize descriptor-defined defaults
  -> commit
       -> invoke shared Holon Validator
            -> invoke descriptor-kernel semantics
       -> persist only when valid
```

Holon Loading initially owns automatic default materialization through a modular
descriptor-default materialization service. The descriptor kernel owns semantic computation and
validation. Commit must invoke the reusable Holon Validator for persisted graphs and
refuse persistence when blocking violations remain. The Holon Validator remains
independently callable outside commit and Holon Loading. Commit does not invoke
default materialization; it validates the default-materialized graph supplied
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

Default materialization begins only after construction of the complete staged
application graph, resolution of all keyed references, and binding of each
holon's `DescribedBy` relationship.

This automatic materialization policy is initially specific to Holon Loading.
Interactive creation may present effective defaults for human confirmation and
write confirmed values explicitly. The service boundaries must permit later
reuse by other creation paths without moving mutation into the kernel or commit.

Once written, a materialized default is ordinary explicit property state. The
loader may retain ephemeral provenance for diagnostics, but commit persists no
authored-versus-default marker. Later descriptor-default changes do not alter
saved holons.

`HolonDescriptor::instance_properties()` supplies the effective property
declarations. `PropertyDescriptor` exposes the schema-backed
`default_value()` accessor for each declaration. No separate kernel-level
default helper is required.

A mutation-capable default-materialization service exposes a graph-level
runtime operation such as `materialize_defaults(staged_graph)`. It detects
omissions, reads defaults from effective `PropertyDescriptor`s, and writes
applicable values through staged-holon mutation APIs. Descriptor wrappers, the
Holon Validator, and commit do not receive mutation capabilities.

Any default-materialization error prevents creation/load orchestration from
invoking commit. Retention or reversion of successful default writes in the
uncommitted staged graph is an error-recovery policy, not a persistence
guarantee.

A materialization error is a failure to determine or apply a declared default.
An omitted required property with no applicable default remains absent and is
reported by the Holon Validator, not by the materialization service.

Default materialization accumulates independent errors where practical.
Successful writes remain in the uncommitted staged graph for diagnostics and
are not individually reverted. After reporting errors, creation/load
orchestration abandons or rolls back the failed transaction as a whole.

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
- duplicate inherited contract-member identity;
- duplicate semantic member name;
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

Implementations may cache immutable results of descriptor-kernel queries when
graph identity and versioning make cache validity explicit.

A future optimization may represent a descriptor's effective surface as a
transient ordinary holon and hide its use behind reference-layer operations.
That optimization is deferred. If introduced, it must remain call-site
transparent and semantically equivalent to direct kernel evaluation.

The subsystem does not currently depend on:

- a persisted effective-descriptor artifact;
- DAG-CBOR encoding of effective surfaces;
- descriptor-dependent PVL validation; or
- a second mutable cache that can disagree with descriptor holons.

Cached or derived results are replaceable implementation products. Descriptor
holons interpreted by the descriptor kernel remain authoritative.

## 15. Definition and Extension Governance

Runtime recognition of a descriptor category does not decide who may define or
extend that category.

Schema ownership, Extension Schema compatibility, authorization, and
core-controlled descriptor branches are governance concerns. They must not be
inferred from:

- the availability of a Rust wrapper;
- `TypeKind` alone;
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
| Contract, inheritance, key-rule, and conformance algorithms | Descriptor kernel |
| Descriptor-driven holon-validation orchestration | Validation framework |
| Descriptor-independent Integrity validation | PVL |
| Holon lifecycle and shared in-memory state | Shared objects layer |
| Uniform transient, staged, and saved access | Reference layer |
| Descriptor resolution and typed runtime interpretation | Runtime descriptor subsystem |
| Graph adaptation for kernel invocation | Runtime descriptor subsystem |
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
