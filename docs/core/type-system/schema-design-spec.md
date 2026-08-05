# MAP Schema Design Spec (v2.0)

## 1. Purpose

This specification defines the structural model of the MAP Type System. It
establishes the kinds of schema entities, the relationships among them, the
declaration surfaces carried by each descriptor category, and the structural
invariants every MAP schema must satisfy.

This is a current-state design specification distilled from
[`schema-2.0.md`](schema-2.0.md). The earlier document preserves the reasoning
and comparisons that led to this design; this document states the resulting
design without the proposal history.

## 2. Authority and Boundaries

Authority is divided by concern:

- this specification owns the structural schema model and its invariants;
- the
  [descriptor-kernel semantic rules](descriptor-semantics-rules.md)
  own representation-neutral algorithms for contract resolution, semantic
  inheritance, key-rule resolution, cardinality evaluation, and conformance;
- the [TDL specification](tdl/tdl-spec.md) owns source syntax, binding,
  omission, and lowering behavior;
- the TDL corpus in `map-holons/schema-src` owns exact schema identities,
  descriptor declarations, member inventories, and values; and
- runtime descriptor construction and invocation belong to the runtime
  descriptor documentation.

This specification does not define:

- Rust wrapper or trait APIs;
- loader DTOs or persistence formats;
- TDL or JSON grammar;
- effective-value computation algorithms;
- transaction or storage behavior; or
- component-specific type inventories.

Exact qualified keys shown here are illustrative. The current TDL corpus is
authoritative when an inventory or declaration identity changes.

## 3. Ontology as Data

MAP schemas are represented as MAP data. Types, properties, relationships,
constraints, key rules, and schemas are expressed as holons and relationships
rather than as a separate host-language class model.

A **type descriptor** is a holon that defines a category of instances. It has
two distinct structural roles:

1. As a holon, it must conform to the contract of its own describing type.
2. As a type, it declares the contract imposed on the instances it describes.

These roles are connected but never flattened into one surface.

For example:

```text
Book.HolonType
  DescribedBy MetaHolonType.MetaTypeDescriptor
  Extends HolonType.TypeDescriptor
```

`DescribedBy` determines the contract that `Book.HolonType` must satisfy as a
descriptor holon. `Extends` classifies it as a holon type and contributes to the
contract that it passes to books.

## 4. Three Independent Relationships

Schema 2.0 separates conformance, specialization, and instance discovery.

### 4.1 `DescribedBy`

```text
H --DescribedBy--> T
```

`DescribedBy` identifies the type whose effective instance contract governs
`H`. Every semantically valid holon has exactly one `DescribedBy` target.

The target must be:

- a type in the unified hierarchy rooted at `TypeDescriptor`; and
- non-abstract.

Ordinary holons and descriptor holons use the same relationship. Descriptor
holons are described by the applicable meta-type.

### 4.2 `Extends`

```text
T --Extends--> P
```

`Extends` establishes optional single-parent type specialization. It serves
three purposes:

- subtype classification and substitutability;
- additive inheritance of instance-contract declarations; and
- the lineage over which explicitly declared semantic inheritance may be
  evaluated.

`Extends` does not generally copy or inherit populated descriptor state. A
property or relationship participates in semantic inheritance only according
to its own `InheritanceMode`.

Every `Extends` source and target is a type descriptor. A type has at most one
direct parent, and the complete graph is acyclic.

### 4.3 `Instances`

`Instances` is the inverse of `DescribedBy`:

```text
T --Instances--> H
```

It supports inverse traversal and discovery. Conformance is defined by the
authored `DescribedBy` direction and does not depend on an `Instances`
relationship being physically materialized.

## 5. Instance Contracts

A type declares the contract for its described instances through:

- `InstanceProperties`, targeting property descriptors; and
- `InstanceRelationships`, targeting declared relationship descriptors.

These are contract declarations. They are not ordinary property values or
relationship targets populated on each type descriptor.

The local declarations of a type form its local instance contract. A subtype's
effective instance contract contains its inherited declarations plus its local
declarations. Contract inheritance is additive: a subtype may add members but
may not remove, shadow, or override an inherited member.

Contract-member identity is the identity of the referenced descriptor:

- the referenced `PropertyType` for a property member; or
- the referenced declared relationship descriptor for a relationship member.

