## 🧬 Starting Point: Types as Holons

In MAP, every type description is, itself, a **holon**.

This means that every type must:
- Be **described by** a `TypeDescriptor`
- Be **owned by** a `HolonSpace`

These aren't optional conventions — they are **defining structural obligations** of being a holon.

> ✅ Every type in MAP is a holon.  
> Therefore: every type must have `DescribedBy` and `OwnedBy` relationships.

---

# Modeling MAP Value Types



## 🔠 Example: MapStringValueType and PropertyNameValueType

Consider two value types:

- `MapStringValueType`: A general-purpose string type
- `PropertyNameValueType`: A string type used specifically for property names

They both represent **strings** at the data level, but differ in usage and constraint.

Both are:

- **Holons** → Must be `DescribedBy` and `OwnedBy`
- **TypeDescriptors** → Must be instances of `MetaValueType`

So the following relationships apply:

```
MapStringValueType —[DescribedBy]→ MetaValueType  
PropertyNameValueType —[DescribedBy]→ MetaValueType
```

At this point, we know these two holons are not just any holons — they are **type descriptors** used in the schema.

---

## 🧱 Shared Constraints via Compositional Inheritance

Different value types require different constraints:

- Strings → min/max length, format, case convention
- Integers → min/max values
- Enums → allowed variants
- Bytes → fixed length, encoding

But many types share these constraints. For example:

```
MapStringValueType        ─┐
                          ├─[Extends]→ StringValueConstraints
PropertyNameValueType     ─┘
```

In this pattern:

- `MapStringValueType` and `PropertyNameValueType` are both holons and descriptors.
- `StringValueConstraints` is just a **constraint facet** — it contributes properties like `min_length`, `max_length`, or `case_convention`.

Importantly:

> `StringValueConstraints` is **not** a type. It’s not a descriptor.  
> It doesn’t have a `type_name`, doesn’t need to be `DescribedBy`, and doesn’t appear in any schema.

It just **extends** the value type it’s associated with, in a purely compositional way.

---

## 🧷 Why Keys Matter

Semantic keys are foundational to the MAP architecture — not just for expressing relationships during import, but for enabling **retrieval, referencing, and bootstrapping** in a decentralized, descriptor-driven system.

They enable holons to be meaningfully identified and linked across the full lifecycle — from initial import to runtime introspection — even before they've been committed to the system or assigned a permanent ID.

---

### 🔄 Staged Relationships Without IDs

In staged or import workflows, holons frequently reference other holons that haven’t yet been committed — and therefore lack a system-assigned ID (e.g., a Holochain `ActionHash`).

Keys solve this by allowing holons to be referenced using `$ref: "key"` rather than relying on fragile temporary identifiers or rigid load ordering.

✅ Keys enable:
- Cross-file linkage between staged holons
- ID-free `$ref` expressions in JSON
- Relationship validation prior to commit
- Deduplication and merging of equivalent entries

📘 Example:
```json
{
  "type_name": "RelationshipType",
  "key": "(PersonType)-[MentoredBy]->(PersonType)",
  "relationships": [
    { "name": "SOURCE_FOR", "target": [{ "$ref": "PersonType" }] },
    { "name": "TARGET_FOR", "target": [{ "$ref": "PersonType" }] }
  ]
}
```

This relationship type can be referenced by other holons using its `key`, without requiring an ID to exist yet.

---

### 🧱 Bootstrapping Descriptors Before Descriptor Logic Exists

Many MAP behaviors — including validation, inverse relationship population, and declarative key generation — depend on descriptors like `PropertyType`, `RelationshipType`, or `HolonType`.

> But you can’t run logic that depends on descriptors until descriptors are present.

By requiring materialized `key` fields in the JSON of Keyed Holons, we can:
- Import descriptors without requiring key generation logic
- Reference them from other holons in the same import graph
- Stage and introspect schemas and data prior to persistence

