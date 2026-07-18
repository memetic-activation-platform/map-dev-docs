# Storage Layer and SmartLink Design Specification (v1.0)

## 1. Purpose

This specification defines the MAP storage-layer contract used to persist and
retrieve versioned `HolonNode` records and persist or retrieve relationship
occurrences as `SmartLink` records. It also defines the canonical version 1
`SmartLink` `LinkTag` format.

The storage layer is a generic, version-specific graph store. It exposes stored
graph facts and prefix-native access paths. It does not execute MAP queries or
construct reference-layer results. Within the guest, it is the sole adapter to
Holochain persistence and retrieval host functions and persisted Holochain
representations.

The words **must**, **must not**, **should**, and **may** are normative.

## 2. Scope and Layer Boundary

### 2.1 Storage responsibilities

The storage layer understands:

- `HolonNode` records
- semantic root-create and new-version write requests
- runtime version metadata derived from enclosing Holochain records
- `SmartLink` records
- local source identifiers
- local and external target identifiers
- canonical relationship names
- canonical target keys
- authoritative relationship-occurrence properties
- optional cached target properties
- `SmartLink` tag encoding and prefix retrieval

It provides:

- semantic root and new-version `HolonNode` persistence
- exact stored-holon retrieval by `LocalId`, including `VersionMetadata`
- outgoing `SmartLink` expansion by source
- outgoing `SmartLink` expansion by relationship
- outgoing `SmartLink` expansion by relationship and canonical-key selector
- idempotent `SmartLink` insertion
- exact, idempotent `SmartLink` deletion

### 2.2 Responsibilities above storage

The coordination and reference layers are responsible for:

- descriptor resolution and validation
- canonical-key computation
- duplicate and cardinality policy
- occurrence-ID assignment
- inverse-relationship realization
- `SmartReference` construction
- `HolonCollection` construction
- target-holon hydration through the Holons Cache Manager
- property filtering other than canonical-key selection
- ordering, including interpretation of `SequencePosition`
- limiting, pagination, projection, and duplicate elimination
- query planning and `QueryExpression` execution

The storage layer must not return `HolonReference`, `SmartReference`,
`HolonCollection`, query-expression, or query-result objects.

Callers above storage identify MAP write intent and exact predecessor
`LocalId` values. They must not select Holochain action types, provide
`original_action_address`, retrieve Holochain records, or invoke Holochain host
functions. Those are storage-layer responsibilities.

### 2.3 Correctness-first scope

This contract prioritizes functional correctness over optimization. A planner
must not infer that an optional target property is present in a `SmartLink`.
Future query statistics, adaptive cache policy, and secondary SmartLink indexes
do not alter this initial contract.

## 3. Canonical Storage Types

The Rust declarations in this section are conceptual signatures. An
implementation may use equivalent newtypes and the existing `HolonError`, but
it must preserve the specified information and behavior.

### 3.1 Identifiers

`LocalId` identifies an exact persisted holon action. A `HolonId` is either a
local target or an external target whose routing identity includes an
`OutboundProxyId` and a target `LocalId`.

`SmartLinkId` is a newtype for the Holochain create-link action hash. It
identifies one exact persisted directional link. It is assigned by Holochain,
returned after insertion and decoding, and is not encoded in the `LinkTag`.

`OccurrenceId` is an opaque 128-bit value that identifies one semantic
relationship occurrence when the relationship allows duplicate targets. Its
canonical representation is exactly 16 bytes.

`SmartLinkId` and `OccurrenceId` are distinct:

- `OccurrenceId` is semantic occurrence identity.
- `SmartLinkId` is physical storage-action identity.
- A declared link and its inverse share an `OccurrenceId` but have different
  `SmartLinkId` values.
- Re-realizing an unchanged occurrence from a new source-holon version retains
  the `OccurrenceId` but creates new directional SmartLinks.

### 3.2 Relationship name

Each SmartLink stores the canonical `RelationshipName`, not a relationship
descriptor ID. Relationship names are unique within the source holon's
EffectiveDescriptor; they are not globally unique.

Coordination resolves and validates the name against that EffectiveDescriptor.
Storage is descriptor-unaware and treats the resulting validated UTF-8 value as
part of the tag prefix and insertion identity. The value must not contain NUL.

### 3.3 Canonical key

`CanonicalKey` is a validated UTF-8 value that contains no NUL byte. The
coordination/reference layer computes it according to the target's effective
descriptor.

The field is structurally mandatory in every `SmartLink`, but its value may be
empty. An empty value represents a target whose holon type is keyless.

### 3.4 Decoded SmartLink

The decoded storage object has this information shape:

```rust
struct SmartLink {
    smartlink_id: SmartLinkId,
    source_id: LocalId,
    target_id: HolonId,
    relationship_name: RelationshipName,
    canonical_key: CanonicalKey,
    occurrence_id: Option<OccurrenceId>,
    relationship_property_values: PropertyMap,
    target_property_values: PropertyMap,
}
```

`relationship_property_values` and `target_property_values` must remain
separate because they have different authority and fallback semantics.

### 3.5 Prepared SmartLink

The coordination layer supplies a fully prepared write request:

```rust
struct PreparedSmartLink {
    source_id: LocalId,
    target_id: HolonId,
    relationship_name: RelationshipName,
    canonical_key: CanonicalKey,
    occurrence_id: Option<OccurrenceId>,
    relationship_property_values: PropertyMap,
    target_property_cache_candidates: Vec<TargetPropertyCacheCandidate>,
}

struct TargetPropertyCacheCandidate {
    property_name: PropertyName,
    value: BaseValue,
}
```

`target_property_cache_candidates` is ordered from highest to lowest packing
priority. Each candidate contains one property name and typed scalar
`BaseValue`.

Before calling storage, coordination must:

