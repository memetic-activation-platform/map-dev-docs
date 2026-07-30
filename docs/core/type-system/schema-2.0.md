# Type-Descriptor and Meta-Type Design (v2.0)

## 1. Problems in the Current Design

### 1.1 `InstanceProperties` and `InstanceRelationships` are not defined precisely enough

The existing terms are appropriate, but their meaning has remained partly implicit.

An `InstanceProperty` or `InstanceRelationship` is not necessarily populated by the type descriptor that declares it. Instead, it is part of the contract that the type imposes on the instances it describes.

Because `Instances` is the inverse of `DescribedBy`:

    T ──Instances──> H

means:

> `H` must conform to the effective instance contract of `T`.

The normative relationship is:

    H ──DescribedBy──> T

The semantics do not depend on the inverse `Instances` relationship having been physically materialized.

The distinction is important:

- declarations on `T` define what its described instances must contain;
- populated values on `T` describe `T` itself.

These are different semantic layers.

### 1.2 `Extends` has been conflated with inheritance of populated values

The primary role of `Extends` is to establish subtype classification and inherit instance-contract declarations.

If a type descriptor populates relationships such as:

    ComponentOf
    UsesKeyRule
    SourceType
    TargetType

those relationship targets do not, by default, become effective values of a type that extends it.

`Extends` therefore provides additive inheritance of instance-contract declarations, not general inheritance of descriptor state.

A limited exception is needed for properties and relationships whose definitions explicitly declare semantic inheritance. For those members, effective values are resolved across the `Extends` hierarchy without being copied into the subtype's local state.

### 1.3 Generic describing types do not impose kind-specific obligations

A generic meta-type can impose obligations common to type descriptors, but it cannot by itself impose the additional obligations of a specific descriptor kind.

For example, suppose `MetaHolonType` declares `UsesKeyRule` as an instance relationship. Every holon-type descriptor must then conform to a contract that includes `UsesKeyRule`.

Merely extending `HolonType` does not impose that obligation on the extending descriptor. It causes the extending descriptor to inherit the instance contract that `HolonType` passes on to the instances it describes.

The descriptor's own conformance obligations must instead come from its `DescribedBy` relationship.

### 1.4 The current structure conflates two independent hierarchies

The design needs to distinguish:

1. the meta-type hierarchy, which defines contracts for type-descriptor holons; and
2. the descriptor-type hierarchy, which defines contracts for described instances and establishes subtype classification.

The hierarchies are connected by `DescribedBy`, but remain distinct.

Using one inheritance path for both purposes would allow meta-level declarations to leak into ordinary instance contracts.

### 1.5 Descriptor defaults and TDL omission have been conflated

A property omitted from TDL is not necessarily absent from the descriptor created from that TDL.

A required descriptor property may define a default value. In that case:

- the property may be omitted from TDL;
- the default is materialized into the descriptor's property map during creation;
- the resulting descriptor contains the property explicitly; and
- downstream evaluation does not require descriptor context merely to recover the default.

TDL omission is therefore an authoring convenience. It is not runtime absence.

---

## 2. Proposed Design

![MAP Schema Root v2.0.jpg](../../media/MAP%20Schema%20Root%20v2.0.jpg)

### 2.1 Define `InstanceProperties` and `InstanceRelationships` as instance-contract declarations

Retain the established terminology with the following definition:

> The `InstanceProperties` and `InstanceRelationships` declared by a type form the contract that the type imposes on the instances it describes.

Define:

    LocalInstanceContract(T)

as the set of `InstanceProperties` and `InstanceRelationships` declared directly by `T`.

If `T` extends `P`, define:

    EffectiveInstanceContract(T)
        =
    EffectiveInstanceContract(P)
        ∪
    LocalInstanceContract(T)

If `T` does not extend another type:

    EffectiveInstanceContract(T)
        =
    LocalInstanceContract(T)

This inheritance is additive. A subtype may add declarations but does not remove declarations inherited from its parent.

#### Contract-member identity

An instance-contract member is identified by the referenced:

- `PropertyType`, for an instance property; or
- relationship descriptor type, for an instance relationship.

A subtype must not redeclare an inherited contract member in an attempt to modify or override it.

If a local contract declaration has the same contract-member identity as an inherited declaration, contract resolution fails with an inherited-member redeclaration error.

If distinct contract-member identities in the effective instance contract claim the same semantic member name, contract resolution fails with a duplicate semantic-member declaration error.

Contract declarations are not set-deduplicated. This is distinct from set union and duplicate elimination for effective populated values under `InheritanceMode Additive`.

In particular, redeclaration does not override inherited:

- cardinality;
- value type;
- source or target constraints;
- requirement status; or
- validation rules.

Any future mechanism for refining inherited constraints must be defined explicitly.

### 2.2 Separate instance conformance from type specialization

Every typed instance participates in describing-type conformance through `DescribedBy`.

Type descriptors additionally participate in specialization and classification through `Extends`.

#### Describing-type conformance

    H ──DescribedBy──> D

means:

> `H` must conform to the effective instance contract of `D`.

Formally:

    ConformanceContract(H)
        =
    EffectiveInstanceContract(DescribingType(H))

`DescribedBy` determines the schema-defined contract that the current instance must satisfy.

#### Type specialization

    T ──Extends──> P

means:

> The instance contract imposed by `T` includes the effective instance contract imposed by `P`.

Formally:

    EffectiveInstanceContract(T)
        =
    EffectiveInstanceContract(P)
        ∪
    LocalInstanceContract(T)

`Extends` determines what instances described by `T` must populate.

It also establishes subtype classification.

It does not, by default, make populated property values or relationship targets of `P` into local or effective values of `T`.

#### Ordinary instances

An ordinary runtime instance participates in `DescribedBy`, but does not itself participate in the descriptor `Extends` hierarchy.

For example:

    Emerging World
        DescribedBy Book.HolonType

#### Type descriptors

A type descriptor participates in both relationships:

    Book.HolonType
        DescribedBy MetaHolonType
        Extends HolonType

These relationships serve different purposes:

- `DescribedBy MetaHolonType` determines what `Book.HolonType` itself must populate;
- `Extends HolonType` determines its classification and the contract it passes on to the instances it describes.

### 2.3 Establish the meta-type branch

Meta-types define contracts for type-descriptor holons.

The meta-type branch is rooted at `MetaTypeDescriptor`, which extends `HolonType`.
All meta-types therefore classify categories of descriptor holons while remaining holon types in
the unified descriptor hierarchy.

    MetaTypeDescriptor
        Extends HolonType
        root of the meta-type branch
        defines the common contract for type-descriptor holons

    MetaHolonType
        Extends MetaTypeDescriptor
        defines the contract for holon-type descriptors

    MetaPropertyType
        Extends MetaTypeDescriptor
        defines the contract for property-type descriptors

    MetaValueType
        Extends MetaTypeDescriptor
        defines the contract for value-type descriptors

    MetaRelationshipType
        Extends MetaTypeDescriptor
        defines the common contract for relationship-type descriptors

    MetaDeclaredRelationshipType
        Extends MetaRelationshipType
        defines the contract for declared-relationship descriptors

    MetaInverseRelationshipType
        Extends MetaRelationshipType
        defines the contract for inverse-relationship descriptors

Inheritance among meta-types is additive declaration inheritance.

For example:

    EffectiveInstanceContract(MetaHolonType)
        =
    EffectiveInstanceContract(MetaTypeDescriptor)
        ∪
    LocalInstanceContract(MetaHolonType)

If `MetaHolonType` declares `UsesKeyRule`, every holon described by `MetaHolonType` must satisfy that declaration according to its cardinality.

### 2.4 Meta-types are described by `MetaHolonType`

Meta-types are themselves holon-type descriptors. They are therefore described by `MetaHolonType`.

    MetaTypeDescriptor
        DescribedBy MetaHolonType

    MetaHolonType
        DescribedBy MetaHolonType

    MetaPropertyType
        DescribedBy MetaHolonType

    MetaValueType
        DescribedBy MetaHolonType

    MetaRelationshipType
        DescribedBy MetaHolonType

    MetaDeclaredRelationshipType
        DescribedBy MetaHolonType

    MetaInverseRelationshipType
        DescribedBy MetaHolonType

This establishes a deliberate reflective fixed point:

    MetaHolonType
        DescribedBy MetaHolonType

The fixed point avoids introducing an unbounded sequence of meta-meta-types.

It is established by explicit authored `DescribedBy` and `Extends` relationships. No descriptor
name or omitted relationship receives bootstrap-specific interpretation.

One generalized relationship pair serves ordinary and descriptor holons:

    (HolonType)-[DescribedBy]->(TypeDescriptor)
    (TypeDescriptor)-[Instances]->(HolonType)

Concrete descriptor types satisfy the target through their own descriptor classification.
Meta-types also satisfy it because `MetaTypeDescriptor Extends HolonType Extends TypeDescriptor`.
Both therefore participate without a separate `DescriptorInstances` relationship.

### 2.5 Establish the descriptor classification hierarchy

The descriptor-type hierarchy is rooted at abstract `TypeDescriptor`.

It provides:

- a shared classification root for descriptor types in the descriptor-type hierarchy;
- a polymorphic target for relationships;
- a query root for descriptor types; and
- a stable semantic category for schema components.

For example:

    Schema.Components -> TypeDescriptor

allows any descriptor type in the descriptor-type hierarchy to be a schema component.

`MetaTypeDescriptor` is a descendant of `TypeDescriptor` through `HolonType`; it remains the
specific root of the meta-type branch and is not the generic describing type for all descriptor
holons.

### 2.6 Describe each descriptor type by its kind-specific meta-type

