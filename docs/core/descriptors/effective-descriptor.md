# EffectiveDescriptor Artifact Design

## 1. Purpose

This document defines the `EffectiveDescriptor` artifact: its identity, canonical representation, payload semantics, bootstrap contract, and lifecycle.

An `EffectiveDescriptor` is the compiled runtime semantic surface of an authored Descriptor Graph. It is not primarily a validation artifact. It is shared by DAHN, Query Engine, Import Pipeline, PVL, Nursery validation, Dance runtime, `RoleAccessDescriptor` compilation, diagnostics, and developer tooling.

The Descriptor Graph remains the authored semantic source. The `EffectiveDescriptor` is the deterministic runtime artifact derived from that source.

---

## 2. Descriptor Graph vs EffectiveDescriptor

MAP intentionally maintains two complementary descriptor representations.

### Descriptor Graph

The Descriptor Graph is optimized for:

- authoring
- ontology evolution
- inheritance
- descriptor composition
- semantic relationships
- human understanding
- governance and review

It is normalized and graph-oriented. It is not the preferred surface for repeated runtime interpretation.

### EffectiveDescriptor

An `EffectiveDescriptor` is optimized for:

- deterministic interpretation
- content-addressability
- peer validation
- caching
- runtime lookup
- efficient traversal
- descriptor-aware visualization
- query execution
- import and provisioning

It is intentionally denormalized and self-contained.

Runtime systems should consume `EffectiveDescriptor`s rather than repeatedly traversing authored Descriptor Graphs.

---

## 3. Compilation Pipeline

Descriptor authoring and runtime execution are separated by a compilation step.

    Descriptor Graph
        |
        | compile
        v
    canonical DAG-CBOR EffectiveDescriptor payload
        |
        | BLAKE3 digest
        v
    canonical EffectiveDescriptor carrier HolonNode
        |
        +--> DAHN
        +--> PVL
        +--> Nursery
        +--> Query Engine
        +--> Import Pipeline
        +--> Dance Runtime
        +--> diagnostics and tooling

Compilation performs three compressions:

- inheritance compression
- definitional relationship compression
- space/reference compression

This avoids repeated graph traversal, repeated inheritance resolution, repeated cross-space dereferencing, and repeated relationship expansion across runtime subsystems.

---

## 4. Identity Model

`EffectiveDescriptor` architecture separates logical type identity, authored revision identity, publication version metadata, payload identity, local retrieval identity, and provenance identity.

### 4.1 `TypeName`

`TypeName` is the key of a `TypeDescriptor` and identifies the continuing logical type.

It does not identify:

- a specific semantic version
- a specific compiled payload
- a specific Holochain entry
- a specific committed descriptor record

### 4.2 `DescriptorRevisionId`

`DescriptorRevisionId` identifies one authored `TypeDescriptor` revision before it is saved.

It is useful because semantic version is assigned only after ordering, merge, acceptance, or publication. Concurrent candidate revisions need stable identity before governance can decide which revision, if any, receives a semantic version.

Conceptually:

    TypeName: Book
    DescriptorRevisionId: 7f4c...

The authored graph can therefore key a `TypeDescriptor` revision by:

    TypeName + DescriptorRevisionId

`DescriptorRevisionId` is not part of the canonical `EffectiveDescriptor` payload. Multiple authored revisions may legitimately compile into the same runtime semantic artifact.

### 4.3 Semantic Version

Semantic version identifies a declared revision of a logical type.

Conceptually:

    TypeName: Book
    SemanticVersion: 1.0.0

Semantic version is publication and revision metadata, not compiled semantic content.

It is assigned after the source `TypeDescriptor` `HolonNode` has been saved and attached through non-definitional `Version` / `VersionFor` relationships.

Therefore semantic version:

- is not part of the canonical `EffectiveDescriptor` payload
- does not participate in `EffectiveDescriptorDigest`
- is not required by Integrity/PVL to interpret an `EffectiveDescriptor`
- can be obtained by runtime consumers from descriptor publication, activation, or provenance context

### 4.4 `EffectiveDescriptorDigest`

`EffectiveDescriptorDigest` is the substrate-independent identity of the exact compiled payload.

It is calculated as:

    EffectiveDescriptorDigest =
      BLAKE3(canonical DAG-CBOR EffectiveDescriptor payload)

The digest is not a hash of the authored Descriptor Graph. It is a hash of the canonical compiled artifact after inheritance, definitional relationships, and space/reference dependencies have been resolved into the runtime payload.

The digest is independent of:

- Holochain `EntryHash`
- `ActionHash`
- `ExternalId`
- `OutboundProxyId`
- route information
- local provenance
- activation state
- storage substrate

### 4.5 `EffectiveDescriptorHash`

`EffectiveDescriptorHash` is the Holochain `EntryHash` of the canonical EffectiveDescriptor carrier `HolonNode`.

It is used for:

- local Holochain retrieval
- `must_get_entry` / deterministic dependency lookup
- ordinary holon descriptor binding
- Holochain-local activation records
- local cache lookup

