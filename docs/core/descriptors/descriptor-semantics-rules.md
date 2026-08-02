# Descriptor-Kernel Semantic Rules (v2.0)

These rules define the representation-neutral semantics enforced by the descriptor kernel for Schema 2.0.

A creation adapter is any boundary component that converts authored, imported, migrated, or programmatically constructed input into the explicit holon representation supplied to the descriptor kernel.

Creation adapters include:

- TDL adapters;
- JSON or graph import adapters;
- schema bootstrap loaders;
- programmatic builders;
- migration tooling; and
- runtime holon-creation APIs.

```text
Authored, Imported, or Programmatic Input
        │
        ▼
Creation Adapter / Completion Stage
    • parse concrete syntax, when applicable
    • resolve identities and references
    • expand source-language shorthand, when applicable
    • determine omitted values from the bound schema
    • materialize applicable descriptor-defined defaults
    • produce an explicit holon representation
        │
        ▼
Descriptor Kernel
    • validate descriptor semantics
    • compute effective contracts
    • compute effective semantic inheritance
    • validate conformance
```

Every creation path must pass through a completion stage that materializes applicable descriptor-defined defaults before descriptor-kernel validation.

The descriptor kernel validates the resulting explicit representation against these rules. It does not inject defaults, complete omitted values, or otherwise mutate the explicit representation supplied to it.

**The descriptor kernel is purely semantic. It computes and validates; it does not transform authored representations.**

## 1. Definitions

For any holon `H`:

    D(H) = the unique target of H.DescribedBy

For any type `T`:

    parent(T)
        =
    the optional unique target of the local `Extends` relationship populated directly on `T`

If `T` has no local `Extends` target:

    parent(T)
        =
    absent

The `Extends` lineage of a type is:

    L(T)
        =
    [T, parent(T), parent(parent(T)), ...]

The lineage is self-first and ends when a type has no parent.

Therefore, if `T` has no parent:

    L(T)
        =
    [T]

`L(T)` is defined only for types. Ordinary holons do not have an `Extends` lineage. Their type-dependent semantics are resolved through `D(H)`.

For any types `actual` and `required`, define:

    SubtypeOf(actual, required)
        =
    actual Extends* required

where `Extends*` is the reflexive-transitive closure of `Extends`.

For any holon `H`, define:

    EffectiveEndpointType(H)
        =
    H,       when H is itself a type descriptor
    D(H),    otherwise

Relationship endpoint compatibility is:

    EndpointCompatible(H, requiredType)
        =
    SubtypeOf(EffectiveEndpointType(H), requiredType)

This is one endpoint rule for all holons. Meta-types govern descriptor-holon conformance;
abstract descriptor types classify descriptor holons in descriptor-to-descriptor relationships.

For any type `T`, define:

    AdmissibleDescribingType(T)
        =
    SubtypeOf(T, TypeDescriptor)

For any type `T`, define:

    LocalInstanceContract(T)

as the declarations reached directly from `T` through:

- `InstanceProperties`; and
- `InstanceRelationships`.

An instance-contract member is identified by:

- the referenced `PropertyType`, for an instance property; or
- the referenced relationship descriptor type, for an instance relationship.

For any property or relationship member `M`, let:

    InheritanceMode(M)

be the materialized property value on the property or relationship descriptor that determines semantic inheritance for values populated through `M`.

For any type `T` and member `M`:

    LocalValues(T, M)

is the set of values or relationship targets populated locally on `T` through `M`.

    EffectiveValues(T, M)

is the value set obtained by applying the semantic-inheritance mode declared by `M` across the `Extends` lineage of `T`.

## 2. Structural Validity

Every semantically valid holon has exactly one `DescribedBy` target. Zero or multiple targets are errors.

Every type has at most one direct `Extends` parent. Multiple parents are errors.

An `Extends` lineage must not repeat a node identity. Repetition is a cycle and is an error.

`Extends` is semantically a relation between types. A non-type source or target is an error.