A subtype must not redeclare an inherited contract member to alter its value
type, endpoint constraints, cardinality, requiredness, or validation rules.
Distinct member descriptors must not claim the same semantic member name in one
effective contract.

The descriptor-kernel semantic rules define the exact resolution and error
behavior for inherited contracts.

## 6. Unified Descriptor Hierarchy

All descriptor categories participate in one acyclic `Extends` graph rooted at
abstract `TypeDescriptor`.

```text
TypeDescriptor
  HolonType
    MetaTypeDescriptor
      MetaHolonType
      MetaPropertyType
      MetaValueType
        value-family meta-types
      MetaRelationshipType
        MetaDeclaredRelationshipType
        MetaInverseRelationshipType
  PropertyType
  ValueType
    scalar value categories
    enum and enum-variant categories
    value-array categories
  RelationshipType
    DeclaredRelationshipType
    InverseRelationshipType
```

`TypeDescriptor` provides:

- the common classification root for descriptor types;
- a polymorphic relationship target;
- a query root for descriptor types; and
- the common category of schema components.

`MetaTypeDescriptor` extends `HolonType`. Meta-types are therefore holon types
and remain transitively classified as `TypeDescriptor`. The meta-type branch is
a branch of the unified hierarchy, not a separate inheritance graph.

`RelationshipType` is the common classification parent of declared and inverse
relationship descriptors.

Subtype recognition follows transitive `Extends`. It does not follow type
names, TDL declaration forms, key suffixes, or `TypeKind` values.

## 7. Meta-Types and Descriptor Categories

Meta-types define the self-conformance contracts of descriptor holons.
Descriptor categories classify the instances and relationship endpoints those
descriptors describe.

The distinction is structural:

- `MetaPropertyType` describes property descriptor holons;
- `PropertyType` classifies property descriptors in relationships and queries;
- `MetaDeclaredRelationshipType` describes declared relationship descriptor
  holons; and
- `DeclaredRelationshipType` classifies declared relationship descriptors.

The applicable meta-type is selected through `DescribedBy`. The descriptor's
semantic category is selected through its `Extends` lineage. Extending
`PropertyType` does not replace being described by `MetaPropertyType`, and
being described by `MetaPropertyType` does not place meta-type declarations in
the contracts of ordinary instances.

### 7.1 Reflective fixed point

Meta-types are themselves descriptor holons and are described by
`MetaHolonType`. `MetaHolonType` is explicitly self-describing:

```text
MetaHolonType --DescribedBy--> MetaHolonType
```

This authored fixed point terminates the reflective model. It is not a hidden
bootstrap mode and does not depend on descriptor names or omitted
relationships.

Circular source dependencies needed to express the fixed point are handled by
the schema loader's multi-pass loading process. They do not introduce a
different schema-validity model.

### 7.2 `TypeKind`

`TypeKind` records the semantic kind of a descriptor. It supports
classification-oriented metadata, tooling, and presentation.

`TypeKind` does not determine:

- the target of `DescribedBy`;
- compatibility of an `Extends` edge;
- conformance obligations;
- endpoint substitutability; or
- runtime wrapper selection.

Those behaviors follow authored graph relationships and descriptor contracts.

## 8. Descriptor Declaration Surfaces

The meta-type contracts define which structural members each descriptor
category carries. The TDL corpus owns the exact member inventory; this section
defines the role of each surface.

### 8.1 Common type-descriptor surface

Every type descriptor carries common identity and descriptive metadata and is
a component of one schema. The common structural surface includes:

- type identity and display metadata;
- `IsAbstractType`;
- `TypeKind`;
- `ComponentOf`;
- optional `Extends`; and
- other cross-cutting descriptor relationships defined by the Core Schema.

### 8.2 Holon-type descriptors

A holon-type descriptor may define:

- an `InstanceKeyRule` for its described instances;
- `InstanceProperties`;
- `InstanceRelationships`;
- whether additional properties are allowed; and
- whether additional relationships are allowed.

Keylessness is represented by an explicit effective key-rule target, currently
`NoneRule.KeyRuleType`, rather than by a missing semantic rule. Exact key-rule
resolution belongs to the descriptor-kernel semantic rules.

### 8.3 Property descriptors

The property-descriptor contract defines:

- exactly one governing `ValueType`;
- whether the property value is required;
- an optional `DefaultValue`; and
- an `InheritanceMode` for populated values carried through the property.

