# Descriptors Design Spec

## Purpose

This spec defines a lean, reusable descriptor model for MAP's self-describing ontology.

The design supports:

- inverse relationship auto-population
- descriptor-driven validation
- descriptor-bound behavior (commands and dances)
- IntegrationHub command execution
- generated, schema-aligned descriptor accessors
- flattened type inheritance without pushing traversal burden onto callers
- value-type-driven query semantics

The design is intentionally conservative in execution strategy, but progressive in semantic structure. It establishes descriptor-bound behavior now using static Rust implementations, while preparing for future dynamic dispatch.

---

## Authoritative Schema Source

The authoritative source of truth for the MAP Core Schema is the core schema JSON under:

- host/import_files/map-schema/core-schema/

Generated descriptor accessors and descriptor obligations must be derived from these JSON definitions, not handwritten Rust mirrors.

Where this spec defines target behavior that is not yet represented in the current core schema JSON, the required path is:

- extend the core schema definitions first
- then generate or implement against those updated definitions

This spec is therefore a target-state design to be materialized incrementally across multiple PRs. Some of those PRs must explicitly extend the core schema so the schema remains authoritative.

---

## Core Position

Descriptors are active holons.

Each descriptor:

- is a holon
- owns the semantic definition of a type
- owns the behaviors associated with that type

Descriptor wrappers are thin typed views over a backing HolonReference.

Behavior is:

- semantically attached to descriptors
- implemented in Rust in this phase
- exposed through commands (local invocation)
- optionally exposed through dances (protocol invocation)

Commands are execution plumbing. Descriptors are the semantic source of truth.

---

## Four-Level MAP Ontology Model

The following diagram defines the four-level MAP ontology model that this spec assumes.

![4-Level MAP Meta-Schema.jpg](../docs/core/media/4-Level%20MAP%20Meta-Schema.jpg)


The model distinguishes four ontology levels:

- meta-level
- abstract type level
- core type level
- instance level

Within this model:

- `TypeDescriptor` is the root descriptor of descriptors at the core type level
- meta-types define kind-level obligations
- abstract types anchor structure and relationship patterns for concrete types
- instances are holons described by concrete type descriptors

Runtime wrappers and implementation helpers are not part of this ontology model. They are runtime projections over it.

---

## Descriptor Layers

The descriptor design spans three distinct layers that must not be conflated.

### Ontology Layer

At the ontology layer, descriptors are holons defined in the MAP schema, including:

- `TypeDescriptor`
- `MetaTypeDescriptor`
- `MetaHolonType`
- `MetaPropertyType`
- `MetaValueType`
- `MetaRelationshipType`
- `MetaDeclaredRelationshipType`
- `MetaInverseRelationshipType`
- `HolonType`
- `PropertyType`
- `ValueType`
- `DeclaredRelationshipType`
- `InverseRelationshipType`

These ontology-level descriptor holons define:

- structure
- obligations
- relationships

`TypeDescriptor` is the root descriptor of descriptors. It is self-describing and forms the irreducible foundation of the MAP type system.

### Runtime Layer

At the runtime layer, descriptor wrappers are Rust types such as:

- `HolonDescriptor`
- `PropertyDescriptor`
- `ValueDescriptor`
- `RelationshipDescriptor`
- `DeclaredRelationshipDescriptor`
- `InverseRelationshipDescriptor`

These:

- wrap descriptor holons
- provide typed access
- do not define ontology

### Implementation Layer

At the implementation layer, shared helpers and routing abstractions include:

- `TypeHeader`
- `Descriptor` trait
- inheritance traversal helpers
- static dispatch logic

These:

- centralize logic
- improve ergonomics
- are not part of the ontology

---

## Design Constraints



### MAP ontology principles

- Each TypeKind has exactly one top-level abstract MetaType and one top-level abstract type.
- Meta-types declare a type kind's obligations.
- Top-level meta-types extend nothing.
- Meta-types may have sub-meta-types.
- Abstract type descriptors extend meta-types and anchor core relationship types.
- Each MAP type is DescribedBy exactly one concrete TypeDescriptor.
- Concrete type descriptors extend the abstract type for their TypeKind.
- TypeDescriptor is both described and describing.
- TypeDescriptor is self-describing and is the ontological anchor of all descriptors.

