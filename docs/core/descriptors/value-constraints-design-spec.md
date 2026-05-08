# Value Constraints Design Spec

## Purpose

This document proposes a generalized `ValueConstraint` model for MAP value-type validity semantics.

The immediate motivation is a gap discovered during review of Descriptor PR3 / Issue 463: the current schema-backed model does not fully express the intrinsic validation semantics that MAP `ValueType`s were always intended to carry. Historically, designs for `IntegerValueType`, `StringValueType`, and `ValueArrayValueType` included built-in validity properties such as numeric bounds, string length limits, and array cardinality constraints. Those semantics are no longer clearly represented in the authoritative core schema.

This document proposes a recovery path that does not simply reintroduce ad hoc fields such as `min_value` and `max_value`, but instead establishes a first-class, extensible, and execution-efficient `ValueConstraint` model.

---

## Problem Statement

MAP `ValueType`s are intended to do more than identify scalar kind. They are also meant to define the core validity semantics for values of that kind.

Examples of intended semantics include:

- `IntegerValueType`
    - numeric lower and upper bounds
    - eventually additional numeric constraints
- `StringValueType`
    - minimum and maximum length
    - eventually pattern and format constraints
- `ValueArrayValueType`
    - minimum and maximum item count
    - uniqueness / ordering semantics
- `EnumValueType`
    - membership in the declared variant set

The current schema-backed descriptor model does not fully express this validation surface. In particular:

- integer bounds such as `min_value` / `max_value` are absent from the current authoritative core schema
- direct property-based constraint representation is too weak for long-term needs
- several constraint semantics are ambiguous if represented only as simple fields
- the current design leaves `ValueDescriptor::is_valid` without a complete schema-backed validity model

---

## Design Goals

The design should satisfy the following goals:

1. Restore value-type-owned validity semantics as a first-class part of MAP’s model.
2. Represent validation rules explicitly and unambiguously.
3. Support extensibility without forcing the core schema to hard-code every possible future constraint as a direct property.
4. Preserve efficient runtime execution.
5. Keep `ValueDescriptor::is_valid` descriptor-owned and statically implemented in Rust.
6. Distinguish between schema expressiveness and executable core validation semantics.
7. Support introspection, inheritance, and future descriptor-driven tooling.

---

## Design Summary

Introduce a first-class abstract `ValueConstraint` concept.

Rather than embedding all validation semantics directly as ad hoc fields on each `ValueType`, MAP should model constraints explicitly as holons. A `ValueType` may declare one or more `Constraints` relationships to `ValueConstraint` holons. Each constraint holon is itself described by a concrete constraint type that determines its semantics.

Examples:

- an `IntegerValueType` may declare constraints such as:
    - `MinimumValueConstraint`
    - `MaximumValueConstraint`
- a `StringValueType` may declare constraints such as:
    - `MinimumLengthConstraint`
    - `MaximumLengthConstraint`
    - `PatternConstraint`
    - `FormatConstraint`
- a `ValueArrayValueType` may declare constraints such as:
    - `MinimumItemsConstraint`
    - `MaximumItemsConstraint`
    - `UniqueItemsConstraint`
    - `OrderedItemsConstraint`

At runtime, descriptor resolution should produce family-specific typed constraint collections. `ValueDescriptor::is_valid` should execute a deterministic validation walk over those collections via static Rust dispatch rather than by performing open-ended graph interpretation.

---

## Core Architectural Principle

The design must preserve a strict separation between:

- declarative schema representation
- executable runtime validation

In the schema, constraints are modeled as holons and relationships.

At runtime, only a closed, recognized set of constraint kinds is treated as core-executable by `ValueDescriptor::is_valid`. Each recognized constraint kind maps to statically implemented Rust logic.

This allows MAP to remain reflective and extensible without turning core validation into a general-purpose constraint interpreter.

---

## Why Not Just Re-Add `min_value` and `max_value`?

