# MAP TypeDescriptor DSL Specification

This document rigorously defines a Domain-Specific Language (DSL) for authoring MAP **TypeDescriptor holons** in a compact, human-readable form that compiles deterministically into the canonical MAP JSON import format.

The DSL is **descriptor-only**: it defines types (schema descriptors), not instances.  
The JSON import format remains the canonical loader format; the DSL is a source-level authoring representation.

---

# 1. Design Principles

The DSL is designed to satisfy the following constraints:

1. The DSL defines **only TypeDescriptor holons**.
2. Every descriptor implicitly:
    - is `DescribedBy #TypeDescriptor`
    - belongs to exactly one schema via `ComponentOf`.
3. A DSL file contributes descriptors to **exactly one schema**.
4. Inheritance uses **single additive inheritance**.
5. Relationship types are **not extensible**.
6. Property types are **not extensible**.
7. Validation of extensibility is determined by the **meta-type layer**, not the DSL grammar.
8. Boolean attributes default to **false** and become **true by presence**.
9. The DSL supports both:
    - complete schema files
    - documentation fragments.

---

# 2. File Structure

A complete DSL file begins with a schema declaration.

schema <SchemaIdentifier>

All descriptors following this declaration implicitly compile with:

ComponentOf <SchemaIdentifier>

Example:

schema MAP Metaschema-v0.0.2

def relationship ComponentOf
source TypeDescriptor
target SchemaType

property Description
value MapStringValueType

---

# 3. Descriptor Separation

Descriptors are separated by:

- blank lines
- or the appearance of a new top-level descriptor keyword.

No commas, semicolons, or braces are used.

Indentation is used for readability but is not semantically significant beyond grouping clauses under a descriptor.

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
inverse  
value  
keyrule  
cardinality  
ordered  
duplicates

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

Each descriptor compiles to a **TypeDescriptor holon**.

---

# 6. Descriptor Grammar (EBNF)

File                ::= SchemaDecl NL Descriptor+

SchemaDecl          ::= "schema" Identifier

Descriptor          ::= ValueDecl
| PropertyDecl
| RelationshipDecl
| EnumDecl
| VariantDecl
| HolonDecl

Identifier          ::= <valid MAP identifier>

---

# 7. Value Type Descriptors

Syntax:

[abstract] value <Identifier>
[extends <Identifier>]
Clause*
MetaBlock?

Example:

value MapStringValueType

value MapLocalizedString
extends MapStringValueType

Compilation rules:

- If `extends` omitted → inject `Extends ValueType`.
- If `abstract` present → `is_abstract_type = true`.

---

# 8. Property Type Descriptors

Syntax:

[abstract] property <Identifier>
[value <ValueTypeIdentifier>]
Clause*
MetaBlock?

Example:

property Description
value MapStringValueType

Compilation rules:

- `Extends PropertyType` injected if omitted.
- PropertyType descriptors are **not extensible** by default; semantic validation enforces this.

---

# 9. Relationship Type Descriptors

Relationship descriptors define graph edge semantics.

Relationship types are **atomic and not extensible**.

## 9.1 Declared Relationship

relationship <Identifier>
def relationship <Identifier>

Syntax:

[abstract] relationship <Identifier>
source <SourceType>
target <TargetType>
Clause*
MetaBlock?

Example:

relationship UsesKeyRule
source TypeDescriptor
target KeyRuleType

## 9.2 Definitional Relationship

def relationship <Identifier>
source <SourceType>
target <TargetType>

Rules:

- `def` sets `is_definitional = true`.
- Absence of `def` → `is_definitional = false`.

## 9.3 Inverse Relationship

inverse relationship <Identifier>
source <SourceType>
target <TargetType>
inverse <DeclaredRelationshipIdentifier>

Example:

inverse relationship Components
source SchemaType
target TypeDescriptor
inverse ComponentOf

Rules:

- `inverse relationship` implies `Extends InverseRelationshipType`.
- `def` is **not allowed** with inverse relationships.

Compiler injections:

relationship → Extends DeclaredRelationshipType  
inverse relationship → Extends InverseRelationshipType

---

# 10. Enum Type Descriptors

Syntax:

[abstract] enum <Identifier>
Clause*
VariantBlock?

Example:

enum DeletionSemantic

Variants may be declared inline.

---

# 11. Enum Variant Descriptors

Variants compile to independent TypeDescriptors.

Syntax:

variant <Identifier>
MetaBlock?

Example:

variant Allow

Compiler injects:

Extends EnumVariantType  
VariantOf <EnumIdentifier>

---

# 12. Holon Type Descriptors

Syntax:

[abstract] holon <Identifier>
[extends <Identifier>]
Clause*
MetaBlock?

Example:

holon Book
extends CulturalExpression

Compilation rules:

- If `extends` omitted → inject `Extends HolonType`.

---

# 13. Descriptor Clauses

Clauses refine descriptor semantics.

ExtendsClause        ::= "extends" Identifier  
ValueClause          ::= "value" Identifier  
SourceClause         ::= "source" Identifier  
TargetClause         ::= "target" Identifier  
InverseClause        ::= "inverse" Identifier  
KeyRuleClause        ::= "keyrule" Identifier  
CardinalityClause    ::= "cardinality" Integer ".." Integer  
FlagClause           ::= "ordered" | "duplicates"

---

# 14. Boolean Flags

The following flags are presence-based:

abstract  
def  
ordered  
duplicates

Presence ⇒ true  
Absence ⇒ false

Example:

relationship ParentOf
source HolonType
target HolonType
ordered

---

# 15. Metadata Blocks

Optional metadata fields are defined using a block.

MetaBlock ::= "{" Field* "}"

Field ::= Identifier ":" Literal

Example:

{
description: "Links a type descriptor to the schema that contains it."
display_plural: "Component Relationships"
}

Typical metadata:

description  
display_name  
display_plural  
plural

---

# 16. Default Inheritance Injection

If a descriptor omits `extends`, the compiler injects defaults:

ValueType          → Extends ValueType  
PropertyType       → Extends PropertyType  
HolonType          → Extends HolonType  
EnumType           → Extends EnumValueType  
VariantType        → Extends EnumVariantType  
RelationshipType   → Extends DeclaredRelationshipType  
InverseRelationshipType → Extends InverseRelationshipType

---

# 17. Extensibility Rules

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
EnumValueType            non-extensible  
EnumVariantType          non-extensible

---

# 18. Compiler Responsibilities

A DSL compiler must:

1. Inject implicit relationships:
    - DescribedBy
    - ComponentOf
    - default Extends
2. Populate required descriptor properties:
    - type_name
    - display_name
    - type_kind
    - instance_type_kind
3. Convert clauses into canonical MAP JSON relationships.
4. Validate:
    - single inheritance
    - meta-type extensibility
    - relationship definitional rules.

---

# 19. Example DSL File

schema MAP Metaschema-v0.0.2

def relationship ComponentOf
source TypeDescriptor
target SchemaType
cardinality 0..32767
{
description: "Links a type descriptor to the schema that contains it."
}

inverse relationship Components
source SchemaType
target TypeDescriptor
inverse ComponentOf

property Description
value MapStringValueType

value MapStringValueType

holon TypeDescriptor
extends HolonType