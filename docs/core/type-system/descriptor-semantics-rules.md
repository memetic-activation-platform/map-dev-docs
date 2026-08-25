# Descriptor-Kernel Semantic Rules (v2.0.1)

This document defines the representation-neutral semantics of the Schema 2.0 descriptor kernel.
It is organized around the four jobs assigned to the kernel:

1. validate descriptor semantics;
2. compute effective semantic inheritance;
3. compute effective specifications and contracts; and
4. validate holon conformance.

The shared Holon Validator is the reusable validation entry point. It selects validation scope and
context, coordinates applicable rules, accumulates violations, and invokes the descriptor kernel
for the computations and predicates defined here. The validation framework must not independently
reimplement these semantics.

Callers supply an explicit holonic representation. How that representation was authored,
transported, completed, or staged is outside the kernel's semantic authority.

```text
Explicit Holonic Representation
        |
        v
Holon Validator
    - select validation scope and context
    - coordinate applicable rules
    - accumulate validation results
        |
        v
Descriptor Kernel
    - validate descriptor semantics
    - compute effective semantic inheritance
    - compute effective specifications and contracts
    - validate holon conformance
```

When a creation path treats omission as selection of a descriptor-defined default, that path must
materialize the value before kernel validation. The kernel computes and validates; it does not
transform the explicit representation supplied to it.

## 1. Shared Definitions

### 1.1 Notation

Each formal term declares a semantic signature using `Input -> Output`. A term returning `Boolean`
is a predicate and is defined with **iff**. A value-producing function is defined with `=`. These
are semantic result types, not Rust API signatures.

Named computations define products the kernel must derive. Stable rule IDs identify conditions the
kernel must explicitly validate. Explanatory text supplies motivation and consequences without
creating a second version of the computation or rule.

Rule IDs use `DS-<AREA>-<NUMBER>`. Moving a rule does not change its ID, and a retired ID is not
reused. The index in Section 7 is the implementation checklist for independently testable kernel
validations.

### 1.2 Describing Type

For every holon `H`:

    D : Holon -> Holon

    D(H) = the unique target of H.DescribedBy

Holons are self-describing in the MAP sense: each holon selects the holon type descriptor governing
its conformance through `DescribedBy`.

A descriptor may be self-describing when it satisfies the same compatibility and conformance rules
as every other descriptor. Core Schema 2.0 authors `MetaHolonType.MetaTypeDescriptor` as
self-describing.

No semantic rule follows `DescribedBy` transitively. If `D(H) = H`, contract computation still
terminates because effective products are computed before conformance is evaluated. Selecting the
already computed contract of `H` does not recursively validate `H`.

### 1.3 Extends Lineage and Descriptor Classification

For every holon `H`:

    parent : Holon -> Optional<Holon>

    parent(H) = the optional unique target of H.Extends

The `Extends` lineage of `H` is:

    L : Holon -> Sequence<Holon>

    L(H) = [H, parent(H), parent(parent(H)), ...]

The lineage is self-first and ends when a holon has no parent. Therefore:

    L(H) = [H], when parent(H) is absent

Descriptor classification is derived from that lineage:

    IsDescriptor : Holon -> Boolean

    IsDescriptor(H) iff TypeDescriptor is a member of L(H)

This avoids a separate descriptor-kind flag. `TypeDescriptor` is a descriptor because its lineage
contains itself. An ordinary holon without `Extends` has lineage `[H]` and is not a descriptor.

For type descriptor `T` and required type descriptor `R`:

    TypeSubstitutable : (TypeDescriptor, TypeDescriptor) -> Boolean

    TypeSubstitutable(T, R) iff R is a member of L(T)

`TypeSubstitutable(T, R)` expresses type substitutability. It does not mean that `T` conforms as
an instance of `R`; the contract governing `T` itself is selected through `D(T)`.

Runtime descriptor wrappers apply the same classification rule. Each wrapper
`W` declares one required descriptor category:

    CategoryAnchor : RuntimeWrapper -> TypeDescriptor

For example, `CategoryAnchor(PropertyDescriptor)` is
`PropertyType.TypeDescriptor`. A wrapper may narrow descriptor `T` only when:

    WrapperAdmissible : (Holon, RuntimeWrapper) -> Boolean

    WrapperAdmissible(T, W) iff TypeSubstitutable(T, CategoryAnchor(W))

This is a runtime-facing consequence of `TypeSubstitutable`, not a second graph-classification system.
Wrapper inventory, APIs, and encapsulation remain core-runtime concerns.

### 1.4 Abstract Descriptors

For every holon `H`:

    IsAbstract : Holon -> Boolean

    IsAbstract(H)
        iff
    IsDescriptor(H)
        and
    the unique effective IsAbstractType value of H is true

Completion materializes the required default of `false` for applicable descriptors when omission
is accepted. Only descriptor holons can therefore be abstract.

### 1.5 Instance TypeKind

Every type descriptor defines semantics for instances, but those instances do not all have the
same representation kind. A holon type describes holons, a property type describes property
occurrences, a declared relationship type describes declared relationship occurrences, and a
value type describes values. Dance, Command, and Operator are more specialized kinds of holon.

In simple terms, a meta-type says what a type definition must look like. An Instance TypeKind
anchor says what kind of instances that type defines. A descriptor holon needs both facts, and they
come from its two axes rather than from one flattened hierarchy.

The authored Boolean property `DefinesInstanceTypeKind` marks the descriptor anchors that
establish those kinds. It is declared by `MetaTypeDescriptor` because it is available on every
type descriptor. The kernel assigns that property the `Local` rule: an anchor designation is local
to the descriptor on which it is populated and is never inherited as a Boolean value.

For every descriptor holon `T`:

    IsInstanceTypeKindAnchor : Holon -> Boolean

    IsInstanceTypeKindAnchor(T)
        iff
    IsDescriptor(T)
        and
    T has the unique local completed DefinesInstanceTypeKind value true

Completion materializes the required default `false` when no value is authored. The kernel does
not infer an anchor from abstractness, a local name, a TDL declaration form, or a Rust enum.

For every descriptor holon `T`, define:

    InstanceTypeKind : Holon -> Optional<Holon>

    InstanceTypeKind(T)
        =
    the first IsInstanceTypeKindAnchor in the self-first lineage L(T), when one exists

The result is a descriptor identity, not a string label. A more specific anchor may extend another
anchor. For example, `DanceType.HolonType` can define a Dance kind while extending
`HolonType.TypeDescriptor`; Dance instances are therefore specialized holons.

`TypeDescriptor` intentionally has no `InstanceTypeKind`. It is the abstract root that unifies the
descriptor hierarchy, not a type that directly describes a representation kind. Every other
descriptor obtains a kind anchor from its lineage. Meta-types do not define another representation
kind merely because they are meta-types: their nearest anchor is normally
`HolonType.TypeDescriptor`, because type descriptors are themselves holons.

An anchor must be abstract. It classifies a representation family and may be extended, but it must
not directly describe runtime instances. Concrete descendants describe instances of the kind
selected by their nearest anchor.

When a runtime `InstanceTypeKind` or legacy `TypeKind` value is exposed, it is a derived projection
of the resolved anchor identity. It is not authored descriptor state or an independent source of
classification truth.

