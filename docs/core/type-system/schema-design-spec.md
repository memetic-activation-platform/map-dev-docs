# MAP Schema Design Spec (v2.0.1)

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
  own representation-neutral definitions, rule IDs, and algorithms for descriptor classification,
  effective specifications, instance contracts, semantic inheritance, key-rule resolution,
  cardinality evaluation, and conformance;
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

A **type descriptor** is a holon that defines semantics for instances. It has
two distinct structural roles:

1. As a holon, it must conform to the effective specification of its own describing type.
2. As a type, its own lineage determines the effective specification imposed on the instances it
   describes.

These roles are connected but never flattened into one surface.

For example:

```text
Book.HolonType
  DescribedBy MetaHolonType.MetaTypeDescriptor
  Extends HolonType.TypeDescriptor
```

`L(D(Book.HolonType))` determines the effective specification that the descriptor holon must
conform to. `L(Book.HolonType)` classifies it as a holon type and determines the effective
specification it imposes on books.

## 4. Three Independent Relationships

Schema 2.0 separates conformance, specialization, and instance discovery.

### 4.1 `DescribedBy`

```text
H --DescribedBy--> T
```

`DescribedBy` identifies the type whose effective specification governs `H`.
Every semantically valid holon has exactly one `DescribedBy` target.

The target must be:

- concrete; and
- compatible with the role of `H` under the graph-defined describing-category rules.

Ordinary holons and descriptor holons use the same relationship. Descriptor
holons are described by compatible meta-types; ordinary holons are described by compatible holon
types. Exact compatibility is defined by the descriptor-kernel semantic rules.

### 4.2 `Extends`

```text
T --Extends--> P
```

`Extends` establishes optional single-parent type specialization. It serves two structural
purposes:

- subtype classification and substitutability;
- the lineage over which effective descriptor semantics are resolved.

`Extends` does not itself prescribe additive contract inheritance or copy
populated descriptor state. The descriptor kernel's canonical
`InheritanceRules` table selects each member's policy: `InstanceProperties`,
`InstanceRelationships`, the affordances, `ValidationBindings`, and `Constraints` are
`Additive`; `InstanceKeyRule` is `Override`; every other member is `Local`.
Contract declarations and behavioral affordances therefore accumulate without
requiring authored inheritance-policy state.

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

The **instance contract** is the property-and-relationship portion of a type's effective
specification. A type declares it through:

- `InstanceProperties`, targeting property descriptors; and
- `InstanceRelationships`, targeting declared relationship descriptors.

These are ordinary populated descriptor relationships interpreted as contract declarations. They
do not represent property values or relationship occurrences populated on every described
instance.

The local declarations of a type form its local instance contract. The
effective declarations reached through `InstanceProperties` and
`InstanceRelationships` are resolved under the kernel's `Additive` rule. A
subtype's effective instance contract therefore contains inherited and local
declarations. A subtype may add members but may not remove or redeclare an
inherited member. The term **shadow** is reserved for contributions excluded by
the kernel's `Override` rule.

Contract-member identity is the identity of the referenced descriptor:

- the referenced `PropertyType` for a property member; or
- the referenced declared relationship descriptor for a relationship member.

A subtype must not redeclare an inherited contract member to alter its value
type, endpoint type declarations, cardinality, requiredness, or validation rules.
Schema 2.0 deliberately defers subtype refinement of inherited members; adding such support would
require explicit variance and compatibility rules.
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

Every type descriptor sits at the nexus of two axes:

- **type as holon: `L(D(T))`** determines the effective specification to which descriptor holon
  `T` must conform; and
- **type as classifier: `L(T)`** determines the effective specification that `T` imposes on the
  instances it describes.

The axes meet through `DescribedBy`, but they are never flattened. Extending `PropertyType` does
not make a descriptor conform to `MetaPropertyType`; selecting `MetaPropertyType` through
`DescribedBy` does not place meta-type declarations in the instance contract of ordinary property
occurrences.

### 7.1 Meta-types

Meta-types answer: **what must this type definition look like?** They are concrete holon-type
descriptors whose effective specifications govern descriptor holons.

For example:

- `MetaPropertyType.MetaTypeDescriptor` describes property descriptor holons;
- `MetaDeclaredRelationshipType.MetaRelationshipType` describes declared relationship descriptor
  holons; and
- `MetaDanceType.MetaHolonType` describes dance-type descriptor holons.

Meta-types are themselves descriptor holons. Their nearest Instance TypeKind anchor is normally
`HolonType.TypeDescriptor`, because every type descriptor is structurally a holon. Being a
meta-type does not create a separate runtime representation kind.

### 7.2 Instance TypeKind anchors

An Instance TypeKind anchor answers: **what kind of instances does this type define?** The common
descriptor contract declares the required Boolean property
`DefinesInstanceTypeKind`, with default `false` and the kernel's `Local` rule.

A local completed value of `true` designates that descriptor as an anchor. The Instance TypeKind
of descriptor `T` is the nearest designated anchor in the self-first lineage `L(T)`. The anchor is
a descriptor identity, not an enum value or name-derived category.

Anchors must be abstract: they classify representation families and may be extended, but do not
directly describe runtime instances. A more specific anchor may extend another anchor. Thus
`DanceType.HolonType` defines Dance as a specialized kind while remaining a subtype of
`HolonType.TypeDescriptor`; Dance instances are specialized holons rather than a different
fundamental storage representation.

`TypeDescriptor` is the sole descriptor root without an Instance TypeKind. Every other descriptor
must resolve one nearest anchor. The current Core Schema corpus designates the anchors shown in the
root diagram, including Holon, Value, Property, Relationship, DeclaredRelationship,
InverseRelationship, Dance, DanceResponse, Command, and Operator. The corpus owns the exact list.

### 7.3 Meta-type pairing

The two axes cannot vary independently. A descriptor's nearest Instance TypeKind anchor determines
the meta-type category that may describe it by following the anchor's own `DescribedBy`
relationship. A property descriptor therefore requires a describing type equal to or extending
the meta-type that describes `PropertyType.TypeDescriptor`; a Dance descriptor similarly requires
the meta-type paired with `DanceType.HolonType`.

This graph-defined pairing lets extension schemas introduce a new Instance TypeKind and its
meta-type without adding a category to kernel code. `TypeDescriptor` is the one root exception: it
has no Instance TypeKind and is described by `MetaHolonType.MetaTypeDescriptor`. Ordinary holons
are required to be described by `HolonType.TypeDescriptor` or one of its subtypes.

The descriptor-kernel semantic rules define `InstanceTypeKind`,
`RequiredDescribingCategory`, and the exact compatibility predicates and validation rules.

### 7.4 Self-description

A descriptor may be self-describing when it satisfies the same describing-type compatibility and
conformance rules as every other descriptor. Core Schema 2.0 authors
`MetaHolonType.MetaTypeDescriptor` as self-describing:

```text
MetaHolonType.MetaTypeDescriptor
  DescribedBy MetaHolonType.MetaTypeDescriptor
```

No semantic rule follows `DescribedBy` transitively, requires all describing chains to converge on
that descriptor, or reserves self-description to one identity. Evaluation remains finite because
effective products are computed before conformance selects them. A self-describing descriptor
must still conform to its own effective specification.

### 7.5 Runtime projections

Legacy `TypeKind` and `InstanceTypeKind` values are not authored descriptor state. A runtime API may
expose a derived projection of the resolved Instance TypeKind anchor, but that projection is not an
independent classification fact and does not participate in conformance. Typed wrapper
admissibility continues to use descriptor identity and transitive `Extends` against the wrapper's
category anchor.

## 8. Descriptor Declaration Surfaces

The meta-type contracts define which structural members each descriptor
category carries. The TDL corpus owns the exact member inventory; this section
defines the role of each surface.

The entries below describe semantic fields, not a requirement that consumers
read locally populated state directly. Relationship-member values resolve
across a descriptor's own `Extends` lineage under the kernel-selected
`InheritanceRule`. The resulting `EffectiveMemberDefinition` is the
authoritative view consumed by conformance, default materialization,
cardinality, endpoint validation, collection policy, and key-rule selection.

Property-member inheritance requires a corresponding kernel rule table and is
not yet specified. Implementations must not infer that property members are
local, additive, or override-only merely because their relationship-member
counterparts have a rule.