`EffectiveDescriptorHash` is distinct from `EffectiveDescriptorDigest`.

When two spaces use the same canonical Holochain carrier, identical payloads should produce identical carrier `EntryHash` values. Cross-substrate architecture must still treat the BLAKE3 digest as the portable artifact identity.

### 4.6 Provenance

`CompiledFrom` points to an exact committed source descriptor revision, normally by `ActionHash`.

It is provenance and navigation, not semantic artifact identity.

Therefore:

- provenance is separate from semantic identity
- `CompiledFrom` is not required by PVL
- multiple authored descriptor graphs may legitimately compile into the same `EffectiveDescriptorDigest`
- changing provenance without changing the payload must not change the digest

---

## 5. Canonical Carrier Contract

`EffectiveDescriptor` artifacts are represented as conventional MAP holons, not as a new Holochain `EntryType`.

The canonical carrier `HolonNode` has exactly this semantic property set:

- `EffectiveDescriptorDagCbor`
- `EffectiveDescriptorDigest`

No additional semantic or cosmetic properties are permitted on the carrier.

The carrier must not contain:

- display labels
- notes
- timestamps
- author-dependent metadata
- route-specific IDs
- local provenance
- activation state
- mutable operational metadata
- arbitrary additional properties

The carrier is immutable compiled data. A changed payload always produces a new artifact rather than an update to an existing artifact.

`EffectiveDescriptor` artifacts do not themselves have an `EffectiveDescriptor` dependency. They require a bootstrap validation path in Integrity/PVL.

Required bootstrap/provisioning order:

1. commit `EffectiveDescriptor` artifacts
2. create provenance/navigation links such as `CompiledFrom` / `CompiledInto`
3. activate descriptors in an AgentSpace
4. commit ordinary holons that bind to activated descriptor artifacts

---

## 6. Payload Content

The canonical DAG-CBOR payload contains the runtime semantic surface.

It should include:

- `type_name`
- `EffectiveDescriptor` format version
- canonical encoding identifier
- `conforms_to`
- effective properties
- effective relationships
- effective inverse relationships
- effective key rules
- declarative dance contracts, when included
- PVL-safe rule surface
- Nursery rule surface
- explicit dependency declarations where needed for activation-time analysis

It must exclude:

- `ActionHash`
- `ExternalId`
- `OutboundProxyId`
- TrustChannel route information
- local provenance
- activation state
- semantic version / version-range metadata
- local storage identifiers
- cache metadata

Pattern constraints are Nursery-only unless MAP adopts a future deterministic, bounded, linear-time pattern language suitable for PVL.

Version metadata can still be associated with an `EffectiveDescriptor` through publication records, activation records, or provenance/navigation relationships. It is deliberately outside the canonical payload so that assigning or changing a semantic version does not alter the runtime semantic digest.

---

## 7. Illustrative Payload Shape

The following JSON is illustrative only. The stored representation is canonical DAG-CBOR in `EffectiveDescriptorDagCbor`.

```json
{
  "type_name": "Book",
  "format_version": "map.effective-descriptor.v1",
  "canonical_encoding": "dag-cbor",
  "conforms_to": [
    {
      "type_name": "Publication"
    }
  ],
  "effective_properties": {
    "title": {
      "property_key": "title",
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
    "isbn": {
      "property_key": "isbn",
      "value": {
        "kind": "String",
        "constraints": {
          "pattern": "isbn-v1"
        }
      },
      "required": false,
      "source": "declared"
    }
  },
  "effective_relationships": {
    "AUTHORED_BY": {
      "relationship_key": "AUTHORED_BY",
      "target_type": {
        "type_name": "Person"
      },
      "ordered": true,
      "required": true,
      "source": "inherited"
    }
  },
  "effective_inverse_relationships": {},
  "effective_key_rule": {
    "key_rule_type": "Optional",
    "recommended_key_properties": ["isbn"],
    "fallback": "keyless"
  },
  "effective_dances": {
    "view": {
      "dance_key": "view",
      "contract": "map.dance-contract.view.v1",
      "source": "inherited"
    }
  },
  "pvl_surface": {
    "required_properties": ["title"],
    "property_value_checks": {
      "title": {
        "base_type": "String",
        "min_length": 1,
        "max_length": 256
      }
    },
    "relationship_checks": {
      "AUTHORED_BY": {
        "target_type_name": "Person",
        "ordered": true
      }
    }
  },
  "nursery_surface": {
    "rules": [
      {
        "rule_key": "likely_duplicate_isbn",
        "severity": "warning",
        "reason": "Requires local snapshot query over existing Book claims."
      }
    ]
  }
}
```

---

## 8. Illustrative Runtime Structures

