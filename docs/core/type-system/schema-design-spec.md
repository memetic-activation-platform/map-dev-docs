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
  own representation-neutral algorithms for effective instance-contract interpretation, semantic
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
relationship being physically materialized. Committed inverse traversal does:
commit must materialize the paired `Instances` occurrence or report the
non-complete outcome required by the relationship persistence specification.

## 5. Instance Contracts

A type declares the contract for its described instances through:

- `InstanceProperties`, targeting property descriptors; and
- `InstanceRelationships`, targeting declared relationship descriptors.

These are contract declarations. They are not ordinary property values or
relationship targets populated on each type descriptor.

The local declarations of a type form its local instance contract. The
effective declarations reached through `InstanceProperties` and
`InstanceRelationships` are resolved according to the `InheritanceMode`
materialized on those relationship descriptors. The Core Schema sets both to
`Additive`, so a subtype's effective instance contract contains inherited and
local declarations. A subtype may add members but may not remove, shadow, or
override an inherited member.

Contract-member identity is the identity of the referenced descriptor:

- the referenced `PropertyType` for a property member; or
- the referenced declared relationship descriptor for a relationship member.

A subtype must not redeclare an inherited contract member to alter its value
type, endpoint constraints, cardinality, requiredness, or validation rules.
Distinct property descriptors must not have the same local `TypeName` in one
effective property contract. Distinct relationship descriptors must not have
the same local `TypeName` in one effective relationship contract. Property and
relationship names occupy separate namespaces.

These names are exact, case-sensitive `MapString` values derived from each
descriptor's required local `TypeName`; the semantic layer performs no Unicode
normalization. The construction and validation boundary binds names to
descriptor identity before conformance and occurrence grouping proceed.

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

This authored fixed point closes the reflective model. It is not a hidden
bootstrap mode and does not depend on declaration forms or omitted
relationships. It is the only permitted `DescribedBy` cycle. Starting from
any holon and repeatedly following `DescribedBy` must reach this self-loop
without first repeating another identity.

Circular references among components of the same schema needed to express the
fixed point are handled by the schema loader's multi-pass loading process.
They do not introduce a different schema-validity model or a cycle between
schema holons.

Reference resolution and semantic evaluation are distinct. Once references
are resolved, the kernel computes and memoizes effective contracts and other
effective products by descriptor identity for the current graph snapshot. It
then validates holons against those products. Contract computation does not
recursively validate the descriptor whose contract is being computed, so the
reflective self-loop does not cause unbounded conformance recursion.

`MetaHolonType.MetaTypeDescriptor` is concrete and must conform to its own
effective instance contract. Adding a required member to that meta contract
therefore also adds a requirement to the reflective root itself. The revised
schema is invalid unless the root supplies a conforming value or completion
materializes a valid descriptor-defined default. Schema authors must validate
this self-conformance before publishing the schema package.

### 7.2 `TypeKind`

`TypeKind` is a derived runtime and tooling projection, not authored descriptor
state. A descriptor's category is established by its resolved identity and
transitive `Extends` lineage. Typed wrapper construction and category-specific
behavior test that lineage against the wrapper's required category anchor.

Where an API still exposes a `TypeKind` enum, its value must be derived from
that lineage classification and any additional authoritative descriptor
semantics represented by the enum, such as an array's effective element value
type. It may cache or summarize those established facts, but it must not be
independently authored, persisted, defaulted, or accepted as competing
evidence of classification.

Accordingly, `TypeKind.PropertyType` is not part of the Schema 2.0 common
descriptor contract. The legacy authored `TypeKind`/`InstanceTypeKind`
property surface and any key rule that requires such a populated property must
be retired or rewritten to consume lineage-derived classification.

## 8. Descriptor Declaration Surfaces

The meta-type contracts define which structural members each descriptor
category carries. The TDL corpus owns the exact member inventory; this section
defines the role of each surface.

The entries below describe semantic fields, not a requirement that consumers
read locally populated state directly. For any property or relationship
descriptor, the descriptor kernel resolves each field across that descriptor's
own `Extends` lineage according to the field descriptor's `InheritanceMode`.
The resulting `EffectiveMemberDefinition` is the authoritative view consumed
by conformance, default materialization, cardinality, endpoint validation,
collection policy, and key-rule selection.

