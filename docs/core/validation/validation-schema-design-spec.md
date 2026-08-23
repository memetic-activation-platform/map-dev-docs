# Validation Extension Schema Design Spec

## Purpose and authority

This specification defines the Validation Schema extension: the one-way Core-dependent holon
types and relationships for validation implementation, organization, result/evidence, `Validate`,
and non-Commit validation consumers.

The [Validation Architecture](validation-arch.md) owns validation layers, validator hierarchy,
execution profiles, result semantics, and PVL separation. The
[Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md) own the
representation-neutral meaning of Schema 2.0 descriptor conformance rules. This document owns the
runtime extension shape used to implement, group, invoke, and report validation rules. Core Schema
owns the rule and binding vocabulary that defines Commit acceptance.

## Package boundary

Core owns:

- `MetaValidationRule`, abstract `ValidationRule`, the Commit rule-family descriptors, and their
  Commit-semantic metadata;
- the generic additive `ValidationBindings` relationship contract; and
- MAP-seeded, initially unbound Commit rule identities.

The Validation Schema extension owns:

- `ValidationImplementation`;
- `ValidationRuleSet`;
- `ValidationResult`;
- `Validate.OperatorType` and its extension-owned affordance relationships;
- `CommandValidationRule`, `DanceValidationRule`, and `AgreementValidationRule` families;
- rule-to-implementation relationships;
- rule-set membership relationships; and
- result/evidence relationships.

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

Checks that follow directly from Core Schema-defined descriptor semantics may be represented by
MAP-seeded `ValidationRule` holons before executable support exists. A rule becomes an active,
non-optional Core commitment only when the appropriate Core type declares the compatible
occurrence of `ValidationBindings` in the same delivered capability as its handler. Applications
and extensions cannot remove or override that effective Core relationship; until it is introduced,
the unbound rule is not discovered during Commit validation.

Rust may expose typed `ValidationRule` wrappers around `HolonReference`s to ValidationRule holons.
Those wrappers provide schema-backed access to rule metadata, parameter schemas, and dispatch
inputs. They are runtime facades over holon data, not separate semantic authorities and not the
descriptor-kernel algorithms themselves.

Execution-layer and required-context compatibility belong to the implementation, not the semantic
rule. The initial built-in implementation records them in its static registry; future dynamic
resolution may represent them on `ValidationImplementation` holons.

### Core rule families and extension `Validate`

Core's `MetaValidationRule` describes validation-rule type descriptors. Core Commit rule families
do not require a `Validate` affordance: initial Commit execution uses static dispatch and is not a
schema-dispatched operator call.

The Validation Schema defines a local `Validate` operator for extension execution profiles. Its
Command, Dance, and Agreement rule families may afford that operator through extension-owned
relationships.

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

Specific families may add metadata and parameter declarations appropriate to their validation
context. For example, String validation rules and enum-value validation rules need not share the
same parameter shape merely because both specialize values.

Concrete validation rule holons should be described by the narrowest applicable rule-family
descriptor. For example, `StringLength.ValidationRule` should be described by
`StringValidationRule.HolonType`, not directly by abstract `ValidationRule.HolonType`.

### `ValidationBindings` relationships

`ValidationBindings` is the Core-owned definitional declared relationship from a type to a
compatible `ValidationRule`. Declaring it changes what Commit accepts as an instance of the type.

The generic relationship contract is available to compatible descriptor kinds, but each active
occurrence is declared on the specific applicable type. Validation discovers it through that
type's effective `available_relationships` surface. An occurrence declared generically on
`TypeDescriptor` is not a substitute for a commitment declared on the governed type.

Schema conformance must verify that the target rule family is compatible with the declaring type's
effective descriptor kind. A String-value rule, for example, cannot bind to a declared relationship
type.

A binding may carry binding-specific metadata, including:

