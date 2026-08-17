# Runtime Descriptor Facades Draft (Superseded)

> **Status: Superseded and non-authoritative.** This facade-oriented draft remains temporarily for
> comparison during the documentation refactor. The current runtime descriptor authority is the
> [Runtime Descriptor Subsystem Design Spec](../core-runtime/descriptors/descriptors-design-spec.md).

## 1. Purpose

This specification defines the caller-facing Rust facade over MAP descriptor holons. It covers:

- how descriptor wrappers represent descriptor holons;
- how callers narrow a `HolonReference` to a descriptor category;
- how local structural access differs from effective semantic access;
- how descriptor facades delegate to the shared descriptor kernel; and
- which responsibilities remain outside the facade layer.

The descriptor facade is an API over the explicit holon graph. It is not a second descriptor
representation and does not define schema semantics.

## 2. Authority

The current authoritative sources are:

1. [`schema-design-spec.md`](../type-system/schema-design-spec.md) for the structural descriptor
   and meta-type model.
2. The Schema 2.0 TDL corpus in `map-holons/schema-src` for exact descriptor declarations.
3. [`descriptor-semantics-rules.md`](../type-system/descriptor-semantics-rules.md) for effective semantics and
   conformance.
4. [`layered-desc-arch.md`](layered-desc-arch.md) for representation and component boundaries.
5. The
   [Runtime Descriptor Subsystem Design Spec](../core-runtime/descriptors/descriptors-design-spec.md)
   for descriptor-specific runtime integration and facade boundaries.

This retained draft does not independently define a runtime facade contract.

[`schema-2.0.md`](../type-system/schema-2.0.md) retains the design rationale but is not a parallel
normative authority.

Generated loader JSON is an output projection of the Core Schema TDL. It is not the source from
which descriptor meaning or runtime APIs are independently defined.

When this document names a schema member, the TDL corpus determines its exact descriptor identity,
cardinality, value type, and kernel inheritance rule. This document does not duplicate complete schema
inventories.

## 3. Core representation contract

Every descriptor is an ordinary holon in the explicit Holons Core graph.

A runtime descriptor facade:

- stores exactly one private `HolonReference`;
- reads properties and relationships through the Reference Layer;
- works with transient, staged, and saved references; and
- does not copy descriptor properties or relationships into authoritative Rust fields; and
- does not expose a public accessor that lets consumers bypass the facade and directly traverse
  the wrapped reference.

Representative shape:

```rust
pub struct HolonDescriptor {
    holon: HolonReference,
}
```

Internal implementation helpers may borrow the wrapped reference to share accessor logic among
typed wrappers. That implementation mechanism must not become a public escape hatch from facade
semantics.

Wrappers may hold borrowed helper views, such as `TypeHeader<'_>`, and implementations may use
bounded caches. Neither becomes a mutable source of descriptor truth.

## 4. Descriptor classification and narrowing

Typed narrowing follows descriptor identity and the Schema 2.0 `Extends` hierarchy.

For a descriptor holon `D`, a facade category is admissible when:

```text
TypeSubstitutable(D, category-root)
```

Examples:

| Facade                           | Required descriptor category                |
|----------------------------------|---------------------------------------------|
| `HolonDescriptor`                | `HolonType.TypeDescriptor`                  |
| `PropertyDescriptor`             | `PropertyType.TypeDescriptor`               |
| `RelationshipDescriptor`         | `RelationshipType.TypeDescriptor`           |
| `DeclaredRelationshipDescriptor` | `DeclaredRelationshipType.RelationshipType` |
| `InverseRelationshipDescriptor`  | `InverseRelationshipType.RelationshipType`  |
| `ValueDescriptor`                | `ValueType.TypeDescriptor`                  |
| `KeyRuleDescriptor`              | `KeyRuleType.HolonType`                     |
| `DanceDescriptor`                | `DanceType.HolonType`                       |
| `CommandDescriptor`              | `CommandType.HolonType`                     |
| `OperatorDescriptor`             | `OperatorType.HolonType`                    |

`TypeKind`, a declaration form, a key suffix, or a type-name comparison is not sufficient proof of
facade category. Those values may support diagnostics or optimized dispatch only after semantic
classification has been established.

Public narrowing operations must fail when the reference does not belong to the requested
category. Internal constructors may accept a previously validated reference, but the validation
obligation must remain explicit at that boundary.

More specialized facades, such as `HolonSpaceDescriptor`, `TransactionDescriptor`,
`EnumValueDescriptor`, or `ValueArrayDescriptor`, are justified only when they expose a meaningful
typed contract or behavior beyond their parent facade. They remain thin views over the same
reference.