### Architectural principles

- Every descriptor is a holon.
- Descriptor wrappers store a single HolonReference.
- Behavior is attached to descriptors via affordances.
- Commands are local invocation affordances.
- Dances are cross-boundary protocol affordances.
- Execution strategy (static vs dynamic) is not part of the ontology.
- TypeScript is a delegating client, not a second descriptor engine.
- Single type inheritance is a committed ontology constraint: maximum `Extends` cardinality is 1 and must be enforced when committing schema descriptors.

---

## Goals

- Establish descriptor-bound behavioral ownership
- Keep descriptor structs minimal and aligned with ontology
- Centralize inheritance traversal and descriptor lookup
- Generate schema-aligned accessors
- Provide command-based execution surface
- Prepare for dynamic dispatch without requiring it now

---

## Non-Goals

- Full dynamic dispatch or ABI loading
- Schema evolution strategy
- Multi-inheritance
- TypeScript-based validation
- Final dance-specific APIs

---

## Stable vs Variable Design Surface

This spec distinguishes between stable design commitments and variable design surfaces.

### Stable Commitments

These are intended to remain stable across near-term schema and implementation evolution:

- descriptors are active holons in the ontology
- `TypeDescriptor` is self-describing and is the root descriptor of descriptors
- meta-types define kind-level obligations
- abstract types anchor concrete type structure and relationship patterns
- runtime descriptor wrappers are thin typed views over descriptor holons
- runtime helpers such as `TypeHeader` and descriptor traits are implementation artifacts, not ontology
- core-schema definitions are authoritative for structural descriptor obligations
- single inheritance through `Extends` is the committed direction
- maximum `Extends` cardinality is 1 and is enforced at schema commit time
- duplicate inherited property and relationship declarations are rejected at schema commit time
- generated structural accessors must derive strictly from schema-declared `InstanceProperties` and `InstanceRelationships`
- behavior is descriptor-bound and implemented statically in Rust in this phase
- TypeScript is a delegating client, not a second descriptor engine

### Variable Surfaces

These are expected to evolve incrementally through schema extensions, code generation improvements, and follow-on implementation PRs:

- the exact generated accessor inventory for evolving schema domains
- command-affordance modeling in schema
- dance-affordance modeling in schema
- `CommandDescriptor` ontology and generated/runtime scaffolding
- `ValueType` operator definitions in schema
- value-operator runtime APIs and their eventual schema-driven form
- collection-descriptor obligations once collection abstractions are defined in schema
- enum, enum-variant, and value-array relationship obligations where the current schema is incomplete
- impact-analysis and CI-enforcement details from the schema ripple process
- the eventual move from static dispatch to richer/dynamic dispatch models

### Interpretation Rule

When reading this spec:

- stable commitments should be treated as architectural constraints
- variable surfaces should be treated as target-state areas to be realized incrementally
- where a variable surface is structural, the correct path is to extend the core schema first and then let the schema ripple process propagate the change

---

## Descriptor Model

### One wrapper type per TypeKind

Define one descriptor wrapper per top-level TypeKind:

- HolonDescriptor
- PropertyDescriptor
- RelationshipDescriptor
- CollectionDescriptor
- EnumVariantDescriptor
- ValueDescriptor

For value types, define specialized wrappers:

- StringValueDescriptor
- IntegerValueDescriptor
- BooleanValueDescriptor
- EnumValueDescriptor

These are typed views, not alternative storage models.

---

## Descriptor Affordances

Each descriptor may afford behaviors.

Affordances fall into two categories:

### Commands

- direct invocation
- local-only
- synchronous
- used by host and TypeScript

Target-state schema note:

- `CommandDescriptor` should define at minimum:
- command name
- input/output contract, initially opaque if necessary
- the relationship by which a descriptor affords the command

