# Descriptor-Kernel Semantic Rules (v2.0.0)

These rules define the representation-neutral semantics enforced by the descriptor kernel for Schema 2.0.

The shared Holon Validator is the reusable validation entry point. It owns validation scope,
context, rule coordination, and result accumulation, and invokes the kernel for the pure semantic
predicates and conformance algorithms defined here. The validation framework must not reimplement
these rules.

Callers supply the Holon Validator with an explicit holonic representation. How that representation
was authored or constructed is outside the kernel's semantic authority.

For Holon Loading, JSON and TDL parsers produce `LoaderRefRep`; guest loader components construct
the staged holonic representation and may materialize descriptor defaults before commit invokes
the Holon Validator. Parsers do not perform the descriptor-driven validation defined here.

```text
Explicit Holonic Representation
        │
        ▼
Holon Validator
    • select validation scope and context
    • coordinate applicable rules
    • accumulate validation results
        │
        ▼
Descriptor Kernel
    • validate descriptor semantics
    • compute effective contracts
    • compute effective semantic inheritance
    • validate conformance
```

When a creation path treats omission as selection of a descriptor-defined default, it must
materialize that value before descriptor-kernel validation. A creation path may instead require an
explicit value or human confirmation of a suggested default.

The descriptor kernel validates the resulting explicit representation against these rules. It does not inject or materialize defaults, or otherwise mutate the explicit representation supplied to it.

**The descriptor kernel is purely semantic. It computes and validates; it does not transform authored representations.**

## 1. Definitions

### Notation

Each formal term declares a semantic type signature using `Input -> Output`. A term returning
`Boolean` is a predicate and is defined with **iff**. Value-producing functions are defined with
`=`. Unary predicates use an `Is...` name where that makes their Boolean result clearer. Relational
predicates retain names such as `SubtypeOf` and `EndpointCompatible`.

These are semantic result types, not Rust API signatures. Malformed or inaccessible graph state
fails evaluation under the structural rules below.

### Validation Rule IDs

An independently testable descriptor-kernel validation has a stable rule ID of the form
`DS-<AREA>-<NUMBER>`. Rule IDs provide the implementation checklist and a durable reference for
tests, diagnostics, issues, and conformance reports. Moving a rule within this document does not
change its ID, and a retired ID is not reused.

Named definitions and resolution algorithms specify values the kernel must compute. Rule IDs
identify conditions the kernel must explicitly validate. Explanatory text states purpose and
consequences but does not replace the identified validation.

### Descriptor Hierarchy

#### D(H)

For any holon `H`:

    D : Holon -> Holon

    D(H) = the unique target of H.DescribedBy

A descriptor may be self-describing when it satisfies the same describing-type compatibility and
conformance rules as every other descriptor. Core Schema 2.0 authors
`MetaHolonType.MetaTypeDescriptor` as self-describing.

`D(H) = H` does not create semantic recursion because:

- `EffectiveInstanceContract(H)` is computed from `H` and its acyclic `Extends` lineage.
- Conformance is evaluated afterward.
- Resolving `D(H)` selects that computed contract; it does not recursively validate `H`.

No semantic rule follows `DescribedBy` transitively.

### Lineage Hierarchy

#### parent(H)

For any holon `H`:

    parent : Holon -> Optional<Holon>

    parent(H) = the optional unique target of H.Extends

#### L(H)

The `Extends` lineage of `H` is:

    L : Holon -> Sequence<Holon>

    L(H) = [H, parent(H), parent(parent(H)), ...]

The lineage is self-first and ends when a holon has no parent.

Therefore, if `H` has no parent:

    L(H) = [H]

#### IsDescriptor(H)

    IsDescriptor : Holon -> Boolean

    IsDescriptor(H)
        iff
    TypeDescriptor is a member of L(H)

This says exactly what we mean:

- A holon is a _descriptor_ if its lineage includes `TypeDescriptor`.
- `TypeDescriptor` is a descriptor because its lineage is `[TypeDescriptor]`.
- An ordinary holon without `Extends` has lineage `[H]`, which does not contain `TypeDescriptor`.
- A disconnected or cyclic `Extends` chain does not establish descriptor status and fails structural validation.

### Descriptor Classification

#### SubtypeOf(T, R)

For any holon `T` and descriptor holon `R`:

    SubtypeOf : (Holon, Holon) -> Boolean

    SubtypeOf(T, R) iff R is a member of L(T)

`T` is therefore substitutable for itself and every ancestor in its lineage. This is classification substitutability, not instance conformance; `T` conforms through `D(T)`.

#### WrapperAdmissible(T, W)

For any descriptor holon `T` and typed descriptor wrapper `W` with required category anchor
`CategoryAnchor(W)`, define:

    WrapperAdmissible : (Holon, RuntimeWrapper) -> Boolean

    WrapperAdmissible(T, W)
        iff
    SubtypeOf(T, CategoryAnchor(W))

`WrapperAdmissible(T, W)` answers whether the descriptor holon `T` may be safely narrowed to a runtime wrapper that promises the operations of a particular descriptor category. It uses only `T`'s own lineage because the wrapper represents `T`'s descriptor category, not the category of the
meta-type that describes `T`.

`WrapperAdmissible` is therefore a runtime-facing application of `SubtypeOf`, not a second form of graph classification. It is not used for relationship endpoint validation, describing-type compatibility, or conformance. The core runtime owns the available wrappers and their category anchors; this specification supplies the lineage rule by which narrowing is justified.

Descriptor identity and transitive `Extends` lineage are therefore the positive authority for descriptor-wrapper selection. A runtime `TypeKind` value, when exposed, is a derived projection of this established classification and any additional effective descriptor semantics that its shape summarizes. It is not an authored property, a conformance input, or an independent classification fact.

### Abstract Descriptors

#### IsAbstract(H)

For any holon `H`, define:

    IsAbstract : Holon -> Boolean

    IsAbstract(H)
        iff
    IsDescriptor(H)
        and
    H has the unique effective IsAbstractType value true

Completion materializes the required default of `false` for applicable concrete descriptors.
Only descriptor holons can therefore be abstract.

### Describing-Type Compatibility

Every descriptor holon has two classifications with different jobs:

- its own lineage `L(H)` determines what kind of descriptor it is; and
- the lineage of `D(H)` determines the contract that the descriptor holon itself must satisfy.

Those classifications cannot be allowed to vary independently. Otherwise, a property descriptor
could choose a holon meta-type and avoid the required property-descriptor contract, or a holon-type
descriptor could choose a property meta-type and acquire an unrelated contract.

The purpose of the following two functions is to derive the required pairing from the authored
graph. The kernel does not keep a hard-coded table saying that property types pair with property
meta-types, relationship types pair with relationship meta-types, and so on. The one deliberate
root anchor is `HolonType.TypeDescriptor`, which defines the category of descriptors permitted to
describe ordinary holons.

