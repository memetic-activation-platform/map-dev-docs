# Descriptors Design Spec (v1.3)

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

## Change Log

### v1.3

- added an explicit relationship persistence policy requiring inverse materialization to be treated as part of the semantic relationship commitment
- clarified that the runtime must not silently commit only the forward side when inverse materialization is required by descriptor semantics
- specified that unresolved non-local inverse materialization must become durable deferred-repair work with detection and remediation rather than an undiagnosed one-sided steady state

### v1.2

- introduced the v1.2 descriptor runtime model and its TypeKind-organized descriptor surface

## Scope

It is intentionally narrow and normative. Background material, rollout process, behavior allocation, and schema ripple process belong in the companion specs.

The organizing principle here is `TypeKind`: the main contract is what descriptor wrapper exists for each kind, what operations it exposes, and what schema-backed accessors it should provide.

Instead of leaving key operations as freestanding helpers or central registries, the design moves those operations onto descriptor wrappers themselves. That includes convenience lookup methods, inheritance flattening, validation-oriented behavior, and the static dispatch points needed for later dance/command and query/operator support.

### Domain-Definability Policy

Domain-definability is a MAP Core policy attached to `TypeKind`, not a schema-declared `InstanceProperty` that every type descriptor must carry.

The core schema records persistent type definitions. MAP Core Rust code
interprets each type definition's declared `type_kind` through the Rust
`TypeKind` model. That Rust model is the authoritative source for whether a
non-core domain author may define new types of that kind.

This policy is evaluated when a caller attempts to define a new type.

Initial posture:

- `Holon`, `Property`, `Relationship`, `Value`, `ValueArray`, `EnumVariant`, `Collection`, and `Dance` are domain-definable where otherwise permitted by schema validation and security policy.
- `Command` and `Operator` are core-defined only, not domain-definable.
- Command and operator inventories evolve with MAP Core versions and their Rust implementations.

The descriptor layer may expose command and operator discovery through schema-backed descriptors, but it must not treat command or operator type creation as a domain-definable extension point.

### TypeKind-Specific Names

Every descriptor exposes the shared descriptor header, including `type_name`. When a runtime API identifies a descriptor by name, it should use a TypeKind-specific Rust name wrapper rather than raw `MapString`.

TypeKind-specific name wrappers provide two guarantees:

- they prevent accidental cross-family name usage, such as passing a property name where a command name is required
- they centralize the naming convention for that TypeKind

For TypeKinds that already have schema-backed name properties, such as `PropertyName`, `RelationshipName`, and `DanceName`, the wrapper should continue to expose that schema-backed name. For command and operator descriptors, no separate schema-backed name property is introduced in this phase. Instead:

- `CommandName` is a Rust wrapper over the concrete `CommandType` descriptor's shared `type_name`
- `OperatorName` is a Rust wrapper over the concrete `OperatorType` descriptor's shared `type_name`
- `CommandDescriptor::command_name()` should derive `CommandName` from the shared descriptor header
- `OperatorDescriptor::operator_name()` should derive `OperatorName` from the shared descriptor header

Because commands and operators are core-defined only, their stable name inventories should be represented in MAP Core Rust code through TypeKind-specific core name enums such as `CoreCommandTypeName` and `CoreOperatorTypeName`. These enums are implementation aids for known core names; they do not replace the schema-backed descriptor holons.

Descriptor lookup APIs should match the ergonomics already provided by the reference layer. Name-based descriptor accessors should accept conversion traits such as `ToPropertyName`, `ToRelationshipName`, `ToDanceName`, `ToCommandName`, and `ToOperatorName` rather than forcing callers to manually construct wrapper values at every call site.

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
- Every runtime descriptor wrapper is a thinly typed view over a backing `HolonReference`.
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
pub trait ReadableHolon {
    fn holon_descriptor(&self) -> Result<HolonDescriptor, HolonError>;
}
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
- `Extends` confers type inheritance: structural obligations and affordance declarations may be flattened across the inheritance chain.
- `Extends` does not confer value inheritance for descriptor-instance property values such as shared header fields or governance markers.
- Callers should experience a flattened effective descriptor view for inherited structure and affordances.
- Normal descriptor use must not require caller-side `Extends` walking.
- Descriptor wrappers should not store a constructor-time cached `extends_chain`.

Flattening the `Extends` hierarchy is one of the core ergonomic promises of the descriptor layer. Callers should ask for the effective property, relationship, affordance, or rule they need and get a descriptor-level answer, not a chain they must interpret themselves. This flattening applies to declared type structure, not to the values populated on individual descriptor holons.

Traversal rules:

- include `self` first
- walk parent-ward until no `Extends` target exists
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

- `InstanceDance`: domain-definable behavior afforded by holon types
- `Command`: core-defined behavior afforded by holon types, but not domain-definable
- `Operator`: core-defined semantic affordances of value types

All three families follow the same inheritance posture:

- affordances flatten across `Extends`
- callers should not reconstruct inherited behavior themselves
- no override
- no deletion
- duplicate redeclaration is invalid

They differ in where they are declared:

- `InstanceDance` is afforded by `HolonType` descriptors
- `Command` is afforded by `HolonType` descriptors and inherited by their descendants
- `Operator` is afforded by `ValueType` descriptors

Dynamic execution/binding of dances and commands is deferred. The concern of this spec is descriptor structure, affordance lookup, and the static runtime surfaces on which later dispatch will attach.

## Behavior Ownership Matrix

The table below makes explicit where the behavior promised by this spec lives.

| Behavior                            | Owning Runtime Descriptor                                  |
|-------------------------------------|------------------------------------------------------------|
| Property lookup by name             | `HolonDescriptor`                                          |
| Relationship lookup by name         | `HolonDescriptor`                                          |
| Inverse relationship lookup by name | `HolonDescriptor`                                          |
| Instance dance lookup               | `HolonDescriptor`                                          |
| Property-to-value semantic bridge   | `PropertyDescriptor`                                       |
| Value validation                    | `ValueDescriptor`                                          |
| Operator discovery                  | `ValueDescriptor`                                          |
| Operator support check              | `ValueDescriptor`                                          |
| Operator application                | `ValueDescriptor`                                          |
| Command lookup                      | descriptor wrappers via shared behavior affordance support |
| Relationship structural semantics   | `RelationshipDescriptor`                                   |

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

- `OperatorType`: a descriptor holon that defines an available operator
- operator invocation: a runtime method call on a descriptor, not a holon instance

Initial operator posture:

- operators are core-defined, not domain-definable
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

All descriptor wrappers should expose the shared structural accessors implied by
the v2.0 descriptor model: `TypeHeader` plus the common descriptor
relationships rooted at `DescriptorRoot`.

This shared surface is what makes descriptor wrappers feel coherent as a family. It gives every descriptor the same basic type-introspection vocabulary while leaving kind-specific behavior to the sections below.

### Shared properties

- `type_name()`
- `type_name_plural()`
- `display_name()`
- `display_name_plural()`
- `description()`
- `type_kind()`
- `is_abstract_type()`

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

```text
fn get_property_by_name<N: ToPropertyName>(
    &self,
    property_name: N,
) -> Result<PropertyDescriptor, HolonError>;

fn get_relationship_by_name<N: ToRelationshipName>(
    &self,
    relationship_name: N,
) -> Result<RelationshipDescriptor, HolonError>;

fn get_inverse_relationship_by_name<N: ToRelationshipName>(
    &self,
    declared_relationship_name: N,
) -> Result<RelationshipDescriptor, HolonError>;

fn afforded_instance_dances(&self) -> Result<Vec<DanceDescriptor>, HolonError>;

fn get_instance_dance_by_name<N: ToDanceName>(
    &self,
    dance_name: N,
) -> Result<DanceDescriptor, HolonError>;

fn afforded_commands(&self) -> Result<Vec<CommandDescriptor>, HolonError>;

fn get_command_by_name<N: ToCommandName>(
    &self,
    command_name: N,
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

```text
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

### Relationship Persistence Policy

Inverse relationships are part of the semantic meaning of a committed relationship occurrence, not an optional local cache effect.

When a declared relationship has an inverse, the runtime should treat the forward occurrence and the inverse occurrence as one logical relationship commitment.

Normative policy:

- the system must not silently commit only the forward relationship occurrence when the inverse occurrence is required by descriptor semantics
- if both relationship endpoints are locally resolvable, commit-time persistence should materialize both directions in the same semantic operation
- inability to resolve a non-local target for inverse materialization must be surfaced as unresolved semantic work, not treated as successful completion of a one-sided relationship write
- unresolved inverse materialization for a non-local target should create a durable deferred-repair item that can be retried when the relevant trust channel, agent, or identifier-resolution path becomes available
- if identifier resolution such as `ExternalId` support exists for establishing the relationship, it should be applicable symmetrically to both directions rather than being treated as a forward-only exception path
- runtimes should provide detection and remediation of deferred inverse materialization work rather than leaving one-sided relationship state as an undiagnosed steady state

This policy allows eventual consistency across membranes without redefining semantic consistency as "forward-only writes succeed and inverse writes are skipped."

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