- resolve and validate the relationship descriptor
- validate source and target compatibility
- enforce cardinality and duplicate policy
- compute the canonical key, including an empty key for a keyless type
- assign or preserve `OccurrenceId` as required
- initialize every required authoritative relationship property
- select and prioritize optional target-property cache candidates

Storage must not repeat or reinterpret those descriptor-driven decisions.

### 3.6 Stored holon and write intent

Storage keeps persisted semantic content and record-derived runtime metadata
distinct while returning them together:

```rust
struct VersionMetadata {
    version_id: LocalId,
    lineage_id: Option<LineageId>,
}

struct StoredHolonNode {
    holon_node: HolonNode,
    version_metadata: VersionMetadata,
}
```

`VersionMetadata` is derived from the enclosing Holochain record and is not
serialized into `HolonNode`.

The holon write contract expresses MAP intent without exposing Holochain action
types:

```rust
enum HolonWriteRequest {
    PublishRoot {
        holon_node: HolonNode,
    },
    PublishVersion {
        holon_node: HolonNode,
        predecessor_ids: Vec<LocalId>,
    },
}
```

Equivalent names and Rust layouts are permitted, but the request must preserve
this information and must not require callers to supply a Holochain `Action`,
`Record`, or `original_action_address`.

## 4. Storage Read Algebra

### 4.1 Operations

The minimal read surface is shown below in Rust-like pseudocode. These
signatures specify operation behavior and information shape; they do not
prescribe a Rust trait or module layout.

```text
fn get_holon(
    local_id: &LocalId,
) -> Result<Option<StoredHolonNode>, HolonError>;

fn get_holons(
    local_ids: &[LocalId],
) -> Result<Vec<Option<StoredHolonNode>>, HolonError>;

fn expand_all_from_source(
    source_id: &LocalId,
) -> Result<Vec<SmartLink>, HolonError>;

fn expand_from_source(
    source_id: &LocalId,
    relationship_name: &RelationshipName,
) -> Result<Vec<SmartLink>, HolonError>;

fn expand_from_source_by_key(
    source_id: &LocalId,
    relationship_name: &RelationshipName,
    key_match: &KeyMatch,
) -> Result<Vec<SmartLink>, HolonError>;
```

All expansion sources are local `LocalId` values. Coordination routes an
external source request to the appropriate HolonSpace before invoking this
storage interface. Expansion targets may be local or external.

### 4.2 Missing holons

For `get_holon`, `Ok(None)` means that storage did not find the requested
action; `Err` means retrieval failed.

`get_holons` must return exactly one positional result for each supplied ID. It
must preserve input order, cardinality, and duplicate IDs. This permits the
coordination layer to choose fail-fast, partial-result, or not-found semantics.

Every returned `StoredHolonNode` includes metadata derived from the exact
enclosing record. Storage must not return a bare `HolonNode` in a way that loses
exact-version or lineage identity.

### 4.3 Key selector

```rust
enum KeyMatch {
    Exact(CanonicalKey),
    StartsWith(CanonicalKeyPrefix),
}
```

The operations have these rules:

- `Exact("")` selects keyless targets.
- `StartsWith("")` is invalid because it is equivalent to relationship-only
  expansion.
- `Exact` includes the key-terminating NUL byte in the storage prefix.
- `StartsWith` omits the key-terminating NUL byte from the storage prefix.
- Matching is byte-prefix matching over validated canonical UTF-8 bytes.

### 4.4 Expansion result semantics

Expansion returns all matching live SmartLinks and preserves every distinct
`OccurrenceId`. Storage does not apply semantic ordering, filtering, limiting,
projection, or hydration. Holochain link-return order has no semantic meaning,
so the returned vector is unordered.

If expansion encounters a live SmartLink whose tag cannot be decoded or fails
canonical validation, the entire operation must fail with
`InvalidWireFormat`. The error must identify the offending `SmartLinkId`.
Storage must not silently omit the malformed graph fact or return an apparently
complete partial result.

### 4.5 Reverse navigation

Reverse navigation uses the separately persisted inverse SmartLink declared by
the relationship model. The initial storage algebra does not scan by target and
does not provide a generic reverse-link index. A future target-based access path
requires an explicit index design.

## 5. Storage Write Algebra

### 5.1 Holon publication

The semantic operation shape is:

```text
fn persist_holon(
    request: HolonWriteRequest,
) -> Result<StoredHolonNode, HolonError>;
```

For `PublishRoot`, storage invokes Holochain `create_entry`. For
`PublishVersion`, storage retrieves the exact predecessor records, resolves and
validates their shared lineage root, and invokes Holochain `update_entry`
against the root `Create`. Detailed lineage rules are defined in Section 15.

The returned `StoredHolonNode` is decoded from the resulting record. Storage
must not accept caller-supplied `VersionMetadata`; those values are always
derived from persisted Holochain facts.

### 5.2 SmartLink insert operation

The operation and outcome shape are shown in Rust-like pseudocode rather than
as a prescribed Rust API:

```text
fn put_smartlink(
    prepared: PreparedSmartLink,
) -> Result<PutSmartLinkOutcome, HolonError>;

enum PutSmartLinkOutcome {
    Inserted(SmartLinkId),
    AlreadyPresent(SmartLinkId),
    Conflict(SmartLinkId),
}
```

Storage must check for an existing identity on every insertion attempt.

The semantic insertion identity is:

```text
source_id
+ target_id
+ relationship_name
+ occurrence_id
```

`target_id` includes external routing identity when the target is external.
`occurrence_id` participates as an optional value: absence and presence are
different identities.

The outcome rules are:

- If no live SmartLink has the identity, storage inserts the prepared link and
  returns `Inserted` with its new `SmartLinkId`.
- If identity, canonical key, and authoritative relationship properties match,
  storage returns `AlreadyPresent` with the existing `SmartLinkId`.
