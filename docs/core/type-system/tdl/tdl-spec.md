# MAP Type Definition Language (TDL) Specification v0.8

## **Validation status:**

The Schema 2.0 Core Schema TDL corpus is the primary test of this specification's syntactic
completeness and expressive adequacy.

The representation architecture is resolved: the TDL parser produces the same schema-backed
`LoaderRefRep` holon graph as the MAP JSON parser. Source conversion may render JSON or TDL
directly from that graph. When loading, the existing Holon Loader resolves `LoaderRefRep` into the
staged Holons Core shared-object and Reference Layer representation. Guest-side Schema 2.0
semantics operate through `HolonDescriptor` and its typed descriptor wrappers. There is no separate
semantic IR or graph-adapter layer.

## ChangeLog

Entries before `v0.8` describe the model implemented by those historical revisions. Where they
conflict, the `v0.8` rules are authoritative.

- `v0.8`

  - resolves the semantic middle as the explicit Holons Core graph accessed through
    `HolonDescriptor` and existing Reference Layer operations, retiring the separate Canonical
    Holon IR as a target architecture
  - unifies the descriptor hierarchy by defining `MetaTypeDescriptor Extends HolonType`
  - defines one generalized `(HolonType)-[DescribedBy]->(TypeDescriptor)` relationship and
    `(TypeDescriptor)-[Instances]->(HolonType)` inverse
  - introduces abstract `RelationshipType` as the shared classification parent of declared and
    inverse relationship descriptor roots
  - distinguishes meta-type conformance contracts from abstract descriptor endpoint categories
  - defines uniform endpoint compatibility through cumulative graph classification
  - requires explicit directional deletion semantics on declared and inverse relationship
    descriptors
  - identifies `MetaValueType` as the Core Schema describing type for enum-variant descriptor
    declarations
  - permits abstract descriptor holons to omit category-specific positive-minimum conformance
    members while enforcing the universal descriptor baseline and validating supplied members
  - introduces `instance` as the generic holon declaration form while retaining specialized
    descriptor declaration forms and the compilation-scoping `schema` form
  - derives descriptor category from identity and transitive `Extends` rather than authored
    `TypeKind`
  - requires quoted keys and references when whitespace makes bare form ambiguous
  - renames descriptor shorthand `keyrule` to `instance_keyrule`, which lowers to
    `InstanceKeyRule`
  - represents unbounded relationship cardinality as `min..*`, lowering `*` to an absent optional
    `MaxCardinality` rather than a finite sentinel
  - defines `BaseValueValueType` as the broad representation type for `DefaultValue`, with
    dependent validation against the carrying property descriptor's selected `ValueType`

- `v0.7`

  - requires every descriptor declaration to provide an explicit `type` clause that lowers to
    `DescribedBy`
  - makes `Extends` genuinely optional for every descriptor; omission means that no local
    `Extends` relationship is populated
  - defines the declaration identifier as the descriptor's authored key and validates that key
    against the effective key rule supplied by the descriptor's explicit type
  - requires descriptor and schema references to use keys
  - replaces holon property/relationship attachment shorthand with an explicit relationship map
    capable of representing both instance-contract declarations and other populated descriptor
    relationships
  - removes TDL name-based and declaration-kind-based bootstrap exceptions
  - preserves only representation-level bootstrap sufficient to resolve keys, references, and the
    explicitly authored reflective graph

- `v0.6`

  - aligns TDL lowering and validation with the Schema 2.0 two-hierarchy model rooted at
    `MetaTypeDescriptor` and abstract `TypeDescriptor`
  - removes general `TypeKind` compatibility from `Extends` validation
  - separates descriptor self-conformance, described-instance contracts, and inherited populated
    descriptor values
  - replaces blanket Boolean omission handling with guest-side materialization of required
    descriptor defaults during Holon Loading
  - aligns contract inheritance, `InheritanceMode`, admissibility, endpoint, and key-rule semantics
    with the shared descriptor-semantics kernel
  - retains a fixed grammar by expressing schema-defined descriptor properties through one generic
    property-assignment clause rather than schema-specific keywords

- `v0.5`

  - replaces projected-TypeKind and fixed-slot validation with descriptor-driven holon conformance
  - establishes shared descriptor-semantics behavior over the explicit holon graph through
    `HolonDescriptor`
  - makes the existing descriptor inheritance rules authoritative for lineage, inherited-member
    flattening, identity-based deduplication, and cycle/cardinality errors
  - retains source-adapter syntax/default responsibilities and the existing runtime-loader boundary
  - clarifies that R5 code generation and R6 editor services consume, but do not redefine, the
    shared descriptor semantics established in R4

- `v0.4`

  - renamed Domain Specific Lanuguage (DSL) to Type Definition Language (TDL) 
  - moved complete formal EBNF grammar for TDL to the Appendix
  - aligns TDL validation with a source-neutral holon-representation boundary
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

This document rigorously defines a Type Definition Language (TDL) for authoring MAP schema packages
in a compact, human-readable form that lowers deterministically into the source-neutral Canonical
Holon IR and can be projected to the canonical MAP JSON import format.

TDL supports generic holon instances as well as specialized declaration forms for type descriptor
holons. The specialized forms provide descriptor-oriented shorthand; they do not establish a
separate representation or author category metadata. The specialized `schema` form establishes
compilation scope and lowers to the schema holon contributed by the file.
The JSON import format remains the canonical loader format. The explicit holon graph provided by
Holons Core shared objects and the Reference Layer is the semantic middle shared by TDL, JSON
import/export tooling, validation, semantic diff, and future editor services.
In compiled JSON, the `type` field is shorthand for a holon's `DescribedBy` relationship.
Every non-schema declaration therefore supplies an explicit `type` clause. A descriptor may
describe the instance shape of its type by populating `InstanceProperties` and
`InstanceRelationships` through its relationship map.

---

# 1. Design Principles

The TDL is designed to satisfy the following constraints:

1. TDL can author generic holon instances and type descriptor holons in one schema package.
2. Every non-schema declaration explicitly supplies exactly one `type` key, which lowers to
   `DescribedBy`. Declaration forms do not select or default the describing type.
3. Every descriptor may supply at most one `extends` clause. Omission means that the descriptor
   has no local `Extends` target.
4. Every descriptor belongs to exactly one schema via the `ComponentOf` relationship implied by
   its containing TDL file.
5. A TDL file contributes holons to **exactly one schema**. Implicit `ComponentOf` applies only to
   descriptor declarations, not generic instances.
6. The specialized `depends_on` clause establishes the dependency closure needed for resolution
   and lowers to the schema holon's semantic `DependsOn` relationship.
7. `Extends` uses optional single inheritance in the unified hierarchy rooted at abstract
   `TypeDescriptor`; `MetaTypeDescriptor Extends HolonType` establishes the meta-type branch.
8. Descriptor category and runtime-wrapper admissibility derive from resolved descriptor identity
   and transitive `Extends`. `TypeKind` is not authored or persisted descriptor state.
9. `InstanceProperties` and `InstanceRelationships` declarations inherit additively through a
   type's own `Extends` lineage; populated descriptor values follow their member descriptor's
   `InheritanceMode`.
10. Presence-based Boolean keywords lower to explicit `true`. Their absence is an omission, not a
   general implicit `false`; Holon Loading materializes `false` only when a required property
   declares that default.
11. Instance-contract declarations are ordinary populated relationships in the declaring
    descriptor's relationship map: `InstanceProperties` targets property descriptor keys, while
    `InstanceRelationships` targets declared relationship descriptor keys.
12. The TDL supports both:
    - complete schema files
    - documentation fragments.
13. The TDL supports both a compact line-oriented surface form and a braced
    block surface form. They are semantically equivalent.