#### GoverningDescriptorCategory(H)

For any descriptor holon `H`:

    GoverningDescriptorCategory : Holon -> Holon

    GoverningDescriptorCategory(H)
        =
    the first abstract holon in the self-first lineage L(H)

`GoverningDescriptorCategory(H)` identifies where the descriptor family containing `H` declares
its describing-type policy. Concrete descriptors inherit that policy from the nearest abstract
category in their own lineage; the kernel must not infer the policy from a concrete descriptor's
name or declaration syntax.

For example, the governing category of `Title.PropertyType` is
`PropertyType.TypeDescriptor`. The former is a concrete property descriptor, while the latter is
the abstract category that establishes how property descriptors must themselves be described.

An abstract descriptor is its own governing category. It can therefore establish a more specific
pairing for all of its descendants. This is what makes the mechanism extensible: an extension
schema can introduce a new abstract descriptor category without adding that category to kernel
code.

#### RequiredDescribingCategory(H)

For any holon `H`, define the descriptor category required of its describing type:

    RequiredDescribingCategory : Holon -> Holon

    RequiredDescribingCategory(H)
        =
    D(GoverningDescriptorCategory(H)),    when IsDescriptor(H)
    HolonType.TypeDescriptor,             otherwise

`RequiredDescribingCategory(H)` identifies the category that `D(H)` must equal or extend. For a
descriptor holon, it follows the governing category's authored `DescribedBy` relationship to find
the paired meta-type category. For example:

    GoverningDescriptorCategory(Title.PropertyType)
        =
    PropertyType.TypeDescriptor

    RequiredDescribingCategory(Title.PropertyType)
        =
    D(PropertyType.TypeDescriptor)
        =
    MetaPropertyType.MetaTypeDescriptor

`Title.PropertyType` must therefore be described by `MetaPropertyType.MetaTypeDescriptor` or one
of its subtypes. That requirement ensures that the descriptor itself receives the property-type
contract, including `ValueType`, requiredness, defaults, and inheritance policy.

For a non-descriptor holon, the required category is the deliberately hard-coded
`HolonType.TypeDescriptor` root. This prevents an ordinary holon from being described by a
property, relationship, value, or other non-holon descriptor category. It does not constrain the
set of available holon types: any descriptor whose lineage includes `HolonType.TypeDescriptor`
remains admissible.

Together, the two functions preserve the correspondence between a descriptor's own category and
the contract selected through `DescribedBy`, while allowing the correspondence itself to remain
authored, extensible, and graph-defined.

### Contract Members and Binding

A holon's populated state and its conformance contract refer to members differently:

- populated properties and relationships are organized under compact semantic names such as
  `Title` or `AuthoredBy`; while
- the effective contract contains references to the descriptor holons that define those members,
  such as `Title.PropertyType` or the declared `AuthoredBy` relationship descriptor.

Holons are self-describing: every holon `H` selects its holon type descriptor through `D(H)`.
Property values and relationship instances are not holons and do not have their own `DescribedBy`
relationship. They therefore cannot independently select the descriptor that defines their
semantics.

To discover the characteristics of a populated property value or relationship instance, the
runtime starts with its owning or source holon, obtains that holon's `HolonDescriptor`, and looks
up the member in the holon's effective contract. That lookup returns the property or relationship
descriptor whose effective definition governs the member.

The purpose of member binding is to connect each populated name to its contract descriptor. Until
that connection is made, the validator does not know which effective member definition supplies
the value type, endpoints, cardinality, requiredness, inheritance policy, or other constraints for
the populated value or relationship occurrence.

An instance-contract member is identified by:

- the referenced `PropertyType`, for an instance property; or
- the referenced relationship descriptor type, for an instance relationship.

Descriptor identity, rather than the member name, remains authoritative after binding. Names are
the representation-level means of selecting members from a contract; they are not substitutes for
descriptor identity.

#### PropertyMemberName(P)

For any property descriptor `P`:

    PropertyMemberName : Holon -> PropertyName

    PropertyMemberName(P)
        =
    the PropertyName formed from P's required local TypeName

#### RelationshipMemberName(R)

For any declared relationship descriptor `R`:

    RelationshipMemberName : Holon -> RelationshipName

    RelationshipMemberName(R)
        =
    the RelationshipName formed from R's required local TypeName

#### Why TypeName, Not Key

`TypeName` supplies the semantic name by which a member is populated on a holon. A descriptor's
`Key` serves a different purpose: it locates or references the descriptor holon itself before
stable identity is available.

For example:

    contract declaration:    InstanceProperties -> Title.PropertyType
    populated property:      Title -> "The Dispossessed"

`Title.PropertyType` is the descriptor's lookup key. `Title` is the property member name derived
from that descriptor's local `TypeName`. Binding resolves the latter to the former's descriptor
identity and then validates the value through `EffectiveMemberDefinition(Title.PropertyType)`.

Using descriptor keys as member names would conflate lookup identity with member semantics. Keys
may incorporate information required by their key rule, such as descriptor category, immediate
parent, or relationship endpoints. That information is useful for resolving the descriptor but is
not part of the property or relationship name exposed by a holon. A key may also change when a
key-affecting schema structure changes; member syntax must not depend on the shape of the
descriptor's lookup key.

Once a contract reference has been resolved, binding and validation use the resolved descriptor
identity. The key is not repeatedly interpreted during semantic validation.

Property names and relationship names occupy separate namespaces. The same string may identify one
property member and one relationship member in the same contract without ambiguity because
properties and relationship occurrences are stored and validated as different member kinds.
Within either namespace, names are compared as exact, case-sensitive `MapString` values. The
descriptor kernel performs no case folding or Unicode normalization. A source or API adapter may
accept ergonomic spelling only by converting it to the canonical stored name before binding.

For a holon `H`, member-name binding resolves an authored or stored property or relationship name
against `ConformanceContract(H)`. A declared member must resolve to exactly one descriptor of the
corresponding kind; ambiguity is always an error. A missing binding is an error unless the
applicable additional-member policy permits an undeclared member of that kind. After successful
binding, semantic validation and occurrence grouping use the resolved descriptor identity, not the
name string. A permitted undeclared addition remains explicitly unbound and is grouped only within
its own kind by its exact stored name.

### Semantic Inheritance Collections

#### InheritanceMode(M)

For any property or relationship member `M`, let:

    InheritanceMode : Member -> InheritanceModeValue

    InheritanceMode(M)
        =
    the required singular InheritanceMode value in EffectiveMemberDefinition(M)

Completion ensures the defining local property is materialized where required by the schema;
effective member interpretation supplies the value consumed by inheritance resolution.

#### LocalValues(T, M)