### Dances

- envelope-based invocation
- cross-boundary
- protocol-driven
- deferred in this phase

Behavior is attached to descriptors but executed statically in this phase.

To keep these affordances schema-aligned, the core schema should be extended to model them explicitly:

- add `CommandDescriptor` type definitions to the core schema
- add command-affordance relationships for descriptors that expose commands
- defer dance-affordance schema detail until the dance model is ready, but do not treat dances as permanently schema-external

---

## Common Descriptor Abstractions

### Descriptor trait

```rust
pub trait Descriptor {
    fn holon(&self) -> &HolonReference;
}
```

### TypeHeader

Shared helper for:

- type_name
- display_name
- description
- type_kind
- instance_type_kind

`TypeHeader` is the runtime projection of the shared properties and relationships defined by `TypeDescriptor` and `MetaTypeDescriptor`.

Expose:

- header()
- convenience accessors via trait defaults

---

## Inheritance Resolution

- Single inheritance only
- No cached extends chain
- Traversal performed on demand
- Fail on multiple extends or cycles
- Flatten inheritance for callers
- Maximum `Extends` cardinality of 1 is enforced at schema commit time and may be assumed by inheritance resolution
- Lookup should generally chase parentward only until a match is found rather than materializing the full chain unless whole-chain knowledge is required

---

## Behavioral Allocation Principles

Behavior must be owned by the most specific descriptor.

Ontology ownership and runtime ownership should be distinguished where useful.

| Behavior Type          | Ontology Owner                                                                              | Runtime Owner                        |
|------------------------|---------------------------------------------------------------------------------------------|--------------------------------------|
| Holon read/write       | Holon descriptor holons                                                                     | `HolonDescriptor`                    |
| Property constraints   | Property descriptor holons                                                                  | `PropertyDescriptor`                 |
| Value validation       | Value descriptor holons                                                                     | `ValueDescriptor`                    |
| Value comparison       | Value descriptor holons                                                                     | `ValueDescriptor`                    |
| Relationship traversal | Relationship descriptor holons                                                              | `RelationshipDescriptor`             |
| Type introspection     | Descriptor holons via shared structure defined by `TypeDescriptor` and `MetaTypeDescriptor` | Descriptor wrappers via `TypeHeader` |

No behavior should be freestanding.

All externally meaningful behavior must be descriptor-bound. Internal helper functions may exist, but they must not define new semantics outside the descriptor model.

---

## Descriptor Operations

### HolonDescriptor

- get_property_by_name
- get_relationship_by_name
- get_inverse_relationship_by_name

### PropertyDescriptor

- value_type

### RelationshipDescriptor

- participates in traversal and validation

---

## ValueDescriptor

ValueDescriptor defines value semantics.

It owns:

- validation
- comparison
- operator support

### Validation

```rust
fn is_valid(&self, value: &BaseValue) -> Result<(), HolonError>;
```

### Operator Support

```rust
fn supports_operator(&self, operator: ValueOperator) -> bool;

fn apply_operator(
    &self,
    operator: ValueOperator,
    lhs: &BaseValue,
    rhs: &BaseValue,
) -> Result<bool, HolonError>;
```

Important schema-alignment note:

- the current core schema does not yet define operator metadata on `ValueType`
- to keep core schema definitions authoritative, operator support must be introduced by extending the `ValueType` definitions in the core schema
- Rust should not grow a disconnected operator registry that bypasses schema authority
- runtime operator implementations must not introduce operators that cannot later be represented in schema

---

## Value Operators

Operators are defined per ValueType.

Examples:

- Equals
- LessThan
- GreaterThan
- Between
- Contains
- RegexMatch
- Before
- After

Operators are not global.

Each ValueType defines:

- which operators are valid
- what those operators mean

In this phase, value operators are part of the runtime behavior layer attached to `ValueDescriptor`. They are not yet schema-declared.

This is a core-schema gap. A future PR series should add operator definitions and the relevant `ValueType` relationships/properties to the core schema before relying on schema-driven generation or schema-driven introspection of operator semantics.

