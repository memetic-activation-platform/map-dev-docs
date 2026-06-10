# MAP _Holon Data Loader_ Design Specification (v1.2)

---

## 📘 Summary

The _Holon Data Loader_ converts holon data presented in JSON files into Holons and HolonRelationships that are staged and committed to a single MAP Space using existing MAP APIs.

Because MAP type definitions are themselves holons, the loader supports importing descriptor holons just like any other data. In canonical JSON imports, the `type` field is shorthand for a `DescribedBy` relationship, so runtime holons and schema descriptors share the same loader surface.

Input files are syntactically validated against a JSON Schema to ensure they represent well-formed holons, properties, and relationships.

Validation of imported holons against the concrete descriptors that describe them is triggered by standard Holochain validation callbacks. These callbacks, implemented in the `holons_integrity_zome`, invoke shared validation functions that are **Holochain-independent**, enabling reuse across runtime and tooling contexts.

---

## 🔄 What’s Changed in v1.2

- **Unified `$ref` Model**
  - Replaced mixed and ambiguous reference semantics with a clean, key-based model
  - Removed distinction between staged vs saved references in syntax

- **Eliminated `temp_key`**
  - All references now use stable keys or IDs
  - Simplifies authoring and loader implementation

- **Introduced Staged-First Resolution**
  - Key-based references now resolve:
    1. Against holons in the current import
    2. Then against persisted holons
  - Enables order-independent and circular references

- **Simplified `$ref` Syntax**
  - Default form is now just `key`
  - `#` prefix retained for backward compatibility but made semantically inert

- **Opaque Key Handling**
  - Keys are treated as opaque strings by the loader
  - The loader does not parse type information out of key text
  - Any type-derived key structure is the responsibility of key rules, not loader syntax

- **Moved Authoring Details to Authoring Guide**
  - JSON structure, `$ref` usage examples, and formatting rules relocated
  - Design spec now focuses on architecture and semantics

- **Explicit `$ref` Resolution Semantics**
  - Defined deterministic resolution order
  - Established staged precedence over persisted holons

---

## 🧠 Design Principles

| Principle                  | Description                                                     |
|----------------------------|-----------------------------------------------------------------|
| Holonic Uniformity         | Everything — including types — is a holon                       |
| Two-Pass Resolution        | Prevents ordering constraints and supports circular references  |
| Identity-Based Referencing | Loader references resolve by logical identity using opaque keys |
| Descriptor Integrity       | Descriptor holons must satisfy their `DescribedBy` meta-type and inherited structural anchors |
| Import Scope               | One import targets one HolonSpace                               |
| Staged-First Resolution    | References prefer holons in the current import                  |
| Minimal Syntax             | Concise reference model with limited, consistent prefixes       |

---

## 🔗 `$ref` Model (Design-Level Specification)

All holon-to-holon references are expressed using a `$ref` string. For the loader, `$ref` is interpreted as an opaque key reference, not as a lifecycle marker.

### 🧠 Conceptual Model

A `$ref` identifies a holon by logical identity using its key.

The loader resolves references using a **staged-first strategy**, making imports deterministic and order-independent.

---

## ✅ Supported `$ref` Forms

### 1. Local Reference by Key

Allowed variants:

- `future-primal`
- `#future-primal`

**Design Semantics:**

- Identifies a holon by logical key
- The key is treated as an opaque string by the loader
- `#` prefix is retained for backward compatibility but is **semantically inert**

---

## 🔍 Resolution Semantics

### Key-Based References

For any reference of the form:

- `key`
- `#key`

Resolution proceeds as follows:

1. Check staged holons (current import)
2. If not found, check saved holons (DHT)
3. If not found, fail resolution

---

## ⚠️ Critical Design Guarantees

- `$ref` syntax does **not encode lifecycle state** (staged vs saved)
- `#` prefix **MUST NOT alter resolution behavior**
- There is **no separate namespace** for staged holons
- Key-based references are **deterministic** due to staged-first resolution
- If a key exists in both staged and saved holons:
  - **Staged holon takes precedence**
