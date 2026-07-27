# MAP Type Definition Language (TDL) Specification v0.6

## ChangeLog

Entries before `v0.6` describe the model implemented by those historical revisions. Where they
conflict, the `v0.6` rules are authoritative.

- `v0.6`

  - aligns TDL lowering and validation with the Schema 2.0 two-hierarchy model rooted at
    `MetaTypeDescriptor` and abstract `TypeDescriptor`
  - removes general `TypeKind` compatibility from `Extends` validation
  - separates descriptor self-conformance, described-instance contracts, and inherited populated
    descriptor values
  - replaces blanket Boolean omission handling with descriptor-driven completion of required
    defaults
  - aligns contract inheritance, `InheritanceMode`, admissibility, endpoint, and key-rule semantics
    with the shared descriptor-semantics kernel
  - retains a fixed grammar by expressing schema-defined descriptor properties through one generic
    property-assignment clause rather than schema-specific keywords

- `v0.5`

  - replaces projected-TypeKind and fixed-slot validation with descriptor-driven holon conformance
  - establishes a representation-neutral descriptor-semantics kernel shared by Canonical Holon IR
    and runtime descriptor adapters
  - makes the existing descriptor inheritance rules authoritative for lineage, inherited-member
    flattening, identity-based deduplication, and cycle/cardinality errors
  - retains source-adapter syntax/default responsibilities and the existing runtime-loader boundary
  - clarifies that R5 code generation and R6 editor services consume, but do not redefine, the
    shared descriptor semantics established in R4

- `v0.4`

  - renamed Domain Specific Lanuguage (DSL) to Type Definition Language (TDL) 
  - moved complete formal EBNF grammar for TDL to the Appendix
  - aligns TDL validation with the source-neutral Canonical Holon IR boundary
  - replaces non-extensible property/relationship rules with TypeKind-compatible inheritance
  - defines layered diagnostics, post-lowering requiredness, relationship inverse completeness,
    effective key-rule validation, semantic diff/fidelity, and loader projectability

- `v0.3`

  - aligned the DSL with the then-current `DescriptorRoot` model, superseded by the Schema 2.0
    two-root model in `v0.6`
  - replaces implicit `DescribedBy #TypeDescriptor` with TypeKind-specific
    meta-type injection
  - clarifies that the JSON `type` field compiled by the DSL is shorthand for
    `DescribedBy`
  - clarifies that `extends` remains single inheritance and defaults to the
    appropriate abstract type anchor
  - replaced examples that used the then-removed `TypeDescriptor` node with
    `DescriptorRoot` or concrete descriptor identifiers
  - treated `DescriptorRoot` and top-level abstract anchors as bootstrap
    exceptions rather than ordinary DSL declarations

- `v0.2`

  - introduces explicit document versioning
  - adds schema-level `depends_on` declarations
  - adds schema declaration bodies with `header` and openness flags
  - adds `properties` and `relationships` attachment blocks for `holon`
    declarations
  - adds qualified relationship references for attachment blocks
  - promotes braced declaration bodies and nested block styling as the
    preferred authoring form
  - renames generic metadata blocks to `header` blocks
  - adds `deletion_semantic` as an explicit relationship clause
  - adds `allows_additional_properties` and
    `allows_additional_relationships` as explicit holon openness flags
  - clarifies compiler responsibilities for `InstanceProperties` and
    `InstanceRelationships`

This document rigorously defines a Type Definition Language (TDL) for authoring MAP **type descriptor holons** in a compact, human-readable form that lowers deterministically into the source-neutral Canonical Holon IR and can be projected to the canonical MAP JSON import format.

The TDL is **descriptor-only**: it defines types (schema descriptors), not instances.  
The JSON import format remains the canonical loader format; the Canonical Holon IR is the semantic middle shared by TDL, JSON import/export tooling, validation, semantic diff, and future editor services.
In compiled JSON, the `type` field is shorthand for the descriptor's
`DescribedBy` relationship.
Holon declarations may describe the instance shape of the type through
descriptor-owned attachment blocks; this still defines descriptors, not
instances.

---

# 1. Design Principles

The TDL is designed to satisfy the following constraints:

1. The TDL defines **only type descriptor holons**.
2. Every descriptor implicitly:
    - is `DescribedBy` the kind-specific meta-type for its declaration kind
    - extends exactly one inheritance parent unless it is an explicitly
      bootstrapped root descriptor
    - belongs to exactly one schema via `ComponentOf`.
3. A TDL file contributes descriptors to **exactly one schema**.
4. A TDL file may declare explicit schema dependencies.
5. `Extends` uses single inheritance within one of the two separate hierarchies rooted at
   `MetaTypeDescriptor` and abstract `TypeDescriptor`.
6. `TypeKind` organizes descriptor kinds but does not determine `Extends` compatibility,
   conformance, or admissibility.
7. `InstanceProperties` and `InstanceRelationships` declarations inherit additively through a
   type's own `Extends` lineage; populated descriptor values follow their member descriptor's
   `InheritanceMode`.
8. Presence-based Boolean keywords lower to explicit `true`. Their absence is an omission, not a
   general implicit `false`; descriptor-driven completion materializes `false` only when a required
   property declares that default.
9. Holon instance shape may be declared inline on the holon descriptor.
10. The TDL supports both:
    - complete schema files
    - documentation fragments.
11. The TDL supports both a compact line-oriented surface form and a braced
    block surface form. They are semantically equivalent.
12. Source adapters own syntax and source-format conveniences; descriptor-driven completion owns
    required defaults; Canonical Holon IR validation owns source-neutral schema semantics.
13. Semantic diff and fidelity checks compare normalized Canonical Holon IR, not concrete source text.
14. Descriptor validity is derived from resolved descriptors. Validators must not replace
    descriptor-declared property, relationship, value, or inheritance rules with hard-coded
    schema-specific tables or name-based inference.
15. Canonical Holon IR and runtime holons use the same representation-neutral descriptor-semantics
    kernel for inheritance and effective descriptor behavior; adapters provide graph access but do
    not redefine those rules.
16. Every TDL descriptor is validated as a holon against
    `ConformanceContract(H) = EffectiveInstanceContract(DescribingType(H))`; its own `Extends`
    lineage separately determines classification and the contract it passes to described instances.

---

# 2. File Structure

A complete TDL file begins with a schema declaration.

```
schema <SchemaIdentifier>

Optional schema dependency clauses may follow:

depends_on <SchemaIdentifier>
```

The document or its containing package must bind interpretation to a specific Core Schema version.
Ordinarily, the schema dependency closure supplies that binding. Requiredness, defaults,
descriptor kinds, relationships, cardinalities, and validation rules are resolved against that
version.