Reintroducing direct fields would recover some lost semantics, but it would not solve the deeper modeling problem.

Direct property-based constraint representation has several weaknesses:

- it is ambiguous about semantics such as inclusive vs exclusive bounds
- it assumes only one fixed representation per constraint family
- it does not scale cleanly to richer constraint forms such as pattern, format, normalization, or multiple reusable rule types
- it tightly couples constraint vocabulary to the value-type definition itself
- it provides a weaker foundation for composition, inheritance, and future introspection

For these reasons, this design favors first-class constraints over direct primitive fields.

---

## Proposed Schema Model

### Abstract Concepts

Introduce the following abstract concepts:

- `ValueConstraint`
    - abstract descriptor category for constraints applicable to `ValueType`s
- `Constraints`
    - family-specific relationship declared on each abstract value-family type and targeting the corresponding family-specific constraint type

At minimum, the schema should support:

- each abstract value-family type declaring zero or more `Constraints`
- each `ValueConstraint` being a holon
- each `ValueConstraint` being `DescribedBy` a concrete constraint type
- each abstract value-family type constraining the target of `Constraints` to the matching family-specific constraint type
- each concrete constraint type constraining which `ValueType` families it may validly apply to

For value constraints specifically, the preferred placement is not one generalized `Constraints` declaration on `ValueType`.

Instead, `Constraints` should be declared on each abstract value-family type, such as:

- `IntegerValueType -> Constraints -> IntegerValueConstraint`
- `StringValueType -> Constraints -> StringValueConstraint`
- `BytesValueType -> Constraints -> BytesValueConstraint`
- `ValueArrayValueType -> Constraints -> ValueArrayConstraint`

This makes the allowed constraint families explicit in the ontology and keeps the target of each `Constraints` relationship strongly typed.

It also simplifies both sides of the design:

- for value type definitions, it is explicit which constraint family is allowed
- for constraint type definitions, properties and validation semantics only need to be expressed against the matching value family

### Constraint Type Families

Examples of concrete constraint types:

#### Integer

- `MinimumValueConstraint`
- `MaximumValueConstraint`
- `MultipleOfConstraint`

#### String

- `MinimumLengthConstraint`
- `MaximumLengthConstraint`
- `PatternConstraint`
- `FormatConstraint`

#### Bytes

- `MinimumBytesLengthConstraint`
- `MaximumBytesLengthConstraint`
- `EncodingConstraint`
- `FormatHintConstraint`

#### Value Array

- `MinimumItemsConstraint`
- `MaximumItemsConstraint`
- `UniqueItemsConstraint`
- `OrderedItemsConstraint`

#### Enum

Enum semantics are partly structural rather than purely rule-like. Variant membership is still primarily defined by the enum’s variant set, but additional enum-specific constraint types could be introduced if needed later.

---

## Constraint Semantics

Each executable constraint type must define explicit semantics.

Examples:

### `MinimumValueConstraint`

Properties:
- `value`
- `inclusive: bool`

Semantics:
- valid iff actual numeric value is greater than `value`
- or greater than or equal to `value` if `inclusive == true`

### `MaximumValueConstraint`

Properties:
- `value`
- `inclusive: bool`

Semantics:
- valid iff actual numeric value is less than `value`
- or less than or equal to `value` if `inclusive == true`

### `MinimumLengthConstraint`

Properties:
- `value`

Semantics:
- valid iff string length is at least `value`

### `PatternConstraint`

Properties:
- `pattern`
- optionally `pattern_dialect`

Semantics:
- valid iff the string matches the declared pattern according to the supported runtime pattern semantics

### `FormatConstraint`

Properties:
- `format`

Semantics:
- valid iff the string satisfies the recognized format semantics supported by the runtime

The core rule is that semantics must be explicit, not implied by naming convention alone.

---

## Executability Model

Not every `ValueConstraint` that exists in the schema must be executable by core runtime validation.

This design introduces a conceptual distinction between:

- core-executable constraints
- non-core or advisory constraints

### Core-Executable Constraints

These are recognized by the descriptor runtime and executed through static Rust validation logic.

Examples:
- minimum / maximum numeric bounds
- min / max length
- item count constraints
- uniqueness flags
- recognized format checks

### Advisory or Higher-Layer Constraints

These may exist in the schema for documentation, UI guidance, negotiation, domain-specific policy, or future higher-layer validation, but are not executed by the core `is_valid` path unless and until explicitly adopted into the recognized executable set.

This keeps the hot path bounded and predictable.

---

## Runtime Execution Model

### High-Level Flow

1. Resolve the `ValueType`
2. Resolve its declared `Constraints`
3. Validate that each constraint is structurally compatible with the value kind
4. Resolve recognized constraints into typed descriptor-owned collections
5. Execute a deterministic validation walk in `ValueDescriptor::is_valid`

### Bottom-Up Instance Validation Model

The intended validation model is instance validation, not merely descriptor self-validation.

The key runtime problem is bringing instance values into contact with constraint parameters defined in the schema-backed constraint holons.

For example:

- a `MinimumValueConstraint` may define:
  - `value`
  - `is_inclusive`
- an `IntegerValueDescriptor` owns a collection of integer constraints
- a `PropertyDescriptor` references that integer descriptor
- a `HolonTypeDescriptor` owns the property descriptor

Validation therefore proceeds downward toward the concrete value and then applies the relevant typed constraint family at the bottom of the chain.

The validation flow is:

1. a `HolonTypeDescriptor` validates an instance holon
2. it iterates its property descriptors
3. each property descriptor extracts the candidate property value from the instance
4. the property descriptor delegates to the referenced value descriptor
5. the value descriptor invokes the appropriate typed constraint family against the candidate value

This gives MAP a compositional instance-validation model while preserving strongly typed, family-specific runtime semantics.

### Family-Typed Validation

Each constraint family should validate the runtime value kind it is responsible for rather than forcing all constraints through a single untyped `BaseValue` interface.

Examples:

- integer constraints validate integer values
- string constraints validate string values
- boolean constraints validate boolean values
- array constraints validate value arrays

This means the effective runtime contract should be family-typed even if the schema-level architecture is generalized.

Examples of family-specific signatures:

```rust
trait IntegerConstraintValidation {
    fn is_valid(&self, value: i64) -> Result<(), HolonError>;
}

trait StringConstraintValidation {
    fn is_valid(&self, value: &str) -> Result<(), HolonError>;
}

trait ValueArrayConstraintValidation {
    fn is_valid(&self, value: &[BaseValue]) -> Result<(), HolonError>;
}
```

The exact Rust trait layout can be refined during implementation, but the design intent is clear: executable instance validation should be typed by value family.

### Constraint Family Enums

Each executable value family should also have a concrete runtime enum representing the recognized constraint set for that family.

For example:

```rust
enum IntegerConstraint {
    Minimum(MinimumValueConstraint),
    Maximum(MaximumValueConstraint),
    MultipleOf(MultipleOfConstraint),
}
```

This allows:

- family-safe ownership by the descriptor
- efficient static dispatch
- compatibility checks at descriptor-resolution time
- a bounded executable surface in Rust

The descriptor can then own a family-specific collection such as:

```rust
struct IntegerValueDescriptor {
    constraints: Vec<IntegerConstraint>,
}
```

and validate through a bounded dispatch loop:

```rust
impl IntegerValueDescriptor {
    fn is_valid(&self, value: i64) -> Result<(), HolonError> {
        for constraint in &self.constraints {
            constraint.is_valid(value)?;
        }
        Ok(())
    }
}
```

This is the concrete execution posture the design is aiming for.

### Deterministic Validation Walk

A descriptor should not walk the graph and reinterpret constraint holons on every validation call.

Instead, the resolved constraints should live directly in the family-specific runtime enum collections owned by each descriptor.

