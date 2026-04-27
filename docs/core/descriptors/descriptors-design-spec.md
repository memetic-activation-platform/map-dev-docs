# Descriptors Design Spec (v1.2)

This spec defines the core runtime descriptor model for MAP. This model introduces a significant set of capabilities into the MAP core that move us much closer to the MAP vision of **_open-ended self-describing, active holons and holon relationships._** 

We have implemented holons and holon relationships, but these holons are neither _self-describing_ nor _active_. Dances, as currently implemented, are decoupled from holon types and are centrally dispatched. We've added the ability to load descriptors via the Holon Data Loader, but these loaded descriptors are not linked to any MAP core behaviors -- inverse relationships are not being populated, holon keys are not being composed and, most importantly, there is no descriptor-driven validation.

### Highlights

The capabilities introduced via this spec include the following:

- **Re-allocation of standalone behavior to descriptors.** Until now, dances and commands have been implemented as standalone functions. Moving these behaviors to descriptors gives us a modular, extensible foundation. 
- **Decentralized (but static) dance/command dispatch.** The current approach to dispatching dances is _centralized_ and _static_. We have a single, flat, hard-coded dispatch table. Adding support for new dances requires extending this table and a rebuild. To support the MAP's architectural goals, we need: (1) dances structured around holons types,(2) decentralized dispatch and (3) dynamic loading of dance implementations. This spec introduces (1) and (2), but not yet (3).
- **Validation operator support.** MAP ValueType descriptors specify various constraints on values of that type (e.g., min/max lengths, min/max values, required). This spec introduces simple is_valid operators that encapsulate the logic for enforcing these constraints.
- **Query operator support.** OpenCypher and GQL support WHERE clauses that filter results on the basis of value-type specific operators. This spec introduces support for such operators.
- **Convenience lookup methods.** This spec prescribes various lookup methods (e.g., property and relationship and inverse relationship descriptor lookups by name).
- **Automatic compression of Extends Inheritance**. The MAP's type definition language allows a type descriptor to inherit instance properties, instance relationships and instance behaviors (dances and commands) from other types via (at most one) `Extends` relationship. This spec encapsulates navigation upwards through the chain of Extends so that all such inheritance is effectively flattened -- callers don't have to worry about navigating Extends relationships and implementing inheritance logic.
- **JSON Core Schema definitions drive descriptors definition.** Changes to the MAP Core Schema almost always have a ripple effect on the code base, test cases, and documentation. This spec references a companion document: [Schema Ripple Design Spec](schema-ripple-design-spec.md) that describes an approach to ensuring proper ripple-effects are handled with minimal effort.

## Status

Proposed

Note: MAP design docs are normally published from the separate dev-docs repository. This file is a working draft captured alongside code for iteration and should be moved or mirrored there when the design stabilizes.

## Scope

It is intentionally narrow and normative. Background material, rollout process, behavior allocation, and schema ripple process belong in the companion specs.

The organizing principle here is `TypeKind`: the main contract is what descriptor wrapper exists for each kind, what operations it exposes, and what schema-backed accessors it should provide.

Instead of leaving key operations as freestanding helpers or central registries, the design moves those operations onto descriptor wrappers themselves. That includes convenience lookup methods, inheritance flattening, validation-oriented behavior, and the static dispatch points needed for later dance/command and query/operator support.

## Authoritative Source

The authoritative source of truth for descriptor structure is the core schema JSON under:

- `host/import_files/map-schema/core-schema/`

Structural accessors should derive from those definitions, not from handwritten Rust mirrors. In this phase, that derivation is expected to be AI-assisted rather than produced by a permanent hard-coded generator. The important constraint is that the resulting descriptor surface remains schema-backed, reviewable, and aligned with the current authoritative JSON definitions.

This does not prevent the spec from prescribing new or updated descriptor definitions in the core schema. The constraint is on implementation: runtime behavior should be tied back to schema definitions, not float free of them.

## Common Contract