The schema declaration may also use the braced form when the schema holon
itself needs a header or openness flags:

`schema <SchemaIdentifier> {
  SchemaBodyClause*
}`

All descriptors following this declaration implicitly compile with:

`ComponentOf <SchemaIdentifier>`

Example:

`schema MAP Metaschema-v0.0.2 {
  depends_on MAP Core Schema-v0.0.7

  header {
    description: "Schema containing MAP metaschema descriptors."
  }
}

def relationship ComponentOf
source TypeDescriptor
target Schema.HolonType

property Description
value MapStringValueType
IsValueRequired true
`
---

# 3. Descriptor Separation

Descriptors are separated by:

- blank lines
- or the appearance of a new top-level descriptor keyword.

Semicolons are not used. Commas are optional only in braced list blocks.

Indentation is used for readability but is not semantically significant beyond grouping clauses under a descriptor.

Braces may be used to group descriptor bodies and nested blocks such as
`header`, `properties`, `relationships`, and `variants`. The braced style is
the preferred house style for examples because it makes large schema
definitions easier to scan.

List-style blocks remain newline-oriented by default. In braced list blocks,
commas are optional and may be used as a stylistic aid, especially when
editing or reordering items. This applies to `properties`, `relationships`,
and inline `variants` blocks, but not to `header` fields.

---

# 4. Reserved Keywords

The following tokens are reserved:

schema  
abstract  
value  
property  
relationship  
inverse  
def  
enum  
variant
holon  
extends  
source  
target  
keyrule  
cardinality  
deletion_semantic
ordered  
duplicates
depends_on
header
allows_additional_properties
allows_additional_relationships
properties
relationships
variants

---

# 5. Descriptor Kinds

The TDL supports the following descriptor kinds:

value  
property  
relationship  
inverse relationship  
enum  
variant  
holon

Each descriptor compiles to a **type descriptor holon**.

---

# 6. Descriptor Identity, Properties, and References

Each declaration identifier establishes the authored symbol used to resolve that descriptor within
the file's schema and dependency scope.

References resolve to descriptor identity, not merely matching text. Qualified references may be
used wherever an unqualified name would be ambiguous. Resolution must preserve distinct descriptor
identities even when later validation reports that they claim the same semantic contract-member
name.

TDL uses one fixed property-assignment form for descriptor properties that do not have dedicated
surface syntax:

    <PropertyReference> <PropertyValue>

The core schema bound to the document determines whether the referenced property exists, whether it
is allowed on the descriptor, its value type, requiredness, constraints, and default. The schema
does not dynamically create new grammar productions or keywords.

Examples:

    IsValueRequired true
    DefaultValue None
    InheritanceMode Additive

`InheritanceMode None` may be omitted because Schema 2.0 defines it as a required property with a
materialized default of `None`. `Additive` and `Override` must be authored explicitly when intended.
Likewise, any required property without a default must be supplied explicitly.

Concise TDL may omit values that the bound schema completes deterministically. Expanded canonical
TDL emits all materialized required defaults through the same property-assignment form. Changing a
bound-schema default can therefore change the interpretation of unchanged concise TDL and is a
schema-versioning event.

---

# 7. Surface Styles

The TDL supports two equivalent surface styles.

Compact form:

value MapLocalizedString
extends MapStringValueType

Braced form:

value MapLocalizedString {
  extends MapStringValueType
}

Examples in this specification prefer the braced form.

---

# 8. Value Type Descriptors

Syntax:

[abstract] value <Identifier>
[extends <Identifier>]
Clause*
HeaderBlock?

or

[abstract] value <Identifier> {
  Clause*
  HeaderBlock?
}

Example:

value MapStringValueType

value MapLocalizedString {
  extends MapStringValueType
}

Compilation rules:

- Inject `type: #MetaValueType`.
- If `extends` is omitted for an ordinary value descriptor, inject `Extends ValueType`.
- Top-level abstract anchors such as `ValueType` are bootstrap descriptors and
  do not extend themselves.
- If `abstract` present → `is_abstract_type = true`.

---

# 9. Property Type Descriptors

Syntax:

[abstract] property <Identifier>
[value <ValueTypeIdentifier>]
Clause*
HeaderBlock?

or

[abstract] property <Identifier> {
  [value <ValueTypeIdentifier>]
  Clause*
  HeaderBlock?
}

Example:

property Description {
  value MapStringValueType
  IsValueRequired true
}

Compilation rules:

- Inject `type: #MetaPropertyType`.
- If `extends` is omitted for an ordinary property descriptor, inject
  `Extends PropertyType`.
- `IsValueRequired`, `DefaultValue`, and non-default `InheritanceMode` values use the fixed
  descriptor-property assignment form.
- `DefaultValue` is valid only when `IsValueRequired` is `true`.
- If `InheritanceMode` is omitted, descriptor-driven completion materializes the required default
  value `None`.
- An explicit `extends` clause is validated by the shared Schema 2.0 hierarchy and conformance
  rules, not by a TDL-specific property-family or `TypeKind` rule.

---

# 10. Relationship Type Descriptors

Relationship descriptors define graph edge semantics.

An explicit `extends` clause on a relationship descriptor is validated by the shared Schema 2.0
hierarchy and conformance rules. TDL does not impose a separate same-`TypeKind` or
declared-versus-inverse inheritance rule.

## 10.1 Declared Relationship

relationship <Identifier>
def relationship <Identifier>

Syntax:

[abstract] [def] relationship <Identifier>
source <SourceType>
target <TargetType>
Clause*
HeaderBlock?

or

[abstract] [def] relationship <Identifier> {
  source <SourceType>
  target <TargetType>
  Clause*
  HeaderBlock?
}

Example:

relationship UsesKeyRule {
  source TypeDescriptor
  target KeyRuleType
  InheritanceMode Override
  cardinality 0..32767
  deletion_semantic Allow
}

## 10.2 Definitional Relationship

def relationship <Identifier>
source <SourceType>
target <TargetType>

Rules:

- Presence of `def` lowers to explicit `is_definitional = true`.
- Absence of `def` leaves the property omitted; creation-time completion materializes a declared
  required default such as `false`.

Declared relationship validation:

- Every declared relationship descriptor must have exactly one inverse relationship descriptor paired with it.
- Every inverse relationship descriptor must point back to a declared relationship descriptor, and that declared relationship must point to no other inverse.
- Relationship descriptor cardinality bounds are required semantic slots. Both `min_cardinality` and `max_cardinality` must be present after lowering, and `min_cardinality <= max_cardinality`.
- A non-default `InheritanceMode` uses the fixed descriptor-property assignment form. If omitted,
  descriptor-driven completion materializes `None`.

