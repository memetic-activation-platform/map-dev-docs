# MAP Type Definition Language (TDL) Specification v0.4

## ChangeLog

- `v0.4`

  - renamed Domain Specific Lanuguage (DSL) to Type Definition Language (TDL) 
  - moved complete formal EBNF grammar for TDL to the Appendix

- `v0.3`

  - aligns the DSL with the MAP Type System v2.0 `DescriptorRoot` model
  - replaces implicit `DescribedBy #TypeDescriptor` with TypeKind-specific
    meta-type injection
  - clarifies that the JSON `type` field compiled by the DSL is shorthand for
    `DescribedBy`
  - clarifies that `extends` remains single inheritance and defaults to the
    appropriate abstract type anchor
  - replaces examples that used the removed `TypeDescriptor` node with
    `DescriptorRoot` or concrete descriptor identifiers
  - treats `DescriptorRoot` and top-level abstract anchors as bootstrap
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

This document rigorously defines a Type Definition Language (TDL) for authoring MAP **type descriptor holons** in a compact, human-readable form that compiles deterministically into the canonical MAP JSON import format.

The TDL is **descriptor-only**: it defines types (schema descriptors), not instances.  
The JSON import format remains the canonical loader format; the TDL is a source-level authoring representation.
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
    - is `DescribedBy` the TypeKind-specific meta-type for its declaration kind
    - extends exactly one inheritance parent unless it is an explicitly
      bootstrapped root descriptor
    - belongs to exactly one schema via `ComponentOf`.
3. A TDL file contributes descriptors to **exactly one schema**.
4. A TDL file may declare explicit schema dependencies.
5. Inheritance uses **single additive inheritance**.
6. Relationship types are **not extensible**.
7. Property types are **not extensible** unless the core meta-type design says
   otherwise.
8. Validation of extensibility is determined by the **meta-type layer**, not the TDL grammar.
9. Boolean attributes default to **false** and become **true by presence**.
10. Holon instance shape may be declared inline on the holon descriptor.
11. The TDL supports both:
    - complete schema files
    - documentation fragments.
12. The TDL supports both a compact line-oriented surface form and a braced
    block surface form. They are semantically equivalent.

---

# 2. File Structure

A complete TDL file begins with a schema declaration.

```
schema <SchemaIdentifier>

Optional schema dependency clauses may follow:

depends_on <SchemaIdentifier>
```

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
source DescriptorRoot
target Schema.HolonType

property Description
value MapStringValueType
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
}

Compilation rules:

- Inject `type: #MetaPropertyType`.
- If `extends` is omitted for an ordinary property descriptor, inject
  `Extends PropertyType`.
- PropertyType descriptors are **not extensible** by default; semantic validation enforces this.

---

# 10. Relationship Type Descriptors

Relationship descriptors define graph edge semantics.

Relationship types are **atomic and not extensible**.

## 10.1 Declared Relationship

relationship <Identifier>
def relationship <Identifier>

Syntax:

[abstract] relationship <Identifier>
source <SourceType>
target <TargetType>
Clause*
HeaderBlock?

or

[abstract] relationship <Identifier> {
  source <SourceType>
  target <TargetType>
  Clause*
  HeaderBlock?
}

Example:

relationship UsesKeyRule {
  source DescriptorRoot
  target KeyRuleType
  deletion_semantic Allow
}

## 10.2 Definitional Relationship

def relationship <Identifier>
source <SourceType>
target <TargetType>

Rules:

- `def` sets `is_definitional = true`.
- Absence of `def` → `is_definitional = false`.

## 10.3 Inverse Relationship

inverse relationship <Identifier>
source <SourceType>
target <TargetType>
inverse <DeclaredRelationshipIdentifier>

Example:

inverse relationship Components {
  source Schema.HolonType
  target DescriptorRoot
  inverse ComponentOf
}

Rules:

- `inverse relationship` implies `Extends InverseRelationshipType`.
- `def` is **not allowed** with inverse relationships.

Compiler injections:

- relationship → `type: #MetaDeclaredRelationshipType`, `Extends DeclaredRelationshipType`
- inverse relationship → `type: #MetaInverseRelationshipType`, `Extends InverseRelationshipType`

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
Section 6. The core clause families are:

- `ExtendsClause`
- `ValueClause`
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

Presence ⇒ true  
Absence ⇒ false

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

Formal `HeaderBlock` and `HeaderField` productions are defined in Section 6.

Example:

header {
  description: "Links a type descriptor to the schema that contains it."
  display_plural: "Component Relationships"
}

The `header` block carries shared `DescriptorRoot` fields, not arbitrary
structure.

Typical header fields:

description  
display_name  
display_plural  
plural

---

# 17. Default Description and Inheritance Injection

For ordinary descriptors, the compiler injects both the TypeKind-specific
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

