# EffectiveDescriptor Representation Notes

## 1. Purpose

This note captures the current design understanding of `EffectiveDescriptor`s as the compiled runtime representation of MAP descriptors.

The central architectural insight is that MAP now distinguishes between two complementary representations of ontology:

- the **Descriptor Graph**, which is optimized for authoring, evolution, inheritance, composition, and semantic editing
- the **EffectiveDescriptor**, which is optimized for deterministic runtime consumption

`EffectiveDescriptor`s are therefore not primarily a validation artifact. They form the shared runtime semantic surface consumed by multiple MAP subsystems, including DAHN, PVL, the Query Engine, Nursery validation, import processing, and future runtime services.

The key conclusions are:

- `EffectiveDescriptor`s are flattened, compact runtime surfaces derived from authored descriptor graphs.
- They perform inheritance, relationship, and space/reference compression.
- They establish a stable runtime ABI between descriptor authoring and runtime execution.
- They should remain representable as conventional MAP holons.
- Their compiled payload should be stored in a new canonical binary value type rather than by introducing a new Holochain `EntryType`.
- Provenance can be carried through ordinary MAP relationships such as `CompiledFrom` / `CompiledInto`.

---

## 2. Descriptor Graph vs EffectiveDescriptor

MAP intentionally maintains two representations of descriptor semantics.

### Descriptor Graph

The Descriptor Graph is the semantic source of truth.

It is optimized for:

- authoring
- ontology evolution
- inheritance
- descriptor composition
- semantic relationships
- human understanding

Its structure is normalized and graph-oriented.

It is not optimized for repeated runtime interpretation.

---

### EffectiveDescriptor

An `EffectiveDescriptor` is the compiled runtime representation of a descriptor.

It is optimized for:

- deterministic interpretation
- content-addressability
- peer validation
- caching
- runtime lookup
- efficient traversal
- descriptor-aware visualization
- query execution

It is intentionally denormalized and self-contained.

Runtime systems should generally consume `EffectiveDescriptor`s rather than traversing the authored Descriptor Graph.

---

## 3. Runtime Compilation Pipeline

Descriptor authoring and runtime execution are separated by a compilation step.

```
Descriptor Graph
        │
        │  compile
        ▼
EffectiveDescriptor
        │
        ├──────────► DAHN
        ├──────────► PVL
        ├──────────► Nursery
        ├──────────► Query Engine
        ├──────────► Import Pipeline
        ├──────────► Dance Runtime
        └──────────► future runtime services
```

This compilation boundary establishes a stable runtime semantic surface.

Descriptor edits occur against the authored graph.

Runtime systems consume the compiled surface.

This separation avoids repeated graph traversal, repeated inheritance resolution, repeated cross-space dereferencing, and repeated relationship expansion across every runtime subsystem.

---

## 4. What an EffectiveDescriptor Is

An `EffectiveDescriptor` is the canonical runtime semantic surface of a descriptor.

It is not simply a validation artifact.

Rather, it represents the complete effective runtime semantics needed by downstream runtime consumers.

Those semantics include:

- inherited properties
- inherited relationships
- value constraints
- relationship constraints
- key rules
- inverse relationships
- PVL structural rules
- runtime lookup metadata
- cross-space definitional resolution

Its primary consumers include:

- DAHN
- PVL / Integrity validation
- Nursery validation
- Query Engine
- Import Pipeline
- Dance runtime
- descriptor-aware diagnostics
- developer tooling

Validation is therefore one consumer of the runtime semantic surface rather than the reason the surface exists.

---

## 5. Example EffectiveDescriptor

The following is an illustrative deserialized `EffectiveDescriptor` for a simple `Book` type.

It is shown as JSON for readability. In storage, this structure would be encoded into canonical bytes and stored in the `effective_descriptor_bytes` property.

