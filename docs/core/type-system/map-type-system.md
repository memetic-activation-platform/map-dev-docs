# MAP Type System (v1.2)

## ChangeLog

### v1.2

- clarifies the MAP meta-schema around the `TypeDescriptor` and `MetaTypeDescriptor` model
- preserves MAP's single-inheritance rule: each type may extend at most one other type
- gives explicit architectural priority to the distinction between `DescribedBy` and `Extends`
- clarifies that the JSON `type` field is shorthand for the `DescribedBy` relationship
- clarifies that diagram stereotypes such as `<<MetaHolonType>>` are shorthand for `DescribedBy`
- clarifies that `TypeDescriptor` is self-describing and serves as the concrete bootstrap descriptor for descriptor holons
- clarifies that `MetaTypeDescriptor` defines the shared descriptor obligations inherited across descriptor lineages
- clarifies that each concrete descriptor holon is a single holon; MAP does not instantiate a second companion `TypeDescriptor` holon for each descriptor definition
- clarifies that effective descriptor obligations arise from both:
  - descriptor-wide semantics propagated through `DescribedBy -> TypeDescriptor`
  - TypeKind-specific semantics inherited through `Extends`
- clarifies that `InstanceProperties` and `InstanceRelationships` are interpreted differently depending on where they appear in the descriptor hierarchy
- formalizes that `Extends` preserves descriptor structure while `DescribedBy` interprets populated instance-surface declarations from the effective describing type
- clarifies that only concrete type descriptors describe ordinary runtime instances
- clarifies that abstract type descriptors serve as inheritance anchors and relationship anchors
- clarifies that all MAP type descriptors are descriptor holons: ordinary MAP holons whose role is to define types
- explicitly defines the MAP type graph as the graph of descriptor holons and the relationships among them

### v1.1

- distinguishes three major MAP type categories:
  - descriptors
  - runtime shared types
  - runtime envelopes
- introduces `runtime-shared-types.md` as the canonical home for cross-surface runtime shared types
- clarifies that `BaseValue`, rather than a separate `Value` layer, is the canonical scalar runtime shared type
- clarifies that runtime envelopes remain documented in their owning surface directories

### v1.0

- established the baseline overview of MAP as a self-describing holonic type system

---

The **MAP Type System** provides a holonic, self-describing, and extensible foundation for representing knowledge in an agent-centric world. MAP types are represented by **descriptor holons**: structured, versioned, queryable holons whose role is to define the structure, semantics, and constraints of other holons.

The **MAP type graph** is the graph of descriptor holons and the typed relationships among them. It includes descriptor holons such as `HolonType`, `PropertyType`, `RelationshipType`, `ValueType`, `Schema.HolonType`, and `Description.PropertyType`, connected by relationships such as `DescribedBy`, `Extends`, `ComponentOf`, `InstanceProperties`, `InstanceRelationships`, `SourceType`, `TargetType`, and `UsesKeyRule`.

Holons are typed by descriptor holons, and descriptor holons are themselves holons in this same graph.

This holonic approach means:

- Descriptor holons can describe runtime holons.
- Descriptor holons can describe other descriptor holons.
- Descriptor holons can inherit obligations from other descriptor holons.
- Descriptor holons can be extended, queried, versioned, and governed as data.
- Schemas can evolve without requiring every new domain type to be compiled into the core codebase.

The MAP Type System enables agents to:

- define their own schemas and vocabularies
- share and evolve types collaboratively
- validate, introspect, and visualize holons at runtime
- build interoperable semantic structures across HolonSpaces

![IfYouCanDescribeIt.png](../media/IfYouCanDescribeIt.png)

This document introduces the architecture of the MAP Type System, structured around the v1.2 meta-schema model, TypeKinds, schemas, HolonSpaces, key rules, introspection semantics, and the small family of runtime shared types reused across higher-level surfaces.

For a concrete design-validation discipline that pressure-tests this model, see `schema-v2-pressure-test-checklist.md`.

---

## 1. Introduction: What Is the MAP Type System?

The MAP Type System is:

- **Self-describing**: Holons are typed by descriptor holons, and descriptor holons are themselves holons in the MAP type graph.
- **Compositional**: Holons can be connected through typed relationships to build meaningful semantic graphs.
- **Introspectable**: Any holon can answer:
  - What kind of holon am I?
  - What properties do I have?
  - What relationships do I participate in?
- **Extensible**: Agents can define new types without altering the core codebase.
- **Governable**: Types belong to schemas, and schemas are stewarded within HolonSpaces.

### MAP's Ontology-as-Data Meta-Modeling Approach

The Memetic Activation Platform (MAP) models its ontology as **data**: not as code, not as syntax-bound models, but as a declarative, introspectable system of holons and relationships.

Every type, property, relationship, and rule in the MAP ecosystem is represented as structured data, specifically as one or more descriptor holons and their relationships. This creates the MAP type graph: a self-describing semantic graph in which schemas can be queried, validated, transformed, and evolved using the same mechanisms used for ordinary MAP data.