## 5. Resolving a holon's descriptor

`ReadableHolon::holon_descriptor()` is the primary entry point from a holon instance to its
describing type.

It must:

1. read the source holon's local `DescribedBy` targets;
2. require exactly one target;
3. require the target to be an admissible holon-type descriptor; and
4. return a `HolonDescriptor` over that target reference.

It must not infer the descriptor from a Rust type, `TypeKind`, key suffix, persisted entry type, or
source-format declaration.

The method resolves the describing type. It does not combine the source holon's descriptor lineage
with the describing type's lineage. Schema 2.0 keeps conformance, specialization, and semantic
inheritance as separate operations.

## 6. Shared descriptor metadata

`TypeHeader` is a borrowed convenience view over shared descriptor metadata declared by the Core
Schema. It centralizes typed reads without storing duplicate values.

The shared surface includes schema-backed values such as:

- type name and plural type name;
- display name and plural display name;
- description;
- abstractness; and
- the local `DefinesInstanceTypeKind` designation.

Accessors read completed explicit state. They do not synthesize defaults or reinterpret an absent
required value. Missing or malformed required state is an error.

Schema additions and removals control the available structural surface. Rust helper names may be
idiomatic, but each schema-backed accessor must identify the descriptor member from which it reads.

## 7. Local and effective access

Descriptor facades expose two different kinds of operation.

### 7.1 Local structural access

Local access reads state populated directly on the wrapped descriptor holon. Examples include:

- shared header properties;
- a property descriptor's local `IsValueRequired`, `DefaultValue`, and `ValueType`;
- a relationship descriptor's local endpoints, cardinality, inverse, and deletion semantic; and
- a descriptor's direct `Extends` target.

Local access does not walk inheritance or apply kernel inheritance rules.

### 7.2 Effective semantic access

Effective access is provided through `HolonDescriptor` and its typed descriptor wrappers. Examples
include:

- effective instance properties and relationships;
- lookup of an effective property or relationship by semantic member name;
- effective command, dance, and operator affordances;
- effective instance key rules;
- effective populated values under `Local`, `Additive`, or `Override`; and
- endpoint and subtype compatibility.

API names must make effective behavior clear. Collection operations such as
`instance_properties()`, `instance_relationships()`, `afforded_commands()`, and
`afforded_dances()` return effective results unless explicitly named `local_*`.

There is no generic facade rule that every relationship is flattened or that the first populated
ancestor always wins. The member descriptor's Schema 2.0 semantics determine the operation:

- instance-contract declarations accumulate because the kernel assigns
  `InstanceProperties` and `InstanceRelationships` `Additive`;
- populated values use their kernel-selected inheritance rule;
- `Local` remains local;
- `Additive` combines distinct contributions with provenance; and
- `Override` selects the complete contribution set from the nearest populating type.

The facade must preserve kernel errors for cycles, multiple parents, duplicate inherited
declarations, incompatible member identities, and invalid cardinality. It must not silently choose
an answer from an invalid graph.

## 8. Facade responsibilities by category

The following table assigns runtime API ownership without restating the Core Schema.

| Facade | Caller-facing responsibility |
| --- | --- |
| `HolonDescriptor` | Effective instance contract, relationship permission, key rule, and afforded behavior discovery for holon instances |
| `PropertyDescriptor` | Property requiredness, default metadata, and selected value descriptor |
| `RelationshipDescriptor` | Relationship identity, endpoints, cardinality, ordering, duplicate policy, and deletion semantic |
| `DeclaredRelationshipDescriptor` | Declared orientation and required inverse lookup when an inverse is defined |
| `InverseRelationshipDescriptor` | Inverse orientation and declared-partner lookup |
| `ValueDescriptor` | Value-family classification, effective constraints, and effective operator discovery |
| `KeyRuleDescriptor` | Descriptor-backed key-rule identity and evaluation entry point |
| `DanceDescriptor` | Dance identity and schema-backed dance contract metadata |
| `CommandDescriptor` | Command identity and schema-backed command metadata |
| `OperatorDescriptor` | Operator identity and schema-backed operator metadata |

Subsystem execution remains outside these structural facades:

- dance implementation selection and invocation are defined by
  [`dances-design-spec.md`](../dances/dances-design-spec.md);
- command ingress, lifecycle, and routing are defined by
  [`commands.md`](../commands-and-runtime/commands.md);
- value-constraint execution is defined by
  [`value-constraints-design-spec.md`](../type-system/value-constraints-design-spec.md); and
- query execution is defined by
  [`query-engine-design-spec.md`](../map-queries/query-engine-design-spec.md).

Facades provide descriptor-backed discovery and typed entry points. They do not create parallel
registries or redefine subsystem execution semantics.