### 1.6 Describing-Category Pairing

Every descriptor has two classifications with different jobs:

- `L(H)` determines what kind of descriptor `H` is; and
- `L(D(H))` determines the contract that `H` itself must satisfy.

Those classifications cannot vary independently. Otherwise a property descriptor could select a
holon meta-type and avoid the property-descriptor contract, or a holon-type descriptor could select
an unrelated property meta-type.

The expected pairing is derived from the authored graph rather than from a kernel table of known
descriptor categories. `InstanceTypeKind(H)` supplies the explicit category designation; the
kernel does not use abstractness as a proxy for it. An extension schema can add an instance kind
and its meta-type pairing without adding that category to kernel code.

For every holon `H`:

    RequiredDescribingCategory : Holon -> Holon

    RequiredDescribingCategory(H)
        =
    D(InstanceTypeKind(H)),            when IsDescriptor(H)
                                            and InstanceTypeKind(H) is present
    MetaHolonType.MetaTypeDescriptor,  when H is TypeDescriptor
    HolonType.TypeDescriptor,          otherwise

For a descriptor with an instance-kind anchor, following that anchor's `DescribedBy` relationship
identifies the paired meta-type category. Thus:

    RequiredDescribingCategory(Title.PropertyType)
        =
    D(PropertyType.TypeDescriptor)
        =
    MetaPropertyType.MetaTypeDescriptor

`Title.PropertyType` must be described by that meta-type or a subtype so that the descriptor itself
receives the property-descriptor contract.

`TypeDescriptor` is the one root exception. It defines no instance kind and is required to be
described by `MetaHolonType.MetaTypeDescriptor`, the concrete meta-type for holon-type descriptor
holons.

`HolonType.TypeDescriptor` is the one deliberately hard-coded category anchor. It answers what may
describe an ordinary holon. The set of concrete holon types remains extensible because any
descriptor whose lineage includes that root is admissible.

### 1.7 Effective Specification and Contract

A type descriptor's **effective specification** is the complete set of semantics it imposes on
its instances after resolution across its own lineage. It includes, as applicable:

- the `InstanceTypeKind` of its instances;
- the properties and relationships those instances may or must populate;
- the effective key rule for holon instances;
- inherited affordances such as Commands and Dances; and
- other descriptor members selected by the kernel inheritance table for descendants.

This document uses **instance contract** more narrowly for the property and relationship member
declarations against which populated instance state is validated. The contract is part of the
effective specification; it is not a synonym for every inherited semantic product.

This distinction keeps the two axes clear:

- `L(D(H))` determines the effective specification to which `H` must conform; and
- when `H` is itself a type descriptor, `L(H)` determines the effective specification that `H`
  imposes on the instances it describes.

### 1.8 Contract Members and Binding

A holon's populated state and its conformance contract refer to members differently:

- populated properties and relationships are organized under compact names such as `Title` and
  `AuthoredBy`; and
- the contract contains references to descriptor holons such as `Title.PropertyType` and the
  declared `AuthoredBy` relationship descriptor.

Property values and relationship instances are not holons and do not carry `DescribedBy`. Their
characteristics must be discovered through the owning or source holon. At runtime, the source
holon's `HolonDescriptor` looks up the populated member in the effective contract and returns the
descriptor whose effective definition governs it.

An instance-contract member is identified by resolved descriptor identity:

- the referenced property descriptor for an instance property; or
- the referenced relationship descriptor for an instance relationship.

Names are the representation-level means of selecting those descriptors from a contract. They do
not replace descriptor identity after binding.

`PropertyMemberName` and `RelationshipMemberName` are member-navigation names,
not descriptor keys and not global relationship-type names. The same local
relationship member name may therefore identify distinct relationship
descriptors when those descriptors belong to separate effective conformance
contracts. A navigation surface that exposes both descriptors must use distinct
member names unless the navigation API is explicitly qualified by descriptor
identity.

For a property descriptor `P` and declared relationship descriptor `R`:

    PropertyMemberName : Holon -> PropertyName
    RelationshipMemberName : Holon -> RelationshipName

    PropertyMemberName(P)
        =
    the PropertyName formed from P's required local TypeName

    RelationshipMemberName(R)
        =
    the RelationshipName formed from R's required local TypeName

`TypeName` is used because it supplies the semantic name populated on a holon. `Key` instead
locates or references the descriptor holon before resolved identity is available. For example:

    contract declaration:    InstanceProperties -> Title.PropertyType
    populated property:      Title -> "The Dispossessed"

`Title.PropertyType` is the descriptor lookup key. `Title` is the property name. Binding resolves
the latter to the descriptor identity and validation consumes its effective definition.

Keys may incorporate category, immediate parent, or relationship endpoints. Such information is
useful for resolving descriptors but does not belong in member syntax. After resolution, semantic
validation uses descriptor identity and does not repeatedly interpret the key.

Property and relationship names occupy separate namespaces. Within each namespace names are exact,
case-sensitive `MapString` values. The kernel performs no case folding or Unicode normalization.

### 1.9 Enum Members and Tokens

Enum values are stored as scalar `MapString` tokens, not as self-describing holons or references to
enum-variant descriptors. Validation therefore needs one canonical token by which a stored value
selects a variant from its governing enum value type.

For every enum-variant descriptor `V`:

    EnumMemberName : Holon -> MapString

    EnumMemberName(V)
        =
    the MapString formed from V's required local TypeName

The local `TypeName` is the semantic value token. The variant's key identifies and resolves the
descriptor holon; display names are presentation metadata. Neither the key, a qualified key suffix,
nor any display name participates in enum-value matching.

## 2. Job One: Validate Descriptor Semantics

### 2.1 Purpose

Descriptors are executable schema. Before their declarations can govern another holon, the kernel
must establish that their graph structure, classification, and effective definitions are coherent.

Some checks in this job are structural prerequisites for all later computation. Others consume the
effective products defined in Jobs Two and Three. Section 6 states the evaluation order without
duplicating the rules here.

### 2.2 Structural Graph Validity

#### DS-STRUCT-001: Exactly one describing type

For every holon `H`, the explicit representation must contain exactly one `DescribedBy` target.
Zero targets and multiple targets are distinct violations.

#### DS-STRUCT-002: At most one direct parent

For every holon `H`, the explicit representation must contain at most one direct `Extends` target.

#### DS-STRUCT-003: Acyclic Extends lineage

No resolved holon identity may occur more than once while traversing `L(H)`. This check is evaluated
only along paths for which the next parent is unique.

#### DS-STRUCT-004: Extends lineage terminates at TypeDescriptor

For every holon with a direct `Extends` parent, the final holon in its finite lineage must be the
designated `TypeDescriptor` root.

These checks establish the assumptions used by `D(H)`, `parent(H)`, `L(H)`, and every later product.
A malformed or inaccessible lineage does not yield a partial semantic result.

`TypeDescriptor` is the abstract root of the unified descriptor hierarchy.
`HolonType.TypeDescriptor` is the branch for descriptors whose instances are holons.
`MetaTypeDescriptor.HolonType` extends that branch and roots the meta-type hierarchy.
`RelationshipType.TypeDescriptor` roots the common declared and inverse relationship branches.