#### What It Is

- **Ontology-as-data**: Type system elements such as `Book.HolonType`, `Description.PropertyType`, `MetaHolonType`, and `MapStringValueType` are modeled as descriptor holons: structured MAP holons that define types.
- **Declarative architecture**: Relationships, constraints, inheritance, and key rules are declared explicitly rather than implied by code or syntax.
- **Syntax-independent**: The MAP type system is not coupled to OWL, LinkML, JSON Schema, Ecore, or any other concrete modeling syntax.
- **Portable and generative**: Because the ontology is represented as data, it can be transformed into other modeling formats, schemas, documentation, forms, validators, or APIs.

#### Why This Matters

- **Interoperability**: MAP avoids vendor lock-in and can interoperate across tooling ecosystems.
- **Transparency and introspection**: Every visible type system element can be queried, inspected, and reasoned about.
- **Extensibility**: New domain schemas can be introduced declaratively.
- **Automation**: The data-native model supports generation of schemas, forms, validators, visualizers, and adapters.
- **Evolvability**: The underlying semantics can remain stable while external representations evolve.

#### A Foundation for Federated Semantics

This architecture positions MAP as a semantic engine for decentralized systems, federated knowledge graphs, and commons-oriented technology. Semantic clarity, flexibility, and sovereignty are preserved because schemas are represented as data and stewarded within HolonSpaces.

---

## 2. Organizing the MAP Type System

At the heart of MAP is a self-describing type system built from data. The foundational building blocks of this system are **type descriptors**: holons that define the structure, semantics, and constraints of MAP types.

> **Terminology:** A **descriptor holon** is a MAP holon whose role is to define a type. In less formal contexts this document may say “descriptor” or “type descriptor,” but the underlying entity is always a holon in the MAP type graph.

A relatively small number of descriptor types are built into MAP. These provide the foundation from which an open-ended set of domain types can be derived.

Type descriptors are grouped into **schemas**, which are cohesive collections of related type definitions. Each schema defines its own conceptual namespace and boundary of meaning. Every schema is stewarded within a single **HolonSpace**, anchoring it in a governance and trust context. A schema belongs to exactly one HolonSpace, but it may be referenced by types or instances across other spaces.

This layered organization follows a clear pattern:

- Type descriptors define types.
- Schemas group type descriptors.
- HolonSpaces steward schemas.

This structure allows types to evolve in well-bounded contexts while participating in broader federated semantics.

### Three Practical Type Categories

In current MAP architecture, it is useful to distinguish three major practical categories of types:

- **Descriptors**
  - schema-defining and meaning-defining types such as `HolonType`, `PropertyType`, `RelationshipType`, and `ValueType`
- **Runtime Shared Types**
  - the small set of cross-surface runtime-carried types reused inside commands, dances, queries, and related pathways
- **Runtime Envelopes**
  - surface-owned containers such as command, dance, query, and trust-channel request and result wrappers

This document focuses primarily on the descriptor-holon side of the type system. The authoritative definitions are maintained in the `host/import_files/map-schema` folder within the `map-holons` repo.

The canonical definitions for MAP runtime shared types live in `runtime-shared-types.md`.

Runtime envelopes remain documented in their owning surface directories rather than here.

---

## 3. TypeKind: A Semantic Organizing Principle

Every MAP type descriptor declares a **TypeKind**. A TypeKind identifies what kind of type is being described.

TypeKind serves two roles:

1. **Organizational**: It groups descriptors that share structural expectations and validation behavior.
2. **Semantic**: It identifies the ontological kind of thing being defined in the MAP worldview.

Examples:

- `Holon` identifies descriptors that classify data-bearing holons.
- `Property` identifies descriptors that define scalar properties.
- `Relationship` identifies descriptors that define typed links between holons.
- `Value(String)` identifies descriptors for string-like scalar values.
- `EnumVariant` identifies descriptors for enum variants.

TypeKind is not itself the inheritance mechanism. Structural obligations are carried through the descriptor hierarchy using `DescribedBy` and `Extends`.

### Complete List of TypeKinds

The current set of supported TypeKinds is listed below. This set will evolve as MAP matures. Adding a new TypeKind requires a MAP release. Adding new type descriptors within an existing TypeKind does not.

| TypeKind              | Group        | Description                                              |
|-----------------------|--------------|----------------------------------------------------------|
| `Holon`               | Structural   | Describes a type that classifies data-bearing holons     |
| `Property`            | Structural   | Describes a scalar property of a holon                   |
| `Relationship`        | Structural   | Describes a directed link between holons                 |
| `EnumVariant`         | Structural   | Describes a variant in a defined enum                    |
| `Collection`          | Structural   | Describes a named group or set of holons                 |
| `Dance`               | Behavioral   | Describes an interactive protocol or workflow            |
| `Value(String)`       | Scalar Value | A scalar value based on a string                         |
| `Value(Integer)`      | Scalar Value | A scalar value based on an integer                       |
| `Value(Boolean)`      | Scalar Value | A scalar value based on a boolean                        |
| `Value(Enum)`         | Scalar Value | A scalar value selected from a known enumeration         |
| `Value(Bytes)`        | Scalar Value | A binary value serialized as base64                      |
| `ValueArray(String)`  | Scalar Array | An array of strings                                      |
| `ValueArray(Integer)` | Scalar Array | An array of integers                                     |
| `ValueArray(Boolean)` | Scalar Array | An array of booleans                                     |
| `ValueArray(Enum)`    | Scalar Array | An array of enum values                                  |
| `ValueArray(Bytes)`   | Scalar Array | An array of binary values                                |