This makes it possible to:
- Import the MAP Meta-Schema
- Import domain-specific schema extensions
- Import valid data instances
  ...all in a single, unified process.

---

### 🔍 Associative Retrieval in Distributed Systems

In distributed architectures like Holochain, data is stored in **Distributed Hash Tables (DHTs)** — meaning:

- You cannot “query the whole database” as you would in a centralized store
- You typically need a **known hash or path** to locate content efficiently

Materialized **keys** provide the critical link between **semantic meaning** and **retrieval paths**:

✅ They support:
- **Associative lookup**: finding content based on associated properties (e.g., type, relationship role)
- **Path-based indexing**: storing holons under DHT paths that reflect their keys (e.g., `path!(("HolonType", key))`)
- **Declarative retrieval APIs**: enabling callers to say “get me the [MentoredBy] relationship” without knowing its ID

Without keys:
- Content is only retrievable via opaque identifiers
- Queries become tightly coupled to global indexes or full scans (inefficient or unavailable in DHTs)
- Schema introspection and semantic queries are significantly harder

---

### 🧠 Summary

Keys are not just syntactic sugar — they are critical infrastructure for:

- Declarative, schema-linked imports
- ID-free reference resolution across files
- Bootstrapping descriptors before runtime logic is available
- Efficient, semantic-based retrieval in distributed systems
- Federated schema evolution and shared introspection

By embracing materialized, semantically meaningful keys, MAP achieves a powerful combination of:

- Structural clarity
- Introspectable relationships
- Decentralized operability
- Self-hosted schema evolution

This makes keys one of the most essential capabilities in the MAP Type System.

---

## 📐 Layered Inheritance: The Value Type Stack

```
MetaValueType —[Describes]→ MapStringValueType —[Extends]→ StringValueConstraints
```

This gives us three clear layers:

1. **Meta Descriptor Level** — defines what a value type must contain
2. **Descriptor Level** — a value type like `MapStringValueType` or `PropertyNameValueType`
3. **Constraint Layer** — reusable modular constraints via `Extends`

| Layer         | Holon                     | Purpose                          |
|---------------|---------------------------|----------------------------------|
| Meta          | `MetaValueType`           | Describes value type descriptors |
| Type          | `MapStringValueType`      | Actual TypeDescriptor            |
| Constraint    | `StringValueConstraints`  | Adds constraint properties       |

---

## 🔁 Pattern Repeats for All Primitive Types

Here’s the same pattern across other type kinds:

| ValueType               | DescribedBy     | ExtendedBy                | Constraints Provided                |
|-------------------------|-----------------|---------------------------|-------------------------------------|
| `MapStringValueType`    | `MetaValueType` | `StringValueConstraints`  | `min_length`, `max_length`, etc.    |
| `PropertyNameValueType` | `MetaValueType` | `StringValueConstraints`  | Custom limits, `case_convention`    |
| `MapIntegerValueType`   | `MetaValueType` | `IntegerValueConstraints` | `min_value`, `max_value`            |
| `MapBytesValueType`     | `MetaValueType` | `BytesValueConstraints`   | `length`, `encoding`, `format_hint` |
| `MapEnumValueType`      | `MetaValueType` | `EnumValueConstraints`    | `Variants` relationship             |
| `MapBooleanValueType`   | `MetaValueType` | *(none needed)*           | *(no constraints required)*         |

---

## 🧩 Are Meta Types Holons Too?

Yes — and this is where the architectural recursion becomes elegant.

Just as `MapStringValueType` is a holon and needs to be `DescribedBy`, so too does `MetaValueType`.

Let’s follow the thread:

```
MetaValueType         —[DescribedBy]→ MetaTypeDescriptor  
MetaIntegerValueType  —[DescribedBy]→ MetaValueType
```

So:  
🔁 *Meta types themselves are holons*  
🔁 *They need to be described*  
🔁 *They participate in the same system they define*

---