These rules apply to every descriptor wrapper, regardless of `TypeKind`.

Taken together, these rules define the common MAP descriptor posture: thin wrappers, schema-backed structure, no duplicated ontology state, and descriptor-local behavior rather than centralized descriptor registries.

### Representation

- Every descriptor is itself a holon.
- Every runtime descriptor wrapper is a thin typed view over a backing `HolonReference`.
- Every wrapper stores a single private `holon: HolonReference`.
- Descriptor wrappers do not duplicate ontology state as Rust fields.

Representative shape:

```rust
pub struct HolonDescriptor {
    holon: HolonReference,
}
```

### Shared runtime abstractions

`ReadableHolon` should expose:

```rust
fn holon_descriptor(&self) -> Result<HolonDescriptor, HolonError>;
```

Semantics:

- follow the source holon's single `DescribedBy` relationship
- error if none exists
- error if more than one exists
- wrap the resulting `HolonReference` in `HolonDescriptor`

All descriptor wrappers should implement:

```rust
pub trait Descriptor {
    fn holon(&self) -> &HolonReference;
}
```

Shared descriptor/header access should be centralized through a runtime `TypeHeader` helper. Descriptor wrappers should expose direct convenience methods through shared code rather than storing header fields directly.

This shared layer is also the place where behavior that is common across descriptor kinds should live. The goal is not a monolithic dispatcher, but a small amount of shared runtime support that lets each concrete descriptor kind own its own behavior cleanly.

### Inheritance

- Descriptor inheritance is single inheritance through `Extends`.
- Callers should experience a flattened effective descriptor view.
- Normal descriptor use must not require caller-side `Extends` walking.
- Descriptor wrappers should not store a constructor-time cached `extends_chain`.

Flattening the `Extends` hierarchy is one of the core ergonomic promises of the descriptor layer. Callers should ask for the effective property, relationship, or rule they need and get a descriptor-level answer, not a chain they must interpret themselves.

Traversal rules:

- include `self` first
- walk parentward until no `Extends` target exists
- error on multiple `Extends`
- error on cycles
- for lookups, chase only far enough to find a match unless a full chain is truly needed

### Overrides

- Child descriptor redeclaration of an inherited property name is invalid.
- Child descriptor redeclaration of an inherited relationship name is invalid.
- These invalid structures should be prevented at descriptor/schema commit time.
- Runtime descriptor lookup should still fail loudly if such an invalid saved or staged structure is encountered.

### Generated accessors

- Structural accessors should be generated or derived strictly from schema-declared `InstanceProperties` and `InstanceRelationships`.
- If an accessor is not justified by the current authoritative schema, it should not be introduced as if it were schema-backed.
- If the intended accessor is part of the target design but not yet justified by the current schema, that is a core-schema deficiency to correct.

This is the mechanism by which the JSON core schema definitions drive the runtime descriptor surface. The schema defines the structural obligations; the runtime descriptor wrappers expose those obligations as typed convenience accessors.

### Error semantics

Descriptor operations should fail precisely on:

- missing required `DescribedBy`
- multiple `DescribedBy`
- multiple `Extends`
- cycles in `Extends`
- missing required header field
- invalid descriptor/value kind casts
- missing `InverseOf` when inverse lookup requires it
- duplicate inherited declarations

## Behavior Affordances

Descriptors are the semantic home for behavior affordances. In this phase, the design distinguishes three behavior families:

- `InstanceDance`: domain-extensible behavior afforded by holon types
- `Command`: core-defined behavior afforded by descriptors, but not domain-extensible
- `Operator`: core-defined semantic affordances of value types

All three families follow the same inheritance posture:

- affordances flatten across `Extends`
- callers should not reconstruct inherited behavior themselves
- no override
- no deletion
- duplicate redeclaration is invalid

They differ in where they are declared:

- `InstanceDance` is afforded by `HolonType` descriptors
- `Command` is afforded by core descriptor types and inherited by their descendants
- `Operator` is afforded by `ValueType` descriptors