## 10.3 Inverse Relationship

Syntax:

[abstract] inverse relationship <Identifier>
source <SourceType>
target <TargetType>
inverse <DeclaredRelationshipIdentifier>
[extends <Identifier>]
Clause*
HeaderBlock?

or

[abstract] inverse relationship <Identifier> {
  source <SourceType>
  target <TargetType>
  inverse <DeclaredRelationshipIdentifier>
  Clause*
  HeaderBlock?
}

Example:

inverse relationship Components {
  source Schema.HolonType
  target TypeDescriptor
  inverse ComponentOf
  cardinality 0..32767
}

Rules:

- If `extends` is omitted, `inverse relationship` injects `Extends InverseRelationshipType`.
- `def` is **not allowed** with inverse relationships.
- `InheritanceMode` follows the same property-assignment and default-completion rule as declared
  relationships.

Compiler injections:

- relationship -> `type: #MetaDeclaredRelationshipType`; if `extends` is omitted,
  `Extends DeclaredRelationshipType`
- inverse relationship -> `type: #MetaInverseRelationshipType`; if `extends` is omitted,
  `Extends InverseRelationshipType`

`deletion_semantic` is valid only on relationship descriptors.

---

# 11. Enum Type Descriptors

Syntax:

[abstract] enum <Identifier>
Clause*
VariantBlock?
HeaderBlock?

or

[abstract] enum <Identifier> {
  Clause*
  HeaderBlock?
  VariantBlock?
}

Example:

enum DeletionSemantic

or

enum DeletionSemantic {
  variants {
    Allow
  }
}

Variants may be declared inline. Inside a `variants { ... }` block, the
`variant` keyword is omitted because the surrounding block already establishes
the context.

Compilation rules:

- Inject `type: #MetaValueType`.
- Set `type_kind` to `Value(Enum)` unless explicitly overridden by a future
  enum-specific surface.
- If `extends` is omitted for an ordinary enum value descriptor, inject
  `Extends ValueType`.

---

# 12. Enum Variant Descriptors

Variants compile to independent type descriptor holons.

Syntax:

variant <Identifier>
HeaderBlock?

or

variant <Identifier> {
  HeaderBlock?
}

Example:

variant Allow

This standalone form remains valid for cases where a variant needs to be
declared or documented separately from the enum's inline `variants` block.

Compiler injects:

- DescribedBy the enum-variant meta-type declared by the core schema
- Extends the enum-variant abstract anchor declared by the core schema
- VariantOf <EnumIdentifier>

---

# 13. Holon Type Descriptors

Syntax:

[abstract] holon <Identifier>
[extends <Identifier>]
Clause*
[PropertyAttachBlock]
[RelationshipAttachBlock]
HeaderBlock?

or

[abstract] holon <Identifier> {
  [extends <Identifier>]
  Clause*
  [PropertyAttachBlock]
  [RelationshipAttachBlock]
  HeaderBlock?
}

Example:

holon Book {
  extends CulturalExpression
  allows_additional_properties

  properties {
    Title
    Author
  }

  relationships {
    WrittenBy
  }
}

Compilation rules:

- Inject `type: #MetaHolonType`.
- If `extends` is omitted for an ordinary holon descriptor, inject
  `Extends HolonType`.
- `properties` entries compile to `InstanceProperties`.
- `relationships` entries compile to `InstanceRelationships`.
- `allows_additional_properties` and `allows_additional_relationships`
  populate the corresponding holon descriptor properties.

## 13.1 Holon Property Attachment Block

Syntax:

properties
  <PropertyIdentifier>
  <PropertyIdentifier>
  ...

or

properties {
  <PropertyIdentifier>
  <PropertyIdentifier>
  ...
}

or

properties {
  <PropertyIdentifier>,
  <PropertyIdentifier>,
  ...
}

Example:

holon DanceInvocation {
  properties {
    InvocationSource
  }
}

Rules:

- Each entry must resolve to a PropertyType descriptor.
- Order in the block is not semantically significant unless the underlying
  schema evolves to make `InstanceProperties` ordered.
- Commas in braced property blocks are optional.

## 13.2 Holon Relationship Attachment Block

Syntax:

relationships
  <RelationshipIdentifier>
  <RelationshipIdentifier>
  ...

or

relationships
  (<SourceIdentifier>)-[<RelationshipIdentifier>]->(<TargetIdentifier>)
  ...

or

relationships {
  <RelationshipIdentifier>
  (<SourceIdentifier>)-[<RelationshipIdentifier>]->(<TargetIdentifier>)
  ...
}

or

relationships {
  <RelationshipIdentifier>,
  (<SourceIdentifier>)-[<RelationshipIdentifier>]->(<TargetIdentifier>),
  ...
}

Example:

holon DanceInvocation {
  relationships {
    InvokesDance
    (DanceInvocation)-[Target]->(HolonType)
    (DanceInvocation)-[Request]->(HolonType)
  }
}

Rules:

- A bare relationship entry resolves by relationship `type_name`.
- A qualified relationship entry resolves by exact source/label/target
  descriptor.
- Each entry must resolve to a relationship descriptor.
- The attachment block describes the relationships instances of the holon type
  may carry; it does not create a new relationship type.
- Commas in braced relationship blocks are optional.

---

# 14. Descriptor Clauses

Clauses refine descriptor semantics.

The formal productions for clauses and nested blocks are defined in
Appendix B. The core clause families are:

- `ExtendsClause`
- `ValueClause`
- `PropertyAssignmentClause`
- `SourceClause`
- `TargetClause`
- `InverseClause`
- `KeyRuleClause`
- `CardinalityClause`
- `DeletionSemanticClause`
- `RelationshipFlagClause`
- `HolonOpenFlagClause`
- `SchemaOpenFlagClause`
- `PropertyAttachBlock`
- `RelationshipAttachBlock`
- `VariantBlock`

---

# 15. Boolean Flags

The following flags are presence-based:

abstract  
def  
ordered  
duplicates
allows_additional_properties
allows_additional_relationships

Presence lowers to an explicit `true` value.

Absence leaves the corresponding value omitted. Before kernel validation, descriptor-driven
completion materializes the effective property descriptor's default only when the property is
required. TDL does not define a blanket Boolean default.

Example:

relationship ParentOf {
  source HolonType
  target HolonType
  deletion_semantic Allow
  ordered
}

---

# 16. Header Blocks

Optional descriptor header fields are defined using a `header` block.

Formal `HeaderBlock` and `HeaderField` productions are defined in Appendix B.

Example:

header {
  description: "Links a type descriptor to the schema that contains it."
  display_plural: "Component Relationships"
}

The `header` block carries shared descriptor-holon properties declared through the applicable
meta-type contract, not arbitrary structure.