For example:

```rust
struct IntegerValueDescriptor {
    constraints: Vec<IntegerConstraint>,
}
```

Then `ValueDescriptor::is_valid` becomes a bounded, deterministic walk over that family-specific collection.

In the normal case, the family-specific constraint enum is the resolved runtime structure used by validation.

Some families may still need family-local enrichment when moving from schema fields to runtime-ready values. For example, a pattern constraint may need to turn a stored pattern string into a compiled regex handle. But that does not require a universal umbrella `ResolvedValueConstraint` layer.

The default design should therefore remain simple:

- each value family has its own executable constraint enum
- each typed descriptor owns a collection of that enum
- validation walks that collection directly

This approach is consistent with the design as long as runtime instance validation remains:

- family-typed
- statically dispatched
- bounded
- free of open-ended graph interpretation in the hot path

### Efficiency Goals

This model should preserve efficiency by ensuring that:

- graph traversal is done during descriptor resolution, not per validation call
- structural incompatibility is rejected before value validation begins
- executable semantics are static Rust match arms or equivalent static dispatch
- no dynamic scripting engine or open-ended evaluator is required

---

## Descriptor Responsibilities

`ValueDescriptor` remains the owner of value validity evaluation.

Its responsibilities should include:

- determining base value-kind compatibility
- resolving effective inherited constraints
- validating constraint graph correctness
- resolving executable constraints into typed runtime structures
- evaluating resolved constraints against candidate values
- returning validation-oriented `HolonError` outcomes for invalid values or invalid descriptor state

For higher-level descriptor composition, the intended delegation chain is:

- `HolonTypeDescriptor::is_valid(instance_holon)`
  - iterates declared property descriptors and declared relationship descriptors
- `PropertyDescriptor::is_valid(instance_property_value)`
  - delegates to the referenced value descriptor
- `ValueDescriptor::is_valid(typed_value)`
  - iterates the executable constraints for its family
- `Constraint::is_valid(typed_value)`
  - performs the actual typed comparison against the constraint parameters

This compositional model is one of the main reasons to keep constraint semantics explicit and family-typed.

This design does not move validity ownership out of descriptors. It gives descriptors a more complete and extensible schema-backed semantic surface.

---

## Constraint Compatibility Rules

Each executable constraint type must declare the value families to which it can apply.

Examples:

- `MinimumValueConstraint`
  - valid for integer-like numeric value types
  - invalid for strings, enums, booleans
- `PatternConstraint`
  - valid for string-like value types
  - invalid for integers and booleans
- `MinimumItemsConstraint`
  - valid for value arrays
  - invalid for strings and integers

Descriptor resolution should fail fast if a `ValueType` declares an incompatible constraint.

This avoids silent nonsense and keeps invalid schema graphs explicit.

---

## Inheritance and Effective Constraints

The design should support inherited constraints when `ValueType`s extend other `ValueType`s.

Example:

- base `IntegerValueType` may declare a broad allowed range
- a specialized `AgeValueType` may add a narrower minimum
- a specialized `PortNumberValueType` may constrain both lower and upper bounds

Follow-on design work must define how multiple constraints of the same family combine.

Options include:
- simple additive conjunction
- override semantics
- family-specific merge rules

The default posture should be conservative and explicit. Contradictory or ambiguous combinations should be treated as descriptor invalidity unless a merge rule is clearly defined.

---

## Suggested Initial Constraint Families

The initial executable set should stay focused.

### Phase 1 Candidate Set

#### Integer
- `MinimumValueConstraint`
- `MaximumValueConstraint`

#### String
- `MinimumLengthConstraint`
- `MaximumLengthConstraint`
- optional: `PatternConstraint`

#### Value Array
- `MinimumItemsConstraint`
- `MaximumItemsConstraint`
- `UniqueItemsConstraint`
- `OrderedItemsConstraint`