#### DS-STRUCT-005: TypeDescriptor is the unique descriptor root

`TypeDescriptor` has no direct `Extends` parent. Every other descriptor has a finite lineage that
contains `TypeDescriptor`. A holon whose lineage does not contain that root is not treated as a
descriptor merely because it has a descriptor-like name, properties, or describing type.

### 2.3 Relationship-Specific Cycle Policy

Cycle policy belongs to the relationship being traversed:

- `Extends` is acyclic because inheritance requires a finite ancestor order.
- `DescribedBy` is single-valued but not transitively interpreted. Self-description and other
  `DescribedBy` cycles do not create semantic recursion.
- schema `DependsOn` is acyclic. Multi-pass loading resolves forward and circular references among
  components of one schema; it does not make mutually dependent schema versions independently
  versionable.
- inverse pairing and application relationships may form cycles unless their own descriptors
  prohibit them. Traversals over such cycles use bounded identity-based visitation.

#### DS-SCHEMA-001: Acyclic schema dependencies

The versioned schema `DependsOn` graph must be acyclic.

#### DS-SCHEMA-002: Declared cross-schema dependencies

Every authored cross-schema reference must be covered by a direct `DependsOn` edge from the
source component's schema to the target component's schema. Transitive reachability is sufficient
for lookup but does not replace that declaration.

#### DS-SCHEMA-003: Kernel inheritance-rule table

Inheritance policy is a kernel semantic, not authored descriptor state. The
kernel's canonical `InheritanceRules` table assigns:

- `Additive` to `InstanceProperties`, `InstanceRelationships`,
  `AffordsCommand`, `AffordsDance`, `AffordsOperator`, `ValidationBindings`, and
  `Constraints`;
- `Override` to `InstanceKeyRule`; and
- `Local` to every other member, including every property and every
  relationship not explicitly listed above.

The table is keyed by canonical `CoreRelationshipTypeName` for its non-local
entries. A Core implementation must cover every listed relationship in unit
tests and prove the local fallback. The Core Schema corpus does not author or
validate inheritance-policy values.

### 2.4 Describing-Type Compatibility

Describing-type compatibility preserves the graph-defined distinction between ordinary holons and
descriptor holons while pairing each descriptor category with the correct meta-type contract.

    IsMetaType : Holon -> Boolean

    IsMetaType(T)
        iff
    TypeSubstitutable(T, MetaTypeDescriptor.HolonType)

    DescribingLineagesCompatible : Holon -> Boolean

    DescribingLineagesCompatible(H)
        iff
    (IsDescriptor(H) iff IsMetaType(D(H)))
        and
    TypeSubstitutable(D(H), RequiredDescribingCategory(H))

The first clause requires descriptor holons, and only descriptor holons, to be described by
meta-types. The second clause applies the category selected by `RequiredDescribingCategory(H)`:
the graph-derived meta-type pairing for a descriptor, or the deliberately hard-coded
`HolonType.TypeDescriptor` category for an ordinary holon. The latter admits specialized holon
types such as Dance, Command, and Operator while rejecting property, relationship, and value
types as direct `DescribedBy` targets.

These clauses reject all of the important mismatches without a hard-coded category table:

- `MyBook DescribedBy MapString.ValueType` fails because a value type does not describe holons.
- `Title.PropertyType DescribedBy Book.HolonType` fails because a descriptor must be described by
  a meta-type.
- `Title.PropertyType DescribedBy MetaHolonType.MetaTypeDescriptor` fails because the meta-type is
  not the category paired with the Property instance-kind anchor.
- `Title.PropertyType DescribedBy MetaPropertyType.MetaTypeDescriptor` succeeds when the remaining
  descriptor structure also conforms.

The pairing is not inferred from names, TDL declaration forms, abstractness, or `TypeKind`.

#### DS-KIND-001: Local anchor designation

`DefinesInstanceTypeKind` must resolve locally to exactly one Boolean value on every descriptor
for which the completed contract requires it. It uses the kernel's `Local`
inheritance rule; inherited truth must never turn every descendant into another anchor.

#### DS-KIND-002: Anchors are abstract

For every descriptor `T`, `IsInstanceTypeKindAnchor(T)` implies `IsAbstract(T)`.

#### DS-KIND-003: Root kind exception

`TypeDescriptor` must not define an instance kind. Every other descriptor must have exactly one
nearest `InstanceTypeKind` result in its single self-first lineage.

#### DS-KIND-004: Required describing-category compatibility

For every holon `H`, `D(H)` must equal or extend `RequiredDescribingCategory(H)`.

#### DS-KIND-005: Descriptor/meta-type correspondence

For every holon `H`, `IsDescriptor(H)` must be equivalent to `IsMetaType(D(H))`.

A runtime `InstanceTypeKind` or legacy `TypeKind` projection must agree with the graph-derived
`InstanceTypeKind(T)`. Runtime projections do not participate in these validations.

### 2.5 Effective Contract Integrity

Contract construction is defined in Job Three. Once computed, a descriptor's contract must satisfy
the following declaration-level invariants.

#### DS-CONTRACT-001: No inherited-member redeclaration

An inherited contract member may not be redeclared locally. Repeating the same resolved member
descriptor identity is a `RedundantInheritedMemberDeclaration`, even when the declaration is
unchanged. Contract construction must inspect contribution provenance so additive duplicate
normalization cannot hide that repetition.

Schema 2.0 does not support subtype refinement of an inherited member's cardinality, value type,
requirement status, endpoints, or validation constraints. A subtype cannot express refinement by
substituting a different member descriptor with the same semantic member name; that violates
`DS-CONTRACT-002`. Variance and compatibility rules for safe subtype refinement are deliberately
deferred. Introducing them would be a future semantic change, not a relaxation inferred by an
implementation.

#### DS-CONTRACT-002: Unique semantic member names

Within one effective conformance contract, two distinct descriptor identities
may not claim the same `PropertyMemberName` in the property namespace or the
same `RelationshipMemberName` in the relationship namespace. Such a collision
is a `DuplicateSemanticMemberDeclaration`, including when the newer declaration
was intended to refine an inherited member. This rule does not impose global
uniqueness across independently owned contracts or descriptor identities.

#### DS-CONTRACT-003: Well-formed effective member definitions

The effective definition of every contract member must be well formed:

- a required singular field resolves to exactly one effective value;
- an optional singular field resolves to zero or one effective value;
- minimum and maximum cardinalities are non-negative;
- a present maximum is not less than the minimum; and
- every effective field satisfies its own value, endpoint, collection, and constraint policy.

#### DS-CONTRACT-004: Contract member kind compatibility

Every `InstanceProperties` target must have an `InstanceTypeKind` equal to or specializing
`PropertyType.TypeDescriptor`. Every `InstanceRelationships` target must have an
`InstanceTypeKind` equal to or specializing
`DeclaredRelationshipType.RelationshipType`. A property descriptor's selected `ValueType` target
must have an `InstanceTypeKind` equal to or specializing `ValueType.TypeDescriptor`.

These are checks over the products computed by Jobs Two and Three. They are not alternate local-read
rules.