Typical header fields:

description  
display_name  
display_plural  
plural

---

# 17. Default `DescribedBy` and `Extends` Injection

For ordinary descriptors, the compiler injects both the declaration-kind-specific
`DescribedBy` target and the default abstract inheritance anchor when
`extends` is omitted:

| TDL declaration kind      | Injected `type` / `DescribedBy`      | Default `Extends` target      |
|---------------------------|--------------------------------------|-------------------------------|
| `value`                   | `MetaValueType`                      | `ValueType`                   |
| `enum`                    | `MetaValueType`                      | `ValueType`                   |
| `property`                | `MetaPropertyType`                   | `PropertyType`                |
| `holon`                   | `MetaHolonType`                      | `HolonType`                   |
| `relationship`            | `MetaDeclaredRelationshipType`       | `DeclaredRelationshipType`    |
| `inverse relationship`    | `MetaInverseRelationshipType`        | `InverseRelationshipType`     |
| `variant`                 | core enum-variant meta-type          | core enum-variant anchor      |

These are independent relationships. The injected `DescribedBy` selects the descriptor holon's
self-conformance contract through the meta-type hierarchy. The injected or authored `Extends`
selects its classification and described-instance contract through the descriptor-type hierarchy.
The compiler must not merge the two paths.

`TypeDescriptor`, `MetaTypeDescriptor`, and the top-level abstract anchors are bootstrap
descriptors. `TypeDescriptor` and `MetaTypeDescriptor` are the separate roots of the
descriptor-type and meta-type `Extends` hierarchies. They are installed by the core schema
bootstrap path and are not ordinary TDL declarations that extend themselves.

The bootstrap path also establishes that every meta-type is `DescribedBy MetaHolonType` and that
`MetaHolonType` is self-describing. Ordinary declaration keywords must not synthesize or reinterpret
that reflective fixed point.

Ordinary keyword semantics are not overridden by reserved bootstrap names. A
declaration such as `abstract property MetaPropertyType` still carries the
ordinary `property` injections shown above; if those injections produce the
wrong semantics for that descriptor, then the declaration is simply not a valid
ordinary TDL encoding of the bootstrap anchor. The compiler must not silently
reinterpret ordinary `value`, `property`, `holon`, `relationship`, or `enum`
declarations based only on descriptor name. Bootstrap descriptors therefore
remain explicit exceptions to ordinary TDL authoring unless and until the
language defines a first-class bootstrap syntax.

---

# 18. Extensibility Rules

TDL lowers `extends` to the shared Schema 2.0 `Extends` relationship. The grammar does not define a
parallel inheritance policy.

Validation rules:

- A descriptor may have at most one direct `Extends` target.
- Multi-step `Extends` chains are valid.
- The `Extends` target must resolve to a descriptor.
- The `Extends` graph must be acyclic.
- Every `Extends` edge must remain within either the meta-type hierarchy rooted at
  `MetaTypeDescriptor` or the descriptor-type hierarchy rooted at abstract `TypeDescriptor`.
- No general same-`TypeKind` compatibility rule applies to an `Extends` edge.
- An authored or injected `type_kind` is an ordinary descriptor-governed property value. Its
  property descriptor and enum value descriptor determine whether the value is valid; declaration
  keywords, descriptor names, and string prefixes do not create an additional compatibility rule.

The shared descriptor-semantics kernel supplies three separate resolutions:

1. `ConformanceContract(H) = EffectiveInstanceContract(DescribingType(H))` determines the
   properties and relationships that holon `H`, including a descriptor holon, must populate.
2. `EffectiveInstanceContract(T)` additively accumulates `InstanceProperties` and
   `InstanceRelationships` declarations across `T`'s own `Extends` lineage. A subtype may add
   declarations but may not remove, override, shadow, or redeclare inherited declarations.
3. `EffectiveValues(T, M)` resolves populated descriptor values across `T`'s own `Extends` lineage
   according to the materialized `InheritanceMode(M)`: `None` returns only local values,
   `Additive` unions inherited and local values, and `Override` returns the complete local value set
   from the nearest type in the self-first lineage that populates `M`.

Contract declarations are not set-deduplicated. Redeclaring an inherited member identity is an
error, and distinct member identities that claim the same semantic member name are also an error.
By contrast, `Additive` populated values use set union under the value kind's identity or equality
rule while retaining all contribution provenance. `Override` selects the complete local value set
from the nearest type in the self-first lineage and retains selected and shadowed provenance.

Descriptor self-conformance through `DescribedBy` is never flattened together with the descriptor's
own `Extends` lineage. Meta-type contract declarations therefore do not leak into ordinary
described-instance contracts.

Canonical Holon IR validation accesses these rules through an IR graph adapter. Runtime descriptor
behavior accesses the same rules through a `HolonReference` graph adapter. Neither adapter owns an
alternate contract, semantic-inheritance, or conformance algorithm.

Effective key-rule validation uses the same kernel semantics:

- `UsesKeyRule.DeclaredRelationshipType` has `InheritanceMode Override`.
- `instance_key_rule(T)` is the unique target in `EffectiveValues(T, UsesKeyRule)`.
- `holon_key_rule(H) = instance_key_rule(DescribingType(H))`.
- Key-rule resolution does not perform an additional fallback through `DescribedBy`.
- Recognize the canonical key-rule descriptors `TypeNameRule.KeyRuleType`,
  `SchemaNameRule.KeyRuleType`, `TypeKindRule.KeyRuleType`, `EnumVariantRule.KeyRuleType`,
  `RelationshipRule.KeyRuleType`, `ExtendedTypeRule.KeyRuleType`, and `NoneKeyRule`.
- Treat `NoneKeyRule` as explicit keylessness, not as an absent `UsesKeyRule`.
- Validate the required inputs for the selected key rule.
- If an authored key is present, report a diagnostic when it differs from the generated key.

---

# 19. Validation Model

TDL validation is layered. A diagnostic carries both:

- a validation layer, identifying the responsibility boundary that failed
- a diagnostic origin, identifying the source location, symbol, or authored/imported element to inspect

The validation layers are:

- `syntax`
- `ir_structural`
- `declaration_shape`
- `descriptor_kind`
- `reference_symbol`
- `schema_aware`
- `semantic_fidelity`
- `runtime_loader_boundary`

Source adapters own parsing, syntax diagnostics, and explicit TDL conveniences. After source
lowering and symbol resolution, descriptor-driven completion uses the kernel's read-only contract
resolution to materialize descriptor-defined defaults for omitted required properties. If no
explicit value or valid default exists, completion reports a missing-required-property diagnostic.
Optional omissions remain absent. Kernel validation receives the completed explicit representation
and does not inject defaults or otherwise mutate it. Defaults are creation-time completion rules,
not read-time fallback behavior.

