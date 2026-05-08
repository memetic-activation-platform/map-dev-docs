# Relationship Constraints Design Spec

## Purpose

This document proposes a first-class `RelationshipConstraint` model for MAP relationship descriptor semantics.

It is a companion to the `ValueConstraint` design work and reflects a broader architectural conclusion: constraints should not be treated as a value-type-only concern. Relationship descriptors also carry rule-like semantics that govern validity, structure, and behavior, and those semantics should be modeled explicitly rather than as an ad hoc set of hard-coded instance properties.

This document also clarifies an important boundary that emerged in the design discussion:

- some relationship semantics are true constraints
- some relationship semantics are intrinsic semantic markers
- ordered relationships introduce a separate need for per-target-occurrence positional data

---

## Problem Statement

`MetaRelationshipType` currently hard-codes several relationship-related semantics through `InstanceProperties`, including:

- `IsDefinitional`
- `IsOrdered`
- `AllowsDuplicates`
- `MinCardinality`
- `MaxCardinality`
- `DeletionSemantic`

These do not all belong to the same conceptual category.

In particular:

- `MinCardinality`, `MaxCardinality`, and `AllowsDuplicates` behave like constraints
- `IsDefinitional` and `DeletionSemantic` are intrinsic relationship semantics, not constraints
- `IsOrdered` is closer to an intrinsic semantic capability than a constraint, but it also implies the need to represent order position for each target occurrence

The current model therefore conflates:

- structural semantics
- validity constraints
- orderedness
- per-occurrence ordering data

This makes the ontology harder to extend and weakens the correspondence between schema design and descriptor/runtime semantics.

---

## Design Goals

The design should satisfy the following goals:

1. Introduce a first-class model for relationship constraints.
2. Separate constraints from intrinsic relationship semantics.
3. Treat orderedness as an explicit semantic capability rather than only as a boolean flag with implied behavior.
4. Define how ordered relationships capture per-target position.
5. Preserve efficient runtime execution and validation.
6. Keep the architecture aligned with the four-level MAP ontology.
7. Avoid turning relationships into arbitrary property bags unless there is a narrow, principled reason to do so.

---

## Design Summary

The design should distinguish three categories of relationship semantics.

### 1. Intrinsic Relationship Semantics

These define what the relationship means, rather than constraining allowed instances.

Examples:

- `IsDefinitional`
- `DeletionSemantic`
- `IsOrdered`

### 2. Relationship Constraints

These govern structural validity or allowed multiplicity patterns for instances of the relationship.

Examples:

- minimum cardinality
- maximum cardinality
- duplicate policy

### 3. Per-Occurrence Ordering Data

If a relationship is ordered, each target occurrence must carry some representation of its position in that order.

This is neither a pure constraint nor a pure relationship-level semantic marker. It is occurrence-level data required to realize the semantics of orderedness.

---

## Relationship Constraints as First-Class Concepts

MAP should introduce a first-class `RelationshipConstraint` concept.

A `RelationshipType` should be able to declare one or more `Constraints` relationships to relationship constraint holons, analogous to the emerging `ValueConstraint` direction for value types.

Examples of concrete relationship constraint kinds:

- `MinCardinalityConstraint`
- `MaxCardinalityConstraint`
- `DuplicatePolicyConstraint`

Each constraint holon should itself be `DescribedBy` a concrete constraint type that determines:

- its semantics
- the descriptor families it may apply to
- any payload properties required to evaluate it

This makes the rule surface explicit and extensible while preserving a bounded set of recognized executable constraints in Rust.

---

## What Should Not Be Modeled as Constraints

The following should remain intrinsic relationship semantics rather than being migrated blindly into the relationship-constraint family:

- `IsDefinitional`
- `DeletionSemantic`

These are not validity checks in the same sense as cardinality or duplicate rules. They describe core semantics of the relationship itself.

`IsOrdered` should also remain in this semantic category. It signals that:

- order among targets is meaningful
- the order should be preserved
- consumers may rely on that order
- additional operator or presentation semantics may be enabled because of orderedness

This is broader than a simple validity constraint.

---

## Ordered Relationships

### Orderedness as a Semantic Marker

`IsOrdered` should be treated as an intrinsic semantic marker on relationship descriptors.