### 2.6 Default Declaration Integrity

For property descriptor `P`, requiredness, value type, and default come from
`EffectiveMemberDefinition(P)`.

    IsValueRequired : Holon -> Boolean

    IsValueRequired(P)
        iff
    the effective IsValueRequired field of P is true

    HasDefaultValue : Holon -> Boolean

    HasDefaultValue(P)
        iff
    EffectiveMemberDefinition(P) contains a DefaultValue

#### DS-DEFAULT-001: Defaults require required properties

A default may be defined only for a required property:

    HasDefaultValue(P) implies IsValueRequired(P)

The valid declaration states are therefore optional without a default, required without a
default, and required with a default. Optional-with-default is intentionally not represented:
omission of an optional property means absence rather than implicit value selection.

`DefaultValue.PropertyType` uses `BaseValueValueType.ValueType` so its representation can hold any
runtime `BaseValue`. The value is then dependently validated against the effective `ValueType` of
the property descriptor that declares the default.

#### DS-DEFAULT-002: Default value conformance

The default must satisfy the same effective value type and constraints as an explicitly populated
value. An invalid default makes the property descriptor invalid.

This rule validates the declaration of a default. It does not authorize the kernel to materialize
that default into another holon.

### 2.7 Relationship-Descriptor Integrity

#### DS-REL-001: Bijective inverse pairing

Every declared relationship descriptor has exactly one effective inverse, and every inverse is
paired back to exactly that declared descriptor.

#### DS-REL-002: Inverse endpoint correspondence

For a declared relationship descriptor `R` and paired inverse `I`, effective endpoints must
correspond:

    SourceType(I) = TargetType(R)
    TargetType(I) = SourceType(R)

Directional cardinality constraints need not match. Each direction is evaluated per source over
the same occurrence graph.

#### DS-REL-003: Directional deletion declarations

Declared and inverse relationship descriptors each require an effective `DeletionSemantic`. The
inverse value is resolved independently rather than copied from the declared direction. The kernel
validates presence and value type. Pairwise deletion execution, cascade cycles, and interactions
between `Block` and `Cascade` remain proposed rather than settled here; they are delegated to the
[Relationship Constraints specification](relationship-constraints-design-spec.md).

### 2.8 Key-Rule Integrity

#### DS-KEY-001: Exactly one effective instance key rule

Every type descriptor whose `InstanceTypeKind` equals or specializes
`HolonType.TypeDescriptor` must resolve exactly one effective `InstanceKeyRule` target. Zero or
multiple effective targets are invalid.

#### DS-KEY-002: Key-rule target compatibility

The selected target must conform to the effective target constraint of `InstanceKeyRule` and must
provide a supported key-rule strategy or configured key-rule instance. An abstract target cannot
serve directly as the selected rule.

#### DS-KEY-003: Explicit keyless baseline

The effective `InstanceKeyRule` definition must remain singular, required, and `Override`.
`HolonType.TypeDescriptor` must explicitly select `NoneRule.KeyRuleType`. An absent relationship is
not a representation of keylessness.

### 2.9 Enum-Descriptor Integrity

#### DS-ENUM-001: Unique enum member names

For any enum value-type descriptor `E`, distinct variant descriptor identities in the effective
`Variants` target collection must have distinct `EnumMemberName` values. A duplicate token makes
the enum definition ambiguous and is an error even when the variant descriptor keys differ.

### 2.10 Constraint-Descriptor Integrity

#### DS-CONSTRAINT-001: Constraint monotonicity

For every type descriptor and constraint family, the effective accepted-state set of a subtype must
be a subset of, or equal to, the effective accepted-state set of its parent. A local constraint
contribution that weakens an inherited applicable constraint is invalid. Equal contributions may be
diagnosed by authoring tools but do not weaken the definition.

#### DS-CONSTRAINT-002: Constraint applicability

For every occurrence `T -[Constraints]-> C`, `C` must be described by a concrete `ConstraintType`
whose effective `ApplicableToInstanceTypeKinds` targets include `InstanceTypeKind(T)`. The check
uses the existing graph-derived Instance TypeKind anchors. It does not introduce or consult a
separate capability taxonomy.

#### DS-CONSTRAINT-003: Constraint configuration

Every constraint holon must conform to the effective property and relationship contract of its
concrete `ConstraintType`. A constraint family additionally validates every configuration
invariant necessary to interpret the configured constraint, such as non-negative counts and a
minimum that does not exceed a present maximum. An invalid constraint makes the constrained type's
effective definition invalid; it is never advisory or silently ignored.

## 3. Job Two: Compute Effective Semantic Inheritance

### 3.1 Purpose and Scope

Descriptor members can contribute semantics to descendant descriptors. One
generic inheritance engine computes those effective values, but its policy is
selected by the kernel's canonical `InheritanceRules` table rather than by
authored descriptor state.

Semantic inheritance applies only to descriptor semantics across `Extends`. It does not create
general value inheritance among ordinary runtime holons, and it never copies inherited values into
local descriptor state.

### 3.2 Inputs and Result

For member `M`:

    InheritanceRule : Member -> { Local, Additive, Override }

    InheritanceRule(M)
        =
    the kernel-selected rule for M

`InheritanceRules` is a closed kernel table. Its named entries are
`InstanceProperties`, `InstanceRelationships`, `AffordsCommand`,
`AffordsDance`, `AffordsOperator`, `ValidationBindings`, `Constraints`, and
`InstanceKeyRule`; all other members resolve to `Local`. The table is
available before effective contracts and member definitions are computed.

For type `T` and member `M`:

    LocalValues : (Holon, Member) -> ContributionCollection

    LocalValues(T, M)
        =
    the values or relationship occurrences populated locally on T through M

Local contributions retain authored occurrence identity, duplicates, and authoritative order so
invalid local state and contribution provenance remain observable.

    EffectiveValues : (Holon, Member) -> EffectiveCollection

    EffectiveValues(T, M)
        =
    the policy-aware collection produced by applying InheritanceRule(M) across L(T)
    and then applying M's collection policy

The collection operations used by all modes are:

    Concatenate : (ContributionCollection, ContributionCollection)
                  -> ContributionCollection
    NormalizeForMember : (Member, ContributionCollection) -> EffectiveCollection

### 3.3 Local

When `InheritanceRule(M) = Local`:

    EffectiveValues(T, M)
        =
    NormalizeForMember(M, LocalValues(T, M))

Only local contributions participate. An ancestor's value cannot satisfy a local requirement.

### 3.4 Additive

When `InheritanceRule(M) = Additive` and `T` has parent `P`:

    EffectiveValues(T, M)
        =
    NormalizeForMember(
        M,
        Concatenate(EffectiveValues(P, M), LocalValues(T, M))
    )

When `T` has no parent, additive resolution normalizes its local values.

Inherited contributions precede local contributions. Recursion therefore produces root-to-self
contribution order while preserving authoritative local order within each contributor.

Additive inheritance accumulates. It does not imply replacement, precedence, last-write-wins, or
removal of inherited contributions.

