# MAP Validation Architecture (v2.0)

> **Status:** Draft
>
> This document defines the overall MAP validation architecture. It describes the validation guarantees, validation layers, validator hierarchy, validation contexts, declarative rule model, execution profiles, results, and end-to-end validation flows.
>
> The deterministic Peer Validation Layer is specified separately in the **PVL Design Specification**, which is authoritative for Integrity Zome validation behavior, supported operations, dependency handling, deterministic execution, and resource bounds.

---

## 1. Purpose and Scope

MAP requires validation at several architectural layers with different guarantees, dependencies, and execution constraints.

This document defines:

- the validation guarantee model
- the boundaries between validation layers
- the distinction between validation layers and validator kinds
- the validator delegation hierarchy
- level-specific validation contexts
- validation rules as first-class holons
- descriptor-declared validation commitments
- validation-rule implementation and dispatch
- Promise Theory and Dance alignment
- validation results, receipts, and evidence
- end-to-end validation flows
- the transition from built-in validation to declarative extensibility

This document depends on separate specifications for:

- Peer Validation Layer design
- EffectiveDescriptor structure and compilation
- Type activation and runtime recognition
- transaction and Nursery behavior
- Dance dispatch and DanceImplementation binding
- TrustChannel and agreement semantics

This document does not define:

- the detailed PVL execution contract
- numeric PVL resource limits
- EffectiveDescriptor payload encoding
- TypeActivation governance
- RoleAccessDescriptor behavior
- TrustChannel protocol behavior
- social attestation or dispute-resolution processes

---

## 2. Architectural Principles

### 2.1 Validation is layered

No single validation environment has enough context, authority, or determinism to perform every validation.

Validation rules belong in the innermost layer capable of evaluating them safely and correctly.

Rules move outward as their dependencies become:

- less bounded
- less deterministic
- more contextual
- more temporal
- more social
- more dependent on open-world state

### 2.2 Validation is rule-driven

Each distinct validation concern is represented conceptually as a validation rule.

Examples include:

- required property presence
- prohibition of undescribed properties
- value-kind conformance
- string-length constraints
- legal enum variants
- relationship target-type conformance
- relationship cardinality
- transaction coherence

A validator orchestrates the rules applicable at its validation level and delegates narrower concerns to more specialized validators.

### 2.3 Validation rules are semantic objects

A validation rule is not identical to the Rust function, WASM module, or Dance implementation that executes it.

The rule defines the semantic condition to evaluate.

An implementation defines how that condition is evaluated in a particular execution environment.

This separation allows a single rule to have:

- a built-in Rust implementation
- a PVL-safe compiled implementation
- a runtime WASM implementation
- a diagnostic implementation
- a human-review implementation

### 2.4 Validation is declaratively extensible

The long-term MAP design represents validation rules, rule sets, implementations, and results as holons.

Type descriptors declare which validation rules apply to their instances.

Meta-types contribute the starter set of validation rules for their type kind. Concrete descriptors inherit those rules compositionally and may add more specific rules.

### 2.5 Validation execution is context-dependent

Not every validation rule may execute in every layer.

A rule must be compatible with:

- the available validation context
- the execution engine
- determinism requirements
- dependency bounds
- authority and trust requirements
- resource limits

### 2.6 Peer validity is not global truth

Peer validation proves only what every validating peer can deterministically reproduce.

It does not prove:

- current type activation
- global uniqueness
- social legitimacy
- agreement compliance
- relationship cardinality over an open graph
- absence of conflicting data
- truth of open-world assertions

### 2.7 Validation outcomes are evidence

A validation result records that a rule was evaluated under a particular context and produced an outcome.

A result does not automatically prove that:

- the rule was appropriate
- the implementation was trustworthy
- the input context was complete
- the result remains current
- every peer can reproduce it

---

## 3. Validation Guarantee Model

MAP distinguishes several validation guarantees.

### 3.1 Descriptor-Relative Structural Validity

Descriptor-relative validation establishes:

> The object conforms to the descriptor artifact against which it was validated.

This may include:

- required properties
- permitted properties
- value-kind conformance
- value constraints
- local relationship typing
- abstract or non-instantiable type rejection

Descriptor-relative validity does not establish that the descriptor is currently recognized or socially legitimate.

### 3.2 Peer Admissibility

Peer validation establishes:

> The DHT operation satisfies the deterministic integrity rules compiled into the DNA.

This is the responsibility of the Peer Validation Layer.

Peer admissibility may include descriptor-relative validation where the PVL Design Specification permits it.

### 3.3 Transaction-Local Semantic Validity

Nursery validation establishes:

> The staged transaction satisfies the rules that can be evaluated against the staged transaction and an available local snapshot.

This may include:

- relationship cardinality
- required relationships
- multi-holon consistency
- duplicate detection
- command preconditions
- Dance preconditions

Nursery validation is pre-commit protection for honest coordinators. It is not peer consensus.

### 3.4 Runtime Recognition

Runtime recognition establishes:

> The current AgentSpace recognizes the descriptor and data under its current activation and governance state.

Recognition is:

- temporal
- revocable
- AgentSpace-specific
- governance-mediated

It must not be conflated with immutable peer validation.

### 3.5 Agreement and Access Validity

Agreement-layer validation establishes:

> The requested access, projection, or behavior is permitted by the applicable agreement, role, capability, and TrustChannel context.

This validation belongs outside PVL.

### 3.6 Social or Attested Validity

Social and attestation layers may establish:

> A recognized agent or process has asserted, reviewed, approved, disputed, or resolved a claim.

These processes may provide important evidence but are not deterministic peer validation.

---

## 4. Validation Layers

Validation layers describe **where validation executes** and **what context is available**.

They are distinct from validator kinds, which describe **what is being validated**.

| Layer | Context Available | Primary Guarantee |
|---|---|---|
| Peer Validation Layer | DHT operation, Integrity context, fixed constants, bounded deterministic dependencies | Peer admissibility |
| Nursery | Staged transaction, referenced staged objects, local snapshot, coordinator services | Transaction-local semantic validity |
| Runtime Recognition | Activated descriptor set, runtime reads, AgentSpace state | Current recognition |
| Application | Application state, workflow context, command or Dance context | Domain-specific validity |
| Trust and Agreement | Agreement, role, capability, TrustChannel context | Access and projection validity |
| Attestation and Social | Agents, attestations, review and dispute processes | Social evidence and resolution |

### 4.1 Peer Validation Layer

The Peer Validation Layer is the deterministic validation kernel executed inside the Integrity Zome.

PVL:

- validates DHT admissibility
- runs only bounded and deterministic rules
- does not use general runtime services
- does not execute arbitrary validation Dances
- does not resolve open-world graph state
- rejects unsupported required semantics

The authoritative specification is the **PVL Design Specification**.

This architecture document identifies PVL as one validation layer but does not duplicate its execution rules, dependency model, or resource limits.

### 4.2 Nursery Validation

Nursery validation operates before commit against a staged transaction.

It may evaluate:

- transaction-wide consistency
- required relationships
- relationship cardinality
- multi-holon dependencies
- duplicate detection
- command preconditions
- Dance preconditions
- activation-aware descriptor selection
- dynamic or extensible validation rules
- warnings and advisory checks

Nursery validation may use the Reference Layer and other coordinator-side services unavailable to PVL.

### 4.3 Runtime Recognition and Validation

Runtime validation operates when data is read, navigated, projected, or used.

It includes:

- activation filtering
- quarantine or diagnostic classification
- view-specific validity
- stale-validation detection
- optional revalidation
- advisory checks

Structurally valid but unrecognized data may exist on the DHT. Normal runtime APIs may hide it while diagnostic APIs expose it explicitly.

### 4.4 Application Validation

Applications may define additional rules associated with:

- workflows
- forms
- commands
- publication processes
- domain semantics
- user-interface feedback
- application-specific consistency

Application validation must not be mistaken for peer consensus.

### 4.5 Trust and Agreement Validation

Trust and agreement validation may consider:

- participant identity
- agreement membership
- roles
- capabilities
- disclosure permissions
- projection policies
- TrustChannel constraints
- exfiltration controls

### 4.6 Attestation and Social Validation

Social validation may involve:

- human review
- steward approval
- signed attestations
- reputation
- dispute resolution
- governance decisions

These processes are open-world and may not be deterministic.

---

## 5. Two Orthogonal Dimensions

MAP validation has two independent dimensions.

### 5.1 Execution Layer

The execution layer identifies where validation runs:

- PVL
- Nursery
- runtime
- application
- trust and agreement
- social and attestation

### 5.2 Validator Hierarchy

The validator hierarchy identifies the object or semantic level being validated:

- Holon
- Property
- generic ValueType
- specific ValueType
- Relationship
- Transaction
- Command
- Dance
- Agreement

A validator is not inherently a PVL validator or Nursery validator.

Its suitability for a layer depends on:

- the rule being executed
- the validation context supplied
- dependency requirements
- determinism classification
- resource limits
- available implementation

For example, the same conceptual `StringLengthRule` may be:

- executed by a built-in PVL implementation
- executed by Nursery during import
- executed by a client for immediate form feedback

---

## 6. Validator Architecture

Validators orchestrate validation at a particular semantic level.

Each validator:

1. receives a level-specific validation context
2. invokes the applicable validation rules for that level
3. accumulates structured results
4. delegates narrower concerns to the next validator level
5. stops or continues according to rule outcome and orchestration policy

The core delegation hierarchy is:

    HolonValidator
        PropertyValidator
            ValueValidator
                StringValueValidator
                IntegerValueValidator
                BooleanValueValidator
                EnumValueValidator
                BytesValueValidator
        RelationshipValidator

Additional validators may operate alongside this hierarchy:

    TransactionValidator
    CommandValidator
    DanceValidator
    AgreementValidator

---

## 7. Validation Traits and Contexts

The following Rust definitions are architectural sketches. Concrete ownership, lifetime, reference, and result types may differ in implementation.