For any type `T` and member `M`:

    LocalValues : (Holon, Member) -> ContributionCollection

    LocalValues(T, M)
        =
    the contribution collection populated locally on T through M

The collection retains every authored value or relationship-occurrence identity, including
duplicates, and authoritative semantic order when applicable so policy violations can be reported
before normalization.

#### EffectiveValues(T, M)

    EffectiveValues : (Holon, Member) -> EffectiveCollection

    EffectiveValues(T, M)
        =
    the policy-aware collection produced by applying InheritanceMode(M) across L(T)
    and then applying M's collection policy

#### AdditiveCombine(M, A, B)

For any member `M` and contribution collections `A` and `B`, define:

    Concatenate : (ContributionCollection, ContributionCollection)
                  -> ContributionCollection
    NormalizeForMember : (Member, ContributionCollection) -> EffectiveCollection
    AdditiveCombine : (Member, ContributionCollection, ContributionCollection)
                      -> EffectiveCollection

    AdditiveCombine(M, A, B)
        =
    NormalizeForMember(M, Concatenate(A, B))

`Concatenate(A, B)` places all contributions from `A` before all contributions from `B`.
`NormalizeForMember` applies the member's ordering and duplicate policy as defined in Section 7.

## 2. Structural Validity

### 2.1 Graph structure

#### DS-STRUCT-001: Exactly one describing type

For every holon `H`, validation passes iff the explicit representation of `H` contains exactly one
`DescribedBy` target. Zero targets and multiple targets are distinct violations of this rule.

#### DS-STRUCT-002: At most one direct parent

For every holon `H`, validation passes iff the explicit representation of `H` contains at most one
direct `Extends` target. Multiple direct targets violate this rule.

#### DS-STRUCT-003: Acyclic Extends lineage

For every holon `H`, validation passes iff no resolved holon identity occurs more than once while
traversing `L(H)`. A repeated identity identifies an `Extends` cycle and violates this rule. This
rule is evaluated only along paths for which `DS-STRUCT-002` has established a unique next parent.

#### DS-STRUCT-004: Extends lineage terminates at TypeDescriptor

For every holon `H` with a direct `Extends` parent, validation passes iff the final holon in `L(H)`
is the designated `TypeDescriptor` root. This rule is evaluated only after `DS-STRUCT-002` and
`DS-STRUCT-003` have established that the lineage is unambiguous and finite.

`TypeDescriptor` is the abstract root of the unified descriptor-type hierarchy.

`MetaTypeDescriptor` extends `HolonType` and is the root of the meta-type branch. Concrete
meta-types extend within that branch and remain transitively substitutable for `HolonType` and
`TypeDescriptor`.

`RelationshipType` extends `TypeDescriptor` and is the common abstract classification root for
`DeclaredRelationshipType` and `InverseRelationshipType`.

Cycle policy is relationship-specific:

- `Extends` is acyclic because lineage and semantic inheritance require a finite ancestor order.
- `DescribedBy` is single-valued but not transitively interpreted. Self-description and other
  cycles do not create semantic recursion; each holon is evaluated against its directly selected
  conformance contract.
- schema `DependsOn` is acyclic. Dependency closure follows this DAG with identity-based
  visitation. Multi-pass reference resolution handles forward and circular references among
  components of the same schema, not cycles between schema versions.
- declared/inverse pairing and arbitrary application relationship occurrences may form graph
  cycles unless their own descriptor-defined constraints prohibit them. Such cycles do not imply
  recursive contract inheritance; any operation that traverses them uses bounded identity-based
  visitation.

No other relation becomes cyclic or acyclic merely because the descriptor kernel traverses it. A
specialized design that requires a stronger cycle invariant must declare that invariant for the
specific relationship.

For descriptor components owned by different schemas, every authored cross-schema reference must
be covered by a direct `DependsOn` edge from the source component's schema to the target
component's schema. Reachability through a transitive dependency is sufficient for lookup but does
not satisfy this declaration invariant.

### 2.2 Describing-lineage compatibility rule

For every holon `H`:

    DescribingLineagesCompatible : Holon -> Boolean

    DescribingLineagesCompatible(H)
        iff
    when IsDescriptor(H):
        SubtypeOf(D(H), MetaTypeDescriptor.HolonType)
            and
        SubtypeOf(D(H), RequiredDescribingCategory(H))

    otherwise:
        not SubtypeOf(D(H), MetaTypeDescriptor.HolonType)
            and
        SubtypeOf(D(H), RequiredDescribingCategory(H))

`DescribingLineagesCompatible(H)` must be true.

The first case applies to descriptor holons: their describing types must belong both to the general
meta-type branch and to the more specific category paired with their governing descriptor
category.

The second case applies to ordinary holons: their describing types must belong to
`HolonType.TypeDescriptor`, as supplied by `RequiredDescribingCategory(H)`, but must not belong to
the meta-type branch. The exclusion matters because `MetaTypeDescriptor.HolonType` is itself a
subtype of `HolonType.TypeDescriptor`; without it, an ordinary holon could be described by a
meta-type.

The pairing is derived from the existing `Extends` and `DescribedBy` graph. It is not determined by
names, declaration forms, or a separately populated category label.

A descriptor holon's own conformance obligations come from `D(H)`, not from the descriptor-type ancestor it extends.

An `Extends` edge contributes directly to lineage classification. Descriptor-category compatibility
and typed-wrapper admissibility are evaluated through `SubtypeOf` and `WrapperAdmissible`, not by
comparing authored kind labels. Any incompatible conformance
obligations are detected separately against descriptor-authored contracts.

Any graph-access failure or malformed lineage fails the semantic operation. No partial lineage is a valid effective result.

An abstract type may:

- exist as a descriptor holon;
- participate in `Extends`;
- serve as the required target of relationships; and
- participate in `SubtypeOf` classification.

An abstract type may not directly describe a concrete runtime holon.

Formally:

    D(H) = T
        implies
    not IsAbstract(T)

## 3. Effective Contract and Member Interpretation

### 3.1 Instance-contract interpretation

`InstanceProperties` and `InstanceRelationships` are ordinary populated relationship members whose
targets are interpreted as instance-contract declarations. They define what a type requires of the
instances it describes.

They do not describe ordinary populated properties or relationships on the type descriptor itself.

For every populated property or relationship member `M`, propagation across `Extends` is governed
solely by `InheritanceMode(M)` and the `EffectiveValues` rules in Section 6. The descriptor kernel
does not select an inheritance algorithm from the member's semantic name or role. In particular,
it has no contract-specific inheritance branch for `InstanceProperties` or
`InstanceRelationships`.

For any type `T`:

    EffectiveInstanceContract : Holon -> Contract

    EffectiveInstanceContract(T)
        =
    the contract interpretation of:
        EffectiveValues(T, InstanceProperties)
        and
        EffectiveValues(T, InstanceRelationships)

