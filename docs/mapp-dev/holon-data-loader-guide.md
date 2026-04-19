# Holon Data Loader Authoring Guide (v1.1)

---

## 📘 Overview

The **Holon Data Loader** enables the import of holons and their relationships into a MAP Space using JSON files.

This guide provides a **complete reference for authoring valid import data**, including:
- JSON structure
- Holon composition
- Relationship modeling
- `$ref` usage
- Validation expectations

It is intended for both human authors and tooling systems generating MAP-compatible data.

---

## 🧠 Core Authoring Principles

- **Everything is a holon** — including types, properties, and relationships
- **One import targets one HolonSpace**
- **All required TypeDescriptors must be present or preloaded**
- **Relationships are expressed exclusively via `$ref` or embedding**
- **Holons may reference others defined in the same file or already persisted**
- **Resolution is staged-first** — references prefer holons defined in the current import
- **Order does not matter** — references are resolved after all holons are staged

---

## 📂 JSON Import Structure

A JSON import file contains:

```
{
  "meta": { ... },        // optional
  "holons": [ ... ]       // required
}
```

### `meta` (optional)
Metadata about the import (e.g., version, description, author)

### `holons` (required)
An array of holon definitions

---

## 🧩 Holon Structure

Each holon is defined as:

```
{
  "type": "<TypeRef>",
  "key": "<optional-key>",
  "properties": { ... },
  "relationships": [ ... ]
}
```

### Fields

| Field | Required | Description |
|------|----------|-------------|
| `type` | ✅ | `$ref` to the holon’s TypeDescriptor |
| `key` | ⚠️ | Required for keyed holons |
| `properties` | ✅ | Map of property values |
| `relationships` | optional | Array of relationship definitions |

---

## 🔑 Keyed vs Keyless Holons

### Keyed Holons

- Have a `key`
- Are uniquely identifiable within a space
- Can be referenced via `$ref`

### Keyless Holons

- Do **not** have a `key`
- Cannot be referenced via `$ref`
- Must be embedded inside another holon

---

## 🔗 Relationships

Each relationship is defined as:

```
{
  "name": "<RelationshipName>",
  "target": <Target>
}
```

### Target forms

#### 1. Reference
```
{ "$ref": "some-key" }
```

#### 2. Multiple references
```
[
  { "$ref": "a" },
  { "$ref": "b" }
]
```

#### 3. Embedded holon (keyless)
```
{
  "type": "<TypeRef>",
  "properties": { ... },
  "relationships": [ ... ]
}
```

---

## 🔁 Declared vs Inverse Relationships

- Only **Declared Relationships** are persisted
- Inverse relationships are:
  - inferred automatically
  - not directly stored

### Authoring support

You may express inverse relationships in JSON; the loader will rewrite them into their declared form.

⚠️ Do not define both directions of the same relationship in one import.

---

## 🔗 `$ref` Usage

All relationship targets referencing keyed holons must use `$ref`.

---

## ✅ Supported `$ref` Formats

### 1. Local Reference by Key (Preferred)

Allowed forms:

- `future-primal`
- `#future-primal`

Optional type-qualified variants:

- `BookType:future-primal`
- `#BookType:future-primal`

**Guidance:**
- Use simple key references whenever possible
- Use type-qualified references only when needed for disambiguation
- The `#` prefix is optional and has no effect on behavior

---

### 2. Local Reference by ID

```
id:uhCAkYmv...
```

**Guidance:**
- Refers to a persisted holon
- Does not resolve to holons in the current import
- Use sparingly in authored data

---

### 3. External Reference by Proxy Name

```
@Library:future-primal
@Library:BookType:future-primal
```

**Guidance:**
- References a holon in another HolonSpace
- `Library` must be a configured proxy
- Prefer proxy name for readability

---

### 4. External Reference by Proxy ID

```
ext:<ProxyId>:<LocalId>
```

**Guidance:**
- Fully explicit external reference
- Typically system-generated

---

## 🔍 Resolution Behavior

### Key-based references

1. Check holons in current import
2. If not found, check persisted holons
3. If not found, fail

### Important implications

- You can reference holons defined later in the file
- Circular references are supported
- Import ordering is irrelevant

---

## ⚠️ Constraints

- `$ref` targets must resolve successfully
- Only keyed holons may be referenced
- Keyless holons must be embedded
- Keys must be unique within the import
- If a key exists in both import and persisted data:
  - The import version takes precedence
- `#` prefix does not affect behavior
- There is no staged vs saved syntax distinction

---

## 🧪 Validation Expectations

### Pre-load (Schema Validation)
- JSON structure must conform to schema
- `$ref` strings must be valid format

### Loader-level validation
- All `$ref` targets must resolve
- No references to keyless holons
- Keys must be unique
- Relationship definitions must be valid

### Runtime validation
- Enforced via TypeDescriptors
- Includes:
  - required properties
  - value types
  - relationship constraints
  - cardinality rules

---

## 📘 Example

```
{
  "type": "BookType",
  "key": "future-primal",
  "properties": {
    "title": {
      "type": "MapString",
      "value": "Future Primal"
    }
  },
  "relationships": [
    {
      "name": "AUTHORED_BY",
      "target": { "$ref": "charles-eisenstein" }
    },
    {
      "name": "CITED_IN",
      "target": { "$ref": "@Library:climate-effects-2024" }
    }
  ]
}
```

---

## 🧩 Best Practices

- Prefer simple key-based `$ref`s
- Use type-qualified `$ref`s only when needed
- Keep keys stable and meaningful
- Group related holons together
- Avoid relying on implicit matches to existing data
- Use embedding for contextual, non-reusable data
- Define proxies before referencing external data

---

## 🚫 Removed / Deprecated Concepts

- `temp_key` is no longer used
- There is no staged-only reference syntax
- `$ref` does not encode lifecycle state

---

## 🔮 Future Enhancements

- JSON Schema validation for `$ref`
- Authoring tools with autocomplete
- Preview (dry-run) mode
- Improved diagnostics for resolution failures

---

## 📎 Summary

This guide defines how to author valid MAP import data using:

- A consistent holon structure
- Clear distinction between keyed and keyless holons
- A simplified, identity-based `$ref` system
- Two-pass resolution enabling flexible authoring

Authors can rely on:
- minimal syntax
- strong validation
- deterministic behavior

while maintaining clarity and expressiveness in JSON imports.