- Differences in optional cached target-property maps do not affect
  `AlreadyPresent`.
- If identity matches but the canonical key or authoritative relationship
  properties differ, storage returns `Conflict` with the existing
  `SmartLinkId` and does not insert another link.
- Storage must never create two live SmartLinks with the same insertion
  identity.

Ignoring target-cache differences for idempotency is intentional. Cache-policy
changes apply prospectively to new SmartLinks. Retrofitting existing links would
require a separate maintenance operation that replaces, rather than duplicates,
the physical link; that operation is outside this initial contract.

### 5.3 SmartLink delete operation

The operation and outcome shape are shown in Rust-like pseudocode rather than
as a prescribed Rust API:

```text
fn delete_smartlink(
    smartlink_id: &SmartLinkId,
) -> Result<DeleteSmartLinkOutcome, HolonError>;

enum DeleteSmartLinkOutcome {
    Deleted,
    AlreadyAbsent,
}
```

Deletion is exact and idempotent. It deletes only the create-link action named
by `SmartLinkId`. A malformed ID or persistence failure is an error.

### 5.4 No SmartLink replacement operation

The initial storage contract has no in-place update or replacement operation.
Ordinary semantic relationship changes produce a new source `HolonNode` version
and new SmartLinks; links attached to the prior source version remain historical
facts. Exact deletion remains available for declared deletion policy,
correction, and recovery workflows.

## 6. Duplicate Occurrences

Occurrence identity is conditional on relationship duplicate policy:

- If `AllowsDuplicates` is false, `occurrence_id` must be absent. No occurrence
  ID is assigned or tracked; set-style insertion equivalence applies.
- If `AllowsDuplicates` is true, `occurrence_id` must be present and unique for
  each newly added occurrence.

Storage is descriptor-unaware and therefore does not decide which rule applies.
The coordination layer's `add_related_holons()` behavior must resolve the
descriptor and prepare the correct form before storage insertion.

For duplicate-allowing relationships, coordination must:

- check and assign occurrence identity when an occurrence is first inserted
- retain the ID while that occurrence survives transient, staged, committed,
  cloned, or newly versioned representations
- assign a new ID to a genuinely new occurrence, even when it has the same
  target
- reuse the ID on the declared and inverse SmartLinks
- reuse the ID on commit retries rather than regenerating it
- preserve occurrence-local properties with the occurrence

A suitable reference-layer implementation may use a non-holon runtime value:

```rust
struct RelationshipOccurrence {
    occurrence_id: Option<OccurrenceId>,
    target: HolonReference,
    relationship_property_values: PropertyMap,
}
```

This runtime shape is not part of the storage API; it illustrates the
information that must survive until `PreparedSmartLink` construction.

## 7. SmartLink Tag Version 1

### 7.1 Design goals

The format must provide:

- deterministic bytes for equivalent prepared content
- relationship and canonical-key prefix access paths
- exact local or external target reconstruction
- compact optional occurrence identity
- physically separate authoritative and cached property sections
- typed scalar property values
- strict structural validation

There is no backward-compatibility requirement for the previous prolog format.
Version 1 therefore contains no `LegacyProlog`, `PROLOG_SEPARATOR`, reference
type character, or `KeyMarker`.

### 7.2 Byte layout

The canonical byte order is:

| Field | Size | Encoding |
| --- | ---: | --- |
| `StableHeader` | 3 bytes | Existing `SMARTLINK_HEADER_BYTES`: `E2 82 B7` |
| `RelationshipName` | variable | Validated UTF-8, no NUL |
| relationship delimiter | 1 byte | `00` |
| `CanonicalKey` | variable | Validated UTF-8, no NUL; may be empty |
| key delimiter | 1 byte | `00` |
| `PayloadVersion` | 1 byte | `01` |
| `PayloadFlags` | 1 byte | Bit field defined below |
| `OutboundProxyId` | 0 or 39 bytes | Present for an external target |
| `OccurrenceId` | 0 or 16 bytes | Present when flagged |
| property sections | variable | TLV sections defined below |

The Holochain link target carries the target action hash. For an external
target, the tag's fixed-width `OutboundProxyId` supplies its HolonSpace routing
identity and the link target supplies its local action identity.

### 7.3 Payload flags

`PayloadFlags` version 1 uses:

| Bit | Meaning |
| ---: | --- |
| 0 | External target; a 39-byte `OutboundProxyId` follows |
| 1 | `OccurrenceId` is present |
| 2-7 | Reserved; must be zero |

A decoder must reject a version 1 tag whose reserved flag bits are nonzero.

### 7.4 Prefixes

The encoder constructs storage prefixes as follows:

```text
relationship:
  StableHeader | RelationshipName | 00

relationship + key prefix:
  StableHeader | RelationshipName | 00 | CanonicalKeyPrefix

relationship + exact key:
  StableHeader | RelationshipName | 00 | CanonicalKey | 00
```

The exact-key delimiter prevents `Exact("abc")` from also matching keys such as
`"abcd"`. For a keyless target, the exact-key prefix ends in two consecutive NUL
bytes after the relationship name.

### 7.5 Version handling

The initial decoder recognizes only `PayloadVersion = 1` and the section types
defined by this specification. An unknown version or section type is
`InvalidWireFormat`. Version 1 does not define ignorable extension sections.
Compatibility behavior must be designed only when another format is introduced.

## 8. Property Sections

### 8.1 Section framing

Each property section is encoded as:

```text
SectionType:u8 | SectionLength:u16-be | SectionPayload
```

Version 1 defines:

| Type | Meaning | Authority |
| ---: | --- | --- |
| `01` | Relationship property map | Authoritative occurrence data |
| `02` | Target property map | Optional immutable target-value cache |