14. Concrete-syntax parsers own syntax and source-to-`LoaderRefRep` lowering. Holon Loading owns
    automatic descriptor-default materialization; the Holon Validator invokes descriptor semantics
    through `HolonDescriptor` after the guest constructs the staged application graph.
15. TDL/JSON source-conversion fidelity compares normalized `LoaderRefRep` graphs, not concrete
    source text or default-materialized application holons.
16. Descriptor validity is derived from resolved descriptors. Validators must not replace
    descriptor-declared property, relationship, value, or inheritance rules with hard-coded
    schema-specific tables or name-based inference.
17. Loaded and runtime holons use the same `HolonDescriptor` surface for inheritance and effective
    descriptor behavior. The host-side TDL parser does not execute descriptor semantics.
18. Every TDL-produced holon is validated against
    `ConformanceContract(H) = EffectiveInstanceContract(DescribingType(H))`; its own `Extends`
    lineage separately determines classification and the contract it passes to described instances.
19. An abstract descriptor must satisfy positive minimums inherited from the universal descriptor
    baseline, `EffectiveInstanceContract(MetaTypeDescriptor.HolonType)`, but may omit a
    category-specific member introduced below that baseline. Supplied members, maximum
    cardinalities, and universal structural invariants remain fully validated. Non-abstract
    descriptors must satisfy the complete effective contract.

---

# 2. File Structure

A complete TDL file begins with a schema declaration.

```tdl
schema <SchemaKey>

Optional schema dependency clauses may follow:

depends_on <SchemaKey>
```

The document or its containing package must bind interpretation to a specific Core Schema version.
Ordinarily, the schema dependency closure supplies that binding. Requiredness, defaults,
descriptor kinds, relationships, cardinalities, and validation rules are resolved against that
version.

The schema declaration may also use the braced form when the schema holon
itself needs a header or openness flags:

`schema <SchemaKey> {
  SchemaBodyClause*
}`

All descriptors following this declaration implicitly compile with:

`ComponentOf <SchemaKey>`

The schema declaration key is the authored key of the schema holon contributed by the file.
`depends_on` entries are likewise schema holon keys. Schema creation validates the authored schema
key against the effective key rule of the bound `Schema` type.

`depends_on` binds the current versioned schema to an exact dependency schema identity. The
resulting schema dependency graph must be acyclic. A schema must not depend on itself, and no
dependency path may return to its source.

Every descriptor reference whose source and target are owned by different schemas requires a
direct `depends_on` declaration from the source schema to the target schema. A transitive
dependency makes the target available in the resolution closure but does not satisfy this direct
dependency declaration requirement.

Several TDL files may name and contribute to the same schema. Their components may use forward or
circular references because those references remain within one schema node. The multi-pass loader
resolves that within-schema closure; it does not make cycles among distinct schema holons valid.

Schema syntax is specialized because it establishes compilation and dependency-resolution scope
before ordinary holon validation. `depends_on` is therefore not merely relationship-map sugar,
although it lowers to the ordinary semantic `DependsOn` relationship.

Example:

`schema "MAP Metaschema-v0.0.2" {
  depends_on "MAP Core Schema-v0.0.7"

  header {
    description: "Schema containing MAP metaschema descriptors."
  }
}

def relationship (TypeDescriptor)-[ComponentOf]->(Schema) {
  type MetaDeclaredRelationshipType
  extends DeclaredRelationshipType
  source TypeDescriptor
  target Schema
}

property Description.PropertyType {
  type MetaPropertyType.MetaTypeDescriptor
  extends PropertyType.TypeDescriptor
  value MapStringValueType.StringValueType
  IsValueRequired true
}
`
---

# 3. Declaration Separation

Declarations are separated by:

- blank lines
- or the appearance of a new top-level declaration-form keyword.

Semicolons are not used. Commas are optional between entries in braced maps and lists.

Indentation is used for readability but is not semantically significant beyond grouping clauses under a descriptor.

Braces may be used to group descriptor bodies and nested blocks such as
`header`, `relationships`, and `variants`. The braced style is
the preferred house style for examples because it makes large schema
definitions easier to scan.

Map and list blocks remain newline-oriented by default. Commas are optional between relationship
map entries and variant entries. Commas are recommended between targets inside bracketed
relationship target collections. These rules do not apply to `header` fields.

---

# 4. Reserved Keywords

The following tokens are reserved:

schema  
instance
abstract  
value  
property  
relationship  
inverse  
def  
enum  
variant
holon  
type
extends  
source  
target  
instance_keyrule
cardinality  
deletion_semantic
ordered  
duplicates
depends_on
header
allows_additional_properties
allows_additional_relationships
relationships
variants

---

# 5. Declaration Forms

TDL provides the specialized compilation-scoping form:

schema

the generic holon form:

instance

and the following descriptor-oriented forms:

value  
property  
relationship  
inverse relationship  
enum  
variant  
holon

Each declaration compiles to a holon. Descriptor-oriented forms compile to type descriptor holons
and make descriptor-specific shorthand available. `instance` provides only explicit `type`, fixed
property assignments, and a relationship map.

The declaration form selects available surface clauses. It does not select or default a
declaration's `type` or classify the resulting holon. Category follows the resolved descriptor's
transitive `Extends` lineage.

---

# 6. Identity, Properties, and References

The key following a declaration-form label is the holon's explicitly authored key.
It is not merely a local symbol or a `type_name`.

Every non-schema declaration must provide exactly one:

    type <TypeKey>

The `type` key resolves the descriptor that describes the declared holon and lowers to the declared
holon's unique `DescribedBy` target. The authored key must conform to the effective instance key
rule supplied by that describing type. A holon descriptor's own `instance_keyrule` clause is
different: it populates `InstanceKeyRule` and governs holons described by that descriptor, not the
key of the descriptor itself.

References elsewhere in TDL use keys. A reference may resolve to a holon in the current schema
package or dependency closure. Key binding must produce exactly one resolved holon identity; later
semantic validation uses that identity and does not repeatedly group or resolve by key. Binding
must not fall back to `type_name`, display name, declaration form, or suffix inference.

The current unqualified-key model requires keys to be unique within that bound closure. How
independent Extension Schemas with colliding local keys coexist or qualify their references is part
of the deferred Extension Schema identity design, not an inference made by TDL.

A key or reference containing whitespace must be quoted. Delimiter-free keys may be written bare.
Quoting is lexical only and does not change key identity. Fully qualified relationship keys retain
their dedicated structural syntax.

A qualified relationship key has the form:

    (<SourceTypeKey>)-[<RelationshipName>]->(<TargetTypeKey>)

The complete expression identifies one authoritative declared relationship descriptor. Its source,
target, cardinality, deletion behavior, ordering, duplicate policy, inheritance mode, and inverse
pairing come from that descriptor. Using the key as a relationship-map target does not redeclare or
override any of those semantics.

Every relationship endpoint is a holon. Endpoint validation uses:

    EndpointCompatible(H, requiredType)
        =
    requiredType is in L(DescribingType(H))
        or
    requiredType is in L(H), when H participates in Extends

Every holon is classified through its describing type's lineage and, when it participates in
`Extends`, through its own lineage as well. Meta-types govern descriptor-holon conformance while
abstract descriptor categories such as `PropertyType`, `ValueType`, `RelationshipType`,
`DeclaredRelationshipType`, and `InverseRelationshipType` classify descriptor holons used in
descriptor-to-descriptor relationships. Qualified relationship keys therefore use those abstract
descriptor endpoint categories rather than their meta-types.

TDL uses one fixed property-assignment form for descriptor properties that do not have dedicated
surface syntax:

    <PropertyName> <PropertyValue>