- `DanceType` is the schema type for dance descriptors
- Rust should expose `DanceType` holons through the `DanceDescriptor` wrapper
- `HolonType` descriptors should be able to afford dances through a schema-declared relationship such as `AffordsInstanceDance`

Primary instance-facing lookup surface on `HolonDescriptor`:

```text
fn afforded_instance_dances(&self) -> Result<Vec<DanceDescriptor>, HolonError>;

fn get_instance_dance_by_name<N: ToDanceName>(
    &self,
    dance_name: N,
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

`CommandType` defines a core command affordance. Commands are part of the descriptor foundation because they provide the stable cross-language execution surface, but unlike dances they are not domain-definable in this phase.

Wrappers:

- `CommandDescriptor`

Prescribed core-schema role:

- `CommandType` should be introduced as the schema type for command descriptors
- Rust should expose `CommandType` holons through the `CommandDescriptor` wrapper
- the existing `map_commands_contract::CommandDescriptor` lifecycle metadata type should be named `CommandLifecyclePolicy` so `CommandDescriptor` is reserved for the schema-backed descriptor wrapper
- stable MAP command identities should be represented as thin concrete `CommandType` holons using the shared `TypeHeader` surface unless a later phase introduces richer metadata
- concrete `CommandType` holons should be defined at the stable leaf command identity, not at a collapsed command-family or handler-label level
- command-envelope identities that carry richer request semantics, such as dance or query execution commands, are still `CommandType`s; the command type describes the MAP Commands API entrypoint, while dance and query descriptor families own the invoked behavior semantics
- relevant core `HolonType` descriptors should afford commands through a schema-declared relationship such as `AffordsCommand`
- schema command inventory and command affordance anchoring are separate obligations: stable leaf MAP Commands should have `CommandType` holons even when their runtime target does not yet have a schema-backed `HolonType` affordance anchor
- the intended relationship shape is:
  - `(HolonType) -[AffordsCommand]-> (CommandType)`
  - `(CommandType) -[AffordedBy]-> (HolonType)`
- the declared relationship name includes `Command` because `HolonType` descriptors may afford multiple behavior families; the inverse may use `AffordedBy` because relationship identity is the fully qualified source/name/target shape

Primary instance-facing lookup surface on `HolonDescriptor`:

```text
fn afforded_commands(&self) -> Result<Vec<CommandDescriptor>, HolonError>;