---

## 4. MAP Meta-Schema v1.2 Model

MAP v1.2 organizes descriptor semantics using four principal levels:

- Meta-Level
- Abstract Type Level
- Core Type Level
- Instance Level

![MAP Schema Diagrams - 4-Level MAP Meta-Schema-v1.2.jpg](../media/MAP%20Schema%20Diagrams%20-%204-Level%20MAP%20Meta-Schema-v1.2.jpg)

The first three levels are made of descriptor holons. The fourth level contains ordinary runtime instances: holons described by concrete descriptor holons.

### Architectural Summary

- `MetaTypeDescriptor` is the abstract root of the descriptor inheritance hierarchy.
- TypeKind-specific meta-types extend `MetaTypeDescriptor`.
- Abstract type descriptors extend the meta-type appropriate to their TypeKind.
- Concrete type descriptors extend the abstract type descriptor appropriate to their TypeKind.
- Runtime instances are described by concrete type descriptors.
- `TypeDescriptor` is self-describing and serves as the concrete bootstrap descriptor for descriptor holons.
- Inheritance is single, additive, and monotonic.

### The Three Independent Axes

The MAP type system depends on keeping three axes distinct. All three axes are relationships among holons, and the descriptor side of these relationships forms the MAP type graph.

#### `DescribedBy`

`DescribedBy` answers:

- What descriptor defines this holon?
- What is this holon's immediate type?

It is a relationship from an instance to its descriptor.

When MAP evaluates `Instance DescribedBy Type`, it evaluates the effective definition of `Type` after flattening the full `Extends` hierarchy of that type.

Examples:

- `MAP Metaschema` is `DescribedBy` `Schema.HolonType`
- `Schema.HolonType` is `DescribedBy` `TypeDescriptor`
- `TypeName.PropertyType` is `DescribedBy` `TypeDescriptor`

#### `Extends`

`Extends` answers:

- What more general type does this descriptor inherit from?
- What obligations does it add to?

It is a relationship between type descriptor holons.

`Extends` is transitive, additive, monotonic, and structure-preserving. No transformation occurs across `Extends`: if a parent type declares an `InstanceProperties` or `InstanceRelationships` relationship, the child inherits that same relationship as a relationship on the child type.

Examples:

- `Schema.HolonType` extends `HolonType`
- `TypeName.PropertyType` extends `PropertyType`
- `HolonType` extends `MetaHolonType`
- `MetaHolonType` extends `MetaTypeDescriptor`

#### `Instances`

Instances are holons that instantiate a type by being `DescribedBy` a concrete descriptor holon. They have a `DescribedBy` relationship to their type descriptor holon. The properties and relationships they may populate are determined by the effective `InstanceProperties` and `InstanceRelationships` of their describing type after `Extends` flattening.

`Instances` is the inverse of the DescribedBy relationship.
Examples:

- `Schema.HolonType` has instances such as `MAP Metaschema`
- `TypeDescriptor` has instances such as `Schema.HolonType`, `Book.HolonType`, and `TypeName.PropertyType`

### Why the Distinction Matters

This distinction is the central architectural key to the v1.2 model.

A descriptor holon such as `TypeName.PropertyType` is a single holon. MAP does not create a second companion holon to hold its descriptor-wide metadata.

Instead:

- `TypeName.PropertyType` stores its own authored properties such as `type_name`, `display_name`, and `description`
- `TypeName.PropertyType` is `DescribedBy` `TypeDescriptor`
- `TypeName.PropertyType` extends `PropertyType`

This means:

- descriptor-wide semantics come from the `DescribedBy -> TypeDescriptor` axis
- TypeKind-specific semantics come from the `Extends -> PropertyType` axis

These axes must never be conflated.

If `DescribedBy` and `Extends` are confused, the model collapses into false multiple inheritance or into the mistaken idea that each descriptor is composed from multiple instantiated companion holons.

### Diagram and JSON Shorthand

In diagrams, stereotype notation such as `<<MetaHolonType>>` is shorthand for `DescribedBy`.

In JSON import files, the `type` field is shorthand for `DescribedBy`.

For example:

    {
      "key": "Schema.HolonType",
      "type": "#TypeDescriptor",
      "properties": {
        "type_name": "Schema",
        "type_kind": "Holon",
        "is_abstract_type": false
      },
      "relationships": [
        {
          "name": "Extends",
          "target": { "$ref": "#HolonType" }
        }
      ]
    }