---

## Generated Accessors

Generated from schema:

- properties
- relationships

Generated accessors are:

- read-only
- structural
- thin wrappers over holon APIs

Behavioral methods are handwritten.

### Generated accessor inventory from current core schema

Using the current authoritative JSON under `host/import_files/map-schema/core-schema/`, the generated accessor surface should be derived from the effective `InstanceProperties` and `InstanceRelationships` declared on the abstract/core type descriptors for each kind.

The inventory below is intentionally strict: if an accessor is not justified by the current core schema definitions, it should not be generated yet.

All generated accessors must be derived strictly from schema-declared `InstanceProperties` and `InstanceRelationships`.

### Shared descriptor accessors

All descriptor wrappers should expose the shared header/property accessors implied by `TypeDescriptor` and `MetaTypeDescriptor`, typically via delegation through `TypeHeader`:

- `type_name()`
- `type_name_plural()`
- `display_name()`
- `display_name_plural()`
- `description()`
- `is_abstract_type()`
- `instance_type_kind()`

All descriptor wrappers should also expose the common descriptor relationships declared in `MetaTypeDescriptor` and descriptor structure:

- `component_of()`
- `extends()`
- `uses_key_rule()`

In addition to these generated schema-based accessors, handwritten helper operations remain:

- `header()`
- `holon()`
- inheritance traversal helpers
- lookup helpers such as `get_property_by_name()` and `get_relationship_by_name()`

### `HolonDescriptor`

Generate the following additional accessors from `HolonType` plus inherited meta-types:

Properties:

- `allows_additional_properties()`
- `allows_additional_relationships()`

Relationships:

- `properties()`
- `described_by()`
- `owned_by()`

Notes:

- `described_by()` is schema-driven for holon instances and distinct from the `ReadableHolon::holon_descriptor()` convenience method.
- A matching inverse accessor such as `instances()` should only be generated if the schema itself declares that obligation on the relevant abstract descriptor.

### `PropertyDescriptor`

Generate the following additional accessors from `MetaPropertyType` and `PropertyType`:

Properties:

- `is_required()`
- `property_name()`

Relationships:

- `value_type()`

### `RelationshipDescriptor`

Generate the following common relationship-descriptor accessors from `MetaRelationshipType`:

Properties:

- `deletion_semantic()`
- `is_definitional()`
- `is_ordered()`
- `allows_duplicates()`
- `min_cardinality()`
- `max_cardinality()`
- `property_name()`
- `allows_additional_properties()`
- `allows_additional_relationships()`

Relationships:

- `source_type()`
- `target_type()`

### `DeclaredRelationshipDescriptor`

Generate the following declared-relationship-specific accessor from `DeclaredRelationshipType`:

Relationships:

- `has_inverse()`

### `InverseRelationshipDescriptor`

Generate the following inverse-relationship-specific accessor from `InverseRelationshipType`:

Relationships:

- `inverse_of()`

### `ValueDescriptor`

Based on the current `ValueType` definition, generate no additional schema-specific accessors beyond the shared descriptor/header accessors and shared descriptor relationships:

- `component_of()`
- `extends()`
- `uses_key_rule()`

Validation behavior such as `is_valid()` remains a handwritten API.

### `StringValueDescriptor`

Based on the current `StringValueType` definition, generate no additional schema-specific accessors beyond those inherited from `ValueType`.

### `IntegerValueDescriptor`

Based on the current `IntegerValueType` definition, generate no additional schema-specific accessors beyond those inherited from `ValueType`.

Schema extension required for future target behavior:

- if integer constraints such as `min_value` or `max_value` are desired, they must be added to the core schema first
- only then should `min_value()` and `max_value()` be generated

### `BooleanValueDescriptor`

Based on the current `BooleanValueType` definition, generate no additional schema-specific accessors beyond those inherited from `ValueType`.

### `BytesValueDescriptor`

Based on the current `BytesValueType` definition, generate no additional schema-specific accessors beyond those inherited from `ValueType`.

