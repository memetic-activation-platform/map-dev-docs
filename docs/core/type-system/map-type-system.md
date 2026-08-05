# MAP Type System

## Purpose

The MAP Type System is a self-describing, extensible ontology represented as
MAP data. Types, properties, relationships, constraints, key rules, and schemas
are holons connected through typed relationships. The same graph can therefore
be authored, loaded, validated, queried, versioned, and governed using MAP's
ordinary holonic mechanisms.

This document is the conceptual overview and navigation point for the type
system. It is not the normative source for detailed schema rules, semantic
algorithms, runtime APIs, or exact descriptor declarations.

## Authority map

| Concern | Authority |
|---|---|
| Structural schema model and invariants | [Schema Design Spec](schema-design-spec.md) |
| Effective contracts, inheritance, key resolution, defaults, and conformance | [Descriptor-Kernel Semantic Rules](descriptor-semantics-rules.md) |
| Value-constraint semantics | [Value Constraints Design Spec](value-constraints-design-spec.md) |
| Relationship-constraint semantics | [Relationship Constraints Design Spec](relationship-constraints-design-spec.md) |
| Extension-schema rules | [Extension Schema Design](extension-schema-design.md), currently WIP and non-authoritative |
| TDL syntax, binding, omission, and translation | [TDL Specification](tdl/tdl-spec.md) |
| Exact schema identities and declarations | `map-holons/schema-src/*.tdl` |
| Runtime descriptor subsystem | [Runtime Descriptor Subsystem Design Spec](../core-runtime/descriptors/descriptors-design-spec.md) |
| Construction, completion, and kernel invocation | [Layered Descriptor Architecture](../descriptors/layered-desc-arch.md) |
| Cross-surface runtime representations | [MAP Runtime Shared Types](../core-runtime/runtime-shared-types.md) |
| Validation architecture and execution layers | [Validation Architecture](../validation/validation-arch.md) |

The retained [Schema 2.0 design discussion](schema-2.0.md) records the reasoning
and comparisons that led to the current structural specification. It is useful
background, not the concise current-state authority.

## Ontology as data

A **type descriptor** is a holon that defines a category of instances. It has
two distinct roles:

1. As a holon, it conforms to the contract of its own describing type.
2. As a type, it declares the contract imposed on the instances it describes.

For example:

```text
Book.HolonType
  DescribedBy MetaHolonType.MetaTypeDescriptor
  Extends HolonType.TypeDescriptor
```

`DescribedBy` determines what `Book.HolonType` must contain as a descriptor
holon. `Extends` classifies it as a holon type and contributes to the contract
it declares for books. Keeping those roles separate is central to Schema 2.0.

Ontology-as-data gives MAP several important properties:

- schemas can be extended without compiling each domain type into MAP Core;
- agents can inspect and reason about type definitions at runtime;
- schema declarations can drive validation, tooling, forms, and APIs; and
- types remain portable across concrete authoring and serialization formats.

## Three independent relationships

Schema 2.0 separates conformance, specialization, and instance discovery.

### `DescribedBy`

```text
H --DescribedBy--> T
```

`DescribedBy` identifies the type whose effective instance contract governs a
holon. Every semantically valid holon has exactly one describing type, and that
type must be concrete and classified under `TypeDescriptor`.

Ordinary holons and descriptor holons follow the same rule. Descriptor holons
are described by concrete meta-types.

### `Extends`

```text
T --Extends--> P
```

`Extends` establishes optional single-parent specialization among type
descriptors. It supplies subtype classification and additive inheritance of
instance-contract declarations. It also provides the lineage used by members
whose own `InheritanceMode` permits semantic inheritance.

`Extends` does not make all populated descriptor values inherit automatically.
It is also not a substitute for `DescribedBy`.

### `Instances`

```text
T --Instances--> H
```

`Instances` is the inverse traversal of `DescribedBy`. It supports discovery;
it does not independently define conformance.

## Descriptor model

All descriptor categories participate in one acyclic `Extends` hierarchy
rooted at abstract `TypeDescriptor`.

```text
TypeDescriptor
  HolonType
    MetaTypeDescriptor
      concrete meta-type branches
  PropertyType
  ValueType
  RelationshipType
    DeclaredRelationshipType
    InverseRelationshipType
```

The hierarchy serves classification and substitutability. Concrete meta-types
describe descriptor holons, while abstract descriptor categories provide
classification roots and polymorphic relationship endpoints.