After successful completion, every required property is physically present in the Canonical Holon
IR. In particular, the kernel never interprets an absent `InheritanceMode` as `None`. Source-origin
metadata may distinguish an authored value from a materialized default for diagnostics, but both
are ordinary explicit semantic state unless separate provenance semantics are modeled.

After structural decoding and reference resolution, every non-bootstrap Canonical Holon IR holon
is validated by conformance to its resolved descriptor. Explicit bootstrap roots are limited to the
minimum structures needed to make that resolution possible and are validated by their dedicated
bootstrap contract.

1. Resolve exactly one `DescribedBy` target for every holon.
2. Require the describing type to be non-abstract and a transitive subtype of either
   `TypeDescriptor` or `MetaTypeDescriptor`.
3. Obtain `ConformanceContract(H)` from
   `EffectiveInstanceContract(DescribingType(H))`.
4. Validate required properties and relationships and the describing type's applicable
   additional-member policies.
5. Resolve populated descriptor values through `EffectiveValues(T, M)` and the materialized
   `InheritanceMode(M)`.
6. Resolve each property's `PropertyType` and `ValueType`, then validate primitive value
   shape, enum membership, cardinality, and applicable value constraints. String length is counted
   in Unicode grapheme clusters.
7. Reject `DefaultValue` on optional properties. Validate every permitted default against the same
   constraints as the required property it defaults.
8. Validate relationships using their relationship descriptors, including allowed relationship
   names, effective cardinality, source compatibility, target compatibility, inverse pairing, and
   the additional-relationship policy.
9. For an ordinary endpoint holon `H` required to satisfy type `R`, require
   `SubtypeOf(DescribingType(H), R)`. For a descriptor target `D` used as a type, require
   `SubtypeOf(D, R)`. An abstract descriptor may serve as `R`; abstractness prevents instantiation,
   not use as a type anchor.
10. Apply the same process to descriptor holons. Descriptor self-conformance comes from the
    kind-specific meta-type selected by `DescribedBy`; the descriptor's own `Extends` lineage
    separately determines classification and the contract it passes to described instances.

TDL property declarations populate `IsValueRequired` through the fixed descriptor-property
assignment form. Once lowered, requiredness is descriptor data consumed through the effective
contract, not a descriptor-kind switch statement.

The structural bootstrap needed to decode keys, properties, relationships, and references must be
small and representation-oriented. It may establish enough graph structure to resolve descriptors,
but it must not embed Core Schema property names, enum variants, required-slot tables, or
descriptor-family validity rules.

Some model-wide invariants are evaluated after individual holon conformance, including closed-world
symbol uniqueness, inheritance cycles, inverse-pair consistency, and effective-key uniqueness.
These checks consume resolved descriptor identity, effective contracts, and effective values rather
than inferred descriptor families.

Uniqueness validation is closed-world. TDL validation flags duplicate canonical symbols or keys, duplicate local property names, duplicate local relationship names, and duplicate inverse ownership inside the model being validated. It does not check whether another persisted MAP schema elsewhere already uses the same key or symbol.

Scoped schema-semantic validation failures are blocking errors. Warnings are reserved for compatibility aliases or non-canonical source-adapter observations that do not make the Canonical Holon IR semantically invalid.

# 20. Compiler Responsibilities

A TDL compiler must:

1. Inject implicit relationships:
    - `type` / `DescribedBy` using the declaration kind's meta-type
    - ComponentOf
    - default Extends to the declaration kind's abstract anchor
    - schema `DependsOn`
2. Populate schema declaration bodies into the schema holon descriptor,
   including:
    - schema `header`
    - schema openness flags
3. Populate declaration-derived descriptor properties:
    - type_name
    - display_name
    - type_kind
    - explicit `is_abstract_type = true` when `abstract` is present
4. Convert clauses and holon attachment blocks into Canonical Holon IR properties and
   relationships that can be projected to canonical MAP JSON, including:
    - `ValueType`
    - `DefaultValue`
    - `InheritanceMode`
    - `IsValueRequired`
    - `SourceType`
    - `TargetType`
    - `InverseOf`
    - `UsesKeyRule`
    - `deletion_semantic`
    - `InstanceProperties`
    - `InstanceRelationships`
5. Run descriptor-driven completion for every produced holon, including the schema holon:
    - preserve explicitly authored or keyword-injected values
    - materialize an effective descriptor-defined default only for an omitted required property
    - materialize `InheritanceMode = None` where the effective conformance contract requires it
    - report missing required properties for which no valid default exists
    - supply explicit completed Canonical Holon IR to kernel validation.
6. Validate:
    - single inheritance
    - separation of the `MetaTypeDescriptor` and `TypeDescriptor` `Extends` hierarchies
    - acyclic `Extends` chains
    - exactly one `DescribedBy` relationship for every holon
    - non-abstract, two-root describing-type admissibility
    - descriptor conformance for every descriptor holon
    - additive effective instance contracts, including inherited-identity redeclaration and
      semantic-name collision errors
    - required and additional properties through `ConformanceContract`
    - property values through their resolved value descriptors, including enum membership and
      effective cardinality, value constraints, default validity, and grapheme-cluster string
      lengths
    - populated descriptor values through the `InheritanceMode` values `None`, `Additive`, or
      `Override`,
      including duplicate handling and provenance
    - allowed relationships, cardinality, source/target compatibility, and additional-relationship
      policy through effective relationship descriptors
    - closed-world symbol and key uniqueness
    - relationship inverse-pair completeness
    - relationship cardinality bounds and `min_cardinality <= max_cardinality`
    - effective key-rule resolution and generated-key consistency when an authored key is present
    - relationship definitional rules
    - ordinary keyword injections are determined by declaration kind, not by
      reserved descriptor name
    - abstract descriptors, including hierarchy roots, may be type anchors but are not valid
      `DescribedBy` targets
    - every holon is described by a concrete admissible type under `TypeDescriptor` or
      `MetaTypeDescriptor`
    - `deletion_semantic` appears only on relationship descriptors
    - openness flags appear only on holon descriptors or schema declarations
    - property attachment targets resolve to property type descriptors
    - relationship attachment targets resolve to relationship descriptors.

# 21. Semantic Diff, Fidelity, and Loader Projection

Semantic diff compares only valid Canonical Holon IR models. If either side cannot be lowered without blocking diagnostics, the diff operation reports diagnostics instead of attempting a partial diff.