The descriptor-type hierarchy is:

    TypeDescriptor
        abstract
        DescribedBy MetaHolonType

    HolonType
        abstract
        Extends TypeDescriptor
        DescribedBy MetaHolonType

    PropertyType
        abstract
        Extends TypeDescriptor
        DescribedBy MetaPropertyType

    ValueType
        abstract
        Extends TypeDescriptor
        DescribedBy MetaValueType

    RelationshipType
        abstract
        Extends TypeDescriptor
        DescribedBy MetaHolonType

    DeclaredRelationshipType
        abstract
        Extends RelationshipType
        DescribedBy MetaDeclaredRelationshipType

    InverseRelationshipType
        abstract
        Extends RelationshipType
        DescribedBy MetaInverseRelationshipType

`RelationshipType` supplies the shared relationship key rule and is the source endpoint category
for:

    (RelationshipType)-[SourceType]->(HolonType)
    (RelationshipType)-[TargetType]->(HolonType)

`TypeDescriptor` is described by `MetaHolonType` because it is itself a holon-type descriptor: it describes descriptor holons within the descriptor classification hierarchy.

Authored descriptors follow the same kind-specific rule.

    Book.HolonType
        Extends HolonType
        DescribedBy MetaHolonType

    TypeName.PropertyType
        Extends PropertyType
        DescribedBy MetaPropertyType

    ComponentOf.DeclaredRelationshipType
        Extends DeclaredRelationshipType
        DescribedBy MetaDeclaredRelationshipType

    Components.InverseRelationshipType
        Extends InverseRelationshipType
        DescribedBy MetaInverseRelationshipType

Therefore, if `MetaHolonType` declares `UsesKeyRule`, both `HolonType` and `Book.HolonType` must satisfy that declaration.

The obligation comes from:

    DescribedBy MetaHolonType

It does not come from extending another holon type.

### 2.7 Keep conformance and semantic classification distinct

Meta-types describe descriptor holons and declare what those descriptor holons must contain.
Abstract descriptor types classify the semantic categories used in descriptor-to-descriptor
relationships.

The meta-type branch remains structurally distinct below `MetaTypeDescriptor`:

    MetaPropertyType
        Extends MetaTypeDescriptor

    MetaDeclaredRelationshipType
        Extends MetaRelationshipType

Descriptor categories extend their semantic classification parents:

    PropertyType
        Extends TypeDescriptor

    DeclaredRelationshipType
        Extends RelationshipType

    TypeName.PropertyType
        Extends PropertyType

Descriptor holons are governed by meta-types through `DescribedBy`:

    PropertyType
        DescribedBy MetaPropertyType

    TypeName.PropertyType
        DescribedBy MetaPropertyType

Meta-type declarations therefore govern descriptor-holon conformance without replacing abstract
descriptor types as semantic relationship endpoint categories.

### 2.8 Require single and acyclic inheritance

Each type may extend at most one parent type.

Formally:

    Cardinality(Extends) = 0..1

The unified `Extends` graph must be acyclic.

Formally:

    NOT (T Extends+ T)

where `Extends+` is the transitive closure of one or more `Extends` relationships.

Single inheritance preserves:

- deterministic ancestry;
- unambiguous contract accumulation;
- deterministic semantic-value resolution;
- straightforward provenance; and
- freedom from multiple-inheritance precedence rules.

### 2.9 Determine descriptor substitutability through transitive `Extends`

A relationship whose target is `TypeDescriptor` accepts a descriptor type when that descriptor is `TypeDescriptor` or transitively extends `TypeDescriptor`.

Define:

    SubtypeOf(actualType, requiredType)
        =
    actualType Extends* requiredType

where `Extends*` is the reflexive transitive closure of `Extends`.

For example:

    Book.HolonType
        Extends HolonType

    HolonType
        Extends TypeDescriptor

therefore:

    Book.HolonType
        Extends* TypeDescriptor

`Book.HolonType` is consequently a valid target of:

    Schema.Components -> TypeDescriptor

The classification path is:

    Book.HolonType
        -> HolonType
        -> TypeDescriptor

Every relationship endpoint is a holon. Define its effective endpoint type as:

    EffectiveEndpointType(H)
        =
    H,                    when H is itself a type descriptor
    DescribingType(H),    otherwise

Endpoint compatibility is uniform:

    EndpointCompatible(H, requiredType)
        =
    EffectiveEndpointType(H) Extends* requiredType

For example, `EffectiveEndpointType(Alice) = Person.HolonType`, while
`EffectiveEndpointType(Description.PropertyType) = Description.PropertyType`.
The latter permits abstract descriptor categories such as `PropertyType`, `ValueType`, and
`RelationshipType` to constrain descriptor-to-descriptor relationships without substituting their
meta-types as semantic endpoints.

For any type `T`, define:

    AdmissibleDescribingType(T)
        =
    SubtypeOf(T, TypeDescriptor)

Every typed holon must be described by a non-abstract admissible describing type.

For every holon `H`:

    AdmissibleDescribingType(DescribingType(H))

and:

    Abstract(DescribingType(H)) = false

All admissible describing types belong to the unified hierarchy rooted at `TypeDescriptor`.
Meta-types are admissible through `MetaTypeDescriptor Extends HolonType Extends TypeDescriptor`.
Admissibility is determined by transitive `Extends`, not by semantic name or descriptor kind.

