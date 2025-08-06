# MAP Type System

The **MAP Type System** is designed to support a living, evolving agent-centric ecosystem — one in which all data structures are self-describing, composable, and extensible by agents. This page introduces the _MAP Type System_ by walking through the foundational concepts, built-in types, and extension mechanisms that power it.

All MAP types belong to one of the following layers:

| Layer | Name            | Purpose                                           | Examples                                    |
|-------|-----------------|---------------------------------------------------|---------------------------------------------|
| 1     | Base Types      | Foundational type layer portable across languages | MapString, MapBytes                         |
| 2     | Core Types      | Types required by the MAP core code itself        | RelationshipName, Holon                     |
| 3     | Extension Types | Agent-Defined Types                               | Book Holon Type, STEWARDS Relationship Type |

---

# 🔹 Layer 1: Base Types and Base Values

**BaseTypes** are the foundational, portable types in the MAP system.  The Base Type determines how a given value will actually be represented in different programming language environments. (i.e., TypeScript and JSON on the client and Rust on the server-side). The Base Types layer includes scalar types (e.g., MapInteger, MapString) and compound types (e.g., MapBytes). The set of Base Types is fixed for any given version of the MAP. Changes or additions to any of these types requires a recompile of the MAP code and an evolution of the persistent data stored using a prior version of the MAP.

✅ Principle: Preserve Type Identity Across Platforms
* The Base Type name should be treated as portable name, used consistently across environments, and interpretable as such by the MAP type system.
* In Rust, we get this via `pub struct MapString(pub String)` — which gives us a unique type identity at the compiler level.
* In TypeScript, and even JSON, we can do similar things — not with strong typing, but through type aliases, tagging, or enforced schema constraints.

### Current Base Types with Portable Name Bindings

The set of Base Types offered by the MAP with their language bindings are shown in the following table.


| Base Type      | Rust Binding                          | TypeScript Binding                         | JSON Binding (Tagged Format)                   |
|----------------|---------------------------------------|--------------------------------------------|------------------------------------------------|
| `MapString`    | `pub struct MapString(pub String)`    | `export type MapString = string;`          | `{ "type": "MapString", "value": "..." }`      |
| `MapBoolean`   | `pub struct MapBoolean(pub bool)`     | `export type MapBoolean = boolean;`        | `{ "type": "MapBoolean", "value": true }`      |
| `MapInteger`   | `pub struct MapInteger(pub i64)`      | `export type MapInteger = number;`         | `{ "type": "MapInteger", "value": 42 }`        |
| `MapEnumValue` | `pub struct MapEnumValue(pub String)` | `export type MapEnumValue = string;`       | `{ "type": "MapEnumValue", "value": "DRAFT" }` |
| `MapBytes`     | `pub struct MapBytes(pub Vec<u8>)`    | `export type MapBytes = string; // base64` | `{ "type": "MapBytes", "value": "aGVsbG8=" }`  |


### Base Values

MAP represents actual runtime values using the `BaseValue` enum. This enum wraps each of the base types, enabling them to be used uniformly in property maps, serialized holons, and validation contexts.

    pub enum BaseValue {
        StringValue(MapString),
        BooleanValue(MapBoolean),
        IntegerValue(MapInteger),
        EnumValue(MapEnumValue),
        BytesValue(MapBytes),
    }

Each variant corresponds to a specific MAP Base Type. This allows property values to be stored and inspected in a type-safe and introspectable way.

Only `BaseValue` variants may be used as `PropertyValue`s within a holon's `PropertyMap`:

    pub type PropertyValue = BaseValue;
    pub type PropertyMap = BTreeMap<PropertyName, Option<PropertyValue>>;

By wrapping all scalar values in a unified enum, MAP ensures that holon properties are portable, self-describing, and easy to serialize and deserialize across environments.

### Notes

- **Rust bindings use the newtype pattern** (e.g. `pub struct MapString(pub String)`) to distinguish each base type with a unique identity while still leveraging native Rust primitives. This allows custom trait implementations, typed serialization, and compile-time safety.

- **All types derive `Clone`, `PartialEq`, and other basic traits**, ensuring they are usable in Holochain entry types, maps, and standard logic.

- **Display implementations** are provided for all base types and for `BaseValue`, with formatting that is human-readable and variant-specific. This is especially helpful for debugging, logging, or visualization.

- **`BaseValue`** acts as the unified runtime representation of scalar values. Its variant names are aligned with the base type wrappers (e.g., `StringValue(MapString)`), and it includes:
    - A method `into_bytes()` for deterministic binary encoding
    - A `Display` implementation
    - A `From<&BaseValue> for String` conversion (via `Into<String>`)

- **TypeScript bindings** are currently defined as simple aliases (e.g., `type MapString = string`) for interoperability with JSON and browser-based UIs. This preserves the MAP naming scheme in typed code.

- **JSON bindings** assume a tagged format for clarity and round-tripping, such as:

  {
  "type": "StringValue",
  "value": "Hello"
  }

- **`ValueType`** defines the kind of scalar value a property can hold, and is used within type descriptors to constrain values semantically (e.g., enforce that a field is a `String`, `Integer`, etc.).