Compile/decompile fidelity is semantic. Fidelity checks compare normalized Canonical Holon IR
content, including descriptor identity, `DescribedBy`, local instance-contract declarations,
materialized defaults, `InheritanceMode`, references, descriptor-governed properties and
relationships, effective key-rule semantics, relationship pairs, cardinalities, and literal
semantic values. Formatting, JSON field order, source ordering where semantically irrelevant, and
equivalent source-format shorthand are not semantic differences.

Runtime-loader boundary validation is limited to projectability. TDL tooling should catch Canonical Holon IR facts that make projection to the existing loader/import shape impossible or malformed, without changing loader behavior, changing Nursery/PVL semantics, or introducing a new runtime import path.

---

# 22. Example TDL File

```
schema MAP Metaschema-v0.0.2 {
  depends_on MAP Core Schema-v0.0.7

  header {
    description: "Schema containing MAP metaschema descriptors."
  }
}

def relationship ComponentOf {
  source TypeDescriptor
  target Schema.HolonType
  cardinality 0..32767
  deletion_semantic Allow

  header {
    description: "Links a type descriptor to the schema that contains it."
  }
}

inverse relationship Components {
  source Schema.HolonType
  target TypeDescriptor
  inverse ComponentOf
  cardinality 0..32767
}

property Description {
  value MapStringValueType
  IsValueRequired true
}

value MapStringValueType

holon Schema {
  allows_additional_properties

  properties {
    Description
  }

  relationships {
    Components
  }
}
```

# Appendix A: TDL Keyword Contracts

This section provides a concise list of the rules used on decompile (from JSON->TDL) to replace JSON clauses with keywords. And likewise, to expand keywords into JSON clauses on compile (TDL->JSON).

## Global Principles

| Principle | Contract |
| --- | --- |
| One semantic middle | JSON and TDL both normalize through the Canonical Holon IR. |
| Compile direction | Each keyword defines what semantic content is injected or lowered when authoring TDL. |
| Decompile direction | Each keyword defines what canonical holon content may collapse back into the concise TDL surface. |
| Losslessness | Decompile may collapse content only when recompiling would produce the same semantic holon content. |
| Implied content | Decompile should omit content already implied by file structure, descriptor kind, keyword, or default injection. |
| Fixed property form | Schema-defined descriptor properties without dedicated syntax use `<PropertyReference> <PropertyValue>`; the bound schema validates their meaning. |
| Expanded form | An expanded canonical TDL projection emits materialized required defaults through property assignments instead of depending on omission. |
| Literal residue | If current TDL cannot express some content truthfully, preserve that content in literal form rather than collapsing it incorrectly. |
| No name-based reinterpretation | Decompile and compile behavior are driven by declaration kind and explicit syntax, not by reserved-looking descriptor names alone. |
| File membership | A file-level `schema` declaration implies `ComponentOf <SchemaIdentifier>` for all following descriptors. That implied relationship should not be repeated in concise decompiled descriptors. |
| Bootstrap exception | If a bootstrap descriptor cannot be expressed truthfully with ordinary keyword rules, decompile to the most literal truthful form. |

## Keyword Contracts