This means:

- `Schema.HolonType` is `DescribedBy` `TypeDescriptor`
- `Schema.HolonType` extends `HolonType`
- `Schema.HolonType` is a concrete holon type descriptor
- runtime schema holons may be `DescribedBy` `Schema.HolonType`

---

## 5. MetaTypeDescriptor

`MetaTypeDescriptor` is the unique abstract root of the descriptor inheritance hierarchy.

It defines the characteristics all descriptors share. These include descriptor-wide semantics such as:

- `TypeName`
- `TypeNamePlural`
- `DisplayName`
- `DisplayNamePlural`
- `Description`
- `TypeKind`
- `ComponentOf`
- `UsesKeyRule`
- `Extends`

It also defines the abstract descriptor-wide interpretation of:

- `InstanceProperties`
- `InstanceRelationships`

At this level, these do not yet mean ordinary runtime instance surface. Instead, they define the descriptor obligations that descriptor holons inherit as part of the bootstrap model.

### Bootstrap Role

`MetaTypeDescriptor` exists to make the descriptor world legible to itself.

It is abstract, but it allows the system to state that descriptor holons have shared obligations before any specific TypeKind branch is considered.

`TypeDescriptor` then serves as the concrete self-describing bootstrap descriptor holon that realizes those semantics for descriptor holons.

### Special Bootstrap Note

Because `TypeDescriptor` is self-describing, the bootstrap relationship between `MetaTypeDescriptor`, `TypeDescriptor`, and descriptor holons requires careful interpretation:

- `MetaTypeDescriptor` defines the abstract root semantics all descriptors inherit
- `TypeDescriptor` is a concrete descriptor holon in the graph
- descriptor holons are `DescribedBy` `TypeDescriptor`
- descriptor holons may therefore be self-describing without requiring a second companion descriptor holon per definition

The crucial propagation rule is that `DescribedBy` does not copy descriptor relationship types onto the described holon. Instead, it interprets populated `InstanceProperties` and `InstanceRelationships` declared on the effective describing type and exposes only their targets as the described holon's ordinary instance surface.

---

## 6. Meta-Types

Meta-types define the obligations for descriptors of a given TypeKind.

Top-level meta-types extend `MetaTypeDescriptor`:

- `MetaHolonType`
- `MetaPropertyType`
- `MetaValueType`
- `MetaRelationshipType`

Sub-meta-types may extend other meta-types. For example:

- `MetaDeclaredRelationshipType` extends `MetaRelationshipType`
- `MetaInverseRelationshipType` extends `MetaRelationshipType`

### MetaHolonType

`MetaHolonType` defines the obligations of holon type descriptors.

It declares the semantics shared by `HolonType` descriptors, including:

- `InstanceProperties`
- `InstanceRelationships`
- `DescribedBy`
- `OwnedBy`

Concrete examples that ultimately inherit through this branch include:

- `Schema.HolonType`
- `HolonSpace.HolonType`
- `Book.HolonType`
- `Person.HolonType`

### MetaPropertyType

`MetaPropertyType` defines the obligations of property type descriptors.

It declares that property type descriptors specify:

- `IsRequired`
- `ValueType`

Concrete examples include:

- `Description.PropertyType`
- `DisplayName.PropertyType`
- `TypeName.PropertyType`

### MetaValueType

`MetaValueType` defines the obligations of value type descriptors.

Value types describe scalar or scalar-array value semantics. They do not declare ordinary instance properties or instance relationships because values are not holons and do not participate in relationships as holons.

Concrete examples include:

- `MapStringValueType`
- `MapIntegerValueType`
- `MapBooleanValueType`
- `MapBytesValueType`
- `MapEnumValueType`

### MetaRelationshipType

`MetaRelationshipType` defines the obligations of relationship type descriptors.

Relationship type descriptors may specify:

- `SourceType`
- `TargetType`
- `MinCardinality`
- `MaxCardinality`
- `DeletionSemantic`
- `IsDefinitional`
- `AllowsDuplicates`
- `IsOrdered`

Sub-meta-types specialize this pattern for declared and inverse relationship types.

### MetaInverseRelationshipType

`MetaInverseRelationshipType` additionally defines:

- `InverseOf`

---

## 7. Abstract Type Descriptors

Abstract type descriptors extend the meta-type appropriate to their TypeKind and anchor inheritance hierarchies for their TypeKind.

Examples:

| Abstract Type Descriptor   | Extends                        |
|----------------------------|--------------------------------|
| `HolonType`                | `MetaHolonType`                |
| `PropertyType`             | `MetaPropertyType`             |
| `ValueType`                | `MetaValueType`                |
| `DeclaredRelationshipType` | `MetaDeclaredRelationshipType` |
| `InverseRelationshipType`  | `MetaInverseRelationshipType`  |

Abstract type descriptors are not instantiable. No ordinary runtime holon may be directly `DescribedBy` an abstract type descriptor.

