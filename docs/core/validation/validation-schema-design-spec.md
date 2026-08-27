# Validation Extension Schema Design Spec

## Purpose and authority

This specification defines the Validation Schema extension: the one-way Core-dependent holon
types and relationships for validation implementation, organization, result/evidence, `Validate`,
and non-Commit validation consumers.

The [Validation Architecture](validation-arch.md) owns validation layers, validator hierarchy,
execution profiles, result semantics, and PVL separation. The
[Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md) own the
representation-neutral meaning of Schema 2.0 descriptor conformance rules. This document owns the
runtime extension shape used to implement, group, invoke, and report validation rules. The
type-system-owned `Constraints` relationship defines configured invariants; Core owns the
complementary rule and binding vocabulary for Commit obligations that are not constraints.

## Package boundary

Core owns:

- `MetaValidationRule`, abstract `ValidationRule`, and the Commit rule-family descriptors;
- the complete Commit-rule metadata closure: `ValidationLevel`, `ValidationSeverity`,
  `ValidationBlockingBehavior`, and `ValidationDeterminismClass`, including their enum variants,
  plus `ValidationLevel`, `DefaultSeverity`, `MinimumBlockingBehavior`, `DeterminismClass`,
  `SemanticAuthority`, and `ValidationRuleDescription` property descriptors;
- the generic additive `ValidationBindings` / `ValidationBindingFor` relationship pair for
  non-constraint rules; and
- the classified, initially unbound Core Commit-rule inventory.

The Validation Schema extension owns:

- `ValidationImplementation`;
- `ValidationRuleSet`;
- `ValidationResult`;
- `Validate.OperatorType` and its extension-owned affordance relationships;
- `CommandValidationRule`, `DanceValidationRule`, and `AgreementValidationRule` families;
- no VAL0b relationship contract that connects those types to rules, subjects, or one another.

The extension structurally depends on Core. Core has neither a structural dependency nor a
`load_with` dependency on the extension. The extension lives in
`map-holons/schema-src/validation/schema.tdl`; its generated loader artifact is
`map-holons/generated/json-imports/validation/schema.json`. The package is
`MAP Validation Schema-v0.1.0` and explicitly depends on `MAP Core
Schema-v0.0.7`.

The Validation Schema does not own:

- TDL syntax or source lowering;
- descriptor-kernel conformance algorithms;
- descriptor retrieval or effective-product computation;
- Holon Loading default materialization;
- Holochain Integrity callback behavior;
- descriptor-independent PVL semantics; or
- TypeActivation and governance policy.

## Core-owned rule and binding model

### ValidationRule

A Core-owned `ValidationRule` is a holon that names one semantic validation condition.

It defines the commitment content, not the executable implementation. The complete current
Core-owned metadata surface is the six property descriptors listed in the package boundary above.
Constraint parameters belong only to `Constraint` instances and their `ConstraintType` contracts.
Future remediation, profile, or execution metadata require an explicit schema-design decision;
they are not implied by this initial Core closure.

Rule instances must have stable `ValidationRule` identities even when their first implementation is
a Rust method on a family-specific wrapper. Rule identity is a stable authored semantic key, such
as `RequiredPropertyPresence.ValidationRule` or `ExtensionFoo.StringPattern.ValidationRule`, not a
generated storage identity. Saved holon identity may be resolved normally, but semantic rule
identity and wrapper dispatch must remain stable across loads and schema packaging.

Fixed or contextual checks that remain outside the configured constraint model may be represented
by MAP-seeded `ValidationRule` holons before executable support exists. A rule becomes an active,
non-optional Core commitment only when the appropriate Core type declares the compatible
occurrence of `ValidationBindings` in the same delivered capability as its handler. Applications
and extensions cannot remove or override that effective Core relationship; until it is introduced,
the unbound rule is not discovered during Commit validation. A parameterized definitional invariant
does not become a rule merely to gain a stable identity.

Rust may expose typed `ValidationRule` wrappers around `HolonReference`s to ValidationRule holons.
Those wrappers provide schema-backed access to rule metadata and dispatch inputs. They are runtime
facades over holon data, not separate semantic authorities and not the
descriptor-kernel algorithms themselves.

