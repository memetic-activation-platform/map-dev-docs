# MAP Holon Data Loader: JSON Import Format – Comprehensive Authoring Guide

This guide provides developers with a complete and authoritative reference for constructing valid JSON import files for the MAP Holon Data Loader. It reflects current conventions for authoring schema definitions, base/core types, and domain-specific instances in a self-describing, holonic data model.

---

## ✨ Overview

The MAP Holon Data Loader allows for the declarative import of holons and their relationships into a (single) MAP Holon Space. The import format is intentionally minimal, self-describing, and designed for bootstrapping both type descriptors and real data without relying on runtime logic.

All holons — including types, schemas, and instances — are defined uniformly. Their type, structure, and descriptors are all expressible using the same format.

---

# 📚 Foundational Concepts

MAP import files are composed of **holons** — self-contained objects representing types, data, or components. This section introduces key concepts that underpin the entire format.

## Holons and Types

Every holon has a `type` that points to a type descriptor (e.g., `BookType`, `PropertyType`). The type is used to determine:

- What properties are allowed
- What relationships can be included
- How validation is applied

The `type` field acts as both a signal and a shortcut. It removes the need to include an explicit `DescribedBy` relationship.

## Keyed vs. Keyless Holon Types

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

## 📚 Best Practices

- ✅ Include `UsesKeyRule` for every HolonType descriptor
- ✅ Use consistent naming across `type_name`, `display_name`, and `key`
- ✅ Use inline embedding for keyless holons or unique instances
- ✅ Use `$ref` for reusable, keyed holons
- ❌ Do not author `DescribedBy` or `OwnedBy` — these are handled automatically

---

## Referencing Other Holons: `$ref` and Inline Embedding

In MAP’s JSON import format, holons frequently refer to other holons — whether to define relationships, specify constraints, compose schemas, or extend descriptors. These references can be expressed in one of two interchangeable forms:

1. **`$ref` strings** — Concise pointers to other keyed holons
2. **Inline embedded holons** — Full holon objects defined in place

Both forms are valid anywhere a holon is expected, and the Holon Data Loader treats them equivalently when staging, validating, and committing.

---

### 🧠 Motivation: Reference Scenarios MAP Must Support

| Scenario                     | Example                                                                 |
|-----------------------------|-------------------------------------------------------------------------|
| **Staged vs. Saved**        | Refer to holons defined in the same file or already saved in the space  |
| **Local vs. External**      | Link to holons from another HolonSpace (e.g., shared schemas)           |
| **Keyed vs. Keyless**       | `$ref` keyed holons; embed keyless ones                                |
| **Reusable vs. One-Off**    | Reuse types and entities via `$ref`; define constraints inline          |

---

### 🧭 `$ref` Semantics

`$ref` is a string-based shorthand for referencing previously defined, saved, or external **keyed** holons. It can be used anywhere a holon is expected and the type can be inferred from context.

##### Supported `$ref` Formats

| `$ref` Format        | Meaning                                      | Example              |
|----------------------|----------------------------------------------|----------------------|
| `"#key"`             | Reference to a keyed holon by key only       | `"#future-primal"`   |
| `"id:<HolonId>"`     | Reference by ActionHash (HolonId)            | `"id:uhCAkYmv..."`   |
| `"@Proxy:key"`       | External holon via proxy name + key          | `"@Library:Books"`   |
| `"ext:<Proxy>:<Id>"` | External holon via proxy ID + local ID       | `"ext:uhProxy:uhId"` |

> 🔍 **The holon’s type is inferred from context.**  
> If the key does not match a holon of the expected type, validation will fail.

---

### 📦 Inline Embedded Holons

Use inline embedding to define a holon directly in context. This is required for:

- **Keyless holons**
- **One-off structures**, like constraints or descriptors
- Situations where local scoping improves clarity

> Caveat: Each inline Holon is importing a new Holon, be careful to avoid unwanted duplication


---

### ✅ Reference Examples

TBD

---

### 🚫 Invalid Reference Cases

- ❌ `$ref` to a keyless holon (must be embedded)
- ❌ `id:` reference to a keyless holon — even though syntactically allowed, **keyless holons must never be the target of a declared relationship**
- ❌ References outside expected type context
- ❌ Mixing `$ref` and `type` in a single object