- The loader treats keys as opaque strings and does not parse type information from key text

---

## 🧩 Design Implications of the `$ref` Model

### 1. Elimination of `temp_key`

- No transient identifier namespace is required
- Keys serve as stable identifiers across both staged and saved contexts
- Simplifies authoring and reduces cognitive overhead

---

### 2. Order Independence

Because references resolve against staged holons:

- Holons may reference others defined later in the file
- Circular references are naturally supported
- Import ordering is no longer significant

---

### 3. Unified Identity Model

There is no distinction in syntax between:

- referencing a holon being created
- referencing an existing holon

This enables:

- seamless merging of imports with existing data
- consistent mental model for authors and tooling

---

### 4. Opaque Keys

- Loader references remain concise and portable because they use keys
- Any type-derived key prefix is part of the key itself, not a loader qualifier
- The loader does not infer type from key text

This keeps loader behavior simple and aligned with key-rule ownership of key structure.

---

## 🧩 Process Overview

![img.png](media/DataLoaderFlow.png)

---

## 🧭 Step-by-Step Flow

1. Define holons (e.g., Airtable)
2. Export CSV
3. Convert to JSON
4. Validate against JSON Schema
5. Parse into `HolonImportSpec`
6. Invoke Holon Data Loader
7. Stage holons (Pass 1)
8. Resolve relationships (Pass 2)
9. Commit to DHT
10. Trigger validation
11. Run shared validation logic

---

## 💾 Staging and Commit Process

### Pass 1: Stage Holons
- Create in-memory holon representations
- Populate properties only
- Register keys for resolution
- Queue relationships for Pass 2

---

### Pass 2: Resolve and Stage Relationships
- Resolve all `$ref` targets
- Resolve descriptor `DescribedBy` links first so descriptor identity is available
- Resolve `Extends` links next so descriptor ancestry is queryable
- Resolve `InverseOf` links before general relationship matching
- Rewrite inverse relationships to declared form
- Inline embedded keyless holons
- Populate remaining relationship links against the now-queryable descriptor graph

---

### Commit
- Persist holons via `holons_core`
- Write nodes and SmartLinks
- Trigger validation callbacks

---

## 🔁 Declared vs Inverse Relationships

- Only **Declared Relationships** are persisted
- Inverse relationships are:
  - inferred
  - automatically maintained
  - not directly written

### Authoring Support

The loader allows inverse-style authoring and rewrites it into declared form during staging.

---

## 📌 Keyed vs Keyless Holons

| Feature                              | Keyed Holons | Keyless Holons |
|-------------------------------------|--------------|----------------|
| Has `key`                           | Yes          | No             |
| Can be referenced via `$ref`        | Yes          | No             |
| Must be embedded                    | Optional     | Required       |
| Can be relationship target          | Yes          | No             |

Keyless holons:
- exist only within parent context
- must not be referenced independently

---

## 🔍 Validation Lifecycle

### 1. Pre-Load (Schema Validation)
- JSON Schema ensures structural correctness
- Cascading validation across Meta, Core, and Domain schemas

---

### 2. Loader-Level Validation
- `$ref` targets must resolve
- No references to keyless holons
- Key uniqueness enforced
- Relationship consistency enforced

---

### 3. Post-Commit (Runtime Validation)
- Triggered by Holochain conductor
- Uses shared validation logic
- Enforces:
  - type rules
  - cardinality
  - constraints
  - referential integrity

---

## 🔮 Future Enhancements

- Schema validation for `$ref` expressions
- Streaming imports
- Reference diagnostics
- Preview (dry-run) mode
- Cross-space resolution via relationship navigation or Dance requests if later required

---

## 📎 Summary

The Holon Data Loader provides:

- A unified import mechanism for types and instances
- Deterministic, order-independent loading via two-pass resolution
- A simplified, key-based `$ref` model
- Strong validation across schema, loader, and runtime layers
- Seamless integration with MAP’s holonic and agent-centric architecture

The `$ref` model is central to this design, enabling deterministic staged-first, saved-second resolution while keeping loader responsibilities narrow: resolve opaque keys, not interpret key structure.