### 8.1 Common type-descriptor surface

Every type descriptor carries common identity and descriptive metadata and is
a component of one schema. The common structural surface includes:

- type identity and display metadata;
- `IsAbstractType`;
- `DefinesInstanceTypeKind`;
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
- an optional `DefaultValue`.

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
- constraints applicable to the value descriptor family.

An enum variant's required local `TypeName` is its canonical stored enum token. Variant keys resolve
descriptor identity and display names support presentation; neither substitutes for the token.
Tokens are exact, case-sensitive `MapString` values and must be unique within an effective enum
definition. Renaming a variant's local `TypeName` is therefore a value-affecting schema change and
does not rewrite persisted values.

Value-constraint declarations and their evaluation are delegated to the
[value constraints design](value-constraints-design-spec.md)
and the descriptor-kernel semantic rules.

### 8.5 Relationship descriptors

Every concrete relationship descriptor defines a direction with:

- exactly one source-type declaration;
- exactly one target-type declaration;
- ordering policy;
- duplicate policy;
- definitional status;
- directional deletion semantics.

Directional cardinality is a configured `CardinalityConstraint` attached through the generic
`Constraints` relationship. Its minimum is required and its maximum is optional; an absent maximum
means unbounded, and no finite integer is reserved as an unbounded sentinel.

Declared relationships and inverse relationships are separate descriptor holons. Every declared
relationship has one authoritative inverse, and every inverse identifies its declared relationship.
Source and target constraints and deletion semantics are directional descriptor members; cardinality
is a directional constraint contribution. Inverse-direction behavior is explicit rather than
inferred by swapping or copying the declared direction.

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

The relationship has cardinality `1..1`; the kernel assigns it the `Override`
inheritance rule.
Consequently, every type descriptor whose resolved Instance TypeKind is
`HolonType.TypeDescriptor` or one of its specializations has exactly one effective instance key
rule, supplied locally or by its nearest contributing ancestor. This includes abstract holon-type
anchors; `HolonType.TypeDescriptor` supplies the explicit keyless baseline.

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
- enum-variant keys;
- relationship descriptor keys;
- extended-type descriptor keys;
- described-type-qualified keys;
- configured constraint-instance keys;
- configured format keys; and
- explicit keylessness.

The TDL corpus owns the exact key-rule inventory and identities. Target
strategies include `TypeNameRule.KeyRuleType`,
`SchemaNameRule.KeyRuleType`,
`EnumVariantRule.KeyRuleType`, `RelationshipRule.KeyRuleType`,
`ExtendedTypeRule.KeyRuleType`, `DescribedTypeRule.KeyRuleType`,
`ConstraintInstanceRule.KeyRuleType`, `FormatRule.KeyRuleType`, and
`NoneRule.KeyRuleType`.

`TypeKindRule.KeyRuleType` and its authored `TypeKind` input are retired from the Schema 2.0
corpus. A future key rule may deliberately consume a graph-derived Instance TypeKind identity, but
it must define that input and its key-stability consequences independently.

Configured format rules are ordinary holons. Their effective specification includes a
template string and an ordered `TemplateParameters` relationship to the
property descriptors whose values supply the template parameters.

### 9.5 Constraint-instance keys

`Constraint.HolonType` selects `ConstraintInstanceRule.KeyRuleType` as the
inherited `InstanceKeyRule` for configured constraint holons. The rule derives
the key of a constraint instance `C` from exactly two inputs:

```text
ConstraintKey(C) = ConstraintName(C) + "." + LocalTypeName(D(C))
```

`D(C)` is the constraint instance's direct `DescribedBy` target. It must be a
concrete descendant of `ConstraintType.HolonType`; `LocalTypeName(D(C))` is
that descriptor's own `TypeName`, not an ancestor name or a transitive
`DescribedBy` result. `ConstraintName(C)` is the required local string property
on `C` and must be a valid unqualified semantic-key component. Thus a constraint
named `ExactlyOne`, described by `CardinalityConstraint.ConstraintType`, has
the key `ExactlyOne.CardinalityConstraint`.

The rule rejects a missing, duplicate, or invalid `ConstraintName`, a missing
or incompatible direct describing type, and an authored key that differs from
the derived key. Equal names under different concrete constraint types remain
distinct; duplicate derived keys remain ordinary semantic-key collisions.