Dynamic execution/binding of dances and commands is deferred. The concern of this spec is descriptor structure, affordance lookup, and the static runtime surfaces on which later dispatch will attach.

## Behavior Ownership Matrix

The table below makes explicit where the behavior promised by this spec lives.

| Behavior | Owning Runtime Descriptor |
|---|---|
| Property lookup by name | `HolonDescriptor` |
| Relationship lookup by name | `HolonDescriptor` |
| Inverse relationship lookup by name | `HolonDescriptor` |
| Instance dance lookup | `HolonDescriptor` |
| Property-to-value semantic bridge | `PropertyDescriptor` |
| Value validation | `ValueDescriptor` |
| Operator discovery | `ValueDescriptor` |
| Operator support check | `ValueDescriptor` |
| Operator application | `ValueDescriptor` |
| Command lookup | descriptor wrappers via shared behavior affordance support |
| Relationship structural semantics | `RelationshipDescriptor` |

Interpretation rules:

- descriptor wrappers own externally meaningful behavior
- shared runtime helpers may support those behaviors, but should not become a second semantic layer
- behavior should be attached as close as possible to the descriptor kind that semantically owns it

## Static Dispatch Model

This spec introduces decentralized but static dispatch for dances, commands, and operators.

`Decentralized` means:

- behavior is discovered from descriptors and their affordances, not from a single global dispatch table
- inheritance-aware behavior lookup is local to the relevant descriptor wrapper
- different descriptor kinds may own different dispatch surfaces

`Static` means:

- once a descriptor or affordance has been resolved, behavior is dispatched to handwritten Rust implementations associated with the relevant descriptor kind
- there is no dynamic module loading in this phase
- there is no runtime plugin registry in this phase

Dispatch shape in this phase:

1. resolve the relevant descriptor
2. resolve the effective inherited affordance set through flattened `Extends`
3. select the requested dance, command, or operator by name or identity
4. dispatch through descriptor-local static Rust code

This is the mechanism by which standalone behavior is re-allocated onto descriptors without yet committing to dynamic implementation loading.

## Operator Model

Operators are part of the descriptor foundation because query construction, collection filtering, relationship-navigation filtering, and value validation all need a discoverable comparator surface.

This spec distinguishes:

- `OperatorDescriptor`: a descriptor holon that defines an available operator
- operator invocation: a runtime method call on a descriptor, not a holon instance

Initial operator posture:

- operators are core-defined, not domain-extensible
- operator affordances are declared by `ValueType` descriptors
- value descriptors expose the effective inherited operator surface
- operator application is descriptor-local static Rust dispatch

Minimum metadata promised by `OperatorDescriptor`:

- stable operator identity
- human-readable display metadata
- arity
- operator category
- applicability to value types

Initial runtime promises:

- descriptors can enumerate available operators for filter/query construction
- descriptors can answer whether a given operator is supported
- descriptors can apply a supported operator to concrete operands

The initial operator family should at least cover the comparator use cases required for:

- value validation support where appropriate
- OpenCypher and GQL-style value comparison
- collection filtering
- relationship-navigation filtering driven by value comparison

## Shared Descriptor Surface

All descriptor wrappers should expose the shared structural accessors implied by `TypeDescriptor` and `MetaTypeDescriptor`.

This shared surface is what makes descriptor wrappers feel coherent as a family. It gives every descriptor the same basic type-introspection vocabulary while leaving kind-specific behavior to the sections below.

### Shared properties

- `type_name()`
- `type_name_plural()`
- `display_name()`
- `display_name_plural()`
- `description()`
- `is_abstract_type()`
- `instance_type_kind()`

### Shared relationships

- `component_of()`
- `extends()`
- `uses_key_rule()`

### Shared handwritten helpers

- `header()`
- `holon()`
- inheritance traversal helpers

## Descriptor Kinds

### Holon

`HolonDescriptor` is the primary structural descriptor for holon types. It carries the most important convenience API in this phase because callers routinely need to resolve properties and relationships by name without manually traversing inheritance or inverse links.