### 7.1 Shared Types

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub enum ValidationOperation {
        Create,
        Update,
        Delete,
        Import,
        Read,
        Execute,
    }

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub enum ValidationLayer {
        PeerValidation,
        Nursery,
        Runtime,
        Application,
        TrustAgreement,
        Attestation,
    }

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub enum ValidationSeverity {
        Error,
        Warning,
        Information,
    }

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    pub enum ValidationOutcome {
        Valid,
        Invalid,
        Warning,
        Deferred,
        UnresolvedDependencies,
        NotApplicable,
    }

    #[derive(Debug, Clone, PartialEq, Eq)]
    pub struct ValidationResult {
        pub rule_id: ValidationRuleId,
        pub outcome: ValidationOutcome,
        pub severity: ValidationSeverity,
        pub message: String,
        pub path: Option<ValidationPath>,
    }

A validation call may return multiple results because one validator may execute several rules.

### 7.2 Holon-Level Validation

#### Trait

    pub trait HolonValidationRule {
        fn validate(
            &self,
            context: &HolonValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct HolonValidationContext<'a> {
        pub holon: &'a Holon,
        pub descriptor: &'a Holon,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

The descriptor is represented as a holon because TypeDescriptors are themselves holons in the MAP type system. Implementations may use a typed descriptor view where available.

#### Responsibilities

The HolonValidator:

- invokes holon-level validation rules
- obtains the property descriptors applicable to the holon
- delegates each described property to the PropertyValidator
- delegates relationships to the RelationshipValidator where the execution layer supports relationship validation
- aggregates all resulting ValidationResults

#### Initial Holon-Level Rules

##### `IsDescribedRule`

Verifies that the holon is associated with a valid concrete type descriptor.

If the descriptor cannot be established, descriptor-dependent validation cannot continue.

Depending on the execution layer, the outcome may be:

- `Invalid`
- `UnresolvedDependencies`
- `Deferred`

##### `NoUndescribedPropertiesRule`

Verifies that every property present in the holon's property map has a corresponding property descriptor in the holon's effective descriptor.

The rule may respect an explicit descriptor-defined open-property policy where supported.

##### `IsInstantiableRule`

Rejects instances described by an abstract or otherwise non-instantiable type.

##### `DescriptorBindingRule`

Where applicable, verifies that the holon's descriptor identity is correctly bound and that operation-specific descriptor-binding rules are satisfied.

Examples include preventing retyping through an ordinary update.

#### Delegation

After holon-level rules execute, the HolonValidator iterates through the property descriptors rather than only the properties that happen to be present.

This ensures that missing required properties are still presented to the PropertyValidator.

For each described property, it constructs a PropertyValidationContext containing:

- the property name
- the optional property value
- the property descriptor
- the parent holon
- operation and layer information

### 7.3 Property-Level Validation

#### Trait

    pub trait PropertyValidationRule {
        fn validate(
            &self,
            context: &PropertyValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct PropertyValidationContext<'a> {
        pub property_name: &'a PropertyName,
        pub property_value: Option<&'a PropertyValue>,
        pub property_descriptor: &'a Holon,
        pub parent_holon: &'a Holon,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

#### Responsibilities

The PropertyValidator:

- determines whether a required property is present
- performs other property-level checks
- delegates a present value to the generic ValueValidator
- remains agnostic about string, integer, enum, boolean, and bytes semantics

The PropertyValidator does not independently check whether the runtime value variant matches the declared ValueType kind. That responsibility belongs to the generic ValueValidator.

#### Initial Property-Level Rules

##### `RequiredPropertyRule`

Verifies that a property declared as required has a present value.

The rule must use the MAP-defined semantics for:

- absent property
- present property with no value
- explicit null, if supported
- empty but valid scalar values

An optional property with no value does not delegate to the ValueValidator.

#### Delegation

When a property value is present, the PropertyValidator:

1. resolves the property's ValueType descriptor
2. constructs a ValueValidationContext
3. delegates to the generic ValueValidator

### 7.4 Generic ValueType Validation

#### Trait

    pub trait ValueValidationRule {
        fn validate(
            &self,
            context: &ValueValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct ValueValidationContext<'a> {
        pub value: &'a PropertyValue,
        pub value_type_descriptor: &'a Holon,
        pub parent_property_descriptor: &'a Holon,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

#### Responsibilities

The generic ValueValidator:

- verifies that the actual BaseValue variant matches the ValueType kind declared by the descriptor
- resolves the appropriate type-specific validator
- delegates only when the value kind matches
- rejects unsupported required value semantics

#### Initial Generic Value-Level Rules

##### `PropertyValueTypeRule`

Compares the actual BaseValue variant with the ValueType kind represented by the ValueType descriptor.

Examples:

- `BaseValue::StringValue` requires a String ValueType descriptor
- `BaseValue::IntegerValue` requires an Integer ValueType descriptor
- `BaseValue::BooleanValue` requires a Boolean ValueType descriptor
- `BaseValue::EnumValue` requires an Enum ValueType descriptor
- `BaseValue::BytesValue` requires a Bytes ValueType descriptor

When the actual value kind does not match:

- the rule emits an error
- type-specific validation is not invoked

#### Delegation

When value-kind conformance succeeds, the ValueValidator delegates to the validator for the specific ValueType kind.

### 7.5 String Value Validation

#### Trait

    pub trait StringValueValidationRule {
        fn validate(
            &self,
            context: &StringValueValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct StringValueValidationContext<'a> {
        pub value: &'a MapString,
        pub descriptor: &'a Holon,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

#### Initial Rules

##### `StringLengthRule`

Verifies that the string length falls within the minimum and maximum limits defined by the String ValueType descriptor.

The specification must define whether length is measured in:

- bytes
- Unicode scalar values
- grapheme clusters

PVL-safe execution must use the fixed measurement defined by the PVL specification.

##### `StringFormatRule`

Verifies a deterministic format constraint supported by the descriptor and execution layer.

Possible examples include:

- fixed key shape
- restricted character set
- deterministic pattern subset

General-purpose regular-expression execution must not be assumed PVL-safe.

##### `StringNormalizationRule`

Where required, verifies that the value uses the expected normalization form.

This rule may be included only where normalization behavior is deterministic and consistently implemented.

### 7.6 Integer Value Validation

#### Trait

    pub trait IntegerValueValidationRule {
        fn validate(
            &self,
            context: &IntegerValueValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct IntegerValueValidationContext<'a> {
        pub value: &'a MapInteger,
        pub descriptor: &'a Holon,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

#### Initial Rules

##### `IntegerRangeRule`

Verifies that the supplied integer falls within the inclusive or exclusive minimum and maximum bounds defined by the Integer ValueType descriptor.

Boundary semantics must be explicit.

### 7.7 Boolean Value Validation

#### Trait

    pub trait BooleanValueValidationRule {
        fn validate(
            &self,
            context: &BooleanValueValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct BooleanValueValidationContext<'a> {
        pub value: &'a MapBoolean,
        pub descriptor: &'a Holon,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

Boolean values may require no type-specific rule beyond generic value-kind conformance unless a descriptor introduces contextual restrictions.

### 7.8 Enum Value Validation

#### Trait

    pub trait EnumValueValidationRule {
        fn validate(
            &self,
            context: &EnumValueValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct EnumValueValidationContext<'a> {
        pub value: &'a MapEnumValue,
        pub descriptor: &'a Holon,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

#### Initial Rules

##### `LegalEnumVariantRule`

Verifies that the supplied enum value matches a variant declared by the Enum ValueType descriptor.

Variant comparison must use the canonical enum identity or canonical serialized value defined by the type system.

### 7.9 Bytes Value Validation

#### Trait

    pub trait BytesValueValidationRule {
        fn validate(
            &self,
            context: &BytesValueValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct BytesValueValidationContext<'a> {
        pub value: &'a MapBytes,
        pub descriptor: &'a Holon,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

#### Initial Rules

##### `BytesLengthRule`

Verifies that the byte sequence falls within the minimum and maximum lengths defined by the Bytes ValueType descriptor.

##### `BytesFormatRule`

Where applicable, verifies a deterministic content-format constraint.

Format interpretation that depends on external libraries, mutable standards, or unbounded parsing may be restricted to Nursery or higher layers.

### 7.10 Relationship Validation

#### Trait

    pub trait RelationshipValidationRule {
        fn validate(
            &self,
            context: &RelationshipValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct RelationshipValidationContext<'a> {
        pub relationship_name: &'a RelationshipName,
        pub relationship_descriptor: &'a Holon,
        pub source_holon: &'a Holon,
        pub target_holon: Option<&'a Holon>,
        pub operation: ValidationOperation,
        pub layer: ValidationLayer,
    }

#### Initial Relationship-Level Rules

##### `DeclaredRelationshipRule`

Verifies that the relationship is declared for the source holon's type.

##### `SourceTypeConformanceRule`

Verifies that the source holon's concrete type conforms to the relationship descriptor's declared SourceType.

##### `TargetTypeConformanceRule`

Verifies that the target holon's concrete type conforms to the relationship descriptor's declared TargetType.

##### `RelationshipCardinalityRule`

Verifies minimum and maximum cardinality.

This rule generally requires transaction or graph context and therefore normally belongs to Nursery or runtime validation rather than op-local PVL.

##### `RequiredRelationshipRule`

Verifies that a required outbound or inbound relationship exists.

This rule generally requires Nursery or runtime context.

##### `RelationshipUniquenessRule`

Verifies relationship-level uniqueness or exclusivity where the required graph context is available.

### 7.11 Transaction Validation

#### Trait

    pub trait TransactionValidationRule {
        fn validate(
            &self,
            context: &TransactionValidationContext,
        ) -> Vec<ValidationResult>;
    }

#### Context

    pub struct TransactionValidationContext<'a> {
        pub transaction: &'a StagedTransaction,
        pub snapshot: &'a ValidationSnapshot,
        pub layer: ValidationLayer,
    }

#### Initial Transaction-Level Rules

Possible transaction rules include:

- cross-holon coherence
- relationship cardinality after transaction application
- required related-object creation
- duplicate detection
- command preconditions
- transaction dependency closure
- incompatible operation detection
- staged update conflict detection

These rules belong primarily to Nursery validation.

---

## 8. Validation Rule Model

### 8.1 `ValidationRule`

A `ValidationRule` holon defines one semantic validation condition.

A rule may describe:

- what is checked
- the validator level at which it operates
- required context
- default severity
- determinism characteristics
- dependency characteristics
- whether failure blocks an operation
- whether the rule may be deferred
- human-readable remediation guidance

Illustrative shape:

    {
      "key": "RequiredProperty.Rule",
      "type": "#ValidationRule",
      "properties": {
        "display_name": "Required Property",
        "description": "A required property must have a value.",
        "validation_level": "Property",
        "default_severity": "Error",
        "determinism_class": "Deterministic"
      }
    }

The rule identifies the semantic check. It does not contain executable implementation details.

### 8.2 `ValidationImplementation`

A `ValidationImplementation` holon binds a ValidationRule to executable behavior.

Illustrative properties include:

- engine
- entrypoint
- ABI
- implementation version
- module identity
- module hash
- resource profile
- PVL-safety classification
- activation status

Illustrative relationships include:

- `ImplementsRule`
- `SupportsContext`
- `AffordingType`
- `SupersedesImplementation`

A single ValidationRule may have multiple implementations.

### 8.3 `ValidationRuleSet`

A `ValidationRuleSet` is a reusable named composition of validation rules.

Rule sets are useful where rules must be grouped independently of descriptor inheritance.

Examples include:

- import validation profile
- publication-readiness profile
- strict security profile
- schema-authoring profile
- diagnostic profile

Illustrative shape:

    {
      "key": "StandardHolonRules.RuleSet",
      "type": "#ValidationRuleSet",
      "relationships": {
        "IncludesRule": [
          { "$ref": "#IsDescribed.Rule" },
          { "$ref": "#NoUndescribedProperties.Rule" }
        ]
      }
    }

Rule sets are optional. Descriptor-declared validations remain the primary applicability mechanism.

### 8.4 `ValidationResult`

A `ValidationResult` records the outcome of applying a rule or rule set to a target under a defined context.

A result may include:

- rule identity
- target identity or digest
- descriptor identity
- validation layer
- operation
- implementation identity
- engine identity
- outcome
- severity
- message
- validation path
- unresolved dependencies
- timestamp where meaningful outside PVL
- validator identity
- signature or attestation

ValidationResults may be transient or persisted.

---

## 9. Integration with the MAP Type System

### 9.1 Descriptor-Declared Validations

Type descriptors will eventually declare rules through a relationship such as:

    <TypeDescriptor> —InstanceValidations→ <ValidationRule>

The relationship means:

> Instances described by this TypeDescriptor are subject to this validation rule when evaluated in a compatible validation layer.

### 9.2 Meta-Type Starter Rules

Meta-types declare the starter set of rules appropriate to their type kind.

Examples:

- MetaHolonType contributes holon-level rules
- MetaPropertyType contributes property-level rules
- MetaValueType contributes generic value-level rules
- MetaStringValueType contributes string-specific rules
- MetaIntegerValueType contributes integer-specific rules
- MetaEnumValueType contributes enum-specific rules
- MetaRelationshipType contributes relationship-level rules

### 9.3 Compositional Inheritance

The effective validation set for a concrete TypeDescriptor is derived compositionally from:

1. validations contributed by its meta-type
2. validations contributed by inherited or extended descriptors
3. validations declared directly by the concrete descriptor
4. optional validation profiles selected by the execution context

The combination algorithm must define:

- duplicate rule handling
- rule identity
- precedence
- replacement or override semantics
- incompatible rule detection
- parameter inheritance

### 9.4 Rule Parameters

Rules may be generic and obtain their parameters from the descriptor being validated.

For example:

- `StringLengthRule` reads minimum and maximum length from a String ValueType descriptor
- `IntegerRangeRule` reads minimum and maximum values from an Integer ValueType descriptor
- `RequiredPropertyRule` reads required or optional status from a PropertyType descriptor

This avoids creating a separate ValidationRule holon for every distinct numeric constraint.

### 9.5 Rule Applicability

The descriptor's `InstanceValidations` relationship is the primary source of rule applicability.

An optional `AppliesTo` relationship on a ValidationRule may document compatible target kinds or descriptors, but it should not compete with descriptor-declared membership as the primary dispatch source.

---

## 10. Execution Profiles

The architecture supports several execution profiles.

### 10.1 Initial Built-In Rust Profile

The initial implementation uses:

- Rust validation traits
- level-specific validation contexts
- built-in Rust rule implementations
- hard-coded invocation order
- hard-coded delegation between validators
- no general Dance dispatch
- no dynamic module loading

For example:

    pub fn validate_holon(
        context: &HolonValidationContext,
    ) -> Vec<ValidationResult> {
        let mut validation_results = Vec::new();

        validation_results.extend(
            IsDescribedRule.validate(context)
        );

        validation_results.extend(
            NoUndescribedPropertiesRule.validate(context)
        );

        validation_results.extend(
            validate_described_properties(context)
        );

        validation_results
    }

The exact Rust organization may use:

- zero-sized rule structs
- functions
- static arrays
- match-based constructor dispatch
- enum-based dispatch

The architectural requirement is that each validation check remains a distinct rule even when invocation is hard-coded.

### 10.2 Descriptor-Driven Built-In Profile

The next stage resolves rule identities from the descriptor's effective validation set but still dispatches only to built-in Rust implementations.

Illustrative dispatch:

    pub fn construct_property_validation_rule(
        validation_rule_id: &ValidationRuleId,
    ) -> Result<Box<dyn PropertyValidationRule>, ValidationError> {
        match validation_rule_id.as_str() {
            "RequiredProperty.Rule" => {
                Ok(Box::new(RequiredPropertyRule))
            }
            _ => Err(
                ValidationError::UnsupportedValidationRule(
                    validation_rule_id.clone(),
                ),
            ),
        }
    }

This is effectively constructor dispatch:

1. resolve the rule holon
2. identify the rule
3. construct the built-in Rust implementation
4. invoke it with the level-specific context

### 10.3 Runtime Dance Profile

Nursery and higher layers may eventually execute validations through standardized Dances.

In this profile:

1. the descriptor declares a ValidationRule
2. the runtime resolves an active ValidationImplementation
3. the implementation advertises a compatible validation Dance
4. the dispatcher constructs a validation request
5. the implementation performs the Dance
6. the response is converted to one or more ValidationResults

PVL must not depend on this general runtime dispatch mechanism.

### 10.4 Human or Social Validation Profile

Some rules may require:

- steward review
- peer attestation
- approval workflow
- dispute resolution
- human judgment

These rules may use Dances and ValidationResults but are not deterministic structural validators.

---

## 11. Dance Alignment

### 11.1 Validation as a Dance

Validation dispatch may be modeled as a specialized Dance.

A validation request contains:

- rule identity
- target identity or target value
- validation context
- descriptor identity
- requested result format

The response contains:

- outcome
- severity
- messages
- validation path
- evidence
- unresolved dependencies

### 11.2 `Validate` DanceType

A standard `Validate` DanceType may define the general validation protocol.

More specialized DanceTypes may exist for:

- ValidateHolon
- ValidateProperty
- ValidateValue
- ValidateRelationship
- ValidateTransaction
- ValidateImport
- ReviewValidationResult

### 11.3 Rule and Implementation Separation

The relationship is:

    ValidationRule
        defines what condition is evaluated

    ValidationImplementation
        defines how the condition is evaluated

    Validate Dance
        defines how the evaluation is requested and returned

    ValidationResult
        records the outcome

### 11.4 PVL Restriction

PVL may execute code compiled into the Integrity Zome that implements known ValidationRules.

PVL does not:

- resolve arbitrary DanceImplementations
- load dynamic modules
- execute coordinator Dances
- consult runtime activation state
- invoke application services

---

## 12. Promise Theory Alignment

The Promise Theory interpretation must distinguish the rule from the promiser.

### 12.1 ValidationRule as Commitment Content

A ValidationRule expresses the content of a validation commitment:

> Evaluate condition X against target Y using context Z.

The rule itself is not necessarily an autonomous promiser.

### 12.2 Descriptor Commitment

When a TypeDescriptor declares:

    <TypeDescriptor> —InstanceValidations→ <ValidationRule>

the descriptor commits instances of that type to the rule's validation contract.

### 12.3 Implementation Promise

A ValidationImplementation promises:

> I can evaluate ValidationRule X using execution contract Y under conditions Z.

The promise may include:

- supported validation context
- supported engine
- resource requirements
- determinism classification
- version
- activation scope

### 12.4 Dance as Enactment

The validation Dance is the enactment of the implementation promise.

### 12.5 ValidationResult as Evidence

A ValidationResult provides evidence that:

- the validation was requested
- a particular implementation evaluated it
- a particular outcome was returned

It does not automatically prove the semantic correctness of the result.

### 12.6 Membrane and Trust Boundaries

AgentSpaces may govern:

- which ValidationRules are recognized
- which implementations are active
- which validators are trusted
- which results are accepted as evidence
- which validation profiles are mandatory
- which externally authored modules may execute

---

## 13. Rule Execution and Orchestration

### 13.1 Invocation Order

Within a validator level, rule invocation order should be deterministic where one rule may affect whether subsequent rules can run.

Typical order:

1. prerequisite and descriptor-resolution rules
2. structural rules
3. type-conformance rules
4. constraint rules
5. advisory rules
6. delegation

### 13.2 Short-Circuiting

Some failures prevent meaningful downstream validation.

Examples:

- no descriptor is available
- the value kind does not match the ValueType kind
- an unsupported descriptor format is encountered
- required dependencies are unresolved

Rules should declare or imply whether failure:

- stops the validator
- stops only delegation
- allows independent rules to continue
- produces a deferred result

### 13.3 Aggregation

Validators should aggregate independent failures where practical.

For example, a holon may report several missing required properties in one validation run.

### 13.4 Operation Awareness

Validation contexts include the operation because some rules differ across:

- create
- update
- delete
- import
- read
- execute

Examples include:

- descriptor binding may be fixed across update
- delete may require different relationship checks
- import may allow deferred external references
- read-time validation may produce warnings rather than commit-blocking errors

### 13.5 Layer Awareness

Validation contexts include the validation layer so that implementations can:

- reject unsupported execution environments
- alter result classification where permitted
- determine whether unresolved dependencies are deferrable
- select appropriate evidence behavior

Layer awareness must not allow PVL rules to become nondeterministic.

---

## 14. Validation Results, Receipts, and Evidence

### 14.1 Transient Results

Most validation executions return transient ValidationResult values.

Examples include:

- form feedback
- import errors
- Nursery commit rejection
- runtime diagnostics
- PVL adapter output

### 14.2 Persisted Results

ValidationResults may be persisted when they provide useful durable evidence.

Examples include:

- steward approval
- external audit
- publication certification
- deferred-validation completion
- signed import report
- dispute evidence

### 14.3 Receipts

A validation receipt may record:

- input digest
- descriptor identity
- rule identity
- rule-set identity
- implementation identity
- engine version
- validator identity
- outcome
- signature

Receipt verification proves that an assertion was made over a particular input.

It does not prove semantic correctness unless the receipt acceptance rule and asserted semantics are independently enforceable.

### 14.4 PVL Results

PVL's authoritative output remains the Holochain validation callback result defined by the PVL Design Specification.

PVL does not normally persist a ValidationResult holon for every validated operation.

---

## 15. End-to-End Validation Flows

### 15.1 Holon Data Loader

    load authored data
        parse transport representation
        resolve references available to the loader
        resolve descriptor
        construct HolonValidationContext
        run built-in holon rules
        delegate to property validators
        delegate to generic value validators
        delegate to specific ValueType validators
        run relationship and transaction checks where possible
        return structured ValidationResults
        stage valid data in Nursery

### 15.2 Nursery Commit

    stage transaction
        resolve recognized descriptors
        validate each holon
        validate each property and value
        validate relationships
        validate transaction-wide constraints
        evaluate command and Dance preconditions
        fail, warn, defer, or approve
        commit approved operations

### 15.3 Peer Validation

    receive DHT operation
        Integrity adapter converts Holochain payload
        invoke PVL entry point
        run only PVL-supported validation
        return Valid, Invalid, or UnresolvedDependencies

The detailed flow is defined by the PVL Design Specification.

### 15.4 Runtime Read

    read committed data
        verify current descriptor recognition
        apply activation filtering
        optionally run runtime validation
        expose recognized data through normal APIs
        expose unrecognized or questionable data through diagnostics

### 15.5 Extensible Validation Dance

    collect descriptor-declared validations
        resolve active ValidationImplementation
        verify engine and context compatibility
        construct Validate Dance request
        execute implementation
        validate response contract
        convert response to ValidationResults
        aggregate results
        persist evidence where policy requires

### 15.6 Social Review

    validation result requires human or steward review
        initiate review Dance
        collect attestations or decisions
        record signed result
        apply AgentSpace governance policy
        update recognition or publication state where appropriate

---

## 16. Initial Implementation Scope

The initial implementation should deliver the validation architecture incrementally without requiring dynamic dispatch.

### 16.1 Required Initial Components

- level-specific Rust validation traits
- level-specific validation contexts
- distinct built-in validation-rule implementations
- hard-coded rule invocation
- deterministic validator delegation
- structured ValidationResults
- Holon Data Loader integration
- Nursery integration
- adapter integration with existing Holochain-independent validation entry points
- PVL integration only for the subset defined by the PVL Design Specification

### 16.2 Initial Rules

Initial Holon rules:

- `IsDescribedRule`
- `NoUndescribedPropertiesRule`
- `IsInstantiableRule`
- `DescriptorBindingRule`

Initial Property rules:

- `RequiredPropertyRule`

Initial generic ValueType rules:

- `PropertyValueTypeRule`

Initial String rules:

- `StringLengthRule`
- optional deterministic `StringFormatRule`

Initial Integer rules:

- `IntegerRangeRule`

Initial Enum rules:

- `LegalEnumVariantRule`

Initial Bytes rules:

- `BytesLengthRule`

Initial Relationship rules where supported:

- `DeclaredRelationshipRule`
- `SourceTypeConformanceRule`
- `TargetTypeConformanceRule`

Initial Nursery-only relationship rules:

- `RequiredRelationshipRule`
- `RelationshipCardinalityRule`

### 16.3 Deferred Components

The following are deferred:

- descriptor-declared `InstanceValidations`
- dynamic rule collection
- ValidationImplementation holons
- generic Dance-based validation dispatch
- WASM validation modules
- third-party validation engines
- human-in-the-loop workflows
- reusable ValidationRuleSets unless needed by initial schemas
- persisted validation receipts except for explicit use cases

---

## 17. Future Evolution

### 17.1 Descriptor-Declared Rules

Replace hard-coded per-level rule lists with rule identities collected from descriptors.

### 17.2 Built-In Rule Registry

Dispatch descriptor-declared rule identities to built-in Rust implementations.

### 17.3 ValidationImplementation Holons

Represent executable bindings separately from semantic rules.

### 17.4 Dance-Based Dispatch

Use the general Dance dispatcher in Nursery and higher layers.

### 17.5 Multiple Engines

Potential engines include:

- Builtin Rust
- WASM
- process-isolated implementation
- declarative expression engine
- human review

### 17.6 Rule Profiles

Support reusable ValidationRuleSets for:

- imports
- publication
- diagnostics
- security
- interoperability certification

### 17.7 Validation Provenance

Persist signed ValidationResults and receipts where durable evidence is useful.

### 17.8 Application and Agreement Rules

Allow applications and agreements to contribute validation commitments without modifying core validators or PVL.

---

## 18. Benefits

| Feature | Benefit |
|---|---|
| Layered validation | Rules execute where their dependencies and guarantees fit |
| Validator delegation | Each validator remains narrowly scoped |
| Level-specific contexts | Rules receive only the context appropriate to their concern |
| First-class ValidationRules | Validation semantics become inspectable and reusable |
| Rule and implementation separation | A semantic rule may support multiple execution engines |
| Descriptor declaration | Validation commitments become part of the type system |
| Built-in initial execution | The Proof of Concept remains implementable without dynamic dispatch |
| Dance compatibility | Runtime validation can evolve into MAP's general behavior model |
| Promise Theory alignment | Commitments, capabilities, enactments, and evidence remain explicit |
| Structured results | Validation feedback can be aggregated, displayed, logged, or attested |
| PVL separation | Integrity semantics remain bounded and independently specified |

---

## 19. Open Decisions

The architecture leaves the following decisions open:

- final name of the descriptor-to-rule relationship:
    - `Validations`
    - `InstanceValidations`
    - `ValidationRules`
- exact ValidationRule schema
- exact ValidationImplementation schema
- rule-parameter representation
- duplicate and override semantics during compositional inheritance
- whether default severity belongs on the rule or descriptor-to-rule binding
- validation profile selection
- persistent ValidationResult criteria
- validation receipt format
- DanceType granularity
- implementation activation policy
- which deterministic format rules are PVL-safe
- how validator implementations obtain typed views of descriptor holons
- whether rule invocation order is explicit data or derived from validator level
- whether rules may declare prerequisite rules
- how breaking validation changes interact with descriptor and DNA versioning

---

## 20. Implementation Checklist

### Architecture Foundation

- [ ] Define shared ValidationResult types.
- [ ] Define ValidationOperation.
- [ ] Define ValidationLayer.
- [ ] Define validator-level context structs.
- [ ] Define validation-rule traits for each level.
- [ ] Define deterministic result aggregation.
- [ ] Define short-circuit and delegation behavior.

### Holon and Property Validation

- [ ] Implement HolonValidator orchestration.
- [ ] Implement `IsDescribedRule`.
- [ ] Implement `NoUndescribedPropertiesRule`.
- [ ] Implement `IsInstantiableRule`.
- [ ] Implement property-descriptor iteration.
- [ ] Implement PropertyValidator orchestration.
- [ ] Implement `RequiredPropertyRule`.

### Value Validation

- [ ] Implement generic ValueValidator.
- [ ] Implement `PropertyValueTypeRule`.
- [ ] Implement StringValueValidator.
- [ ] Implement `StringLengthRule`.
- [ ] Implement IntegerValueValidator.
- [ ] Implement `IntegerRangeRule`.
- [ ] Implement BooleanValueValidator.
- [ ] Implement EnumValueValidator.
- [ ] Implement `LegalEnumVariantRule`.
- [ ] Implement BytesValueValidator.
- [ ] Implement `BytesLengthRule`.

### Relationship Validation

- [ ] Define RelationshipValidationContext.
- [ ] Implement RelationshipValidator orchestration.
- [ ] Implement `DeclaredRelationshipRule`.
- [ ] Implement `SourceTypeConformanceRule`.
- [ ] Implement `TargetTypeConformanceRule`.
- [ ] Implement Nursery-level cardinality validation.
- [ ] Implement required-relationship validation where transaction context permits.

### Integration

- [ ] Integrate with Holochain-independent create validation.
- [ ] Integrate with Holochain-independent update validation.
- [ ] Integrate with delete validation where applicable.
- [ ] Integrate with SmartLink create validation.
- [ ] Integrate with SmartLink delete validation.
- [ ] Integrate with Holon Data Loader validation.
- [ ] Integrate with Nursery transaction validation.
- [ ] Integrate the PVL-safe subset according to the PVL Design Specification.

### Testing

- [ ] Test each rule independently.
- [ ] Test delegation between validator levels.
- [ ] Test multiple errors in one validation pass.
- [ ] Test operation-specific behavior.
- [ ] Test layer-specific behavior.
- [ ] Test missing descriptors.
- [ ] Test undescribed properties.
- [ ] Test missing required properties.
- [ ] Test BaseValue and ValueType mismatches.
- [ ] Test string limits.
- [ ] Test integer limits.
- [ ] Test enum membership.
- [ ] Test relationship source and target conformance.
- [ ] Test transaction-level cardinality.
- [ ] Test Holon Data Loader fixtures.
- [ ] Test Holochain adapter behavior.
- [ ] Test PVL behavior separately against the PVL Design Specification.

---

## 21. Summary

MAP validation is both layered and holonic.

The validation layers determine where a rule can safely execute and what guarantee its outcome provides.

The validator hierarchy determines how validation is decomposed and delegated from whole holons to properties, values, specific ValueTypes, relationships, and transactions.

ValidationRules provide durable semantic identities for individual checks. TypeDescriptors will eventually declare the rules that apply to their instances, inheriting starter validation commitments from their Meta-Types and adding type-specific rules.

The initial implementation remains intentionally conservative:

- built-in Rust implementations
- hard-coded rule invocation
- explicit validator delegation
- no general dynamic dispatch

This provides the validation required for the Holon Data Loader, Nursery, and Holochain integration while establishing a direct evolutionary path toward:

- descriptor-declared validations
- reusable rule sets
- multiple validation implementations
- Dance-based dispatch
- Promise Theory-aligned commitments
- signed validation evidence
- community-extensible validation ecosystems