| Keyword | Compile (TDL -> JSON)                                                                                                                                                                                                                                                                   | Decompile (JSON -> TDL)                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `schema` | Declare the schema for the file; lower `depends_on` to schema dependency relationships; imply `ComponentOf <SchemaIdentifier>` for all following descriptors; lower schema header and openness content to the schema holon.                                                                      | Collapse the schema holon to the leading `schema <SchemaIdentifier>` declaration; collapse schema dependencies to `depends_on`; omit per-descriptor `ComponentOf`; use braced `schema { ... }` form only when schema header or openness content is present; preserve non-expressible schema residue literally.                                                                                                                                                                         |
| `value` | Inject meta-type `MetaValueType`; if ordinary and `extends` omitted, inject `Extends ValueType`; lower `keyrule` and header content.                                                                                                                                                             | Collapse implied meta-type to `value`; collapse `is_abstract_type` to `abstract`; omit ordinary default `extends ValueType`; collapse `UsesKeyRule` to `keyrule`; preserve only residue not expressible by ordinary value syntax.                                                                                                                                                                                                                                                      |
| `enum` | Inject meta-type `MetaValueType`; if ordinary and `extends` omitted, inject `Extends ValueType`; lower `keyrule`, inline variants, and header content.                                                                                                                                              | Collapse implied meta-type to `enum`; collapse `is_abstract_type` to `abstract`; omit ordinary default `extends ValueType`; collapse `UsesKeyRule` to `keyrule`; render `variants { ... }` when lossless; preserve only residue not expressible by ordinary enum syntax.                                                                                                                                                                                                                   |
| `variant` | Inject enum-variant meta-type and enum-variant anchor `Extends`; lower `VariantOf <EnumIdentifier>` and header content.                                                                                                                                                                          | Collapse implied meta-type and anchor to `variant`; collapse `is_abstract_type` to `abstract`; omit ordinary injected enum-variant anchor; collapse ownership to variant context or `VariantOf`; preserve only residue not expressible by ordinary variant syntax.                                                                                                                                                                                                                     |
| `property` | Inject meta-type `MetaPropertyType`; if ordinary and `extends` omitted, inject `Extends PropertyType`; lower `value`, `keyrule`, header content, and fixed descriptor-property assignments such as `IsValueRequired`, `DefaultValue`, and `InheritanceMode`.                                  | Collapse implied meta-type to `property`; collapse `is_abstract_type` to `abstract`; omit ordinary default `extends PropertyType`; collapse `ValueType` and `UsesKeyRule` to their dedicated clauses; render remaining descriptor properties through fixed property assignments; omit materialized defaults only when the bound schema reconstructs them.                                                                                                                              |
| `relationship` | Inject meta-type `MetaDeclaredRelationshipType`; if ordinary and `extends` omitted, inject `Extends DeclaredRelationshipType`; lower `source`, `target`, `keyrule`, cardinality, `deletion_semantic`, flags, header content, optional `def`, and descriptor-property assignments.             | Collapse implied meta-type to `relationship`; collapse `is_abstract_type` and `is_definitional`; omit ordinary default `extends DeclaredRelationshipType`; collapse dedicated relationships and flags to their clauses; render properties such as non-default `InheritanceMode` through fixed property assignments; preserve non-expressible residue literally.                                                                                                                       |
| `inverse relationship` | Inject meta-type `MetaInverseRelationshipType`; if ordinary and `extends` omitted, inject `Extends InverseRelationshipType`; lower `source`, `target`, `inverse`, `keyrule`, cardinality, flags, header content, and descriptor-property assignments.                                         | Collapse implied meta-type and ordinary inverse anchor to `inverse relationship`; collapse `is_abstract_type`; collapse dedicated relationships to their clauses; render properties such as non-default `InheritanceMode` through fixed property assignments; preserve literal residue whenever the concise form would not round-trip faithfully.                                                                                                                                   |
| `holon` | Inject meta-type `MetaHolonType`; if ordinary and `extends` omitted, inject `Extends HolonType`; lower `keyrule`, openness flags, header content, `properties { ... }` to `InstanceProperties`, and `relationships { ... }` to `InstanceRelationships`.                                          | Collapse implied meta-type to `holon`; collapse `is_abstract_type` to `abstract`; omit ordinary default `extends HolonType`; collapse `UsesKeyRule` to `keyrule`; collapse openness flags to presence-based syntax; collapse `InstanceProperties` to `properties { ... }`; collapse `InstanceRelationships` to `relationships { ... }`; preserve direct literal descriptor relationships that are not instance-attachment semantics; preserve other non-expressible residue literally. |
| `abstract` | Set `is_abstract_type = true` on the declared descriptor.                                                                                                                                                                                                                                        | Collapse `is_abstract_type = true` to the `abstract` prefix and omit the explicit property when no additional literal requirement prevents that collapse.                                                                                                                                                                                                                                                                                                                              |
| `def` | On declared relationships only, set `is_definitional = true`.                                                                                                                                                                                                                                    | Collapse `is_definitional = true` to the `def` prefix for declared relationships; do not emit `def` for inverse relationships.                                                                                                                                                                                                                                                                                                                                                         |
| `extends` | Lower to `Extends <TargetDescriptor>`.                                                                                                                                                                                                                                                           | Collapse `Extends` to `extends` except when the target is the ordinary injected default for the declaration kind, in which case omit it; preserve literal form for bootstrap or non-ordinary cases not truthfully expressible by ordinary syntax.                                                                                                                                                                                                                                      |
| `value` clause | On property descriptors, lower to `ValueType <TargetValueType>`.                                                                                                                                                                                                                                 | Collapse `ValueType` relationships back to the `value` clause when they represent ordinary property value typing.                                                                                                                                                                                                                                                                                                                                                                      |
| descriptor property | Lower `<PropertyReference> <PropertyValue>` through the bound descriptor contract; examples include `IsValueRequired true`, `DefaultValue None`, and `InheritanceMode Additive`.                                                                                                                | Emit schema-defined properties without dedicated syntax through the same fixed form; omit a materialized default only in concise output when recompilation against the same bound schema reproduces it.                                                                                                                                                                                                                                                                                 |
| `source` | On relationship descriptors, lower to `SourceType <SourceType>`.                                                                                                                                                                                                                                 | Collapse `SourceType` back to `source` when representable exactly.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `target` | On relationship descriptors, lower to `TargetType <TargetType>`.                                                                                                                                                                                                                                 | Collapse `TargetType` back to `target` when representable exactly.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `inverse` | On inverse relationship descriptors, lower to `InverseOf <DeclaredRelationshipIdentifier>`.                                                                                                                                                                                                      | Collapse `InverseOf` back to `inverse` only when the concise form reconstructs the same semantic target exactly.                                                                                                                                                                                                                                                                                                                                                                       |
| `keyrule` | Lower to `UsesKeyRule <KeyRuleType>`.                                                                                                                                                                                                                                                            | Collapse `UsesKeyRule` back to `keyrule` when it is ordinary clause-shaped descriptor semantics.                                                                                                                                                                                                                                                                                                                                                                                       |
| `properties { ... }` | For holon descriptors, lower entries to `InstanceProperties`; each entry must resolve to a property descriptor.                                                                                                                                                                                  | Collapse `InstanceProperties` attachment semantics back to `properties { ... }`; do not use this block for unrelated literal descriptor properties.                                                                                                                                                                                                                                                                                                                                    |
| `relationships { ... }` | For holon descriptors, lower entries to `InstanceRelationships`; bare entries resolve by relationship `type_name`, qualified entries by exact source/label/target descriptor.                                                                                                                    | Collapse only true instance-attachment semantics back to `relationships { ... }`; do not collapse direct literal descriptor relationships with explicit target holons into this block unless the language explicitly defines that as equivalent.                                                                                                                                                                                                                                       |
| `header { ... }` | Lower header fields such as description/display fields/type plural metadata to descriptor properties.                                                                                                                                                                                            | Collapse header-shaped descriptor properties back into `header { ... }` whenever they are representable by the header surface; omit compiled-form duplicates that are fully implied by concise header syntax.                                                                                                                                                                                                                                                                          |
| openness flags | Lower `allows_additional_properties` and `allows_additional_relationships` to explicit `true` descriptor or schema Boolean properties; leave absent flags omitted for descriptor-driven completion.                                                                                           | Collapse true values back to presence-based flags on `schema` or `holon`; omit an explicit false value only when recompilation and descriptor-driven completion reproduce the same explicit semantic value.                                                                                                                                                                                                               |
| `cardinality` | Lower to `min_cardinality` and `max_cardinality`.                                                                                                                                                                                                                                                | Collapse paired cardinality properties back to `cardinality min..max`.                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `deletion_semantic` | Lower to the relationship descriptor property of the same semantic name.                                                                                                                                                                                                                         | Collapse the property back to the `deletion_semantic` clause on relationship descriptors only.                                                                                                                                                                                                                                                                                                                                                                                         |
| `ordered` / `duplicates` | Set the corresponding relationship Boolean properties to explicit `true`; leave absent flags omitted for descriptor-driven completion.                                                                                                                                                          | Collapse true values back to presence-based flags; omit an explicit false value only when recompilation and descriptor-driven completion reproduce the same explicit semantic value.                                                                                                                                                                                                                                     |


# Appendix B. Descriptor Grammar (EBNF)

The grammar below defines the concrete descriptor syntax. It is intentionally
syntactic rather than semantic: rules such as two-hierarchy `Extends` separation,
descriptor conformance, required cardinality bounds, relationship inverse completeness,
and "inverse relationships cannot be definitional" are enforced by validation, not by
the grammar itself.

Lexical conventions:

- `Identifier` means a valid MAP identifier token.
- `Reference` means a valid MAP descriptor or schema reference as accepted by
  the implementation, including qualified names such as `Schema.HolonType`.
- `Literal` means a JSON-style scalar literal accepted in descriptor-property assignments or
  header fields.
- `Integer` means a non-negative base-10 integer literal.
- `NL` means one or more line breaks.