---

### ✅ Summary

| Reference Form | Best For                            | Requires Key | Reusable? |
|----------------|-------------------------------------|--------------|-----------|
| `$ref`         | Reuse of shared or saved holons     | ✅ Yes       | ✅ Yes    |
| Inline         | One-off or keyless components       | ❌ No        | ❌ No     |

---

# 📁 File Structure

Each JSON import file consists of two top-level keys:

```json
{
  "meta": { ... },
  "holons": [ ... ]
}
```

- `meta`: Metadata describing the file
- `holons`: List of holon definitions to be imported

Each entry in the `holons` array is a self-contained JSON object representing a single holon.

---

## 🔹 Holon Definition

Each holon is a JSON object with four primary fields:

- `type`: The descriptor for this holon (replaces `DescribedBy`)
- `key`: Required only for keyed holons
- `properties`: A map of named scalar property values
- `relationships`: A list of outbound relationships to other holons

See the **Foundational Concepts** section above for background on types, keys, references, and embedding.

---

## 🧩 `type`

The `type` field identifies the HolonType (or other descriptor type) that describes this holon. It replaces the need to author a `DescribedBy` relationship.

- Format: a `#Key` reference to a known type descriptor
- Required for all holons

Example:

```json
"type": "#BookType"
```

This implies:
- The holon is described by a `BookType`
- All properties and relationships must conform to the rules defined by that type

---

## 🧩 `key`

The `key` is a unique identifier for **keyed** holons. It is:

- Required for holons of **keyed Holon Types**
- Not allowed for holons of **keyless Holon Types**
- Used as the reference target for `$ref` within the same or other import files

Keys are derived based on the holon’s **HolonType**, which includes a `UsesKeyRule` relationship pointing to a `FormatKeyRule`. This rule specifies how to construct the key from the holon’s property values — and sometimes values on **related holons**.

> 🔄 Because the key can be deterministically derived from the holon’s structure, including it is **technically redundant**. However, the `key` field is explicitly included in the JSON import for:
> - Improved readability
> - `$ref` compatibility
> - Validation of key correctness at staging time

### ⚠️ Important

If any property value involved in key derivation changes, the `key` field and any `$ref`'s to it **must also be updated** to match the new derived value. The loader will recompute the key using the declared `FormatKeyRule` and compare it to the authored key — raising a validation error if they do not match.

---

### 🔢 Key Derivation Rules

Every keyed holon must declare a `UsesKeyRule` relationship pointing to a `FormatKeyRule` — a holon that defines how the key should be constructed.

#### FormatKeyRule Structure

A `FormatKeyRule` has two fields:

- `format`: A string template (e.g., `"$0"`, `"($0)-[$1]->($2)"`)
- `property_names`: An ordered list of names (strings) that supply the values for the placeholders

Example:

```json
{
  "type": "#FormatKeyRule",
  "properties": {
    "format": "$0",
    "property_names": ["type_name"]
  }
}
```

#### ✅ Common Patterns

**Single-property key** (e.g., `MapStringValueType`):
```json
{
  "format": "$0",
  "property_names": ["type_name"]
}
```

**Relationship Type Keys ** (inspired by OpenCypher notation):
```json
{
  "format": "($0)-[$1]->($2)",
  "property_names": ["source_type", "type_name", "target_type"]
}
```

#### ✍️ Declaring UsesKeyRule

Inline:

```json
{
  "name": "UsesKeyRule",
  "target": {
    "type": "#FormatKeyRule",
    "properties": {
      "format": "$0",
      "property_names": ["type_name"]
    }
  }
}
```

By reference:

```json
{
  "name": "UsesKeyRule",
  "target": { "$ref": "FormatKeyRule:BookType.KeyRule" }
}
```

The loader validates all authored `key` values by recomputing them using the declared key rule and comparing the result.

---

## 🧩 `properties`

The `properties` field contains a map of property name to **scalar value**, like so:

```json
"properties": {
  "type_name": "BookType",
  "enabled": true,
  "max_length": 255
}
```

Each value must be one of the supported MAP scalar types:
- `string` (e.g., `"BookType"`)
- `number` (e.g., `42`, `3.14`)
- `boolean` (e.g., `true`, `false`)
- or an array of scalars (for multi-valued properties)

