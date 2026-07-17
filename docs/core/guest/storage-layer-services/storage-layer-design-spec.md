# Storage Layer and SmartLink Design Specification (v1.0)

## 1. Purpose

This specification defines the MAP storage-layer contract used to retrieve
`HolonNode` records and persist or retrieve relationship occurrences as
`SmartLink` records. It also defines the canonical version 1 `SmartLink`
`LinkTag` format.

The storage layer is a generic, version-specific graph store. It exposes stored
graph facts and prefix-native access paths. It does not execute MAP queries or
construct reference-layer results.

The words **must**, **must not**, **should**, and **may** are normative.

## 2. Scope and Layer Boundary

### 2.1 Storage responsibilities

The storage layer understands:

- `HolonNode` records
- `SmartLink` records
- local source identifiers
- local and external target identifiers
- canonical relationship names
- canonical target keys
- authoritative relationship-occurrence properties
- optional cached target properties
- `SmartLink` tag encoding and prefix retrieval

It provides:

- exact `HolonNode` retrieval by `LocalId`
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

## 4. Storage Read Algebra

### 4.1 Operations

The minimal read surface is shown below in Rust-like pseudocode. These
signatures specify operation behavior and information shape; they do not
prescribe a Rust trait or module layout.

```text
fn get_holon(
    local_id: &LocalId,
) -> Result<Option<HolonNode>, HolonError>;

fn get_holons(
    local_ids: &[LocalId],
) -> Result<Vec<Option<HolonNode>>, HolonError>;

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

### 5.1 Insert operation

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

### 5.2 Delete operation

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

### 5.3 No replacement operation

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

## 9. Tag-Budget Packing

The complete encoded tag must not exceed the Holochain `LinkTag` limit,
currently 1024 bytes.

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
deterministic for the same prepared input and tag-size limit.

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

## 13. Normative Invariants

An implementation conforms to this specification when all of these invariants
hold:

1. Storage returns only `HolonNode` and `SmartLink` storage objects.
2. Every SmartLink has a local exact-version source and a local or external
   exact-version target.
3. Every tag contains the canonical-key segment, which may be empty.
4. Relationship and exact/prefix key lookup use the canonical prefix grammar.
5. Relationship properties and cached target properties remain physically and
   semantically separate.
6. Authoritative relationship properties are never dropped to satisfy the tag
   budget.
7. Optional target properties are whole-value, best-effort cache entries.
8. Typed property entries decode unambiguously and maps encode deterministically.
9. A duplicate-allowing occurrence has a 16-byte `OccurrenceId`; a
   non-duplicate relationship occurrence has none.
10. Declared and inverse realizations of one occurrence share `OccurrenceId`
    but have distinct `SmartLinkId` values.
11. Insertion is idempotent by semantic identity and authoritative content;
    optional cache differences never create a second live occurrence.
12. Expansion fails rather than silently omitting a malformed live SmartLink.
13. Expansion results are unordered and unhydrated.
14. Storage performs no general property filtering, ordering, limiting,
    projection, query planning, or query execution.

## 14. Related Design Sources

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