`TypeDescriptor` is the abstract root of the unified descriptor-type hierarchy.

`MetaTypeDescriptor` extends `HolonType` and is the root of the meta-type branch. Concrete
meta-types extend within that branch and remain transitively substitutable for `HolonType` and
`TypeDescriptor`.

`RelationshipType` extends `TypeDescriptor` and is the common abstract classification root for
`DeclaredRelationshipType` and `InverseRelationshipType`.

A descriptor holon's own conformance obligations come from `D(H)`, not from the descriptor-type ancestor it extends.

There is no general `instance_type_kind` compatibility rule on an `Extends` edge. Any incompatible obligations are detected by ordinary conformance against descriptor-authored rules, not by comparing kind labels.

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
    Abstract(T) = false

## 3. Contract Resolution

`InstanceProperties` and `InstanceRelationships` are instance-contract declarations. They define what a type requires of the instances it describes.

They do not describe ordinary populated properties or relationships on the type descriptor itself.

For any type `T`:

    EffectiveInstanceContract(T)
        =
    LocalInstanceContract(T),                       if T has no parent

    EffectiveInstanceContract(parent(T))
        union
    LocalInstanceContract(T),                       otherwise

This inheritance is additive.

A subtype may add instance-contract declarations, but it does not remove, override, or shadow inherited declarations.

A subtype must not redeclare an inherited contract member in an attempt to modify:

- cardinality;
- value type;
- requirement status;
- source or target constraints; or
- validation rules.

If a local contract declaration has the same contract-member identity as an inherited declaration, contract resolution fails with an inherited-member redeclaration error.

If distinct contract-member identities in the effective instance contract claim the same semantic member name, contract resolution fails with a duplicate semantic-member declaration error.

Contract declarations are not set-deduplicated. This is distinct from set union and duplicate elimination for effective populated values under `InheritanceMode Additive`.

For any holon `H`, the contract used to validate `H` itself is:

    ConformanceContract(H)
        =
    EffectiveInstanceContract(D(H))

`DescribedBy` therefore determines the schema-defined contract that the current holon must satisfy.

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

`Extends` is defined only between types in the unified hierarchy rooted at `TypeDescriptor`.

`MetaTypeDescriptor Extends HolonType` establishes the meta-type branch without introducing a
second hierarchy. Concrete meta-types extend within that branch. Descriptor semantic categories
extend their applicable abstract descriptor parents.

Every `Extends` edge must be single-valued, acyclic, and descriptor-valid.

### 5.2 Descriptor substitutability

Subtype classification follows transitive `Extends`.

All relationship endpoints use:

    EndpointCompatible(H, requiredType)
        =
    SubtypeOf(EffectiveEndpointType(H), requiredType)

Accordingly, a relationship whose target is `TypeDescriptor` accepts any descriptor holon that
equals or transitively extends `TypeDescriptor`. A relationship whose target is `PropertyType`
accepts property descriptor holons through their own descriptor classification, while an ordinary
holon is classified through `D(H)`.

This substitutability rule is classification by lineage. It is separate from descriptor self-conformance and separate from semantic inheritance of populated values.

Descriptor holons are themselves described through the meta-type branch. Their self-conformance obligations are determined by their kind-specific describing meta-type.

For example:

    D(Book.HolonType)
        =
    MetaHolonType

Therefore, the admissibility and self-conformance of `Book.HolonType` are evaluated through `MetaHolonType`, while its classification as a descriptor type is evaluated through its descriptor-type `Extends` lineage.

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

When an input omits it, the pre-kernel creation or completion stage materializes the default before descriptor-kernel validation:

    InheritanceMode = None

There is no runtime interpretation of absence as `None`.

For a type `T` and member `M`, effective values are resolved as follows.

### 6.1 `None`

If:

    InheritanceMode(M) = None

then:

    EffectiveValues(T, M)
        =
    LocalValues(T, M)

Only locally populated values contribute to the effective semantics of `T`.

Values populated on ancestors do not contribute.