It declares that the target set is semantically ordered. This may affect:

- presentation
- query result ordering
- operator semantics such as before/after
- editing and reordering behavior

### Orderedness Is Not Sufficient by Itself

Declaring `IsOrdered` is not enough. If order is meaningful, MAP must also define how the position of each target occurrence is represented.

Without explicit positional data, order would be left to accidental implementation details such as:

- insertion order
- creation timestamp
- incidental storage order

Those are not adequate for semantically meaningful manual ordering.

---

## Representing Per-Target Position

MAP does not currently support properties on relationships in the general case. Ordered relationships put pressure on that rule because order position is inherently occurrence-specific.

This design therefore identifies a real architectural question:

Should MAP introduce a narrow exception that allows a relationship occurrence to carry bounded metadata when the relationship semantics require it?

The current design posture is:

- do not generalize relationships into arbitrary property bags
- do allow a carefully bounded mechanism for per-occurrence metadata where required by declared semantics
- ordered relationships are the clearest first case

At this stage, the design is leaning toward direct occurrence-level metadata on the realized relationship representation rather than introducing an intermediate occurrence holon for the initial implementation.

Two modeling approaches were considered.

### Option A: Property on the Relationship Occurrence

Each target occurrence carries an explicit position property such as:

- `ordinal`
- `sequence_position`
- `order_token`

Advantages:

- direct and simple
- aligns closely with the semantic need
- easy to consume in runtime ordering logic

Tradeoffs:

- creates a targeted exception to MAP’s current “no properties on relationships” posture
- must be carefully bounded so it does not become a general escape hatch

### Option B: Intermediate Occurrence / Ordering Holon

Instead of storing position directly on the relationship occurrence, MAP could introduce a small intermediate holon representing the ordered target occurrence.

That holon would carry:

- the target reference
- the order position data
- possibly other narrowly justified occurrence-level metadata in the future

Advantages:

- preserves the principle that relationships themselves remain lean
- gives an explicit data home to occurrence-specific semantics

Tradeoffs:

- adds structural complexity
- may be heavier than necessary for the initial use case

At this stage, ordered relationships clearly require one of these two approaches. The current design bias is to start with Option A because it aligns well with SmartLink storage realization and keeps the implementation lighter, while still preserving a bounded exception rather than turning relationships into general property bags.

### Current Design Bias

The current preferred model is:

- ordered relationships may carry bounded occurrence-level metadata
- `SequencePosition` is the first built-in core occurrence property
- this metadata is attached to the realized relationship occurrence, not to the target holon
- this should be treated as a narrow semantic exception, not a general relaxation of MAP's relationship model

This also lays the foundation for possible future `RelationshipProperties` support if MAP later chooses to formalize a broader occurrence-level property model.

---

## `SequencePosition` as Core Occurrence Metadata

`SequencePosition` should be defined as a built-in core property concept for ordered relationships.

It should not be treated as:

- a cached property of the target holon
- a generic value-level constraint
- merely a UI sorting hint

It should instead be treated as authoritative occurrence-level relationship metadata.

This matters because the same target holon could appear:

- in different ordered relationships
- at different positions in different source contexts
- potentially multiple times in one relationship if duplicates are allowed

Therefore, `SequencePosition` belongs to the relationship occurrence, not to the target holon.

---

## Ordering Value Type Reuse

The concept of explicit order position should be reusable across descriptor families.

The same underlying value type or semantic pattern could be used for:

- enum variant ordinals
- ordered relationship target positions

This is desirable because both express the same general concept: explicit sequence position with stable semantic meaning.

Possible shared concepts include:

- `OrdinalValueType`
- `SequencePositionValueType`

The exact naming can be decided later, but the reuse principle is sound.

If MAP chooses to introduce a reusable core value type here, `SequencePositionValueType` is likely the better name for relationship ordering, while enum-specific modeling may still choose whether to expose `ordinal` as a dedicated semantic alias on top of the same underlying value semantics.

---

## Ordering Strategy Options

There is an important design question about how ordered positions should be represented.

### Option 1: Simple Monotonically Increasing Sequence

Example:

- `1, 2, 3, 4, 5`

Advantages:

- simple to understand
- easy to sort
- easy to validate

Tradeoffs:

- inserting between existing positions forces renumbering
- repeated edits may produce unnecessary churn
- concurrent or distributed edits may become more awkward

This is the simplest conceptual model, but it is operationally expensive if arbitrary insertion is common.

### Option 2: Gap-Based Integer Sequence

Example:

- `100, 200, 300`
- insert between `100` and `200` as `150`

Advantages:

- avoids renumbering on many inserts
- still easy to sort
- keeps the model numerically simple

Tradeoffs:

- eventually gaps can be exhausted in heavily edited regions
- periodic normalization may still be needed

This is a strong practical option if MAP wants a simple numeric ordering model with less churn.

### Option 3: Fractional / Dense Ordering Tokens

Example:

- choose a value between two neighbors rather than renumbering
- not necessarily restricted to simple integers

Advantages:

- minimizes renumbering pressure
- supports frequent mid-list inserts

Tradeoffs:

- more complex to reason about and validate
- may introduce portability or precision concerns if naively modeled as floating point

If pursued, this should be treated as an ordered-token design, not as ordinary numeric arithmetic.

### Option 4: Lexicographic Ordering Tokens

Example:

- string-like order keys designed for insertion between adjacent positions

Advantages:

- widely used in collaborative ordering systems
- very low renumbering pressure

Tradeoffs:

- more complex than a simple ordinal
- probably overkill for initial MAP core semantics unless collaborative reordering pressure is high

### Current Design Bias

For initial MAP core semantics, a gap-based integer sequence is the recommended direction:

- much simpler than generalized dense ordering tokens
- avoids forced renumbering on most inserts
- keeps sort and validation semantics straightforward
- is more than sufficient for realistic manually ordered sets

The recommended refinement is:

- represent position as an integer `sequence_position`
- assign initial positions using a fixed stride rather than consecutive integers
- prefer a stride with good midpoint headroom, such as `1024`
- insert between adjacent positions by assigning the integer midpoint when one exists
- if no midpoint exists, renormalize the relevant ordered sequence locally to restore spacing

Example:

- initial positions: `1024, 2048, 3072`
- insert between `1024` and `2048` -> `1536`
- insert between `1024` and `1536` -> `1280`
- insert between `1024` and `1280` -> `1152`

This gives MAP a simple, deterministic ordering model that keeps inserts cheap in the common case without introducing fractional or lexicographic ordering tokens.

The design should still keep open whether renormalization is:

- sequence-wide within one ordered relationship instance
- localized to a small affected neighborhood

but the core ordering strategy itself is now fairly clear.

---

## SmartLink Storage Realization

Ordered relationship semantics have direct implications for storage realization because relationships are currently persisted as Holochain `Links` using the `SmartLink` link type.

`SmartLinks` already serve as the concrete storage-level realization of relationship occurrences and already encode query-relevant metadata in the `LinkTag` body to support:

- filtering
- ordering
- pagination
- reduced need to fetch target holons

This makes `SmartLink` the natural home for ordered relationship occurrence metadata such as `SequencePosition`.

### Two Distinct Property Maps

The current SmartLink design uses one `smart_property_values` map. The updated design should distinguish two semantically different categories of values:

- `relationship_property_values`
  - authoritative occurrence-level metadata carried by the relationship realization itself
  - examples: `SequencePosition`
- `target_property_values`
  - cached values copied from the target holon for query optimization
  - examples: cached key/display/filter/sort properties

These two maps have different semantics:

- `relationship_property_values` are authoritative and non-recoverable from the target holon
- `target_property_values` are opportunistic cache values and are recoverable by fetching the target holon

Because of that difference, they should not be treated as one undifferentiated property bag.

### LinkTag Encoding Priority

Holochain `LinkTag`s are limited to roughly 1 KB. That means encoding order and loss policy must be explicit.

The encoding priority should be:

1. SmartLink structural fields
2. relationship occurrence properties
3. cached target property values

This yields the following design rules:

- required relationship occurrence properties must be encoded first
- failure to fit required relationship occurrence properties is an error
- failure to fit optional cached target values is acceptable
- cached target values may be truncated or omitted when the `LinkTag` budget is exhausted

This is especially important for ordered relationships because `SequencePosition` has no alternate storage home if it is omitted.

### Storage Semantics