`InheritanceMode.PropertyType` anchors this interpretation by declaring its
own `InheritanceMode` as `None`. Its required default of `None` is materialized
locally on other applicable concrete descriptors during completion, so the
policy that governs a member is available without inheriting that field from
the member's parent.

### 8.1 Common type-descriptor surface

Every type descriptor carries common identity and descriptive metadata and is
a component of one schema. The common structural surface includes:

- type identity and display metadata;
- `IsAbstractType`;
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

For every pair, the inverse's effective source constraint must equal the
declared descriptor's effective target constraint, and its effective target
constraint must equal the declared descriptor's effective source constraint.
The two directions describe one occurrence graph with shared semantic
occurrence identity. Their cardinalities remain independent and are evaluated
per source in their respective directions.

Inverse occurrences are derived from authoritative declared occurrences and
materialized by commit. They do not represent virtual edges contributed by the
declared relationship's semantic inheritance. Pairwise deletion execution is
still proposed and is delegated to the relationship constraints and
relationship persistence specifications.

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

`KeyRuleForInstancesOf` traverses materialized inverse occurrences to holon
types that explicitly populate `InstanceKeyRule`. It does not enumerate
descendant types that merely inherit the same effective selection through
`Override`. Selection semantics remain authoritative in the `InstanceKeyRule`
direction; finding every effective user requires effective-key-rule evaluation
over candidate types.

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
inherited baseline for descriptor holons. This makes a descriptor's semantic key a
consequence of the key rule selected by the descriptor's meta-type rather than
of a TDL declaration form or key suffix.

Under the current `ExtendedTypeRule`, changing the immediate `Extends` parent
changes the derived key for subsequently created descriptor versions. Because
`Extends` is definitional, this is a breaking schema change rather than a
key-stable internal refactor.

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

The TDL corpus owns the exact key-rule inventory and identities. Target
strategies include `TypeNameRule.KeyRuleType`,
`SchemaNameRule.KeyRuleType`,
`EnumVariantRule.KeyRuleType`, `RelationshipRule.KeyRuleType`,
`ExtendedTypeRule.KeyRuleType`, `DescribedTypeRule.KeyRuleType`,
`FormatRule.KeyRuleType`, and `NoneRule.KeyRuleType`.

The transitional `TypeKindRule.KeyRuleType` depends on the retired authored
`TypeKind` property and is not part of the target inventory. A future key rule
may deliberately consume lineage-derived category identity, but it must define
that input and its key-stability consequences independently.

Configured format rules are ordinary holons. Their schema contract includes a
template string and an ordered `TemplateParameters` relationship to the
property descriptors whose values supply the template parameters.

The descriptor-kernel semantic rules own effective key-rule resolution,
required-input validation, and key derivation. The TDL specification owns
validation of authored declaration keys and the `instance_keyrule` shorthand.

Keys must be unique within the bound schema package and dependency closure.
Cross-schema qualification and coexistence of colliding local keys are deferred
to the WIP Extension Schema identity design; this specification does not
silently impose a new qualified-key format.

A persisted holon retains the explicit key stored when that version was
created. Later changes to its effective key rule, rule inputs, or descriptor
lineage do not recompute or mutate that key. Key migration and aliases require
an explicit operation.

## 10. Endpoint Classification

Every relationship endpoint is a holon. Endpoint constraints name holon-type
descriptors, including abstract holon types used as polymorphic anchors.

Every holon is classified through the lineage of its `DescribedBy` target and,
when it participates in `Extends`, through its own lineage as well. This
cumulative rule permits relationships to target abstract categories such as
`TypeDescriptor`, `PropertyType`, `ValueType`, or `RelationshipType` without
using their describing meta-types as endpoint categories.

The descriptor-kernel semantic rules define the uniform endpoint-compatibility
algorithm.

## 11. Abstract Descriptors

An abstract descriptor may:

- participate in `Extends`;
- provide inherited instance-contract declarations;
- serve as a polymorphic relationship endpoint constraint; and
- participate in type queries and subtype classification.

An abstract descriptor may not directly describe a concrete runtime holon.

Every concrete meta-type inherits the effective instance contract of
`MetaTypeDescriptor.HolonType`. That graph-derived contract is the universal
descriptor baseline. Abstract descriptors must satisfy its positive minimums,
including the universal `DescribedBy` and `ComponentOf` relationships.

