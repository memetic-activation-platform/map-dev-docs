# MAP Descriptor-Independent PVL Design Spec — v0.4

## 1. Purpose

This document specifies the descriptor-independent subset of the MAP Peer Validation Language (PVL).

This PVL layer defines the fixed structural and resource-safety rules enforced by the Holochain Integrity Zome without resolving or interpreting:

- authored Descriptor Graphs
- `TypeDescriptor`s
- `EffectiveDescriptor`s
- descriptor caches
- type activation
- coordinator state
- TrustChannel agreements
- dynamic validation rules

The goal is to establish a small, deterministic, peer-reproducible validation floor that can be implemented immediately and remain valid regardless of whether MAP later adopts descriptor-dependent PVL.

The SmartLink structural rules in this specification validate the canonical storage contract defined in the [Storage Layer and SmartLink Design Specification](../guest/storage-layer-services/storage-layer-design-spec.md), which owns the version 1 tag byte format, the prepared-write boundary, and storage insertion identity. PVL validates that contract; it does not define a competing one.

This specification is intended to be prescriptive enough to support issue definition and implementation.

## 1.1 Trust Posture

This PVL layer is a deterministic hygiene floor, not an adversarial defense system.

MAP AgentSpaces are limited-membership communities. Every space is its own DHT, participation is governed by an Agreement (roles, accessible properties and relationships, Promise Weave entry), and misbehaving members are expected to be removed through governance rather than resisted indefinitely at the storage layer. Some space churn is an accepted cost of learning.

Descriptor-independent PVL therefore exists to:

- reject malformed or non-canonical data regardless of author intent
- bound resource consumption per entry, link, and validation call
- keep the committed graph structurally coherent across lifecycle, authorship, and provenance
- catch coordinator bugs before they pollute the DHT

It deliberately does not attempt:

- spam or flooding defense beyond per-object resource bounds
- per-agent rate limiting or write quotas
- role, agreement, or access enforcement
- semantic validation of any kind

Rate limiting and abuse response are governance and operational concerns. If experience shows that a storage-level control is needed, it can be added in a future DNA version as a deliberate migration.

---

# 2. Validation Guarantee

Descriptor-independent PVL proves:

> A submitted MAP entry or link is structurally well formed, uses supported native representations, remains within fixed resource bounds, and obeys the descriptor-independent create, update, delete, and structural provenance rules of the DNA.

It does not prove:

- that a property is declared by the holon’s type
- that a descriptor-required property is present
- that a value satisfies descriptor-defined constraints
- that a holon satisfies its descriptor-defined key rule
- that a relationship is declared by the source type
- that a relationship target has the required type
- that cardinality, ordering, exclusivity, or uniqueness constraints hold
- that a descriptor is activated
- that a TrustChannel or agreement permits an operation
- that an agent has authority to create, delete, or repair a relationship link

Those rules remain outside this specification. In particular, relationship-write authority is defined over MAP agents, AgentSpaces, agreements, roles, and security policy — not over Holochain signing keys — and is never inferred from substrate action authorship (Section 8.5).

---

# 3. Normative Limit Definition

## 3.1 Location of Limit Constants

All descriptor-independent PVL limits must be defined in one Integrity-safe module shared by the Integrity Zome and coordinator-side preflight validation.

Recommended location:

    shared_crates/shared_validation/src/pvl_limits.rs

or an equivalently low-gravity crate that:

- compiles to Integrity WASM
- has no coordinator dependencies
- has no ReferenceLayer dependencies
- has no descriptor dependencies
- exposes constants and pure validation helpers

The constants should be grouped into a versioned contract:

    pub struct PvlLimitsV1;

or:

    pub mod pvl_limits_v1;

The DNA must compile against one exact limit version.

Changing a limit changes Integrity semantics and therefore requires deliberate DNA versioning.

One constant is defined elsewhere and consumed here: the MAP SmartLink v1 tag ceiling `MAP_SMARTLINK_V1_MAX_BYTES` is part of version 1 wire-format validity and has its single authoritative definition alongside the Tag v1 codec (storage spec Section 9). `pvl_limits_v1` re-exports that definition rather than declaring a second constant, so storage packing and PVL enforcement cannot drift.

---

## 3.2 Serialization Basis

Limits involving entry, tag, or payload size must be measured against the canonical serialized byte representation presented to Integrity.

Do not estimate size from:

- Rust heap allocation
- character count
- JSON text
- debug formatting
- decoded object size

Use serialized bytes.

For UTF-8 strings and names, limits are measured in UTF-8 bytes, not Unicode scalar values or displayed characters.

---

## 3.3 Layering: Pure Core and Substrate Adapter

MAP core crates must not depend on Holochain. Descriptor-independent PVL is therefore split into two layers:

    holons_integrity (zome)          — validation callbacks only, no logic
      -> holons_guest_integrity      — substrate adapter (Holochain-aware)
           -> shared_validation      — pure PVL core (substrate-independent)
                -> core_types -> integrity_core_types

The pure core (`shared_validation`):