The SmartLink body should no longer be understood only as a cache of target properties.

It should instead be understood as containing:

- required relationship-occurrence metadata
- optional cached target metadata

That reframing is important because it accurately reflects both semantics and storage priority.

### Suggested SmartLink Evolution

The concrete runtime/storage representation may evolve toward a structure like:

```rust
struct LinkTagObject {
    relationship_name: String,
    proxy_id: Option<OutboundProxyId>,
    relationship_property_values: Option<PropertyMap>,
    target_property_values: Option<PropertyMap>,
}
```

The exact field names can be refined, but the semantic split should be preserved.

---

## Ordering Assignment Semantics

The blast radius of ordered relationships extends beyond descriptor semantics into the full lifecycle of how ordering is assigned, adjusted, and maintained.

The design should therefore define explicit ordering assignment semantics rather than leaving position creation as an implementation detail.

### Creation Cases

For ordered relationships, `SequencePosition` must be assigned at write time.

The basic cases are:

- create first occurrence in an empty ordered relationship
- append after the current tail
- prepend before the current head
- insert between two existing occurrences
- move an existing occurrence to a new position

### Recommended Assignment Rules

Using the current preferred gap-based integer model:

- first occurrence receives an initial canonical position such as `1024`
- append assigns `tail + stride`
- prepend assigns `head - stride`
- insert between neighbors assigns the integer midpoint when one exists
- move operations should usually be treated as remove-and-reinsert for ordering purposes

This keeps ordering assignment deterministic and easy to reason about.

### Midpoint Exhaustion

If two adjacent sequence positions differ by `1`, no integer midpoint exists.

In that case, the implementation should:

1. renormalize the relevant ordered sequence or affected neighborhood
2. restore spacing using the configured stride
3. retry the intended insert or move

This makes exhaustion a maintenance event rather than a semantic failure.

### Canonical Stride

The implementation should standardize an initial stride value for newly normalized or newly created ordered sequences.

The current recommendation is to use a stride such as `1024` because it:

- provides good midpoint headroom
- remains integer-only
- keeps values easy to sort and inspect

The exact canonical stride can still be finalized in implementation work, but it should be treated as part of the storage/commit contract rather than as an arbitrary UI concern.

---

## Commit Processing Implications

Ordered relationships also have a direct ripple effect on commit processing.

If a relationship is ordered, relationship-creation and relationship-update flows must manage `SequencePosition` explicitly.

Examples:

- creating the first target occurrence in an ordered relationship must assign an initial `SequencePosition`
- appending a target should assign a position after the current tail
- inserting between two existing targets should assign the integer midpoint when available
- if no midpoint exists, local renormalization should occur before completing the update
- reordering operations must update the affected SmartLinks

This means orderedness is not just a query concern. It affects:

- storage encoding
- mutation logic
- validation
- query execution

### Commit-Time Responsibilities

Commit processing for ordered relationships should explicitly own the following responsibilities:

- determine whether the relationship descriptor is ordered
- determine the intended insertion or move semantics
- compute the correct `SequencePosition`
- encode that value into required relationship-occurrence metadata
- persist the updated SmartLink realization
- trigger local renormalization when no midpoint is available

### Operation Shapes

At the operation level, MAP will likely need to support concepts such as:

- append target
- prepend target
- insert target before another target
- insert target after another target
- move target before another target
- move target after another target

Even if these are not all surfaced as first-class public commands immediately, the commit layer should be designed with these semantic cases in mind.

### Validation Expectations

If `IsOrdered == true`, then validation should ensure:

- each ordered relationship occurrence has a valid `SequencePosition`
- ordering values are well-formed integers
- ordering values satisfy any uniqueness/consistency expectations required by the chosen model

If `IsOrdered == false`, `SequencePosition` should normally be absent unless a future design explicitly permits it for some other reason.

### Inverse Relationship Limitation

Inverse relationships introduce an important constraint on orderedness.

Inverse relationship occurrences are auto-populated as a side effect of committing the declared relationship occurrence. That means the inverse side has no independent authoring moment in which a caller can specify manual ordering intent such as:

- append here
- insert before another target
- move after another target

Because manual semantic ordering requires an explicit write-time ordering decision, auto-populated inverse relationships do not provide a coherent place to supply that intent.