It is also the primary instance-facing entrypoint for inherited behavior lookup. From a caller's perspective, the same descriptor used to inspect a holon type should also answer what dances and commands that type effectively affords.

Wrapper:

- `HolonDescriptor`

Required handwritten operations:

```rust
fn get_property_by_name(
    &self,
    property_name: PropertyName,
) -> Result<PropertyDescriptor, HolonError>;

fn get_relationship_by_name(
    &self,
    relationship_name: RelationshipName,
) -> Result<RelationshipDescriptor, HolonError>;

fn get_inverse_relationship_by_name(
    &self,
    declared_relationship_name: RelationshipName,
) -> Result<RelationshipDescriptor, HolonError>;

fn afforded_instance_dances(&self) -> Result<Vec<DanceDescriptor>, HolonError>;

fn get_instance_dance_by_name(
    &self,
    dance_name: DanceName,
) -> Result<DanceDescriptor, HolonError>;

fn afforded_commands(&self) -> Result<Vec<CommandDescriptor>, HolonError>;

fn get_command_by_name(
    &self,
    command_name: CommandName,
) -> Result<CommandDescriptor, HolonError>;
```

Lookup semantics:

- search `self` first, then ancestors in `Extends` order
- return the first matching declaration found
- relationship lookup should match both declared and inverse relationship descriptors
- inverse lookup should resolve the declared relationship first, then follow `InverseOf`
- dance lookup should resolve the effective inherited dance affordance set
- command lookup should resolve the effective inherited command affordance set

These lookup methods are intentionally convenience-heavy. They are part of the value of introducing descriptors as first-class runtime wrappers: descriptor consumers should be able to ask for a property, relationship, or inverse relationship by name and receive the effective descriptor directly.

The same convenience principle applies to behavior. Callers should be able to ask a holon descriptor which dances and commands it affords without separately reconstructing inheritance or consulting a central dispatch table.

Schema-backed additional properties:

- `allows_additional_properties()`
- `allows_additional_relationships()`

Schema-backed additional relationships:

- `properties()`
- `described_by()`
- `owned_by()`

### Property

`PropertyDescriptor` is the bridge from holon structure to value semantics. Its main job in this phase is to make the property's value type directly reachable as a typed descriptor.

Wrapper:

- `PropertyDescriptor`

Required handwritten/runtime operation:

```rust
fn value_type(&self) -> Result<ValueDescriptor, HolonError>;
```

Schema-backed additional properties:

- `is_required()`
- `property_name()`

Schema-backed additional relationships:

- `value_type()`

### Relationship

Relationship descriptors carry the structural semantics of graph edges. In this phase they remain mostly structural, but they are important because they centralize relationship metadata that other systems should stop treating as freestanding configuration.

Wrappers:

- `RelationshipDescriptor`
- `DeclaredRelationshipDescriptor`
- `InverseRelationshipDescriptor`

`RelationshipDescriptor` requires no additional handwritten behavior in this phase beyond shared descriptor access, inheritance participation, and inverse-related lookup support.

This is also the area where later decentralized dance/command dispatch should attach. The direction is static and descriptor-local: relationship-aware behavior should live with relationship descriptors and their close collaborators rather than in a central god-dispatcher.

Schema-backed properties on `RelationshipDescriptor`:

- `deletion_semantic()`
- `is_definitional()`
- `is_ordered()`
- `allows_duplicates()`
- `min_cardinality()`
- `max_cardinality()`
- `property_name()`
- `allows_additional_properties()`
- `allows_additional_relationships()`

Schema-backed relationships on `RelationshipDescriptor`:

- `source_type()`
- `target_type()`

Schema-backed relationships on `DeclaredRelationshipDescriptor`:

- `has_inverse()`

Schema-backed relationships on `InverseRelationshipDescriptor`:

- `inverse_of()`

### Dance