## 9. Typed names and identity

Runtime lookup APIs use TypeKind-specific or role-specific name wrappers rather than unconstrained
`MapString` values where a stable semantic name category exists.

Examples include:

- `PropertyName`;
- `RelationshipName`;
- `DanceName`;
- `CommandName`; and
- `OperatorName`.

These wrappers:

- prevent accidental cross-family lookup;
- centralize conversion from schema-backed descriptor identity;
- provide conversion traits such as `ToPropertyName` and `ToDanceName`; and
- do not duplicate descriptor identity as separately authoritative state.

Known-core enums such as `CoreCommandTypeName` are implementation aids for stable Core Schema
identities. They do not replace descriptor holons and must remain synchronized with the Core Schema
TDL corpus.

Lookup uses semantic identity, not display labels. Duplicate effective declarations that claim the
same semantic name are errors as defined by the descriptor kernel.

## 10. Validation and completion boundary

Descriptor facades consume the completed explicit holon graph.

They do not:

- materialize descriptor defaults;
- complete omitted values;
- mutate authored state during reads;
- define conformance independently of the descriptor kernel; or
- treat a missing required value as a lazy request for its default.

Convenience methods such as `is_valid`, `allows_property`, or `allows_relationship` delegate to
kernel-owned semantics and map representation-neutral violations into the caller's error vocabulary.

Creation and completion ordering is defined by
[`layered-desc-arch.md`](layered-desc-arch.md). A facade may still encounter invalid saved or staged
state and must fail precisely rather than assuming all references were previously validated.

## 11. Error contract

Facade operations distinguish at least:

- graph-access failure;
- missing or multiple `DescribedBy` targets;
- invalid facade narrowing;
- missing or multiple `Extends` targets;
- cyclic inheritance;
- missing required explicit member state;
- malformed property value shape;
- missing or multiple required relationship targets;
- duplicate inherited declaration identity;
- duplicate semantic member name;
- unresolved or inaccessible reference;
- invalid endpoint category; and
- descriptor-kernel conformance violations.

Errors should retain descriptor and member identity and, where available, kernel contribution
provenance. Runtime wrappers map these failures to `HolonError`; source and loader adapters may add
source-location provenance at their boundaries.

## 12. Schema-backed accessor derivation

Structural accessor eligibility comes from effective `InstanceProperties` and
`InstanceRelationships` in the Schema 2.0 TDL corpus.

Generated or mechanically derived accessors are permitted when they:

- remain thin Reference Layer reads;
- preserve required, optional, and cardinality distinctions;
- do not embed separate inheritance or validation logic; and
- are regenerated or checked when the Core Schema TDL changes.

Handwritten helpers are appropriate for typed narrowing, effective lookup, and domain-oriented
composition. They must delegate effective semantics to the shared kernel.

Generation workflow, module layout, PR sequencing, and test checklists belong in implementation
plans rather than this design specification.

## 13. Deferred effective-surface caching

Persisted or transient effective-surface artifacts are outside the current roadmap. Runtime
behavior uses live `HolonDescriptor` access. Any future cache must remain encapsulated behind that
surface and preserve observable identity, error behavior, and provenance; it must not become a
second mutable semantic authority.

## 14. Relationship persistence boundary

Descriptor facades expose relationship metadata and inverse identity. They do not own commit-time
materialization, SmartLink storage, distributed retry, or inverse repair.

Relationship occurrence persistence is defined by
[`relationship-persistence-design-spec.md`](../transactions/relationship-persistence-design-spec.md). Storage
encoding remains governed by the storage-layer specifications.

## 15. Definition governance

Whether a caller may define a new descriptor in a particular branch is schema-governance and
authorization policy, not a `TypeKind`-based facade behavior.

Core-controlled branches such as command and operator descriptors may be discoverable through the
same facade model while remaining closed to domain-defined extensions. Facades expose descriptor
classification; the schema-authoring and authorization boundary enforces who may create or extend
those descriptors.

This specification does not define a complete domain-definability matrix. Such a matrix must be
maintained with schema governance rather than inferred from Rust wrapper availability.

## 16. Explicit non-responsibilities

The runtime descriptor facade layer does not own:

- TDL or JSON parsing;
- graph construction or default materialization;
- the normative descriptor algorithms;
- relationship occurrence persistence;
- dance, command, operator, or query dispatch;
- command inventories;
- schema migration sequencing;
- source diagnostics;
- code generation workflow; or
- domain authorization policy.

Its responsibility is deliberately narrow: provide typed, consistent, caller-friendly access to
descriptor data and kernel-defined effective semantics over the explicit holon graph.