Their purpose is to:

- define reusable TypeKind-specific semantics
- serve as inheritance anchors for concrete type descriptors
- provide stable source and target anchors for core relationship types
- allow validation to be expressed against abstract categories while runtime instances use concrete descriptors

Examples:

- `Schema.HolonType` extends `HolonType`
- `Description.PropertyType` extends `PropertyType`
- `MapStringValueType` extends `ValueType`
- `ComponentOf.RelationshipType` extends `DeclaredRelationshipType`

---

## 8. TypeDescriptor

`TypeDescriptor` is the concrete bootstrap descriptor for descriptor holons.

It is self-describing.

This means:

- `TypeDescriptor` is itself a holon in the graph
- `TypeDescriptor` is `DescribedBy` `TypeDescriptor`
- `TypeDescriptor` extends `HolonType`

`TypeDescriptor` therefore sits at a special boundary in the architecture:

- it is concrete because it is an actual holon in the graph
- it is bootstrap because it is the descriptor used by descriptor holons
- it is root-like because descriptor holons depend on it for their immediate descriptive identity

### What TypeDescriptor Does

`TypeDescriptor` does not exist as a separate companion holon for each descriptor definition.

For example, when MAP loads `TypeName.PropertyType`, it does not instantiate both:

- `TypeName.PropertyType`
- a separate per-definition `TypeDescriptor`

Instead, MAP instantiates one descriptor holon:

- `TypeName.PropertyType`

That holon:

- stores its own authored fields such as `type_name = "TypeName"`
- is `DescribedBy` the shared `TypeDescriptor`
- extends `PropertyType`

So `TypeDescriptor` is not a per-descriptor payload container. It is the concrete bootstrap descriptor that makes descriptor holons legible as descriptors.

### Effective Semantics of Descriptor Holons

For a descriptor holon such as `TypeName.PropertyType`, the effective obligations are the combination of:

- authored properties and relationships on `TypeName.PropertyType`
- descriptor-wide semantics propagated from `TypeDescriptor`
- inherited TypeKind-specific semantics from the `PropertyType` lineage

More precisely:

- `Extends` carries descriptor structure forward unchanged
- `DescribedBy` consumes populated `InstanceProperties` and `InstanceRelationships` from the effective describing type
- only the populated targets of those relationships become ordinary properties and relationships available on the described holon
- the relationship types `InstanceProperties` and `InstanceRelationships` do not themselves propagate onto the described holon

This is the key interpretive rule of the v1.2 design.

---

## 9. Concrete Type Descriptors

Concrete type descriptors define actual MAP types.

Each concrete type descriptor:

- is `DescribedBy` `TypeDescriptor`
- extends the abstract type descriptor appropriate to its TypeKind
- fulfills inherited descriptor obligations
- may describe runtime instances
- participates in schemas
- may be keyed or keyless depending on its key rule

Examples:

| Concrete Type Descriptor       | Described By      | Extends                    |
|--------------------------------|-------------------|----------------------------|
| `TypeDescriptor`               | `TypeDescriptor`  | `HolonType`                |
| `Schema.HolonType`             | `TypeDescriptor`  | `HolonType`                |
| `HolonSpace.HolonType`         | `TypeDescriptor`  | `HolonType`                |
| `Description.PropertyType`     | `TypeDescriptor`  | `PropertyType`             |
| `MapStringValueType`           | `TypeDescriptor`  | `ValueType`                |
| `ComponentOf.RelationshipType` | `TypeDescriptor`  | `DeclaredRelationshipType` |

A concrete type descriptor is a holon while also defining a type for other holons. These are separate axes.

For example, `Schema.HolonType` is:

- described by `TypeDescriptor`, because it is a descriptor holon
- extended from `HolonType`, because it is a concrete specialization of the abstract holon type root
- used to describe schema holon instances, such as `MAP Metaschema`

This is not multiple inheritance. It is one `DescribedBy` relationship plus one `Extends` relationship.

---

## 10. Runtime Instances

Runtime instances are the ordinary holons that populate MAP HolonSpaces.

They:

- are described by concrete type descriptors
- include values for properties specified by their type
- participate in relationships specified by their type
- may be keyed or keyless depending on the `UsesKeyRule` of their type descriptor

Examples:

- `MAP Metaschema` is described by `Schema.HolonType`
- a specific HolonSpace is described by `HolonSpace.HolonType`
- a book holon may be described by `Book.HolonType`
- a person holon may be described by `Person.HolonType`

Runtime instances are never described by abstract type descriptors.

---

## 11. Compositional Inheritance via Extends

MAP uses `Extends` as its inheritance mechanism.

`Extends` means that a type inherits the obligations of a more general type. These obligations may include:

- required properties
- allowed properties
- required relationships
- allowed relationships
- validations
- key rule expectations
- semantic commitments

MAP supports only **single inheritance**:

- a type may extend at most one other type

MAP inheritance is **strictly additive and monotonic**:

- a subtype may add obligations
- a subtype may refine by adding constraints
- a subtype may not remove inherited obligations
- a subtype may not weaken inherited obligations

This keeps type evolution predictable and validation tractable.

### Examples

`MetaPropertyType` extends `MetaTypeDescriptor`.

This means `MetaPropertyType` inherits the descriptor obligations shared by all TypeKinds and adds obligations specific to property type descriptors.

`Description.PropertyType` extends `PropertyType`.

This means `Description.PropertyType` inherits the general obligations of property type descriptors and specializes them for the `description` property.

`Schema.HolonType` extends `HolonType`.

This means `Schema.HolonType` inherits the general obligations of holon type descriptors and specializes them for schema holons.

### Extends Is Not DescribedBy

This must remain explicit:

- `DescribedBy` identifies what descriptor directly types a holon
- `Extends` identifies what more general type a type inherits from

`Schema.HolonType` does not extend `TypeDescriptor`.

It is `DescribedBy` `TypeDescriptor`.

It extends `HolonType`.

This distinction is foundational for reading every MAP schema correctly.

### Formal Semantics of `Extends`

`Extends` is a relationship between types.

If:

`ChildType Extends ParentType`

then `ChildType` inherits the properties and relationships declared on `ParentType`.

Inheritance through `Extends` is:

- transitive
- additive
- monotonic
- structure-preserving

No transformation occurs across `Extends`.

If `ParentType` declares:

`InstanceRelationships -> R`

then `ChildType` inherits:

`InstanceRelationships -> R`

as an `InstanceRelationships` relationship on the child type.

The same rule holds for `InstanceProperties`.

### Formal Semantics of `DescribedBy`

`DescribedBy` is a relationship from an instance to a concrete type.

If:

`Instance DescribedBy Type`

then MAP evaluates the effective definition of `Type`.

The effective definition of `Type` is computed by flattening its full `Extends` hierarchy.

`DescribedBy` does not perform inheritance.

Instead, it interprets populated `InstanceProperties` and `InstanceRelationships` on the effective describing type.

Only the targets of populated `InstanceProperties` and `InstanceRelationships` propagate.

The `InstanceProperties` and `InstanceRelationships` relationship types themselves do not propagate.

### Propagation of `InstanceProperties`

If the effective describing type has:

`InstanceProperties -> P`

where `P` is a `PropertyType`, then an instance described by that type may or must populate property `P`.

This does not mean the instance receives an `InstanceProperties` relationship to `P`.

It means `P` becomes part of the ordinary property surface the instance may populate.

### Propagation of `InstanceRelationships`

If the effective describing type has:

`InstanceRelationships -> R`

where `R` is a `DeclaredRelationshipType`, then an instance described by that type may or must participate in relationship `R`.

This does not mean the instance receives an `InstanceRelationships` relationship to `R`.

It means `R` becomes part of the ordinary relationship surface the instance may populate.

### Descriptor-Level Constraint Relationships Do Not Propagate

Relationships such as:

`InstanceProperties -> PropertyType`

and:

`InstanceRelationships -> DeclaredRelationshipType`

define what a type may declare.

They do not themselves propagate to instances.

Only populated targets propagate across `DescribedBy`.

### Example: Ordinary Runtime Holon

If:

`Book.HolonType InstanceProperties -> Title.PropertyType`

and:

`Book.HolonType InstanceRelationships -> AuthorOf.RelationshipType`

then:

`Emerging World DescribedBy Book.HolonType`

may populate property `Title` and may participate in relationship `AuthorOf`.

But `Emerging World` does not receive `InstanceProperties` or `InstanceRelationships` as relationships.

### Example: Descriptor Holon

If:

`TypeDescriptor InstanceProperties -> TypeName.PropertyType`

and:

`TypeDescriptor InstanceRelationships -> Extends.RelationshipType`

then:

`TypeName.PropertyType DescribedBy TypeDescriptor`

may populate property `type_name` and may participate in relationship `Extends`.

But `TypeName.PropertyType` does not receive `InstanceProperties` or `InstanceRelationships` as relationships.

### TypeDescriptor Bootstrap Invariant

`TypeDescriptor` is the concrete bootstrap type used as the `DescribedBy` target for descriptor holons.

It manually declares an instance surface corresponding to the shared descriptor surface defined by `MetaTypeDescriptor`.

This correspondence is a manually maintained bootstrap invariant:

- `MetaTypeDescriptor` declares the abstract descriptor surface through `InstanceProperties` and `InstanceRelationships`
- `TypeDescriptor` declares the corresponding ordinary property and relationship surface that descriptor holons expose after `DescribedBy` interpretation

---

## 12. Abstract Types as Relationship Anchors

In MAP, relationship type descriptors declare `SourceType` and `TargetType`. These define which kinds of holons a relationship may connect.

To support reusable relationships across schemas and domains, MAP anchors many core relationship types to abstract type descriptors.

Examples:

- `ValueType` has source `PropertyType` and target `ValueType`
- `InstanceProperties` has source `HolonType` and target `PropertyType`
- `InstanceRelationships` has source `HolonType` and target `DeclaredRelationshipType`
- `SourceType` has source `RelationshipType` and target `HolonType`
- `TargetType` has source `RelationshipType` and target `HolonType`

Although abstract type descriptors are not instantiable, they are valid reference anchors in the type graph.

### Validation Behavior

When validating a relationship instance:

- Let `R` be the relationship type descriptor.
- Let `S` be the source holon.
- Let `T` be the target holon.
- Let `R.SourceType` be the expected source type.
- Let `R.TargetType` be the expected target type.

The relationship instance is valid if:

- `S.DescribedBy` is equal to or extends `R.SourceType`
- `T.DescribedBy` is equal to or extends `R.TargetType`

This allows relationship types to be declared once against abstract anchors while remaining applicable to all concrete descriptors that extend those anchors.

---

## 13. Design Principles Recap

1. The MAP type system distinguishes three axes: **description** using `DescribedBy`, **inheritance** using `Extends`, and **instantiation** using `Instances`.

2. The MAP type graph is the graph of descriptor holons and the typed relationships among them.

3. In diagrams, `<<TypeName>>` is shorthand for `DescribedBy`. In JSON, `type` is shorthand for `DescribedBy`.

4. Every ordinary holon must be directly `DescribedBy` exactly one concrete type descriptor.

5. `MetaTypeDescriptor` is the unique abstract root of the descriptor inheritance hierarchy.

6. `MetaTypeDescriptor` declares the shared descriptor semantics inherited by all descriptor branches.

7. The top-level meta-types extend `MetaTypeDescriptor`: `MetaHolonType`, `MetaPropertyType`, `MetaValueType`, and `MetaRelationshipType`.

8. Meta-types define TypeKind-specific descriptor obligations.

9. `MetaHolonType` defines the obligations of holon type descriptors, including `InstanceProperties` and `InstanceRelationships`.

10. `MetaPropertyType` defines the obligations of property type descriptors, including `ValueType` and `IsRequired`.

11. `MetaValueType` defines the obligations of value type descriptors. Value types do not declare ordinary instance properties or instance relationships.

12. `MetaRelationshipType` defines the obligations of relationship type descriptors, including source type, target type, cardinality, deletion semantics, and inverse relationships.

13. Meta-types may have sub-meta-types that extend them, such as `MetaDeclaredRelationshipType` and `MetaInverseRelationshipType` extending `MetaRelationshipType`.

14. Each abstract type descriptor extends the meta-type appropriate to its TypeKind.

15. Abstract type descriptors are not instantiable and serve as inheritance anchors for concrete type descriptors.

16. Concrete type descriptors are `DescribedBy` `TypeDescriptor` and extend the abstract type appropriate to their TypeKind.

17. `TypeDescriptor` is self-describing and serves as the concrete bootstrap descriptor for descriptor holons.

18. A descriptor holon is a single holon. MAP does not instantiate a second companion `TypeDescriptor` holon for each descriptor definition.

19. The effective semantics of a concrete descriptor arise from:
- descriptor-wide semantics interpreted through `DescribedBy -> TypeDescriptor`
- TypeKind-specific obligations inherited through `Extends`
- authored properties and relationships on the concrete descriptor itself

20. A MAP type may extend at most one other type. MAP supports single inheritance only.

21. Inheritance is strictly additive and monotonic. A subtype may add obligations but may not remove or weaken inherited obligations.

22. Only concrete type descriptors describe ordinary runtime instances.

23. Abstract type descriptors are valid relationship anchors even though they are not directly instantiable.

24. `DescribedBy` and `Extends` must never be conflated. The first answers what directly types a holon. The second answers what a type inherits from.

25. `Extends` preserves descriptor structure. If a parent type declares `InstanceProperties` or `InstanceRelationships`, a child type inherits those same relationships unchanged.

26. `DescribedBy` interprets descriptor structure. It consumes populated `InstanceProperties` and `InstanceRelationships` from the effective describing type and exposes only their targets as the described holon's ordinary property and relationship surface.

27. The relationship types `InstanceProperties` and `InstanceRelationships` do not themselves propagate onto described instances.

28. `TypeDescriptor` is a bootstrap special case whose ordinary property and relationship surface must correspond to the abstract descriptor surface defined by `MetaTypeDescriptor`.

---

## 14. Key Rules, Keyed Types, and Keyless Types

MAP supports both keyed and keyless holon types.

A **keyed type** defines instances that have stable semantic identity within a HolonSpace. These instances can be referenced by key in import files and relationship targets.

A **keyless type** defines instances whose identity is contextual. Keyless holons are typically embedded and are not independently referenced.

Key behavior is specified through `UsesKeyRule`.

Examples:

- `TypeName.KeyRule` derives a key from a type name.
- `TypeKind.KeyRule` may derive a key from type name and TypeKind.
- `Relationship.KeyRuleType` derives keys for relationship descriptors from source type, relationship name, and target type.
- `None.KeyRuleType` marks a type as keyless.