- holds the limit contract, `PvlViolation`, the error-code registry, and every check expressible over `integrity_core_types` data (`HolonNode`, `PropertyMap`, `BaseValue`, `LocalId`, and the decoded SmartLink storage types)
- validates hash-shaped identifiers structurally, by role and byte shape, without parsing Holochain types
- has no `hdi`, `hdk`, or `holo_hash` dependency

The canonical SmartLink Tag v1 codec and the storage-boundary types it operates on live in `core_types`: the SmartLink shape carries `HolonId` and external routing identity, which `core_types` owns, and `core_types` already depends on `integrity_core_types`, so a lower placement would create a dependency cycle. The [storage implementation plan](../guest/storage-layer-services/storage-layer-impl-plan.md) specifies the same `core_types` placement. PVL consumes that shared codec; it must not define a second decoder or a competing tag model.

The substrate adapter (`holons_guest_integrity`):

- maps Holochain ops and actions onto lifecycle checks
- parses exact Holochain hash types where they are available
- resolves deterministic dependencies (`must_get_*`) and enforces the dependency budget
- passes resolved, decoded data into pure core functions

Coordinator preflight invokes the pure core directly. The shared pure-core checks are therefore identical for Integrity and preflight by construction. Adapter-level behavior — exact Holochain hash parsing, op-to-lifecycle mapping, and `must_get_*` dependency resolution — executes only in Integrity, so preflight does not reproduce those failure modes. If preflight parity for adapter-level failures becomes necessary, add a coordinator preflight adapter that shares the substrate adapter's preparation path rather than duplicating its logic.

---

# 4. Proposed PVL v1 Limits

These are the proposed normative initial values.

They should be ratified against the fixture and benchmark process in Section 12 before the implementation issue is finalized.

| Constant | Proposed value |
|---|---:|
| `MAX_HOLON_NODE_BYTES` | 262,144 bytes |
| `MAX_PROPERTY_COUNT` | 256 |
| `MAX_PROPERTY_NAME_BYTES` | 128 bytes |
| `MAX_STRING_VALUE_BYTES` | 16,384 bytes |
| `MAX_ENUM_VALUE_BYTES` | 256 bytes |
| `MAX_CANONICAL_KEY_BYTES` | 256 bytes |
| `MAX_BYTES_VALUE_BYTES` | 131,072 bytes |
| `MAX_COLLECTION_ITEMS` | 1,024 |
| `MAX_VALUE_NESTING_DEPTH` | 2 |
| `MAP_SMARTLINK_V1_MAX_BYTES` | 512 bytes |
| `MAX_RELATIONSHIP_NAME_BYTES` | 128 bytes |
| `MAX_REMOTE_OBJECT_ID_BYTES` | 256 bytes |
| `MAX_VALIDATION_DEPENDENCIES_PER_OP` | 8 |

The design intent behind each value is defined below.

---

# 5. HolonNode Limits

## 5.1 Total HolonNode Entry Size

    MAX_HOLON_NODE_BYTES = 262_144

A serialized `HolonNode` must not exceed 256 KiB.

Rationale:

- ordinary MAP holons should contain structured semantic data, not bulk media
- large binary artifacts should be stored outside the DHT and referenced by digest or locator
- 256 KiB provides substantial room for rich property maps
- the limit bounds decoding, hashing, validation, gossip, storage, and traversal cost
- the limit is substantially below the substrate ceiling

Validation rule:

    serialized_holon_node_len <= MAX_HOLON_NODE_BYTES

Violation:

    PvlViolation::HolonNodeTooLarge {
        actual_bytes,
        max_bytes,
    }

---

## 5.2 Property Count

    MAX_PROPERTY_COUNT = 256

A `HolonNode.property_map` must contain no more than 256 entries.

Rationale:

- most domain holons should be far smaller
- unusually broad types remain possible
- validation effort is bounded independently of serialized size
- an attacker cannot create a pathological number of tiny properties

Validation rule:

    property_map.len() <= MAX_PROPERTY_COUNT

Violation:

    PvlViolation::TooManyProperties {
        actual_count,
        max_count,
    }

---

## 5.3 Property Name Length

    MAX_PROPERTY_NAME_BYTES = 128

Each property name must:

- be valid UTF-8
- be non-empty
- contain no leading or trailing whitespace
- contain no control characters
- encode to no more than 128 UTF-8 bytes

Property names should use the existing MAP canonical naming rules. PVL must not invent a competing normalization algorithm.

If the existing property-name type already guarantees part of this contract, PVL should rely on that constructor and separately enforce the byte limit.

Violations:

    PvlViolation::EmptyPropertyName

    PvlViolation::InvalidPropertyName {
        reason,
    }

    PvlViolation::PropertyNameTooLong {
        actual_bytes,
        max_bytes,
    }

---

# 6. Property Value Limits

## 6.1 String Values

    MAX_STRING_VALUE_BYTES = 16_384

A scalar string value must not exceed 16 KiB of UTF-8 data.

This applies to ordinary string values, descriptions, labels, and other unrestricted native string representations unless a narrower native limit applies.

Violation:

    PvlViolation::StringValueTooLarge {
        property_name,
        actual_bytes,
        max_bytes,
    }

Descriptor-defined string limits may be narrower, but they are outside descriptor-independent PVL.

---

## 6.2 Enum Values

    MAX_ENUM_VALUE_BYTES = 256