Property types are enforced by the `PropertyType` descriptor referenced in the holon’s `type`. The loader will convert each value into its appropriate `BaseValue` variant based on the declared value type — not based on any in-band `"type"` or `"value"` tags.

> 🔒 Property values must be scalars. You **cannot** use structured objects (like `{ "type": ..., "value": ... }`) inside the `properties` field. Those are only valid in embedded holons or type definitions.

---

## 🧩 `relationships`

In MAP, **every relationship pair** is modeled as two named, uni-directional relationships:

- A **declared relationship** (e.g., `(Person)-[HasAddress]->(Address)`)
- Its corresponding **inverse relationship** (e.g., `(Address)-[AddressOf]->(Person)`)

Strictly speaking, only **declared relationships** are allowed to be **directly populated in the system’s internal storage model**. Inverse relationships are **automatically derived** based on this. However, the **JSON import format allows you to populate either direction** for convenience.

If a JSON import populates an **inverse relationship**, the _Holon Data Loader_ will:

1. Look up its `InverseOf` link to find the declared relationship type.
2. Internally redirect the population to that declared relationship.
3. Leave the inverse direction empty (it will be auto-derived later).

This supports a more natural and readable JSON layout in many scenarios.

---

### ⚠️ Authoring Guidelines

- ✅ **Only populate one direction** of a relationship pair.  
  Do **not** populate both `HasAddress` and `AddressOf`.

- ⚠️ If the relationship involves a **keyless holon type**:
  - The **declared relationship** must be defined on the **keyed holon type**.
  - You must **embed the keyless holon inline**, using the **inverse direction**.

---

### ✅ Example: Embedding a Keyless Holon

Let’s say `PersonType` declares the relationship `HasAddress → AddressType`, and `AddressType` is keyless. We want to attach an address to a person:

```json
{
  "type": "#PersonType",
  "key": "charles-eisenstein",
  "properties": {
    "name": "Charles Eisenstein"
  },
  "relationships": [
    {
      "name": "AddressOf",  // inverse of declared "HasAddress"
      "target": {
        "type": "#AddressType",  // keyless, so must be embedded
        "properties": {
          "city": "Keene",
          "state": "New Hampshire"
        }
      }
    }
  ]
}
```

### 🧠 Explanation

- `AddressType` is keyless → it **must not** be the target of a declared relationship.
- `PersonType` declares `HasAddress → AddressType`
- JSON authors embed the keyless `Address` and populate its **inverse relationship**, `AddressOf → Person`
- The loader internally flips it and populates `HasAddress(charles-eisenstein → [Address])`

### 🔁 Declared vs. Inverse Relationships

When importing **instance holons**, each outbound `relationship` must ultimately correspond to a **declared relationship** — that is, a relationship defined as outbound from the holon’s type.

However, the MAP import format allows you to use **either direction of a relationship pair** when authoring instance data:

- A **declared relationship**, such as:
  ```
  (Book)-[AUTHORED_BY]->(Person)
  ```
- Its corresponding **inverse relationship**, such as:
  ```
  (Person)-[AuthorOf]->(Book)
  ```

These two together form a **relationship pair**, where one is marked as the `InverseOf` the other in its relationship type definition.

> 🔄 Even though only declared relationships are persisted, the loader will **redirect inverse relationship usage to the appropriate declared relationship** and populate it accordingly.

---

### ✅ Authoring Either Direction

In your JSON import file, you may use either side:

```json
{
  "name": "AUTHORED_BY",
  "target": { "$ref": "person-789" }
}
```

or:

```json
{
  "name": "AuthorOf",
  "target": { "$ref": "book-123" }
}
```

Either form will result in the declared `AUTHORED_BY` relationship being populated.

---

### ⚠️ Authoring Guidelines

- ✅ **Only populate one direction** of a relationship pair.  
  Do **not** populate both `AUTHORED_BY` and `AuthorOf` — choose one or the other.

- ⚠️ If one end of the relationship is a **keyless holon** (e.g., an inline annotation or constraint):
  - The **keyless holon’s type must declare** the relationship.
  - You must populate the **inverse direction** using an **embedded target**, not a `$ref`.

---