`TypeKind` remains useful classification metadata for tooling and
presentation. It does not determine `DescribedBy`, `Extends` compatibility,
conformance, endpoint substitutability, or runtime wrapper selection.

### Reflective fixed point

Meta-types are themselves descriptor holons and are described by
`MetaHolonType`. `MetaHolonType` is explicitly self-describing:

```text
MetaHolonType --DescribedBy--> MetaHolonType
```

This authored fixed point closes the reflective model. It is not a hidden
bootstrap exception. Circular source dependencies needed to express it are
handled by multi-pass schema loading.

## Instance contracts

A type declares the contract of its described instances through:

- `InstanceProperties`, which target property descriptors; and
- `InstanceRelationships`, which target declared relationship descriptors.

A subtype inherits its parent's contract declarations and may add local
members. It may not remove, shadow, or redeclare an inherited member to change
that member's type, endpoint, cardinality, requiredness, or validation rules.

Property descriptors select value types and may define requiredness and
defaults. Relationship descriptors define directional endpoints, cardinality,
ordering, duplicate policy, definitional status, deletion semantics, and
semantic inheritance behavior. The focused constraint specs and descriptor
semantic rules define the resulting validity and conformance behavior.

## Effective semantics

Schema declarations are not evaluated by copying ancestor state into every
descriptor. The descriptor kernel computes effective contracts and effective
member values over the existing holonic representation.

At a high level:

- contract declarations inherit additively through `Extends`;
- populated member values follow that member's `InheritanceMode` of `None`,
  `Additive`, or `Override`;
- identity-based duplicate elimination preserves contribution provenance;
- cardinality and constraints apply to effective values or targets; and
- conformance is checked against the effective contract of the holon's
  `DescribedBy` target.

The exact algorithms and error conditions belong exclusively to the
[Descriptor-Kernel Semantic Rules](descriptor-semantics-rules.md).

## Keys and defaults

Holon identity and semantic keys are distinct. A holon's semantic key is
selected through the effective `InstanceKeyRule` of its describing holon type.
Keylessness is explicit through `NoneRule.KeyRuleType`; it is not represented by
an absent rule.

Descriptor holons use the same mechanism as ordinary holons. Their keys follow
the key rule selected by their concrete meta-type rather than a declaration
syntax, filename, or hard-coded Rust convention.

Required property defaults are descriptor-defined values. A creation-specific
completion service may materialize them after descriptor binding and before
validation. The descriptor kernel may provide semantic helpers for that
operation, but validation and commit do not silently inject defaults.

## Schemas and extension

A `Schema` holon identifies a logical collection of descriptor components.
Every descriptor belongs to exactly one schema, and a schema may depend on
other schemas needed to resolve and validate its declarations. Dependencies
may be mutually recursive, so the loader resolves a dependency closure through
multiple passes rather than requiring a simple DAG.

Logical ownership and physical source placement are separate. Component
sections own the meaning and behavior of their schema concepts, while the
authoritative TDL files remain colocated in `map-holons/schema-src` to support
imports and corpus-wide loading.

The same structural type model applies to MAP Core and Extension Schemas. The
cross-schema ownership, compatibility, and evolution model remains deferred;
the [Extension Schema Design](extension-schema-design.md) is explicitly WIP.

## Runtime boundary

Schema entities use MAP's ordinary holonic runtime representation. The type
system does not introduce a separate semantic IR or a parallel descriptor
graph abstraction.

Creation adapters parse concrete syntaxes such as TDL or MAP JSON into the
loader's holonic representation. In loader flows, completion binds descriptors
and materializes applicable defaults before validation. The descriptor kernel
then computes and validates semantics without transforming the authored
representation. Commit orchestrates validation before persistence but does not
perform completion.

Runtime wrappers, references, storage formats, transactions, and PVL remain
owned by their respective runtime documents. PVL is descriptor-independent;
descriptor-driven holon validation occurs above the integrity layer.

## Summary

MAP's type system is one self-describing graph with deliberately separate
relationships for conformance, specialization, and discovery. Descriptors are
ordinary holons that both conform to meta-type contracts and declare contracts
for their own instances. Schema 2.0 keeps those roles explicit, represents keys
and constraints as schema data, and evaluates them through a shared semantic
kernel over the existing holonic representation.

This overview explains that shape. The authority map above identifies the
document or source that owns each normative detail.