`DanceDescriptor` defines an affordable instance behavior. It is the descriptor-level foundation for later dance dispatch, but this spec stops at descriptor structure and lookup rather than dynamic execution or module binding.

Wrappers:

- `DanceDescriptor`

Prescribed core-schema role:

- `DanceDescriptor` should be introduced as a descriptor kind in core schema
- `HolonType` descriptors should be able to afford dances through a schema-declared relationship such as `AffordsInstanceDance`

Primary instance-facing lookup surface on `HolonDescriptor`:

```rust
fn afforded_instance_dances(&self) -> Result<Vec<DanceDescriptor>, HolonError>;

fn get_instance_dance_by_name(
    &self,
    dance_name: DanceName,
) -> Result<DanceDescriptor, HolonError>;
```

Inheritance semantics:

- instance dances inherit exactly like properties and relationships
- domain-specific `HolonType`s may add dances
- overrides and deletions are not allowed
- lookup should return the effective flattened dance affordance set, not only local declarations

Static dispatch note:

- once a dance has been resolved through descriptor lookup, execution should dispatch through descriptor-local static Rust code in this phase
- dynamic implementation loading is deferred

Current schema note:

- this behavior family is prescribed by this design and requires corresponding core-schema additions if they do not yet exist in the authoritative schema

### Command

`CommandDescriptor` defines a core command affordance. Commands are part of the descriptor foundation because they provide the stable cross-language execution surface, but unlike dances they are not domain-extensible in this phase.

Wrappers:

- `CommandDescriptor`

Prescribed core-schema role:

- `CommandDescriptor` should be introduced as a descriptor kind in core schema
- relevant core descriptor types should afford commands through a schema-declared relationship such as `AffordsCommand`

Primary instance-facing lookup surface on `HolonDescriptor`:

```rust
fn afforded_commands(&self) -> Result<Vec<CommandDescriptor>, HolonError>;

fn get_command_by_name(
    &self,
    command_name: CommandName,
) -> Result<CommandDescriptor, HolonError>;
```

Command rules:

- commands are defined by holons core, not by domain schemas
- command affordances may be inherited through `Extends`
- overrides and deletions are not allowed
- lookup should return the effective flattened command affordance set, not only local declarations

Descriptor-surface note:

- `HolonDescriptor` is the main caller-facing command lookup surface for holon instances
- other descriptor wrappers may also expose command lookup where core-defined commands are meaningful for that descriptor kind

Static dispatch note:

- once a command has been resolved through descriptor lookup, execution should dispatch through descriptor-local static Rust code in this phase
- dynamic implementation loading is deferred

Current schema note:

- this behavior family is prescribed by this design and requires corresponding core-schema additions if they do not yet exist in the authoritative schema

### Operator

`OperatorDescriptor` defines an introspectable operator available to a value type. Operators are first-class descriptor holons for discovery and UI/query introspection, but operator invocation is not modeled as a holon instance in this phase. Instead, value descriptors dispatch operator application to static Rust implementations.

Wrappers:

- `OperatorDescriptor`

Prescribed core-schema role:

- `OperatorDescriptor` should be introduced as a descriptor kind in core schema
- `ValueType` descriptors should afford operators through a schema-declared relationship such as `AffordsOperator`
- the intended shape is:
  - `(ValueTypeDescriptor) -[AffordsOperator]-> (OperatorDescriptor)`

Minimal prescribed schema-backed properties:

- `operator_name()`
- `display_name()`
- `description()`
- `arity()`
- `operator_category()`

Minimal prescribed schema-backed relationships:

- `applies_to_value_type()`

Required handwritten/runtime behavior on `ValueDescriptor`:

```rust
fn supported_operators(&self) -> Result<Vec<OperatorDescriptor>, HolonError>;

fn supports_operator(
    &self,
    operator: &OperatorDescriptor,
) -> Result<bool, HolonError>;

fn apply_operator(
    &self,
    operator: &OperatorDescriptor,
    lhs: &BaseValue,
    rhs: &BaseValue,
) -> Result<bool, HolonError>;
```