`DescriptorRoot` and the top-level abstract anchors are bootstrap descriptors.
They are installed by the core schema bootstrap path and are not ordinary TDL
declarations that extend themselves.

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

Whether a descriptor may be extended is determined by the meta-type property:

is_extensible : Boolean

Validation rule:

If TargetDescriptor.is_extensible == false  
then extending it is a validation error.

Typical configuration:

HolonType                extensible  
ValueType                extensible  
PropertyType             non-extensible  
DeclaredRelationshipType non-extensible  
InverseRelationshipType  non-extensible  
core enum-variant anchor non-extensible

---

# 19. Compiler Responsibilities

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
3. Populate required descriptor properties:
    - type_name
    - display_name
    - type_kind
    - is_abstract_type
4. Convert clauses and holon attachment blocks into canonical MAP JSON
   relationships, including:
    - `ValueType`
    - `SourceType`
    - `TargetType`
    - `InverseOf`
    - `UsesKeyRule`
    - `deletion_semantic`
    - `InstanceProperties`
    - `InstanceRelationships`
5. Validate:
    - single inheritance
    - meta-type extensibility
    - relationship definitional rules
    - ordinary keyword injections are determined by declaration kind, not by
      reserved descriptor name
    - ordinary descriptors do not use `DescriptorRoot` as their `Extends`
      target
    - ordinary runtime holons are described only by concrete type descriptors
    - `deletion_semantic` appears only on relationship descriptors
    - openness flags appear only on holon descriptors or schema declarations
    - property attachment targets resolve to property type descriptors
    - relationship attachment targets resolve to relationship descriptors.

---

# 20. Example TDL File