> 🧠 Internally, only **declared relationships** are directly populated. The system automatically backfills the corresponding **inverse relationships**.

A separate section provides guidance on **defining declared and inverse relationship types**, and how the `InverseOf` and `Inverse` links connect them.

In MAP, **every relationship pair** is modeled as two named, uni-directional relationships:

- A **declared relationship** (e.g., `(Book)-[AuthoredBy]->(Person)`)
- Its corresponding **inverse relationship** (e.g., `(Person)-[AuthorOf]->(Book)`)

Strictly speaking, only **declared relationships** are allowed to be **directly populated in the system’s internal storage model**. Inverse relationships are **automatically derived** based on this. However, the **JSON import format allows you to populate either direction** for convenience.

If a JSON import populates an **inverse relationship**, the _Holon Data Loader_ will:

1. Look up its `InverseOf` link to find the declared relationship type.
2. Internally redirect the population to that declared relationship.
3. Leave the inverse direction empty (it will be auto-derived later).

This supports a more natural and readable JSON layout in many scenarios.

#### ✅ Example: Using Inverse in JSON

You may populate the `Extends` relationship directly:

```json
{
  "name": "Extends",
  "target": { "$ref": "MetaTypeDescriptor" }
}
```

Or, equivalently, populate the inverse `ExtendedBy`:

```json
{
  "name": "ExtendedBy",
  "target": {
    "type": "#MetaHolonType",
    "properties": {
      "type_name": "MetaHolonType"
    }
  }
}
```

Both will result in the same internal relationship being established — on the declared `Extends` direction.

---

### ⚠️ Authoring Rules and Caveats

To ensure consistency and correctness, observe the following:

- ✅ **Only one direction** of a relationship pair should be populated in your JSON file.
- ✅ If you choose to use the **inverse relationship** in your JSON, ensure the inverse type includes an `InverseOf` link to its declared counterpart.
- ⚠️ If **either** source or target holon type in the relationship is **keyless**:
  - That keyless type **must declare** the relationship (i.e., be the source of the declared direction).
  - The **inverse direction must be populated inline**, via embedded holons — since keyless holons cannot be referenced.

---

### 🔄 Relationship Pairing: `InverseOf` and `Inverse`

Each inverse relationship must include an `InverseOf` link to its declared counterpart:

```json
{
  "name": "InverseOf",
  "target": { "$ref": "#(RelationshipType)-[Extends]->(RelationshipType)" }
}
```

Once this is present, the system automatically adds the reverse link using `Inverse`:

```json
{
  "name": "Inverse",
  "target": { "$ref": "#(RelationshipType)-[ExtendedBy]->(RelationshipType)" }
}
```

You do **not** need to author `Inverse` links directly.

==== OLDER STUFF

The `relationships` field is a list of outbound links from the holon to other holons.

Each entry must contain:
- `name`: the name of the relationship
- `target`: a single holon, a `$ref`, or an array of either

You may use either of the following forms:

```json
{
  "name": "UsesKeyRule",
  "target": { "$ref": "FormatKeyRule:Book.KeyRule" }
}
```

or

```json
{
  "name": "Components",
  "target": [
    { "$ref": "BookType" },
    { "$ref": "PersonType" }
  ]
}
```

> ✅ The loader automatically normalizes all `target` values to arrays.  
> Even single references are treated as 1-element arrays internally.

> ⚠️ Cardinality constraints are enforced using the type descriptor associated with the relationship name. For example, relationships like `DescribedBy` or `ComponentOf` often have `max_cardinality = 1`.

# 📂 Embedded Schema Structure

Schemas may embed their components directly via inverse relationships:

```json
{
  "type": "#MapSchemaType",
  "key": "MAP Core Schema",
  "relationships": [
    {
      "name": "Components",
      "target": [ { holon }, { holon } ]
    }
  ]
}
```

These will be rewritten by the loader into `ComponentOf` declarations from each child.

## Defining the Relationships for a Type:

### 🔄 Declaring vs. Instantiating Relationships

In the MAP import format, it is essential to distinguish between two conceptually distinct usages of relationships:

#### 1. Declaring Allowed Relationships for a Type

When defining a **type descriptor**, we use the `InstanceRelationships` relationship to declare what kinds of relationships instances of this type **may** include. The targets of `InstanceRelationships` must be **relationship types**.