`Constraints` is an additive member. The effective constraint collection preserves
ancestor-before-local provenance, then `DS-CONSTRAINT-001` evaluates the resulting contribution
set for attempted relaxation. Applicability is validated on every local contribution before it can
participate in the effective collection. These checks establish valid definition data; they do not
select a validation engine or provide the context needed to execute every constraint.

### 3.5 Override

When `InheritanceRule(M) = Override`:

    EffectiveValues(T, M)
        =
    NormalizeForMember(M, LocalValues(T, M)),
        when LocalValues(T, M) is non-empty

    EffectiveValues(parent(T), M),
        otherwise, when parent(T) exists

    empty collection,
        otherwise

Override resolution is self-first. The nearest type in `L(T)` that locally populates `M` supplies
the complete effective collection. More distant contributions are shadowed rather than combined.

### 3.6 Effective Collection Policy

Effective values are policy-aware collections, not universal sets. For relationship member `M`,
`NormalizeForMember` uses the effective ordering and duplicate policy:

| `IsOrdered` | `AllowsDuplicates` | Effective collection |
| --- | --- | --- |
| `false` | `false` | set |
| `false` | `true` | multiset |
| `true` | `false` | duplicate-free sequence |
| `true` | `true` | sequence |

For ordered relationships, local order comes from authoritative relationship-occurrence metadata,
not incidental storage, retrieval, or serialization order. For unordered relationships, retained
processing order has no semantic meaning.

When duplicates are allowed, every occurrence and occurrence identity remain. When duplicates are
disallowed, targets are compared by semantic identity. The first occurrence in ancestor-before-
local order supplies the retained occurrence and, when ordered, its position.

For property members, the local representation contains at most one value per property name.
Across inheritance, equal contributions normalize as one value. More than one distinct contribution
is a conflicting effective property value and fails `DS-PROP-002`; property singularity does not
come from relationship cardinality fields.

Properties use the `Local` rule. A descriptor property therefore never inherits
an ancestor's populated value through `EffectiveValues`; a descriptor that
requires a property value must carry it locally.

Normalization never excuses invalid local state. It must not hide duplicate local occurrences or an
inherited contract-member redeclaration.

### 3.7 Contribution Provenance

Effective resolution retains enough provenance to explain and validate the result.

For additive inheritance, provenance identifies every inherited and local contribution, its
contributing type, and any contributions collapsed by normalization.

For override inheritance, provenance identifies the winning contribution collection and shadowed
collections from more distant ancestors. Shadowed values do not contribute to effective
cardinality.

The exact provenance representation is an implementation concern. Preserving these semantic facts
is mandatory.

An `Additive` relationship member with a finite maximum shares that maximum across every
contribution in the lineage. The maximum is not reset for each descendant. In particular, maximum
one means an inherited contribution leaves no room for a distinct local contribution. This is a
valid but potentially surprising schema design; authoring tools should surface it without
prohibiting it.

### 3.8 Instance TypeKind Selection

`InstanceTypeKind(T)` is an effective classification product resolved self-first across `L(T)`.
The first local `DefinesInstanceTypeKind = true` designation wins. More distant anchors remain in
the lineage and establish kind substitutability; their Boolean values are not inherited onto `T`.

This uses the local `DefinesInstanceTypeKind` designation with a dedicated
self-first classification rule; it is not an authored inheritance policy. The
anchor rules are validated by `DS-KIND-001` through `DS-KIND-003`.

### 3.9 Effective Key-Rule Selection

`InstanceKeyRule` is an ordinary inherited relationship member. The kernel
assigns it the `Override` rule. Its effective definition declares cardinality
`1..1` and a `KeyRuleType.HolonType` target; key-rule selection then resolves
targets through the generic inheritance engine.

Only holon types participate. Property values, value instances, and relationship instances are not
holons and do not have independent semantic keys.

For holon type `T`:

    instance_key_rule : Holon -> Holon

    instance_key_rule(T)
        =
    the unique target in EffectiveValues(T, InstanceKeyRule)

The root holon type establishes explicit keylessness:

    HolonType.TypeDescriptor
        InstanceKeyRule -> NoneRule.KeyRuleType

A descendant remains keyless unless it or a nearer ancestor overrides that target. Keylessness is
not represented by an absent effective rule.

Resolution fails when the effective target collection contains zero or more than one key rule.

For every holon `H`:

    holon_key_rule : Holon -> Holon

    holon_key_rule(H) = instance_key_rule(D(H))

A key rule populated on type `T` governs holons described by `T`; it does not govern the key of `T`
itself. The key of descriptor `T` is governed by the effective key rule of `D(T)`.

`ExtendedTypeRule.KeyRuleType` derives descriptor keys from the local type name and immediate
`Extends` target type name. A descriptor without `Extends` falls back to its local type name.
Changing the immediate parent is therefore key-affecting for newly created descriptor versions.

`DescribedTypeRule.KeyRuleType` derives named ordinary-holon keys from the local type name and the
local type name of `D(H)`. Configured `FormatRule` holons derive keys from an authored template and
ordered property-descriptor parameters.

Key lookup is not identity. Before identity is available, a source reference may bind by key only
when that key resolves uniquely in the schema package and dependency closure. After resolution,
relationships and semantic validation use resolved identity.

Schema-qualified key namespaces and coexistence of colliding local keys from independent extension
schemas belong to the deferred Extension Schema identity design. The kernel does not silently infer
qualification or claim that the current unqualified-key model resolves those collisions.

A persisted key is explicit state:

    PersistedKey : Holon -> Optional<Key>

    PersistedKey(H)
        =
    the Key stored when the holon version was created, when present

`PersistedKey(H)` is absent for a keyless holon.

Later key-rule or schema changes do not retroactively recompute persisted keys. Migration and alias
behavior must be explicit.

### 3.10 Stored and Effective Inverse Occurrences

A declared relationship occurrence is the authoritative authored fact. Commit materializes its
paired inverse occurrence for traversal. Effective inheritance is then resolved independently in
each direction from the occurrences locally available in that direction.

The kernel does not reverse the declared direction's `EffectiveValues` to manufacture virtual
inverse edges. Consequently:

- `Instances` discovers holons whose explicit `DescribedBy` occurrences have committed inverse
  occurrences;
- `KeyRuleForInstancesOf` discovers types that explicitly populate `InstanceKeyRule`, not every
  descendant that inherits the same rule through `Override`; and
- a query for every type effectively governed by a key rule must evaluate each candidate type's
  effective key-rule selection.

Commit outcomes, deferred cross-space inverse materialization, recognition, and repair belong to the
[Relationship Persistence specification](../transactions/relationship-persistence-design-spec.md).
The kernel consumes the explicit occurrence graph supplied to it.

## 4. Job Three: Compute Effective Specifications and Contracts

### 4.1 Purpose

Inheritance produces effective collections. Specification computation assembles those products
into the semantics a type imposes on its instances. Contract computation interprets the subset
that declares populated property and relationship members.

This distinction matters because `InstanceProperties` and
`InstanceRelationships` are ordinary populated relationship members. The
kernel's `InheritanceRules` table assigns both `Additive`; contract computation
begins only after that generic resolution finishes.

### 4.2 Effective Specification