A native enum token must:

- be valid UTF-8
- be non-empty
- encode to no more than 256 bytes

This rule validates only the native representation.

It does not verify that the value is a member of a descriptor-defined enum.

Violations:

    PvlViolation::EmptyEnumValue {
        property_name,
    }

    PvlViolation::EnumValueTooLarge {
        property_name,
        actual_bytes,
        max_bytes,
    }

---

## 6.3 Integer Values

Integer values must decode into the exact integer representation supported by `PropertyValue`.

PVL must reject:

- unsupported integer widths
- overflowing conversions
- alternate serialized representations that decode ambiguously
- floating-point values presented where an integer is required by the native enum

No additional magnitude limit is required if the Rust type is already a fixed-width signed integer.

Violation:

    PvlViolation::UnsupportedNativeValue {
        property_name,
        value_kind,
    }

or:

    PvlViolation::MalformedPropertyValue {
        property_name,
        reason,
    }

---

## 6.4 Boolean Values

Boolean values must use the one canonical native Boolean representation.

Numeric or string substitutes such as:

    0
    1
    "true"
    "false"

must not be accepted as native Boolean values.

Violation:

    PvlViolation::MalformedPropertyValue {
        property_name,
        reason,
    }

---

## 6.5 Byte Values

    MAX_BYTES_VALUE_BYTES = 131_072

A single native bytes property must not exceed 128 KiB.

The total `HolonNode` limit still applies, so a holon cannot contain multiple maximum-sized byte values.

Bulk files, images, audio, video, model binaries, and other large artifacts must not be embedded directly in a `HolonNode`.

Violation:

    PvlViolation::BytesValueTooLarge {
        property_name,
        actual_bytes,
        max_bytes,
    }

---

## 6.6 Collection Values

Where native property arrays or collections are supported:

    MAX_COLLECTION_ITEMS = 1_024

A collection must not contain more than 1,024 elements.

Each element must independently satisfy its scalar or byte-value limit.

A collection must be homogeneous if the native `PropertyValue` variant declares a homogeneous array type.

PVL validates only native collection representation. It does not validate descriptor-defined minimum or maximum collection cardinality.

Violations:

    PvlViolation::CollectionTooLarge {
        property_name,
        actual_items,
        max_items,
    }

    PvlViolation::HeterogeneousCollection {
        property_name,
        expected_kind,
        actual_kind,
        item_index,
    }

Grounding note (v0.2): the current `PropertyValue` (`BaseValue`) has no collection variant, so these rules are satisfied by construction and require only regression tests until a collection representation is introduced.

---

## 6.7 Nesting Depth

    MAX_VALUE_NESTING_DEPTH = 2

PVL v1 permits only:

- depth 1: scalar value
- depth 2: collection of scalar values

Recursive arrays, arrays of arrays, arbitrary maps, and nested object values are not supported unless a future native `PropertyValue` representation explicitly adds them.

Violation:

    PvlViolation::ValueNestingTooDeep {
        property_name,
        actual_depth,
        max_depth,
    }

If the current `PropertyValue` model cannot represent nested values, this limit is satisfied by construction and requires only a regression test.

Grounding note (v0.2): verified — `BaseValue` is scalar-only, so value depth is fixed at 1 today. The depth-2 allowance is reserved headroom for a future collection representation.

---

## 6.8 Null and Option Semantics

PVL must distinguish:

- property absent from the map
- property present with a concrete value
- property present with `None`, if the current representation permits it

Descriptor-independent PVL does not enforce requiredness.

However, a present property with an invalid or unsupported `None` encoding must be rejected if the canonical `PropertyMap` contract does not recognize it.

If `BTreeMap<PropertyName, Option<PropertyValue>>` remains the native representation, then:

- `None` is structurally valid
- it does not count as a concrete value
- descriptor-dependent requiredness must later treat it as unsatisfied

No PVL error is generated solely because a property value is `None`, unless `None` is removed from the supported native representation.

Grounding note (v0.2): the current native representation is `BTreeMap<PropertyName, PropertyValue>` with no `Option`, so present-`None` is unrepresentable today. This section applies only if an optional-value representation is introduced.

---

# 7. Identifier Limits

## 7.1 Holochain Hash-Shaped Identifiers

Identifiers representing Holochain hashes must be validated using the existing canonical parser or validated wrapper type.

PVL must not rely only on a generic maximum-length check.

The validation should confirm:

- exact supported encoded length
- supported hash prefix/type
- checksum or internal hash encoding validity, where provided by the Holochain type
- correct role, where a role-specific wrapper exists

Examples include:

- `ActionHash`
- `EntryHash`
- `AgentPubKey`
- current ActionHash-shaped `LocalId`

Violation:

    PvlViolation::InvalidIdentifier {
        field_name,
        identifier_kind,
        reason,
    }

No separate arbitrary maximum should override the exact native hash shape.

Per §3.3, exact Holochain hash parsing happens in the substrate adapter. The pure core enforces role and byte shape — for example, the 39-byte ActionHash-shaped `LocalId` — without depending on `holo_hash`.

Grounding note (v0.2): `LocalId` is currently `LocalId(pub Vec<u8>)` with no validating constructor, so the shape check is new PVL logic in the pure core, not a delegation to an existing parser.