Therefore:

- inverse relationship types should not declare `IsOrdered == true`
- `IsOrdered == true` on an inverse relationship type should be treated as descriptor-invalid

This does not mean inverse traversal must be random. Inverse retrieval may still apply a deterministic presentation or query ordering policy, such as sorting by:

- creation time
- target key
- another explicit retrieval-time sort choice

However, such ordering is not the same as semantically meaningful manual relationship ordering and should not be modeled as inverse-side `SequencePosition`.

---

## Ordering Retrieval Semantics

The blast radius also extends to how ordered relationships are read back and exposed to higher layers.

If MAP persists `SequencePosition`, then retrieval APIs and query flows must treat it as part of the authoritative relationship realization.

### Retrieval from SmartLinks

For ordered relationships, retrieval should:

1. read the SmartLinks for the relationship
2. decode required relationship-occurrence properties
3. extract `SequencePosition`
4. sort or preserve ordering according to that value
5. only then resolve or hydrate target holons as needed

This ensures that ordering can be realized without fetching target holons first.

### Query Engine Implications

The query engine should be able to:

- respect explicit relationship order by default when traversing an ordered relationship
- sort on `SequencePosition` directly from SmartLink metadata
- paginate ordered results without target fetches solely for ordering purposes

This is one of the strongest reasons to keep `SequencePosition` in the SmartLink realization itself.

### Relationship Navigation Expectations

Higher-level relationship navigation APIs should be clear about whether they:

- preserve descriptor-defined order
- return an unordered set
- allow caller-requested alternate sorting

For ordered relationships, the default navigation posture should generally preserve explicit sequence order unless the caller explicitly asks for another ordering mode.

For inverse relationships, navigation may still choose a deterministic retrieval order, but this should be understood as a retrieval policy rather than as semantic manual ordering.

### Fallback and Integrity Behavior

Because `SequencePosition` is authoritative occurrence metadata, retrieval should not silently ignore malformed or missing ordering data on an ordered relationship.

Instead, ordered retrieval should surface:

- descriptor/relationship invalidity
- malformed occurrence metadata
- missing required sequence position

as explicit errors or invalid-state outcomes, rather than degrading into incidental link order.

---

## Ordering Storage and Retrieval Contract

Taken together, the ordered relationship design implies a concrete contract spanning write path, storage, and read path.

### Set

Order is set by commit-time logic that assigns or updates `SequencePosition` based on ordered relationship semantics.

### Store

Order is stored as authoritative occurrence-level metadata inside the SmartLink realization, with priority over optional target-property caches.

### Retrieve

Order is retrieved by decoding `SequencePosition` from SmartLink metadata and using it as the canonical basis for ordered navigation, sorting, and pagination.

This contract should be made explicit because ordered relationships are not fully specified unless all three phases are defined together.

---

## Relationship Constraints and Runtime Execution

As with value constraints, relationship constraints should be modeled declaratively in schema space but executed through bounded, statically implemented Rust logic.

The high-level runtime flow should be:

1. resolve the `RelationshipType`
2. resolve intrinsic relationship semantics
3. resolve declared `RelationshipConstraint` holons
4. validate compatibility and descriptor correctness
5. compile recognized executable constraints into an internal plan
6. resolve any orderedness-related occurrence metadata requirements
7. apply those semantics during relationship validation and related operations
8. expose retrieval-time helpers or expectations for ordered relationship traversal

Examples of compiled relationship constraints could include:

```rust
enum CompiledRelationshipConstraint {
    MinCardinality { value: u32 },
    MaxCardinality { value: u32 },
    DuplicatePolicy { allows_duplicates: bool },
}
```

Orderedness itself may compile into semantic flags or ordering helpers rather than into the same enum family as constraints.

For ordered relationships, runtime behavior should also have access to the occurrence-level ordering metadata model and its storage/normalization rules.

---

## Four-Level Ontology Considerations

The placement of `Constraints` in the four-level MAP ontology should be considered carefully.

This document recommends:

- do not define `Constraints` only on `MetaValueType`
- prefer a generalized `Constraints` pattern high enough in the descriptor hierarchy to support both value and relationship descriptors
- use concrete constraint types and kind-specific meta typing to narrow valid applicability