For type descriptor `T`:

    EffectiveSpecification : Holon -> Specification

    EffectiveSpecification(T)
        =
    the descriptor semantics resolved from L(T), including:
        InstanceTypeKind(T)
        EffectiveInstanceContract(T)
        EffectiveValues(T, M) for applicable inherited descriptor member M
        instance_key_rule(T), when T describes holons

The effective specification includes inherited affordances, key selection, constraints, and other
member-controlled semantics in addition to the instance contract. It is a computed semantic
product, not a stored `EffectiveDescriptor` holon or another intermediate representation.

### 4.3 Effective Instance Contract

For type descriptor `T`:

    EffectiveInstanceContract : Holon -> Contract

    EffectiveInstanceContract(T)
        =
    the contract interpretation of:
        EffectiveValues(T, InstanceProperties)
        and
        EffectiveValues(T, InstanceRelationships)

The kernel assigns both contract relationships `Additive`. Descendants
therefore accumulate inherited and local contract declarations. This policy is
not configurable by an authored descriptor.

After effective values are available, contract interpretation checks inherited redeclarations and
duplicate member names under Job One. The surviving property and relationship descriptor
identities form the effective instance contract.

### 4.4 Conformance Contract

For every holon `H`:

    ConformanceContract : Holon -> Contract

    ConformanceContract(H) = EffectiveInstanceContract(D(H))

`DescribedBy` therefore selects the contract that the current holon must satisfy.

More broadly, `EffectiveSpecification(D(H))` supplies every type-dependent semantic that governs
`H`; `ConformanceContract(H)` selects the member-declaration portion used to validate populated
state.

### 4.5 Effective Member Definition

For property or relationship descriptor `M`:

    EffectiveMemberDefinition : Holon -> MemberDefinition

    EffectiveMemberDefinition(M)
        =
    for every semantic member S in ConformanceContract(M):
        S -> EffectiveValues(M, S), with contribution provenance

An effective member definition is a computed view over `M` and its `Extends` lineage. It is not a
stored intermediate representation and does not copy values into `M`.

For a property descriptor, the view includes effective `ValueType`, `IsValueRequired`,
`DefaultValue`, and constraints of the selected value type.

For a relationship descriptor, the view includes effective endpoints, cardinalities, ordering,
duplicate policy, definitional and deletion semantics, and applicable relationship constraints.

Every field is resolved through the kernel-selected inheritance rule for its
canonical member identity. Properties and unnamed relationship members use
`Local`; no field becomes inherited merely because it participates in a member
definition.

### 4.6 Descriptor Self-Semantics and Described Instances

Every type descriptor `T` plays two distinct semantic roles:

1. `EffectiveSpecification(D(T))`, including `ConformanceContract(T)`, governs `T` as a holon.
2. `EffectiveSpecification(T)`, including `EffectiveInstanceContract(T)`, governs the instances
   that `T` describes.

These roles are connected through `DescribedBy` but are never flattened into one surface.

For example:

    Book.HolonType
        Extends HolonType.TypeDescriptor
        DescribedBy MetaHolonType.MetaTypeDescriptor

means:

- `Book.HolonType` itself conforms to
  `EffectiveInstanceContract(MetaHolonType.MetaTypeDescriptor)`; and
- holons described by `Book.HolonType` conform to
  `EffectiveInstanceContract(Book.HolonType)`.

Extending `HolonType.TypeDescriptor` classifies `Book.HolonType` as a holon-type descriptor. It does
not impose the populated self-contract of `MetaHolonType`. Conversely, being described by
`MetaHolonType` does not add meta-type declarations to the ordinary Book instance contract.

This separation is the central reason the existing holonic representation can serve as the
semantic intermediate representation. The kernel computes views over ordinary holons and
relationships rather than translating them into a second semantic object model.

### 4.7 Product Evaluation and Memoization

Effective products are computed from one immutable graph snapshot and memoized by product kind and
resolved descriptor identity. Products involving multiple identities, such as
`EffectiveValues(T, M)`, are memoized by the complete tuple.

Computing `EffectiveInstanceContract(T)` does not first validate `T`. Selecting
`ConformanceContract(H)` reads the already computed contract of `D(H)` without recursively asking
whether either holon conforms.

Encountering the same in-progress product dependency is a semantic evaluation cycle unless a rule
explicitly defines a fixed point. `DescribedBy` edges do not themselves create product dependencies
because conformance is evaluated after product computation.

Any graph mutation, including default materialization, invalidates affected snapshot products.
Final conformance uses products computed from the completed graph supplied to validation.

## 5. Job Four: Validate Holon Conformance

### 5.1 Purpose

Conformance asks whether one explicit holon representation conforms to the effective specification
selected by its `DescribedBy` relationship. It does not fill omissions, materialize defaults, or
normalize the holon's authored state.

For every holon `H`:

    H conforms
        iff
    its describing type is valid
        and
    every populated or required member satisfies ConformanceContract(H)

Descriptor holons use exactly this process. Their describing meta-types select the contracts that
govern their own populated descriptor state.

### 5.2 Describing-Type Validity

The holon's describing lineage must satisfy `DescribingLineagesCompatible(H)` as defined in Job
One through `DS-KIND-004` and `DS-KIND-005`. Conformance consumes that result; it does not define
another classification rule.

#### DS-CONFORM-001: Concrete describing type

The describing type must also be concrete:

    not IsAbstract(D(H))

Abstract descriptors may participate in lineages and endpoint classification, but no holon may use
an abstract descriptor as its direct describing type.

### 5.3 Member Binding

For each populated property or relationship name, binding searches the corresponding namespace of
`ConformanceContract(H)`.

#### DS-BIND-001: Unique property-member binding

Every populated property name must resolve to exactly one property descriptor in
the property namespace of `ConformanceContract(H)`, unless the effective
additional-property policy permits an undeclared property. More than one match
within that contract is always ambiguous and invalid. This binding rule does not
compare property-member names across other contracts.

#### DS-BIND-002: Unique relationship-member binding

Every populated relationship name must resolve to exactly one declared
relationship descriptor in the relationship namespace of
`ConformanceContract(H)`, unless the effective additional-relationship policy
permits an undeclared relationship. More than one match within that contract is
always ambiguous and invalid. Separate source contracts may use the same
forward relationship member name; if they are both exposed through one
name-based inverse navigation surface, their inverse member names must differ.

After binding, conformance and occurrence grouping use resolved descriptor identity rather than the
name string. A permitted undeclared member remains explicitly unbound and is grouped only within
its member kind by exact stored name.

Binding is necessary because property values and relationship instances are not self-describing.
Their source holon and its effective contract supply the route to the descriptor that governs them.

### 5.4 Abstract Descriptor Completeness

Abstract descriptors may omit category-specific required members so that abstract categories can
declare contracts that only concrete descendants fully realize. They may not omit universal
descriptor structure.

Define the graph-derived baseline:

    UniversalDescriptorContract : Contract

    UniversalDescriptorContract
        =
    EffectiveInstanceContract(MetaTypeDescriptor.HolonType)

    UniversalDescriptorMember : Member -> Boolean

    UniversalDescriptorMember(M)
        iff
    M is a member of UniversalDescriptorContract