---

## 7.2 RemoteObjectId

    MAX_REMOTE_OBJECT_ID_BYTES = 256

Where a native structure permits an opaque `RemoteObjectId`, it must:

- be non-empty
- contain no more than 256 bytes

Its internal semantics are steward-defined and are not interpreted by PVL.

Violations:

    PvlViolation::EmptyIdentifier {
        field_name,
        identifier_kind,
    }

    PvlViolation::IdentifierTooLong {
        field_name,
        identifier_kind,
        actual_bytes,
        max_bytes,
    }

If `RemoteObjectId` is not present in an Integrity-visible structure, this rule is not invoked in the initial implementation.

---

# 8. SmartLink Limits

## 8.1 SmartLink Tag or Payload Size

    MAP_SMARTLINK_V1_MAX_BYTES = 512

The complete serialized version 1 SmartLink tag must not exceed 512 bytes.

The storage specification (Section 9) distinguishes three values. The Holochain `LinkTag` ceiling (1,024 bytes) is a substrate platform fact and is never duplicated as an independent MAP constant. The MAP SmartLink v1 ceiling (512 bytes) is normative wire-format validity: the shared codec rejects a larger version 1 tag as malformed, and PVL rejects it before persistence. The active packing budget (initially 512 bytes) is storage writer policy; it may be lowered without narrowing validity, so PVL accepts structurally valid version 1 tags up to the 512-byte ceiling regardless of the packing budget in force when a link was written.

The ceiling has one shared authoritative definition alongside the Tag v1 codec (Section 3.1); storage and PVL consume that definition rather than declaring separate limits. Changing the MAP ceiling is a format-evolution decision and a DNA-versioning event.

The limit includes all encoded Tag v1 fields:

- relationship-name and canonical-key prefix segments
- payload version and flags
- external routing identity (`OutboundProxyId`)
- occurrence identity
- the authoritative relationship-property section
- the cached target-property section

Violation:

    PvlViolation::SmartLinkTagTooLarge {
        actual_bytes,
        max_bytes,
    }

---

## 8.2 Relationship Identifier Length

    MAX_RELATIONSHIP_NAME_BYTES = 128

A relationship identifier must:

- be valid UTF-8
- be non-empty
- contain no NUL byte (it is a NUL-delimited tag prefix segment)
- contain no control characters
- have no leading or trailing whitespace
- encode to no more than 128 bytes

This rule validates only the identifier representation.

It does not verify that the relationship is declared by a descriptor.

Violations:

    PvlViolation::EmptyRelationshipName

    PvlViolation::InvalidRelationshipName {
        reason,
    }

    PvlViolation::RelationshipNameTooLong {
        actual_bytes,
        max_bytes,
    }

---

## 8.3 SmartLink Base and Target

A SmartLink base and target must use one of the exact reference forms supported by the native SmartLink format.

PVL must reject:

- unsupported hash kinds
- malformed encoded hashes
- missing required reference fields
- nonzero reserved payload-flag bits
- an external-target flag without the fixed-width 39-byte `OutboundProxyId`, or the reverse

Violations:

    PvlViolation::InvalidSmartLinkEndpoint {
        endpoint,
        reason,
    }

    PvlViolation::UnsupportedSmartLinkEndpointKind {
        endpoint,
        endpoint_kind,
    }

---

## 8.4 Canonical Key Values

    MAX_CANONICAL_KEY_BYTES = 256

Every SmartLink tag carries a structurally mandatory `CanonicalKey` segment (storage spec Sections 3.3 and 7.2). The segment must:

- be valid UTF-8
- contain no NUL byte (it is a NUL-delimited tag prefix segment)
- encode to no more than 256 UTF-8 bytes

An empty canonical key is valid and represents a keyless target type.

The coordination/reference layer computes the canonical key from the target's descriptor semantics before storage insertion. Descriptor-independent PVL validates only the native representation and the byte bound; it does not verify that the key was computed correctly for the target's type.

Rationale:

- the canonical key participates in the tag prefix grammar, so exact-key and key-prefix retrieval depend on its structural validity
- an unbounded key would let a holon that passes every entry-level limit still push its relationship tags toward `MAP_SMARTLINK_V1_MAX_BYTES` and squeeze out authoritative relationship properties
- the largest key in the current core-schema corpus is 96 bytes, giving 2.6× headroom

Violation:

    PvlViolation::CanonicalKeyTooLarge {
        actual_bytes,
        max_bytes,
    }

A canonical key containing invalid UTF-8 or a NUL byte is a malformed tag and maps to `MalformedSmartLink` with the appropriate reason.

---

## 8.5 Occurrence Identity and Provenance

Descriptor-independent PVL validates SmartLink structure and provenance, not relationship write authority.

Inverse pairing in the canonical storage model is carried by occurrence identity, not by a forward-link hash (storage spec Sections 3.1, 5.1, and 6):

- a declared link and the inverse realization of the same semantic occurrence share an `OccurrenceId` and have distinct `SmartLinkId` values
- for non-duplicate relationships, the semantic identity is source + target + relationship + absent occurrence ID
- `SmartLinkId` is the Holochain create-link action hash and is never encoded in the tag