This allows:

- `ValueType` to declare value constraints
- `RelationshipType` to declare relationship constraints
- future descriptor families to reuse the same pattern where appropriate

At the same time, there is a good case for introducing more kind-specific meta types over time, such as:

- `MetaIntegerValueType`
- `MetaStringValueType`
- `MetaEnumValueType`

and, if justified:

- more specific meta relationship subfamilies

These would help express kind-specific obligations and compatibility rules cleanly, but they should not force duplication of the generalized `Constraints` pattern itself.

---

## Suggested Initial Relationship Constraint Set

The first executable relationship-constraint set should stay narrow.

Recommended initial candidates:

- `MinCardinalityConstraint`
- `MaxCardinalityConstraint`
- `DuplicatePolicyConstraint`

Recommended initial intrinsic semantics to keep distinct:

- `IsDefinitional`
- `DeletionSemantic`
- `IsOrdered`

This preserves conceptual clarity while recovering the most important currently hard-coded relationship rule semantics.

---

## Open Design Questions

The follow-on design work should resolve:

1. Should ordered-target position be stored directly on the relationship occurrence or on an intermediate occurrence holon?
2. What is the best exact schema shape for `SequencePosition` and its reusable value semantics across enums and relationships?
3. What is the best initial ordering representation:
   - simple monotonic sequence
   - gap-based integer sequence
   - dense/fractional ordering token
   - lexicographic ordering token
4. Should MAP standardize one shared ordering value type for enum variant ordinal and ordered relationship position?
5. How should SmartLink tag grammar distinguish relationship-occurrence properties from cached target properties?
6. What exact truncation/overflow behavior should apply when optional target cache values exceed `LinkTag` space limits?
7. What exact API/command surface should MAP expose for append/prepend/insert/move semantics?
8. Should ordered relationship retrieval always preserve explicit order by default, or should that remain caller-selectable?
9. Which exact relationship semantics belong in the constraint family versus the intrinsic semantic family?
10. How should orderedness interact with operator affordances such as before/after and possibly relational comparisons?
11. What runtime validation and normalization rules should apply to ordered relationships?
12. Should inverse traversal define a standard deterministic default ordering policy even though inverse relationships are not semantically ordered?

---

## Recommended Next Steps

1. Align this spec with the `ValueConstraint` design work under a generalized descriptor-constraint architecture.
2. Define `SequencePosition` as a built-in core occurrence property for ordered relationships.
3. Update SmartLink modeling to distinguish relationship-occurrence properties from cached target properties.
4. Define LinkTag encoding priority so required relationship metadata is encoded before optional target caches.
5. Define ordering assignment semantics for create/append/prepend/insert/move operations.
6. Define retrieval semantics so ordered relationship traversal reads `SequencePosition` from SmartLinks as the authoritative basis for ordering.
7. Add the descriptor-validity rule that inverse relationship types cannot declare `IsOrdered == true`.
8. Choose the initial ordering representation and normalization policy.
9. Define the first relationship-constraint schema types and their payload properties.
10. Update `MetaRelationshipType` so that true constraints are no longer represented only as a hard-coded bag of instance properties.
11. Preserve `IsDefinitional`, `DeletionSemantic`, and `IsOrdered` as intrinsic semantics unless later analysis justifies a different posture.

---

## Conclusion

MAP should generalize its emerging constraint architecture beyond values and introduce a first-class `RelationshipConstraint` family.

At the same time, the design should avoid collapsing every relationship-related semantic into the constraint bucket. `IsDefinitional`, `DeletionSemantic`, and `IsOrdered` are better understood as intrinsic semantics. Orderedness in particular raises a separate and important design requirement: MAP must define how per-target position is represented without carelessly abandoning its preference for lean relationships.

The current design direction is to treat `SequencePosition` as authoritative occurrence-level metadata carried by the realized relationship representation, with SmartLink evolving to encode required relationship properties before optional cached target properties.

The resulting blast radius is intentionally broad: ordered relationship design must define how order is assigned, stored, retrieved, validated, and consumed by query/navigation layers. That distinction between constraints, intrinsic semantics, occurrence-level ordering data, and target-cached query metadata is the key to keeping the relationship descriptor model expressive, principled, and implementable.