The Core Schema declares:

    InheritanceMode(InstanceProperties) = Additive
    InheritanceMode(InstanceRelationships) = Additive

Those descriptor-defined values cause inherited and local targets of both relationships to
accumulate through ordinary `Additive` resolution. If either relationship declared another mode,
its effective targets would follow that mode instead; contract interpretation does not override
the descriptor-authored setting.

Under the Core Schema's current `Additive` settings, a subtype may add instance-contract
declarations, but it does not remove, override, or shadow inherited declarations.

A subtype must not redeclare an inherited contract member in an attempt to modify:

- cardinality;
- value type;
- requirement status;
- source or target constraints; or
- validation rules.

If a local contract declaration has the same contract-member identity as an inherited declaration,
contract interpretation fails with an inherited-member redeclaration error.

If distinct property-descriptor identities in the effective instance contract have the same
`PropertyMemberName`, or distinct relationship-descriptor identities have the same
`RelationshipMemberName`, contract interpretation fails with a duplicate member-name declaration
error in the corresponding namespace.

Contract-specific behavior begins only after generic effective-value resolution. The contract
interpreter must inspect contribution provenance before accepting the effective contract.
Identity-equal inherited and local contributions may collapse to one target during `Additive`
resolution, but that collapse must not normalize an invalid inherited-member redeclaration.
Distinct declaration identities that claim the same member name in the same namespace likewise
remain an error.

After those declaration-level checks succeed, the two effective target collections form the
effective instance contract.

For any holon `H`, the contract used to validate `H` itself is:

    ConformanceContract : Holon -> Contract

    ConformanceContract(H)
        =
    EffectiveInstanceContract(D(H))

`DescribedBy` therefore determines the schema-defined contract that the current holon must satisfy.

### 3.2 Effective member definitions

For any property or relationship descriptor `M`, define its effective member definition:

    EffectiveMemberDefinition : Holon -> MemberDefinition

    EffectiveMemberDefinition(M)
        =
    for every semantic member S in ConformanceContract(M):
        S -> EffectiveValues(M, S), with contribution provenance

`EffectiveMemberDefinition(M)` is a derived semantic view over `M` and its own `Extends` lineage.
It is not a new stored representation and does not copy effective values into `M`'s local state.

For a property descriptor, the view includes effective semantics such as:

- `ValueType`;
- `IsValueRequired`;
- `DefaultValue`;
- `InheritanceMode`; and
- the effective constraints of its selected value type.

For a relationship descriptor, the view includes effective semantics such as:

- `SourceType` and `TargetType`;
- `MinCardinality` and `MaxCardinality`;
- `IsOrdered` and `AllowsDuplicates`;
- `IsDefinitional` and `DeletionSemantic`;
- `InheritanceMode`; and
- applicable relationship constraints.

Each field is resolved by the ordinary inheritance behavior declared by that field's own descriptor.
No field is read locally merely because it participates in a member definition. Required singular
fields must resolve to exactly one effective value; optional singular fields must resolve to zero
or one; and every effective field must satisfy its own value, endpoint, collection, cardinality,
and constraint rules.

The Core Schema anchors interpretation of `InheritanceMode` itself:

    InheritanceMode(InheritanceMode.PropertyType) = None

`InheritanceMode.PropertyType` declares that value explicitly, and its required default of `None`
is materialized locally on other applicable concrete descriptors during completion. Resolving a
member's inheritance policy therefore does not require inheriting the `InheritanceMode` field from
that member's parent.

The descriptor kernel and descriptor-default materialization service consume effective member
definitions as follows:

- conformance resolves each contract member to `EffectiveMemberDefinition(M)` before validating an
  occurrence through that member;
- default materialization reads effective `IsValueRequired`, `DefaultValue`, and `ValueType` from
  the property member definition;
- inheritance reads the effective `InheritanceMode` of the populated member;
- relationship conformance reads effective endpoints, cardinality, ordering, duplicate, and
  deletion policies from the relationship member definition; and
- key-rule selection reads the effective definition of `InstanceKeyRule` before resolving its
  effective targets.

### 3.3 Evaluation strategy and termination

Semantic evaluation separates effective-product computation from holon conformance:

1. Resolve references and validate structural preconditions, including the acyclic `Extends`
   hierarchy.
2. Compute effective semantic products from the resulting graph snapshot. These products include
   lineages, effective values, effective instance contracts, effective member definitions, and
   effective key rules.
3. Validate every holon against the already computed products selected by its `DescribedBy`
   target.

Computing `EffectiveInstanceContract(T)` does not first validate `T`. Likewise, selecting
`ConformanceContract(H)` reads the effective contract of `D(H)` without recursively requesting a
conformance result for either `H` or `D(H)`. Self-description therefore selects the descriptor's
own computed contract rather than creating an unbounded validation recursion.

Within one immutable evaluation snapshot, effective products are memoized by product kind and
resolved descriptor identity. Products involving two identities, such as `EffectiveValues(T, M)`,
are memoized by the complete identity tuple. Encountering the same in-progress product dependency
again is a semantic evaluation cycle and fails unless a rule in this specification explicitly
defines that fixed point. `DescribedBy` edges do not create such product dependencies because
conformance is not part of effective-product computation.

Memoized products are snapshot-scoped. Any graph mutation, including descriptor-default
materialization, invalidates affected products; final conformance uses products computed from the
completed graph supplied to validation.

## 4. Descriptor Self-Semantics vs. Described-Instance Semantics

Schema 2.0 keeps two semantic layers separate.

For a type descriptor `T`:

1. `ConformanceContract(T)` governs the populated properties and relationships that `T` itself must contain as a descriptor holon.
2. `EffectiveInstanceContract(T)` governs the contract that `T` passes on to the instances it describes.

These are connected by `DescribedBy`, but they are not flattened into one effective surface.

In particular:

- extending `HolonType` does not by itself impose the self-conformance obligations of `MetaHolonType`;
- being described by `MetaHolonType` does not add those meta-type declarations to the ordinary instance contract of runtime holons described by `T`; and
- a type's own `InstanceProperties` and `InstanceRelationships` declarations are interpreted as declarations about described instances, not as populated state on the descriptor.

Example:

    Book.HolonType
        Extends HolonType
        DescribedBy MetaHolonType

means:

- `Book.HolonType` itself must conform to `EffectiveInstanceContract(MetaHolonType)`;
- instances described by `Book.HolonType` must conform to `EffectiveInstanceContract(Book.HolonType)`.

## 5. Type Hierarchies and Substitutability

### 5.1 Valid `Extends` relationships

`Extends` relationships form the unified hierarchy rooted at `TypeDescriptor`. Every holon that
participates in this hierarchy has an own lineage, and every such lineage must terminate at that
root.