### 2.10 Distinguish declaration inheritance from semantic inheritance

The design defines two forms of inheritance across `Extends`.

#### Declaration inheritance

Declaration inheritance applies to:

    InstanceProperties
    InstanceRelationships

It determines the effective contract that a type imposes on the instances it describes.

    EffectiveInstanceContract(T)
        =
    EffectiveInstanceContract(ExtendedType(T))
        ∪
    LocalInstanceContract(T)

Declaration inheritance is always additive.

#### Semantic inheritance

Populated values are resolved according to the `InheritanceMode` declared by their `PropertyType` or relationship descriptor:

- `None` retains only locally populated values;
- `Additive` combines inherited and local values by set union; and
- `Override` uses the complete value set supplied by the nearest type in the self-first `Extends` lineage that locally populates the member.

Values resolved through `Additive` or `Override` contribute to the subtype's effective semantics, but they do not become locally populated state on the subtype descriptor.

Populated values remain local when the member declares `InheritanceMode None`.

#### Descriptor-local state

For example:

    HolonType
        ComponentOf CoreSchema

does not imply:

    Book.HolonType
        ComponentOf CoreSchema

`ComponentOf` describes the descriptor holon itself.

Because `ComponentOf.DeclaredRelationshipType` has:

    InheritanceMode None

the target `CoreSchema` remains local to `HolonType`.

#### Inherited type semantics

Suppose `MetaHolonType` includes `AffordsCommands` in the instance contract of holon-type descriptors:

    MetaHolonType
        InstanceRelationships
            AffordsCommands

Suppose the relationship type declares additive inheritance:

    AffordsCommands.DeclaredRelationshipType
        InheritanceMode Additive

Now consider:

    HolonType
        AffordsCommands
            ReadableHolonCommands
            WritableHolonCommands

    Book.HolonType
        Extends HolonType
        AffordsCommands
            BorrowBookCommand

The locally populated commands of `Book.HolonType` are:

    LocalValues(Book.HolonType, AffordsCommands)
        =
    {
        BorrowBookCommand
    }

Its effective commands are:

    EffectiveValues(Book.HolonType, AffordsCommands)
        =
    {
        ReadableHolonCommands,
        WritableHolonCommands,
        BorrowBookCommand
    }

The inherited targets contribute to the meaning of `Book.HolonType`, but they are not stored as local `AffordsCommands` relationships on it.

---
## 3. Semantic Inheritance

### 3.1 Declare semantic inheritance with `InheritanceMode`

`InheritanceMode` is a property of:

- `PropertyType`; and
- relationship descriptor types.

It determines whether values populated through that member are inherited across `Extends`.

The initial value set is:

    enum InheritanceModeValueType {
        variants {
            None
            Additive
            Override
        }
    }

The property type is conceptually:

    property InheritanceMode {
        value InheritanceModeValueType
        required true
        default None
    }

`MetaPropertyType`, `MetaDeclaredRelationshipType`, and `MetaInverseRelationshipType` include `InheritanceMode` in their instance contracts.

    MetaPropertyType
        InstanceProperties
            InheritanceMode

    MetaDeclaredRelationshipType
        InstanceProperties
            InheritanceMode

    MetaInverseRelationshipType
        InstanceProperties
            InheritanceMode

`InheritanceMode` is required, not optional.

Because its default is `None`, it may be omitted from TDL. During descriptor creation, the default is materialized into the descriptor's property map.

After successful creation, every applicable property or relationship descriptor physically contains an `InheritanceMode` value.

Formally:

    InheritanceMode(M)
        =
    M.PropertyMap["InheritanceMode"]

There is no runtime interpretation of absence as `None`.

For any type `T`:

    parent(T)

is the optional unique target of the local `Extends` relationship populated directly on `T`.

Parent resolution does not:

- inherit `Extends`;
- follow `DescribedBy`;
- infer a parent from descriptor kind; or
- search by semantic name.

### 3.2 `None`

`None` means that only locally populated values contribute to the descriptor's effective semantics.

    EffectiveValues(T, M)
        =
    LocalValues(T, M)

Examples include:

    ComponentOf.DeclaredRelationshipType
        InheritanceMode None

    SourceType.DeclaredRelationshipType
        InheritanceMode None

    TargetType.DeclaredRelationshipType
        InheritanceMode None

Because `None` is materialized as the default, these declarations may be omitted from TDL.

### 3.3 `Additive`

`Additive` means that inherited and local values are combined by set union across the `Extends` hierarchy.

If `T` has parent `P`:

    EffectiveValues(T, M)
        =
    EffectiveValues(P, M)
        ∪
    LocalValues(T, M)

If `T` does not have a parent:

    EffectiveValues(T, M)
        =
    LocalValues(T, M)

For example:

    AffordsCommands.DeclaredRelationshipType
        InheritanceMode Additive

Possible uses include:

- validation rules;
- supported commands;
- supported dances;
- supported visualizers; and
- other capabilities associated with instances of a type.