```
schema MAP Metaschema-v0.0.2 {
  depends_on MAP Core Schema-v0.0.7

  header {
    description: "Schema containing MAP metaschema descriptors."
  }
}

def relationship ComponentOf {
  source DescriptorRoot
  target Schema.HolonType
  cardinality 0..32767
  deletion_semantic Allow

  header {
    description: "Links a type descriptor to the schema that contains it."
  }
}

inverse relationship Components {
  source Schema.HolonType
  target DescriptorRoot
  inverse ComponentOf
}

property Description {
  value MapStringValueType
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
| Literal residue | If current TDL cannot express some content truthfully, preserve that content in literal form rather than collapsing it incorrectly. |
| No name-based reinterpretation | Decompile and compile behavior are driven by declaration kind and explicit syntax, not by reserved-looking descriptor names alone. |
| File membership | A file-level `schema` declaration implies `ComponentOf <SchemaIdentifier>` for all following descriptors. That implied relationship should not be repeated in concise decompiled descriptors. |
| Bootstrap exception | If a bootstrap descriptor cannot be expressed truthfully with ordinary keyword rules, decompile to the most literal truthful form. |

## Keyword Contracts

| Keyword | Compile (TDL -> JSON)                                                                                                                                                                                                                                                                   | Decompile (JSON -> TDL)                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `schema` | Declare the schema for the file; lower `depends_on` to schema dependency relationships; imply `ComponentOf <SchemaIdentifier>` for all following descriptors; lower schema header and openness content to the schema holon.                                                                      | Collapse the schema holon to the leading `schema <SchemaIdentifier>` declaration; collapse schema dependencies to `depends_on`; omit per-descriptor `ComponentOf`; use braced `schema { ... }` form only when schema header or openness content is present; preserve non-expressible schema residue literally.                                                                                                                                                                         |
| `value` | Inject meta-type `MetaValueType`; if ordinary and `extends` omitted, inject `Extends ValueType`; lower `keyrule` and header content.                                                                                                                                                             | Collapse implied meta-type to `value`; collapse `is_abstract_type` to `abstract`; omit ordinary default `extends ValueType`; collapse `UsesKeyRule` to `keyrule`; preserve only residue not expressible by ordinary value syntax.                                                                                                                                                                                                                                                      |
| `enum` | Inject meta-type `MetaValueType`; if ordinary and `extends` omitted, inject `Extends ValueType`; lower inline variants and header content.                                                                                                                                                       | Collapse implied meta-type to `enum`; collapse `is_abstract_type` to `abstract`; omit ordinary default `extends ValueType`; render `variants { ... }` when lossless; preserve only residue not expressible by ordinary enum syntax.                                                                                                                                                                                                                                                    |
| `variant` | Inject enum-variant meta-type and enum-variant anchor `Extends`; lower `VariantOf <EnumIdentifier>` and header content.                                                                                                                                                                          | Collapse implied meta-type and anchor to `variant`; collapse `is_abstract_type` to `abstract`; omit ordinary injected enum-variant anchor; collapse ownership to variant context or `VariantOf`; preserve only residue not expressible by ordinary variant syntax.                                                                                                                                                                                                                     |
| `property` | Inject meta-type `MetaPropertyType`; if ordinary and `extends` omitted, inject `Extends PropertyType`; lower `value <ValueTypeIdentifier>`, `keyrule`, and header content.                                                                                                                       | Collapse implied meta-type to `property`; collapse `is_abstract_type` to `abstract`; omit ordinary default `extends PropertyType`; collapse `ValueType` to `value`; collapse `UsesKeyRule` to `keyrule`; preserve only residue not expressible by ordinary property syntax.                                                                                                                                                                                                            |
| `relationship` | Inject meta-type `MetaDeclaredRelationshipType`; if ordinary and `extends` omitted, inject `Extends DeclaredRelationshipType`; lower `source`, `target`, `keyrule`, `cardinality`, `deletion_semantic`, `ordered`, `duplicates`, header content, and optional `def` to `is_definitional = true`. | Collapse implied meta-type to `relationship`; collapse `is_abstract_type` to `abstract`; collapse `is_definitional = true` to `def`; omit ordinary default `extends DeclaredRelationshipType`; collapse `SourceType`, `TargetType`, `UsesKeyRule`, cardinality, deletion semantic, ordered, and duplicates to clauses; collapse `InverseOf` to `inverse` only when lossless; preserve non-expressible residue literally.                                                               |
| `inverse relationship` | Inject meta-type `MetaInverseRelationshipType`; inject `Extends InverseRelationshipType`; lower `source`, `target`, `inverse`, `keyrule`, cardinality, flags, and header content.                                                                                                                | Collapse implied meta-type and ordinary inverse anchor to `inverse relationship`; collapse `is_abstract_type` to `abstract`; collapse `SourceType`, `TargetType`, and `InverseOf` to clauses only when exact; preserve literal residue whenever the concise inverse form would not round-trip faithfully.                                                                                                                                                                              |
| `holon` | Inject meta-type `MetaHolonType`; if ordinary and `extends` omitted, inject `Extends HolonType`; lower `keyrule`, openness flags, header content, `properties { ... }` to `InstanceProperties`, and `relationships { ... }` to `InstanceRelationships`.                                          | Collapse implied meta-type to `holon`; collapse `is_abstract_type` to `abstract`; omit ordinary default `extends HolonType`; collapse `UsesKeyRule` to `keyrule`; collapse openness flags to presence-based syntax; collapse `InstanceProperties` to `properties { ... }`; collapse `InstanceRelationships` to `relationships { ... }`; preserve direct literal descriptor relationships that are not instance-attachment semantics; preserve other non-expressible residue literally. |
| `abstract` | Set `is_abstract_type = true` on the declared descriptor.                                                                                                                                                                                                                                        | Collapse `is_abstract_type = true` to the `abstract` prefix and omit the explicit property when no additional literal requirement prevents that collapse.                                                                                                                                                                                                                                                                                                                              |
| `def` | On declared relationships only, set `is_definitional = true`.                                                                                                                                                                                                                                    | Collapse `is_definitional = true` to the `def` prefix for declared relationships; do not emit `def` for inverse relationships.                                                                                                                                                                                                                                                                                                                                                         |
| `extends` | Lower to `Extends <TargetDescriptor>`.                                                                                                                                                                                                                                                           | Collapse `Extends` to `extends` except when the target is the ordinary injected default for the declaration kind, in which case omit it; preserve literal form for bootstrap or non-ordinary cases not truthfully expressible by ordinary syntax.                                                                                                                                                                                                                                      |
| `value` clause | On property descriptors, lower to `ValueType <TargetValueType>`.                                                                                                                                                                                                                                 | Collapse `ValueType` relationships back to the `value` clause when they represent ordinary property value typing.                                                                                                                                                                                                                                                                                                                                                                      |
| `source` | On relationship descriptors, lower to `SourceType <SourceType>`.                                                                                                                                                                                                                                 | Collapse `SourceType` back to `source` when representable exactly.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `target` | On relationship descriptors, lower to `TargetType <TargetType>`.                                                                                                                                                                                                                                 | Collapse `TargetType` back to `target` when representable exactly.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `inverse` | On inverse relationship descriptors, lower to `InverseOf <DeclaredRelationshipIdentifier>`.                                                                                                                                                                                                      | Collapse `InverseOf` back to `inverse` only when the concise form reconstructs the same semantic target exactly.                                                                                                                                                                                                                                                                                                                                                                       |
| `keyrule` | Lower to `UsesKeyRule <KeyRuleType>`.                                                                                                                                                                                                                                                            | Collapse `UsesKeyRule` back to `keyrule` when it is ordinary clause-shaped descriptor semantics.                                                                                                                                                                                                                                                                                                                                                                                       |
| `properties { ... }` | For holon descriptors, lower entries to `InstanceProperties`; each entry must resolve to a property descriptor.                                                                                                                                                                                  | Collapse `InstanceProperties` attachment semantics back to `properties { ... }`; do not use this block for unrelated literal descriptor properties.                                                                                                                                                                                                                                                                                                                                    |
| `relationships { ... }` | For holon descriptors, lower entries to `InstanceRelationships`; bare entries resolve by relationship `type_name`, qualified entries by exact source/label/target descriptor.                                                                                                                    | Collapse only true instance-attachment semantics back to `relationships { ... }`; do not collapse direct literal descriptor relationships with explicit target holons into this block unless the language explicitly defines that as equivalent.                                                                                                                                                                                                                                       |
| `header { ... }` | Lower header fields such as description/display fields/type plural metadata to descriptor properties.                                                                                                                                                                                            | Collapse header-shaped descriptor properties back into `header { ... }` whenever they are representable by the header surface; omit compiled-form duplicates that are fully implied by concise header syntax.                                                                                                                                                                                                                                                                          |
| openness flags | Lower `allows_additional_properties` and `allows_additional_relationships` to descriptor or schema boolean properties.                                                                                                                                                                           | Collapse true values back to presence-based flags on `schema` or `holon`; omit explicit false values in concise forms unless literal fallback is required.                                                                                                                                                                                                                                                                                                                             |
| `cardinality` | Lower to `min_cardinality` and `max_cardinality`.                                                                                                                                                                                                                                                | Collapse paired cardinality properties back to `cardinality min..max`.                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `deletion_semantic` | Lower to the relationship descriptor property of the same semantic name.                                                                                                                                                                                                                         | Collapse the property back to the `deletion_semantic` clause on relationship descriptors only.                                                                                                                                                                                                                                                                                                                                                                                         |
| `ordered` / `duplicates` | Set the corresponding relationship boolean properties to true.                                                                                                                                                                                                                                   | Collapse true values back to presence-based flags; omit explicit false values in concise forms unless literal fallback is required.                                                                                                                                                                                                                                                                                                                                                    |


# Appendix B. Descriptor Grammar (EBNF)

The grammar below defines the concrete descriptor syntax. It is intentionally
syntactic rather than semantic: rules such as "property types are not
extensible" and "inverse relationships cannot be definitional" are enforced by
validation, not by the grammar itself.

Lexical conventions:

- `Identifier` means a valid MAP identifier token.
- `Reference` means a valid MAP descriptor or schema reference as accepted by
  the implementation, including qualified names such as `Schema.HolonType`.
- `Literal` means a JSON-style scalar literal accepted in header fields.
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
                         | SchemaOpenFlagClause ;

SchemaOpenFlagClause    ::= "allows_additional_properties"
                         | "allows_additional_relationships" ;

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
                         | HeaderBlock ;

PropertyDecl            ::= [ "abstract" ] "property" Identifier
                            ( CompactPropertyBody | BracedPropertyBody ) ;

CompactPropertyBody     ::= NL { PropertyBodyClause NL } ;
BracedPropertyBody      ::= "{" NL { PropertyBodyClause NL } "}" ;
PropertyBodyClause      ::= ExtendsClause
                         | ValueClause
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

InverseRelationshipBodyClause ::= CardinalityClause
                                | KeyRuleClause
                                | HeaderBlock ;

EnumDecl                ::= [ "abstract" ] "enum" Identifier
                            ( CompactEnumBody | BracedEnumBody ) ;

CompactEnumBody         ::= NL { EnumBodyClause NL } ;
BracedEnumBody          ::= "{" NL { EnumBodyClause NL } "}" ;
EnumBodyClause          ::= ExtendsClause
                         | HeaderBlock
                         | VariantBlock ;

VariantDecl             ::= "variant" Identifier
                            ( CompactVariantBody | BracedVariantBody ) ;

CompactVariantBody      ::= NL { VariantBodyClause NL } ;
BracedVariantBody       ::= "{" NL { VariantBodyClause NL } "}" ;
VariantBodyClause       ::= HeaderBlock ;

HolonDecl               ::= [ "abstract" ] "holon" Identifier
                            ( CompactHolonBody | BracedHolonBody ) ;

CompactHolonBody        ::= NL { HolonBodyClause NL } ;
BracedHolonBody         ::= "{" NL { HolonBodyClause NL } "}" ;
HolonBodyClause         ::= ExtendsClause
                         | HeaderBlock
                         | HolonOpenFlagClause
                         | PropertyAttachBlock
                         | RelationshipAttachBlock ;

HolonOpenFlagClause     ::= "allows_additional_properties"
                         | "allows_additional_relationships" ;

ExtendsClause           ::= "extends" Reference ;
ValueClause             ::= "value" Reference ;
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