### 6.2 `Additive`

If:

    InheritanceMode(M) = Additive

and `T` has parent `P`, then:

    EffectiveValues(T, M)
        =
    EffectiveValues(P, M)
        union
    LocalValues(T, M)

If `T` has no parent:

    EffectiveValues(T, M)
        =
    LocalValues(T, M)

Additive inheritance accumulates all distinct inherited and local contributions by set union.

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
    LocalValues(T, M)

If `LocalValues(T, M)` is empty and `T` has parent `P`, then:

    EffectiveValues(T, M)
        =
    EffectiveValues(P, M)

If `LocalValues(T, M)` is empty and `T` has no parent:

    EffectiveValues(T, M)
        =
    empty set

Equivalently:

    EffectiveValues(T, M)
        =
    LocalValues(T, M),
        if LocalValues(T, M) is non-empty

    EffectiveValues(parent(T), M),
        otherwise, if parent(T) exists

    empty set,
        otherwise

Override resolution is self-first.

The first type in `L(T)` that locally populates `M` supplies the entire effective value set.

Contributions from more distant ancestors are shadowed for effective-value purposes. They are not combined with the winning contribution set.

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

## 7. Duplicate Elimination and Provenance

Additive inheritance uses set union.

If the same value or relationship target appears both locally and through inheritance, it appears once in the effective value set.

Duplicate elimination is based on the identity or equality rule defined for the relevant value kind or relationship-target kind.

Duplicate elimination must not erase contribution provenance.

For `Additive` inheritance, provenance records:

- every inherited contribution;
- every local contribution;
- the ancestor that contributed each inherited value; and
- duplicate contributions that collapse to one effective value.

For `Override` inheritance, provenance records:

- the local or nearest inherited contribution set that supplies the effective values; and
- shadowed contribution sets from more distant ancestors.

Shadowed values do not contribute to effective cardinality, but their provenance may remain available for explanation, inspection, and debugging.

The exact representation of provenance is an implementation concern. Retaining the semantic fact of contribution provenance is mandatory.

## 8. Cardinality and Constraint Evaluation

Cardinality determines how many effective values or targets a holon may have for a declared member.

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

cardinality is evaluated against the local value set.

Consequently, a required singular member must be satisfied locally. An ancestor's value does not satisfy the subtype's local requirement.

### 8.2 `Additive`

For a member with:

    InheritanceMode Additive

cardinality is evaluated against the union of inherited and local values.

Consequently, a singular member is violated if distinct inherited and local contributions produce more than one effective value.

Duplicate contributions that collapse to the same effective value count once for cardinality, while their separate provenance is retained.

### 8.3 `Override`

For a member with:

    InheritanceMode Override

cardinality is evaluated against the resolved override value set.

A locally populated value set, when present, replaces the inherited effective value set and must independently satisfy the member's cardinality and applicable constraints.

For a singular member with cardinality `1..1`, the following are valid:

- exactly one local value; or
- no local value and exactly one inherited effective value.

The following are invalid:

- more than one local value;
- no local or inherited effective value; or
- an inherited effective value set containing more than one value.

A local override is not added to the inherited value set.

If distinct contract-declaration identities with the same semantic name survive identity deduplication, contract resolution fails before conformance proceeds.

## 9. Key-Rule Resolution

`InstanceKeyRule` on a holon type governs holons described by that type. It does not govern the key
of the type descriptor holon on which it is populated.

The declared relationship:

    (HolonType.TypeDescriptor)-[InstanceKeyRule]->(KeyRuleType.HolonType)

declares:

    cardinality 1..1
    InheritanceMode Override

Only holon types participate because property values, value instances, and relationship instances
are not holons and do not have independent semantic keys.

For any holon type `T`:

    instance_key_rule(T)
        =
    the unique target in EffectiveValues(T, InstanceKeyRule)

Resolution is self-first. The first type in `L(T)` that locally populates `InstanceKeyRule`
supplies the complete effective target set. More distant targets are shadowed.

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