```json
{
  "type_key": "Book",
  "semantic_version": "1.0.0",
  "definition_hash": "defhash:book:v1:7f3a9c...",
  "source_type_key": "Book",
  "is_abstract_type": false,
  "type_kind": "Holon",
  "canonical_encoding": "map.effective-descriptor.v1",

  "effective_properties": {
    "title": {
      "property_key": "title",
      "property_definition_hash": "defhash:property:title:...",
      "value": {
        "kind": "String",
        "constraints": {
          "min_length": 1,
          "max_length": 256
        }
      },
      "required": true,
      "source": "inherited"
    },

    "description": {
      "property_key": "description",
      "property_definition_hash": "defhash:property:description:...",
      "value": {
        "kind": "String",
        "constraints": {
          "max_length": 5000
        }
      },
      "required": false,
      "source": "inherited"
    },

    "isbn": {
      "property_key": "isbn",
      "property_definition_hash": "defhash:property:isbn:...",
      "value": {
        "kind": "String",
        "constraints": {
          "pattern": "^(97[89])?\\d{9}[\\dX]$"
        }
      },
      "required": false,
      "source": "declared"
    },

    "publication_year": {
      "property_key": "publication_year",
      "property_definition_hash": "defhash:property:publication_year:...",
      "value": {
        "kind": "Integer",
        "constraints": {
          "min": 0,
          "max": 3000
        }
      },
      "required": false,
      "source": "declared"
    }
  },

  "effective_relationships": {
    "AUTHORED_BY": {
      "relationship_key": "AUTHORED_BY",
      "relationship_definition_hash": "defhash:relationship:authored_by:...",
      "source_type_key": "Book",
      "source_type_definition_hash": "defhash:type:book:...",
      "target_type_key": "Person",
      "target_type_definition_hash": "defhash:type:person:...",
      "min_cardinality": 1,
      "max_cardinality": null,
      "ordered": true,
      "required": true,
      "source": "inherited"
    },

    "PUBLISHED_BY": {
      "relationship_key": "PUBLISHED_BY",
      "relationship_definition_hash": "defhash:relationship:published_by:...",
      "source_type_key": "Book",
      "source_type_definition_hash": "defhash:type:book:...",
      "target_type_key": "Organization",
      "target_type_definition_hash": "defhash:type:organization:...",
      "min_cardinality": 0,
      "max_cardinality": 1,
      "ordered": false,
      "required": false,
      "source": "declared"
    },

    "PART_OF_SERIES": {
      "relationship_key": "PART_OF_SERIES",
      "relationship_definition_hash": "defhash:relationship:part_of_series:...",
      "source_type_key": "Book",
      "source_type_definition_hash": "defhash:type:book:...",
      "target_type_key": "BookSeries",
      "target_type_definition_hash": "defhash:type:book_series:...",
      "min_cardinality": 0,
      "max_cardinality": 1,
      "ordered": false,
      "required": false,
      "source": "declared"
    }
  },

  "effective_inverse_relationships": {
    "HAS_BOOK": {
      "relationship_key": "HAS_BOOK",
      "relationship_definition_hash": "defhash:relationship:has_book:...",
      "source_type_key": "Library",
      "source_type_definition_hash": "defhash:type:library:...",
      "target_type_key": "Book",
      "target_type_definition_hash": "defhash:type:book:...",
      "inverse_of": "HOLDS",
      "min_cardinality": 0,
      "max_cardinality": null,
      "ordered": false
    }
  },

  "effective_key_rule": {
    "key_rule_type": "Optional",
    "recommended_key_properties": ["isbn"],
    "fallback": "keyless"
  },

  "pvl_surface": {
    "required_properties": ["title"],

    "property_value_checks": {
      "title": {
        "base_type": "String",
        "min_length": 1,
        "max_length": 256
      },
      "description": {
        "base_type": "String",
        "max_length": 5000
      },
      "isbn": {
        "base_type": "String",
        "pattern": "^(97[89])?\\d{9}[\\dX]$"
      },
      "publication_year": {
        "base_type": "Integer",
        "min": 0,
        "max": 3000
      }
    },

    "relationship_checks": {
      "AUTHORED_BY": {
        "target_type_key": "Person",
        "target_type_definition_hash": "defhash:type:person:...",
        "min_cardinality": 1,
        "max_cardinality": null,
        "ordered": true
      },
      "PUBLISHED_BY": {
        "target_type_key": "Organization",
        "target_type_definition_hash": "defhash:type:organization:...",
        "min_cardinality": 0,
        "max_cardinality": 1,
        "ordered": false
      },
      "PART_OF_SERIES": {
        "target_type_key": "BookSeries",
        "target_type_definition_hash": "defhash:type:book_series:...",
        "min_cardinality": 0,
        "max_cardinality": 1,
        "ordered": false
      }
    }
  },

  "non_pvl_semantics": {
    "nursery_rules": [
      {
        "rule_key": "likely_duplicate_isbn",
        "severity": "warning",
        "reason": "Requires local snapshot query over existing Book claims."
      }
    ],
    "trust_or_attestation_rules": [
      {
        "rule_key": "publisher_must_be_verified_org",
        "reason": "Depends on agreement-scoped trust or external attestation."
      }
    ]
  }
}
```