The property name resolves through the describing type's effective property contract. That
contract determines the authoritative property descriptor, value type, requiredness, constraints,
and default. Ambiguous or undeclared names are errors unless the effective additional-property
policy permits them. The schema does not dynamically create new grammar productions or keywords.

Property member names and relationship member names come from the required local `TypeName` of
their descriptors and occupy separate namespaces. Within either namespace, binding compares exact,
case-sensitive `MapString` values without Unicode normalization. Any ergonomic spelling conversion
is an adapter operation performed before binding.

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

value MapLocalizedString.MapStringValueType
type MetaStringValueType.MetaValueType
extends MapStringValueType.StringValueType

Braced form:

value MapLocalizedString.MapStringValueType {
  type MetaStringValueType.MetaValueType
  extends MapStringValueType.StringValueType
}

Examples in this specification prefer the braced form.

---

# 8. Value Type Descriptors

Syntax:

[abstract] value <ValueTypeKey>
type <TypeKey>
[extends <TypeKey>]
Clause*
HeaderBlock?

or

[abstract] value <ValueTypeKey> {
  type <TypeKey>
  Clause*
  HeaderBlock?
}

Example:

abstract value ValueType.TypeDescriptor {
  type MetaValueType.MetaTypeDescriptor
}

value MapLocalizedString.MapStringValueType {
  type MetaStringValueType.MetaValueType
  extends MapStringValueType.StringValueType
}

Compilation rules:

- Require exactly one explicit `type` clause and lower it to `DescribedBy`.
- Lower `extends` only when explicitly authored. Omission produces no local `Extends` target.
- If `abstract` present → `is_abstract_type = true`.

---

# 9. Property Type Descriptors

Syntax:

[abstract] property <PropertyTypeKey>
type <TypeKey>
[value <ValueTypeKey>]
Clause*
HeaderBlock?

or

[abstract] property <PropertyTypeKey> {
  type <TypeKey>
  [value <ValueTypeKey>]
  Clause*
  HeaderBlock?
}

Example:

property Description.PropertyType {
  type MetaPropertyType.MetaTypeDescriptor
  extends PropertyType.TypeDescriptor
  value MapStringValueType.StringValueType
  IsValueRequired true
}

Compilation rules:

- Require exactly one explicit `type` clause and lower it to `DescribedBy`.
- Lower `extends` only when explicitly authored.
- `IsValueRequired`, `DefaultValue`, and non-default `InheritanceMode` values use the fixed
  descriptor-property assignment form.
- `DefaultValue` is valid only when `IsValueRequired` is `true`.
- If `InheritanceMode` is omitted, Holon Loading materializes the required descriptor default
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

relationship <RelationshipKey>
def relationship <RelationshipKey>

Syntax:

[abstract] [def] relationship <RelationshipKey>
type <TypeKey>
source <SourceType>
target <TargetType>
Clause*
HeaderBlock?

or

[abstract] [def] relationship <RelationshipKey> {
  type <TypeKey>
  source <SourceType>
  target <TargetType>
  Clause*
  HeaderBlock?
}

Example:

relationship (HolonType.TypeDescriptor)-[InstanceKeyRule]->(KeyRuleType.HolonType) {
  type MetaDeclaredRelationshipType.MetaRelationshipType
  extends DeclaredRelationshipType.RelationshipType
  source HolonType.TypeDescriptor
  target KeyRuleType.HolonType
  InheritanceMode Override
  cardinality 1..1
  deletion_semantic Allow
}

## 10.2 Definitional Relationship

def relationship <RelationshipKey>
source <SourceType>
target <TargetType>

Rules:

- Presence of `def` lowers to explicit `is_definitional = true`.
- Absence of `def` leaves the property omitted; Holon Loading materializes a declared
  required default such as `false`.

Declared relationship validation:

- Every declared relationship descriptor must provide exactly one `source` clause and exactly one
  `target` clause.
- The authored relationship key must conform to the effective key rule supplied by its explicit
  type.
- The source key, relationship name, and target key encoded by a qualified authored key must match
  the descriptor's populated `SourceType`, semantic relationship name, and `TargetType`.
- Every declared relationship descriptor must have exactly one inverse relationship descriptor paired with it.
- Every inverse relationship descriptor must point back to a declared relationship descriptor, and that declared relationship must point to no other inverse.
- The inverse descriptor's effective source constraint must equal the declared descriptor's
  effective target constraint, and its effective target constraint must equal the declared
  descriptor's effective source constraint. Directional cardinalities are validated independently
  and need not match.
- `min_cardinality` is a required semantic slot. `max_cardinality` is optional; absence means
  unbounded. When present, `min_cardinality <= max_cardinality`.
- A `cardinality min..*` clause lowers to the required minimum and omits `max_cardinality`. A
  finite upper bound lowers both properties.
- `DeletionSemantic` is required on every declared relationship descriptor and must be supplied
  explicitly when its property descriptor does not define a default.
- A non-default `InheritanceMode` uses the fixed descriptor-property assignment form. If omitted,
  Holon Loading materializes `None` when declared as the effective default.

## 10.3 Inverse Relationship

Syntax:

[abstract] inverse relationship <RelationshipKey>
type <TypeKey>
source <SourceType>
target <TargetType>
inverse <DeclaredRelationshipKey>
[extends <TypeKey>]
Clause*
HeaderBlock?

or

[abstract] inverse relationship <RelationshipKey> {
  type <TypeKey>
  source <SourceType>
  target <TargetType>
  inverse <DeclaredRelationshipKey>
  Clause*
  HeaderBlock?
}

Example:

inverse relationship (Schema)-[Components]->(TypeDescriptor) {
  type MetaInverseRelationshipType
  extends InverseRelationshipType
  source Schema
  target TypeDescriptor
  inverse (TypeDescriptor)-[ComponentOf]->(Schema)
  cardinality 0..*
  deletion_semantic Block
}

Rules:

- Require exactly one explicit `type` clause and lower it to `DescribedBy`.
- Lower `extends` only when explicitly authored.
- Require exactly one `source`, one `target`, and one `inverse` clause.
- Validate that the authored inverse relationship key matches its populated source, semantic name,
  and target and conforms to the effective key rule supplied by its explicit type.
- Validate that the inverse's effective source and target constraints mirror the paired declared
  relationship's effective target and source constraints. Do not require directional
  cardinalities to match.
- `def` is **not allowed** with inverse relationships.
- `InheritanceMode` follows the same property-assignment and guest materialization rule as declared
  relationships.
- `DeletionSemantic` is required on every inverse relationship descriptor and is directional. It
  must be authored or completed independently of the paired declared relationship.

`deletion_semantic` is valid only on relationship descriptors.

---

# 11. Enum Type Descriptors

Syntax:

[abstract] enum <EnumTypeKey>
type <TypeKey>
Clause*
VariantBlock?
HeaderBlock?

or

[abstract] enum <EnumTypeKey> {
  type <TypeKey>
  Clause*
  HeaderBlock?
  VariantBlock?
}

Example:

enum DeletionSemantic.MapEnumValueType {
  type MetaEnumValueType.MetaValueType
  extends MapEnumValueType.EnumValueType
}

or

enum DeletionSemantic.MapEnumValueType {
  type MetaEnumValueType.MetaValueType
  extends MapEnumValueType.EnumValueType
  variants {
    variant Allow {
      type MetaEnumVariantValueType.MetaValueType
      extends MapEnumVariantValueType.EnumVariantValueType
    }
  }
}

Variants may be declared inline, but each inline variant remains a descriptor declaration and must
include the `variant` keyword and an explicit `type` clause.

Compilation rules:

- Require exactly one explicit `type` clause and lower it to `DescribedBy`.
- Lower `extends` only when explicitly authored.