This baseline includes universal members such as `DescribedBy` and `ComponentOf`. A member such as
`ValueType`, introduced below that baseline by a category-specific meta-type, remains
category-specific.

For member `M` in `ConformanceContract(H)`:

    EnforceMinimum : (Holon, Member) -> Boolean

    EnforceMinimum(H, M)
        iff
    not IsAbstract(H)
        or
    UniversalDescriptorMember(M)

#### DS-CONFORM-002: Member-specific minimum enforcement

When `EnforceMinimum(H, M)` is true, the member's effective minimum is enforced. When it is false,
absence does not violate the minimum. A populated member still must satisfy maximum cardinality,
type, endpoint, and every other applicable constraint.

The exemption does not relax structural validity. Abstract descriptors still require one concrete,
lineage-compatible `DescribedBy` target, one schema through `ComponentOf`, and a valid optional
`Extends` parent.

### 5.5 Property Conformance

For each property descriptor `P` in `ConformanceContract(H)`, conformance consumes
`EffectiveMemberDefinition(P)`.

#### DS-PROP-001: Required property presence

The property satisfies requiredness only when it is present in the explicit representation,
unless `EnforceMinimum(H, P)` is false. A default materialized before validation is ordinary
explicit state; absence never causes the kernel to read a fallback value.

#### DS-PROP-002: Property value conformance

Each present value must satisfy the effective value type, native representation, and value
constraints. A property name carries at most one property value; optionality is expressed by
`IsValueRequired`, while multiplicity within a value is modeled by an applicable array value type.
When semantic inheritance supplies property values across a descriptor lineage, more than one
distinct contribution is a `ConflictingEffectivePropertyValues` error rather than a cardinality
violation. Equal contributions normalize to one effective value.

Current foundational interpretations include:

- enum membership follows `DS-ENUM-002` and `DS-ENUM-003`;
- integer bounds honor inclusive and exclusive declarations; and
- string lengths follow the Unicode grapheme-cluster policy owned by the
  [Value Constraints specification](value-constraints-design-spec.md) rather than counting scalar
  values or encoded bytes.

#### DS-ENUM-002: Exact enum token membership

For a value governed by enum value-type descriptor `E`, a stored token `S` conforms exactly when
there is exactly one variant `V` in the effective `Variants` target collection of `E` for which:

    S = EnumMemberName(V)

Comparison is exact and case-sensitive. The kernel performs no case folding or Unicode
normalization. A variant key, qualified key, display name, or plural display name is not an enum
token and must not be accepted as one.

#### DS-ENUM-003: Enum token non-retroactivity

Changing a variant descriptor's local `TypeName` changes its `EnumMemberName` and is therefore a
value-affecting, breaking schema change. It does not rewrite, alias, or reinterpret persisted enum
values. A schema evolution that replaces a token must retain the old member while it remains
accepted or explicitly migrate stored values before validating them against the new specification.

Changes to a variant's key or display metadata do not change the token when its local `TypeName`
remains unchanged.

#### DS-PROP-003: Additional-property policy

An unbound property is valid only when the effective additional-property policy permits it. A
permitted unbound value still must be a valid native MAP property value.

### 5.6 Relationship Conformance

For each relationship descriptor `R` in `ConformanceContract(H)`, conformance consumes
`EffectiveMemberDefinition(R)`.

#### DS-OCC-001: Relationship occurrence grouping

All occurrences bound to the same resolved descriptor identity form one relationship collection.
An absent relationship has count zero. A permitted undeclared relationship has no descriptor
identity and is grouped by exact name within the relationship namespace.

The final collection, rather than a mode-specific intermediate collection, is evaluated against the
effective minimum and maximum. Job Two already determines whether the collection is local,
additive, or overridden. Cardinality therefore needs one rule, not a separate restatement for each
kernel inheritance rule.

#### DS-OCC-002: Endpoint compatibility

Every source and target must satisfy the effective endpoint constraints. Define:

    EndpointCompatible : (Holon, TypeDescriptor) -> Boolean

    EndpointCompatible(H, requiredType)
        iff
    TypeSubstitutable(D(H), requiredType)

For occurrence:

    source -[R]-> target

the validator checks:

    EndpointCompatible(source, SourceType(R))
    EndpointCompatible(target, TargetType(R))

Every holon is an instance of its direct describing type. Endpoint compatibility therefore asks
only whether the holon's `DescribedBy` target can substitute for the required type. A descriptor
holon is tested through its describing meta-type like every other holon; its own `Extends` lineage
is not an independent endpoint-admission path.

Endpoint compatibility does not select the contract against which `H` conforms.

#### DS-OCC-003: Relationship collection policy

The final occurrence collection must satisfy the effective ordering and duplicate policy. Ordered
relationships require authoritative ordering metadata. When duplicates are allowed, distinct
occurrence identities must remain distinguishable.

#### DS-OCC-004: Additional-relationship policy

An unbound relationship is valid only when the effective additional-relationship policy permits
it. Its source, target, and native occurrence representation must still be structurally valid.

### 5.7 Relationship Cardinality and Value Constraints

Relationship cardinality is evaluated against the final occurrence collection supplied to
conformance:

- populated relationship state of ordinary `H` is checked under `ConformanceContract(H)`;
- inherited descriptor relationships are checked against `EffectiveValues(T, R)`; and
- duplicate policy determines which occurrences remain in the counted collection.

Properties have no descriptor cardinality fields. `IsValueRequired` controls property presence,
and the holon property map permits at most one value for each property name. Multiplicity inside a
property value is governed by its selected array value type; `MinimumItems`, `MaximumItems`, and
other array constraints belong to that value type.

#### DS-CARD-001: Effective cardinality

For a bound relationship descriptor `R`, every effective applicable
`CardinalityConstraint` supplies a minimum and optional maximum applied to the final effective
occurrence collection. An absent maximum means unbounded; no finite sentinel represents infinity.
All applicable constraints must pass, so additive subtype contributions can only retain or narrow
the admitted collection. `DS-CARD-001` is the stable validation and diagnostic identity for this
evaluation; it is not a second store of cardinality parameters.

For Commit validation, that collection is the prospective occurrence collection of the current MAP
Space: locally committed occurrences, minus locally removed or superseded occurrences in the
Commit, plus locally staged declared occurrences and locally derived inverse occurrences. A
cross-space inverse occurrence is outside this scope. Its later materialization or recognition does
not retroactively change the validation result of the declaring Commit. The cross-space commit
boundary is defined by the [Relationship Occurrence Persistence Design Spec](../transactions/relationship-persistence-design-spec.md).

Distinct contributions that normalize to one effective occurrence count once when duplicates are
disallowed. Retained duplicates count separately when duplicates are allowed. Provenance remains
available even when normalization reduces the count.

### 5.8 Key Conformance

For every holon `H`, `holon_key_rule(H)` selects the rule in
`EffectiveSpecification(D(H))` that governs the key of `H`.

#### DS-KEY-004: Explicit keylessness

When `holon_key_rule(H) = NoneRule.KeyRuleType`, `H` must not carry a semantic key.

#### DS-KEY-005: Key presence and value

