# Validation Schema Design Spec

## Purpose and authority

This specification defines the Validation Schema package: the MAP schema-owned holon types,
relationships, and metadata used to express descriptor-authored validation commitments and
validation evidence.

The [Validation Architecture](validation-arch.md) owns validation layers, validator hierarchy,
execution profiles, result semantics, and PVL separation. The
[Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md) own the
representation-neutral meaning of Schema 2.0 descriptor conformance rules. This document owns the
runtime schema shape used to name, attach, group, implement, and report validation rules.

The Validation Schema is not MAP Core. MAP Core should not absorb the validation object model or
validation applicability facts. A validation-owned `ValidationBinding` holon associates one target
type descriptor with one `ValidationRule`; Core types remain owned by Core.

## Package boundary

The Validation Schema owns:

- `MetaValidationRule`;
- `ValidationRule`;
- `ValidationImplementation`;
- `ValidationRuleSet`;
- `ValidationResult`;
- `ValidationBinding` holons and their `AppliesTo` / `UsesRule` relationship descriptors;
- validation-rule metadata properties;
- rule-to-implementation relationships;
- rule-set membership relationships; and
- result/evidence relationships.

The Validation Schema source corpus includes TDL definitions for the seeded validation-owned types,
MAP-seeded core rule instances, and validation bindings. It lives in
`map-holons/schema-src/map-validation-schema.tdl`; its generated loader artifact is
`map-holons/generated/json-imports/map-validation-schema.json`. The package is
`MAP Validation Schema-v0.1.0` and explicitly depends on `MAP Core
Schema-v0.0.7`. TDL expresses these holons and
relationships as ordinary schema content; Descriptor-Aware Holon Validation gives those definitions
their runtime meaning.

The Validation Schema does not own:

- TDL syntax or source lowering;
- descriptor-kernel conformance algorithms;
- descriptor retrieval or effective-product computation;
- Holon Loading default materialization;
- Holochain Integrity callback behavior;
- descriptor-independent PVL semantics; or
- TypeActivation and governance policy.

## Core model

### ValidationRule

A `ValidationRule` is a holon that names one semantic validation condition.

It defines the commitment content, not the executable implementation. A rule may declare:

- validator level, such as Holon, Property, Value, Relationship, Transaction, Command, Dance, or
  Agreement;
- parameter schema and default parameter values;
- default severity;
- minimum blocking behavior;
- determinism and dependency classification;
- deferability; and
- remediation guidance.

Rule instances must have stable `ValidationRule` identities even when their first implementation is
a Rust method on a family-specific wrapper. Rule identity is a stable authored semantic key, such
as `RequiredPropertyPresence.ValidationRule` or `ExtensionFoo.StringPattern.ValidationRule`, not a
generated storage identity. Saved holon identity may be resolved normally, but semantic rule
identity and wrapper dispatch must remain stable across loads and schema packaging.

Checks that follow directly from Core Schema-defined descriptor semantics are represented by
MAP-seeded `ValidationRule` holons loaded with the applicable MAP schema package. They are
non-authorable in the sense that application and extension descriptor authors must not attach,
remove, replace, opt into, or opt out of them as optional commitments. They are a non-revokable base
set attached by schema load through validation-owned `ValidationBinding` holons and executed through
the same `ValidationRule` wrapper dispatch path as extension-authored rules.

Rust may expose typed `ValidationRule` wrappers around `HolonReference`s to ValidationRule holons.
Those wrappers provide schema-backed access to rule metadata, parameter schemas, and dispatch
inputs. They are runtime facades over holon data, not separate semantic authorities and not the
descriptor-kernel algorithms themselves.

Execution-layer and required-context compatibility belong to the implementation, not the semantic
rule. The initial built-in implementation records them in its static registry; future dynamic
resolution may represent them on `ValidationImplementation` holons.

### MetaValidationRule and Validate

`MetaValidationRule` is the meta-type that describes validation-rule type descriptors. It narrows
operator affordance to validation-rule descriptors rather than adding local operator affordances to
all holon-type descriptors.

The Validation Schema defines a local `Validate` operator. `ValidationRule` family descriptors
afford `Validate` through `AffordsOperator`.

Validation's `AffordsOperator` is a ValidationRule-owned relationship identity,
distinct from Core's ValueType-owned `AffordsOperator` relationship. The two
source contracts may share the forward semantic member name. Their inverses are
distinct because both are navigable from `OperatorType` by name:

- `OperatorType -[ValueTypeAffordedBy]-> ValueType` is Core-owned;
- `OperatorType -[ValidationRuleAffordedBy]-> ValidationRule` is
  Validation-owned.