fn get_command_by_name<N: ToCommandName>(
    &self,
    command_name: N,
) -> Result<CommandDescriptor, HolonError>;
```

Command rules:

- commands are defined by holons core, not by domain schemas
- command lookup by name matches the concrete `CommandType`'s shared `type_name`
- command lookup should normalize internally to the same canonical value used by the command descriptor's `type_name`
- `CommandDescriptor::command_name()` should derive `CommandName` from the shared descriptor header
- no separate `CommandName` schema property is prescribed in this phase
- concrete command `type_name` values should use stable UpperCamel leaf command identities rather than runtime handler labels
- command affordances may be inherited through `Extends`
- overrides and deletions are not allowed
- lookup should return the effective flattened command affordance set, not only local declarations

Descriptor-surface note:

- `HolonDescriptor` is the main caller-facing command lookup surface for holon instances
- command affordance lookup is intentionally scoped to holon-type descriptors in this phase
- `TransactionType` is the core `HolonType` anchor for transaction-scoped command affordances

Static dispatch note:

- once a command has been resolved through descriptor lookup, execution should dispatch through descriptor-local static Rust code in this phase
- dynamic implementation loading is deferred

Current schema note:

- this behavior family is prescribed by this design and requires corresponding core-schema additions if they do not yet exist in the authoritative schema

### Transaction

`TransactionType` defines the core transaction model: the descriptor-backed API surface for transaction-scoped command affordances. It is a core `HolonType`, not a new `TypeKind`, and not the schema type of live transaction contexts.

`TransactionType` exists so transaction-scoped MAP Commands can be discovered through the same descriptor-local affordance surface as other commands. It is the schema type of the transaction command scope, not the instance shape of `TransactionContext`.

Runtime `TransactionContext` values, SDK `MapTransaction` handles, wire-layer transaction identity, nursery state, staging state, transient state, lifecycle state, and execution guards remain runtime/execution concerns. The fields and methods of live runtime transaction structs are not inferred into `TransactionType`, and should not be reflected as `TransactionDescriptor` accessors merely because they exist on runtime execution objects.

Persistent transaction records are a distinct design concept. This descriptor design reserves `TransactionType` for the core transaction model: the descriptor-backed command-scope API surface afforded by `HolonSpaceType`. It does not currently define persisted transaction-record instances. A future transaction-record/audit design may either introduce a separate `TransactionRecordType` or explicitly revise the meaning of `TransactionType`; that choice is not implied by this descriptor model.

Wrappers:

- `HolonSpaceDescriptor`
- `TransactionDescriptor`

`HolonSpaceDescriptor` is the Rust descriptor wrapper over the core `HolonSpaceType` holon. It is the descriptor-local home for space-specific schema affordances, including discovery of the transaction model afforded by a holon space.

`TransactionDescriptor` is the Rust descriptor wrapper over the core `TransactionType` holon. It is not a wrapper over a live `TransactionContext`, not a persisted transaction instance, not a transaction audit/record holon, and not the SDK-facing `MapTransaction`.

Core-schema role:

- `HolonSpaceType` is a concrete core `HolonType`
- Rust exposes `HolonSpaceType` holons through the `HolonSpaceDescriptor` wrapper
- `HolonSpaceDescriptor` remains a thin typed view over `HolonReference`
- `TransactionType` is a core `HolonType`
- Rust exposes `TransactionType` holons through the `TransactionDescriptor` wrapper
- `TransactionDescriptor` remains a thin typed view over `HolonReference`
- `HolonSpaceType` affords exactly one transaction model through:
  - `(HolonSpaceType) -[AffordsTransactionModel]-> (TransactionType)`
- the inverse relationship is:
  - `(TransactionType) -[TransactionModelAffordedBy]-> (HolonSpaceType)`
- `AffordsTransactionModel` identifies the transaction command-scope API surface available from a holon space
- `TransactionModelAffordedBy` identifies the holon-space type that affords a transaction model without implying lifecycle containment or ownership of `TransactionType`
- `AffordsTransactionModel` uses deletion semantic `Allow`; deleting or replacing the source `HolonSpaceType` does not delete, block on, or cascade to the target `TransactionType`
- `TransactionModelAffordedBy` also uses deletion semantic `Allow`; deleting or replacing the source `TransactionType` does not delete, block on, or cascade to the target `HolonSpaceType`
- the relationship declares the model afforded by a space, not ownership or lifecycle containment of the model type
- `TransactionType` affords transaction-scoped command descriptors through the existing command affordance relationship shape:
  - `(HolonType) -[AffordsCommand]-> (CommandType)`
  - `(CommandType) -[AffordedBy]-> (HolonType)`
- `TransactionType` affords every stable transaction-scoped MAP Command in the current MAP Core command inventory:
  - `Commit`
  - `UndoLast`
  - `RedoLast`
  - `UndoToMarker`
  - `RedoToMarker`
  - `LoadHolons`
  - `Dance`
  - `Query`
  - `GetAllHolons`
  - `GetStagedHolonByBaseKey`
  - `GetStagedHolonsByBaseKey`
  - `GetStagedHolonByVersionedKey`
  - `GetTransientHolonByBaseKey`
  - `GetTransientHolonByVersionedKey`
  - `GetStagedCount`
  - `GetTransientCount`
  - `NewHolon`
  - `StageNewHolon`
  - `StageNewFromClone`
  - `StageNewVersion`
  - `StageNewVersionFromId`
  - `DeleteHolon`
- `HolonSpaceType` continues to afford `BeginTransaction`; `TransactionType` affords commands that require an open transaction context

Primary transaction-facing lookup surface:

```text
impl HolonSpaceDescriptor {
    fn transaction_model(&self) -> Result<TransactionDescriptor, HolonError>;
}

impl TransactionDescriptor {
    fn afforded_commands(&self) -> Result<Vec<CommandDescriptor>, HolonError>;