Key-rule resolution fails when a local or resolved effective target set contains more than one
rule, or when no local or inherited target exists.

For any holon `H`, the rule governing its key is selected by the type that describes it:

    holon_key_rule(H)
        =
    instance_key_rule(DescribingType(H))

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

`DescribedTypeRule.KeyRuleType` derives keys for named ordinary holons as:

    {local type_name}.{DescribingType(H).type_name}

`FormatRule.KeyRuleType` is a concrete holon type for reusable configured rules. Each configured
rule is an ordinary holon described by `FormatRule.KeyRuleType` and supplies `TypeName`,
`TemplateString`, and an ordered `TemplateParameters` relationship to one or more property
descriptors. For example, `ImplementationName.FormatRule` uses template `{0}` and
`ImplementationName.PropertyType` as its sole parameter.

Key-rule resolution is not a special-case inheritance algorithm. It is an ordinary application of
`InheritanceMode Override` over `InstanceKeyRule`.

## 10. Required Properties and Default Values

`DefaultValue` is a property of property-type descriptors.

`DefaultValue.PropertyType` uses `BaseValueValueType.ValueType` so its representation can contain
any runtime `BaseValue`. The default is then dependently validated against the `ValueType` selected
by the property descriptor on which `DefaultValue` is populated.

A default may be defined only for a required property:

    HasDefaultValue(P)
        implies
    IsValueRequired(P) = true

The valid combinations are:

- optional and no default: the property remains absent when omitted;
- required and no default: creation fails unless a value is supplied;
- required and defaulted: the pre-kernel creation or completion stage materializes the default before kernel validation.

Optional properties must not define defaults.

Default materialization is performed by the pre-kernel creation or completion stage for every creation path.

A conforming creation pipeline must ensure that, for every required property in the effective conformance contract:

1. If an explicit value is supplied, that value is retained.
2. Otherwise, if the effective property declaration defines a `DefaultValue`, materialize that value into the property map.
3. Otherwise, creation reports a missing-required-property violation unless the created holon is
   itself an abstract descriptor.
4. Supply the completed explicit representation to the descriptor kernel for validation.

An explicit value always takes precedence over a default.

The descriptor kernel does not perform these completion steps. It validates the explicit representation resulting from them.

A default value must satisfy the same constraints as an explicitly supplied value, including:

- value-type conformance;
- cardinality;
- range constraints;
- enumeration membership;
- representation constraints; and
- applicable validation rules.

An invalid default makes the property-type descriptor invalid.

After successful creation and validation, every required property is physically present in the
resulting property map unless the holon is itself an abstract descriptor covered by the
completeness exemption in Section 11.2.

Defaults are creation-time completion semantics, not read-time fallback semantics.

Once materialized, a default is ordinary explicit state. A later change to the descriptor's default does not implicitly alter already-created holons.

## 11. Conformance

### 11.1 Descriptor admissibility

Every typed holon must be described by a non-abstract type in the unified hierarchy rooted at
`TypeDescriptor`.

For every holon `H`:

    AdmissibleDescribingType(D(H))

and:

    Abstract(D(H)) = false

Only after descriptor admissibility is established are the descriptor's effective instance contract, property constraints, and relationship constraints evaluated.

A holon `H` conforms iff:

- `AdmissibleDescribingType(D(H))`;
- `Abstract(D(H)) = false`; and
- its populated properties and relationships satisfy `ConformanceContract(H)`.

For meta-type holons, `D(H)` belongs to the branch rooted at `MetaTypeDescriptor`, which is
admissible through `MetaTypeDescriptor Extends HolonType Extends TypeDescriptor`.

Admissibility is determined by transitive `Extends`, not by semantic name or descriptor kind.

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

An abstract descriptor holon may omit a property or relationship whose effective conformance
declaration has a positive minimum cardinality. This is a completeness exemption for the
descriptor holon's own populated state; it does not alter the effective contract that the
descriptor passes to the instances it describes.