`DefaultValue` uses a broad `BaseValue` representation, but a populated default
must also conform to the `ValueType` selected by its containing property
descriptor.

### 8.4 Value-type descriptors

Value-type descriptors classify values and identify their representation and
validation family. Specialized value categories provide additional structural
members, including:

- operators afforded by the value type;
- variants owned by enum value types;
- the element value type of value arrays; and
- family-compatible value constraints.

Value-constraint declarations and their evaluation are delegated to the
[value constraints design](value-constraints-design-spec.md)
and the descriptor-kernel semantic rules.

### 8.5 Relationship descriptors

Every concrete relationship descriptor defines a direction with:

- exactly one source-type constraint;
- exactly one target-type constraint;
- minimum cardinality;
- optional maximum cardinality;
- ordering policy;
- duplicate policy;
- definitional status;
- directional deletion semantics; and
- semantic inheritance mode.

`MinCardinality` is required. An absent `MaxCardinality` means unbounded; no
finite integer is reserved as an unbounded sentinel.

Declared relationships and inverse relationships are separate descriptor
holons. Every declared relationship has one authoritative inverse, and every
inverse identifies its declared relationship. Source and target constraints,
cardinality, and deletion semantics are directional properties of each
descriptor. Inverse-direction behavior is explicit rather than inferred by
swapping or copying the declared direction.

Relationship semantics beyond this structural surface are delegated to the
[relationship constraints design](relationship-constraints-design-spec.md)
and the descriptor-kernel semantic rules. Persistence of relationship
occurrences is outside the type-system schema model.

## 9. Instance Key Rules

A semantic key identifies a holon according to rules declared by its type. It
is distinct from the holon's immutable `HolonId` and from any storage-specific
identifier.

Key derivation is modeled in the schema rather than hard-coded into declaration
syntax or Rust types. Key rules are ordinary holonic schema entities rooted at
abstract `KeyRuleType.HolonType`. A key-rule target may be:

- a concrete key-rule type descriptor representing a reusable derivation
  strategy; or
- an ordinary configured key-rule holon described by a concrete key-rule type,
  such as an instance of `FormatRule.KeyRuleType`.

### 9.1 `InstanceKeyRule`

Holon types select the rule for their described instances through:

```text
(HolonType.TypeDescriptor)
  --InstanceKeyRule-->
(KeyRuleType.HolonType)
```

The relationship has cardinality `1..1` and `InheritanceMode Override`.
Consequently, every non-abstract holon type has exactly one effective instance
key rule, supplied locally or by its nearest contributing ancestor.

`KeyRuleForInstancesOf` is the inverse traversal from a key rule to the holon
types selecting it. Selection semantics remain authoritative in the
`InstanceKeyRule` direction.

The selected rule governs holons described by the source type. It does not
govern the key of the source descriptor holon itself.

For example:

```text
Book.HolonType
  DescribedBy MetaHolonType.MetaTypeDescriptor
  InstanceKeyRule -> TitleAuthor.FormatRule
```

`TitleAuthor.FormatRule` governs books described by `Book.HolonType`. The key
of the `Book.HolonType` descriptor holon is governed by the effective instance
key rule of its describing type, `MetaHolonType.MetaTypeDescriptor`.

Ordinary holons and descriptor holons therefore use the same key-selection
model: find the holon's `DescribedBy` target, then use that type's effective
`InstanceKeyRule`.

Only holon types select instance key rules. Property values, value instances,
and relationship occurrences are not independent holons and do not have
independent semantic keys.

### 9.2 Explicit keylessness

Keylessness is represented by selecting `NoneRule.KeyRuleType`. It is not
represented by an absent effective key rule.

`HolonType.TypeDescriptor` establishes `NoneRule.KeyRuleType` as the root
baseline. A holon type therefore describes keyless instances unless it or a
nearer ancestor selects another rule.

The explicit target keeps keyed and keyless types within the same cardinality
and inheritance model and prevents absence from carrying two meanings.

### 9.3 Descriptor keys

`MetaTypeDescriptor.HolonType` selects `ExtendedTypeRule.KeyRuleType` as the
inherited baseline for descriptor holons. This makes descriptor identity a
consequence of the key rule selected by the descriptor's meta-type rather than
of a TDL declaration form or key suffix.

Specialized meta-types may override that baseline. For example,
`MetaRelationshipType.MetaTypeDescriptor` selects the relationship key rule,
and `MetaEnumVariantValueType.MetaValueType` selects the enum-variant key rule.