PVL v1 validates the structural form of occurrence identity:

- when the occurrence payload flag is set, the tag must carry exactly 16 `OccurrenceId` bytes
- reserved payload-flag bits must be zero
- whether an occurrence ID is required or forbidden for a given relationship depends on its `AllowsDuplicates` policy, which is descriptor-defined and therefore outside descriptor-independent PVL

Tag version 1 carries no deterministic reference to the forward realization, and Integrity has no link-query surface, so cross-link correspondence between a declared link and its inverse is not verifiable in descriptor-independent PVL v1. If a future tag field deterministically references the forward realization, PVL may verify that the referenced action mirrors the inverse link's base, target, relationship identity, occurrence identity where present, and required structural fields.

PVL must not infer relationship-write authority from the Holochain action author of the source HolonNode. Holochain action authors are substrate-level signing agents, while MAP authority is defined over MAP agents, AgentSpaces, agreements, roles, and security policy. Whether a person, device-agent, organization, or delegated service may assert a relationship is not determined by `CreateLink.author == source_holon_action.author`.

Authorization to create, delete, or repair SmartLinks is outside descriptor-independent PVL unless a future DNA defines a fixed, integrity-local authorization rule.

---

# 9. Validation Dependency Limit

## 9.1 Maximum Dependency Requests

    MAX_VALIDATION_DEPENDENCIES_PER_OP = 8

A single validation path must request no more than eight deterministic dependencies.

The implementation should ordinarily require fewer:

| Operation | Expected dependencies |
|---|---:|
| Create `HolonNode` | 0 |
| Update `HolonNode` | 1 |
| Delete `HolonNode` | 1 |
| Create SmartLink (declared or inverse) | 0–2 |
| Delete SmartLink | 1 |

If a future tag field enables forward-reference provenance verification (Section 8.5), that check must fit within the same budget.

The dependency counter must be explicit in shared validation context or structurally guaranteed by the validation call graph.

PVL must not perform:

- open-ended relationship traversal
- recursive graph search
- “get all links”
- repeated retries inside validation
- dependency requests driven by unbounded user collections

If a required dependency is unavailable, validation returns `UnresolvedDependencies`.

That is not a `HolonError` and must not be reported as invalid data.

If validation logic would exceed the dependency budget, return:

    PvlViolation::ValidationDependencyLimitExceeded {
        requested,
        max,
    }

This represents an invalid or unsupported operation shape, not an unresolved dependency.

---

# 10. Structured PVL Violations

## 10.1 Recommended Error Model

Do not create a flat `HolonError` variant for every individual PVL rule.

Add one structured top-level variant:

    pub enum HolonError {
        ...
        PvlViolation(PvlViolation),
    }

Define a dedicated Integrity-safe enum:

    pub enum PvlViolation {
        ...
    }

This keeps the main `HolonError` stable while allowing PVL violations to remain:

- typed
- testable
- serializable
- mapped to deterministic callback messages
- reusable by coordinator preflight checks

---

## 10.2 Required `PvlViolation` Variants

### Malformed entry

    MalformedHolonNode {
        reason: PvlMalformedReason,
    }

Use when the entry cannot be decoded or violates the fixed native entry shape.

### Malformed link

    MalformedSmartLink {
        reason: PvlMalformedReason,
    }

Use when the tag or payload cannot be decoded or violates the fixed native SmartLink shape.

### Unsupported native representation

    UnsupportedNativeValue {
        property_name: Option<PropertyName>,
        value_kind: String,
    }

Use when data decodes into a representation not supported by PVL v1.

### Resource-limit violations

Use specific variants rather than one opaque limit error:

    HolonNodeTooLarge {
        actual_bytes: u32,
        max_bytes: u32,
    }

    TooManyProperties {
        actual_count: u16,
        max_count: u16,
    }

    PropertyNameTooLong {
        actual_bytes: u16,
        max_bytes: u16,
    }

    StringValueTooLarge {
        property_name: PropertyName,
        actual_bytes: u32,
        max_bytes: u32,
    }

    EnumValueTooLarge {
        property_name: PropertyName,
        actual_bytes: u16,
        max_bytes: u16,
    }

    BytesValueTooLarge {
        property_name: PropertyName,
        actual_bytes: u32,
        max_bytes: u32,
    }

    CanonicalKeyTooLarge {
        actual_bytes: u16,
        max_bytes: u16,
    }

    CollectionTooLarge {
        property_name: PropertyName,
        actual_items: u32,
        max_items: u32,
    }

    ValueNestingTooDeep {
        property_name: PropertyName,
        actual_depth: u8,
        max_depth: u8,
    }

    SmartLinkTagTooLarge {
        actual_bytes: u16,
        max_bytes: u16,
    }

    RelationshipNameTooLong {
        actual_bytes: u16,
        max_bytes: u16,
    }

    IdentifierTooLong {
        field_name: String,
        identifier_kind: String,
        actual_bytes: u16,
        max_bytes: u16,
    }

    ValidationDependencyLimitExceeded {
        requested: u8,
        max: u8,
    }

### Invalid update target

    InvalidUpdateTarget {
        expected_entry_kind: String,
        actual_entry_kind: String,
    }

Use when:

- the update's `original_action_address` does not reference a `Create` action containing a `HolonNode` — update-to-update chains are invalid in MAP's root-addressed lineage topology (KEA; storage plan SL2)
- the update changes native entry category
- an immutable native field changes

Storage SL2 removes `original_id` from the persisted `HolonNode` entry shape; lineage is carried by Holochain record metadata, not by an in-entry field. Lifecycle validation therefore enforces the root-addressed update contract, and strict enforcement activates in coordination with the SL2 write-path change (implementation plan PR 5).

Where useful, distinguish:

    ImmutableNativeFieldChanged {
        field_name: String,
    }

### Invalid delete target

    InvalidDeleteTarget {
        expected_target_kind: String,
        actual_target_kind: String,
    }

Use when a delete targets:

- the wrong entry type
- the wrong action type
- an unsupported revision form

### Link authorship and provenance

Removed in v0.3. Relationship-write authority is not a descriptor-independent PVL concern, and Tag v1 carries no forward-link reference to verify (Section 8.5). The `MAP-PVL-2110`–`2119` code block is reserved for forward-reference provenance validation if a future tag field introduces it.

---

## 10.3 Malformed-Reason Enum

To keep messages stable, use typed malformed reasons:

    pub enum PvlMalformedReason {
        DecodeFailed,
        MissingField(&'static str),
        InvalidDiscriminant(&'static str),
        InvalidUtf8(&'static str),
        InvalidLength(&'static str),
        InvalidFieldCombination,
        NonCanonicalEncoding,
    }

The shared Tag v1 codec defines its own typed decode errors. The substrate adapter and coordinator preflight must map them onto these reasons totally — every codec error variant has exactly one reason — so the deterministic message for a given malformed tag is identical everywhere. Section ordering and duplicate-name violations map to `NonCanonicalEncoding`; unknown versions, flags, sections, and value types map to `InvalidDiscriminant`; fixed-width mismatches (proxy id, occurrence id, boolean, integer) map to `InvalidLength`.

Avoid embedding arbitrary low-level deserializer strings in the deterministic peer-facing result.

The underlying low-level cause may be included in local debug logs, but not in the consensus-visible validation message.

---

# 11. Unresolved Dependencies

An unresolved dependency is not a `HolonError` and not a `PvlViolation`.

It maps directly to:

    ValidateCallbackResult::UnresolvedDependencies(...)

Examples:

- original action for an update is not yet available
- delete target is not yet available

The distinction is:

    dependency absent
      -> UnresolvedDependencies

    dependency present but wrong
      -> PvlViolation

This prevents temporarily unavailable valid data from being permanently rejected.

---

# 12. Limit Ratification Process

Before the constants become part of a production DNA, run a one-time ratification process.

## 12.1 Fixture Corpus

Measure:

- complete core-schema import
- largest core `TypeDescriptor`
- largest current `HolonNode`
- representative content holons
- representative query/request holons
- representative projection holons
- largest current SmartLink tag
- inverse-link tags
- adversarial near-limit fixtures

Record:

- serialized size
- property count
- maximum property-name size
- largest scalar
- largest bytes property
- collection counts
- validation dependency count
- validation execution time

---

## 12.2 Acceptance Rule

A proposed limit is acceptable when:

- all legitimate fixtures fit with at least 2× headroom
- no common workflow approaches more than 50% of the limit
- near-limit validation remains comfortably within the Integrity WASM execution budget
- an attacker cannot multiply the limit into unbounded dependency work
- the limit remains below substrate maxima

If legitimate fixtures exceed the proposed limit, raise only the affected limit and document the reason.

Do not increase all limits proportionally.

---

## 12.3 Benchmark Scenarios

At minimum benchmark:

1. minimal valid HolonNode
2. typical 20-property HolonNode
3. 256-property boundary HolonNode
4. 256 KiB boundary HolonNode
5. 128 KiB bytes property
6. 1,024-item collection
7. SmartLink tag at `MAP_SMARTLINK_V1_MAX_BYTES`
8. maximum dependency path
9. malformed input at maximum size
10. repeated invalid-link validation

The benchmark report should be committed with the implementation issue or linked from it.

---

## 12.4 Initial Measurements (2026-07)

Status: **initially measured, not ratified.**

These measurements predate the canonical Tag v1 format defined by the storage-layer specification. The entry-level measurements (HolonNode size, property counts, names, strings, keys) remain valid; they were taken in the larger update form with the 39-byte `original_id` entry field that Storage SL2 removes, so they slightly overstate future entry sizes. The tag measurements were taken against the former prolog encoding — their 512-byte budget column happens to match the since-ratified MAP v1 ceiling, but the byte counts understate Tag v1 sizes, which add a canonical-key prefix segment, optional 16-byte occurrence identity, TLV property sections, and cached target properties deliberately packed toward the budget.

Ratification requires re-measurement with the shared Tag v1 encoder, published as a committed, reproducible artifact: the measurement program, the corpus commit it ran against, and the generated report. The regression-suite milestone of the implementation plan owns that artifact.

A first measurement pass was run against the complete canonical core-schema import corpus (380 holons across 12 files), with each holon converted to its staged `PropertyMap` (including the `key` property) and serialized exactly as the Holochain `HolonNode` entry, in the larger update form (39-byte `original_id` present). SmartLink tag sizes were measured with a byte-exact replica of the then-current tag encoding across realistic shapes.

| Measurement | Corpus max | Proposed limit | Share of limit |
|---|---:|---:|---:|
| HolonNode entry bytes | 1,204 | 262,144 | 0.5% |
| Property count | 14 | 256 | 5.5% |
| Property name bytes | 31 | 128 | 24% |
| String value bytes | 719 | 16,384 | 4.4% |
| Key bytes | 96 | 256 | 37.5% |
| Relationship name bytes | 23 | 128 | 18% |
| Tag: local target, no smart properties | 33 | 512 | 6.4% |
| Tag: local target + key smart property | 140 | 512 | 27% |
| Tag: external target + key smart property | 180 | 512 | 35% |
| Tag: external + key + 39-byte forward-link reference | 190 | 512 | 37% |

Findings:

- Every proposed limit satisfies the Section 12.2 acceptance rule against the current corpus. No entry or tag exceeds 50% of its limit.
- The key bound (now the Section 8.4 `MAX_CANONICAL_KEY_BYTES`) was added as a result of this pass: keys feed SmartLink tags, and without a key bound a holon passing every per-property limit could still bloat its relationship tags.
- `MAX_HOLON_NODE_BYTES` is set by policy, not by measurement; the largest real holon uses 0.5% of it. The headroom is reserved for future content holons.
- The corpus contains schema descriptors only. Re-measurement must additionally cover representative content holons before the limits are frozen into a production DNA.

---

# 13. Reporting and Logging

## 13.1 Integrity Callback Result

A PVL violation must return:

    ValidateCallbackResult::Invalid(message)

The message should use a stable code and concise deterministic summary.

Recommended format:

    MAP-PVL-<code>: <summary>

Examples:

    MAP-PVL-1003: HolonNode exceeds 262144-byte limit

    MAP-PVL-1101: property count exceeds 256

    MAP-PVL-2201: SmartLink tag exceeds 512-byte limit

    MAP-PVL-2202: canonical key exceeds 256-byte limit

Do not include:

- entire property values
- full serialized entries
- secrets
- TrustChannel data
- arbitrary deserializer output
- nondeterministic debug representations

---

## 13.2 Error Code Registry

Define stable numeric or symbolic codes in:

    shared_crates/shared_validation/src/pvl_error_codes.rs

Suggested groups:

| Range | Category |
|---|---|
| `1000–1099` | HolonNode decoding and shape |
| `1100–1199` | Property and value limits |
| `1200–1299` | Identifier validation |
| `1300–1399` | Update and delete validation |
| `2000–2099` | SmartLink decoding and shape |
| `2100–2199` | Link identifiers and provenance |
| `2200–2299` | Link resource limits |
| `3000–3099` | Dependency-budget violations |

Codes should not be reused after release.

---

## 13.3 Coordinator-Side Reporting

When the same validation helpers are invoked before commit, map:

    PvlViolation
      ->
    HolonError::PvlViolation(...)

The coordinator may return the structured error to:

- command callers
- Dance callers
- import processes
- DAHN diagnostics
- developer tooling

The structured response may include:

- stable PVL code
- affected field or property name
- actual value
- allowed maximum
- remediation hint

Remediation hints are coordinator-side only and are not included in Integrity consensus messages.

---

## 13.4 Integrity Logging

Integrity validation should not emit warning or error logs for every rejected remote op.

Repeated peer validation could otherwise create a log-amplification attack.

Default behavior:

- return deterministic `Invalid` result
- no payload logging
- no routine `warn!` or `error!` call

Optional diagnostic behavior:

- emit `debug!` or `trace!` records behind a diagnostic feature or explicit runtime configuration
- include only:
    - PVL code
    - operation kind
    - action hash
    - entry or link type
- do not include property contents or private identifiers unnecessarily

Example:

    pvl_code=MAP-PVL-2104
    op=RegisterCreateLink
    action_hash=<hash>
    result=invalid

---

## 13.5 Validation Receipts and Persistent Error Holons

Descriptor-independent PVL failures must not automatically create:

- `ValidationResult` holons
- validation receipts
- conflict holons
- audit entries in the DHT

An invalid operation is not integrated and cannot safely trigger another DHT write from Integrity.

Persistent reporting, metrics, or governance escalation belongs to coordinator or operational tooling and is outside PVL.

---

# 14. Initial Error Code Proposal

| Code | `PvlViolation` |
|---|---|
| `MAP-PVL-1001` | `MalformedHolonNode` |
| `MAP-PVL-1002` | `UnsupportedNativeValue` |
| `MAP-PVL-1003` | `HolonNodeTooLarge` |
| `MAP-PVL-1101` | `TooManyProperties` |
| `MAP-PVL-1102` | `EmptyPropertyName` |
| `MAP-PVL-1103` | `InvalidPropertyName` |
| `MAP-PVL-1104` | `PropertyNameTooLong` |
| `MAP-PVL-1110` | `StringValueTooLarge` |
| `MAP-PVL-1111` | `EnumValueTooLarge` |
| `MAP-PVL-1112` | `BytesValueTooLarge` |
| `MAP-PVL-1113` | `CollectionTooLarge` |
| `MAP-PVL-1114` | `HeterogeneousCollection` |
| `MAP-PVL-1115` | `ValueNestingTooDeep` |
| `MAP-PVL-1201` | `InvalidIdentifier` |
| `MAP-PVL-1202` | `EmptyIdentifier` |
| `MAP-PVL-1203` | `IdentifierTooLong` |
| `MAP-PVL-1301` | `InvalidUpdateTarget` |
| `MAP-PVL-1302` | `ImmutableNativeFieldChanged` |
| `MAP-PVL-1303` | `InvalidDeleteTarget` |
| `MAP-PVL-2001` | `MalformedSmartLink` |
| `MAP-PVL-2002` | `InvalidSmartLinkEndpoint` |
| `MAP-PVL-2003` | `UnsupportedSmartLinkEndpointKind` |
| `MAP-PVL-2101` | `EmptyRelationshipName` |
| `MAP-PVL-2102` | `InvalidRelationshipName` |
| `MAP-PVL-2103` | `RelationshipNameTooLong` |
| `MAP-PVL-2201` | `SmartLinkTagTooLarge` |
| `MAP-PVL-2202` | `CanonicalKeyTooLarge` |
| `MAP-PVL-3001` | `ValidationDependencyLimitExceeded` |

This registry may be refined before implementation, but the category boundaries should remain stable.

Registry changes in v0.3, all before any release (the no-reuse rule begins at release):

- `1116`–`1118` removed along with the former key-property rules (superseded by the Section 8.4 canonical-key bound); the block may be reallocated.
- `2110`–`2119` reserved for forward-reference provenance validation if a future tag field introduces it (Section 8.5).

---

# 15. Open Decisions Required Before Issue Generation

Status of the ten pre-implementation decisions, updated for v0.3 after alignment with the storage-layer specification:

1. Confirm the proposed numeric limits against real serialized fixtures.
   **Initially measured** (Section 12.4). Entry-level limits pass the acceptance rule against the core-schema corpus. Tag measurements used the superseded encoding; ratification requires re-measurement with the shared Tag v1 encoder, published as a committed reproducible artifact, and coverage of representative content holons.
2. Confirm whether property collections currently exist in `PropertyValue`.
   **Resolved.** They do not: `PropertyValue = BaseValue` has five scalar variants. Section 6.6 is satisfied by construction.
3. Confirm whether nested values are representable at all.
   **Resolved.** They are not. Section 6.7 is satisfied by construction.
4. Confirm the exact canonical property-name validation already provided by `PropertyName`.
   **Resolved.** `PropertyName(pub MapString)` is a thin wrapper with no validating constructor; PVL implements the Section 5.3 rules itself. Fixtures must confirm that existing core-schema names pass them.
5. Confirm the current SmartLink tag fields and serialized size.
   **Superseded.** The tag format is now owned by the storage-layer specification (Tag v1, storage spec Sections 7–9). PVL validates that contract rather than documenting its own.
6. Confirm the fixed SmartLink attachment-authority rule.
   **Withdrawn (v0.3).** Attachment authority is not a descriptor-independent PVL concern: Holochain action authors are substrate signing agents, not MAP authority holders (Section 8.5). Authorization belongs to agreements, roles, and security policy above storage.
7. Confirm the current inverse-link provenance representation.
   **Resolved by the storage model.** Inverse pairing is occurrence identity — a declared link and its inverse share an `OccurrenceId` — not a forward-link reference. Cross-link correspondence verification is deferred unless a future tag field deterministically references the forward realization (Section 8.5).
8. Confirm which native fields are immutable across HolonNode updates.
   **Resolved by the knowledge-evolution and storage models.** Storage SL2 removes `original_id` from the persisted `HolonNode` entry shape; lineage is carried by Holochain record metadata (`Update.original_action_address` referencing the lineage-root `Create`). Lifecycle validation enforces the root-addressed update contract instead — an update is valid only against a `Create` containing a `HolonNode`, and update-to-update chains are invalid (Section 10.2) — and activates in coordination with the Storage SL2 write-path change.
9. Confirm the exact validated byte representation used by `LocalId`.
   **Resolved.** `LocalId(pub Vec<u8>)`, ActionHash-shaped (39 bytes), with no validating constructor today. Shape checking lives in the pure core; exact hash parsing lives in the substrate adapter (Sections 3.3 and 7.1).
10. Confirm the crate in which `PvlViolation`, limit constants, and error codes will live.
    **Resolved (updated v0.3).** Limits, `PvlViolation`, and error codes live in `shared_validation` (pure core). The Tag v1 codec and storage-boundary types live in `core_types` (dependency-cycle constraint, confirmed by the storage implementation plan). Both are consumed by `holons_guest_integrity` (substrate adapter) and coordinator preflight (Section 3.3).

The remaining open item is Tag v1 re-measurement (Section 12.4). The shared tag ceiling is ratified at 512 bytes (Section 8.1), and decision 8 is resolved by the root-addressed update contract; PR 5 lifecycle activation is sequenced against Storage SL2 rather than gated on an open design decision. Implementation issues can now enumerate exact tasks rather than categories of possible checks.