When the selected rule is not `NoneRule.KeyRuleType`, a newly created holon must carry exactly one
key equal to the result of applying that rule to the explicit completed state of `H`. Missing,
multiple, or mismatched keys are violations.

For a persisted holon, validation uses `PersistedKey(H)` as explicit historical state. It does not
recompute that key under a later schema version merely because the effective rule has changed.

### 5.9 Conformance Results

The Holon Validator reports each independently detected violation. It does not collapse unrelated
failures into one semantic exception.

Structural dependencies still affect which checks can be evaluated. For example, lineage-cycle and
root checks require a unique parent path, and member conformance requires a uniquely bound member
descriptor. An unevaluable dependent check is not fabricated from partial semantic data.

## 6. Evaluation Order and Boundaries

### 6.1 Evaluation Order

The four jobs are documentation responsibilities, not a claim that each runs as one indivisible
phase. A conforming evaluation proceeds in dependency order:

1. resolve references and validate structural prerequisites;
2. compute lineages and effective inherited values;
3. compute effective specifications, contracts, member definitions, and other derived products;
4. validate post-computation descriptor invariants; and
5. validate every holon against the specification selected by its describing type.

This ordering lets descriptor validation consume effective definitions without making conformance
part of product computation. It also makes self-description finite.

### 6.2 Default Materialization Boundary

Default materialization belongs to creation and loading workflows, not the descriptor kernel.

For each property member in the effective conformance contract, a creation path that permits
omission as selection of a default performs the following before kernel validation:

1. preserve an explicitly supplied value;
2. otherwise materialize the effective default when the property is required and a default exists;
3. otherwise leave the property absent for conformance to evaluate; and
4. submit the resulting explicit representation to the Holon Validator.

An interactive workflow may instead present the effective default for confirmation. The semantic
requirement is that the confirmed or defaulted representation be explicit before kernel validation.

Defaults are creation-time semantics, not read-time fallback. Once materialized, a default is
ordinary state. A later descriptor change does not retroactively alter existing holons.

### 6.3 Outside the Kernel

The descriptor kernel does not own:

- TDL, JSON, or other concrete grammars;
- source-language shorthand or omission syntax;
- source conversion;
- identity and key reference transport;
- default materialization;
- persistence layout, transactions, or loader orchestration;
- diagnostic wording or source locations; or
- migration policy for existing keys and materialized values.

Equivalent explicit representations have the same semantics regardless of whether they originated
from TDL, MAP JSON, a migration, bootstrap content, or a programmatic API.

### 6.4 Kernel Outputs

The kernel supplies representation-neutral:

- descriptor-semantic validation results;
- effective inherited collections with semantic provenance;
- effective specifications, instance contracts, and member definitions;
- graph-derived `InstanceTypeKind` classification;
- classification and endpoint-compatibility predicates;
- effective key-rule selection; and
- holon-conformance results.

These outputs are computed over existing holonic representations and reference-layer operations.
They do not require a separate semantic IR or a persisted effective-descriptor representation.

### 6.5 Enforcement Traceability

Implementation staging may defer enforcement of an identified invariant, but it does not change the
normative semantics. A deferred validator may temporarily assume that loaded schema definitions
satisfy the invariant. Later validation must implement the rule as written rather than inventing a
replacement semantic.

This specification does not designate any `DS-*` rule as optional. The implementation plan's
rule-enforcement matrix is the sole authority for delivery timing and assigns both unified
descriptor-hierarchy validation and prohibition on abstract describing types to the initial
kernel/Holon Validator work. Proposed semantics that do not yet have a normative rule are identified
as proposed where discussed; they are not deferred exceptions to existing rules.

## 7. Validation Rule Index

| Rule ID | Required validation |
| --- | --- |
| `DS-STRUCT-001` | Every holon has exactly one describing type |
| `DS-STRUCT-002` | Every holon has at most one direct parent |
| `DS-STRUCT-003` | Every `Extends` lineage is acyclic |
| `DS-STRUCT-004` | Every parented lineage terminates at `TypeDescriptor` |
| `DS-STRUCT-005` | `TypeDescriptor` is the unique descriptor root |
| `DS-SCHEMA-001` | Versioned schema dependencies are acyclic |
| `DS-SCHEMA-002` | Every cross-schema reference has a direct dependency declaration |
| `DS-SCHEMA-003` | Kernel inheritance-rule table defines all non-local Core policies |
| `DS-KIND-001` | Instance-kind anchor designation is local and singular |
| `DS-KIND-002` | Every instance-kind anchor is abstract |
| `DS-KIND-003` | Only `TypeDescriptor` lacks an instance-kind anchor |
| `DS-KIND-004` | Every describing type belongs to the required category |
| `DS-KIND-005` | Descriptor holons, and only descriptor holons, use meta-type describers |
| `DS-CONTRACT-001` | Redundant inherited-member declarations are prohibited |
| `DS-CONTRACT-002` | Semantic member names are unique within each namespace |
| `DS-CONTRACT-003` | Every effective member definition is well formed |
| `DS-CONTRACT-004` | Contract members have the required instance kinds |
| `DS-DEFAULT-001` | Only required properties declare defaults |
| `DS-DEFAULT-002` | Every default conforms to its effective value definition |
| `DS-REL-001` | Declared and inverse relationship pairing is bijective |
| `DS-REL-002` | Inverse endpoints correspond to declared endpoints |
| `DS-REL-003` | Both directions declare valid deletion semantics |
| `DS-KEY-001` | Every holon type resolves exactly one instance key rule |
| `DS-KEY-002` | The selected key-rule target is compatible and executable |
| `DS-KEY-003` | The keyless root is explicit and key-rule inheritance is `Override` |
| `DS-CONSTRAINT-001` | A subtype must not relax an inherited applicable constraint |
| `DS-CONSTRAINT-002` | Every constraint attachment is applicable to the constrained descriptor's Instance TypeKind |
| `DS-CONSTRAINT-003` | Every constraint configuration conforms to its constraint type and family invariants |
| `DS-ENUM-001` | Enum member names are unique within each effective enum definition |
| `DS-ENUM-002` | Stored enum tokens match canonical member names exactly |
| `DS-ENUM-003` | Enum token changes never rewrite or alias persisted values |
| `DS-CONFORM-001` | Every direct describing type is concrete |
| `DS-CONFORM-002` | Minimum enforcement is member-specific for abstract descriptors |
| `DS-BIND-001` | Every declared property name binds uniquely |
| `DS-BIND-002` | Every declared relationship name binds uniquely |
| `DS-PROP-001` | Every enforced required property is explicitly present |
| `DS-PROP-002` | Every populated property value conforms |
| `DS-PROP-003` | Every unbound property is permitted by additional-property policy |
| `DS-OCC-001` | Relationship occurrences are grouped by resolved descriptor identity |
| `DS-OCC-002` | Every relationship source and target is endpoint-compatible |
| `DS-OCC-003` | Every relationship collection satisfies ordering and duplicate policy |
| `DS-OCC-004` | Every unbound relationship is permitted by additional-relationship policy |
| `DS-CARD-001` | Effective relationship cardinality is satisfied |
| `DS-KEY-004` | A keyless holon carries no semantic key |
| `DS-KEY-005` | A keyed new holon carries exactly the computed key |