- The previously defined `BaseType` enum has been removed. Its responsibilities are now handled more cleanly by:
    - `TypeKind` — for classifying descriptors at the schema level (e.g., `Property`, `Value`, `Relationship`)
    - `ValueType` — for describing scalar semantics in descriptors
    - `BaseValue` — for representing actual runtime values

---

### ❓ Open Design Questions

- **Should the inner fields of base types be made private?**  
  This would allow constructors to enforce normalization or validation (e.g., trimming, case enforcement), and would encourage use of `.as_str()` or `.into_inner()` methods over `.0` direct access.

- **Should branded types be adopted in TypeScript?**  
  While simple aliases preserve type names, branded types (e.g., `type MapString = string & { __brand: "MapString" }`) could prevent accidental interchange of semantically distinct types and support safer form generation and validation.

- **Should base types provide a standard set of convenience methods?**  
  Common methods like `new()`, `as_str()`, `len()`, or `is_empty()` could make the base types more ergonomic and reduce boilerplate.

- **Should `BaseValue::into_bytes()` support alternate encodings?**  
  The current implementation uses an 8-byte big-endian format for integers, which is excellent for deterministic hashing but not ideal for human readability or interop. Supporting multiple encoding strategies (e.g., base10 strings, compact varints) could provide more flexibility.

- **Should a `MapBytes` wrapper support bidirectional base64 conversion?**  
  Since JSON and TypeScript serialize `Vec<u8>` as base64 strings, `MapBytes` might benefit from explicit `to_base64()` and `from_base64()` methods to clarify this boundary.

- **Should `MapEnumValue` wrap a `MapString`, or should it just hold a `String` directly?**  
  While the current design is semantically layered, it might introduce unnecessary indirection or confusion. Alternatives could simplify usage or increase clarity.

- **Is there any residual role for a unified base type abstraction?**  
  With the removal of the `BaseType` enum, responsibilities are clearly separated, but future scenarios (e.g., type-based visualizer dispatch or schema browsing tools) might benefit from an abstraction that spans both runtime and schema-level categories.

---


# 🔹 Layer 2: Core Types

In MAP, **Core Types** are predefined, system-governed types that classify values the platform depends on for schema modeling, behavior definition, and runtime introspection. They are the types that the MAP codebase directly relies on — including names, identifiers, constraints, and semantic categories.

Whereas Base Types represent primitive value kinds (like strings and booleans), Core Types represent **semantically meaningful categories of values**. These categories are not arbitrary — they are essential to the functioning of MAP’s schema and behavior systems.

### ✅ What Is a Core Type?

A _**Core Type**_ is any type that:

- Is defined by the MAP core schema
- Has known structure, semantics, and naming conventions
- Is used directly by MAP’s validation, introspection, and behavior logic
- Classifies values that appear throughout schemas, holons, and type descriptors

Importantly, Core Types are not defined structurally differently than other types. What makes them “core” is their role: **the MAP system logic depends on them being present and correctly defined**.

### ✅ Examples of Core Types

Core Types include both:

1. **Meta-Type Core Types** — types that classify other types (e.g., types of properties, relationships, holons)
2. **Attribute and Enum Core Types** — types that classify values, labels, configuration options, and system-level constraints


#### 🧱 Meta-Type Core Types (as Types)

- `MetaPropertyType` — classifies named, typed properties (e.g., `"title"`, `"published_date"`)
- `MetaHolonType` — classifies categories of holons (e.g., `BookType`, `PersonType`)

#### 🔣 Attribute and Enum Core Types

These classify reusable values and system-defined semantics:

- `PropertyName` — classifies names of properties (e.g., `"title"`, `"summary"`)
- `RelationshipName` — classifies names of relationships (e.g., `"AUTHORED_BY"`)
- `SchemaName` — classifies schema identifiers
- `Label` / `Description` — classify display-oriented metadata
- `MaxCardinality` — classifies numeric constraints on relationships
- `DeletionSemantic` — an enum defining deletion behaviors
- `DeletionSemanticAllow`, `DeletionSemanticBlock`, `DeletionSemanticCascade` — enum variants that constrain `DeletionSemantic` values

These types appear throughout the core MAP schemas and are required for defining valid types, relationships, behaviors, and schema metadata.

---

### 📁 Canonical Source of Core Types