Execution-layer and required-context compatibility belong to the implementation, not the semantic
rule. The initial built-in implementation records them in its static registry; future dynamic
resolution may represent them on `ValidationImplementation` holons.

### Core rule families and extension `Validate`

Core's `MetaValidationRule` describes validation-rule type descriptors. Core Commit rule families
do not require a `Validate` affordance: initial Commit execution uses static dispatch and is not a
schema-dispatched operator call.

The Validation Schema defines a local `Validate` operator for future extension execution profiles.
Its Command, Dance, and Agreement rule families may eventually afford that operator through
extension-owned relationships. VAL0b declares the `AffordsOperator` /
`ValidationRuleAffordedBy` descriptor pair but authors no affordance occurrence.

Validation's `AffordsOperator` is an extension-owned relationship identity, distinct from Core's
ValueType-owned `AffordsOperator` relationship. The two source contracts may share the forward
semantic member name. Their inverses are distinct because both are navigable from `OperatorType`
by name:

- `OperatorType -[ValueTypeAffordedBy]-> ValueType` is Core-owned;
- `OperatorType -[ValidationRuleAffordedBy]-> ValidationRule` is
  Validation-owned.

This does not add a Core dependency on Validation or widen operator affordance to general
`HolonType` contracts. `Validate` is not required by the initial static Commit implementation.

### ValidationRule families

`ValidationRule.HolonType` is abstract. It is the root of the validation-rule hierarchy, not the
describing type for ordinary concrete rule holons. Core Commit families specialize the rule shape
by validator level and descriptor family; they do not inherit or require the extension's `Validate`
operator.

Core Commit families include:

```text
ValidationRule.HolonType
  HolonValidationRule.HolonType
  PropertyValidationRule.HolonType
  ValueValidationRule.HolonType
    StringValidationRule.HolonType
    IntegerValidationRule.HolonType
    BooleanValidationRule.HolonType
    EnumValueValidationRule.HolonType
    BytesValidationRule.HolonType
    ValueArrayValidationRule.HolonType
  RelationshipValidationRule.HolonType
  TransactionValidationRule.HolonType
```

The Validation Schema extension defines `CommandValidationRule.HolonType`,
`DanceValidationRule.HolonType`, and `AgreementValidationRule.HolonType`, each extending the
Core `ValidationRule` root.

Specific families may add metadata appropriate to their validation context. They do not define a
second parameter model for configured definitional constraints; string length, numeric bounds,
cardinality, and analogous parameters belong to constraint instances.

Concrete validation rule holons should be described by the narrowest applicable rule-family
descriptor. A fixed string representation rule, if retained, should be described by
`StringValidationRule.HolonType`, not directly by abstract `ValidationRule.HolonType`; configured
string length is a `Constraint`, not a `ValidationRule`.

### `ValidationBindings` relationships

`ValidationBindings` is the Core-owned declared relationship pair for non-constraint rule
commitments:

```text
TypeDescriptor -[ValidationBindings 0..*]-> ValidationRule
ValidationRule -[ValidationBindingFor 0..*]-> TypeDescriptor
```

The forward relationship is additive through `Extends`. Its generic contract is licensed once by
`MetaTypeDescriptor` through inherited `InstanceRelationships`, making it available to descriptor
kinds through ordinary inheritance. Each active forward occurrence is authored only on the concrete
governed descriptor; an occurrence on generic `TypeDescriptor` is not a commitment for all types.
Validation discovers occurrences through the governed descriptor's effective
`available_relationships` surface.

This pair replaces the superseded association model. Core defines no `ValidationBinding.HolonType`,
`AppliesTo` / `HasValidationBinding`, `UsesRule` / `UsedByValidationBinding`, or replacement
association holon.

VAL0b authors no active occurrences, so rule-family/descriptor-kind compatibility is vacuously
satisfied. The first capability that introduces one must prove both that a compatible pairing is
accepted and that an incompatible pairing fails as descriptor/schema self-conformance before
handler dispatch.

A binding may carry binding-specific metadata, including:

- severity or blocking narrowing;
- validation profile applicability; and
- diagnostic labels or remediation context.

A binding or profile may make a rule stricter. It must not weaken the rule below the rule's
declared minimum blocking behavior or below the active profile's requirement.