`ConstraintInstanceRule` is a fixed structural key resolver. It does not
evaluate a constraint, dispatch a validator, create a constraint identity, or
traverse a type's `Constraints` relationship. TDL authors both the instance key
and `ConstraintName`; lowering supplies the ordinary direct `DescribedBy` fact
from the instance's `type` clause and the loader/runtime verifies the result.
The descriptor runtime must register this resolver before a strict Core
bootstrap can validate constraint instances.

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

Every relationship endpoint is a holon. Endpoint type declarations name type
descriptors, including abstract holon types used as polymorphic anchors.

An endpoint is tested through the lineage of its direct `DescribedBy` target.
The required type is admissible when that describing type is substitutable for
it. A descriptor holon follows the same rule: a relationship that intends to
admit property-descriptor holons, for example, constrains the endpoint through
the appropriate describing meta-type rather than through
`PropertyType.TypeDescriptor`.

The descriptor-kernel semantic rules define `TypeSubstitutable` and the
uniform endpoint-compatibility algorithm.

## 11. Abstract Descriptors

An abstract descriptor may:

- participate in `Extends`;
- provide inherited instance-contract declarations;
- serve as a polymorphic endpoint type when they may directly describe an
  endpoint holon; and
- participate in type queries and subtype classification.

An abstract descriptor may not directly describe a concrete runtime holon.

Abstractness does not create a blanket conformance exemption. Minimum enforcement is
member-specific: universally required members remain required, while a member explicitly defined
as concrete-only may relax its minimum for an abstract descriptor. For example, abstract
`PropertyType` need not select a concrete `ValueType` when that minimum applies only to concrete
property descriptors.

Any member an abstract descriptor supplies remains subject to the same binding, value, endpoint,
collection, maximum-cardinality, and constraint rules as a concrete descriptor. The descriptor
kernel owns the completeness policy and exact `DS-CONFORM-002` rule.

Abstract descriptors remain subject to universal structural invariants,
including explicit `DescribedBy`, schema membership, and optional-single-parent
acyclic `Extends`.

## 12. Kernel Inheritance Rules

Schema 2.1 uses one kernel-defined inheritance mechanism for populated
relationship members. Every relationship's effective values are resolved
according to the kernel-selected `InheritanceRule`; inheritance is not authored
descriptor state. The semantic role of a relationship determines the canonical
table entry that applies, not an author-supplied propagation mode.

Property-member inheritance is intentionally deferred until its corresponding
kernel rule table is specified. It is not defined by the relationship table's
local fallback.

### 12.1 Contract-declaration members

`InstanceProperties` and `InstanceRelationships` participate in inheritance
through the same kernel-defined mechanism as other populated descriptor
relationships. The `InheritanceRules` table assigns `Additive` to both,
causing inherited and local contract declarations to accumulate.

A subtype may add contract members but does not alter inherited declarations.

### 12.2 Other populated descriptor relationship members

Every applicable relationship member descriptor resolves an effective
inheritance rule that controls whether values populated through that member
participate in effective descriptor semantics across `Extends`.

The kernel defines three rules:

- `Local`: populated values remain local;
- `Additive`: inherited and local contributions accumulate; and
- `Override`: inspect the descriptor and then each parent in self-first order.
  The first locally populated target set wins and terminates the lookup; an
  unpopulated local member continues the search toward the root. `Override`
  does not imply an implicit clear of inherited values.

The `InheritanceRules` table assigns `Additive` to `InstanceProperties`,
`InstanceRelationships`, `AffordsCommand`, `AffordsDance`, `AffordsOperator`,
`ValidationBindings`, and `Constraints`; it assigns `Override` to
`InstanceKeyRule`; all other relationship members are `Local`. Inheritance does
not copy effective values into local descriptor state. Property-member rules
are deferred and must be added explicitly rather than inferred from this
fallback.

`ValidationBindings` is licensed once through `MetaTypeDescriptor`'s inherited
`InstanceRelationships` contract. Its Core relationship pair is
`TypeDescriptor -[ValidationBindings 0..*]-> ValidationRule` with
`ValidationRule -[ValidationBindingFor 0..*]-> TypeDescriptor` as inverse. Concrete governed
descriptors may author forward occurrences; generic `TypeDescriptor` does not author a universal
binding occurrence.