```ebnf
File                    ::= SchemaSection DescriptorSection ;

SchemaSection           ::= CompactSchemaDecl
                         | BracedSchemaDecl ;

CompactSchemaDecl       ::= "schema" Reference NL
                            { DependsOnDecl NL } ;

BracedSchemaDecl        ::= "schema" Reference "{" NL
                              { SchemaBodyClause NL }
                            "}" NL ;

SchemaBodyClause        ::= DependsOnDecl
                         | HeaderBlock
                         | SchemaOpenFlagClause
                         | PropertyAssignmentClause ;

SchemaOpenFlagClause    ::= "allows_additional_properties"
                         | "allows_additional_relationships" ;

DependsOnDecl           ::= "depends_on" Reference ;

DescriptorSection       ::= Descriptor { DescriptorGap Descriptor } ;
DescriptorGap           ::= NL { NL } ;

Descriptor              ::= ValueDecl
                         | PropertyDecl
                         | DeclaredRelationshipDecl
                         | InverseRelationshipDecl
                         | EnumDecl
                         | VariantDecl
                         | HolonDecl ;

ValueDecl               ::= [ "abstract" ] "value" Identifier
                            ( CompactValueBody | BracedValueBody ) ;

CompactValueBody        ::= NL { ValueBodyClause NL } ;
BracedValueBody         ::= "{" NL { ValueBodyClause NL } "}" ;
ValueBodyClause         ::= ExtendsClause
                         | KeyRuleClause
                         | PropertyAssignmentClause
                         | HeaderBlock ;

PropertyDecl            ::= [ "abstract" ] "property" Identifier
                            ( CompactPropertyBody | BracedPropertyBody ) ;

CompactPropertyBody     ::= NL { PropertyBodyClause NL } ;
BracedPropertyBody      ::= "{" NL { PropertyBodyClause NL } "}" ;
PropertyBodyClause      ::= ExtendsClause
                         | ValueClause
                         | KeyRuleClause
                         | PropertyAssignmentClause
                         | HeaderBlock ;

DeclaredRelationshipDecl ::= [ "abstract" ] [ "def" ] "relationship" Identifier
                             ( CompactDeclaredRelationshipBody
                             | BracedDeclaredRelationshipBody ) ;

CompactDeclaredRelationshipBody ::= NL
                                    SourceClause NL
                                    TargetClause NL
                                    { DeclaredRelationshipBodyClause NL } ;

BracedDeclaredRelationshipBody ::= "{" NL
                                     SourceClause NL
                                     TargetClause NL
                                     { DeclaredRelationshipBodyClause NL }
                                   "}" ;

DeclaredRelationshipBodyClause ::= ExtendsClause
                                 | CardinalityClause
                                 | KeyRuleClause
                                 | DeletionSemanticClause
                                 | RelationshipFlagClause
                                 | PropertyAssignmentClause
                                 | HeaderBlock ;

InverseRelationshipDecl ::= [ "abstract" ] "inverse" "relationship" Identifier
                            ( CompactInverseRelationshipBody
                            | BracedInverseRelationshipBody ) ;

CompactInverseRelationshipBody ::= NL
                                   SourceClause NL
                                   TargetClause NL
                                   InverseClause NL
                                   { InverseRelationshipBodyClause NL } ;

BracedInverseRelationshipBody ::= "{" NL
                                    SourceClause NL
                                    TargetClause NL
                                    InverseClause NL
                                    { InverseRelationshipBodyClause NL }
                                  "}" ;

InverseRelationshipBodyClause ::= ExtendsClause
                                | CardinalityClause
                                | KeyRuleClause
                                | DeletionSemanticClause
                                | RelationshipFlagClause
                                | PropertyAssignmentClause
                                | HeaderBlock ;

EnumDecl                ::= [ "abstract" ] "enum" Identifier
                            ( CompactEnumBody | BracedEnumBody ) ;

CompactEnumBody         ::= NL { EnumBodyClause NL } ;
BracedEnumBody          ::= "{" NL { EnumBodyClause NL } "}" ;
EnumBodyClause          ::= ExtendsClause
                         | KeyRuleClause
                         | PropertyAssignmentClause
                         | HeaderBlock
                         | VariantBlock ;

VariantDecl             ::= "variant" Identifier
                            ( CompactVariantBody | BracedVariantBody ) ;

CompactVariantBody      ::= NL { VariantBodyClause NL } ;
BracedVariantBody       ::= "{" NL { VariantBodyClause NL } "}" ;
VariantBodyClause       ::= HeaderBlock
                         | PropertyAssignmentClause ;

HolonDecl               ::= [ "abstract" ] "holon" Identifier
                            ( CompactHolonBody | BracedHolonBody ) ;

CompactHolonBody        ::= NL { HolonBodyClause NL } ;
BracedHolonBody         ::= "{" NL { HolonBodyClause NL } "}" ;
HolonBodyClause         ::= ExtendsClause
                         | KeyRuleClause
                         | PropertyAssignmentClause
                         | HeaderBlock
                         | HolonOpenFlagClause
                         | PropertyAttachBlock
                         | RelationshipAttachBlock ;

HolonOpenFlagClause     ::= "allows_additional_properties"
                         | "allows_additional_relationships" ;

ExtendsClause           ::= "extends" Reference ;
ValueClause             ::= "value" Reference ;
PropertyAssignmentClause ::= Reference PropertyValue ;
PropertyValue           ::= Literal | Reference ;
SourceClause            ::= "source" Reference ;
TargetClause            ::= "target" Reference ;
InverseClause           ::= "inverse" Reference ;
KeyRuleClause           ::= "keyrule" Reference ;
CardinalityClause       ::= "cardinality" Integer ".." Integer ;
DeletionSemanticClause  ::= "deletion_semantic" Reference ;

RelationshipFlagClause  ::= "ordered"
                         | "duplicates" ;

PropertyAttachBlock     ::= "properties" NL PropertyAttachEntry
                            { NL PropertyAttachEntry }
                         | "properties" "{" [ PropertyAttachEntry
                            { [ "," ] PropertyAttachEntry } [ "," ] ] "}" ;

PropertyAttachEntry     ::= Reference ;

RelationshipAttachBlock ::= "relationships" NL RelationshipAttachEntry
                            { NL RelationshipAttachEntry }
                         | "relationships" "{" [ RelationshipAttachEntry
                            { [ "," ] RelationshipAttachEntry } [ "," ] ] "}" ;

RelationshipAttachEntry ::= Reference
                         | QualifiedRelationshipRef ;

QualifiedRelationshipRef ::= "(" Reference ")-[" Reference "]->(" Reference ")" ;

VariantBlock            ::= "variants" "{" [ VariantItem
                            { [ "," ] VariantItem } [ "," ] ] "}" ;

VariantItem             ::= Identifier
                         | VariantDecl ;

HeaderBlock             ::= "header" "{" NL
                              { HeaderField NL }
                            "}" ;

HeaderField             ::= Identifier ":" Literal ;
```