Additive inheritance retains all distinct inherited and local contributions.

It does not imply:

- replacement;
- precedence;
- last-write-wins behavior; or
- removal of inherited values.

### 3.4 `Override`

`Override` means that a locally populated value set replaces the effective value set inherited from the nearest ancestor.

If local values are present:

    EffectiveValues(T, M)
        =
    LocalValues(T, M)

If local values are absent and `T` has parent `P`:

    EffectiveValues(T, M)
        =
    EffectiveValues(P, M)

If local values are absent and `T` has no parent:

    EffectiveValues(T, M)
        =
    empty set

Equivalently:

    EffectiveValues(T, M)
        =
    LocalValues(T, M),                    if LocalValues(T, M) is non-empty

    EffectiveValues(parent(T), M),         otherwise, if parent(T) exists

    empty set,                            otherwise

Resolution is self-first.

The first type in the `Extends` lineage that locally populates the member supplies the effective value set. More distant ancestor contributions are shadowed for effective-value purposes.

The shadowed contributions remain part of provenance but are not members of the subtype's effective value set.

`Override` is appropriate for singular or replacement-oriented semantics in which a subtype may:

- accept the nearest inherited value;
- define a local replacement; or
- ultimately rely on a value defined by the root type.

For example:

    UsesKeyRule.DeclaredRelationshipType
        InheritanceMode Override

A holon type may then:

- define its own local key rule;
- inherit the nearest key rule defined by an ancestor; or
- inherit the baseline key rule defined by the root `HolonType`.

If the root `HolonType` defines:

    UsesKeyRule -> NoneKeyRule

then keyless holon types inherit `NoneKeyRule` unless a nearer subtype selects another rule.

`NoneKeyRule` is an explicit key-rule descriptor representing keylessness. It is not the absence of a key rule.

### 3.5 Cardinality under `Override`

Cardinality is evaluated against the resolved effective value set.

For a member with:

    InheritanceMode Override

a local value set, when present, must independently satisfy applicable local representation constraints.

For a singular member such as:

    UsesKeyRule cardinality 1..1

the following are valid:

- exactly one local value;
- no local value and exactly one inherited effective value.

The following are invalid:

- more than one local value;
- no local or inherited effective value; or
- an inherited effective value set containing more than one value.

A local value replaces the inherited effective value; it is not added to it.

Thus:

    Parent:
        UsesKeyRule -> NoneKeyRule

    Child:
        UsesKeyRule -> TypeNameKeyRule

produces:

    EffectiveValues(Child, UsesKeyRule)
        =
    {
        TypeNameKeyRule
    }

not:

    {
        NoneKeyRule,
        TypeNameKeyRule
    }

### 3.6 No subtraction, masking, or exclusion modes

The initial design includes no:

- subtraction;
- selective masking;
- exclusion;
- inherited-value removal; or
- partial replacement

inheritance modes.

`Override` replaces the entire inherited effective value set for a member when any local value is present.

It does not selectively remove or modify individual inherited contributions.

More granular modes should be introduced only when supported by a concrete use case.

They would require explicit rules for:

- precedence;
- conflict resolution;
- cardinality;
- partial removal;
- interaction with local declarations; and
- provenance.

### 3.7 Ownership of the declaration

Inheritance behavior belongs to the property or relationship descriptor whose populated values are inherited.

It is not declared:

- separately by every type that uses the property or relationship;
- on each populated value or relationship instance; or
- as a hard-coded exception in effective-descriptor resolution.

For example, additive inheritance is part of the meaning of:

    AffordsCommands.DeclaredRelationshipType

Override inheritance is part of the meaning of:

    UsesKeyRule.DeclaredRelationshipType

These modes do not belong separately to:

    HolonType
    Book.HolonType
    Schema.HolonType

### 3.8 Scope

Semantic inheritance applies only when resolving the effective semantics of type descriptors across `Extends`.

It does not create general value inheritance among ordinary domain instances.

The complete rules are:

> When resolving a type descriptor, values populated through a property or relationship whose descriptor has `InheritanceMode Additive` are accumulated across that type descriptor's `Extends` chain by set union.

> When resolving a type descriptor, values populated through a property or relationship whose descriptor has `InheritanceMode Override` are taken from the nearest type in the `Extends` lineage that locally populates that member.

The resulting values are effective values of the subtype. They are not copied into its local descriptor state.

### 3.9 Provenance under semantic inheritance

Both `Additive` and `Override` inheritance preserve contribution provenance.

For `Additive`, provenance records every inherited and local contribution that participates in the effective value set, including duplicate contributions that collapse under set semantics.

For `Override`, provenance records:

- the local or nearest inherited contribution that supplies the effective value set; and
- shadowed contributions from more distant ancestors.

Shadowed values do not contribute to effective cardinality, but their provenance may remain available for explanation, inspection, and debugging.

### 3.10 Property-value inheritance

Relationship targets naturally form sets.

Scalar property maps ordinarily contain at most one locally populated value per property.

