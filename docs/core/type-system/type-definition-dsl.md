# MAP Type Descriptor DSL Specification v0.3

## ChangeLog

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

This document rigorously defines a Domain-Specific Language (DSL) for authoring MAP **type descriptor holons** in a compact, human-readable form that compiles deterministically into the canonical MAP JSON import format.

The DSL is **descriptor-only**: it defines types (schema descriptors), not instances.  
The JSON import format remains the canonical loader format; the DSL is a source-level authoring representation.
In compiled JSON, the `type` field is shorthand for the descriptor's
`DescribedBy` relationship.
Holon declarations may describe the instance shape of the type through
descriptor-owned attachment blocks; this still defines descriptors, not
instances.

---

# 1. Design Principles

The DSL is designed to satisfy the following constraints:

1. The DSL defines **only type descriptor holons**.
2. Every descriptor implicitly:
    - is `DescribedBy` the TypeKind-specific meta-type for its declaration kind
    - extends exactly one inheritance parent unless it is an explicitly
      bootstrapped root descriptor
    - belongs to exactly one schema via `ComponentOf`.
3. A DSL file contributes descriptors to **exactly one schema**.
4. A DSL file may declare explicit schema dependencies.
5. Inheritance uses **single additive inheritance**.
6. Relationship types are **not extensible**.
7. Property types are **not extensible** unless the core meta-type design says
   otherwise.
8. Validation of extensibility is determined by the **meta-type layer**, not the DSL grammar.
9. Boolean attributes default to **false** and become **true by presence**.
10. Holon instance shape may be declared inline on the holon descriptor.
11. The DSL supports both:
    - complete schema files
    - documentation fragments.
12. The DSL supports both a compact line-oriented surface form and a braced
    block surface form. They are semantically equivalent.

---

# 2. File Structure

A complete DSL file begins with a schema declaration.

schema <SchemaIdentifier>

Optional schema dependency clauses may follow:

depends_on <SchemaIdentifier>

The schema declaration may also use the braced form when the schema holon
itself needs a header or openness flags:

schema <SchemaIdentifier> {
  SchemaBodyClause*
}

All descriptors following this declaration implicitly compile with:

ComponentOf <SchemaIdentifier>

Example:

schema MAP Metaschema-v0.0.2 {
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

The DSL supports the following descriptor kinds:

value  
property  
relationship  
inverse relationship  
enum  
variant  
holon

Each descriptor compiles to a **type descriptor holon**.

---

# 6. Descriptor Grammar (EBNF)

File                ::= SchemaDecl NL Descriptor+

SchemaDecl          ::= "schema" Identifier
                     | "schema" Identifier "{" SchemaBodyClause* "}"
DependsOnDecl       ::= "depends_on" Identifier
SchemaBodyClause    ::= DependsOnDecl
                     | HeaderBlock
                     | OpenFlagClause

Descriptor          ::= ValueDecl
| PropertyDecl
| RelationshipDecl
| EnumDecl
| VariantDecl
| HolonDecl

Identifier          ::= <valid MAP identifier>

---

# 7. Surface Styles

The DSL supports two equivalent surface styles.

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

ExtendsClause        ::= "extends" Identifier  
ValueClause          ::= "value" Identifier  
SourceClause         ::= "source" Identifier  
TargetClause         ::= "target" Identifier  
InverseClause        ::= "inverse" Identifier  
KeyRuleClause        ::= "keyrule" Identifier  
CardinalityClause    ::= "cardinality" Integer ".." Integer  
DeletionSemanticClause ::= "deletion_semantic" Identifier
FlagClause           ::= "ordered" | "duplicates"
OpenFlagClause       ::= "allows_additional_properties"
                       | "allows_additional_relationships"

PropertyAttachBlock  ::= "properties" NL PropertyRef+
                       | "properties" "{" CommaPropertyRefList "}"
RelationshipAttachBlock ::= "relationships" NL RelationshipRef+
                          | "relationships" "{" CommaRelationshipRefList "}"
VariantBlock        ::= "variants" "{" CommaVariantItemList "}"

PropertyRef          ::= Identifier
RelationshipRef      ::= Identifier
                       | QualifiedRelationshipRef
QualifiedRelationshipRef ::= "(" Identifier ")-[" Identifier "]->(" Identifier ")"
VariantItem          ::= Identifier
                       | VariantDecl
CommaPropertyRefList ::= (PropertyRef [","])*
CommaRelationshipRefList ::= (RelationshipRef [","])*
CommaVariantItemList ::= (VariantItem [","])*

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

HeaderBlock ::= "header" "{" Field* "}"

Field ::= Identifier ":" Literal

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

| DSL declaration kind      | Injected `type` / `DescribedBy`      | Default `Extends` target      |
|---------------------------|--------------------------------------|-------------------------------|
| `value`                   | `MetaValueType`                      | `ValueType`                   |
| `enum`                    | `MetaValueType`                      | `ValueType`                   |
| `property`                | `MetaPropertyType`                   | `PropertyType`                |
| `holon`                   | `MetaHolonType`                      | `HolonType`                   |
| `relationship`            | `MetaDeclaredRelationshipType`       | `DeclaredRelationshipType`    |
| `inverse relationship`    | `MetaInverseRelationshipType`        | `InverseRelationshipType`     |
| `variant`                 | core enum-variant meta-type          | core enum-variant anchor      |

`DescriptorRoot` and the top-level abstract anchors are bootstrap descriptors.
They are installed by the core schema bootstrap path and are not ordinary DSL
declarations that extend themselves.

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

A DSL compiler must:

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
    - ordinary descriptors do not use `DescriptorRoot` as their `Extends`
      target
    - ordinary runtime holons are described only by concrete type descriptors
    - `deletion_semantic` appears only on relationship descriptors
    - openness flags appear only on holon descriptors or schema declarations
    - property attachment targets resolve to property type descriptors
    - relationship attachment targets resolve to relationship descriptors.

---

# 20. Example DSL File

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