- parameter overrides admitted by the `ValidationRule`;
- severity or blocking narrowing;
- validation profile applicability; and
- diagnostic labels or remediation context.

A binding or profile may make a rule stricter. It must not weaken the rule below the rule's
declared minimum blocking behavior or below the active profile's requirement.

### Core seed data

Core semantic checks may be represented as seeded `ValidationRule` holons before MAP implements
them. A Core rule becomes active only when its applicable Core type declares a compatible
occurrence of `ValidationBindings` in the same delivered capability as its handler.

These active commitments are authored by the MAP schema package that owns the corresponding
descriptor semantics. Effective relationship semantics make them available to specialized
descriptors through `Extends`; downstream schemas cannot remove inherited Core commitments.

The initial Core TDL contains no active `ValidationBindings` occurrences because no rule handler
has yet been implemented. A future implementation PR introduces its handler, fixtures, and the
corresponding type-specific binding together. For example, after delivering
`StringLength.ValidationRule`:

```text
MapStringValueType.StringValueType
  ValidationBindings -> StringLength.ValidationRule

PostalCode.StringValueType
  Extends -> MapStringValueType.StringValueType
  ValidationBindings -> PostalCodeFormat.ValidationRule
```

The effective relationship surface of `PostalCode.StringValueType` then includes both bindings.

## TDL corpus deliverable

The Core corpus must provide `MetaValidationRule`, abstract `ValidationRule`, the Commit families,
rule metadata, the generic `ValidationBindings` relationship contract, and MAP-seeded unbound
Commit rules.

The Validation Schema extension must provide `ValidationImplementation`, `ValidationRuleSet`,
`ValidationResult`, `Validate`, and Command/Dance/Agreement rule families with their supporting
relationships.

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
discovered through effective `ValidationBindings` relationships.

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
- The `ValidationBindings` relationship may supply descriptor-specific or profile-specific overrides.
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
`StringLength.ValidationRule` versus `StringPattern.ValidationRule`. The initial static Commit path
does not require the extension `Validate` operator; that operator remains the common execution
contract for future extension profiles. This provides:

- stable rule identity for diagnostics and future schema declarations;
- deterministic built-in execution;
- fail-closed handling for enforced or unknown unsupported mandatory rules; and
- a migration path to `ValidationImplementation` and Dance-based execution.

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
| Relationship collection policy and cardinality | Relationship / Nursery | `DS-OCC-003`, `DS-CARD-001` where graph context is available |
| Relationship descriptor pairing and deletion declarations | Relationship Descriptor | `DS-REL-*` |
| Descriptor structure, kind, and contract validity | Descriptor Holon | `DS-STRUCT-*`, `DS-KIND-*`, `DS-CONTRACT-*` |
| Default declaration validity | Descriptor Property | `DS-DEFAULT-*` |
| Schema dependency validity | Schema / Descriptor Holon | `DS-SCHEMA-*` |
| Instance key rule validity | Holon | `DS-KEY-*` |

Extension-authored `ValidationRule` holons are for additional validation commitments not already
implied by Core Schema descriptor semantics. They extend the Core rule vocabulary, use the same
type-specific `ValidationBindings` mechanism, and are added by schemas that depend on Core.

## Extension authoring

An extension author adds validation commitments by:

1. declaring a `ValidationRule` holon in a schema that depends on Core;
2. declaring an occurrence of `ValidationBindings` on the applicable type in the same delivered capability as a
   compatible handler;
3. supplying binding/profile parameters only where the rule admits them; and
4. ensuring that Commit has a compatible static handler before relying on the rule to pass Commit,
   or that an extension profile has its required `Validate` implementation.

Extension-authored mandatory rules fail closed when selected by commit-oriented validation and no
implementation is available.

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
- Exact property and relationship names for rule metadata and result evidence.
- Duplicate, override, and incompatible-rule handling for bindings collected across an `Extends`
  lineage.
- Validation profile representation and selection rules.