The key rule system is part of the descriptor model because key derivation is a semantic obligation of a type.

---

## 15. Base Types and Base Values

Several TypeKinds, such as `Value(String)`, `Value(Boolean)`, or `ValueArray(Enum)`, correspond to scalar value types. These are backed by a fixed set of **Base Types** that define how values are represented, stored, and validated across environments.

### Base Types

Base Types are the foundational portable value types in MAP. A Base Type determines how a value is represented across programming environments such as Rust, TypeScript, and JSON.

The set of Base Types is fixed for a given MAP version. Adding or changing Base Types requires a MAP release because Base Types affect runtime representation and persistence.

### Principle: Preserve Type Identity Across Platforms

The Base Type name should be treated as a portable name, used consistently across environments and interpretable by the MAP type system.

In Rust, type identity is preserved through newtypes such as:

    pub struct MapString(pub String);

In TypeScript and JSON, similar identity can be preserved through type aliases, tagging, or enforced schema constraints.

### Current Base Types with Portable Name Bindings

| Base Type      | Rust Binding                          | TypeScript Binding                         | JSON Binding                                   |
|----------------|---------------------------------------|--------------------------------------------|------------------------------------------------|
| `MapString`    | `pub struct MapString(pub String)`    | `export type MapString = string;`          | `{ "type": "MapString", "value": "..." }`      |
| `MapBoolean`   | `pub struct MapBoolean(pub bool)`     | `export type MapBoolean = boolean;`        | `{ "type": "MapBoolean", "value": true }`      |
| `MapInteger`   | `pub struct MapInteger(pub i64)`      | `export type MapInteger = number;`         | `{ "type": "MapInteger", "value": 42 }`        |
| `MapEnumValue` | `pub struct MapEnumValue(pub String)` | `export type MapEnumValue = string;`       | `{ "type": "MapEnumValue", "value": "DRAFT" }` |
| `MapBytes`     | `pub struct MapBytes(pub Vec<u8>)`    | `export type MapBytes = string; // base64` | `{ "type": "MapBytes", "value": "aGVsbG8=" }`  |

### BaseValue

MAP represents scalar runtime values using the `BaseValue` enum.

    pub enum BaseValue {
        StringValue(MapString),
        BooleanValue(MapBoolean),
        IntegerValue(MapInteger),
        EnumValue(MapEnumValue),
        BytesValue(MapBytes),
    }

Each variant corresponds to a specific MAP Base Type. This allows property values to be stored and inspected uniformly while preserving type identity.

Only `BaseValue` variants may be used as `PropertyValue`s within a holon's `PropertyMap`:

    pub type PropertyValue = BaseValue;
    pub type PropertyMap = BTreeMap<PropertyName, Option<PropertyValue>>;

By wrapping all scalar values in a unified enum, MAP ensures that holon properties are portable, self-describing, and serializable across environments.

### Notes

- Rust bindings use the newtype pattern, such as `pub struct MapString(pub String)`, to distinguish each base type while still leveraging native Rust primitives.
- Base types can support custom trait implementations, typed serialization, deterministic hashing, and compile-time safety.
- `BaseValue` acts as the unified runtime representation of scalar values.
- `BaseValue` includes deterministic binary encoding support, display support, and conversion behavior.
- TypeScript bindings are currently simple aliases for interoperability with JSON and browser-based UIs.
- JSON bindings assume a tagged format for clarity and round-tripping.
- `ValueType` descriptors define the semantic value constraints that property descriptors reference.
- The previously defined `BaseType` enum has been removed. Its former responsibilities are handled by:
  - `TypeKind` for descriptor classification
  - `ValueType` descriptors for scalar semantics
  - `BaseValue` for runtime scalar representation

---

## 16. Summary

The MAP Type System v1.2 separates description, inheritance, and instantiation into distinct axes.

The v1.2 meta-schema model is organized around:

- `MetaTypeDescriptor` as the abstract root of descriptor inheritance
- TypeKind-specific meta-types
- abstract type descriptors that anchor inheritance
- `TypeDescriptor` as the concrete self-describing bootstrap descriptor
- concrete type descriptors that define usable MAP types
- runtime instances described by those concrete type descriptors

This preserves MAP's self-describing, holonic architecture while making explicit the central distinction that keeps the model coherent:

- `DescribedBy` says what directly types a holon
- `Extends` says what a type inherits from

More precisely:

- `Extends` preserves structure
- `DescribedBy` interprets structure
- `Extends` carries `InstanceProperties` and `InstanceRelationships` forward as relationships between types
- `DescribedBy` consumes populated `InstanceProperties` and `InstanceRelationships` and exposes their targets as ordinary properties and relationships on the described instance

The result is a type system that is:

- introspectable
- extensible
- schema-governed
- TypeKind-aware
- single-inheritance
- monotonic
- suitable for open-ended, agent-defined semantics