Each section type may occur at most once. Non-empty sections must appear in
ascending type order. Empty maps are omitted to conserve tag space. A duplicate,
out-of-order, empty, truncated, or unknown section is `InvalidWireFormat`.

`SectionLength` is the exact byte length of `SectionPayload` and does not
include the type or length fields.

### 8.2 Property-entry framing

A section payload is a sequence of entries with no redundant entry count:

```text
PropertyNameLength:u16-be
PropertyName:utf8
ValueType:u8
ValueLength:u16-be
ValueBytes
```

The decoder reads entries until it reaches the exact end of the enclosing
section. It must reject an entry that crosses that boundary or leaves trailing
bytes.

Entries must be sorted by ascending canonical `PropertyName` UTF-8 bytes.
Duplicate property names are invalid. Because names and values are
length-framed, they do not inherit the NUL restriction used by the
prefix-critical relationship name and canonical key.

### 8.3 Typed scalar values

Version 1 supports the current scalar `BaseValue` variants:

| `ValueType` | `BaseValue` | Canonical `ValueBytes` |
| ---: | --- | --- |
| `01` | `StringValue` | UTF-8 bytes |
| `02` | `BooleanValue` | Exactly one byte: `00` false, `01` true |
| `03` | `IntegerValue` | Exactly 8 bytes, signed two's-complement big-endian |
| `04` | `EnumValue` | Canonical enum-value UTF-8 bytes |
| `05` | `BytesValue` | Raw bytes |

Unknown value types, invalid UTF-8, noncanonical lengths, and noncanonical
boolean bytes are `InvalidWireFormat`.

References, relationships, collections, and arbitrary nested values are not
property-section scalar values. A future scalar `BaseValue` variant requires a
new explicitly specified type tag before it can be encoded.

The existing `BaseValue::into_bytes()` output must not be used alone as this
wire representation. It omits the variant discriminator, so identical raw bytes
could otherwise decode as different MAP value types. The `ValueType` byte and
the canonical rules above make decoding unambiguous.

### 8.4 Deterministic map encoding

After property selection, storage must encode admitted entries in canonical
property-name order. Input map iteration order or cache-candidate priority order
must not affect the final bytes.

Canonical ordering serves two separate purposes:

- cache-candidate order determines which optional entries are admitted
- property-name order determines deterministic bytes for the admitted map

## 9. SmartLink Size Limits and Tag-Budget Packing

### 9.1 Distinct size limits

SmartLink storage distinguishes three size limits with different authority and
compatibility consequences:

| Limit | Version 1 value | Meaning | Enforced by |
| --- | ---: | --- | --- |
| Holochain `LinkTag` ceiling | 1024 bytes | Substrate maximum; MAP cannot persist a tag larger than this | Holochain |
| MAP SmartLink v1 ceiling | 512 bytes | Normative maximum size of a valid version 1 SmartLink tag | Shared codec and PVL Integrity validation |
| Active packing budget | 512 bytes | Maximum tag size the current storage writer may produce | Storage encoder |

The corresponding shared MAP definitions are conceptually:

```rust
pub const MAP_SMARTLINK_V1_MAX_BYTES: usize = 512;
pub const SMARTLINK_V1_PACKING_BUDGET_BYTES: usize =
    MAP_SMARTLINK_V1_MAX_BYTES;
```

Equivalent code names are permitted, but there must be only one definition of
the version 1 validity ceiling. The Holochain API is authoritative for its
platform ceiling; MAP must not duplicate that value as an independently
configurable policy limit.

The Holochain ceiling is a platform fact, not MAP's operative format limit.
The lower MAP ceiling bounds MAP resource consumption and leaves substrate
headroom for explicitly designed future formats. A future SmartLink format may
choose a different MAP ceiling, but doing so is a format-evolution decision
subject to Section 13.

The MAP SmartLink v1 ceiling is part of version 1 wire-format validity. The
codec must reject a version 1 tag larger than 512 bytes as
`InvalidWireFormat`, and PVL Integrity validation must reject it before
persistence. The ceiling must have one shared authoritative code definition
alongside the SmartLink codec; storage and PVL must consume that definition
rather than declaring independent numeric constants.

The active packing budget is writer policy and must not exceed either the MAP
ceiling for the current write version or the Holochain ceiling. It is initially
512 bytes but may be lowered when operational evidence warrants a smaller
memory or storage footprint. Lowering the active packing budget affects only
newly encoded SmartLinks. It must not make an existing version 1 tag invalid:
decoders and PVL continue to accept structurally valid version 1 tags up to the
512-byte MAP ceiling.

No coordinator, query planner, or caller may assume that an optional target
property will fit within the active packing budget. Optional cached properties
remain best-effort regardless of the configured budget.

### 9.2 Packing policy

Storage packs fields in this priority order:

1. Header, relationship name, canonical key, payload version, and flags.
2. Required routing and occurrence identity.
3. Every supplied authoritative relationship property.
4. Optional cached target properties.

If fields in the first three groups do not fit, insertion fails. Storage must
not truncate or omit mandatory content.

For optional target-property candidates, storage must:

1. Process candidates in coordination-supplied priority order.
2. Admit a complete property if its canonical encoded entry fits.
3. Skip a non-fitting property without truncating it.
4. Continue trying later candidates that may be smaller.
5. Canonically sort and encode the final admitted map.

Storage must reject duplicate candidate property names. Cache packing is
deterministic for the same prepared input and active packing budget.

## 10. Property Authority and SmartReference Handoff

### 10.1 Relationship properties

`relationship_property_values` describe the relationship occurrence itself.
They are authoritative and must never fall through to the target holon.

`SequencePosition` is the initial built-in example. The same target may have a
different sequence position in another relationship or in another occurrence
of a duplicate-allowing relationship.

### 10.2 Cached target properties

