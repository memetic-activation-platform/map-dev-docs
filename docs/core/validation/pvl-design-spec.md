# MAP Descriptor-Independent PVL Design Spec — v0.1

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

This specification is intended to be prescriptive enough to support issue definition and implementation.

---

# 2. Validation Guarantee

Descriptor-independent PVL proves:

> A submitted MAP entry or link is structurally well formed, uses supported native representations, remains within fixed resource bounds, and obeys the descriptor-independent create, update, delete, authorship, and provenance rules of the DNA.

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

Those rules remain outside this specification.

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
| `MAX_BYTES_VALUE_BYTES` | 131,072 bytes |
| `MAX_COLLECTION_ITEMS` | 1,024 |
| `MAX_VALUE_NESTING_DEPTH` | 2 |
| `MAX_SMART_LINK_TAG_BYTES` | 512 bytes |
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

    MAX_SMART_LINK_TAG_BYTES = 512

The complete serialized SmartLink tag or link payload must not exceed 512 bytes.

The limit includes all embedded fields, such as:

- relationship identifier
- ordering or sequence metadata
- inverse provenance
- forward-link reference
- reference-kind discriminants
- any fixed flags

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
- a reference discriminant inconsistent with its payload
- an external-reference structure missing either required component

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
| Create simple SmartLink | 0–2 |
| Create inverse SmartLink | 1–3 |
| Delete SmartLink | 1 |
| Validate provenance chain | bounded within remaining budget |

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

- the original action is not a HolonNode create/update
- the update changes native entry category
- an immutable native field changes

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

### Invalid link authorship

    InvalidLinkAuthorship {
        policy: String,
        base_author: Option<AgentPubKey>,
        link_author: AgentPubKey,
    }

The precise included fields should avoid leaking data unnecessarily into user-facing messages.

A narrower Integrity-facing representation may store only the policy code.

### Invalid inverse-link provenance

    InvalidInverseLinkProvenance {
        reason: InverseLinkProvenanceReason,
    }

Recommended reasons:

    pub enum InverseLinkProvenanceReason {
        MissingForwardLinkReference,
        ForwardLinkUnavailable,
        ReferencedActionIsNotCreateLink,
        ForwardLinkTypeMismatch,
        SourceTargetNotReversed,
        RelationshipMismatch,
        AuthorMismatch,
    }

An unavailable forward-link action must be handled as `UnresolvedDependencies`, not as `ForwardLinkUnavailable` invalidity.

`ForwardLinkUnavailable` should therefore be used only if the dependency was obtained but had an invalid form; otherwise omit that reason entirely.

---

## 10.3 Malformed-Reason Enum

To keep messages stable, use typed malformed reasons:

    pub enum PvlMalformedReason {
        DecodeFailed,
        MissingField(&'static str),
        InvalidDiscriminant(&'static str),
        InvalidUtf8(&'static str),
        InvalidFieldCombination,
        NonCanonicalEncoding,
    }

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
- referenced forward link for inverse provenance is not yet available

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
7. 512-byte SmartLink tag
8. maximum dependency path
9. malformed input at maximum size
10. repeated invalid-link validation

The benchmark report should be committed with the implementation issue or linked from it.

---

# 13. Reporting and Logging

## 13.1 Integrity Callback Result

A PVL violation must return:

    ValidateCallbackResult::Invalid(message)

The message should use a stable code and concise deterministic summary.

Recommended format:

    MAP-PVL-<code>: <summary>

Examples:

    MAP-PVL-1001: HolonNode exceeds 262144-byte limit

    MAP-PVL-1102: property count exceeds 256

    MAP-PVL-2003: SmartLink tag exceeds 512-byte limit

    MAP-PVL-2104: inverse-link source and target are not reversed

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
| `2100–2199` | Link authorship and provenance |
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
| `MAP-PVL-2110` | `InvalidLinkAuthorship` |
| `MAP-PVL-2111` | `InvalidInverseLinkProvenance` |
| `MAP-PVL-2201` | `SmartLinkTagTooLarge` |
| `MAP-PVL-3001` | `ValidationDependencyLimitExceeded` |

This registry may be refined before implementation, but the category boundaries should remain stable.

---

# 15. Open Decisions Required Before Issue Generation

The following must be resolved before the implementation issue can be considered ready:

1. Confirm the proposed numeric limits against real serialized fixtures.
2. Confirm whether property collections currently exist in `PropertyValue`.
3. Confirm whether nested values are representable at all.
4. Confirm the exact canonical property-name validation already provided by `PropertyName`.
5. Confirm the current SmartLink tag fields and serialized size.
6. Confirm the fixed SmartLink attachment-authority rule.
7. Confirm the current inverse-link provenance representation.
8. Confirm which native fields are immutable across HolonNode updates.
9. Confirm the exact validated byte representation used by `LocalId`.
10. Confirm the crate in which `PvlViolation`, limit constants, and error codes will live.

Once these ten decisions are grounded in the current code and fixtures, the GitHub enhancement issue can enumerate exact implementation tasks rather than describe categories of possible checks.