`MetaTypeDescriptor Extends HolonType` establishes the meta-type branch without introducing a
second hierarchy. Concrete meta-types extend within that branch. Descriptor semantic categories
extend their applicable abstract descriptor parents.

Every `Extends` edge must be single-valued, acyclic, and descriptor-valid.

### 5.2 Endpoint-compatibility rule

Subtype classification follows transitive `Extends`.

The endpoint-compatibility rule is:

    EndpointCompatible : (Holon, Holon) -> Boolean

    EndpointCompatible(H, requiredType)
        iff
    requiredType is a member of L(D(H))
        or
    requiredType is a member of L(H)

For every relationship occurrence:

    source -[relationshipType]-> target

the Holon Validator requires:

    EndpointCompatible(source, SourceType(relationshipType))
    EndpointCompatible(target, TargetType(relationshipType))

This is the purpose of endpoint compatibility: it determines whether the actual source and target
holons are allowed by the relationship descriptor. It accepts subtypes rather than requiring exact
type identity, and it applies one rule uniformly to ordinary holons and descriptor holons.

The two lineage checks cover their two classification routes:

- `L(D(H))` classifies `H` as an instance of its describing type and that type's ancestors. For
  example, a holon described by `Book.HolonType` satisfies an endpoint requiring `Book.HolonType`
  or any ancestor of that type.
- `L(H)` classifies a descriptor holon through its own descriptor lineage. For example,
  `Title.PropertyType` satisfies an endpoint requiring `PropertyType.TypeDescriptor` because that
  required type is in its own lineage.

For a non-descriptor holon, `L(H) = [H]` and the second check contributes no descriptor category.

In plain language: an endpoint is compatible when the required type appears in either its
describing lineage or its own `Extends` lineage.

Endpoint compatibility does not select the contract against which `H` conforms;
`ConformanceContract(H)` is selected only through `D(H)`.

Accordingly, a relationship whose target is `TypeDescriptor` accepts any descriptor holon that
equals or transitively extends `TypeDescriptor`. A relationship whose target is `PropertyType`
accepts property descriptor holons through their own lineages. Every endpoint is also classified
through the lineage of its `DescribedBy` target.

This substitutability rule is classification by lineage. It is separate from descriptor self-conformance and separate from semantic inheritance of populated values.

Descriptor holons are themselves described through the meta-type branch. Their self-conformance obligations are determined by their kind-specific describing meta-type.

For example:

    D(Book.HolonType)
        =
    MetaHolonType

Therefore, the describing-type validity and self-conformance of `Book.HolonType` are evaluated
through `MetaHolonType`, while its classification as a descriptor type is evaluated through its
descriptor-type `Extends` lineage.

## 6. Semantic Inheritance of Populated Descriptor Members

Populated descriptor properties and relationships remain local by default.

They contribute to a subtype's effective descriptor semantics only according to the `InheritanceMode` declared by their `PropertyType` or relationship descriptor type.

The supported modes are:

    None
    Additive
    Override

`InheritanceMode` is required on:

- property-type descriptors;
- declared-relationship descriptors; and
- inverse-relationship descriptors.

When an input omits it, the pre-kernel descriptor-default materialization stage materializes the default before descriptor-kernel validation:

    InheritanceMode = None

There is no runtime interpretation of absence as `None`.

For a type `T` and member `M`, effective values are resolved as follows.

### 6.1 `None`

If:

    InheritanceMode(M) = None

then:

    EffectiveValues(T, M)
        =
    NormalizeForMember(M, LocalValues(T, M))

Only locally populated values contribute to the effective semantics of `T`.

Values populated on ancestors do not contribute.

### 6.2 `Additive`

If:

    InheritanceMode(M) = Additive

and `T` has parent `P`, then:

    EffectiveValues(T, M)
        =
    AdditiveCombine(
        M,
        EffectiveValues(P, M),
        LocalValues(T, M)
    )

If `T` has no parent:

    EffectiveValues(T, M)
        =
    NormalizeForMember(M, LocalValues(T, M))

Additive inheritance accumulates inherited contributions before local contributions. Across a
multi-level lineage, this produces root-to-self contribution order while preserving the
authoritative local order within each type's contribution collection.

`NormalizeForMember` then applies the member's collection policy. It may retain or collapse
duplicate occurrences and may preserve or discard semantic order, as defined in Section 7.

It does not imply:

- replacement;
- precedence;
- last-write-wins behavior; or
- removal of inherited values.

### 6.3 `Override`

If:

    InheritanceMode(M) = Override

and `LocalValues(T, M)` is non-empty, then:

    EffectiveValues(T, M)
        =
    NormalizeForMember(M, LocalValues(T, M))

If `LocalValues(T, M)` is empty and `T` has parent `P`, then:

    EffectiveValues(T, M)
        =
    EffectiveValues(P, M)

If `LocalValues(T, M)` is empty and `T` has no parent:

    EffectiveValues(T, M)
        =
    empty collection

Equivalently:

    EffectiveValues(T, M)
        =
    NormalizeForMember(M, LocalValues(T, M)),
        if LocalValues(T, M) is non-empty

    EffectiveValues(parent(T), M),
        otherwise, if parent(T) exists

    empty collection,
        otherwise

Override resolution is self-first.

The first type in `L(T)` that locally populates `M` supplies the entire effective collection.

Contributions from more distant ancestors are shadowed for effective-value purposes. They are not
combined with the winning contribution collection.

### 6.4 Scope

Semantic inheritance applies only when resolving the effective semantics of type descriptors across `Extends`.

It does not create general value inheritance among ordinary runtime instances.

The resulting inherited values are effective values of the subtype descriptor. They are not copied into its local descriptor state.

Example:

    HolonType
        ComponentOf CoreSchema

does not imply:

    Book.HolonType
        ComponentOf CoreSchema

when:

    InheritanceMode(ComponentOf) = None

By contrast, if:

    InheritanceMode(AffordsCommands) = Additive

then commands populated on ancestor types contribute to the effective commands of descendant types.

If:

    InheritanceMode(InstanceKeyRule) = Override

then the nearest type in the lineage that locally selects a key rule supplies the effective key rule.

## 7. Effective Collection Policy and Provenance

Effective values are policy-aware collections, not universal sets.

For relationship member `M`, `NormalizeForMember(M, contributions)` selects the effective
collection shape from `EffectiveMemberDefinition(M)`:

| `IsOrdered` | `AllowsDuplicates` | Effective collection |
| --- | --- | --- |
| `false` | `false` | set |
| `false` | `true` | multiset |
| `true` | `false` | duplicate-free sequence |
| `true` | `true` | sequence |