For semantic inheritance, a local scalar property value is treated as a singleton contribution set.

#### Additive property inheritance

If an additively inherited scalar property receives distinct contributions from an ancestor and subtype:

    EffectiveValues(T, SomeProperty)
        =
    {
        A,
        B
    }

then its effective value count is two.

The kernel does not interpret this as replacement.

#### Override property inheritance

If an override-inherited scalar property is populated locally:

    LocalValues(T, SomeProperty)
        =
    {
        B
    }

then the local value replaces the inherited effective value:

    EffectiveValues(T, SomeProperty)
        =
    {
        B
    }

If no local value is present, the nearest inherited effective value is retained.

The initial design does not define:

- last-write-wins behavior outside `Override`;
- collection concatenation;
- item-level replacement;
- type-specific merge behavior; or
- selective removal of inherited values.

Accordingly:

- `Additive` should be used only for relationships and properties whose effective semantics legitimately support multiple accumulated values.
- `Override` should be used where the member's effective value set is supplied by the nearest local declaration in the type lineage.

---

## 4. Cardinality, Duplicate Elimination, and Provenance

### 4.1 Apply cardinality to effective values

Cardinality determines how many values of an `InstanceProperty` or targets of an `InstanceRelationship` an instance may effectively have.

Cardinality does not determine whether values are inherited. Inheritance is controlled separately by `InheritanceMode`.

Let `M` be a property or relationship member.

If:

    InheritanceMode(M) = None

then:

    EffectiveValues(T, M)
        =
    LocalValues(T, M)

If:

    InheritanceMode(M) = Additive

and `T` extends `P`, then:

    EffectiveValues(T, M)
        =
    EffectiveValues(P, M)
        ∪
    LocalValues(T, M)

Cardinality and other value constraints are evaluated against:

    EffectiveValues(T, M)

not merely against locally populated values.

### 4.2 Override-inherited singular relationship

Suppose `MetaHolonType` declares:

    UsesKeyRule cardinality 1..1

and:

    UsesKeyRule.DeclaredRelationshipType
        InheritanceMode Override

Every descriptor described by `MetaHolonType` must have exactly one effective `UsesKeyRule` relationship target.

A local target replaces the inherited effective target set. If no local target is populated, the nearest inherited target satisfies the requirement.

### 4.3 Additively inherited singular relationship

Suppose a relationship has:

    cardinality 0..1
    InheritanceMode Additive

If a descriptor inherits one target and locally adds a different target, its effective target count is two.

The descriptor therefore violates the `0..1` cardinality.

### 4.4 Duplicate values

Additive inheritance uses set union.

If the same value or relationship target appears both locally and through inheritance, it appears only once in the effective value set.

Formally:

    { A } ∪ { A } = { A }

Duplicate elimination is based on the identity or equality rule defined for the relevant value or relationship target.

### 4.5 Preserve provenance

Duplicate elimination must not discard provenance.

For example:

    HolonType
        AffordsCommands -> ReadCommand

    Book.HolonType
        Extends HolonType
        AffordsCommands -> ReadCommand

The effective value set is:

    {
        ReadCommand
    }

But the provenance includes both contributions:

    ReadCommand
        inherited from HolonType
        locally declared by Book.HolonType

An effective descriptor must be able to distinguish:

- locally declared contributions;
- inherited contributions;
- the descriptor that contributed each inherited value; and
- duplicate contributions that collapse to one effective value.

The exact representation is an implementation concern, but the semantic requirement is:

> Duplicate elimination does not erase contribution provenance.

### 4.6 String length constraints

String minimum-length and maximum-length constraints are evaluated in Unicode grapheme clusters, representing user-perceived characters.

They are not evaluated in:

- Unicode scalar values; or
- encoded bytes.

A grapheme cluster may contain multiple Unicode scalar values while representing one user-perceived character.

For example, a character formed from a base character and one or more combining marks counts as one grapheme cluster.

Formally, for a string value `S`:

    StringLength(S)
        =
    GraphemeClusterCount(S)

String-length conformance is therefore evaluated as:

    MinimumLength <= StringLength(S) <= MaximumLength

subject to the inclusive or exclusive boundary semantics declared by the applicable value constraint.

Encoded-size limits are separate representation constraints. They must be defined and evaluated independently from semantic string-length constraints.

---

## 5. Required Properties and Default Values

### 5.1 Add `DefaultValue` to property-type descriptors

`DefaultValue` is an instance property of property-type descriptors.

`MetaPropertyType` includes:

    InstanceProperties
        InheritanceMode
        IsValueRequired
        DefaultValue

The exact names used in the core schema remain authoritative.

`DefaultValue` contains the value to materialize when a required property is omitted during instance creation.

### 5.2 Restrict defaults to required properties

A `DefaultValue` may be defined only for a required property.

Formally:

    HasDefaultValue(P)
        implies
    IsValueRequired(P) = true

The valid combinations are:

| Required | Default defined | Meaning when omitted during creation |
|---|---:|---|
| No | No | The property remains absent |
| Yes | No | Creation fails unless a value is supplied |
| Yes | Yes | The default is materialized |