An abstract descriptor need not fabricate category-specific descriptor state
solely to satisfy a positive minimum introduced by a category-specific meta-type below
that baseline. For example, abstract `PropertyType` need not select a concrete
`ValueType`. This member-specific completeness exemption applies only to
absence. Any member the descriptor populates remains subject to declaration
identity, value and endpoint constraints, maximum cardinality, and all other
applicable rules.

Abstract descriptors remain subject to universal structural invariants,
including explicit `DescribedBy`, schema membership, and optional-single-parent
acyclic `Extends`.

## 12. Inheritance Declarations

Schema 2.0 uses one descriptor-defined inheritance mechanism for populated properties and
relationships. Every member's effective values are resolved according to its materialized
`InheritanceMode`. The semantic role of a member affects how its effective values are interpreted,
not how they propagate across `Extends`.

### 12.1 Contract-declaration members

`InstanceProperties` and `InstanceRelationships` participate in inheritance
through the same descriptor-defined `InheritanceMode` mechanism as other
populated descriptor relationships. The Core Schema declares `Additive` for
both, causing inherited and local contract declarations to accumulate. The
descriptor kernel does not hard-code a separate contract-inheritance mode.

A subtype may add contract members but does not alter inherited declarations.

### 12.2 Other populated descriptor members

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
dependencies are directed from the dependent schema version to the exact
schema version it consumes. The `DependsOn` graph is acyclic: a schema must not
depend on itself, and no dependency path may return to its starting schema.
This permits schema versions to be released and bound in dependency order
without requiring every member of a mutually dependent group to be versioned
as one unit.

For descriptor components `A` and `B` owned respectively by distinct schemas
`S` and `T`, every authored reference from `A` to `B` requires a direct
`S DependsOn T` declaration. Transitive reachability of `T` through another
dependency does not replace that declaration. The direct edge records the
versioned contract actually consumed by `S`; reference resolution operates
over the resulting transitive dependency closure.

Multiple TDL files may contribute components to the same schema holon. Forward
and circular references among those components are within-schema references,
not schema-dependency cycles. The loader may resolve them together using
multiple passes without weakening the acyclic `DependsOn` invariant.

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
11. `InstanceProperties` and `InstanceRelationships` declare `InheritanceMode
    Additive`; inherited contract members therefore accumulate and cannot be
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
    every concrete inverse identifies its declared relationship. Their
    effective endpoints mirror each other; their directional cardinalities
    need not match.
22. Abstract descriptors cannot directly describe concrete runtime holons but
    may serve as inheritance and endpoint anchors.
23. Descriptor category and typed-wrapper admissibility are determined by
    resolved descriptor identity and transitive `Extends`. Any exposed
    `TypeKind` value is derived from that classification and is never authored
    or persisted as independent descriptor state.
24. A property's or relationship's populated values inherit only according to
    the effective `InheritanceMode` in that member descriptor's
    `EffectiveMemberDefinition`.
25. Exact schema declarations and identities come from the authoritative TDL
    corpus rather than generated JSON, loader DTOs, or Rust type definitions.
26. Property and relationship member names are exact local `TypeName` values
    in separate namespaces; each populated name must bind to one descriptor
    identity before semantic occurrence grouping unless it is explicitly
    accepted as an undeclared addition by the applicable openness policy.
27. Declared-member occurrence grouping and cardinality use resolved
    member-descriptor identity, not name equality. Permitted undeclared
    additions remain unbound and are grouped by exact stored name within their
    separate property or relationship namespace.
28. Keys are unique within the bound schema package and dependency closure;
    cross-schema qualification remains part of the WIP Extension Schema design.
29. A persisted holon key is not retroactively recomputed when a later schema
    version changes its key rule, key inputs, or descriptor ancestry.
30. The only `DescribedBy` cycle is the explicitly authored self-loop at
    `MetaHolonType.MetaTypeDescriptor`; every other `DescribedBy` chain reaches
    that root without repeating an identity.
31. Effective-product computation is separate from conformance validation and
    is memoized by product kind and resolved descriptor identity within one
    immutable graph snapshot.
32. `MetaHolonType.MetaTypeDescriptor` conforms to its own effective instance
    contract; changes to that contract must leave the reflective root valid.
33. The versioned schema `DependsOn` graph is a DAG; self-dependencies and
    multi-schema dependency cycles are invalid.
34. Every authored reference from a descriptor component in one schema to a
    descriptor component in another is covered by a direct `DependsOn` edge
    from the source schema to the target schema.

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