Operator rules:

- operators are core-defined, not domain-extensible
- operator affordances inherit through the value-type `Extends` chain
- `supported_operators()` is schema-driven and flattened across inheritance
- `apply_operator(...)` is descriptor-local static Rust dispatch
- there is no global operator registry
- there are no operator-instance holons in this phase

Current schema note:

- this behavior family is prescribed by this design and requires corresponding core-schema additions if they do not yet exist in the authoritative schema

### Value

`ValueDescriptor` is the first place where the descriptor layer takes on substantial runtime semantics, not just structure. Value descriptors are the intended home for validation behavior and for the operator support needed by query and filtering logic.

Base wrapper:

- `ValueDescriptor`

Likely narrower wrappers where behavior materially differs:

- `StringValueDescriptor`
- `IntegerValueDescriptor`
- `BooleanValueDescriptor`
- `BytesValueDescriptor`
- `EnumValueDescriptor`
- `ValueArrayDescriptor`

Required handwritten/runtime behavior on `ValueDescriptor`:

```rust
fn is_valid(&self, value: &BaseValue) -> Result<(), HolonError>;

fn supported_operators(&self) -> Result<Vec<OperatorDescriptor>, HolonError>;

fn supports_operator(
    &self,
    operator: &OperatorDescriptor,
) -> Result<bool, HolonError>;

fn apply_operator(
    &self,
    operator: &OperatorDescriptor,
    lhs: &BaseValue,
    rhs: &BaseValue,
) -> Result<bool, HolonError>;
```

Semantics:

- validation is descriptor-owned and implemented in Rust
- dispatch should be value-kind-specific
- invalid values should produce validation-oriented `HolonError`
- operator discovery should expose the effective inherited operator affordance set
- operator application should dispatch through descriptor-local static Rust code

This is a reallocation of behavior that would otherwise tend to sprawl into validators, query code, or other standalone helpers. The design intent is that validation operators and query operators are descriptor-owned, statically implemented, and dispatched through value descriptors rather than through a central registry.

Schema-backed additional accessors from the current core schema:

- none beyond the shared descriptor surface

Current schema deficiencies that should be corrected in follow-on core-schema work:

- integer constraint properties such as `min_value` / `max_value`
- enum variant access from `EnumValueType`
- element value type access from `ValueArrayValueType`
- operator affordance declarations from `ValueType` descriptors to `OperatorDescriptor`s

### Enum Variant

`EnumVariantDescriptor` is narrower, but still important because enum semantics ultimately need both the enum value descriptor view and the variant view. The current schema is still incomplete here, so this section is intentionally thin.

Wrapper:

- `EnumVariantDescriptor`

Schema-backed additional accessors from the current core schema:

- none beyond the shared descriptor surface

Current schema deficiency:

- the intended `variant_of()` accessor is not yet justified by the current authoritative schema and should become schema-backed through a core-schema update

### Collection

`CollectionDescriptor` is included for completeness of the `TypeKind`-organized model, even though the current authoritative core schema does not yet give it a richer descriptor-specific surface.

Wrapper:

- `CollectionDescriptor`

Schema-backed additional accessors from the current core schema:

- none

Current schema note:

- the authoritative core schema does not currently define collection-specific descriptor obligations beyond the shared descriptor surface

## Module Shape

Suggested Rust organization:

- `descriptors/mod.rs`
- `descriptors/descriptor.rs`
- `descriptors/type_header.rs`
- `descriptors/inheritance.rs`
- `descriptors/holon_descriptor.rs`
- `descriptors/property_descriptor.rs`
- `descriptors/relationship_descriptor.rs`
- `descriptors/value_descriptor.rs`
- `descriptors/generated/...`

Generated output should remain clearly separated from handwritten traversal and validation logic.

## Out of Scope

- schema evolution strategy
- dance-specific descriptor APIs
- command surface details
- TypeScript-side behavior allocation
- schema ripple workflow