### 9.4 Core key-rule families

The current Key Rule Schema defines reusable strategies for:

- type-name keys;
- schema-name keys;
- type-kind-qualified keys;
- enum-variant keys;
- relationship descriptor keys;
- extended-type descriptor keys;
- described-type-qualified keys;
- configured format keys; and
- explicit keylessness.

The TDL corpus owns the exact key-rule inventory and identities. In the current
corpus these strategies include `TypeNameRule.KeyRuleType`,
`SchemaNameRule.KeyRuleType`, `TypeKindRule.KeyRuleType`,
`EnumVariantRule.KeyRuleType`, `RelationshipRule.KeyRuleType`,
`ExtendedTypeRule.KeyRuleType`, `DescribedTypeRule.KeyRuleType`,
`FormatRule.KeyRuleType`, and `NoneRule.KeyRuleType`.

Configured format rules are ordinary holons. Their schema contract includes a
template string and an ordered `TemplateParameters` relationship to the
property descriptors whose values supply the template parameters.

The descriptor-kernel semantic rules own effective key-rule resolution,
required-input validation, and key derivation. The TDL specification owns
validation of authored declaration keys and the `instance_keyrule` shorthand.

## 10. Endpoint Classification

Every relationship endpoint is a holon. Endpoint constraints name holon-type
descriptors, including abstract holon types used as polymorphic anchors.

An ordinary holon is classified for endpoint compatibility by its
`DescribedBy` target. A descriptor holon is classified by its own descriptor
identity and transitive `Extends` lineage. This permits relationships to target
abstract categories such as `TypeDescriptor`, `PropertyType`, `ValueType`, or
`RelationshipType` without using their describing meta-types as endpoint
categories.

The descriptor-kernel semantic rules define the uniform endpoint-compatibility
algorithm.

## 11. Abstract Descriptors

An abstract descriptor may:

- participate in `Extends`;
- provide inherited instance-contract declarations;
- serve as a polymorphic relationship endpoint constraint; and
- participate in type queries and subtype classification.

An abstract descriptor may not directly describe a concrete runtime holon.

Abstract descriptors need not fabricate concrete descriptor state solely to
satisfy positive minimum cardinalities in their own self-conformance contract.
This completeness exemption applies only to absence. Any member they do
populate remains subject to declaration identity, value and endpoint
constraints, maximum cardinality, and all other applicable rules.

Abstract descriptors remain subject to universal structural invariants,
including explicit `DescribedBy`, schema membership, and single acyclic
`Extends`.

## 12. Inheritance Declarations

Schema 2.0 distinguishes two forms of inheritance.

### 12.1 Contract inheritance

`Extends` always provides additive inheritance of `InstanceProperties` and
`InstanceRelationships`. A subtype may add contract members but does not alter
inherited declarations.

### 12.2 Semantic inheritance

Each non-abstract property and relationship descriptor carries an
`InheritanceMode` that controls whether values populated through that member
participate in effective descriptor semantics across `Extends`.

The Core Schema defines three modes:

- `None`: populated values remain local;
- `Additive`: inherited and local contributions accumulate; and
- `Override`: the nearest populated contribution set takes precedence.

`InheritanceMode` is required and has a materialized default of `None`.
Inheritance does not copy effective values into local descriptor state.

The descriptor-kernel semantic rules own effective-value resolution, duplicate
elimination, provenance, cardinality evaluation, and error behavior.

## 13. Required Properties and Defaults

`DefaultValue` is part of the property-descriptor structure. A default is valid
only when `IsValueRequired` is true.

The valid structural combinations are:

| Required | Default | Meaning                                |
|----------|---------|----------------------------------------|
| No       | Absent  | Omission represents absence            |
| Yes      | Absent  | Creation must supply a value           |
| Yes      | Present | Completion may materialize the default |

An optional property with a default is invalid because omission would be
ambiguous between absence and default application.

Defaults are creation-time completion declarations, not read-time fallback
state. Every creation path must materialize applicable defaults before
descriptor-kernel validation. The kernel validates the resulting explicit
representation but does not inject defaults or otherwise mutate it.

Once materialized, a default is ordinary explicit state. Changing a descriptor
default does not implicitly change previously created holons.

The completion procedure and conformance checks are defined by the
descriptor-kernel semantic rules. TDL omission behavior is defined by the TDL
specification.