    fn get_command_by_name<N: ToCommandName>(
        &self,
        command_name: N,
    ) -> Result<CommandDescriptor, HolonError>;
}
```

Transaction rules:

- `HolonSpaceDescriptor` is the descriptor-local owner for holon-space-specific schema affordances
- `TransactionType` is defined by MAP Core, not by domain schemas
- `TransactionType` is not domain-definable even though it is a concrete `HolonType`
- domain schemas may not define alternate transaction-scope types or domain-specific subtypes of `TransactionType`
- transaction-scoped command affordances are core-defined and evolve with MAP Core command inventory
- the transaction model afforded by `HolonSpaceType` is core-defined and not domain-definable
- `TransactionType` command discovery is descriptor-local and schema-backed
- runtime `TransactionContext` instances are not instances of `TransactionType`
- `TransactionDescriptor` exposes descriptor-local command discovery, not live transaction state
- transaction-record/audit holons, if introduced, require an explicit transaction-record design decision rather than being implied by the command-scope `TransactionType` model
- `TransactionDescriptor` is the descriptor-local owner for transaction-scoped command discovery and the future static dispatch attachment point for transaction-scoped commands

Runtime discovery path:

- a `HolonSpace` instance resolves its descriptor through `DescribedBy`
- the resulting `HolonDescriptor` may be narrowed to `HolonSpaceDescriptor` when the descriptor holon is `HolonSpaceType`
- `HolonSpaceDescriptor::transaction_model()` resolves the exactly-one afforded `TransactionType`
- the resolved `TransactionType` holon is wrapped as `TransactionDescriptor`
- `TransactionContext` may expose convenience access to the same descriptor by delegating through its bound holon space, but that convenience does not make `TransactionContext` an instance of `TransactionType`

Descriptor contract invariants:

- `TransactionType` is a core `HolonType`
- `HolonSpaceDescriptor` is constructible from the `HolonSpaceType` holon
- `TransactionDescriptor` is constructible from the `TransactionType` holon
- `HolonSpaceDescriptor::transaction_model()` resolves the exactly-one `TransactionType` afforded by `HolonSpaceType`
- `TransactionDescriptor::afforded_commands()` returns every current transaction-scoped MAP Command
- `TransactionDescriptor::get_command_by_name(...)` resolves commands by canonical `CommandName`
- `BeginTransaction` is not afforded by `TransactionType`
- `BeginTransaction` is afforded by `HolonSpaceType`
- the command affordance relationship shape is schema-backed through `(HolonType)-[AffordsCommand]->(CommandType)` and `(CommandType)-[AffordedBy]->(HolonType)`

### Operator

`OperatorType` defines an introspectable operator available to a value type. Operators are first-class descriptor holons for discovery and UI/query introspection, but operator invocation is not modeled as a holon instance in this phase. Instead, value descriptors dispatch operator application to static Rust implementations.

Wrappers:

- `OperatorDescriptor`

Prescribed core-schema role:

- `OperatorType` is the schema type for operator descriptors
- Rust should expose `OperatorType` holons through the `OperatorDescriptor` wrapper
- `ValueType` descriptors should afford operators through a schema-declared relationship such as `AffordsOperator`
- the intended shape is:
  - `(ValueType) -[AffordsOperator]-> (OperatorType)`

Minimal prescribed schema-backed accessors:

- `operator_name()` for stable operator identity, derived from the shared descriptor header's `type_name`
- `display_name()`
- `description()`
- `arity()`
- `operator_category()`

Minimal prescribed schema-backed relationships:

- `afforded_by()`

Required handwritten/runtime behavior on `ValueDescriptor`:

```text
fn supported_operators(&self) -> Result<Vec<OperatorDescriptor>, HolonError>;

fn get_operator_by_name<N: ToOperatorName>(
    &self,
    operator_name: N,
) -> Result<OperatorDescriptor, HolonError>;

fn supports_operator_by_name<N: ToOperatorName>(
    &self,
    operator_name: N,
) -> Result<bool, HolonError>;

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

- operators are core-defined, not domain-definable
- `OperatorDescriptor::operator_name()` should derive `OperatorName` from the shared descriptor header
- no separate `OperatorName` schema property is prescribed in this phase
- operator affordances inherit through the value-type `Extends` chain
- `supported_operators()` is schema-driven and flattened across inheritance
- name-based operator lookup and support checks should accept `ToOperatorName`
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

```text
fn is_valid(&self, value: &BaseValue) -> Result<(), HolonError>;

fn supported_operators(&self) -> Result<Vec<OperatorDescriptor>, HolonError>;

fn get_operator_by_name<N: ToOperatorName>(
    &self,
    operator_name: N,
) -> Result<OperatorDescriptor, HolonError>;

fn supports_operator_by_name<N: ToOperatorName>(
    &self,
    operator_name: N,
) -> Result<bool, HolonError>;

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
- name-based operator lookup should resolve through the same effective inherited operator affordance set
- operator application should dispatch through descriptor-local static Rust code

This is a reallocation of behavior that would otherwise tend to sprawl into validators, query code, or other standalone helpers. The design intent is that validation operators and query operators are descriptor-owned, statically implemented, and dispatched through value descriptors rather than through a central registry.

Schema-backed additional accessors from the current core schema:

- none beyond the shared descriptor surface

Current schema deficiencies that should be corrected in follow-on core-schema work:

- integer constraint properties such as `min_value` / `max_value`
- enum variant access from `EnumValueType`
- element value type access from `ValueArrayValueType`
- operator affordance declarations from `ValueType` descriptors to `OperatorType` holons

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
