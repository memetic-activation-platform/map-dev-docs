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