## 14. Schemas and Dependencies

A `Schema` holon identifies a logical collection of descriptor components.
Every descriptor belongs to exactly one schema through `ComponentOf`.

A schema may declare `DependsOn` relationships to other schemas whose
definitions are required for reference resolution and validation. Schema
dependencies may be mutually recursive. Loading therefore operates over a
dependency closure with multiple passes rather than requiring the dependency
graph to be a simple DAG.

Logical ownership and physical source placement are separate:

- each component owns the meaning and behavioral documentation of its schema
  concepts; and
- all authoritative MAP schema TDL files remain physically centralized in
  `map-holons/schema-src` to support imports and corpus-wide loading.

The planned `schema-catalog.md` will map logical schema identities, owning
components, dependencies, and TDL source files without duplicating their
declarations.

## 15. Extension Schemas

The structural model applies equally to MAP Core schemas and Extension
Schemas. An Extension Schema may define new descriptors and may extend types
owned by MAP Core or by another extender, subject to schema dependency and
extension-compatibility rules.

Extension Schemas do not receive a different descriptor hierarchy, conformance
model, or runtime representation. Cross-schema ownership, compatibility,
versioning, and evolution rules belong in the planned
`extension-schema-design.md`.

## 16. Structural Invariants

A valid Schema 2.0 graph satisfies all of the following:

1. Every holon has exactly one explicit or completed `DescribedBy` target.
2. Every describing type is non-abstract and transitively classified under
   `TypeDescriptor`.
3. Every type has at most one direct `Extends` parent.
4. Every `Extends` source and target is a type descriptor.
5. The complete `Extends` graph is acyclic.
6. `TypeDescriptor` is the abstract root of the unified descriptor hierarchy.
7. `MetaTypeDescriptor` extends `HolonType` and roots the meta-type branch.
8. `RelationshipType` roots the declared and inverse relationship categories.
9. Meta-types govern descriptor-holon conformance through `DescribedBy`;
   abstract descriptor categories govern classification through `Extends`.
10. `InstanceProperties` target property descriptors and
    `InstanceRelationships` target declared relationship descriptors.
11. Contract inheritance is additive; inherited contract members cannot be
    removed, shadowed, or redeclared.
12. Every descriptor belongs to exactly one schema through `ComponentOf`.
13. Every non-abstract holon type has exactly one effective `InstanceKeyRule`
    target classified under `KeyRuleType`.
14. Keylessness is represented by the explicit `NoneRule.KeyRuleType` target,
    not by an absent effective key rule.
15. An `InstanceKeyRule` governs instances described by its source holon type;
    it does not govern the key of the source descriptor holon.
16. Every non-abstract property descriptor selects exactly one value type.
17. A default may be defined only for a required property.
18. Every concrete relationship descriptor has exactly one source type and one
    target type.
19. Every concrete relationship descriptor has a required minimum cardinality;
    an absent maximum means unbounded.
20. Every concrete declared relationship and inverse relationship has explicit
    directional deletion semantics.
21. Every concrete declared relationship has one authoritative inverse, and
    every concrete inverse identifies its declared relationship.
22. Abstract descriptors cannot directly describe concrete runtime holons but
    may serve as inheritance and endpoint anchors.
23. `TypeKind` does not replace graph-based conformance, classification, or
    endpoint compatibility.
24. A property's or relationship's populated values inherit only according to
    that member descriptor's materialized `InheritanceMode`.
25. Exact schema declarations and identities come from the authoritative TDL
    corpus rather than generated JSON, loader DTOs, or Rust type definitions.

## 17. Related Documents

- [`map-type-system.md`](map-type-system.md) provides the conceptual overview.
- [`descriptor-semantics-rules.md`](descriptor-semantics-rules.md)
  defines representation-neutral computation and validation.
- [`tdl-spec.md`](tdl/tdl-spec.md) defines the schema authoring language.
- [`value-constraints-design-spec.md`](value-constraints-design-spec.md)
  defines the value-constraint model.
- [`relationship-constraints-design-spec.md`](relationship-constraints-design-spec.md)
  defines specialized relationship constraints.
- [`layered-desc-arch.md`](../descriptors/layered-desc-arch.md) defines the
  construction, completion, and descriptor-kernel integration layers.
- [`document-role-manifest.md`](../document-role-manifest.md) defines document
  ownership and scoped authority.