For a property member, the local representation supplies at most one value for that property key.
Across inheritance, identity-equal or value-equal property contributions are normalized as one
effective value while distinct contributions remain available for cardinality and constraint
evaluation.

### 7.1 Ordering

For an ordered relationship, each local contribution collection is ordered by authoritative
relationship-occurrence metadata. Incidental storage, retrieval, or serialization order is not
semantic order.

`AdditiveCombine` places the effective ancestor collection before the local collection. Recursive
resolution therefore orders contributions from the most distant effective ancestor to the current
type, preserving authoritative local order within each contributing type.

For an unordered relationship, contribution order may be retained for deterministic processing and
provenance, but it has no semantic meaning in the effective collection.

### 7.2 Duplicate handling

When duplicates are allowed, every relationship occurrence remains in the effective collection and
retains occurrence identity.

When duplicates are disallowed, normalization compares relationship targets by semantic target
identity. The first occurrence in ancestor-before-local contribution order supplies the retained
effective occurrence; later identity-equal contributions collapse into it. For an ordered
relationship, the retained occurrence also supplies the effective position.

Normalization of inherited contributions does not excuse invalid authored local state. Duplicate
local occurrences remain subject to the relationship descriptor's occurrence-conformance rules.
Contract interpretation likewise inspects provenance so an inherited-member redeclaration cannot
be hidden by duplicate normalization.

### 7.3 Provenance

Normalization must not erase contribution provenance.

For `Additive` inheritance, provenance records:

- every inherited contribution;
- every local contribution;
- the type that supplied each contribution; and
- duplicate contributions that collapse to one effective value or occurrence.

For `Override` inheritance, provenance records:

- the local or nearest inherited contribution collection that supplies the effective values; and
- shadowed contribution collections from more distant ancestors.

Shadowed values do not contribute to effective cardinality, but their provenance may remain
available for explanation, inspection, and debugging.

The exact representation of provenance is an implementation concern. Retaining the semantic fact
of contribution provenance is mandatory.

## 8. Cardinality and Constraint Evaluation

Cardinality determines how many effective values or targets a holon may have for a declared member.

The applicable cardinality and constraint policy is read from `EffectiveMemberDefinition(M)`, not
from `M`'s local state. For a property member this includes effective requiredness and value policy.
For a relationship member it includes effective minimum, maximum, ordering, duplicate, endpoint,
and constraint policy.

Cardinality does not determine whether values are inherited. Inheritance is controlled by `InheritanceMode`.

`MinCardinality` is required and must be non-negative. `MaxCardinality` is optional. An absent
maximum means the member is unbounded; no finite integer value is reserved as an unbounded
sentinel. When a maximum is present, it must be non-negative and:

    MinCardinality <= MaxCardinality

For ordinary holon validation, properties and relationships are checked against:

    ConformanceContract(H)

For descriptor-semantic evaluation of a type `T`, cardinality and value constraints are evaluated against:

    EffectiveValues(T, M)

not merely against:

    LocalValues(T, M)

This applies to all inheritance modes.

### 8.1 `None`

For a member with:

    InheritanceMode None

cardinality is evaluated against the local value collection.

Consequently, a required singular member must be satisfied locally. An ancestor's value does not satisfy the subtype's local requirement.

### 8.2 `Additive`

For a member with:

    InheritanceMode Additive

cardinality is evaluated against the normalized collection produced by combining inherited and
local contributions.

Consequently, a singular member is violated if distinct inherited and local contributions produce more than one effective value.

When duplicates are disallowed, contributions that collapse to the same effective value or target
count once while their separate provenance is retained. When duplicates are allowed, each retained
occurrence counts separately.

### 8.3 `Override`

For a member with:

    InheritanceMode Override

cardinality is evaluated against the resolved override collection.

A locally populated collection, when present, replaces the inherited effective collection and must
independently satisfy the member's cardinality and applicable constraints.

For a singular member with cardinality `1..1`, the following are valid:

- exactly one local value; or
- no local value and exactly one inherited effective value.

The following are invalid:

- more than one local value;
- no local or inherited effective value; or
- an inherited effective collection containing more than one value.

A local override is not added to the inherited effective collection.

If distinct contract-declaration identities with the same member name in the same namespace survive
identity deduplication, contract interpretation fails before conformance proceeds.

## 9. Key-Rule Resolution

`InstanceKeyRule` on a holon type governs holons described by that type. It does not govern the key
of the type descriptor holon on which it is populated.

Key-rule resolution first computes:

    EffectiveMemberDefinition(InstanceKeyRule)

The relationship's effective cardinality, target classification, collection policy, and
`InheritanceMode` are read from that definition. Its target collection for holon type `T` is then
resolved through `EffectiveValues(T, InstanceKeyRule)`.

The declared relationship:

    (HolonType.TypeDescriptor)-[InstanceKeyRule]->(KeyRuleType.HolonType)

declares:

    cardinality 1..1
    InheritanceMode Override

Only holon types participate because property values, value instances, and relationship instances
are not holons and do not have independent semantic keys.

For any holon type `T`:

    instance_key_rule : Holon -> Holon

    instance_key_rule(T)
        =
    the unique target in EffectiveValues(T, InstanceKeyRule)

Resolution is self-first. The first type in `L(T)` that locally populates `InstanceKeyRule`
supplies the complete effective target collection. More distant targets are shadowed.

The root holon type establishes explicit keylessness as the baseline:

    HolonType.TypeDescriptor
        InstanceKeyRule -> NoneRule.KeyRuleType

An extension holon type therefore describes keyless instances unless it or a nearer ancestor
overrides that target. Keylessness is never represented by an absent effective key rule.

For example:

    Entity.HolonType
        Extends HolonType.TypeDescriptor

    Book.HolonType
        Extends Entity.HolonType
        InstanceKeyRule -> TypeNameRule.KeyRuleType

produces:

    instance_key_rule(Entity.HolonType)
        =
    NoneRule.KeyRuleType

and:

    instance_key_rule(Book.HolonType)
        =
    TypeNameRule.KeyRuleType

The local `TypeNameRule.KeyRuleType` target replaces the inherited `NoneRule.KeyRuleType`; the two
targets are not combined.

Key-rule resolution fails when a local or resolved effective target collection contains more than one
rule, or when no local or inherited target exists.

For any holon `H`, the rule governing its key is selected by the type that describes it:

    holon_key_rule : Holon -> Holon

    holon_key_rule(H)
        =
    instance_key_rule(D(H))

This applies equally to ordinary holons and descriptor holons. For example:

    Book.HolonType
        DescribedBy MetaHolonType.MetaTypeDescriptor
        InstanceKeyRule -> TitleAuthor.FormatRule

`TitleAuthor.FormatRule` governs instances described by `Book.HolonType`. It does not govern the
key of the `Book.HolonType` descriptor holon. That descriptor key is governed by:

    instance_key_rule(MetaHolonType.MetaTypeDescriptor)