```rust
pub struct EffectiveDescriptor {
    pub type_name: TypeName,
    pub format_version: EffectiveDescriptorFormatVersion,
    pub canonical_encoding: CanonicalEncodingId,

    pub conforms_to: Vec<TypeConformanceSpec>,
    pub effective_properties: BTreeMap<PropertyKey, EffectivePropertySpec>,
    pub effective_relationships: BTreeMap<RelationshipKey, EffectiveRelationshipSpec>,
    pub effective_inverse_relationships: BTreeMap<RelationshipKey, EffectiveInverseRelationshipSpec>,
    pub effective_key_rule: Option<EffectiveKeyRuleSpec>,
    pub effective_dances: BTreeMap<DanceKey, EffectiveDanceSpec>,

    pub pvl_surface: PvlSurface,
    pub nursery_surface: NurserySurface,
}

pub struct EffectiveDescriptorCarrier {
    pub effective_descriptor_dag_cbor: DagCbor,
    pub effective_descriptor_digest: Blake3Digest,
}

pub struct TypeConformanceSpec {
    pub type_name: TypeName,
}

pub struct EffectivePropertySpec {
    pub property_key: PropertyKey,
    pub value: EffectiveValueSpec,
    pub required: bool,
    pub source: EffectiveSourceKind,
}

pub struct EffectiveRelationshipSpec {
    pub relationship_key: RelationshipKey,
    pub target_type: TypeConformanceSpec,
    pub ordered: bool,
    pub required: bool,
    pub source: EffectiveSourceKind,
}

pub struct EffectiveInverseRelationshipSpec {
    pub relationship_key: RelationshipKey,
    pub source_type: TypeConformanceSpec,
    pub inverse_of: RelationshipKey,
    pub ordered: bool,
}

pub struct EffectiveDanceSpec {
    pub dance_key: DanceKey,
    pub declarative_contract: DanceContractId,
    pub source: EffectiveSourceKind,
}
```

---

## 9. Canonical DAG-CBOR and BLAKE3

`EffectiveDescriptorDagCbor` stores the canonical serialized payload using the `DagCbor` ValueType.

`EffectiveDescriptorDigest` stores:

    BLAKE3(EffectiveDescriptorDagCbor)

The serialization contract must define:

- deterministic map-key ordering
- deterministic enum representation
- deterministic integer representation
- canonical null/absence semantics
- string normalization policy
- no floating-point ambiguity unless a deterministic encoding is explicitly specified
- rejection of unsupported CBOR tags or alternate encodings

Null and absence must not be accidentally interchangeable. Each optional field must define whether omission or explicit null is canonical.

---

## 10. Resource Bounds

Each `EffectiveDescriptor` format version defines interpretation-cost bounds.

Required bounds include:

- maximum payload size
- maximum nesting depth
- maximum property count
- maximum relationship count
- maximum inverse relationship count
- maximum `conforms_to` entries
- maximum enum values
- maximum string sizes
- maximum pattern length
- maximum declarative dance entries

These bounds constrain interpretation cost, not merely bytes. A payload may be byte-small but still too expensive to interpret if it creates excessive nesting, fanout, or rule expansion.

Over-limit artifacts must be rejected during artifact validation, provisioning, and deterministic PVL decoding.

---

## 11. EffectiveDanceSet

`effective_dances` is a declarative set of Dance contracts available through the compiled type surface.

It includes:

- inherited declarative dance affordances
- declared dance affordances
- compile-time flattening
- inheritance resolution
- ambiguity detection
- declarative contract identity

It explicitly excludes:

- executable implementations
- WASM
- runtime bindings
- deployment information
- host capability grants

Executable dance binding is handled by a separate runtime artifact.

---

## 12. Provenance Relationships

### 12.1 `CompiledFrom`

    EffectiveDescriptor --CompiledFrom--> HolonType

`CompiledFrom` points to an exact committed source `HolonType` version.

It is useful for:

- source navigation
- diagnostics
- recompilation analysis
- governance review

It is not part of the canonical DAG-CBOR payload and is not required by PVL.

### 12.2 `CompiledInto`

    HolonType --CompiledInto--> EffectiveDescriptor

`CompiledInto` is the inverse navigation relationship.

It is non-definitional for the source `HolonType`; otherwise, every compilation event would change the `HolonType` and trigger an infinite feedback loop.

---

## 13. Validation Flow Using Stored EffectiveDescriptors

The peer-validation flow for an ordinary holon is:

    HolonNode being validated
      has effective_descriptor_hash
        |
        v
    Integrity retrieves EffectiveDescriptor carrier by EffectiveDescriptorHash
        |
        v
    bootstrap-validates the carrier
        |
        v
    verifies EffectiveDescriptorDigest == BLAKE3(EffectiveDescriptorDagCbor)
        |
        v
    decodes canonical DAG-CBOR payload
        |
        v
    PVL validates HolonNode against EffectiveDescriptor.pvl_surface

This avoids:

- live descriptor graph traversal
- inheritance resolution during validation
- SmartLink traversal to discover the descriptor surface
- cross-space descriptor dereferencing during validation
- ReferenceLayer cache dependence
- dynamic rule dispatch

while preserving:

- ordinary MAP holon representation
- graph-addressable provenance
- content-addressed validation surfaces
- Holochain peer-validation semantics