### 12.3 Definitional constraints and validation commitments

`Constraints` and `ValidationBindings` are distinct additive declarative relationships on a type
definition:

```text
TypeDescriptor -[Constraints 0..*]-> Constraint
TypeDescriptor -[ValidationBindings 0..*]-> ValidationRule
```

A **constraint** is a configured, persistent invariant that participates in the definition of the
type to which it is attached. Its concrete `ConstraintType` defines the invariant's parameter
shape and semantic interpretation; the constraint holon carries the configuration for one type
definition. A constraint is an ordinary holon and is itself governed by the effective
specification of its `DescribedBy` type.

`ValidationBindings` names Commit obligations that are not represented by a configured
definitional constraint. It does not store a second copy of a constraint's parameters. The
[Validation Extension Schema Design Specification](../validation/validation-schema-design-spec.md)
owns `ValidationRule` identity, metadata, and execution-facing vocabulary.

The initial classification boundary is:

| Validation concern | Representation |
| --- | --- |
| Length, numeric-bound, value-array count, uniqueness, and other configured accepted-value invariants | `Constraint` holons attached through `Constraints` |
| Directional relationship cardinality | Configured `CardinalityConstraint` holons; `DS-CARD-001` remains the evaluation and diagnostic identity |
| Required-property presence, endpoint declarations, duplicate policy, ordering policy, definitional status, and deletion semantics | Descriptor structure evaluated by fixed validation rules or kernel semantics; not constraint holons in this design |
| `DS-STRUCT-*`, `DS-SCHEMA-*`, `DS-KIND-*`, `DS-CONTRACT-*`, `DS-BIND-*`, `DS-DEFAULT-*`, and `DS-KEY-*` | Fixed descriptor-kernel rules, optionally retaining stable `ValidationRule` identities for diagnostics and dispatch |
| PVL native representation, resource, lifecycle, and Integrity checks | Fixed descriptor-independent PVL rules |
| Transaction, agreement, Runtime Recognition, TrustChannel, and social checks | Contextual validation outside the generic definitional-constraint model |

This classification does not require every fixed rule to become a persisted `ValidationRule`
holon. It prevents a configured invariant from being split between descriptor properties and a
separate rule parameter model.

`Constraints` is licensed once through `MetaTypeDescriptor`'s inherited
`InstanceRelationships` contract. Its Core relationship pair is
`TypeDescriptor -[Constraints 0..*]-> Constraint` with
`Constraint -[Constrains 0..*]-> TypeDescriptor` as inverse. Concrete governed descriptors may
author forward occurrences; generic `TypeDescriptor` does not author a universal constraint
occurrence.

`ConstraintType` declares the descriptor families to which it may be attached:

```text
ConstraintType -[ApplicableToDescriptorTypes 1..*]-> TypeDescriptor
```

An occurrence is well formed only when the constrained descriptor is, or extends, one of the
applicability targets declared by the constraint's concrete describing type. Applicability
establishes where a constraint can be declared; it does not claim that the invariant can execute
without the bounded context required by its semantics. No inverse relationship is required: the
forward declaration is the authoritative applicability commitment.

Effective constraints resolve through the kernel's existing `Additive` rule. A subtype retains
inherited contributions and may add a compatible constraint only when the resulting effective
definition preserves the inherited obligations. A subtype cannot remove, replace, or relax an
inherited constraint.

The Core schema owns the generic constraint vocabulary, the generic relationship pairs, and every
constraint type used to define Core types. An extension may define a constraint type and attach it
to an extension-owned type or subtype under the ordinary direct-dependency and acyclicity rules.
It does not alter a Core type's authored commitments.

Constraint configuration and attachment conformance bottom out in ordinary typed-holon
conformance plus fixed descriptor-kernel semantics. The model introduces no dynamic recursive
validator resolution and no dependency from PVL on descriptors or constraints.

The descriptor-kernel semantic rules own effective-value resolution, duplicate
elimination, provenance, cardinality evaluation, and error behavior.