`MetaTypeDescriptor.HolonType` establishes `ExtendedTypeRule.KeyRuleType` as the inherited default
for descriptor holons. `ExtendedTypeRule` derives:

    {local type_name}.{immediate Extends target type_name}

It uses the immediate target's local `type_name`, not that descriptor's composed key. A descriptor
without `Extends` falls back to its local `type_name`.

Because `Extends` is definitional and contributes to descriptor semantics, changing a descriptor's
immediate parent is a key-affecting schema change under `ExtendedTypeRule`. It is not a key-stable
internal refactor for newly created descriptor versions.

`DescribedTypeRule.KeyRuleType` derives keys for named ordinary holons as:

    {local type_name}.{D(H).type_name}

`FormatRule.KeyRuleType` is a concrete holon type for reusable configured rules. Each configured
rule is an ordinary holon described by `FormatRule.KeyRuleType` and supplies `TypeName`,
`TemplateString`, and an ordered `TemplateParameters` relationship to one or more property
descriptors. For example, `ImplementationName.FormatRule` uses template `{0}` and
`ImplementationName.PropertyType` as its sole parameter.

Key-rule resolution is not a special-case inheritance algorithm. It is an ordinary application of
`InheritanceMode Override` over `InstanceKeyRule`.

### 9.1 Identity, binding scope, and key stability

A semantic key is a stored, human-meaningful lookup value. It is not holon identity. A persisted
holon is identified by `HolonId`, and a resolved relationship refers to that identity rather than
re-resolving the target's key during semantic validation.

Before identity is available, source and loader references may bind by key. Binding requires the
key to resolve to exactly one holon in the current schema package and dependency closure. Duplicate
keys in that closed scope are blocking ambiguity errors.

Schema-qualified key namespaces and coexistence of colliding local keys from independent extension
schemas belong to the deferred Extension Schema identity design. These rules do not silently infer
schema qualification or claim that the current unqualified-key model solves that problem.

For a persisted holon `H`, define:

    PersistedKey : Holon -> Optional<Key>

    PersistedKey(H)
        =
    the explicit Key value stored when that holon version was created, when present

`PersistedKey(H)` is absent for a keyless holon.

A later schema version that changes `holon_key_rule(H)`, one of its inputs, or an ancestor used by
that rule does not recompute or mutate `PersistedKey(H)`. New holons and explicitly created new
versions derive and validate their keys against the schema version bound for that creation. Any
migration or aliasing of existing keys must be explicit.

## 10. Required Properties and Default Values

`DefaultValue` is a property of property-type descriptors.

For property descriptor `P`, requiredness, value type, and default are read from:

    EffectiveMemberDefinition(P)

Accordingly, these semantics come from the effective fields of that definition, not necessarily
from values populated locally on `P`.

    IsValueRequired : Holon -> Boolean

    IsValueRequired(P)
        iff
    the effective IsValueRequired field of P is true

`DefaultValue.PropertyType` uses `BaseValueValueType.ValueType` so its representation can contain
any runtime `BaseValue`. The default is then dependently validated against the `ValueType` selected
by the property descriptor on which `DefaultValue` is populated.

A default may be defined only for a required property:

    HasDefaultValue : Holon -> Boolean

    HasDefaultValue(P)
        iff
    EffectiveMemberDefinition(P) contains a DefaultValue

    HasDefaultValue(P)
        implies
    IsValueRequired(P)

The valid combinations are:

- optional and no default: the property remains absent when omitted;
- required and no default: the Holon Validator reports a violation unless a value is supplied;
- required and defaulted: the pre-kernel descriptor-default materialization stage materializes the default before kernel validation.

Optional properties must not define defaults.

Default materialization is performed before kernel validation whenever a creation path accepts
omission as selection of a descriptor-defined default.

A conforming creation pipeline must ensure that, for every property member `P` in the effective
conformance contract, it first resolves `EffectiveMemberDefinition(P)` and then:

1. If an explicit value is supplied, that value is retained.
2. Otherwise, if the effective member definition requires the property and defines a
   `DefaultValue`, materialize that value into the property map.
3. Otherwise, leave the property absent; the Holon Validator reports a missing-required-property
   violation unless `EnforceMinimum(H, P)` is false under Section 11.2.
4. Supply the default-materialized explicit representation to the descriptor kernel for validation.

An explicit value always takes precedence over a default.

The descriptor kernel does not perform these materialization steps. It validates the explicit representation resulting from them.

A default value must satisfy the same constraints as an explicitly supplied value, including:

- value-type conformance;
- cardinality;
- range constraints;
- enumeration membership;
- representation constraints; and
- applicable validation rules.

An invalid default makes the property-type descriptor invalid.

After successful creation and validation, every property whose minimum is enforced is physically
present in the resulting property map. An absent required property is valid only for an abstract
descriptor and category-specific member for which `EnforceMinimum(H, P)` is false.

Defaults are creation-time materialization semantics, not read-time fallback semantics.

Once materialized, a default is ordinary explicit state. A later change to the descriptor's default does not implicitly alter already-created holons.

## 11. Conformance

### 11.1 Describing-type validity

Every holon must be described by a non-abstract type whose own descriptor-category lineage is
compatible with the holon it describes.

For every holon `H`:

    not IsAbstract(D(H))

and:

    DescribingLineagesCompatible(H)

Only after describing-type validity is established are the descriptor's effective instance
contract, property constraints, and relationship constraints evaluated.

A holon `H` conforms iff:

- `not IsAbstract(D(H))`; and
- `DescribingLineagesCompatible(H)`; and
- its populated properties and relationships satisfy `ConformanceContract(H)`.

For meta-type holons, `D(H)` belongs to the branch rooted at `MetaTypeDescriptor`, as required by
the describing-lineage compatibility rule.

Describing-type validity is determined by the paired `Extends` lineages, not by semantic names or
descriptor-kind labels.

For a descriptor holon, kind-specific self-conformance is determined through its describing meta-type.

For example:

    Book.HolonType
        DescribedBy MetaHolonType

means that `Book.HolonType` must satisfy:

    EffectiveInstanceContract(MetaHolonType)

This meta-type self-conformance is distinct from the descriptor-type classification established by:

    Book.HolonType
        Extends HolonType
        Extends* TypeDescriptor

### 11.2 Abstract descriptor completeness

Every concrete meta-type inherits the effective instance contract of
`MetaTypeDescriptor.HolonType`. Define that graph-derived baseline as:

    UniversalDescriptorContract : Contract

    UniversalDescriptorContract
        =
    EffectiveInstanceContract(MetaTypeDescriptor.HolonType)

For any contract member `M`:

    UniversalDescriptorMember : Member -> Boolean

    UniversalDescriptorMember(M)
        iff
    M is a member of UniversalDescriptorContract