This is enough to recover the original screenshot-era design intent while establishing the generalized architecture.

### Later Candidate Set

- `FormatConstraint`
- `MultipleOfConstraint`
- byte encoding / format constraints
- richer string normalization or charset constraints
- domain-specific reusable constraints

---

## Relationship to Existing Designs

This proposal is aligned with the long-standing MAP intention that each core value `TypeKind` carries intrinsic validity semantics.

It intentionally departs from the older field-oriented representation shown in early UML-style designs by generalizing those semantics into a composable `ValueConstraint` layer.

The older direct-field model should be treated as an early simplification of the deeper design intent, not as the long-term target architecture.

---

## Migration Implications

This design implies follow-on updates in several areas.

### Core Schema

Add:
- `ValueConstraint`
- `Constraints`
- concrete executable constraint types
- any required properties on concrete constraint holons

### Descriptors Schema Surface

Add:
- schema-backed access to effective constraints
- possibly generic constraint accessors and selected typed helpers

### Runtime

Add:
- descriptor resolution support for constraint graphs
- resolved typed constraint construction
- static Rust dispatch for executable constraints

### Validation

Refine:
- `ValueDescriptor::is_valid`
- descriptor invalidity reporting for malformed or incompatible constraints

---

## Non-Goals

This design does not attempt to:

- create a general-purpose user-programmable validation language
- allow arbitrary holon graphs to be executed as dynamic validator logic in the core hot path
- fully solve higher-layer social or policy validation
- finalize every future constraint family now

The initial goal is narrower:
restore first-class value validity semantics in a way that is explicit, extensible, and efficient.

---

## Current Design Decisions

The following points are now considered the current design direction for this spec.

### Constraint Instances and Types

`ValueConstraint` holons should be modeled as plain instances described by reusable constraint types.

This keeps the model aligned with the rest of MAP:

- constraint holon = applied/declared instance
- constraint type = reusable schema-level definition of that constraint family

No extra universal layering is required at this stage.

### Constraint Declaration Site and Multiplicity

For value constraints, `Constraints` should be declared on each abstract value-family type rather than once generically on `ValueType`.

Examples:

- `IntegerValueType -> Constraints -> IntegerValueConstraint`
- `StringValueType -> Constraints -> StringValueConstraint`
- `BytesValueType -> Constraints -> BytesValueConstraint`
- `ValueArrayValueType -> Constraints -> ValueArrayConstraint`

This is the preferred design because it:

- keeps the target of `Constraints` strongly typed to the matching constraint family
- makes it explicit which constraint types are allowed for a given abstract value family
- simplifies both value-type and constraint-type definitions
- reduces the need for looser runtime or schema-level compatibility policing

Multiplicity should be:

- each abstract value-family type may declare zero or more `Constraints`
- each declared constraint instance is, by default, owned/applied by one declaring value descriptor

This keeps the initial model simple. If reusable shared constraint instances become desirable later, that can be revisited as a future extension.

### Inheritance Combination Rule

Inherited constraints should combine conjunctively.

That means:

- inherited and locally declared constraints all apply
- narrowing is allowed
- contradiction is descriptor invalidity

Override semantics are not part of the default design.

### Initial Executable Core Set

The initial executable set should stay deliberately small.

Recommended first executable families are:

- Integer
  - `MinimumValueConstraint`
  - `MaximumValueConstraint`
- String
  - `MinimumLengthConstraint`
  - `MaximumLengthConstraint`
  - optional early inclusion of `PatternConstraint`
- Value Array
  - `MinimumItemsConstraint`
  - `MaximumItemsConstraint`
  - `UniqueItemsConstraint`
  - `OrderedItemsConstraint`

Later candidates include:

- `FormatConstraint`
- `MultipleOfConstraint`
- bytes-specific encoding / format constraints
- richer domain-specific constraints

### Pattern and Format Bounding

Pattern and format semantics must be tightly bounded so runtime behavior remains deterministic and portable.