## 🔄 Recursion Meets Structure: MetaTypeDescriptor Extends MetaHolonType

To **avoid repeating** the structural obligations of all holons (like needing `DescribedBy` and `OwnedBy`) across every Meta type…

We simply declare:

```
MetaTypeDescriptor —[Extends]→ MetaHolonType
```

Now, every Meta type (like `MetaValueType`, `MetaPropertyType`, etc.) that is an instance of `MetaTypeDescriptor` inherits from `MetaHolonType`, which defines the baseline expectations for all holon types.

> ✅ Every Meta type becomes both a type descriptor and a holon  
> ✅ DRY design: `MetaHolonType` captures shared structural rules  
> ✅ Recursive closure: the system defines itself in clean, layered cycles

---

## 🧠 Summary of the Pattern

| Concept                 | Relationship                         | Notes                                         |
|-------------------------|--------------------------------------|-----------------------------------------------|
| ValueType               | `DescribedBy → MetaValueType`        | Marks as a valid type holon                  |
| ValueType               | `Extends → ValueConstraints`         | Adds constraints modularly                   |
| MetaValueType           | `DescribedBy → MetaTypeDescriptor`   | Makes it a descriptor of type descriptors    |
| MetaValueType           | `Extends → MetaHolonType`            | Inherits holon-level expectations            |
| Constraints (e.g. StringValueConstraints) | *(no type)* | Purely compositional constraint layer         |

---

## 🧰 Bonus: How You Might Use This in Validation or Import

When validating a `PropertyType` that refers to a ValueType:

1. Confirm the target is a holon
2. Confirm it’s `DescribedBy` `MetaValueType`
3. Confirm it satisfies the constraints from any `Extends` facets

This lets you:

- Reuse constraints
- Compose constraint types
- Keep descriptors clean and minimal
- Keep validation DRY and generalizable

---

================ OLDER ATTEMPTS FOLLOW






## 🧬 Starting Point: Types as Holons

In MAP, every type — including value types — is a **holon**.

Because every type is a holon, it must:

- Be **described by** a `TypeDescriptor`
- Be **owned by** a `HolonSpace`

---

## 🧱 Layer 1: Descriptor Level (Meta Types)

This is the **type of types** level — Meta types describe what type descriptors are.  

For example:

- `MetaValueType` is a `TypeDescriptor`
- It specifies properties and relationships common to all ValueTypes
    - e.g., `type_name`, `ValueType` relationship from `PropertyType`, `type_kind`, etc.

So:

```
MapStringValueType —[DescribedBy]→ MetaValueType  
PropertyNameValueType —[DescribedBy]→ MetaValueType
```

Now these holons are known to be TypeDescriptors and are expected to provide things like `type_name`, and be usable in `ValueType` relationships from `PropertyType`.

But because every type is also a holon, the types themselves need to be `DescribedBy` a `TypeDescriptor` and `OwnedBy` a `HolonSpace`. So TypeDescriptor needs to `Extend` Me

---

## 🧱 Layer 2: Constraint Types via `Extends`

Some ValueTypes want to specify **type-kind-specific constraints** — but you don’t want to bake those constraints into every ValueType. You want a modular, reusable structure.

That’s where `Extends` comes in.

Let’s take an example:

```
MapStringValueType —[Extends]→ StringValueConstraints  
PropertyNameValueType —[Extends]→ StringValueConstraints
```

Here:

- `MapStringValueType` defines the general-purpose string value type.
- `PropertyNameValueType` is a specialized string type, e.g., requiring `snake_case`, specific min/max lengths, etc.
- Both share the constraint logic defined in `StringValueConstraints`.

**The key insight** is that `StringValueConstraints` is *not* a type itself. It doesn’t need a `type_name`, `DescribedBy`, etc. It simply adds constraint properties like:

- `min_length`
- `max_length`
- `case_convention`
- `format_hint`

It's a **constraint facet**, not a descriptor.

---