The following combination is invalid:

| Required | Default defined | Reason |
|---|---:|---|
| No | Yes | Omission would be ambiguous between intentional absence and use of the default |

Optional absence always denotes absence.

It never implicitly requests application of a default.

### 5.3 Materialize defaults during creation

A default value is a creation-time completion rule, not a descriptor-dependent read-time fallback.

A creation adapter is any boundary component that converts authored, imported, migrated, or programmatically constructed input into the explicit holon representation supplied to the descriptor kernel. This includes TDL adapters, JSON or graph import adapters, schema bootstrap loaders, programmatic builders, migration tooling, and runtime holon-creation APIs.

Every creation path must pass through a pre-kernel completion stage that materializes applicable descriptor-defined defaults. The descriptor kernel validates the completed explicit representation; it does not inject defaults, complete omitted values, or otherwise mutate that representation.

For every required property in the effective instance contract:

1. If the proposed property map contains an explicit value, retain it.
2. Otherwise, if the effective property descriptor defines a `DefaultValue`, materialize the default into the property map.
3. Otherwise, report a missing-required-property violation.
4. Supply the completed explicit representation to the descriptor kernel for validation.

Optional absent properties remain absent.

### 5.4 Explicit values take precedence

An explicitly supplied value always takes precedence over a default.

A default is applied only when the property is absent from the proposed property map.

### 5.5 Validate defaults

A default value must satisfy the same constraints as an explicitly supplied value.

This includes:

- value-type conformance;
- cardinality;
- range constraints;
- enumeration membership;
- representation constraints; and
- applicable validation rules.

An invalid default makes the property-type descriptor invalid.

### 5.6 Required-property invariant

After successful creation:

> Every required property is physically present in the resulting property map.

The property map can therefore be evaluated without loading descriptor context merely to recover default values.

### 5.7 Version stability

Once materialized, a default becomes ordinary persisted state.

If a property descriptor's default changes later:

- existing instances retain their previously materialized value;
- newly created instances receive the new default; and
- existing instances change only through an explicit migration or update.

### 5.8 Default provenance

The property map does not inherently distinguish:

- an explicitly supplied value; and
- a value materialized from a default.

If that distinction is required, it must be modeled separately as provenance metadata.

---

## 6. TDL Omission Semantics

### 6.1 Keep the grammar fixed

The TDL grammar remains fixed.

The core schema bound to a TDL document determines:

- which descriptor properties exist;
- which are required;
- which define defaults; and
- which may be omitted from authored TDL.

The schema does not dynamically introduce arbitrary grammatical forms.

It supplies semantic completion for existing forms.

### 6.2 General omission rule

A descriptor property may be omitted from TDL when its absence can be resolved deterministically from the effective descriptor.

There are two valid cases:

1. the property is optional, so it remains absent; or
2. the property is required and defines a default, so the default is materialized.

If a property is required and has no default, it must be supplied explicitly.

### 6.3 `InheritanceMode` omission

`InheritanceMode` is required and defaults to:

    None

Therefore, a property or relationship declaration may omit it when non-inheritance is intended.

The resulting descriptor nevertheless contains:

    InheritanceMode = None

in its materialized property map.

Only non-default cases need to be written explicitly:

    InheritanceMode Additive

or:

    InheritanceMode Override

### 6.4 Bind TDL to a core-schema version

TDL interpretation is bound to a particular core-schema version.

A TDL document or its containing package must identify the core-schema version against which it is interpreted.

The bound schema determines:

- available descriptor kinds;
- descriptor properties;
- requiredness;
- defaults;
- relationships;
- cardinalities; and
- validation rules.

### 6.5 Treat default changes as versioning events

Changing a default that affects omitted TDL declarations changes the interpretation of existing source text.

Such a change is therefore a semantic versioning event.

It may require a major schema version when the same TDL source would produce materially different descriptor semantics.

### 6.6 Support an expanded canonical form

TDL tooling should be able to emit an expanded representation in which all required defaulted properties have been materialized.

The expanded form supports:

- deterministic comparison;
- debugging;
- auditing;
- migration analysis;
- stable generated artifacts; and
- inspection of the descriptor state that will actually be created.

---

## 7. Key Differences Between the Current and Proposed Designs

### 7.1 Meaning of `InstanceProperties` and `InstanceRelationships`

Current:

- Their meaning is partly implicit and can be confused with properties and relationships populated by the type descriptor itself.

Proposed:

- They are explicitly defined as declarations in the contract a type imposes on its described instances.

### 7.2 Role of `DescribedBy`

Current:

- Descriptor holons may be described too generically.

Proposed:

- Each descriptor is described by its kind-specific meta-type.
- `DescribedBy` determines the schema-defined contract the current descriptor holon must satisfy.

### 7.3 Role of `Extends`

Current:

- `Extends` can appear to combine descriptor conformance, contract inheritance, classification, and value propagation.

Proposed:

- `Extends` additively inherits instance-contract declarations.
- It establishes subtype classification and substitutability within its hierarchy.
- It provides the type lineage over which explicitly declared semantic-inheritance behavior is resolved.
- It does not otherwise propagate populated descriptor values or relationship targets.

### 7.4 Relationship between meta-types and descriptor types

Current:

- Descriptor types may extend meta-types, mixing descriptive levels.

Proposed:

- `MetaTypeDescriptor` extends `HolonType`.
- Concrete meta-types extend within the branch rooted at `MetaTypeDescriptor`.
- Abstract descriptor categories extend within the unified hierarchy rooted at `TypeDescriptor`.
- Descriptor types are described by meta-types.

Meta-type conformance and descriptor semantic classification remain distinct roles even though
their types participate in one acyclic `Extends` graph.

### 7.5 Role of `TypeDescriptor`

Current:

- `TypeDescriptor` may appear to serve both as the generic describing type for descriptors and as the root of all meta-level and descriptor-level types.

Proposed:

- `TypeDescriptor` is the abstract root of the descriptor-type classification hierarchy.
- It serves as a polymorphic relationship target and query root for descriptor types.
- `MetaTypeDescriptor` is a descendant of `TypeDescriptor` through `HolonType` and remains the root
  of the meta-type branch.
- It is described by `MetaHolonType`.

### 7.6 Meta-type bootstrap

Current:

- The classification and description of the meta-types may be implicit.

Proposed:

- `MetaTypeDescriptor` extends `HolonType` and is the root of the meta-type branch.
- All meta-types are described by `MetaHolonType`.
- `MetaHolonType` is self-describing.
- The reflective fixed point follows from authored `DescribedBy` and `Extends` relationships rather
  than from a hidden bootstrap exception.

### 7.7 Source of kind-specific obligations

Current:

- It is unclear how obligations declared by `MetaHolonType`, `MetaPropertyType`, and other meta-types apply to authored descriptors.

Proposed:

- Each authored descriptor is directly described by its kind-specific meta-type.
- The effective instance contract of that meta-type therefore applies directly to the descriptor holon.

### 7.8 Polymorphic recognition

Current:

- The path by which descriptor kinds are recognized as `TypeDescriptor` may be unclear.

Proposed:

- Recognition follows the transitive `Extends` hierarchy within the descriptor-type hierarchy.

For example:

    Book.HolonType
        Extends HolonType

    HolonType
        Extends TypeDescriptor

therefore:

    Book.HolonType
        Extends* TypeDescriptor

### 7.9 Value inheritance

Current:

- It is unclear whether populated descriptor values propagate through `Extends`.

Proposed:

- Values remain local under `InheritanceMode None`.
- Every applicable property and relationship descriptor has a materialized `InheritanceMode`.
- `InheritanceMode Additive` causes effective values to accumulate across `Extends`.
- `InheritanceMode Override` selects the complete value set supplied by the nearest type in the self-first `Extends` lineage that locally populates the member.
- Cardinality is evaluated against effective values.
- Inherited values are not copied into local state.
- Contribution provenance is retained.

### 7.10 Defaults

Current:

- Missing values may require descriptor-aware fallback during reads.

Proposed:

- Defaults are permitted only for required properties.
- Defaults are materialized during creation.
- Optional properties cannot define defaults.
- Successful creation leaves every required property physically present.
- TDL omission is distinct from runtime absence.

---

## 8. Overall Structural Rules

The design can be summarized as follows:

1. `DescribedBy` determines the schema-defined contract that the current instance must satisfy.
2. `Extends` determines:
   - the instance contract that the current type passes on to its described instances;
   - subtype classification and substitutability within its hierarchy; and
   - the type lineage over which explicitly declared semantic-inheritance behavior is resolved.
3. The meta-type branch is rooted at `MetaTypeDescriptor`, which extends `HolonType`. Meta-types
   define contracts for descriptor holons and are themselves described by `MetaHolonType`.
4. The unified descriptor-type hierarchy is rooted at abstract `TypeDescriptor`.
5. Descriptor types define contracts for the instances they describe.
6. Meta-type conformance and descriptor semantic classification remain distinct roles within the
   unified `Extends` graph.
7. Every relationship endpoint is a holon and is validated through
   `EffectiveEndpointType(H) Extends* requiredType`.
8. Abstract descriptor types, rather than meta-types, classify descriptor-to-descriptor
   relationship endpoints.
9. Populated values remain local when their property or relationship descriptor declares `InheritanceMode None`. Under `Additive` or `Override`, effective values are resolved across the `Extends` lineage according to that mode. `InheritanceMode` is required, defaults to `None`, and is materialized during descriptor creation.
10. A default may be defined only for a required property. Every creation path materializes applicable defaults into the property map before descriptor-kernel validation; defaults are not resolved as read-time fallbacks.
11. `Extends` is single-valued and acyclic.
12. Every declared and inverse relationship descriptor has an explicit or completed directional
    `DeletionSemantic`; inverse deletion behavior is not inferred from the declared direction.