The current design direction is:

- `PatternConstraint` must use one explicitly chosen supported pattern dialect
- unsupported pattern features should be rejected during descriptor resolution
- `FormatConstraint` should use a closed set of recognized runtime format names
- unknown or unsupported formats should not be loosely interpreted at runtime

### Family-Typed Runtime Interfaces

Runtime validation interfaces should be family-typed.

Examples:

- integer constraints validate `i64`
- string constraints validate `&str`
- boolean constraints validate `bool`
- bytes constraints validate `&[u8]`
- array constraints validate slices/collections of element values
- enum constraints validate the canonical runtime enum-value representation chosen by the implementation

The exact Rust trait layout may still evolve, but the family-typed principle is considered settled.

### Resolved Runtime Structure

Descriptor-owned resolved constraint structures should normally be the family-specific runtime enums themselves.

Examples:

- `IntegerValueDescriptor` owns `Vec<IntegerConstraint>`
- `StringValueDescriptor` owns `Vec<StringConstraint>`

There is no need for a universal umbrella `ResolvedValueConstraint` layer in the default design.

If a particular family requires runtime enrichment, such as compiling a regex from a stored pattern string, that should be handled inside that family's own runtime representation.

### Error Taxonomy

The runtime and descriptor model should distinguish at least the following categories:

- invalid candidate value
  - a valid constraint was applied and the instance value failed it
- invalid descriptor graph
  - the schema/descriptor/constraint graph is malformed, contradictory, or structurally invalid
- incompatible constraint type
  - a constraint family was attached to an incompatible value family
- unsupported executable constraint kind
  - a schema-recognized constraint exists, but the runtime does not execute it in the current core set

These distinctions should remain explicit in both implementation and documentation.

### Caching Posture

Resolved constraint structures should initially be cached at the descriptor-instance level.

That is the simplest implementation posture and is sufficient unless profiling later shows a need for broader caching at the resolved type-graph level.

---

## Residual Questions

The following questions remain open enough to require additional focused design or implementation decisions:

1. Which exact regex/pattern dialect should core runtime support first?
2. Should `PatternConstraint` be included in the very first executable implementation pass or follow immediately after basic min/max families?
3. What is the canonical runtime representation for enum values in family-typed validation?
4. How should bytes-family executable constraints be sequenced once the initial integer/string/array families land?
5. If descriptor-instance caching later proves insufficient, what is the correct resolved type-graph caching strategy?

---

## Recommended Next Steps

1. Charter a focused design issue for `ValueConstraint` architecture.
2. Define the core schema additions for:
   - `ValueConstraint`
   - `Constraints`
   - initial concrete constraint types
3. Define family-specific executable constraint sets for integer, string, and value-array families in the first pass.
4. Encode the conjunctive inheritance rule and descriptor-invalidity behavior for contradictions.
5. Specify the runtime deterministic validation-walk model using family-specific constraint enums as the normal resolved runtime structure.
6. Decide the initial supported pattern dialect and whether `PatternConstraint` lands in the first or second executable pass.
7. Update descriptor design docs to reflect typed, constraint-backed `is_valid` semantics from holon type down to concrete value checks.
8. Sequence implementation so that the first pass restores the minimal intended constraint families without overextending into a universal validation engine.

---

## Conclusion

MAP should restore value-type-owned validity semantics, but it should do so through a first-class `ValueConstraint` model rather than by merely reintroducing a handful of primitive fields.

The runtime model should be explicitly bottom-up and instance-oriented: schema-defined constraint parameters resolve into family-specific executable constraint sets, value descriptors own those sets, and higher-level descriptors validate compositionally by delegating downward until typed value checks occur.

This approach better matches the reflective architecture of the platform, removes ambiguity from constraint semantics, creates room for future growth, and still allows `ValueDescriptor::is_valid` to execute efficiently through statically dispatched Rust logic over a resolved, family-typed constraint structure using a deterministic validation walk.