### 12.4 Core constraint meta-model and initial vocabulary

The preceding relationships are not merely an extension point. Core defines the following
first-class schema model, which is the required representation for every configured
definitional invariant:

```text
Constraint instance
  -[DescribedBy 1]-> concrete ConstraintType

Applicable type descriptor
  -[Constraints 0..*]-> Constraint instance

concrete ConstraintType
  -[ApplicableToDescriptorTypes 1..*]-> TypeDescriptor
  -[InstanceProperties 0..*]-> configuration PropertyType
```

`Constraint` is an ordinary holon family. `ConstraintType` is the abstract descriptor family
whose concrete descendants describe constraint instances. The effective `InstanceProperties` and
`InstanceRelationships` of a concrete `ConstraintType` are the complete configuration contract
of its instances; a constraint's configuration is never split onto the descriptor it constrains
or onto a `ValidationRule` binding. `MetaConstraintType` is the Core meta-type that governs the
declaration of those concrete constraint types, including their applicability declarations.

Concrete value constraints are direct descendants of `ConstraintType.HolonType`.
`LengthConstraint.ConstraintType`, for example, owns its property contract and
static semantics without extending a legacy string-specific constraint family.
It is the `DescribedBy` target of a separately authored constraint instance
such as `DisplayName.LengthConstraint`.

Concrete constraints declare their actual descriptor-family targets: length for
`StringValueType.ValueType`, numeric range for `IntegerValueType.ValueType`,
and item-count/uniqueness for `ValueArrayValueType.ValueType`. A deliberately
broad constraint may target `ValueType.TypeDescriptor`. Applicability uses
ordinary `Extends` lineage, not a second value-representation compatibility
check or capability taxonomy.

Core's initial concrete configured constraint vocabulary is deliberately small:

| Concrete `ConstraintType` | Constrained descriptor family | Configuration contract | Evaluation identity |
| --- | --- | --- | --- |
| `LengthConstraint.ConstraintType` | String value type | `Minimum`, `Maximum`, `MinimumIsInclusive`, `MaximumIsInclusive` | value-length constraint semantics |
| `NumericRangeConstraint.ConstraintType` | Integer value type | `Minimum`, `Maximum`, `MinimumIsInclusive`, `MaximumIsInclusive` | numeric-range constraint semantics |
| `ItemCountConstraint.ConstraintType` | Value-array type | `Minimum`, `Maximum`, `MinimumIsInclusive`, `MaximumIsInclusive` | item-count constraint semantics |
| `UniqueItemsConstraint.ConstraintType` | Value-array type | no configuration member; its attached presence is affirmative | value-array uniqueness semantics |
| `CardinalityConstraint.ConstraintType` | Declared or inverse relationship descriptor | inclusive `Minimum` and optional inclusive `Maximum` | `DS-CARD-001` |

For every bounded type in the first three rows, the two bounds are optional independently, at
least one is required, and an inclusivity field is required exactly when its associated bound is
present. The constraint type's property contract and `DS-CONSTRAINT-003` enforce those facts.
There are no Core `MinimumLength`, `MaximumLength`, `MinimumValue`, `MaximumValue`,
`MinimumItems`, or `MaximumItems` constraint types in the target model.

The static validator selected for a concrete `ConstraintType` interprets the configuration carried
by that instance. This is an implementation association owned by Core's descriptor-aware runtime,
not an authored `ConstraintType -[ValidationBindings]-> ValidationRule` relation and not dynamic
code loading. `ValidationRule` remains available for fixed and contextual obligations that are not
configured definitional constraints.

The normal authoring unit is consequently a named instance plus its explicit attachment. For
example:

```text
DisplayName.StringValueType
  -[Constraints]-> DisplayName.LengthConstraint

DisplayName.LengthConstraint
  -[DescribedBy]-> LengthConstraint.ConstraintType
  Minimum = 1
  MinimumIsInclusive = true
  Maximum = 120
  MaximumIsInclusive = true
```

The source-language spelling may vary only where the TDL specification explicitly provides
syntax. It must always lower into this same authored constraint holon and explicit `Constraints`
occurrence; it must not synthesize an identity, ownership fact, or attachment from properties on
the constrained descriptor.

## 13. Required Properties and Defaults