### Core seed data

Core seeds the classified `ValidationRule` identities that remain fixed or contextual Commit
checks after configured definitional constraints are represented through `Constraints`. A Core rule
becomes active only when its applicable Core type declares a compatible occurrence of
`ValidationBindings` in the same delivered capability as its handler.

These active commitments are authored by the MAP schema package that owns the corresponding
descriptor semantics. Effective relationship semantics make them available to specialized
descriptors through `Extends`; downstream schemas cannot remove inherited Core commitments.

The VAL0b Core TDL contains no active `ValidationBindings` occurrences because no rule handler has
yet been implemented. A future implementation PR introduces its handler, fixtures, and the
corresponding type-specific binding together. For example, after delivering a fixed required-
property rule:

```text
RequiredDisplayName.PropertyType
  ValidationBindings -> RequiredPropertyPresence.ValidationRule
```

An inherited subtype's effective relationship surface then includes that binding. Its configured
length or pattern constraints are instead separately present in its effective `Constraints`
collection.

## TDL corpus deliverable

The Core corpus must provide `MetaValidationRule`, abstract `ValidationRule`, the Commit families,
the complete six-property/four-enum metadata closure, the generic
`ValidationBindings` / `ValidationBindingFor` pair licensed through `MetaTypeDescriptor`, and the
classified unbound Core Commit rules. It must not contain a `ValidationBinding` association holon
or active binding occurrence. The Core type-system corpus separately provides `Constraint`,
`ConstraintType`, `Constraints`, applicability declarations, and every Core constraint type used by
Core definitions.

The Validation Schema extension must provide `ValidationImplementation`, `ValidationRuleSet`,
`ValidationResult`, `Validate`, and Command/Dance/Agreement rule families. VAL0b defines no
rule-to-implementation, rule-set-membership, result/evidence, or `Validate`-affordance occurrence.

The corpus should be usable both as loader input and as a golden fixture for TDL/JSON round-trip
tests. It must not encode executable Rust behavior; it names the holonic rule inventory and
relationship commitments that the runtime wrapper factory recognizes.

The Core sources and their generated JSON are canonical for Commit rule/binding vocabulary. The
extension source remains `map-holons/schema-src/validation/schema.tdl`, with generated JSON at
`map-holons/generated/json-imports/validation/schema.json`.

The design must maintain traceability for every stable `DS-*` rule ID listed in
[Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md), classifying each
under one of the five enforcement categories defined by the
  [Validation Architecture](validation-arch.md). Executable predicates retain distinct stable rule
  identities for diagnostics, evidence, and unsupported-rule handling. Kernel computations,
  coordination obligations, and evolution policies are instead audited through their owning kernel,
  workflow, or test surface; they do not require vacuous `ValidationRule` holons solely for
  one-to-one corpus coverage.

### ValidationImplementation

`ValidationImplementation` reserves a future extension surface for describing executable behavior.
VAL0b defines neither its property shape nor a relationship that selects it for a rule. Dynamic
implementation resolution is outside the first Descriptor-Aware Commit Validation track.

### ValidationRuleSet

`ValidationRuleSet` reserves a future extension surface for reusable validation organization or
profiles. VAL0b defines no membership relationship, expansion semantics, or execution behavior.
Initial Descriptor-Aware Commit Validation operates on configured constraints discovered through
effective `Constraints` relationships and individual non-constraint `ValidationRule` identities
discovered through effective `ValidationBindings` relationships.

### ValidationResult

`ValidationResult` reserves a future extension surface for durable validation evidence. VAL0b
defines no property shape, attachment relationship, persistence policy, or evidence lifecycle.
Commit uses the transient Rust `CommitValidationReport` and `CommitValidationViolation` contracts
defined by the Commit Validation Design Specification instead.

## Deferred parameter and profile model

VAL0b defines no rule parameter-schema, binding override, or profile-selection contract. String
length, integer range, cardinality, and analogous configured semantics are owned by their
constraint instances and the descriptor kernel; required-property behavior remains fixed descriptor
semantics. Any future rule parameter or profile model must define its own Core or extension
property and relationship surface explicitly; it is not implied by `ValidationRule` or
`ValidationBindings`.

## Initial execution profile