This baseline includes the universal descriptor structure inherited by every concrete meta-type,
including `DescribedBy` and `ComponentOf`. A category-specific member is one added by a concrete
or abstract meta-type below that baseline, such as `ValueType` in the property-descriptor contract.

For any holon `H` and member `M` in `ConformanceContract(H)`, define:

    EnforceMinimum : (Holon, Member) -> Boolean

    EnforceMinimum(H, M)
        iff
    not IsAbstract(H)
        or
    UniversalDescriptorMember(M)

An abstract descriptor may therefore omit a category-specific property or relationship whose
effective definition has a positive minimum cardinality. It may not omit a universally required
member. This exemption concerns only the descriptor holon's own populated state; it does not alter
the effective contract that the descriptor passes to the instances it describes.

When `EnforceMinimum(H, M)` is false, absence of `M` does not violate its required minimum. Every
populated member remains subject to declaration identity, value or endpoint constraints, maximum
cardinality, and all other applicable semantic rules.

Structural validity is evaluated independently of this predicate. Every abstract descriptor must
still have exactly one concrete lineage-compatible `DescribedBy` target, belong to exactly one
schema through `ComponentOf`, and satisfy optional-single-parent acyclic `Extends` and all other
model-wide validity rules.

Non-descriptor holons and non-abstract descriptor holons receive no completeness exemption.

### 11.3 Properties

Each declared populated property name is first bound to one property descriptor `P` in
`ConformanceContract(H)`. All subsequent declared-property conformance uses that resolved
descriptor identity and consumes `EffectiveMemberDefinition(P)`. A name with no binding is handled
only as a permitted undeclared addition under the effective additional-property policy.

A property that is required by that effective definition conforms only when it is present in the
explicit representation supplied to the descriptor kernel, including any default value materialized
by the pre-kernel descriptor-default materialization stage, unless the holon is an abstract
descriptor for which `EnforceMinimum(H, P)` is false.

An undeclared property conforms only when the effective openness rule for additional properties permits it.

Every present property value must satisfy the value type, cardinality, and applicable constraints
supplied by `EffectiveMemberDefinition(P)`.

Enum membership uses exact string equality.

Integer minimum and maximum constraints honor their declared inclusive or exclusive boundaries.

String length constraints count Unicode grapheme clusters, representing user-perceived characters, rather than Unicode scalar values or encoded bytes.

### 11.4 Relationships

Each declared populated relationship name is first bound to one relationship descriptor `R` in
`ConformanceContract(H)`. All subsequent declared-relationship conformance and occurrence grouping
use that resolved descriptor identity and consume `EffectiveMemberDefinition(R)`. A name with no
binding is handled only as a permitted undeclared addition under the effective
additional-relationship policy.

For every declared relationship descriptor `R` and its paired inverse `I`, descriptor validity
requires:

    SourceType(I) = TargetType(R)
    TargetType(I) = SourceType(R)

These comparisons use the effective member definition of each direction. Directional cardinalities
need not match; each is evaluated per source over its direction of the shared occurrence graph.

All relationship occurrences bound to the same resolved relationship descriptor identity are
treated as one relationship whose cardinality is the total effective target count. Name resolution
does not remain as a second grouping rule after binding. Permitted undeclared relationship
occurrences have no descriptor identity and are grouped by exact stored name within the
relationship namespace.

An absent relationship has cardinality zero.

A declared relationship conforms only when its effective target count is within the effective
minimum and maximum supplied by `EffectiveMemberDefinition(R)`. For an abstract descriptor covered
by Section 11.2, an absent relationship is exempt from the minimum bound only when
`EnforceMinimum(H, R)` is false; any populated targets remain subject to the maximum bound and all
other relationship semantics.

Every actual source and target must satisfy `EndpointCompatible` against the authoritative
endpoint constraints supplied by `EffectiveMemberDefinition(R)`.

Every declared and inverse relationship descriptor has a required effective `DeletionSemantic`.
An inverse descriptor's value is resolved independently through its effective member definition
and is not derived from its paired declared relationship. The descriptor kernel validates the
presence and value type of both fields. Pairwise deletion execution, including `Block` and
`Cascade` interaction, remains proposed in the relationship-constraints specification and is not
settled by this rule.

An undeclared relationship conforms only when the effective openness rule for additional relationships permits it.

### 11.5 Violations

Conformance reports each independently detected violation.

It does not collapse multiple violations into one aggregate semantic exception.

## 12. Explicit Boundaries

### 12.1 Outside the descriptor kernel

The descriptor kernel does not define or apply:

- TDL, JSON, or other concrete source grammars;
- source-language shorthand or omission syntax;
- default materialization;
- materialization of omitted defaults;
- persistence layout or loader internals;
- runtime transactions or storage behavior;
- diagnostic wording or source locations; or
- migration policy for previously materialized defaults or persisted keys.

Creation paths that permit omission and descriptor-default materialization are responsible for:

- interpreting concrete source representations, when applicable;
- resolving identities and references;
- expanding source-language shorthand, when applicable;
- determining whether omission is permitted by the bound schema;
- performing descriptor-default materialization required by the creation path;
- materializing applicable default values; and
- producing an explicit holon representation for kernel validation.

This responsibility applies to any authored, imported, migrated, bootstrap, programmatic, or
runtime path that treats omission as selection of a descriptor-defined default.

Descriptor-default materialization behavior is normative wherever omission selects a default.
Creation paths must produce the same explicit holonic representation for equivalent confirmed or
defaulted inputs interpreted against the same schema version.

### 12.2 Descriptor-kernel responsibilities

The descriptor kernel defines the representation-neutral semantics of Schema 2.0, including:

- descriptor self-conformance;
- described-instance contracts;
- additive declaration inheritance across `Extends`;
- `SubtypeOf` classification;
- `InheritanceMode`-based semantic inheritance for `None`, `Additive`, and `Override`;
- cardinality evaluation against effective value collections;
- effective key-rule resolution; and
- descriptor-conformance validation.

These semantics are authoritative regardless of where they are invoked.

The descriptor kernel validates explicit representations. It does not materialize defaults, normalize, or mutate them.

### 12.3 Deferred kernel validation

Some Schema 2.0 invariants are part of the descriptor-kernel semantic contract but are not required to be enforced by the initial implementation.

The initial implementation may assume that loaded schema definitions satisfy these invariants.

Deferred validation currently includes:

- validation that every `Extends` participant belongs to the unified descriptor-type hierarchy;
- prohibition on concrete runtime holons being described by abstract types; and
- other schema-authoring invariants explicitly identified as deferred.

Validators may enforce additional graph-wide invariants afterward, but they must not redefine the semantics established by the descriptor kernel.