`DefaultValue` is part of the property-descriptor structure. A default is valid
only when `IsValueRequired` is true.

The valid structural combinations are:

| Required | Default | Meaning                                |
|----------|---------|----------------------------------------|
| No       | Absent  | Omission represents absence            |
| Yes      | Absent  | Creation must supply a value           |
| Yes      | Present | A path accepting omission materializes the default before validation |

An optional property with a default is invalid because omission would be
ambiguous between absence and default application.

Defaults are creation-time completion declarations, not read-time fallback state. A creation path
that accepts omission as selection of a default must materialize that value before
descriptor-kernel validation; an interactive path may instead require confirmation or an explicit
value. Automatic completion is a reusable writable-holon capability: the loader invokes it over
its staged import set, and another creation path may invoke it after attaching `DescribedBy`.
The kernel validates the resulting explicit representation but does not inject defaults or
otherwise mutate it.

Once materialized, a default is ordinary explicit state. Changing a descriptor
default does not implicitly change previously created holons.

The semantic default and conformance rules are defined by the descriptor-kernel semantic rules.
Loader orchestration and TDL omission behavior belong to their delegated documents.

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

A valid Schema 2.0 graph has the following structural shape. The descriptor-kernel rule index owns
the exact independently testable validations and error behavior.

1. Every holon has exactly one `DescribedBy` target.
2. Every direct describing type is concrete and compatible with the holon's graph-defined role.
3. Every holon has at most one direct `Extends` parent.
4. Every descriptor lineage is acyclic and terminates at the unique descriptor root,
   `TypeDescriptor`.
5. `MetaTypeDescriptor.HolonType` extends `HolonType.TypeDescriptor` and roots the meta-type branch.
6. `RelationshipType.TypeDescriptor` roots the declared and inverse relationship categories.
7. `IsDescriptor(H)` follows from `TypeDescriptor` membership in `L(H)`; no authored descriptor flag
   or declaration form determines it.
8. `DefinesInstanceTypeKind` is a local, required Boolean descriptor property with default `false`
   and the kernel's `Local` inheritance rule.
9. Every Instance TypeKind anchor is abstract. `TypeDescriptor` defines no Instance TypeKind; every
   other descriptor resolves one nearest anchor in its lineage.
10. A descriptor's describing meta-type is compatible with the category paired to its nearest
    Instance TypeKind anchor. Ordinary holons are described by compatible descendants of
    `HolonType.TypeDescriptor`.
11. Self-description is valid only when the ordinary describing-type compatibility and conformance
    rules hold. `DescribedBy` has no transitive-closure semantic.
12. `InstanceProperties` target property descriptors and `InstanceRelationships` target declared
    relationship descriptors.
13. The kernel inheritance table assigns `Additive` to `InstanceProperties`,
    `InstanceRelationships`, `AffordsCommand`, `AffordsDance`,
    `AffordsOperator`, `ValidationBindings`, and `Constraints`.
14. The Core `InstanceKeyRule` relationship descriptor declares cardinality `1..1`; the kernel
    inheritance table assigns it `Override`.
15. Every descriptor belongs to exactly one schema through `ComponentOf`.
16. Every holon type resolves exactly one effective `InstanceKeyRule`; keylessness uses the explicit
    `NoneRule.KeyRuleType` target.
17. Every concrete property descriptor selects exactly one compatible value type, and a default may
    be declared only for a required property.
18. Every concrete relationship descriptor defines one source, one target, collection policy, and
    directional deletion semantic; its effective constraints include applicable directional
    cardinality constraints.
19. Every declared relationship and inverse relationship are bijectively paired and have mirrored
    effective endpoints; directional cardinalities may differ.
20. Property and relationship member names derive from required local `TypeName` values, occupy
    separate namespaces, and bind to resolved descriptor identities before conformance.
21. A persisted key and a materialized default are explicit historical state; later schema changes
    do not retroactively recompute them.
22. The versioned schema `DependsOn` graph is a DAG, and every direct cross-schema descriptor
    reference is covered by a direct dependency edge.
23. Exact identities, member inventories, values, and anchor designations come from the authoritative
    TDL corpus rather than generated JSON, runtime DTOs, or local names repeated in this spec.

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