## 🔄 Parallel Pattern for Other Type Kinds

You’d follow this same pattern for other primitive types:

| ValueType              | Extends                  | Constrains via…            |
|------------------------|--------------------------|-----------------------------|
| `MapIntegerValueType`  | `IntegerValueConstraints`| `min_value`, `max_value`    |
| `MapBytesValueType`    | `BytesValueConstraints`  | `length`, `encoding`        |
| `MapBooleanValueType`  | *(no constraints)*       | *(no extra facet needed)*   |
| `MapEnumValueType`     | `EnumValueConstraints`   | `Variants` relationship     |

---

## 📐 Layered Design Overview

```
          ┌────────────────────────────┐
          │     MetaValueType          │ ◄── Describes all ValueType descriptors
          └────────────┬───────────────┘
                       │ DescribedBy
                       ▼
          ┌────────────────────────────┐
          │   MapStringValueType       │ ◄── A TypeDescriptor
          └────────────┬───────────────┘
                       │ Extends
                       ▼
          ┌────────────────────────────┐
          │   StringValueConstraints   │ ◄── Holds constraint properties only
          └────────────────────────────┘
```

You can generalize this:

- Any `MetaType` describes a descriptor
- Any actual `TypeDescriptor` may `Extend` a constraint holon
- Constraint holons are not TypeDescriptors — they don’t get keys, `DescribedBy`, or `OwnedBy`

---

## ✅ Benefits of This Pattern

- **Clarity**: Descriptors describe types. Constraints constrain them.
- **DRY**: Reuse constraints across many types (e.g., `StringValueConstraints`)
- **Composability**: Add further `Extends` layers if needed, e.g., `StringWithRegexConstraints`
- **Separation of Concerns**: Keep metadata (`type_name`, etc.) distinct from behaviorally meaningful constraints

---

## 💡 Optional: Schema Organization

You may wrap the constraint holons (like `StringValueConstraints`) in their own schema:

```json
{
  "key": "MAP Value Constraints Schema",
  "type": "Schema",
  "relationships": [
    {
      "name": "Components",
      "target": [
        { "$ref": "#StringValueConstraints" },
        { "$ref": "#IntegerValueConstraints" },
        ...
      ]
    }
  ]
}
```

---

Would you like to sketch out the JSON structure for one of these examples (e.g., `PropertyNameValueType` extending `StringValueConstraints`) using this approach?




## Annotated Example -- MAP Strings

`MapStringValueType` is an instance of `MetaValueType`. Thus, it can be the target of a Property's `ValueType` relationship. It may often be the case that the `ValueType` for a property is simply `MapString`. But sometimes we want more specific types. For example, the `PropertyNameValueType` is specifically intended to be the type used for `property_names` in the MAP. As a value type, it is ALSO an instance of `MetaValueType` (i.e., its "type" is `MetaValueType`). Note that `MapString` and `PropertyNameValueType` both have `instance_type_kind` of `String`, so they would both be represented in Rust by the MapString type. But `PropertyNameValueType` might want to specify its own case_convention (snake_case), and length restrictions that differ from the more generic `MapStringValueType`.  And, other than sharing the same type kind, MapStringValueType and PropertyNameValueType have no direct relationship to each other.