For a descriptor holon `H`:

    EnforceConformanceMinimums(H)
        =
    not Abstract(H)

When `EnforceConformanceMinimums(H)` is false, an absent property or relationship does not violate
its required minimum. Every populated member remains subject to declaration identity, value or
endpoint constraints, maximum cardinality, and all other applicable semantic rules.

The exemption does not relax universal structural invariants. An abstract descriptor must still
have a concrete admissible describing type, belong to its schema, and satisfy single acyclic
`Extends` and all other model-wide validity rules.

Non-descriptor holons and non-abstract descriptor holons receive no completeness exemption.

### 11.3 Properties

A required property conforms only when it is present in the explicit representation supplied to
the descriptor kernel, including any default value materialized by the pre-kernel creation or
completion stage, unless the holon is an abstract descriptor covered by Section 11.2.

An undeclared property conforms only when the effective openness rule for additional properties permits it.

Every present property value must satisfy the value policy, cardinality, and applicable constraints supplied by its effective property declaration.

Enum membership uses exact string equality.

Integer minimum and maximum constraints honor their declared inclusive or exclusive boundaries.

String length constraints count Unicode grapheme clusters, representing user-perceived characters, rather than Unicode scalar values or encoded bytes.

### 11.4 Relationships

All authored relationship entries with the same semantic relationship name are treated as one relationship whose cardinality is the total effective target count.

An absent relationship has cardinality zero.

A declared relationship conforms only when its effective target count is within the declared
inclusive range. For an abstract descriptor covered by Section 11.2, an absent relationship is
exempt from the minimum bound; any populated targets remain subject to the maximum bound and all
other relationship semantics.

Every actual source and target must satisfy `EndpointCompatible` against the authoritative
relationship descriptor's abstract endpoint constraint.

Every declared and inverse relationship descriptor has a required, materialized
`DeletionSemantic`. The value is directional: it governs deletion of that descriptor's source
holon. An inverse descriptor's value is resolved independently and is not derived from its paired
declared relationship.

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
- completion of omitted values;
- persistence layout or loader internals;
- runtime transactions or storage behavior;
- diagnostic wording or source locations; or
- migration policy for previously materialized defaults.

Creation adapters and completion stages are responsible for:

- interpreting concrete source representations, when applicable;
- resolving identities and references;
- expanding source-language shorthand, when applicable;
- determining whether omission is permitted by the bound schema;
- performing semantic completion required by the creation path;
- materializing applicable default values; and
- producing an explicit holon representation for kernel validation.

This responsibility applies to every authored, imported, migrated, bootstrap, programmatic, and runtime creation path. Graph adapters are one concrete kind of creation adapter.

Completion behavior is normative wherever input omission is permitted. Creation paths must produce the same explicit semantic representation for equivalent inputs interpreted against the same schema version.

### 12.2 Descriptor-kernel responsibilities

The descriptor kernel defines the representation-neutral semantics of Schema 2.0, including:

- descriptor self-conformance;
- described-instance contracts;
- additive declaration inheritance across `Extends`;
- `SubtypeOf` classification;
- `InheritanceMode`-based semantic inheritance for `None`, `Additive`, and `Override`;
- cardinality evaluation against effective value sets;
- effective key-rule resolution; and
- descriptor-conformance validation.

These semantics are authoritative regardless of where they are invoked.

The descriptor kernel validates explicit representations. It does not complete, normalize, or mutate them.

### 12.3 Deferred kernel validation

Some Schema 2.0 invariants are part of the descriptor-kernel semantic contract but are not required to be enforced by the initial implementation.

The initial implementation may assume that loaded schema definitions satisfy these invariants.

Deferred validation currently includes:

- validation that every `Extends` participant belongs to the unified descriptor-type hierarchy;
- prohibition on concrete runtime holons being described by abstract types; and
- other schema-authoring invariants explicitly identified as deferred.

Validators may enforce additional graph-wide invariants afterward, but they must not redefine the semantics established by the descriptor kernel.