This does not add a Core dependency on Validation or widen operator affordance
to general `HolonType` contracts.

Illustrative shape:

```text
MetaValidationRule.MetaHolonType
  DescribedBy MetaHolonType.MetaTypeDescriptor
  Extends MetaHolonType.MetaTypeDescriptor
  InstanceRelationships -> [
    AffordsOperator
  ]

ValidationRule.HolonType
  DescribedBy MetaValidationRule.MetaHolonType
  Extends HolonType.TypeDescriptor
  AffordsOperator -> [
    Validate.OperatorType
  ]

Validate.OperatorType
  ValidationRuleAffordedBy -> [
    ValidationRule.HolonType
  ]
```

Commands remain the client-invocation surface and Dances remain host-to-guest or host-to-host
behavior invocations. The `Validate` operator is a local execution contract for evaluating a
validation rule. The initial family-specific wrapper implementation is the first built-in
execution path for that local operator; it does not require dynamic operator or Dance dispatch.

### ValidationRule families

`ValidationRule.HolonType` is abstract. It is the root of the validation-rule hierarchy, not the
describing type for ordinary concrete rule holons. It affords the common `Validate` operator, which
concrete rule-family descriptors inherit through ordinary `AffordsOperator` additive semantics.
Concrete rule families specialize the rule shape by validator level and descriptor family.

Initial families include:

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
  CommandValidationRule.HolonType
  DanceValidationRule.HolonType
  AgreementValidationRule.HolonType
```

Specific families may add metadata and parameter declarations appropriate to their validation
context. For example, String validation rules and enum-value validation rules need not share the
same parameter shape merely because both specialize values.

Concrete validation rule holons should be described by the narrowest applicable rule-family
descriptor. For example, `StringLength.ValidationRule` should be described by
`StringValidationRule.HolonType`, not directly by abstract `ValidationRule.HolonType`.

### ValidationBinding associations

`ValidationBinding` is a validation-owned association holon, not an extension of a Core descriptor
type and not a relationship authored onto the target descriptor. Each binding has exactly one
`AppliesTo` relationship to a `TypeDescriptor` and exactly one `UsesRule` relationship to a
`ValidationRule`. The inverse relationships, `HasValidationBinding` and
`UsedByValidationBinding`, make the association traversable without changing the ownership of the
Core type or rule.

```text
ValidationBinding -[AppliesTo]-> TypeDescriptor
ValidationBinding -[UsesRule]-> ValidationRule
```

For a binding `B` with `B -[AppliesTo]-> T` and `B -[UsesRule]-> R`, the commitment is:

> Targets governed by `T` are committed to satisfy `R` when the rule is selected by a compatible
> validation layer, operation, and profile.

`T` acts as a classifier here, not as a described holon. Which target it governs follows from the
rule's validator level; the
[Validation Architecture](validation-arch.md) owns that
mapping, the collection algorithm, and the scoping rules for binding targets.

This deliberately avoids a `Validations` relationship on `T`: a Core descriptor need not be
redeclared, augmented, or made into a validation-specific subtype to acquire validation commitments.
The Validation Schema owns the association and depends on Core. The platform bootstrap co-stages
both schema corpora according to the dependency and commit model defined by the
[Validation Architecture](validation-arch.md).

A binding may carry binding-specific metadata, including:

- parameter overrides admitted by the `ValidationRule`;
- severity or blocking narrowing;
- validation profile applicability; and
- diagnostic labels or remediation context.

A binding or profile may make a rule stricter. It must not weaken the rule below the rule's
declared minimum blocking behavior or below the active profile's requirement.

### Core seed data

All core semantic checks that follow from MAP Core Schema descriptor semantics must be represented
as explicit seeded `ValidationRule` holons and explicit seeded `ValidationBinding` holons.

These seed associations are authored by the MAP schema package that owns the corresponding
descriptor semantics. They are not authored by downstream application or extension schemas.
Effective validation collection must include bindings for the target descriptor and its `Extends`
lineage, so base commitments are inherited by specialized descriptors and cannot be removed or
overridden by descendants.

Illustrative seed data:

```text
HolonTypeExactlyOneDescribedBy.ValidationBinding
  AppliesTo -> HolonType.TypeDescriptor
  UsesRule -> ExactlyOneDescribedBy.ValidationRule

PropertyTypeRequiredPresence.ValidationBinding
  AppliesTo -> PropertyType.TypeDescriptor
  UsesRule -> RequiredPropertyPresence.ValidationRule