Different value type kinds require different kinds of constraints. For example, `Strings` have min and max length and perhaps a format type or template. Integers have min/max values. So the definition of each ValueType has a common facet (in its role as a TypeDescriptor) and a type-kind-specific facet (its constraints.

We can use compositional inheritance to model this. Thus,

(MetaValueType) <- [Extends] - (MapValueConstraintsType)
and
(MapStringValueType) <- [Extends] - (StringValueConstraints)
and
(PropertyNameValueType) <- [Extends] - (StringValueConstraints)

At first, I thought MapValueConstraintsType should perhaps be MetaValueConstraintsType -- but then I realized it is not describing another type. For example, StringValueConstraints is not (itself) a type definition. It specifies the constraints for the ValueType that it extends. Values for the type_name property (and all other TypeDescriptor properties) are set on the ValueType it extends. In other words, the PropertyNameValueType is the actual TypeDescriptor.

### MetaValueType

- Is the type that `Describes` `MapValueType`, so its `type` is `TypeDescriptor`

Each instance of `MapValueType` describes a single ValueType. It is a `TypeDescriptor` that provides values for the standard `TypeDescriptor` properties (e.g, `type_name`, `display_name_plural`, `instance_type_kind`, etc.).

MetaValueType is an instance of TypeDescriptor that describes MapValueType
MapValueType is an instance of MetaValueType (i.e., its "type" is "MetaValueType") -- SINGLETON?
MapStringType is an instance of MapValueType (or MetaValueType)

An XxxValueType consists of a TypeDescriptor that is ExtendedBy an XxxConstraintType
The X
StringConstraints Extends MapStringType

As such it provides values for the `TypeDescriptor` `properties`:

* "type_name": "MetaValueType",
* "type_name_plural": "MetaValueTypes",
* "display_name": "Meta Value Type",
* "display_name_plural": "Meta Value Types",
* "description": "Describes the types that can be used as the target of a `Property`'s `ValueType` relationship."
* "instance_type_kind": "Holon"

All Meta types describe types and all type definitions are, themselves, Holons. So the instance_type_kind for all Meta types is "Holon"

- "UsesKeyRule": { "$ref": "#TypeName.KeyRule" }
- instance_type_kind tells you the storage type (i.e., the BaseType) of instances of the type being described
- MapValueType is the TypeDescriptor for all value types
- MetaStringConstraints Extends MetaValueType and

```json

 {
              "key": "MetaPropertyType",
              "type": "#TypeDescriptor",
              "properties": {
                "type_name": "MetaPropertyType",
                "type_name_plural": "MetaPropertyTypes",
                "display_name": "Meta Property Type",
                "display_name_plural": "Meta Property Types",
                "description": "Describes the types of scalar properties that holons can possess."
              },
              "relationships": [
                {
                  "name": "Extends",
                  "target": {
                    "$ref": "#MetaTypeDescriptor"
                  }
                },
                {
                  "name": "UsesKeyRule",
                  "target": {  $ref": "#TypeName.KeyRule" }
                },
                {
                  "name": "InstanceRelationships",
                  "target": [
                    {
                      "$ref": "#(PropertyType)-[ValueType]->(ValueType)"
                    },
                    {
                      "$ref": "#(PropertyType)-[ComponentOf]->(Schema)"
                    },
                    {
                      "$ref": "#(PropertyType)-[DescribedBy]->(TypeDescriptor)"
                    }
                  ]
                }
              ]
            },

```

```json

 {
              "key": "MetaPropertyType",
              "type": "#TypeDescriptor",
              "properties": {
                "type_name": "MetaPropertyType",
                "type_name_plural": "MetaPropertyTypes",
                "display_name": "Meta Property Type",
                "display_name_plural": "Meta Property Types",
                "description": "Describes the types of scalar properties that holons can possess."
              },
              "relationships": [
                {
                  "name": "Extends",
                  "target": {
                    "$ref": "#MetaTypeDescriptor"
                  }
                },
                {
                  "name": "UsesKeyRule",
                  "target": {
                    "$ref": "#TypeName.KeyRule"
                  }
                },
                {
                  "name": "InstanceRelationships",
                  "target": [
                    {
                      "$ref": "#(PropertyType)-[ValueType]->(ValueType)"
                    },
                    {
                      "$ref": "#(PropertyType)-[ComponentOf]->(Schema)"
                    },
                    {
                      "$ref": "#(PropertyType)-[DescribedBy]->(TypeDescriptor)"
                    }
                  ]
                }
              ]
            },

```
### MapValueType

```json
{
  "key": "MapValueType",
  "type": "#TypeDescriptor"
}
```