---

## 6. Deserialized EffectiveDescriptor Struct

The following is an illustrative Rust-style structure for the deserialized effective descriptor payload.

```rust
pub struct EffectiveDescriptor {
    pub type_key: TypeKey,
    pub semantic_version: SemanticVersion,
    pub definition_hash: DefinitionHash,
    pub source_type_key: TypeKey,
    pub is_abstract_type: bool,
    pub type_kind: TypeKind,
    pub canonical_encoding: CanonicalEncodingId,

    pub effective_properties: BTreeMap<PropertyKey, EffectivePropertySpec>,
    pub effective_relationships: BTreeMap<RelationshipKey, EffectiveRelationshipSpec>,
    pub effective_inverse_relationships: BTreeMap<RelationshipKey, EffectiveInverseRelationshipSpec>,
    pub effective_key_rule: Option<EffectiveKeyRuleSpec>,

    pub pvl_surface: PvlSurface,
    pub non_pvl_semantics: NonPvlSemantics,
}

pub struct EffectivePropertySpec {
    pub property_key: PropertyKey,
    pub property_definition_hash: DefinitionHash,
    pub value: EffectiveValueSpec,
    pub required: bool,
    pub source: EffectiveSourceKind,
}

pub struct EffectiveValueSpec {
    pub kind: BaseValueKind,
    pub constraints: ValueConstraints,
}

pub struct ValueConstraints {
    pub min: Option<i64>,
    pub max: Option<i64>,
    pub min_length: Option<u64>,
    pub max_length: Option<u64>,
    pub pattern: Option<String>,
    pub enum_values: Option<Vec<String>>,
}

pub struct EffectiveRelationshipSpec {
    pub relationship_key: RelationshipKey,
    pub relationship_definition_hash: DefinitionHash,

    pub source_type_key: TypeKey,
    pub source_type_definition_hash: DefinitionHash,

    pub target_type_key: TypeKey,
    pub target_type_definition_hash: DefinitionHash,

    pub min_cardinality: u32,
    pub max_cardinality: Option<u32>,
    pub ordered: bool,
    pub required: bool,
    pub source: EffectiveSourceKind,
}

pub struct EffectiveInverseRelationshipSpec {
    pub relationship_key: RelationshipKey,
    pub relationship_definition_hash: DefinitionHash,

    pub source_type_key: TypeKey,
    pub source_type_definition_hash: DefinitionHash,

    pub target_type_key: TypeKey,
    pub target_type_definition_hash: DefinitionHash,

    pub inverse_of: RelationshipKey,
    pub min_cardinality: u32,
    pub max_cardinality: Option<u32>,
    pub ordered: bool,
}

pub struct EffectiveKeyRuleSpec {
    pub key_rule_type: KeyRuleKind,
    pub recommended_key_properties: Vec<PropertyKey>,
    pub fallback: Option<KeyRuleFallback>,
}

pub struct PvlSurface {
    pub required_properties: Vec<PropertyKey>,
    pub property_value_checks: BTreeMap<PropertyKey, PvlValueCheck>,
    pub relationship_checks: BTreeMap<RelationshipKey, PvlRelationshipCheck>,
}

pub struct PvlValueCheck {
    pub base_type: BaseValueKind,
    pub min: Option<i64>,
    pub max: Option<i64>,
    pub min_length: Option<u64>,
    pub max_length: Option<u64>,
    pub pattern: Option<String>,
    pub enum_values: Option<Vec<String>>,
}

pub struct PvlRelationshipCheck {
    pub target_type_key: TypeKey,
    pub target_type_definition_hash: DefinitionHash,
    pub min_cardinality: u32,
    pub max_cardinality: Option<u32>,
    pub ordered: bool,
}

pub struct NonPvlSemantics {
    pub nursery_rules: Vec<NonPvlRuleRef>,
    pub trust_or_attestation_rules: Vec<NonPvlRuleRef>,
}

pub struct NonPvlRuleRef {
    pub rule_key: RuleKey,
    pub severity: RuleSeverity,
    pub reason: String,
}

pub enum EffectiveSourceKind {
    Declared,
    Inherited,
}

pub enum BaseValueKind {
    String,
    Integer,
    Boolean,
    Enum,
    Bytes,
    CanonicalBytes,
}

pub enum KeyRuleKind {
    Required,
    Optional,
    None,
    Derived,
}

pub enum KeyRuleFallback {
    Keyless,
}
```