`target_property_values` are optional copies of properties on the exact target
holon action named by the SmartLink. They are best-effort covering-index data,
not independently definitional state.

Holochain actions and SmartLinks are immutable, and the SmartLink target is an
exact action hash. Therefore, a cached value copied from that target cannot
become stale relative to that target version. No cache invalidation or refresh
protocol is required.

Best-effort means only that a requested property may be absent because the tag
budget or cache policy omitted it. Neither storage nor a planner may assume its
presence.

### 10.3 Materialization without hydration

The coordination/reference layer materializes a decoded SmartLink as a
`SmartReference`; it does not project the SmartLink into a transient holon and
does not hydrate the target holon.

The intended accessor split is:

- `relationship_property_value(name)` reads only authoritative relationship
  occurrence properties.
- `property_value(name)` first checks cached target properties and, when absent,
  asks the Holons Cache Manager for the exact target holon and reads the value
  there.

The reference/coordinator representation must preserve `OccurrenceId` and
relationship properties for as long as occurrence identity or metadata is
needed. The exact runtime wrapper API is outside this storage specification.

## 11. Filtering, Ordering, and Limiting

Storage-native selection is limited to fields supported by the canonical
prefix grammar:

- exact local source identity
- exact relationship name
- exact canonical target key
- canonical target-key prefix

General property predicates operate above storage against reference-layer
abstractions. A `SmartReference` accessor may satisfy a target-property read
from its cache without retrieving the holon, but that optimization does not
turn general property filtering into a storage operation.

Sorting and limiting are also above this storage layer. They may be cited as
use cases for cached values but must not be implemented by the operations in
Section 4.

For a manually ordered relationship, storage returns unsorted SmartLinks with
authoritative `SequencePosition` values attached to their occurrences. The
coordinator/query layer decides when and how to apply that semantic ordering.

No planner decision may depend on optional target-property cache coverage.
Exact-key and key-prefix selection are safe because `CanonicalKey` is a
mandatory structural segment, including an empty segment for keyless types.

## 12. Version-Specific Identity

Every persisted `LocalId` and SmartLink endpoint is based on an exact Holochain
action hash. Source and target identities are therefore already
version-specific.

This storage algebra has no `VersionSelector` and no `LookupByVersionKey`.
Versioned keys used to disambiguate cloned staged or transient holons are
reference-layer concerns, not persisted SmartLink access paths.

## 13. SmartLink Format Evolution

SmartLink encoding is expected to evolve. This section defines the compatibility
boundary between persisted SmartLink bytes, storage behavior, and Holochain
integrity validation.

The current pre-version-1 development format is excluded from the supported
format lineage. There are no production deployments or persisted SmartLinks
that require migration into version 1.

### 13.1 Evolution categories

SmartLink evolution falls into three categories:

1. **Behavioral evolution** changes storage or coordination behavior without
   changing persisted bytes. Examples include new retrieval operations, cache
   candidate selection policy, lowering the active packing budget, or query
   planning behavior.
2. **Compatible encoding evolution** changes persisted content while preserving
   the stable access-path envelope and remaining acceptable to existing
   integrity rules.
3. **Incompatible encoding evolution** changes framing, interpretation, access
   paths, or integrity rules in a way existing validators cannot accept.

Behavioral evolution does not require a new SmartLink payload version.

Compatible encoding evolution is possible within a DNA only when its integrity
rules already permit the new representation and older supported readers can
handle it safely.

Incompatible encoding evolution requires a new DNA lineage or another explicit
migration boundary. It must not be introduced solely by changing coordinator
code.

### 13.2 Stable access-path envelope

The following prefix-critical envelope defines the SmartLink format family:

    StableHeader
    RelationshipName
    00
    CanonicalKey
    00

Compatible payload versions must preserve the meaning and encoding of this
envelope.

`PayloadVersion` occurs after the envelope so relationship, exact-key, and
key-prefix retrieval can locate supported SmartLinks without knowing their
payload version in advance. One prefix retrieval may therefore return links
with different supported payload versions.

A format that changes the stable header, relationship encoding, canonical-key
encoding, or delimiter placement is not merely a new payload version. It
introduces a new access path and requires an explicitly designed link type,
lookup strategy, or DNA migration.

### 13.3 Read-many, write-one policy

A storage implementation has:

- exactly one current write version
- a bounded set of supported read versions
- a bounded set of versions accepted by integrity validation

Storage must write only the current write version.

Storage may read multiple supported versions. Each supported decoder must
normalize its input into the canonical version-independent `SmartLink` shape
defined in Section 3.4.

Coordinator and reference-layer behavior must operate on that canonical
`SmartLink` representation. It must not depend on the payload version that
produced it.

An unsupported payload version is an error. Storage must not silently omit an
unsupported link or return an apparently complete partial expansion.

### 13.4 Version-independent semantic identity

Payload version is not part of SmartLink semantic insertion identity.

Semantic identity remains:

    source_id
    + target_id
    + relationship_name
    + occurrence_id

When an existing SmartLink uses an older supported payload version,
`put_smartlink` must compare its normalized canonical key and authoritative
relationship properties according to the ordinary insertion rules.

If semantic identity, canonical key, and authoritative relationship properties
match, storage returns `AlreadyPresent` even when the existing physical link
uses an older encoding.

A newer encoding must not create a second live relationship occurrence solely
because its payload bytes differ.

Optional cached target-property differences remain irrelevant to semantic
identity and idempotency across payload versions.

### 13.5 Physical identity and replacement

`SmartLinkId` identifies one physical Holochain create-link action. Re-encoding
a semantic relationship occurrence creates a new physical SmartLink with a new
`SmartLinkId`.

Normal `put_smartlink` does not replace an existing SmartLink merely because it
uses an older supported payload version.

Replacing an older physical encoding requires an explicit maintenance or
migration operation that:

1. decodes the existing SmartLink
2. constructs an equivalent canonical prepared representation
3. writes the current payload version
4. verifies the new physical SmartLink
5. deletes the old physical SmartLink when migration policy permits

Such a replacement operation is outside the initial storage contract defined
in Section 5.

A payload version must not be retired from a reader while reachable live
SmartLinks of that version remain in the data set served by that reader.

### 13.6 Integrity validation and DNA identity

SmartLink integrity validation is part of the Holochain integrity zome.
Integrity zomes and DNA modifiers determine the DNA hash and therefore the
network and data store. Coordinator zomes may be updated without changing that
identity, but changing integrity code creates a new DNA lineage.

Consequently, a payload version may be written into an existing DNA only when
that DNA's existing integrity rules accept it.

The set of payload versions accepted by integrity validation must include every
version that a writer can emit. A coordinator must not emit a payload version
that the active DNA cannot validate.

Changing integrity validation to recognize a previously rejected payload
version constitutes DNA evolution. Migration between those DNA lineages must
be designed explicitly.

See the Holochain documentation on
[application structure](https://developer.holochain.org/build/application-structure/)
and [integrity and coordinator zomes](https://developer.holochain.org/build/zomes/)
for the relationship between integrity code, coordinator code, and DNA
identity.

### 13.7 Version 1 compatibility policy

Version 1 is strict:

- only `PayloadVersion = 1` is recognized
- only the section types defined in Section 8 are recognized
- unknown section types are invalid
- unknown scalar value types are invalid
- reserved payload flag bits must be zero
- no section is defined as safely ignorable

Therefore, version 1 does not pre-authorize an unknown future payload version or
extension section.

Under these rules, a future incompatible version requires updated integrity
validation and consequently a new DNA lineage. This is intentional for the
initial design and favors strict validation over speculative forward
compatibility.

If same-DNA forward-compatible extensions are required later, their envelope,
critical-versus-ignorable semantics, integrity rules, and reader behavior must
be specified before such extensions are written. They must not be inferred from
the existence of TLV framing alone.

### 13.8 Migration between DNA lineages

Migration from an older DNA lineage to a newer lineage operates on canonical
storage objects rather than copying opaque tag bytes.

A migration process should:

1. retrieve and decode each supported source SmartLink
2. preserve semantic identity, including `OccurrenceId`
3. preserve authoritative relationship properties
4. reconstruct `PreparedSmartLink` for the destination storage contract
5. apply the destination's current cache-candidate and packing policy
6. insert the destination SmartLink using the destination's current write
   version
7. retain source-to-destination physical identity records when migration
   auditing requires them

`SmartLinkId` is not preserved across DNA migration because it identifies a
physical create-link action in one DNA. Semantic relationship identity is
preserved independently of that physical ID.

Optional cached target properties may differ after migration because they are
repacked according to destination policy and active packing budget.

### 13.9 Initial development cutover

The SmartLink representation that predates this specification is an
unversioned development format. It is not designated `PayloadVersion = 0` and
is not part of the supported production format lineage.

A conforming version 1 decoder must not accept the previous prolog format.

Incremental implementation may keep legacy and version 1 code paths in the
source tree or exercise them in separate test DNAs. That source-level
coexistence does not imply persisted-format interoperability.

Until version 1 behavior is complete, the existing reader, writer, and
validation path may remain active for development data. Version 1 may be
developed and tested through pure codec tests, storage mocks, or an isolated
version 1 test DNA.

Activation of version 1 must switch the following as one coordinated storage
boundary:

- SmartLink writer
- SmartLink readers
- SmartLink integrity validation
- development fixtures and persisted test data

Legacy and version 1 records must not coexist under the same
`LinkTypes::SmartLink` access path unless a temporary compatibility mechanism
has been explicitly designed and tested. No such compatibility mechanism is
part of this specification.

Because there is no production data to preserve, initial activation resets or
rebuilds development DNAs and fixtures rather than migrating the unversioned
development format.

### 13.10 Evolution invariants

SmartLink evolution must preserve these invariants:

1. Payload version never participates in semantic relationship identity.
2. All supported payload versions normalize into the same canonical
   `SmartLink` storage object.
3. Storage emits exactly one current write version.
4. Every emitted version is accepted by the active DNA's integrity rules.
5. Prefix-compatible versions preserve the stable access-path envelope.
6. Unsupported or malformed live SmartLinks cause expansion to fail rather
   than silently disappearing.
7. Physical re-encoding creates a new `SmartLinkId`.
8. An older physical encoding is not replaced implicitly by ordinary
   idempotent insertion.
9. A reader version is not retired while reachable live SmartLinks still
   require it.
10. The pre-version-1 development format creates no production compatibility
    or migration obligation.
11. Lowering the active packing budget affects only newly encoded SmartLinks
    and does not narrow the validity ceiling of a supported payload version.

## 14. Normative Invariants

An implementation conforms to this specification when all of these invariants
hold:

1. Storage returns only `StoredHolonNode` and `SmartLink` storage objects; it
   does not discard record-derived `VersionMetadata` from stored holon results.
2. Every SmartLink has a local exact-version source and a local or external
   exact-version target.
3. Every tag contains the canonical-key segment, which may be empty.
4. Every version 1 tag is at most 512 bytes.
5. The active packing budget does not exceed the current payload version's MAP
   ceiling or the Holochain platform ceiling.
6. Relationship and exact/prefix key lookup use the canonical prefix grammar.
7. Relationship properties and cached target properties remain physically and
   semantically separate.
8. Authoritative relationship properties are never dropped to satisfy the tag
   budget.
9. Optional target properties are whole-value, best-effort cache entries.
10. Typed property entries decode unambiguously and maps encode deterministically.
11. A duplicate-allowing occurrence has a 16-byte `OccurrenceId`; a
   non-duplicate relationship occurrence has none.
12. Declared and inverse realizations of one occurrence share `OccurrenceId`
    but have distinct `SmartLinkId` values.
13. Insertion is idempotent by semantic identity and authoritative content;
    optional cache differences never create a second live occurrence.
14. Expansion fails rather than silently omitting a malformed live SmartLink.
15. Expansion results are unordered and unhydrated.
16. Storage performs no general property filtering, ordering, limiting,
    projection, query planning, or query execution.
17. Storage encapsulates all Holochain persistence and retrieval operations and
    returns only abstract MAP storage types across its boundary.

## 15. Version Lineage and Version-Graph Topology

### 15.1 Separation of lineage identity and immediate ancestry

MAP uses two complementary mechanisms to represent version history:

- Holochain's `Update.original_action_address` identifies the root action of the
  version lineage.
- The definitional declared `Predecessor` relationship represents immediate
  ancestry within the version graph. Its non-definitional inverse, `Successor`,
  is materialized for reverse traversal.

These mechanisms have distinct meanings and must not be conflated:

| Mechanism | Meaning |
| --- | --- |
| `original_action_address` | Stable identity of the lineage to which an update belongs |
| `Predecessor` | Authoritative, definitional relationship to an immediate prior version from which a version was derived |
| `Successor` | Non-definitional materialized inverse identifying an immediate subsequent version |

A lineage is therefore identified by its root `Create` action, while its
branching and merging topology is represented by ordinary SmartLinks.

### 15.2 Lineage identity

`LineageId` is a conceptual newtype around the action hash of the root `Create`
action:

    struct LineageId(ActionHash);

`LineageId` is not stored as a field in `HolonNode`.

For a root version created by a `Create` action, its effective `LineageId` is
the action hash of that `Create`.

For a version created by an `Update` action, its effective `LineageId` is the
action hash held in `Update.original_action_address`.

Conceptually:

    fn effective_lineage_id(
        action: &SignedActionHashed,
    ) -> Result<LineageId, HolonError> {
        match action.action() {
            Action::Create(_) => LineageId(action.as_hash().clone()),
            Action::Update(update) => {
                LineageId(update.original_action_address.clone())
            }
            _ => return Err(HolonError::InvalidVersionAction),
        }
    }

Every MAP `Update` action must use `original_action_address` as a root pointer.
It must reference the lineage's root `Create` action, not the immediately
preceding `Update` action.

This produces a stable, constant-time lineage identity for every persisted
version without adding a lineage field to `HolonNode`.

### 15.3 Version-graph relationships

Immediate version ancestry is represented by the built-in relationship pair:

    Predecessor
        HasInverse Successor

Both directions are persisted as ordinary SmartLinks in accordance with the
inverse-relationship rules defined above this storage layer.

`Predecessor` is the definitional `DeclaredRelationship`. It points from a
version to each immediate version from which it was derived and is the
authoritative relationship fact. Adding, removing, or changing a predecessor
changes the source version's definition.

`Successor` is the non-definitional `InverseRelationship`. It is materialized
from `Predecessor` through the ordinary inverse-realization mechanism and points
from a version to each immediate version derived from it. It is not authored or
reconciled independently.

The version graph may branch:

    v1
     |
     v2
    /  \
v3a  v3b

This is represented as:

    v2  --Predecessor--> v1
    v3a --Predecessor--> v2
    v3b --Predecessor--> v2

with corresponding inverse `Successor` SmartLinks.

The version graph may also merge:

    v3a  v3b
      \  /
       v4

This is represented as:

    v4 --Predecessor--> v3a
    v4 --Predecessor--> v3b

with corresponding inverse links:

    v3a --Successor--> v4
    v3b --Successor--> v4

No separate `AdditionalPredecessor` relationship is required. A merge is
represented by multiple ordinary `Predecessor` occurrences.

### 15.4 Root, ordinary-update, branch, and merge forms

A lineage root has:

- a `Create` action
- an effective `LineageId` equal to its own action hash
- no `Predecessor` occurrences

An ordinary update has:

- an `Update` action
- `original_action_address` equal to the lineage root's `Create` action hash
- exactly one `Predecessor` occurrence

A branch is created when two or more versions identify the same immediate
predecessor:

    v3a --Predecessor--> v2
    v3b --Predecessor--> v2

A merge has:

- an `Update` action
- `original_action_address` equal to the shared lineage root's `Create` action
  hash
- two or more `Predecessor` occurrences

The number of predecessors therefore conveys version-graph structure:

| Predecessor count | Meaning |
| ---: | --- |
| `0` | Lineage root |
| `1` | Ordinary update |
| `2..*` | Merge |

Branching is not a special property of the successor version. It is observable
when one version has multiple materialized `Successor` occurrences.

### 15.5 Storage-layer treatment

`Predecessor` and `Successor` use the same `SmartLink` representation and
storage algebra as other declared and inverse relationship realizations.

The storage layer does not assign special traversal, indexing, or composite
realization behavior to these relationships. In particular, it does not:

- interpret `original_action_address` as an immediate predecessor
- synthesize a `Predecessor` result from Holochain action metadata
- synthesize a `Successor` result by scanning update actions
- introduce a separate reverse-update index
- combine native update metadata with SmartLinks during expansion
- classify retrieved graph topology as a root, branch, or merge query result
- construct a `Lineage` query result

Storage retrieves `Predecessor` and `Successor` occurrences through the
ordinary SmartLink expansion operations.

The storage layer derives the abstract `VersionMetadata` needed by higher
layers. Holochain `Record`, `Action`, `Create`, `Update`,
`original_action_address`, link records, and host-function calls remain
encapsulated within storage. Semantic lineage interpretation remains above the
generic SmartLink read and write algebra.

### 15.6 Storage-layer version-publication responsibilities

The storage write API accepts MAP-semantic intent rather than a caller-selected
Holochain action. Its conceptual request distinguishes:

- creation of a new root holon
- publication of a new version with one or more exact predecessor `LocalId`
  values

For root creation, storage must invoke Holochain `create_entry` and return
record-derived `VersionMetadata` whose `lineage_id` is absent.

For new-version publication, storage must:

- require at least one predecessor
- retrieve each predecessor's exact Holochain `Record`
- resolve each predecessor's effective lineage root
- reject predecessors that do not share one lineage root
- invoke Holochain `update_entry` with that root `Create` action as
  `original_action_address`
- return record-derived `VersionMetadata` for the new exact version

This translation is internal to storage. Callers do not select `Create` versus
`Update`, supply `original_action_address`, retrieve Holochain records, or
interpret Holochain action variants.

Before invoking storage, ordinary MAP Commit Processing remains responsible for
preparing the authoritative `Predecessor` occurrences and their required
`Successor` inverses through the general declared/inverse relationship
mechanism. Storage persists each prepared directional occurrence through the
ordinary SmartLink write operation. Version-lineage processing introduces no
lineage-specific link representation or inverse-realization path.

For every predecessor `p` of an update `v`, storage must enforce:

    effective_lineage_id(p) == effective_lineage_id(v)

For an `Update` action, storage must also enforce:

    effective_lineage_id(v) == LineageId(v.original_action_address)

and:

    v.original_action_address references the root Create action

The fact that Holochain action structures may permit another update topology
does not weaken this MAP invariant. MAP consistently interprets
`original_action_address` as the lineage-root pointer, and that Holochain field
does not cross the storage-layer boundary.

### 15.7 Authority and consistency

The persisted representations have distinct authority:

- `original_action_address` is authoritative for lineage membership.
- `Predecessor` is the authoritative definitional relationship for immediate
  version ancestry.
- `Successor` is the non-definitional materialized inverse of `Predecessor`. It
  supports reverse traversal but is not an independently authoritative lineage
  fact.

There is no requirement that `original_action_address` identify one of an
update's immediate predecessors. Except for the first update after the root, it
normally will not.

For example:

    v1: Create
        LineageId = action_hash(v1)

    v2: Update
        original_action_address = action_hash(v1)
        Predecessor = v1

    v3: Update
        original_action_address = action_hash(v1)
        Predecessor = v2

For `v3`, the root pointer and immediate predecessor intentionally differ:

    lineage root          = v1
    immediate predecessor = v2

This is not redundant conflicting state. The two values answer different
questions.

### 15.8 Query-layer interpretation

Above storage, a `Lineage` may be treated as a first-class query operand whose
identity is its `LineageId`.

Typical lineage operations may include:

- resolving the lineage of an exact holon version
- retrieving the root version
- retrieving immediate predecessors or successors
- finding lineage heads
- traversing complete version history
- identifying branches
- identifying merges
- finding common ancestors or merge bases

The exact `Lineage` abstraction and query operations are outside this storage
specification.

The storage contract provides the required persisted facts:

- exact-version and lineage identity through abstract `VersionMetadata` derived
  internally from `Create` and `Update.original_action_address`
- authoritative immediate version topology through `Predecessor` SmartLinks
- reverse traversal through materialized `Successor` SmartLinks

### 15.9 Version-lineage invariants

An implementation conforms to this version-lineage model when all of the
following invariants hold:

1. Every lineage root is persisted by a `Create` action.
2. The effective `LineageId` of a root is its own `Create` action hash.
3. Every version after the root is persisted by an `Update` action.
4. Every MAP `Update.original_action_address` references the lineage's root
   `Create` action.
5. `HolonNode` does not require a separately persisted `LineageId` field.
6. A lineage root has no `Predecessor` occurrence.
7. Every update has at least one `Predecessor` occurrence.
8. An ordinary update has exactly one `Predecessor`.
9. A merge has two or more `Predecessor` occurrences.
10. Every predecessor of an update has the same effective `LineageId` as the
    update.
11. `Predecessor` is a definitional `DeclaredRelationship` and is authoritative
    for immediate version ancestry.
12. Every `Predecessor` occurrence has a separately persisted inverse
    `Successor` occurrence realized by ordinary MAP Commit Processing.
13. `Successor` is a non-definitional `InverseRelationship` and is not an
    independently authoritative lineage fact.
14. `Predecessor` and `Successor` use the ordinary SmartLink storage contract.
15. No `AdditionalPredecessor` relationship or composite relationship
    realization is required.
16. Storage does not derive immediate ancestry from
    `original_action_address`.
17. Storage does not derive lineage membership from SmartLink traversal.
18. Lineage membership and immediate ancestry remain distinct persisted facts.

## 16. Related Design Sources

- [`HolonReference`](https://github.com/evomimic/map-holons/blob/main/shared_crates/holons_core/src/reference_layer/holon_reference.rs)
  defines the reference-layer state variants that remain above this storage
  boundary.
- [`SmartReference`](https://github.com/evomimic/map-holons/blob/main/shared_crates/holons_core/src/reference_layer/smart_reference.rs)
  defines the saved-reference read-through abstraction.
- The [SmartLink Manager design](https://github.com/evomimic/map-holons/wiki/SmartLink-Manager)
  provides the original SmartLink motivation and storage realization.
- The [Relationship Constraints Design Spec](../../descriptors/relationship-constraints-design-spec.md)
  defines `SequencePosition` as authoritative relationship-occurrence metadata
  and establishes the bounded exception for such data in SmartLinks.
- [Storage-Grounded Query Architecture](../../map-queries/storage-grounded-query-architecture.md)
  defines the higher-level query and coordinator context that consumes this
  storage contract.