Example:

```json
{
  "name": "InstanceRelationships",
  "target": [
    { "$ref": "#(TypeDescriptor)-[ComponentOf]->(Schema)" }
  ]
}
```

This states that instances of this type (e.g., `TypeDescriptor`) may include a `ComponentOf` relationship, and identifies the structural pattern expected for that relationship. The details of that relationship type (cardinality constraints, whether it is definitional, etc.) are defined in the referenced RelationshipType descriptor.

#### 2. Instantiating a Specific Relationship for a Holon

When authoring a specific **holon**, such as a type descriptor or instance, the `relationships` field is used to instantiate actual relationship **instances**. These entries must include:

- A `name`: the name of the relationship
- A `target`: the holon being linked to (typically via `$ref`)

✅ **Correct:**

```json
{
  "name": "UsesKeyRule",
  "target": { "$ref": "#TypeName.KeyRule" }
}
```

❌ **Incorrect:**

```json
{
  "name": "UsesKeyRule",
  "target": {
    "type": "#Format.KeyRuleType",
    "key": "TypeName.KeyRule",
    ...
  }
}
```

The incorrect version attempts to define the target inline — which may duplicate shared definitions and blur the separation of concerns between **relationship declarations** and **relationship instances**.

---

### 🧭 Key Takeaway

> When declaring which relationships a type supports, point to **relationship types**.  
> When instantiating a relationship in a holon, point to a **target holon** — typically via `$ref`.

Following this rule ensures structural clarity, enables reuse, and keeps the MAP type system modular and DRY.

---

## 🔢 Key Derivation Rules

Every keyed holon must declare a `UsesKeyRule`, pointing to a `FormatKeyRule` with:

- `format`: A string template (e.g., `"$0"`, `"($0)-[$1]->($2)"`)
- `property_names`: List of property or inferred names used to fill the format

The authored `key` must match the result of evaluating the format rule.

---

## 📚 Best Practices

- ✅ Include `UsesKeyRule` for every keyed type descriptor
- ✅ Use consistent naming across `type_name`, `display_name`, and `key`
- ✅ Use inline embedding for keyless holons or unique instances
- ✅ Use `$ref` for reusable, keyed holons
- ❌ Do not author `DescribedBy` or `OwnedBy` — these are handled automatically

---

## 🔎 Validation

| Rule ID                     | Title                                      | Description                                                                                                                                                                                                                                                                                                                                                                                                | Severity |
|-----------------------------|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| json-schema                 | Syntactic validation via JSON Schema       | The file must conform to the MAP JSON import format schema.                                                                                                                                                                                                                                                                                                                                                | error    |
| foundational-rule           | Foundational Rule for All Type Descriptors | Every Type Descriptor must be DescribedBy the MetaHolonType and Extend the MetaTypeDescriptor.                                                                                                                                                                                                                                                                                                             | error    |
| unresolved-refs             | Unresolved References                      | All $ref values must resolve to a keyed holon defined in the same or explicitly provided files.                                                                                                                                                                                                                                                                                                            | error    |
| only-declared-properties    | Only Declared Properties May Be Populated  | Holons must not specify properties not listed in InstanceProperties of their type.                                                                                                                                                                                                                                                                                                                         | error    |
| only-declared-relationships | Only Valid Relationships May Be Authored   | The import file may only author relationships that are either: (1) explicitly listed in the holon’s type descriptor via InstanceRelationships, or (2) valid inverse relationships, which are resolved via InverseRelationshipType definitions that point back to a DeclaredRelationshipType where the holon’s type is the TargetType. The system applies updates through the canonical declared direction. | error                       |



Files should be validated against:

1. `bootstrap-import.schema.json` — ensures structural correctness
2. Schema-specific definitions — derived from the loaded Meta-Schema or Core Schema

Holons are further validated at runtime by MAP’s shared validators.

---

## 🎉 Ready to Import

Once authored and validated, the file can be submitted to the Holon Data Loader.

- All `key` and `$ref` references will be resolved
- Relationships will be rewritten as needed
- Keyless holons will be embedded
- All imported holons will be linked to the HolonSpace via `OwnedBy`

For support, contact the MAP stewarding team or refer to the developer documentation.