---

## 7. CanonicalBytes ValueType

`CanonicalBytes` is a new ValueType used to store deterministic serialized artifacts.

It is intended for cases where the payload must be:

- byte-for-byte deterministic
- hash-stable
- suitable for peer validation
- safe to decode inside PVL
- free from JSON ordering ambiguity

For `EffectiveDescriptor` storage:

    effective_descriptor_bytes: CanonicalBytes

contains the canonical serialized form of the `EffectiveDescriptor` struct.

The encoding should be versioned:

    canonical_encoding = "map.effective-descriptor.v1"

The exact binary encoding may be CBOR, MessagePack, postcard, bincode with strict configuration, or another deterministic encoding. The key requirement is canonical determinism, not the specific format.

---

## 8. Provenance via CompiledFrom / CompiledInto

The `EffectiveDescriptor` holon may carry provenance using ordinary MAP relationships.

### 8.1 CompiledFrom

    EffectiveDescriptor --CompiledFrom--> HolonType

`CompiledFrom` points to the exact committed source HolonType version from which the `EffectiveDescriptor` was compiled.

The target should be an `ActionHash`-identified HolonNode version.

This gives precise, version-specific provenance.

`CompiledFrom` is definitional for the `EffectiveDescriptor`.

The meaning and identity of an `EffectiveDescriptor` depends on the exact source descriptor version it was compiled from.

---

### 8.2 CompiledInto

    HolonType --CompiledInto--> EffectiveDescriptor

`CompiledInto` is the inverse of `CompiledFrom`.

It is useful for navigation, indexing, diagnostics, and tooling.

However, `CompiledInto` is not definitional for the HolonType.

Otherwise, every compilation event would change the HolonType's definitional surface and trigger an infinite feedback loop:

    HolonType changes
      → compile EffectiveDescriptor
      → add CompiledInto
      → HolonType definition changes
      → compile again

Therefore:

- `CompiledFrom` is definitional from the EffectiveDescriptor side.
- `CompiledInto` is non-definitional from the HolonType side.

This demonstrates that inverse relationships do not necessarily share the same definitional classification. Definitional status is directional and depends on whether the relationship contributes to the definitional surface of the source holon.

---

## 9. Validation Flow Using Stored EffectiveDescriptors

The peer-validation flow becomes:

    HolonNode being validated
      has effective_descriptor_hash
        ↓
    Integrity Zome calls must_get_valid_record(effective_descriptor_hash)
        ↓
    retrieves EffectiveDescriptor HolonNode
        ↓
    extracts effective_descriptor_bytes: CanonicalBytes
        ↓
    deserializes EffectiveDescriptor
        ↓
    PVL validates HolonNode against EffectiveDescriptor.pvl_surface

This avoids:

- live descriptor graph traversal
- inheritance resolution during validation
- SmartLink traversal during validation
- cross-space descriptor dereferencing during validation
- ReferenceLayer cache dependence
- dynamic rule dispatch

while preserving:

- ordinary MAP holon representation
- graph-addressable provenance
- content-addressed validation surfaces
- Holochain peer-validation semantics