### `EnumValueDescriptor`

Based on the current `EnumValueType` definition, generate no additional schema-specific accessors beyond those inherited from `ValueType`.

Current-schema note:

- the core schema defines the `Variants` / `VariantOf` relationship types
- the current `EnumValueType` abstract descriptor does not yet declare `Variants` as an `InstanceRelationship`
- this is a core-schema deficiency
- a follow-on core-schema PR should add that obligation so `variants()` becomes part of the generated accessor surface

### `EnumVariantDescriptor`

Based on the current `EnumVariantValueType` definition, generate no additional schema-specific accessors beyond the shared descriptor/header accessors.

Current-schema note:

- the core schema defines the `VariantOf` relationship type
- the current `EnumVariantValueType` abstract descriptor does not yet declare `VariantOf` as an `InstanceRelationship`
- this is a core-schema deficiency
- a follow-on core-schema PR should add that obligation so `variant_of()` becomes part of the generated accessor surface

### `ValueArrayDescriptor`

Based on the current `ValueArrayValueType` definition, generate no additional schema-specific accessors beyond those inherited from `ValueType`.

Current-schema note:

- the core schema defines the `ElementValueType` / `ElementValueTypeFor` relationship types
- the current `ValueArrayValueType` abstract descriptor does not yet declare `ElementValueType` as an `InstanceRelationship`
- this is a core-schema deficiency
- a follow-on core-schema PR should add that obligation so `element_value_type()` becomes part of the generated accessor surface

### `CollectionDescriptor`

No collection-specific descriptor accessors should be generated at this time.

Reason:

- the current authoritative core schema files do not define a collection abstract type descriptor with its own `InstanceProperties` or `InstanceRelationships`
- generation should follow the current schema, not anticipated future ontology

---

## Static Dispatch Strategy

This phase uses static dispatch.

- behavior is descriptor-bound
- execution uses Rust match or static routing
- no ABI loading
- no dynamic module resolution

In this phase, dispatch should be organized around descriptor types rather than centralized registries.

Future phases may replace this with dynamic dispatch.

---

## IntegrationHub Exposure

Commands expose descriptor behavior.

Commands:

- are descriptor-bound
- are local invocation endpoints
- are not the semantic source

Initial command surface includes:

- get holon descriptor
- get property descriptor
- get relationship descriptor
- get value type
- validate value
- apply operator

Schema alignment requirement:

- add `CommandDescriptor` definitions to the core schema
- model descriptor-command affordances in schema before treating command exposure as fully descriptor-described rather than just implementation-routed

---

## Query Integration

Query systems must consult ValueDescriptor for:

- valid operators
- operator semantics

Queries should not hardcode operator behavior.

Query and operator impacts should be included in the schema ripple impact manifest.

---

## Error Semantics

Fail on:

- missing DescribedBy
- multiple DescribedBy
- multiple Extends
- cycles
- missing required fields
- invalid casts
- invalid operators
- duplicate inherited declarations

Schema commit must reject:

- any descriptor with more than one `Extends`
- any child descriptor that redeclares a property name already present in its ancestor chain
- any child descriptor that redeclares a relationship name already present in its ancestor chain

---

## Module Shape

- descriptors/mod.rs
- descriptors/descriptor.rs
- descriptors/type_header.rs
- descriptors/inheritance.rs
- descriptors/holon_descriptor.rs
- descriptors/property_descriptor.rs
- descriptors/relationship_descriptor.rs
- descriptors/value_descriptor.rs
- descriptors/generated/

---

## Deferred Questions

- dynamic dispatch and ABI loading
- dance descriptor APIs
- schema evolution
- command descriptor formalization
- operator extensibility model

---

## Summary

The descriptor layer:

- treats descriptors as active semantic holons
- attaches behavior to descriptors
- uses static Rust execution in this phase
- exposes behavior through commands
- defines value semantics through ValueDescriptor
- prepares for future dynamic dispatch

This aligns MAP’s ontology, behavior, and execution model without introducing premature complexity.
