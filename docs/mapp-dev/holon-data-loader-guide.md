# Holon Data Loader Authoring Guide

---

## 📘 Overview

The **Holon Data Loader** enables the import of holons and their relationships into a MAP Space using JSON files. This guide focuses on how to correctly author those JSON files, with particular attention to `$ref` usage, which is central to expressing relationships.

---

## 🧠 Core Authoring Principles

- **Everything is a holon** — including types, properties, and relationships
- **One import targets one HolonSpace**
- **All required TypeDescriptors must be present or preloaded**
- **Relationships are expressed exclusively via `$ref`**
- **Holons may reference others defined in the same file or already persisted**
- **Resolution is staged-first** — references prefer holons defined in the current import

---

## 🔗 `$ref` Usage

All relationship targets must be expressed using a `$ref` string.

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
- Use type-qualified references only when needed for clarity or disambiguation
- The `#` prefix is optional and has no effect on behavior

---

### 2. Local Reference by ID (Explicit)

- `id:uhCAkYmv...`

**Guidance:**
- Use when referencing a specific persisted holon
- Useful when keys are not known or may not be unique
- Not commonly used in authored files; more typical in system-generated references

---

### 3. External Reference by Proxy Name

- `@Library:future-primal`
- `@Library:BookType:future-primal`

**Guidance:**
- Use when referencing holons in another HolonSpace
- `Library` must be a configured proxy in the local space
- Prefer proxy name for readability

---

### 4. External Reference by Proxy ID

- `ext:uhCAkProxy...:uhCAkLocal...`

**Guidance:**
- Fully explicit reference
- Typically system-generated rather than hand-authored

---

## 🔍 Resolution Behavior (Author Awareness)

When using key-based references:

1. The loader first checks holons defined in the current import
2. If not found, it checks holons already stored in the DHT
3. If still not found, the import fails

**Implication for authors:**
- You can reference holons that appear later in the same file
- You do not need to order holons to satisfy dependencies
- You should avoid relying on implicit matches to existing data unless intentional

---

## ⚠️ Important Constraints

- The `#` prefix is **optional** and **does not change meaning**
- There is **no separate namespace** for staged vs saved holons
- Keys must be unique within the scope of the import
- If a key exists both in the import and in the DHT:
  - The import version takes precedence
- All `$ref` values must resolve successfully or the load will fail

---

## 🚫 Removed / Deprecated Concepts

- `temp_key` is no longer used
- There is no staged-only reference syntax
- `$ref` does not encode resolution behavior beyond prefix type (local vs external)

---

## 📘 Example

```json
{
  "type_name": "BookType",
  "key": "future-primal",
  "properties": {
    "title": { "type": "MapString", "value": "Future Primal" }
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

- Prefer simple key references for readability
- Keep keys stable and meaningful
- Avoid unnecessary type qualification unless required
- Group related holons in the same import for clarity
- Ensure external proxies are defined before use

---

## 🔮 Future Enhancements

- Validation of `$ref` formats via JSON Schema
- Authoring tools with autocomplete and validation
- Preview mode for dry-run validation
- Enhanced diagnostics for unresolved references

---

This guide reflects the current canonical `$ref` model and should be used as the basis for all new import files.