The first Descriptor-Aware Holon Validation implementation uses static dispatch keyed by concrete
constraint type for configured constraints, and family-specific Rust `ValidationRule` wrappers plus
a static registry keyed by canonical rule identity for non-constraint checks.

The runtime resolves each concrete constraint holon and its `ConstraintType`, then dispatches the
configured invariant with its parameters. Separately, it resolves the concrete non-constraint rule
holon and its describing rule-family descriptor, constructs the corresponding wrapper, and
dispatches to the registered static handler for its rule key. The initial static Commit path does
not require the extension `Validate` operator; that operator remains unoccupied in VAL0b and
reserved for future extension profiles. This provides:

- stable rule identity for diagnostics and future schema declarations;
- deterministic built-in execution;
- fail-closed handling for enforced or unknown unsupported mandatory rules; and
- a migration path to `ValidationImplementation` and Dance-based execution.

Every effective `Constraints` attachment is mandatory by virtue of that attachment; there is no
separate activation relationship analogous to `ValidationBindings`. If Commit cannot resolve a
compatible handler for its concrete `ConstraintType`, it emits a blocking
`UnsupportedConstraintType` finding and rejects the Commit. It must not ignore the attachment,
fall back to retired descriptor properties, or treat the constraint as inactive. Consequently,
strict Core bootstrap remains unavailable until handlers exist for every effective Core constraint
type used by the corpus.

Built-in Rust enforcement implements the selected rule for a validation context. Where validation
follows directly from Core Schema-defined descriptor semantics, the selected rule delegates
normative `DS-*` meaning to the descriptor kernel. The `ValidationRule` holon supplies the stable
rule identity, metadata, dispatch family, and diagnostics boundary; it does not become a second
source of descriptor semantics.

Core-derived rules may be seeded before implementation, but only an active
occurrence of `ValidationBindings` makes one part of a type's Commit contract. Descriptor
resolution is bootstrap navigation; cardinality of `DescribedBy` remains ordinary relationship
validation rather than a special hard-coded rule.

Every active mandatory binding must resolve to a compatible implementation. Failure emits
`UnsupportedValidationRule` and blocks Commit. Unbound rules do not participate in validation.

## Schema-seeded non-authorable rule inventory

Core may seed Core-derived `ValidationRule` holons for stable identity, diagnostics, and dispatch.
An entry becomes executable only when a compatible type
declares an occurrence of `ValidationBindings` targeting its implemented handler. These Core commitments are not
alterable by application or extension descriptor authors.

| Invariant area | Primary validator level | Semantic authority |
|---|---|---|
| Description and descriptor binding prerequisites | Holon | `DS-STRUCT-001`, `DS-CONFORM-001`, operation-specific no-retyping rules |
| Undescribed property policy and property binding | Holon / Property | `DS-BIND-001`, `DS-PROP-003` |
| Required property presence | Property | `DS-PROP-001` |
| Property value conformance | Property / Value | `DS-PROP-002` |
| BaseValue and selected ValueType kind matching | Generic Value | MAP-seeded value-dispatch rule |
| Core value-constraint conformance | Specific Value | Value-constraint semantics selected by the value type descriptor |
| Enum member validity | Enum Value | `DS-ENUM-*` |
| Relationship declaration and occurrence binding | Relationship | `DS-BIND-002`, `DS-OCC-001`, `DS-OCC-004` |
| Endpoint compatibility | Relationship | `DS-OCC-002` |
| Relationship collection policy | Relationship | `DS-OCC-003` |
| Configured relationship cardinality | Relationship / Nursery | Effective `CardinalityConstraint`; `DS-CARD-001` where graph context is available |
| Relationship descriptor pairing and deletion declarations | Relationship Descriptor | `DS-REL-*` |
| Descriptor structure, kind, and contract validity | Descriptor Holon | `DS-STRUCT-*`, `DS-KIND-*`, `DS-CONTRACT-*` |
| Default declaration validity | Descriptor Property | `DS-DEFAULT-*` |
| Schema dependency validity | Schema / Descriptor Holon | `DS-SCHEMA-*` |
| Instance key rule validity | Holon | `DS-KEY-*` |

### Current ValidationRule disposition