StringLength.ValidationBinding
  AppliesTo -> StringValueType.ValueType
  UsesRule -> StringLength.ValidationRule

EnumTokenMembership.ValidationBinding
  AppliesTo -> EnumValueType.ValueType
  UsesRule -> EnumTokenMembership.ValidationRule

DeclaredRelationshipCardinality.ValidationBinding
  AppliesTo -> DeclaredRelationshipType.RelationshipType
  UsesRule -> RelationshipCardinality.ValidationRule
```

When a downstream schema defines a more specific descriptor, it adds commitments to the inherited
base set rather than restating or replacing it:

```text
PostalCode.StringValueType
  Extends -> MapStringValueType.StringValueType

PostalCodeFormat.ValidationBinding
  AppliesTo -> PostalCode.StringValueType
  UsesRule -> PostalCodeFormat.ValidationRule
```

The effective validation set for `PostalCode.StringValueType` therefore includes the inherited
MAP-seeded String rules plus `PostalCodeFormat.ValidationRule`.

## TDL seed corpus deliverable

The Validation Schema package must provide a TDL corpus that declares:

- `MetaValidationRule.MetaHolonType`;
- abstract `ValidationRule.HolonType`;
- concrete `ValidationRule` family descriptors;
- `Validate.OperatorType`;
- `ValidationBinding.HolonType` plus `AppliesTo`, `UsesRule`, and inverse relationship descriptors;
- `ValidationImplementation`, `ValidationRuleSet`, and `ValidationResult` descriptors; and
- MAP-seeded core `ValidationRule` instances plus their seeded `ValidationBinding` associations.

The corpus should be usable both as loader input and as a golden fixture for TDL/JSON round-trip
tests. It must not encode executable Rust behavior; it names the holonic rule inventory and
relationship commitments that the runtime wrapper factory recognizes.

The source corpus is `map-holons/schema-src/map-validation-schema.tdl`. It will continue to tighten
as exact property names and result-evidence shape are settled.

The design seed must maintain coverage for every stable `DS-*` rule ID listed in
[Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md). The first draft
uses one seeded `ValidationRule` holon per `DS-*` ID so coverage can be audited mechanically. Later
implementation may group Rust execution internally by rule family, but it must preserve distinct
rule identities for diagnostics, evidence, and unsupported-rule handling.

### ValidationImplementation

A `ValidationImplementation` binds a `ValidationRule` to executable behavior.

It may declare:

- implementation engine;
- module identity and hash;
- entrypoint;
- ABI;
- implementation version;
- supported validation layers and contexts;
- resource profile;
- determinism classification;
- activation status; and
- trust or capability requirements.

`ValidationImplementation` is part of the schema model, but dynamic implementation resolution is
not required for the first Descriptor-Aware Holon Validation track.

### ValidationRuleSet

A `ValidationRuleSet` is a named composition of validation rules.

Rule sets are useful for reusable authoring profiles such as import readiness, publication
readiness, schema-authoring checks, security audits, or diagnostics. They are part of the
Validation Schema model, but rule-set expansion and execution are deferred unless an initial schema
requires them.

Initial Descriptor-Aware Holon Validation operates on individual `ValidationRule` identities
collected through `ValidationBinding` associations.

### ValidationResult

A `ValidationResult` records the outcome of applying a validation rule to a target under a specific
context.

It may include:

- rule identity;
- target identity or digest;
- descriptor identity;
- validation layer;
- operation;
- implementation identity where meaningful;
- outcome;
- severity;
- blocking status;
- message;
- validation path;
- unresolved dependencies;
- timestamp where meaningful outside PVL;
- validator identity; and
- signature or attestation where durable evidence is required.

Most validation results are transient. Persisted results are reserved for durable evidence use
cases such as steward review, import reports, publication certification, audit, deferred-validation
completion, or disputes.

## Parameter model

Validation parameters are layered:

- `ValidationRule` defines the parameter schema and default parameter values.
- The `ValidationBinding` may supply descriptor-specific or profile-specific overrides.
- The target descriptor supplies domain parameters already intrinsic to its own semantics.

For example:

- `StringLengthRule` reads length boundaries from the String ValueType descriptor.
- `IntegerRangeRule` reads boundaries from the Integer ValueType descriptor.
- `RequiredPropertyRule` reads requiredness from the PropertyType descriptor.
- A publication profile may strengthen severity or blocking behavior for a rule it selects.

Binding-level or profile-level parameters must not duplicate or override descriptor-owned semantic
fields unless the rule explicitly defines that configuration point.

## Initial execution profile

The first Descriptor-Aware Holon Validation implementation uses family-specific Rust
`ValidationRule` wrappers as the built-in `Validate` implementations.

The runtime resolves the concrete rule holon and its describing rule-family descriptor, constructs
the corresponding wrapper, and invokes `wrapper.validate(context)`. The wrapper provides typed
metadata access for the rule family and dispatches internally by concrete rule key, such as
`StringLength.ValidationRule` versus `StringPattern.ValidationRule`. The afforded `Validate`
operator defines the common operation contract. This provides:

- stable rule identity for diagnostics and future schema declarations;
- deterministic built-in execution;
- fail-closed handling for enforced or unknown unsupported mandatory rules; and
- a migration path to `ValidationImplementation` and Dance-based execution.

Built-in Rust enforcement implements the selected rule for a validation context. Where validation
follows directly from Core Schema-defined descriptor semantics, the selected rule delegates
normative `DS-*` meaning to the descriptor kernel. The `ValidationRule` holon supplies the stable
rule identity, metadata, dispatch family, and diagnostics boundary; it does not become a second
source of descriptor semantics.

Core Schema-derived rules are `ValidationRule` holons, but they are not descriptor-authored
commitments. They are seeded by MAP schema loading as a non-revokable base set. For example,
exactly-one-`DescribedBy` validation is always performed before descriptor-aware validation can
discover effective contracts or additional bindings. BaseValue-vs-ValueType kind matching is
likewise always performed by the generic ValueValidator before family-specific value validation.
Required-property enforcement follows directly from property descriptor requiredness. Descriptor
authors must not be able to remove or override these guards through `ValidationBinding`.

If a mandatory rule is enforced by the active platform capability, or is not a known planned
MAP-seeded rule, lack of a compatible implementation emits `UnsupportedValidationRule` and blocks
commit.
Advisory or runtime-only rules may produce `Deferred`, `Warning`, or `NotApplicable` according to
rule metadata and profile selection.

The temporary platform capability manifest defined by the Validation Architecture permits the
short implementation rollout without changing rule metadata or consumer validation profiles.

## Schema-seeded non-authorable rule inventory

The initial Descriptor-Aware Holon Validation implementation should seed the following
Core Schema-derived `ValidationRule` holons for diagnostics, wrapper dispatch, and evidence. These
rules are attached by MAP schema loading as non-authorable base commitments, not by application or
extension descriptor authors.

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
| Relationship collection policy and cardinality | Relationship / Nursery | `DS-OCC-003`, `DS-CARD-001` where graph context is available |
| Relationship descriptor pairing and deletion declarations | Relationship Descriptor | `DS-REL-*` |
| Descriptor structure, kind, and contract validity | Descriptor Holon | `DS-STRUCT-*`, `DS-KIND-*`, `DS-CONTRACT-*` |
| Default declaration validity | Descriptor Property | `DS-DEFAULT-*` |
| Schema dependency validity | Schema / Descriptor Holon | `DS-SCHEMA-*` |
| Instance key rule validity | Holon | `DS-KEY-*` |

Extension-authored `ValidationRule` holons are for additional validation commitments not already
implied by Core Schema descriptor semantics. They use the same `ValidationBinding` and wrapper
dispatch mechanism, but they are added by extension schemas rather than by the MAP schema load.

## Extension authoring

An extension author adds validation commitments by:

1. declaring a `ValidationRule` holon in a schema that depends on the Validation Schema;
2. creating a validation-owned `ValidationBinding` that applies the rule to the applicable type
   descriptor;
3. supplying binding/profile parameters only where the rule admits them; and
4. ensuring that the target validation profile has a compatible wrapper-based `Validate`
   implementation before relying on the rule to pass commit.

Extension-authored mandatory rules fail closed when selected by commit-oriented validation and no
implementation is available.

## Deferred behavior

The following remain deferred:

- dynamic rule collection beyond the initial effective `ValidationBinding` traversal;
- dynamic `ValidationImplementation` activation and selection;
- WASM, third-party, or process-isolated validation engines;
- generic Dance-based validation dispatch;
- `ValidationRuleSet` expansion and nested rule-set semantics;
- persisted `ValidationResult` policies beyond explicit evidence use cases; and
- validation receipt acceptance rules.

## Open decisions

- Whether binding-specific metadata requires a dedicated binding descriptor shape beyond the
  initial association model.
- Exact property and relationship names for rule metadata and result evidence.
- Duplicate, override, and incompatible-rule handling for bindings collected across an `Extends`
  lineage.
- Validation profile representation and selection rules.