---

# 12. Enum Variant Descriptors

Variants compile to independent type descriptor holons.

Syntax:

variant <VariantKey>
type <TypeKey>
HeaderBlock?

or

variant <VariantKey> {
  type <TypeKey>
  HeaderBlock?
}

Example:

abstract variant EnumVariantValueType.ValueType {
  type MetaValueType.MetaTypeDescriptor
  extends ValueType.TypeDescriptor
}

This standalone form remains valid for cases where a variant needs to be
declared or documented separately from the enum's inline `variants` block.

Compilation rules:

- Require exactly one explicit `type` clause and lower it to `DescribedBy`.
- Lower `extends` only when explicitly authored.
- An inline variant lowers its enclosing enum key to `VariantOf`.
- A standalone variant must explicitly provide the equivalent enum ownership relationship through
  syntax defined by the bound enum-variant schema.

---

# 13. Holon Type Descriptors

Syntax:

[abstract] holon <HolonTypeKey>
type <TypeKey>
[extends <TypeKey>]
Clause*
[RelationshipMap]
HeaderBlock?

or

[abstract] holon <HolonTypeKey> {
  type <TypeKey>
  [extends <TypeKey>]
  Clause*
  [RelationshipMap]
  HeaderBlock?
}

Example:

holon Book {
  type MetaHolonType
  extends CulturalExpression
  allows_additional_properties

  relationships {
    InstanceProperties -> [
      Title.PropertyType,
      Author.PropertyType
    ]
    InstanceRelationships -> [
      (Book)-[WrittenBy]->(Person)
    ]
  }
}

Compilation rules:

- Require exactly one explicit `type` clause and lower it to `DescribedBy`.
- Lower `extends` only when explicitly authored.
- Lower the relationship map to populated relationships on the descriptor holon.
- `allows_additional_properties` and `allows_additional_relationships`
  populate the corresponding holon descriptor properties.

## 13.1 Instance-Contract Declarations

`InstanceProperties` and `InstanceRelationships` are declared through ordinary entries in the
descriptor's relationship map:

holon DanceInvocation.HolonType {
  type MetaHolonType.MetaTypeDescriptor
  extends HolonType.TypeDescriptor
  relationships {
    InstanceProperties -> [
      InvocationSource.PropertyType
    ]
    InstanceRelationships -> [
      (DanceInvocation.HolonType)-[Target]->(HolonType.TypeDescriptor),
      (DanceInvocation.HolonType)-[Request]->(HolonType.TypeDescriptor)
    ]
  }
}

Rules:

- Every `InstanceProperties` target must resolve by key to a property descriptor.
- Every `InstanceRelationships` target must resolve by key to a declared relationship descriptor.
- Inverse relationship descriptors are derived members of their declared relationship pairs and
  must not be explicitly targeted by `InstanceRelationships`.
- The target relationship descriptor is the authoritative source of the attached relationship's
  source, target, cardinality, deletion, ordering, duplicate, inheritance, and inverse semantics.
- A qualified relationship key used as a target is an identity reference, not an inline
  relationship declaration.
- Across `DescribedBy`, `InstanceProperties` governs entries in the described instance's property
  map and `InstanceRelationships` governs its populated declared relationships. TDL does not
  synthesize or require generic `Properties` or `Relationships` relationship descriptors.

## 13.2 Descriptor Relationship Map

Syntax:

relationships {
  <RelationshipKey> -> <TargetKey>
  <RelationshipKey> -> [
    <TargetKey>,
    <TargetKey>
  ]
}

Example:

abstract holon HolonType.TypeDescriptor {
  type MetaHolonType.MetaTypeDescriptor
  relationships {
    InstanceRelationships -> [
      (HolonType.TypeDescriptor)-[DescribedBy]->(TypeDescriptor),
      (HolonType.TypeDescriptor)-[OwnedBy]->(HolonSpace.HolonType)
    ]
    AffordsCommand -> [
      CloneHolon.CommandType,
      GetKey.CommandType
    ]
  }
}

Rules:

- Every map entry name either identifies a relationship member in the describing type's effective
  instance contract or is admitted by the effective additional-relationship policy. Binding selects
  one authoritative declared relationship descriptor identity; ambiguity is an error. Subsequent
  grouping and validation of declared occurrences use that identity rather than the name. A
  permitted undeclared relationship remains unbound and is grouped by its exact stored name.
- Every target must resolve by key and satisfy the authoritative relationship descriptor's target
  constraints.
- A scalar target is equivalent to a singleton target collection.
- Bracketed targets represent the complete locally populated target collection for that
  relationship map entry.
- Target ordering and duplicate handling follow the relationship descriptor.
- Commas between map entries are optional. Commas between bracketed targets are recommended.
- A relationship map may appear on any descriptor kind whose describing type permits the populated
  relationships; it is not limited to `holon` declarations.

## 13.3 Generic Holon Instance

Syntax:

```tdl
instance <HolonKey> {
  type <HolonTypeKey>
  <PropertyName> <PropertyValue>
  relationships {
    <RelationshipName> -> <TargetKey>
  }
}
```

Example:

```tdl
instance ImplementationName.FormatRule {
  type FormatRule.KeyRuleType
  TypeName "ImplementationName"
  TemplateString "{0}"
  relationships {
    TemplateParameters -> ImplementationName.PropertyType
  }
}
```

Rules:

- Require exactly one explicit `type` clause and lower it to `DescribedBy`.
- Validate the authored key against the effective `InstanceKeyRule` supplied by the explicit type.
- Resolve property assignments and relationship-map members through the describing type's
  effective instance contract.
- Do not admit descriptor-only shorthand such as `abstract`, `extends`, `instance_keyrule`,
  `source`, `target`, `cardinality`, or `variants`.
- Do not imply `ComponentOf`; that file-level convenience applies only to descriptor declarations.

---

# 14. Declaration Clauses

Clauses refine descriptor semantics.

The formal productions for clauses and nested blocks are defined in
Appendix B. The core clause families are:

- `ExtendsClause`
- `TypeClause`
- `ValueClause`
- `PropertyAssignmentClause`
- `SourceClause`
- `TargetClause`
- `InverseClause`
- `InstanceKeyRuleClause`
- `CardinalityClause`
- `DeletionSemanticClause`
- `RelationshipFlagClause`
- `HolonOpenFlagClause`
- `SchemaOpenFlagClause`
- `RelationshipMap`
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

Absence leaves the corresponding value omitted in `LoaderRefRep`. When the graph is submitted for
Holon Loading, the guest-side descriptor-default materialization service applies an effective
default where defined. TDL does not define a blanket Boolean default.

Example:

relationship (HolonType)-[ParentOf]->(HolonType) {
  type MetaDeclaredRelationshipType
  extends DeclaredRelationshipType
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

# 17. Explicit `DescribedBy` and Optional `Extends`

Every non-schema declaration must contain exactly one explicit `type` clause:

    type <TypeKey>

The clause lowers to the holon's unique `DescribedBy` relationship. Declaration-form labels such as
`instance`, `holon`, `property`, and `relationship` do not select, constrain, or default the
`type` target. The resolved describing type and its effective instance contract determine
self-conformance.

`type` and `extends` are independent:

- `type` determines the contract that the declared descriptor holon must satisfy;
- `extends` determines descriptor classification, inherited instance-contract declarations, and
  the lineage used for descriptor-member semantic inheritance.

The compiler must not merge the two paths.

Every descriptor may contain zero or one `extends` clause. If omitted, the descriptor has no local
`Extends` target. No declaration form supplies a default parent.

The unified hierarchy and reflective meta-type graph are therefore expressible without reserved
names or syntax exceptions:

abstract holon TypeDescriptor {
  type MetaHolonType.MetaTypeDescriptor
}

abstract holon HolonType.TypeDescriptor {
  type MetaHolonType.MetaTypeDescriptor
  extends TypeDescriptor
}

abstract holon MetaTypeDescriptor.HolonType {
  type MetaHolonType.MetaTypeDescriptor
  extends HolonType.TypeDescriptor
}

holon MetaHolonType.MetaTypeDescriptor {
  type MetaHolonType.MetaTypeDescriptor
  extends MetaTypeDescriptor.HolonType
}

The compiler resolves forward and self references in this explicitly authored graph. It must not
infer root status, self-description, meta-type membership, or inheritance from a descriptor's key
or declaration-form label.

The authored self-reference on `MetaHolonType.MetaTypeDescriptor` is the only permitted
`DescribedBy` cycle. Semantic validation rejects every other self-loop and every multi-holon
`DescribedBy` cycle. Repeatedly following `DescribedBy` from any declaration must reach the
reflective root without first repeating another resolved identity.

---

# 18. Extensibility Rules

TDL lowers `extends` to the shared Schema 2.0 `Extends` relationship. The grammar does not define a
parallel inheritance policy.

Validation rules:

- A descriptor may have at most one direct `Extends` target.
- Multi-step `Extends` chains are valid.
- The `Extends` target must resolve to a descriptor.
- The `Extends` graph must be acyclic.
- Every `Extends` edge must remain within the unified descriptor-type hierarchy rooted at abstract
  `TypeDescriptor`.
- No same-`TypeKind` compatibility rule applies to an `Extends` edge. Category compatibility is the
  graph classification established by the edge and resulting lineage.
- `TypeKind` and legacy `InstanceTypeKind` are not authored or completed properties in Schema 2.0.
  Source adapters must not synthesize them from declaration keywords. A populated legacy value is
  migration input, not current descriptor semantics.

The shared descriptor-semantics kernel supplies four related derived semantic views:

1. `EffectiveValues(T, M)` resolves every populated descriptor member according to its effective
   `InheritanceMode(M)` and collection policy. `None` returns the local collection, `Additive`
   combines effective ancestor contributions before local contributions, and `Override` selects
   the complete collection from the nearest type in the self-first lineage that populates `M`.
2. `EffectiveMemberDefinition(M)` resolves the semantic fields of a referenced property or
   relationship descriptor across that descriptor's own `Extends` lineage. It supplies the
   effective value type, requiredness, default, endpoints, cardinality, collection policy,
   deletion behavior, constraints, and `InheritanceMode` applicable to uses of `M`.
3. `EffectiveInstanceContract(T)` interprets the effective `InstanceProperties` and
   `InstanceRelationships` target collections as contract declarations. The Core Schema declares
   `Additive` for both relationships; the kernel does not provide a separate contract-inheritance
   algorithm.
4. `ConformanceContract(H) = EffectiveInstanceContract(DescribingType(H))` determines the
   properties and relationships that holon `H`, including a descriptor holon, must populate.

Effective collections retain semantic ordering and duplicate occurrences according to the member's
policy. Contract interpretation inspects contribution provenance so additive normalization cannot
hide an inherited-member redeclaration or a same-namespace member-name collision. `Override`
retains selected and shadowed provenance.

Descriptor self-conformance through `DescribedBy` is never flattened together with the descriptor's
own `Extends` lineage. Meta-type contract declarations therefore do not leak into ordinary
described-instance contracts.

Guest-side Holon Validation and runtime descriptor behavior access these rules through
`HolonDescriptor` and its typed descriptor wrappers. TDL parsing does not own or execute an
alternate contract, semantic-inheritance, or conformance algorithm.

Effective key-rule validation uses the same kernel semantics:

- `(HolonType.TypeDescriptor)-[InstanceKeyRule]->(KeyRuleType.HolonType)` has cardinality `1..1`
  and `InheritanceMode Override`.
- `instance_key_rule(T)` is the unique target in `EffectiveValues(T, InstanceKeyRule)`.
- `holon_key_rule(H) = instance_key_rule(DescribingType(H))`.
- Key-rule resolution does not perform an additional fallback through `DescribedBy`.
- Recognize the canonical key-rule descriptors `TypeNameRule.KeyRuleType`,
  `SchemaNameRule.KeyRuleType`, `EnumVariantRule.KeyRuleType`,
  `RelationshipRule.KeyRuleType`, `ExtendedTypeRule.KeyRuleType`,
  `DescribedTypeRule.KeyRuleType`, and `NoneRule.KeyRuleType`.
- Treat transitional `TypeKindRule.KeyRuleType` as unsupported until it is retired or redefined to
  consume a specified lineage-derived category rather than an authored property.
- Treat `NoneRule.KeyRuleType` as explicit keylessness, not as an absent `InstanceKeyRule`.
- `MetaTypeDescriptor.HolonType` supplies `ExtendedTypeRule.KeyRuleType` as the inherited default
  for descriptor holons. It composes local `type_name` with the immediate `Extends` target's local
  `type_name`, falling back to local `type_name` when `Extends` is absent.
- Because `Extends` is definitional, changing the immediate parent is a key-affecting breaking
  change for descriptor versions subsequently created under `ExtendedTypeRule`.
- `FormatRule.KeyRuleType` is concrete. Configured format rules are generic holon instances whose
  own keys are governed by `DescribedTypeRule.KeyRuleType`.
- Validate the required inputs for the selected key rule.
- Every descriptor key is authored. Report a diagnostic when it differs from the key generated by
  the effective instance key rule of the descriptor's explicit type.

A persisted holon's key is explicit stored state. A later schema version that changes the effective
key rule, an input to that rule, or a relevant descriptor ancestor does not recompute or mutate the
key of an existing holon version. New holons and explicitly created versions use the schema version
bound for their creation; migration and aliases are explicit operations.

---

# 19. Validation Model

TDL parsing reports malformed syntax and failures to lower source constructs into `LoaderRefRep`.
It does not perform loader-reference resolution or descriptor-driven Holon Validation.

When parser output is submitted for Holon Loading, guest diagnostics are layered by owner:

- the existing Holon Loader reports duplicate loader keys and unresolved keyed references;
- the descriptor-default materialization service reports failures to determine or apply a declared
  default;
- the Holon Validator reports descriptor-driven holon violations; and
- commit refuses persistence when blocking violations remain.

Source provenance retained with the loader input maps guest diagnostics back to TDL locations.
Source-to-source TDL/JSON conversion does not require guest validation.

After guest graph construction, reference resolution, and descriptor-default materialization,
every loaded holon is validated by conformance to its resolved descriptor. Representation-level
bootstrapping may provide only the
minimal decoding machinery needed to resolve explicitly authored keys and references; it does not
create semantically exempt descriptor holons or supply omitted Core Schema relationships.

Effective-product computation precedes conformance validation. The kernel computes and memoizes
lineages, effective values, effective contracts, effective member definitions, and key rules by
product kind and resolved descriptor identity for the completed graph snapshot. It then validates
all holons, including `MetaHolonType.MetaTypeDescriptor`, against those products. Resolving the
reflective root's conformance contract selects its own already computed effective instance
contract; it does not recursively validate the root.

1. Resolve exactly one `DescribedBy` target for every holon.
2. Require the describing type to be non-abstract and satisfy the graph-derived describing-lineage
   compatibility rule.
3. Obtain `ConformanceContract(H)` from
   `EffectiveInstanceContract(DescribingType(H))`.
4. Validate required properties and relationships and the describing type's applicable
   additional-member policies.
5. Resolve populated descriptor values through `EffectiveValues(T, M)` and the effective
   `InheritanceMode(M)` from `EffectiveMemberDefinition(M)`.
6. Resolve each property's `PropertyType` and `ValueType`, then validate primitive value
   shape, enum membership, cardinality, and applicable value constraints. String length is counted
   in Unicode grapheme clusters.
7. Reject `DefaultValue` on optional properties. Validate every permitted default against the same
   constraints as the required property it defaults.
8. Bind declared property and relationship names to exactly one descriptor identity in their
   separate namespaces, then validate declared occurrences grouped by that identity. Keep
   policy-permitted undeclared additions unbound and group them by exact stored name within their
   respective property or relationship namespace.
9. Validate relationships using their resolved descriptors, including effective cardinality,
   cumulative-classification source and target compatibility, inverse pairing, and the
   additional-relationship policy. An abstract descriptor may serve as an endpoint type anchor;
   abstractness prevents instantiation, not classification.
10. Apply the same process to descriptor holons. Descriptor self-conformance comes from the
    explicit type selected by `DescribedBy`; the descriptor's own `Extends` lineage
    separately determines classification and the contract it passes to described instances.

TDL property declarations populate `IsValueRequired` through the fixed descriptor-property
assignment form. Once lowered, requiredness is descriptor data consumed through the effective
contract, not a descriptor-kind switch statement.

The structural machinery needed to decode keys, properties, relationships, and references must be
small and representation-oriented. It may establish enough representation structure to resolve
the explicitly authored descriptor graph, but it must not create inferred `DescribedBy` or
`Extends` edges, embed Core Schema property names, enum variants, required-slot tables, or
descriptor-family validity rules.

Some model-wide invariants are evaluated after individual holon conformance, including closed-world
symbol uniqueness, inheritance cycles, schema-dependency acyclicity and coverage, inverse-pair
consistency, and effective-key uniqueness.
These checks consume resolved descriptor identity, effective contracts, and effective values rather
than inferred descriptor families.

Uniqueness validation is closed-world. TDL validation flags duplicate canonical symbols or keys,
duplicate local property names, duplicate local relationship names, and duplicate inverse ownership
inside the model being validated. Property and relationship names use separate namespaces. This
validation does not check whether another persisted MAP schema outside the bound package and
dependency closure uses the same key or symbol.

Scoped schema-semantic validation failures are blocking errors. Warnings are reserved for
compatibility aliases or non-canonical source-adapter observations that do not make the completed
explicit holon graph semantically invalid.

# 20. Parser and Holon Loading Responsibilities

A TDL compiler must:

1. Lower explicit and file-implied relationships:
    - lower each required non-schema `type` clause to exactly one `DescribedBy` target
    - lower `extends` only when explicitly authored
    - imply `ComponentOf` from the containing schema declaration for descriptor declarations only
    - lower schema `depends_on` keys to the schema holon's `DependsOn` loader relationship
2. Populate schema declaration bodies into the schema holon descriptor,
   including:
    - schema `header`
    - schema openness flags
3. Lower generic instances from explicit property assignments and relationship maps without
   descriptor shorthand or implicit `ComponentOf`.
4. Populate declaration-form-derived descriptor properties:
    - type_name
    - display_name
    - explicit `is_abstract_type = true` when `abstract` is present
5. Convert clauses and relationship maps into `LoaderRefRep` holons, properties, and keyed
   relationships, including:
    - `ValueType`
    - `DefaultValue`
    - `InheritanceMode`
    - `IsValueRequired`
    - `SourceType`
    - `TargetType`
    - `InverseOf`
    - `InstanceKeyRule`
    - `deletion_semantic`
    - `InstanceProperties`
    - `InstanceRelationships`
6. Preserve explicitly authored, file-implied, or keyword-lowered values and omissions. For source
   conversion, serialize the resulting `LoaderRefRep` as MAP JSON or project it to canonical TDL.
   Do not materialize defaults or run descriptor-driven validation on the host.
7. When loading, submit `LoaderRefRep` through the existing Holon Loader client. Guest loader
   components construct and resolve the staged application graph, materialize applicable defaults,
   and invoke commit. The commit-owned Holon Validator validates:
    - single inheritance
    - membership in the unified `TypeDescriptor` hierarchy, including
      `MetaTypeDescriptor Extends HolonType`
    - acyclic `Extends` chains
    - exactly one `DescribedBy` relationship for every holon
    - exactly one `DescribedBy` cycle: the authored self-loop at
      `MetaHolonType.MetaTypeDescriptor`; every other describing chain converges on that root
    - non-abstract describing-type admissibility through `TypeDescriptor`
    - descriptor conformance for every descriptor holon
    - self-conformance of `MetaHolonType.MetaTypeDescriptor` against its own effective instance
      contract, including any required member added to that contract
    - abstract descriptor completeness: a positive-minimum member may be omitted only when the
      descriptor holon is abstract and the member is category-specific rather than part of
      `EffectiveInstanceContract(MetaTypeDescriptor.HolonType)`; supplied members and universal
      structural invariants remain fully validated
    - additive effective instance contracts, including inherited-identity redeclaration and
      same-namespace member-name collision errors
    - required and additional properties through `ConformanceContract`
    - property values through their resolved value descriptors, including enum membership and
      effective cardinality, value constraints, default validity, and grapheme-cluster string
      lengths
    - populated descriptor values through the `InheritanceMode` values `None`, `Additive`, or
      `Override`,
      including duplicate handling and provenance
    - allowed relationships, cardinality, cumulative-classification source/target compatibility, and
      additional-relationship policy through effective relationship descriptors
    - closed-world symbol and key uniqueness
    - relationship inverse-pair completeness
    - qualified relationship declaration keys agree with their source, relationship name, and
      target
    - required non-negative minimum cardinality, optional non-negative maximum cardinality, and
      `min_cardinality <= max_cardinality` when a maximum is present
    - effective key-rule resolution and generated-key consistency when an authored key is present
    - relationship definitional rules
    - every non-schema declaration supplies exactly one explicit `type` clause
    - the versioned schema `DependsOn` graph is acyclic
    - every direct cross-schema descriptor reference is covered by a direct `DependsOn` edge from
      the source component's schema to the target component's schema
    - the declaration key conforms to the effective key rule supplied by its explicit type
    - declaration-form labels do not infer `DescribedBy`, `Extends`, or authored category metadata
    - `TypeKind` and legacy `InstanceTypeKind` are absent from descriptor state; runtime category
      projection and typed-wrapper selection use resolved identity and transitive `Extends`
    - abstract descriptors, including hierarchy roots, may be type anchors but are not valid
      `DescribedBy` targets
    - every holon is described by a concrete admissible type under `TypeDescriptor`
    - `deletion_semantic` appears only on relationship descriptors
    - openness flags appear only on holon descriptors or schema declarations
    - generic instances use only their generic property and relationship surfaces and receive no
      implicit `ComponentOf`
    - every declared property and relationship name resolves unambiguously in its own namespace to
      a descriptor identity permitted by the describing type's effective contract, and declared
      occurrence grouping uses that identity; an unbound name is accepted only when the applicable
      additional-member policy permits it
    - `InstanceProperties` targets resolve to property descriptors
    - `InstanceRelationships` targets resolve only to declared relationship descriptors
    - relationship-map targets satisfy their authoritative relationship descriptors.

# 21. Semantic Diff, Fidelity, and Loader Projection

TDL/JSON source-conversion fidelity compares deterministic projections of `LoaderRefRep`, including
loader holon keys, descriptor keys, explicit properties, keyed relationships, ordering, and literal
values. Formatting, JSON field order, and equivalent source-format shorthand are not differences.

Fidelity checks do not require guest construction, default materialization, or descriptor-driven
Holon Validation. A separate load operation may submit either source representation through the
existing Holon Loader flow and report guest diagnostics.

---

# 22. Example TDL File

```
schema "MAP Metaschema-v0.0.2" {
  depends_on "MAP Core Schema-v0.0.7"

  header {
    description: "Schema containing MAP metaschema descriptors."
  }
}

def relationship (TypeDescriptor)-[ComponentOf]->(Schema.HolonType) {
  type MetaDeclaredRelationshipType.MetaRelationshipType
  extends DeclaredRelationshipType.RelationshipType
  source TypeDescriptor
  target Schema.HolonType
  cardinality 1..1
  deletion_semantic Block

  header {
    description: "Links a type descriptor to the schema that contains it."
  }
}

inverse relationship (Schema.HolonType)-[Components]->(TypeDescriptor) {
  type MetaInverseRelationshipType.MetaRelationshipType
  extends InverseRelationshipType.RelationshipType
  source Schema.HolonType
  target TypeDescriptor
  inverse (TypeDescriptor)-[ComponentOf]->(Schema.HolonType)
  cardinality 0..*
  deletion_semantic Block
}

property Description.PropertyType {
  type MetaPropertyType.MetaTypeDescriptor
  extends PropertyType.TypeDescriptor
  value MapStringValueType.StringValueType
  IsValueRequired true
}

value MapStringValueType.StringValueType {
  type MetaStringValueType.MetaValueType
  extends StringValueType.ValueType
}

holon Schema.HolonType {
  type MetaHolonType.MetaTypeDescriptor
  instance_keyrule SchemaNameRule.KeyRuleType
  extends HolonType.TypeDescriptor
  allows_additional_properties

  relationships {
    InstanceProperties -> [
      Description.PropertyType
    ]
  }
}
```

# Appendix A: TDL Keyword Contracts

This section provides a concise list of the rules used on decompile (from JSON->TDL) to replace JSON clauses with keywords. And likewise, to expand keywords into JSON clauses on compile (TDL->JSON).

## Global Principles

| Principle | Contract |
| --- | --- |
| One interchange representation | JSON and TDL both parse to `LoaderRefRep`. Holon Loading resolves that graph into the staged Holons Core representation. |
| Compile direction | Each keyword defines what semantic content is injected or lowered when authoring TDL. |
| Decompile direction | Each keyword defines what canonical holon content may collapse back into the concise TDL surface. |
| Losslessness | Decompile may collapse content only when recompiling would produce the same semantic holon content. |
| Implied content | Decompile should omit only content implied by file structure or explicit keyword semantics. Declaration form does not imply `DescribedBy`, `Extends`, or descriptor-default values. Derived category projections are not serialized. |
| Fixed property form | Schema-defined properties without dedicated syntax use `<PropertyName> <PropertyValue>` and lower that authored key and value into `LoaderRefRep`. |
| Literal residue | If current TDL cannot express some content truthfully, preserve that content in literal form rather than collapsing it incorrectly. |
| Explicit type and inheritance | Every non-schema declaration emits its explicit `type`; descriptor forms emit `extends` exactly when a local `Extends` target exists. |
| No name-based reinterpretation | Decompile and compile behavior are driven by explicit syntax and resolved descriptors, not by reserved-looking names or declaration-form defaults. |
| File membership | A file-level `schema` declaration implies `ComponentOf <SchemaKey>` for descriptor declarations only. That implied relationship should not be repeated in concise decompiled descriptors. |

## Keyword Contracts

| Keyword | Compile (TDL -> LoaderRefRep) | Decompile (LoaderRefRep -> TDL) |
| --- | --- | --- |
| `schema` | Declare the schema key for the file; lower `depends_on`; imply `ComponentOf` for following descriptors; lower schema header and openness content. | Emit the schema key and dependencies; omit descriptor-local `ComponentOf` values implied by file membership. |
| `instance` | Author a generic holon from an explicit `type`, fixed property assignments, and a relationship map. It does not imply descriptor metadata or `ComponentOf`. | Emit a generic instance when no descriptor-oriented declaration form applies losslessly. |
| declaration form | Select the surface clauses available for the authored holon shape. It does not infer `DescribedBy`, `Extends`, or category metadata. | Select a lossless surface form from explicit holon semantics without omitting `type` or populated state; do not emit derived category projections as properties. |
| `type` | Resolve the supplied type key and lower it to the declaration's unique `DescribedBy` target. Validate the declaration key against that type's effective instance key rule. | Always emit the resolved `DescribedBy` target as `type <TypeKey>`. |
| `abstract` | Set `is_abstract_type = true`. | Collapse an explicit true value to the `abstract` prefix when lossless. |
| `def` | On declared relationships only, set `is_definitional = true`. | Collapse an explicit true value to `def`; never emit `def` for inverse relationships. |
| `extends` | Lower to one local `Extends <TargetKey>` relationship. Omission produces no local `Extends`. | Emit `extends` exactly when the descriptor has a local `Extends` target. |
| `value` clause | On property descriptors, lower to `ValueType <ValueTypeKey>`. | Collapse the populated `ValueType` relationship when representable exactly. |
| descriptor property | Lower the authored property key and value into `LoaderRefRep`. | Emit schema-defined descriptor properties through the same fixed form. |
| `source` | On relationship descriptors, lower to `SourceType <SourceTypeKey>`. | Collapse the populated `SourceType` relationship when representable exactly. |
| `target` | On relationship descriptors, lower to `TargetType <TargetTypeKey>`. | Collapse the populated `TargetType` relationship when representable exactly. |
| `inverse` | On inverse relationship descriptors, lower the declared relationship key through the bound inverse-pair semantics. | Emit the declared relationship key when the inverse pairing is representable exactly. |
| `instance_keyrule` | Lower to `InstanceKeyRule <KeyRuleKey>` on a holon-type descriptor. The target governs holons described by that descriptor, not the descriptor's own key. | Collapse the populated `InstanceKeyRule` target to `instance_keyrule`. |
| `relationships { ... }` | Resolve each map entry name through the describing type's effective relationship contract and lower its target keys to a populated descriptor relationship. `InstanceProperties` targets property keys; `InstanceRelationships` targets declared relationship keys. | Emit locally populated relationship target collections as map entries, preserving member names, complete target collections, and ordering when applicable. |
| `header { ... }` | Lower header fields such as description/display fields/type plural metadata to descriptor properties.                                                                                                                                                                                            | Collapse header-shaped descriptor properties back into `header { ... }` whenever they are representable by the header surface; omit compiled-form duplicates that are fully implied by concise header syntax.                                                                                                                                                                                                                                                                          |
| openness flags | Lower `allows_additional_properties` and `allows_additional_relationships` to explicit `true` descriptor or schema Boolean properties; preserve absent flags as omissions in `LoaderRefRep`. | Collapse true values back to presence-based flags on `schema` or `holon`; preserve explicit false values. |
| `cardinality` | Lower the minimum to `min_cardinality`; lower a finite maximum to `max_cardinality`, while `*` omits it. | Emit `cardinality min..max` for a finite maximum or `cardinality min..*` when `max_cardinality` is absent. |
| `deletion_semantic` | Lower to the relationship descriptor property of the same semantic name.                                                                                                                                                                                                                         | Collapse the property back to the `deletion_semantic` clause on relationship descriptors only.                                                                                                                                                                                                                                                                                                                                                                                         |
| `ordered` / `duplicates` | Set the corresponding relationship Boolean properties to explicit `true`; preserve absent flags as omissions in `LoaderRefRep`. | Collapse true values back to presence-based flags; preserve explicit false values. |


# Appendix B. TDL Grammar (EBNF)

The grammar below defines the concrete descriptor syntax. It is intentionally
syntactic rather than semantic: rules such as unified-hierarchy `Extends` validity,
descriptor conformance, required minimum cardinality, optional maximum cardinality, relationship inverse completeness,
and "inverse relationships cannot be definitional" are enforced by validation, not by
the grammar itself.

Lexical conventions:

- `Identifier` means a valid MAP identifier token.
- `BareReference` means a delimiter-free MAP key token, including compound keys such as
  `Description.PropertyType`.
- `QuotedReference` means a JSON string containing a MAP key, required when the key contains
  whitespace.
- `Reference` means either reference form; quoting does not change key identity.
- `DescriptorKey` means either a `Reference` or a fully qualified relationship key.
- `Literal` means a JSON-style scalar literal accepted in descriptor-property assignments or
  header fields.
- `Integer` means a non-negative base-10 integer literal.
- `NL` means one or more line breaks.

```ebnf
File                    ::= SchemaSection DeclarationSection ;

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

DeclarationSection      ::= Declaration { DeclarationGap Declaration } ;
DeclarationGap          ::= NL { NL } ;

Declaration             ::= InstanceDecl
                         | ValueDecl
                         | PropertyDecl
                         | DeclaredRelationshipDecl
                         | InverseRelationshipDecl
                         | EnumDecl
                         | VariantDecl
                         | HolonDecl ;

InstanceDecl            ::= "instance" Reference
                            ( CompactInstanceBody | BracedInstanceBody ) ;

CompactInstanceBody     ::= NL TypeClause NL { InstanceBodyClause NL } ;
BracedInstanceBody      ::= "{" NL TypeClause NL { InstanceBodyClause NL } "}" ;
InstanceBodyClause      ::= PropertyAssignmentClause
                         | RelationshipMap ;

ValueDecl               ::= [ "abstract" ] "value" DescriptorKey
                            ( CompactValueBody | BracedValueBody ) ;

CompactValueBody        ::= NL TypeClause NL { ValueBodyClause NL } ;
BracedValueBody         ::= "{" NL TypeClause NL { ValueBodyClause NL } "}" ;
ValueBodyClause         ::= ExtendsClause
                         | PropertyAssignmentClause
                         | RelationshipMap
                         | HeaderBlock ;

PropertyDecl            ::= [ "abstract" ] "property" DescriptorKey
                            ( CompactPropertyBody | BracedPropertyBody ) ;

CompactPropertyBody     ::= NL TypeClause NL { PropertyBodyClause NL } ;
BracedPropertyBody      ::= "{" NL TypeClause NL { PropertyBodyClause NL } "}" ;
PropertyBodyClause      ::= ExtendsClause
                         | ValueClause
                         | PropertyAssignmentClause
                         | RelationshipMap
                         | HeaderBlock ;

DeclaredRelationshipDecl ::= [ "abstract" ] [ "def" ] "relationship" DescriptorKey
                             ( CompactDeclaredRelationshipBody
                             | BracedDeclaredRelationshipBody ) ;

CompactDeclaredRelationshipBody ::= NL
                                    TypeClause NL
                                    { DeclaredRelationshipBodyClause NL } ;

BracedDeclaredRelationshipBody ::= "{" NL
                                     TypeClause NL
                                     { DeclaredRelationshipBodyClause NL }
                                   "}" ;

DeclaredRelationshipBodyClause ::= SourceClause
                                 | TargetClause
                                 | ExtendsClause
                                 | CardinalityClause
                                 | DeletionSemanticClause
                                 | RelationshipFlagClause
                                 | PropertyAssignmentClause
                                 | RelationshipMap
                                 | HeaderBlock ;

InverseRelationshipDecl ::= [ "abstract" ] "inverse" "relationship" DescriptorKey
                            ( CompactInverseRelationshipBody
                            | BracedInverseRelationshipBody ) ;

CompactInverseRelationshipBody ::= NL
                                   TypeClause NL
                                   { InverseRelationshipBodyClause NL } ;

BracedInverseRelationshipBody ::= "{" NL
                                    TypeClause NL
                                    { InverseRelationshipBodyClause NL }
                                  "}" ;

InverseRelationshipBodyClause ::= SourceClause
                                | TargetClause
                                | InverseClause
                                | ExtendsClause
                                | CardinalityClause
                                | DeletionSemanticClause
                                | RelationshipFlagClause
                                | PropertyAssignmentClause
                                | RelationshipMap
                                | HeaderBlock ;

EnumDecl                ::= [ "abstract" ] "enum" DescriptorKey
                            ( CompactEnumBody | BracedEnumBody ) ;

CompactEnumBody         ::= NL TypeClause NL { EnumBodyClause NL } ;
BracedEnumBody          ::= "{" NL TypeClause NL { EnumBodyClause NL } "}" ;
EnumBodyClause          ::= ExtendsClause
                         | PropertyAssignmentClause
                         | RelationshipMap
                         | HeaderBlock
                         | VariantBlock ;

VariantDecl             ::= "variant" DescriptorKey
                            ( CompactVariantBody | BracedVariantBody ) ;

CompactVariantBody      ::= NL TypeClause NL { VariantBodyClause NL } ;
BracedVariantBody       ::= "{" NL TypeClause NL { VariantBodyClause NL } "}" ;
VariantBodyClause       ::= ExtendsClause
                         | HeaderBlock
                         | RelationshipMap
                         | PropertyAssignmentClause ;

HolonDecl               ::= [ "abstract" ] "holon" DescriptorKey
                            ( CompactHolonBody | BracedHolonBody ) ;

CompactHolonBody        ::= NL TypeClause NL { HolonBodyClause NL } ;
BracedHolonBody         ::= "{" NL TypeClause NL { HolonBodyClause NL } "}" ;
HolonBodyClause         ::= ExtendsClause
                         | InstanceKeyRuleClause
                         | PropertyAssignmentClause
                         | HeaderBlock
                         | HolonOpenFlagClause
                         | RelationshipMap ;

HolonOpenFlagClause     ::= "allows_additional_properties"
                         | "allows_additional_relationships" ;

TypeClause              ::= "type" DescriptorKey ;
ExtendsClause           ::= "extends" DescriptorKey ;
ValueClause             ::= "value" DescriptorKey ;
PropertyAssignmentClause ::= Identifier PropertyValue ;
PropertyValue           ::= Literal | DescriptorKey ;
SourceClause            ::= "source" DescriptorKey ;
TargetClause            ::= "target" DescriptorKey ;
InverseClause           ::= "inverse" DescriptorKey ;
InstanceKeyRuleClause   ::= "instance_keyrule" DescriptorKey ;
CardinalityClause       ::= "cardinality" Integer ".." CardinalityMaximum ;
CardinalityMaximum      ::= Integer | "*" ;
DeletionSemanticClause  ::= "deletion_semantic" Reference ;

RelationshipFlagClause  ::= "ordered"
                         | "duplicates" ;

RelationshipMap         ::= "relationships" "{" NL
                              { RelationshipAssignment [ "," ] NL }
                            "}" ;

RelationshipAssignment  ::= Identifier "->" RelationshipTargets ;

RelationshipTargets     ::= DescriptorKey
                         | "[" NL
                             { DescriptorKey [ "," ] NL }
                           "]" ;

QualifiedRelationshipKey ::= "(" DescriptorKey ")-[" Identifier "]->("
                              DescriptorKey ")" ;

DescriptorKey           ::= Reference
                         | QualifiedRelationshipKey ;

Reference               ::= BareReference | QuotedReference ;

VariantBlock            ::= "variants" "{" NL
                              { VariantItem [ "," ] NL }
                            "}" ;

VariantItem             ::= VariantDecl ;

HeaderBlock             ::= "header" "{" NL
                              { HeaderField NL }
                            "}" ;

HeaderField             ::= Identifier ":" Literal ;
```