The following table is the complete disposition of the concrete rule identities in the current
Core Validation Schema corpus. “Fixed kernel” means the identity may remain available for stable
diagnostics or dispatch, but its normative semantics are the cited descriptor-kernel rule rather
than configuration on a `ValidationRule` holon. “Replaced” means the configured invariant is
represented only by the named `ConstraintType` and its attached constraint instances.

| Current identity | Disposition | Semantic authority / replacement |
| --- | --- | --- |
| `AtMostOneDirectParent.ValidationRule` | Fixed kernel | `DS-STRUCT-*` lineage integrity |
| `AcyclicExtendsLineage.ValidationRule` | Fixed kernel | `DS-STRUCT-*` lineage integrity |
| `ExtendsLineageTerminatesAtTypeDescriptor.ValidationRule` | Fixed kernel | `DS-STRUCT-*` lineage integrity |
| `UniqueTypeDescriptorRoot.ValidationRule` | Fixed kernel | `DS-STRUCT-005` |
| `SchemaDependenciesAcyclic.ValidationRule` | Fixed kernel | `DS-SCHEMA-*` |
| `CrossSchemaDependenciesDeclared.ValidationRule` | Fixed kernel | `DS-SCHEMA-*` |
| `CoreAccumulatorsAreAdditive.ValidationRule` | Fixed kernel | kernel inheritance rules |
| `LocalInstanceKindAnchorDesignation.ValidationRule` | Fixed kernel | `DS-KIND-*` |
| `InstanceKindAnchorsAreAbstract.ValidationRule` | Fixed kernel | `DS-KIND-*` |
| `TypeDescriptorRootKindException.ValidationRule` | Fixed kernel | `DS-KIND-*` |
| `DescribingCategoryCompatibility.ValidationRule` | Fixed kernel | `DS-KIND-*` |
| `DescriptorMetaTypeCorrespondence.ValidationRule` | Fixed kernel | `DS-KIND-*` |
| `NoInheritedMemberRedeclaration.ValidationRule` | Fixed kernel | kernel inheritance rules |
| `UniqueSemanticMemberNames.ValidationRule` | Fixed kernel | `DS-CONTRACT-*` |
| `WellFormedEffectiveMemberDefinitions.ValidationRule` | Fixed kernel | `DS-CONTRACT-*` |
| `ContractMemberKindCompatibility.ValidationRule` | Fixed kernel | `DS-CONTRACT-*` |
| `InheritedValueConstraintNonRelaxation.ValidationRule` | Fixed kernel | `DS-CONSTRAINT-001` |
| `DefaultsRequireRequiredProperties.ValidationRule` | Fixed kernel | `DS-DEFAULT-001` |
| `DefaultValueConformance.ValidationRule` | Fixed kernel | `DS-DEFAULT-002` |
| `InverseEndpointCorrespondence.ValidationRule` | Fixed kernel | `DS-REL-002` |
| `DirectionalDeletionDeclarations.ValidationRule` | Fixed kernel | `DS-REL-003` |
| `EffectiveKeyRuleSelection.ValidationRule` | Fixed kernel | `DS-KEY-001` |
| `KeyRuleTargetCompatibility.ValidationRule` | Fixed kernel | `DS-KEY-002` |
| `ExplicitKeylessBaseline.ValidationRule` | Fixed kernel | `DS-KEY-003` |
| `EnumMemberNamesUnique.ValidationRule` | Fixed kernel | `DS-ENUM-001` |
| `AbstractMemberMinimumEnforcement.ValidationRule` | Fixed kernel | descriptor structural minimums |
| `UniquePropertyMemberBinding.ValidationRule` | Fixed kernel | `DS-BIND-*` |
| `RelationshipOccurrenceGrouping.ValidationRule` | Fixed kernel | `DS-OCC-001` |
| `AdditionalRelationshipPolicy.ValidationRule` | Fixed kernel | `DS-OCC-004` |
| `ExplicitKeylessness.ValidationRule` | Fixed kernel | `DS-KEY-004` |
| `KeyPresenceAndValue.ValidationRule` | Fixed kernel | `DS-KEY-005` |
| `ExactlyOneDescribedBy.ValidationRule` | Fixed kernel | `DS-STRUCT-001` |
| `ConcreteDescribingType.ValidationRule` | Fixed kernel | `DS-CONFORM-001` |
| `NoUndescribedProperties.ValidationRule` | Fixed kernel | `DS-PROP-003` |
| `RequiredPropertyPresence.ValidationRule` | Fixed kernel | `DS-PROP-001` |
| `PropertyValueConformance.ValidationRule` | Fixed kernel | `DS-PROP-002` |
| `BaseValueKindMatchesString.ValidationRule` | Fixed kernel | native value-kind conformance |
| `StringLength.ValidationRule` | Replaced | `StringLengthConstraint.ConstraintType` attached to a string value type |
| `BaseValueKindMatchesInteger.ValidationRule` | Fixed kernel | native value-kind conformance |
| `IntegerRange.ValidationRule` | Replaced | `NumericRangeConstraint.ConstraintType` attached to an integer value type |
| `BaseValueKindMatchesBoolean.ValidationRule` | Fixed kernel | native value-kind conformance |
| `BaseValueKindMatchesEnum.ValidationRule` | Fixed kernel | native value-kind conformance |
| `EnumTokenMembership.ValidationRule` | Fixed kernel | enum value semantics |
| `EnumTokenNonRetroactivity.ValidationRule` | Fixed kernel | enum value semantics |
| `BaseValueKindMatchesBytes.ValidationRule` | Fixed kernel | native value-kind conformance |
| `BytesLength.ValidationRule` | Replaced | `BytesLengthConstraint.ConstraintType` attached to a bytes value type |
| `RelationshipOccurrenceBinding.ValidationRule` | Fixed kernel | `DS-BIND-002` |
| `RelationshipEndpointCompatibility.ValidationRule` | Fixed kernel | `DS-OCC-002` |
| `RelationshipCollectionPolicy.ValidationRule` | Fixed kernel | `DS-OCC-003` |
| `RelationshipCardinality.ValidationRule` | Replaced | `CardinalityConstraint.ConstraintType`; `DS-CARD-001` evaluates effective instances |
| `RelationshipDescriptorPairing.ValidationRule` | Fixed kernel | `DS-REL-001` |