The complete and authoritative list of Core Types is maintained as .json files within the import-files directory in the [map-holons GitHub repository](https://github.com/evomimic/map-holons).


### ✅ Core Types and Their Instances

Most agent-defined _**values**_ in MAP — such as schema names, property identifiers, or semantic flags — are _instances_ of Core Types. For example:

- "title", "short_description", and "published_date" are instances of the Core Type `PropertyName`
- "AUTHORED_BY" and "MEMBER_OF" are instances of `RelationshipName`
- "LibrarySchema" is an instance of `SchemaName`
- "Cascade" is constrained by the enum type `DeletionSemantic`, and corresponds to a specific Core Enum Variant Type: `DeletionSemanticCascade`

MAP enum types are structured as **core type descriptors**, and each of their allowed variants is **also a Core Type**, ensuring that both the category and the set of legal values are modeled explicitly.

This approach makes enum values composable, referenceable, and introspectable — just like any other type.

### ✅ Core Type Hierarchy Example

Core Type: PropertyName  
├── "title"  
├── "short_description"  
├── "published_date"

Core Type: RelationshipName  
├── "AUTHORED_BY"  
├── "MEMBER_OF"

Core Type: SchemaName  
├── "BookSchema"  
├── "LibrarySchema"

In each of these cases, the values shown are **agent-defined instances** of the Core Type. The system uses the Core Type to validate, interpret, and introspect the values, but their actual semantics are defined by agents and communities.

### 📌 Summary

- Core Types define semantic categories used throughout MAP
- They have instances — values used in schemas, properties, and descriptors
- They are required by MAP logic and are never agent-defined
- They provide the backbone for agent extensibility

## Meta Types and Inheritance Type Chains

### 📘 Meta Types and Inheritance Type Chains

The MAP Type System is holonic and self-describing. Every MAP type is a **holon** that can answer two key questions:
- *What kind of thing am I?* → via the `DescribedBy` relationship
- *What structural expectations do I inherit?* → via the `Extends` relationship

#### 🧠 Type Descriptors

A **type descriptor** is a holon that classifies other holons — such as `BookType`, `PropertyType`, or `SchemaType`. All type descriptors are:
- `DescribedBy: TypeDescriptor` (or use `"type": "#TypeDescriptor"` as syntactic sugar)
- Structured by the properties and relationships defined by the type they `Extend`

#### 🧬 Meta Types

**Meta types** are higher-order type descriptors that define the **structural expectations** for entire categories of type descriptors. A type descriptor `Extends` a meta type to inherit the properties and relationships it must declare. For example:

- **`HolonType` extends `MetaHolonType`**  
  → This means `HolonType` must define the properties and relationships that all holon descriptors should declare (e.g., `DescribedBy` and `OwnedBy` relationships).

- **`PropertyType` extends `MetaPropertyType`**  
  → This ensures that property descriptors declare a `ValueType`, a `PropertyName`, and relationships such as `PropertyOf`.

- **`MetaHolonType` extends `MetaTypeDescriptor`**  
  → This brings in the shared expectations for all meta-level descriptors, such as declaring `type_name`, `display_name`, and `type_kind`.

By using `Extends`, each type becomes part of a **compositional inheritance chain** — gaining structure, constraints, and semantic roles appropriate to its category. This enables consistent validation, introspection, and UI behavior across the entire type ecosystem.


#### 🗂️ MAP Meta-Schema Type Graph

This diagram illustrates a portion of the MAP Meta-Schema, focusing on core type descriptors (excluding value types and key rule types).


Each node in the diagram represents a holon and uses **UML-style stereotypes** (e.g., `<<TypeDescriptor>>`) to indicate its type. These stereotypes **implicitly encode the `DescribedBy` relationship** — for example, since `SchemaHolonType` has the stereotype `<<TypeDescriptor>>`, it implicitly has a `DescribedBy` relationship to `TypeDescriptor`. This notation reinforces the fact that every holon is self-describing while reducing visual clutter.

Although not strictly necessary, the `DescribedBy` relationship is explicitly shown for `TypeDescriptor` itself to emphasize that it is self-describing.

The diagram shows how type descriptors are organized holonically and linked through two key relationships:

- **`DescribedBy`**: Declares the categorical type of a holon.
- **`Extends`**: Indicates structural inheritance — i.e., what properties and relationships a type must declare.

The node colors reflect the holon's level in the schema hierarchy:
- **Lavender** = Meta-level descriptors (e.g., `MetaHolonType`)
- **Blue** = Type-level descriptors (e.g., `HolonType`, `PropertyType`, `RelationshipType`)
- **Green** = Instance-level holons (e.g., the `MAP Meta-Schema` holon itself)

Relationships are shown as **solid lines**. Each line represents two uni-directional relationships: the **declared** relationship and its **inverse**. A **black dot** indicates the type that **declares** the relationship. **Open arrowheads** indicate the direction of application — clarifying which role applies to which end of the relationship.

For example, `HolonType` declares the `Extends` relationship to `MetaHolonType`. The inverse relationship, `ExtendedBy`, has `MetaHolonType` as its **source type** and `HolonType` as its **target**.

This graph expresses how the MAP type system is structurally self-describing, introspectable, and compositionally extensible.

The table below summarizes key holons from the diagram and clarifies their roles in the MAP type system. For each holon, it lists its categorical type (`type`), its formal `DescribedBy` relationship (sometimes inferred via shorthand), and the type it `Extends` to inherit structural expectations. This provides a compact reference for understanding how MAP achieves self-description, compositional inheritance, and schema-layer separation.

| Holon Key                      | `type`           | `DescribedBy`         | `Extends`            | Notes                              |
|--------------------------------|------------------|-----------------------|----------------------|------------------------------------|
| `'Future Primal'`              | `BookType`       | `BookType` (inferred) | —                    | Concrete instance                  |
| `BookType`                     | `TypeDescriptor` | `TypeDescriptor`      | `HolonType`          | Describes holons                   |
| `HolonType`                    | `TypeDescriptor` | `TypeDescriptor`      | `MetaHolonType`      | Describes holon types              |
| `MetaHolonType`                | `TypeDescriptor` | `TypeDescriptor`      | `MetaTypeDescriptor` | Describes descriptors of holons    |
| `MetaTypeDescriptor`           | `TypeDescriptor` | `TypeDescriptor`      | `MetaHolonType`      | Describes all type descriptors     |
| `TypeDescriptor`               | `TypeDescriptor` | `TypeDescriptor`      | `MetaHolonType`      | Root, self-describing              |
| `SchemaType`                   | `TypeDescriptor` | `TypeDescriptor`      | `HolonType`          | Describes schema holons            |
| `MetaSchemaType`               | `TypeDescriptor` | `TypeDescriptor`      | `MetaHolonType`      | Describes `SchemaType`             |
| `RelationshipType`             | `TypeDescriptor` | `TypeDescriptor`      | `MetaHolonType`      | Base class for all rel descriptors |
| `MetaDeclaredRelationshipType` | `TypeDescriptor` | `TypeDescriptor`      | `RelationshipType`   | Describes declared relationships   |
| `MetaInverseRelationshipType`  | `TypeDescriptor` | `TypeDescriptor`      | `RelationshipType`   | Describes inverse relationships    |

---

### Meta-Value Types



| Holon Key            | DescribedBy     | Extends       | Notes                                                            |
|----------------------|-----------------|---------------|------------------------------------------------------------------|
| TypeDescriptor       | TypeDescriptor  | MetaHolonType | Root, self-describing                                            |
| MetaValueType        | TypeDescriptor  | MetaHolonType | Abstract base for all value type descriptors                     |
| MetaStringValueType  | TypeDescriptor  | MetaValueType | Describes string-based value types                               |
| MetaIntegerValueType | TypeDescriptor  | MetaValueType | Describes integer-based value types                              |
| MetaBooleanValueType | TypeDescriptor  | MetaValueType | Describes boolean value types                                    |
| MetaEnumValueType    | TypeDescriptor  | MetaValueType | Describes value types selected from enum variants                |
| MetaEnumVariantType  | TypeDescriptor  | MetaHolonType | Describes individual enum variants                               |
| MetaBytesValueType   | TypeDescriptor  | MetaValueType | Describes value types as encoded binary data                     |
| MetaValueArrayType   | TypeDescriptor  | MetaValueType | Describes value types representing arrays of another value type  |
| MAP MetaValue Schema | SchemaHolonType | —             | A concrete schema holon instance containing all meta-value types |



### Keyed vs. Keyless Holon Types

Every holon in MAP is an instance of a **HolonType**, and that HolonType determines whether instances are **keyed** or **keyless**.

- **Keyed Holon Types** require that each instance includes a stable `key`, derived from one or more of its properties using a `UsesKeyRule`. Holons of these types:
    - Must include a `key` field in the JSON import
    - May be referenced elsewhere using `$ref`
    - May be the **target** of declared relationships

- **Keyless Holon Types** do **not** permit their instances to include a key. Holons of these types:
    - Must be **embedded inline** wherever they are used
    - May **not** be referenced via `$ref` (not even by `id:`)
    - May **not** be the **target** of any declared relationship
    - Must act as the **source** of at least one relationship to a keyed holon (to remain anchored in the graph)

This distinction is structural and enforced during staging. The loader will reject any violation of these rules — including attempts to reference or directly target a keyless holon.

> 🔍 Whether a holon is keyed is not an authoring choice — it is defined by the HolonType it instantiates.

### 🔢 Key Derivation Rules

Every keyed holon must declare a `UsesKeyRule`, pointing to a `FormatKeyRule` with:

- `format`: A string template (e.g., `"$0"`, `"($0)-[$1]->($2)"`)
- `property_names`: List of property or inferred names used to fill the format

The authored `key` must match the result of evaluating the format rule.

## 🧱 Foundational Rule for All Types

Every MAP type descriptor (e.g., `BookType`, `PropertyType`, `MetaHolonType`) must:

- ✅ Be **DescribedBy the `MetaHolonType`** — this defines the meta-structure of the type descriptor itself
- ✅ **Extend the foundational `MetaTypeDescriptor`** — inheriting shared fields like `type_name`, `description`, etc.

This rule applies uniformly to all types in MAP, including both core types (like `PropertyType`, `SchemaType`) and meta-types (like `MetaHolonType`, `MetaSchemaType`). It ensures:

- 🔄 Reflexivity — Types are holons too
- 🔍 Introspection — Schema tools can explore and validate all descriptors using a shared structure
- 🧱 Composability — Specialized descriptors build on common foundations

> 🧠 Even `MetaHolonType` itself is DescribedBy the `MetaHolonType` and Extends `MetaTypeDescriptor`.

### 🔐 HolonType Requirements

In addition to the foundational rule above, all **HolonTypes** must:

- ✅ Declare a `UsesKeyRule` — either a formatting rule (e.g., `TypeName.KeyRule`) or `None.KeyRule`

This ensures that the distinction between keyed and keyless types is structurally enforced and discoverable via introspection.


---

# 🔹 Layer 3: Extension Types

_Extension Types_ allow agents to extend the system dynamically — without modifying the core codebase.

They enable agents to:

- Define and evolve their own schemas
- Interoperate across shared Core Types
- Build custom domain semantics atop a compact system foundation

This is what makes the MAP type system open-ended — not constrained by the imagination of its designers.

---

### ✅ What Is an Extension Type?

An **Extension Type** is any holon that:

- Belongs to a known **Core Type** — either a _Meta-Type_ (like `HolonType`, `PropertyType`) or an _Attribute/Enum Type_ (like `PropertyName`, `DeletionSemantic`)
- Classifies other holons, values, or relationships
- Is defined by an agent and stored in a schema

---

### 🧠 Principle: Every Type is Both Classifier and Instance

In MAP, **every type plays a dual role**:

- As a **classifier**, it defines a category of values (e.g., `BookType` classifies books)
- As **data**, it is itself an instance of a Core Type (e.g., `BookType` is an instance of `HolonType`)

This mirrors the holonic design of MAP:
> Just as every holon is both a _whole_ and a _part_,  
> every type is both a _type_ and _data_.

This is what allows types to be queried, versioned, and composed — just like any other holon.

Example:

```
📦 HolonType (Core Type)
└── 📄 BookType (Extension Type)
    └── 📘 'Future Primal' (Instance of BookType)
```

---

### ✅ Examples of Extension Types

- `"title"`, `"subtitle"`, `"summary"` — instances of the Core Type `PropertyName`
- `"HAS_AUTHOR"`, `"MENTORED_BY"` — instances of `RelationshipName`
- `"LibrarySchema"`, `"BookSchema"` — instances of `SchemaName`
- `"EN"`, `"FR"` — enum variants in a user-defined `Language` type (itself an instance of `EnumVariantType`)
- `"BookType"`, `"PersonType"` — instances of `HolonType`, used to classify holons

Each of these types contributes to an agent’s schema — while remaining anchored in a shared, system-defined Core Type.

---

### ✅ Why Extension Types Matter

Extension Types unlock:

- **Decentralized schema modeling** — agents define their own vocabularies
- **Semantic interoperability** — shared Core Types allow cross-agent reuse
- **Ontological creativity** — agents invent new semantic primitives for their domains
- **Scalable extensibility** — MAP doesn’t need to “know in advance” what concepts might be needed

MAP’s type system grows outward from a compact core — forever extensible via agent-defined types.

---

## 🔹 Type Descriptors and TypeKinds

To this point, we have been discussing MAP Types in their role as _classifiers_ — that is, as entities that categorize values and holons.

But because MAP is **self-describing**, every type also plays another role: it serves as a **descriptor** — a structured, introspectable specification of what that type means and how it behaves.

In other words:

> A MAP type is not just a name — it is a holon that carries its own definition.  
> That definition can be validated, linked, versioned, and queried — just like any other holon.

This descriptor role is what enables:

- Schema graphs
- UI introspection
- Runtime validation
- Federated type reuse

And it’s what makes the MAP Type System truly **holonic**, **open-ended**, and **self-aware**.

---

## 🧭 Descriptor Roles: One Concept, Many Uses

A type descriptor plays multiple roles depending on how it is used — and these roles are layered, not mutually exclusive.

Let’s walk through these roles using a concrete example: the `📄 BookType` holon — an instance of `HolonType` that classifies books.

| Role                                    | Description                                                                                               |
|-----------------------------------------|-----------------------------------------------------------------------------------------------------------|
| **In its role as a holon**              | `📄 BookType` is a persistent, versioned data object that can be queried, cloned, or linked               |
| **In its role as a type**               | It classifies other holons (like `"Future Primal"` or `"Think Like a Commoner"`) as being of type Book    |
| **In its role as a schema component**   | It is part of a larger schema graph — linked to descriptors for `title`, `author`, `publisher`, etc.      |
| **In its role as a validator**          | It constrains which properties and relationships book holons must or may have                             |
| **In its role as a visualization hint** | It signals which fields should be rendered, in what order, and possibly how (e.g., rich text, tag picker) |
| **In its role as a system dependency**  | MAP logic might require that a `HolonType` is present in the `DESCRIBED_BY` relationship of a holon       |

---

### 📘 Example: `BookType` in a Schema

> 🧾 **Note on JSON Examples**
>
> All examples in this document are shown using JSON, since it provides a familiar and readable syntax for representing holons, their properties, and their relationships. While MAP’s internal representation of holons is not JSON-specific, JSON is used here to:
>
> - Illustrate the structure of type descriptors in a concise, portable way
> - Mirror the format used by the MAP holon data loader for importing types
> - Help developers understand the schema by example
>
> Some conveniences shown (such as embedded inverse relationships) are supported in the **import format** but are **not populated automatically by the type system** itself. In runtime behavior and storage, relationships are directional, and inverse relationships are always derived, not declared.
>
> These examples should be interpreted as **conceptual illustrations**, not literal runtime structures.

```json
{
  "key": "BookType",
  "type": "#TypeDescriptor",
  "properties": {
    "type_name": "BookType",
    "type_name_plural": "Books",
    "display_name": "Book",
    "display_name_plural": "Books",
    "description": "A book, manuscript, or other published artifact intended for reading or reference.",
    "type_kind": "Holon"
  },
  "relationships": [
    {
      "name": "Extends",
      "target": { "$ref": "#MetaHolonType"}
    },
    {
      "name": "InstanceProperties",
      "target": [
        { "$ref": "#title" },
        { "$ref": "#summary" }
      ]
    },
    {
      "name": "InstanceRelationships",
      "target": [
        { "$ref": "#(BookType)-[HAS_AUTHOR]->(PersonType)" }
      ]
    },
    {
      "name": "DescribedBy",
      "target": {
        "$ref": "#MetaHolonType"
      }
    }
  ]
}
```

In this example:

- `BookType` is a holon that **describes** a class of holons representing books.
- It directly includes its metadata (e.g., `display_name`, `description`) as properties.
- The `InstanceProperties` relationship links to two `PropertyType` holons: `title` and `summary`.
- The `InstanceRelationships` link defines the `HAS_AUTHOR` relationship to `PersonType`.
- Its `DescribedBy` relationship connects it to the holonic descriptor for holon types — `MetaHolonType`.

> 💡 In the current MAP design, a type descriptor like `BookType` is self-contained and complete — it includes both metadata and structure, and can be introspected using the standard type resolution logic of MAP.

---

## 🧱 Type Descriptor Structure

In MAP, every type is represented by a single holon that functions as a complete, self-describing type descriptor.

Each descriptor holon:

- Declares its `type` (e.g., `#HolonType`, `#PropertyType`, `#RelationshipType`)
- Contains metadata in its `properties` block, including:
  - `type_name`
  - `type_name_plural`
  - `display_name`
  - `display_name_plural`
  - `description`
  - `type_kind` (optional, for categorization)
- Declares structural semantics in its `relationships` block, including:
  - `InstanceProperties` → links to property types
  - `InstanceRelationships` → links to relationship types
  - `DescribedBy` → links to the meta-type that classifies the descriptor

This unified structure supports full introspection, validation, and visualization.

| Component        | Description                                                               |
|------------------|---------------------------------------------------------------------------|
| Descriptor holon | A self-contained holon that defines a type                                |
| `properties`     | Metadata and semantic identifiers                                         |
| `relationships`  | Structural semantics and linkage to other descriptors                     |
| `DescribedBy`    | Reference to a `MetaXxxType` holon that defines how to interpret the type |

> 📌 Key Principle: Every type descriptor in MAP is a holon — self-contained, queryable, and structurally connected to other types through named relationships.

---

## 🧭 TypeKind: Semantic Role of TypeDescriptors

In the current MAP design, `TypeKind` is **no longer a structuring mechanism**, but it is **still present** as a **semantic property** on `TypeDescriptor` holons.

> ✅ Every `TypeDescriptor` (e.g., `PropertyType`, `RelationshipType`, `EnumVariantType`, etc.) includes a `type_kind` property  
> to declare what *kind of thing* it defines: a property, a relationship, a value, a collection, etc.

This property is used for **semantic tagging, classification, and filtering** — not for behavior control or logic dispatch.

---

### 🔍 Example: `title` as a `PropertyType`

```json
{
  "key": "title",
  "type": "#PropertyType",
  "properties": {
    "property_name": "title",
    "display_name": "Title",
    "description": "The title of the book.",
    "type_kind": "Property"
  },
  "relationships": [
    {
      "name": "ValueType",
      "target": { "$ref": "#MapStringValueType" }
    }
  ]
}
```

Here:

- `type_kind: "Property"` is a value from the Core Type `TypeKind` (a string enum).
- It helps classify this descriptor for introspection, display, and tooling.
- It **does not** control validation or runtime behavior — that’s handled via the `type` field and relationship graph.

---

### 🧩 Purpose of `type_kind` in Today’s Design

| Usage                             | Role                                                           |
|-----------------------------------|----------------------------------------------------------------|
| **Semantic categorization**       | Enables schema viewers or form generators to group descriptors |
| **Filtering / discovery**         | Helps tooling find all e.g., `HolonType` or `EnumVariantType`  |
| **Documentation / introspection** | Makes it easier for agents to understand a type’s intent       |
| **UI hints**                      | Can inform display decisions (e.g., show as dropdown)          |

---

### ✅ Current `TypeKind` Variants

The `TypeKind` enum includes values like:

```rust
pub enum TypeKind {
  Property,
  Relationship,
  EnumVariant,
  Holon,
  Collection,
  Dance,
  Value(BaseTypeKind),
  ValueArray(BaseTypeKind),
}
```

Each variant represents a **semantic role**, not a behavior contract.

---

### 🚫 What `TypeKind` No Longer Does

| Legacy Role                | Current Status                               |
|----------------------------|----------------------------------------------|
| Drives validator behavior  | ❌ Replaced by declarative relationships      |
| Encodes structural layout  | ❌ Replaced by explicit relationships & types |
| Determines loading logic   | ❌ Removed in favor of holon loader model     |
| Primary dispatch mechanism | ❌ Replaced by `type` + relationship graph    |

---

### ✅ What `TypeKind` Still Provides

- Human-friendly *categorization*
- Optional filtering for UI / dev tools
- Interop hints (e.g., group-by panels)
- **Metadata only**, not logic-driving

> You can think of it as a **classifier**, not a controller.

---

## 🧬 Value Type Descriptors

A **Value Type Descriptor** defines rules for scalar values, such as strings, integers, booleans, or enums. It includes:

- A `base_kind` (e.g., `String`, `Integer`)
- Constraints like `min_length`, `max_value`, `pattern`

```rust
pub enum BaseTypeKind {
    String,
    Integer,
    Boolean,
    Enum,
    Bytes,
}
```

#### Example

A value type descriptor for short titles might include:

- `base_kind: String`
- `min_length: 1`
- `max_length: 100`
- `pattern: ^[A-Za-z0-9 ,.!?]+$`

> In its role as a visualization hint, this descriptor tells the UI to render a text field with validation constraints.

---

## 🧾 Naming Conventions

MAP applies consistent naming conventions across types and descriptors to promote readability, interoperability, and code generation.

These conventions are:

| TypeKind           | Naming Convention               | Example                              |
|--------------------|---------------------------------|--------------------------------------|
| `PropertyType`     | `snake_case`                    | `title`, `summary`, `published_date` |
| `RelationshipType` | `SCREAMING_SNAKE_CASE`          | `HAS_AUTHOR`, `MEMBER_OF`            |
| `HolonType`        | `PascalCase` (a.k.a. ClassCase) | `BookType`, `PersonType`             |
| `EnumVariantType`  | `PascalCase`                    | `Published`, `Draft`, `Archived`     |
| `SchemaType`       | `PascalCase`                    | `LibrarySchema`, `CoreSchema`        |

These conventions are often automatically derived from enum variant names in core code, or enforced at runtime by schema validators.

> 🧭 Consistent naming supports composability across schemas and improves developer tooling, visualization, and API generation.

---

## 🔗 Descriptor Graph

Schemas in MAP are built from a graph of descriptors connected via named relationships.

Key relationships include:

- `HAS_ASPECT` → links descriptor to metadata and configuration
- `VALUE_TYPE_FOR` → used by `PropertyType` to define scalar validation
- `PROPERTY_OF`, `SOURCE_FOR`, `TARGET_FOR` → define placement within holons
- `COMPONENT_OF`, `OFFERS`, `APPLIES_TO` → used for collections and behaviors

Together, these graphs define the structure, semantics, and rules of any domain modeled in MAP.

> 📘 Every schema is a living, versioned graph of type descriptors — and every type is a holon within that graph.

## 🔧 Extends / ExtendedBy Relationship Pattern

### 📌 Intent
To define a semantic relationship between two holon types where one **inherits**, **specializes**, or **refines** another — enabling shared structure, type introspection, and logical substitution in schema validation and reasoning.

This pattern provides a way to:
- Express hierarchical relationships between type descriptors
- Support polymorphism in schema definitions
- Enable extension of abstract base types in a self-describing, data-driven way

---

### 💡 Motivation
In MAP, holons are not just data — they are types, descriptors, and structured agents of meaning. In many cases, a given type:
- Generalizes a conceptual category (e.g., `KeyRuleType`, `HolonType`)
- Needs to be **extended** by more specific, concrete types (e.g., `Format.KeyRuleType`, `BookType`)
- Must support introspection or polymorphic behavior in schema tools, UI generators, or validators

The `Extends` relationship encodes this conceptual inheritance explicitly in the type graph.

Additionally, this pattern enables **shared relationship endpoints** — abstract types like `KeyRuleType` or `HolonType` can be used as a **common source or target** in structural relationships (e.g., `UsesKeyRule: KeyRuleType`), improving schema modularity, reusability, and expressiveness.

---

### 🧭 Directionality and Roles in `Extends`

The `Extends` relationship in MAP always points:

> **From the more specific holon type (subtype) → to the more general holon type (supertype)**

This expresses that the subtype **declares** that it is a refinement, specialization, or extension of the supertype. The supertype does not reference or depend on the subtype.

#### ✅ Standard Naming Convention

| Role          | Meaning                                               |
|---------------|-------------------------------------------------------|
| **Subtype**   | The more specific, extending type (e.g., `BookType`)  |
| **Supertype** | The more abstract or general type (e.g., `HolonType`) |

You can remember this as:

```
Subtype Extends Supertype
```

#### 🧩 Declaration Semantics

- The **`Extends` relationship is always declared on the subtype**.
- The supertype remains **agnostic** about which types extend it.
- This preserves modularity and ensures that **abstract types don’t depend on their extensions**.

In contrast:
- `ExtendedBy` is the **inverse** relationship — it is inferred or traversed, not declared.

---

### 🧱 Compositional Inheritance in MAP

MAP deliberately adopts a **compositional** approach to inheritance, avoiding classical OOP-style structural inheritance. Rather than copying or overriding fields:

- `Extends` encodes **semantic ancestry**, not structural merging.
- Subtypes are **free to define their own structure** but can be reasoned about as members of the base type category.
- Relationships and validation logic **apply upward** via ancestry traversal.

This allows abstract types to:
- Serve as **type-class categories**
- Be referenced in relationships without duplication
- Enable validator or UI behavior to be grouped by common ancestry

---

### 🔁 Comparison to Other Inheritance Models

| Inheritance Model                 | Description                                                | Tradeoffs                                                        |
|-----------------------------------|------------------------------------------------------------|------------------------------------------------------------------|
| **Classical Inheritance**         | Subclass copies or overrides fields from parent            | Tight coupling, fragile hierarchies, field conflicts             |
| **Mixin Inheritance**             | Traits or behaviors added through injection or composition | Ambiguous resolution order, hard to visualize                    |
| **MAP Compositional Inheritance** | Types **declare semantic ancestry** via `Extends` only     | Loose coupling, self-describing, supports polymorphism cleanly ✅ |

---

### ✅ Applicability
Use this pattern when:
- You want to define a **base type** that should not be instantiated but provides shared meaning or structure
- You want to define **concrete subtypes** that inherit from or specialize a base type
- You want polymorphic behavior in relationships like `DescribedBy`, `UsesKeyRule`, `SourceType`, `TargetType`
- You want to enable schema processors to reason generically over a category (e.g., “any HolonType”)
- You want to compose domain models using clear, queryable inheritance

---

### 🏗 Structure

This pattern involves a directional relationship from subtype to supertype:

```json
{
  "key": "BookType",
  "type": "#TypeDescriptor",
  "properties": {
    "type_name": "BookType"
    // other properties omitted
  },
  "relationships": [
    {
      "name": "Extends",
      "target": { "$ref": "#HolonType" }
    }
  ]
}
```

This means:
- `BookType` declares that it is a subtype of `HolonType`
- `HolonType` does not list or depend on its subtypes
- Tools can still query `HolonType → ExtendedBy → BookType` using inverse relationship resolution

---

### 🧠 Why This Matters

- Promotes **separation of concerns**: abstract types remain clean and reusable
- Enables **open-ended extension**: new subtypes can be added without modifying supertypes
- Supports **schema introspection**: subtype declarations drive validation and inheritance

## 🧠 MAP’s Self-Describing Holons

One of the foundational strengths of the MAP architecture is that **every holon is self-describing**. This means you can encounter a holon “in the wild” — retrieved from a peer, cached in a local space, embedded in a file — and still understand what it is, what it can do, and how to interact with it.

When interrogated, a holon can answer the following questions through introspection:

---

### ❓ The Four Questions You Can Ask Any Holon

1. **What type of holon are you?**  
   → Identify its structural definition and semantic category.

2. **What properties do you have?**  
   → Reveal the named fields you can inspect or populate.

3. **What relationships do you participate in?**  
   → Show how this holon links to others and under what semantics.

4. **What dances can we do together?** *(planned enhancement)*  
   → Surface interactive protocols (e.g., offers, negotiations, workflows) it supports.

---

### 🧪 How MAP Answers These Questions

MAP’s type system enables precise, runtime discoverability using the following process:

1. **Get the Type**  
   Query the holon’s `DescribedBy` relationship to obtain its `TypeDescriptor`.  
   The `type_name` of that descriptor is the holon’s `type`.

2. **Get the Properties**  
   Ask the `TypeDescriptor` for its `InstanceProperties`, which reference `PropertyType` holons.  
   Then, use the `property_name` of each to look up corresponding fields in the holon’s `properties` object.

3. **Get the Relationships**  
   Ask the `TypeDescriptor` for both `InstanceRelationships` and `InverseInstanceRelationships`,  
   which point to `DeclaredRelationshipType` holons. These define the relationships this holon may source or target.

4. **Get the Dances (Future)**  
   Once supported, the `TypeDescriptor` will reference `DanceDescriptors` that describe structured interactions  
   the holon offers — think of these as holon-level capabilities or APIs.

---

### 🧬 The Role of `Extends`: Compositional Inheritance

A holon’s `TypeDescriptor` may declare an `Extends` relationship to another type descriptor.  
This forms an **inheritance chain**, but unlike class-based languages, this is **semantic and structural**, not implicit or automatic.

To fully understand a holon, MAP must:

- **Traverse the full transitive closure of `Extends`** on its `TypeDescriptor`
- **Aggregate all inherited structure**, including:
  - `InstanceProperties`
  - `InstanceRelationships`
  - `InverseInstanceRelationships`
  - (Future) `DanceDescriptors`

This means:

> The complete interface of a holon — its properties, relationships, and dances — is defined not just by its direct type,  
> but by the **entire lineage of types it extends**.

---

### 🔄 Summary of the Self-Describing Flow

| Question                           | Resolution Path                                                          |
|------------------------------------|--------------------------------------------------------------------------|
| What type are you?                 | `DescribedBy → TypeDescriptor`                                           |
| What properties do you have?       | `TypeDescriptor → InstanceProperties → property_name → holon.properties` |
| What relationships do you support? | `TypeDescriptor → InstanceRelationships + InverseInstanceRelationships`  |
| What dances can we do? (future)    | `TypeDescriptor → DanceDescriptors`                                      |
| What else do you inherit?          | Traverse `Extends` to collect more of the above                          |

---

This compositional model ensures that every holon in MAP carries with it enough semantic metadata to be understood, interacted with, and reasoned about — no matter where it comes from or what created it.