The Core constraint inventory additionally introduces `ItemCountConstraint.ConstraintType` and
`UniqueItemsConstraint.ConstraintType` for configured value-array invariants. They have no
same-named current `ValidationRule` identity to retain or replace.

Extension-authored `ValidationRule` holons are for additional non-constraint validation
commitments. They extend the Core rule vocabulary, use the same type-specific
`ValidationBindings` mechanism, and are added by schemas that depend on Core. An extension-defined
configured invariant is instead an extension `ConstraintType` and constraint instance under the
type-system model.

## Extension authoring

An extension author adds non-constraint validation commitments by:

1. declaring a `ValidationRule` holon in a schema that depends on Core;
2. declaring an occurrence of `ValidationBindings` on the applicable type in the same delivered capability as a
   compatible handler;
3. supplying binding/profile parameters only where the rule admits them; and
4. ensuring that Commit has a compatible static handler before relying on the rule to pass Commit,
   or that an extension profile has its required `Validate` implementation.

Extension-authored mandatory rules fail closed when selected by commit-oriented validation and no
implementation is available.

An extension author adds a configured definitional invariant through the type-system model: define
an extension `ConstraintType`, declare its `ApplicableToDescriptorTypes`, and attach a concrete
constraint instance through `Constraints` to an extension-owned type or subtype. This requires no
new Core descriptor property or specialized relationship pair.

## Deferred behavior

The following remain deferred:

- dynamic rule collection beyond the initial effective `ValidationBindings` traversal;
- dynamic `ValidationImplementation` activation and selection;
- WASM, third-party, or process-isolated validation engines;
- generic Dance-based validation dispatch;
- `ValidationRuleSet` expansion and nested rule-set semantics;
- persisted `ValidationResult` policies beyond explicit evidence use cases; and
- validation receipt acceptance rules.

## Open decisions

- Exact relationship properties used for binding-specific metadata.
- Exact property and relationship names for the deferred extension implementation, rule-set, and
  result/evidence surfaces.
- Duplicate and override handling for active bindings collected across an `Extends` lineage.
- Validation profile representation and selection rules.
