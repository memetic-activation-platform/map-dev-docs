# Storage Layer and SmartLink Implementation Plan

## Purpose

This plan decomposes the
[Storage Layer and SmartLink Design Specification](storage-layer-design-spec.md)
into independently reviewable pull-request units for `map-holons`.

The plan is intentionally limited to storage-layer services within the guest.
It does not implement query-coordinator or reference-layer policy. The storage
layer drives and encapsulates every Holochain persistence and retrieval host
operation; no storage-specific Holochain operation or representation may
escape the storage-layer boundary.

There have been no production deployments and no persisted SmartLinks require
migration. The implementation may therefore make a clean cutover to the
version 1 format without a legacy decoder, dual-write behavior, or data
migration tooling.

## Layer Boundary

### In scope

The storage implementation owns:

- canonical storage-boundary types for `HolonNode`, `SmartLink`, and prepared
  SmartLink writes
- runtime `VersionMetadata` derived from the Holochain `Record` enclosing a
  saved `HolonNode`
- translation from semantic holon-write requests to Holochain `Create` or
  root-addressed `Update`
- storage-side lineage-root resolution and publication validation
- all Holochain persistence and retrieval host-function invocation, record
  interpretation, and wire representation
- structural validation that a MAP `Update` references a root `Create`
- deterministic version 1 tag encoding and strict decoding
- Holochain link creation, exact deletion, and prefix retrieval
- exact and positional-batch `HolonNode` retrieval
- storage-level insertion identity and idempotency outcomes
- tag-budget enforcement and best-effort packing of supplied cache candidates
- structural integrity validation of persisted SmartLinks
- storage-level support for an optional `OccurrenceId`

### Out of scope

The following are coordinator or reference-layer responsibilities and must not
be implemented by a storage PR in this plan:

- resolving relationship descriptors or `AllowsDuplicates`
- computing or validating a canonical key from an EffectiveDescriptor
- assigning, preserving, or pairing occurrence IDs
- enforcing cardinality, source/target compatibility, or inverse semantics
- constructing relationship-occurrence collections
- choosing or prioritizing target-property cache candidates
- creating `SmartReference` or `HolonCollection` values
- hydrating holons through the Holons Cache Manager
- exposing Holochain `Action`, `Record`, `Create`, `Update`,
  `original_action_address`, or host-function concepts through any
  non-storage API
- general property filtering, ordering, limiting, planning, or query execution

Storage accepts semantic `HolonWriteRequest` values and fully prepared
SmartLink requests. It owns storage-level and Holochain-specific translation
and validation. A separate coordinator implementation plan must cover the
descriptor-driven policies and runtime structures needed to prepare SmartLink
requests and consume storage results.

## Delivery Strategy

The new storage API should initially be additive. This allows each storage PR
to compile and be tested without changing query-coordinator behavior in the
same PR.

The existing coordinator-facing SmartLink facade may remain temporarily, but
the new decoder must never accept the old tag format.

After a coordinator PR adopts the new storage contract, the final storage
cleanup PRs remove the temporary facade and obsolete persistence indexes.

Storage SL2 accepts semantic holon-write intent and internally selects the
root-addressed Holochain operation. No separate query-coordinator or guest
commit-processing PR is required to switch Holochain action types.

| PR unit | Lifecycle | Dev Points | Layer | Dependency | Ratchet |
| --- | --- | ---: | --- | --- | --- |
| Storage SL1 (part 1) - SmartLink Tag v1 Codec and Validation | Defined: Issue 590 | 5 | Storage | None; PVL prerequisite | Lands the codec, facade cutover, prefix grammar, and strict structural validation |
| Storage SL1 (part 2) - SmartLink v1 Persistence API | Planned | 5 | Storage | SL1 part 1 | Adds insertion outcomes, expansion operations, physical identity, and exact deletion |
| Storage SL2 - Version-Aware Holon Persistence | Planned | 8 | Storage | None; may proceed alongside SL1 | Adds record-aware reads and activates root-addressed native Holochain update persistence behind a semantic storage API |
| Storage SL3 - OccurrenceId Persistence Semantics | Planned | 2 | Storage | SL1 part 2 | Enables occurrence-aware storage identity and duplicate persistence using the v1 wire field from SL1 part 1 |
| Storage SL4 - Legacy SmartLink Facade Retirement | Planned | 3 | Storage | Guest call-site adoption of SL1 part 2 and SL3 | Removes superseded SmartLink code paths |
| Storage SL5 - Obsolete Persistence Index Retirement | Planned | 3 | Storage | SL2 and no remaining global get-all consumer | Removes `AllHolonNodes` and `HolonNodeUpdates` |

Dev Points estimate complete PR scope, not remaining effort. Issue 590's defined
estimate therefore remains `5` even though implementation is reported to be
nearly complete. Remaining effort should be assessed separately once a pull
request exposes its delivered code shape and outstanding checks.

### Active workstream alignment

[map-holons Issue 590](https://github.com/evomimic/map-holons/issues/590)
is already implementing SL1 part 1 and is assigned to Rashaan as a prerequisite
for the PVL SmartLink validation track. That work should complete under its
current identity rather than being renumbered or broadened to encompass the
remaining storage implementation.

The storage-layer workstream intended for Thomas begins with SL1 part 2 and SL2.
Those units are independent and may be sequenced according to availability:
SL1 part 2 completes the SmartLink storage API on top of Issue 590, while SL2
handles the separate `HolonNode` record and native-update path. Completion of
SL1 part 1 does not imply that Rashaan owns SL1 part 2, SL2, or the remainder
of this plan.

## Storage SL1 - SmartLink V1 Storage Vertical Slice

### Goal

Land SmartLink encoding and its associated retrieval and mutation operations as
one coherent storage capability. The work is split into two reviewable PRs
because the codec and strict integrity validation are also prerequisites for
the PVL track.

SL1 supports set-style persistence, where writers omit `occurrence_id`. Part 1
nevertheless implements the complete v1 wire grammar for the optional
occurrence field so SL3 does not require a format change.

### SL1 Part 1 - Tag v1 codec, facade cutover, and structural validation

Issue 590 owns this slice.

#### Tasks

1. Add the codec-facing storage types in the HDK-independent `core_types`
   module, including `SmartLinkId`, `CanonicalKey`, `CanonicalKeyPrefix`,
   `OccurrenceId`, `KeyMatch`, and encoder-input and decoder-output shapes.
2. Preserve separate `relationship_property_values` and
   `target_property_values` maps in every decoded SmartLink.
3. Implement the pure version 1 codec:
   - stable header, relationship name, and mandatory canonical-key segment
   - payload version, flags, and reserved-bit validation
   - local and external target routing data
   - optional 16-byte `OccurrenceId` wire field
   - typed relationship-property and target-property TLV sections
   - canonical property-name ordering
   - strict malformed-input rejection
4. Implement deterministic tag-budget packing:
   - mandatory prefix, routing, and authoritative fields must fit
   - optional target cache candidates are considered in supplied priority order
   - admitted target cache entries are encoded in canonical name order
   - properties are admitted or omitted whole, never truncated
   - duplicate cache-candidate names are rejected
5. Construct relationship, exact-key, and key-prefix bytes from the canonical
   grammar rather than truncating an encoded full tag.
6. Cut the existing `smartlink_adapter` facade over to Tag v1 so strict
   validation and current relationship writes change format together.
7. Preserve each decoded Holochain create-link action hash as `SmartLinkId`.
8. Replace no-op SmartLink integrity checks with structural version 1
   validation through the shared decoder.
9. Remove the superseded interim codec and legacy format constants.
10. Keep occurrence semantics out of this slice. The codec round-trips the
    optional field, but all SL1 writers emit it absent.

#### Verification

- deterministic local and external target round trips
- empty canonical key and all three prefix forms
- every supported scalar value type
- separate relationship and target property sections
- deterministic property ordering and malformed canonical-order rejection
- target-cache admission, skipping, and canonical reordering
- exact tag-budget boundaries and mandatory-content overflow
- malformed headers, UTF-8, delimiters, lengths, flags, sections, and values
- occurrence-field wire round trip while active writers omit it
- strict validator acceptance and rejection through the shared decoder
- regression coverage for existing forward and inverse relationship traversal

#### Completion condition

The Tag v1 codec is the single codec used by the temporary SmartLink facade and
integrity validation. Current relationship behavior uses the new format, but
the storage-owned insertion, expansion, and deletion API does not yet exist.

### SL1 Part 2 - SmartLink v1 persistence API

This is the first remaining SmartLink unit in the storage-layer workstream.

#### Tasks

1. Complete the storage-boundary API types, including `PreparedSmartLink`,
   `TargetPropertyCacheCandidate`, `PutSmartLinkOutcome`, and
   `DeleteSmartLinkOutcome`.
2. Implement the SmartLink read surface under `persistence_layer`:
   - `expand_all_from_source`
   - `expand_from_source`
   - `expand_from_source_by_key` with exact and starts-with matching
3. Fail an entire expansion with `InvalidWireFormat` and the offending
   `SmartLinkId` when any matching live link is malformed.
4. Implement `put_smartlink` for an absent occurrence ID:
   - compare semantic identity by source, target, relationship, and absent
     occurrence
   - return `Inserted`, `AlreadyPresent`, or `Conflict`
   - ignore optional target-cache differences for idempotency
   - never create two live links with the same insertion identity
5. Implement exact, idempotent `delete_smartlink` by `SmartLinkId`.
6. Keep the new API descriptor-unaware. It must not inspect relationship policy
   or infer any missing prepared field.
7. Leave the cut-over facade in place for existing callers until guest call-site
   adoption permits SL4 to remove it.

#### Likely implementation areas

- `shared_crates/type_system/core_types/src/` for the shared storage API types
- `happ/crates/holons_guest/src/persistence_layer/` for Holochain storage
  operations
- persistence-layer exports and storage-focused integration tests

#### Verification

- all three expansion operations
- unordered, unhydrated decoded results
- `Inserted`, `AlreadyPresent`, and `Conflict`
- cache-map differences returning `AlreadyPresent`
- exact deletion and repeated deletion
- malformed matching links failing the complete expansion

#### Completion condition

The storage API can create, retrieve, decode, and delete version 1 SmartLinks
with no occurrence ID. It is directly testable without materializing
`SmartReference` or `HolonCollection` values. Existing callers may continue
through the temporary facade.

## Storage SL2 - Version-Aware Holon Persistence

### Goal

Establish and activate the storage-layer `HolonNode` persistence path required
by the Knowledge Evolution Architecture independently of the SmartLink work in
SL1. A saved-holon read must preserve both the semantic `HolonNode` and runtime
`VersionMetadata` derived from its enclosing Holochain `Record`. A semantic
storage write request must be translated internally into a root `Create` or an
`Update` whose `original_action_address` identifies the lineage-root `Create`.

This PR closes the write gap end to end behind the storage boundary. Callers
identify MAP intent and exact predecessor versions; storage owns Holochain
action selection, record loading, lineage-root resolution, integrity-facing
representation, and host-function invocation.

### Current implementation gap

The current code has three storage-facing mismatches with the intended model:

- `ForUpdateNewVersion` ultimately calls `create_holon_node`, which persists
  every version with `create_entry`; Holochain therefore records each MAP
  version as an unrelated root `Create`.
- `try_from_record` retains the exact action hash but discards whether the
  enclosing action is a `Create` or `Update` and discards
  `Update.original_action_address`.
- `HolonNode.original_id` persists version-related state inside semantic entry
  content even though exact-version identity and lineage membership are facts
  of the enclosing record.

The staged object's existing `versioned_source_id` remains a semantic handle to
an immediate source version. It is supplied to storage as an exact MAP
identifier, not as Holochain action metadata.

### Storage-boundary information shape

Add the following information shape, using equivalent project newtypes and
naming where appropriate:

```rust
struct VersionMetadata {
    version_id: LocalId,
    lineage_id: Option<LineageId>,
}

struct StoredHolonNode {
    holon_node: HolonNode,
    version_metadata: VersionMetadata,
}

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

`StoredHolonNode` is a storage result, not a transient holon and not a
reference-layer abstraction. Higher layers may use it to construct or update
the existing `SavedHolon` runtime wrapper. `HolonWriteRequest` expresses MAP
intent without exposing Holochain action types.

### Tasks

1. Add `LineageId`, `VersionMetadata`, and a storage-boundary result that keeps
   the decoded `HolonNode` together with its record-derived metadata.
2. Decode supported records as follows:
   - `Create`: `version_id` is the record action hash and `lineage_id` is absent
   - `Update`: `version_id` is the record action hash and `lineage_id` contains
     `Update.original_action_address`
   - any action that cannot enclose a saved `HolonNode` fails explicitly
3. Expose exact-version `get_holon(&LocalId)` returning the storage-boundary
   result rather than discarding the enclosing action metadata.
4. Expose `get_holons(&[LocalId])` with one positional result for every
   supplied ID.
5. Preserve input order, duplicate IDs, missing entries, and result cardinality
   in batch retrieval. Distinguish not-found results from persistence and
   decoding failures.
6. Retire the misleading `get_original_holon_node` name from the new exact-read
   path. A `LocalId` identifies one exact persisted version, not necessarily a
   lineage root.
7. Add a semantic `persist_holon(HolonWriteRequest)` storage operation. Guest
   commit processing maps `ForCreate` and `ForUpdateNewVersion` to this request
   without selecting a Holochain action.
8. For `HolonWriteRequest::PublishRoot`, storage invokes Holochain
   `create_entry` and returns a `StoredHolonNode` whose `lineage_id` is absent.
9. For `HolonWriteRequest::PublishVersion`, require at least one exact
   predecessor ID, load every predecessor's exact record, and derive its
   lineage root:
    - a predecessor `Create` supplies its own action hash
    - a predecessor `Update` supplies its `original_action_address`
10. Reject a new-version request when its predecessors resolve to different
    lineage roots. Otherwise storage invokes Holochain `update_entry` against
    the shared root and returns record-derived `VersionMetadata`.
11. Keep relationship semantics above the raw SmartLink operations. Existing
    commit processing continues to prepare authoritative `Predecessor` and
    inverse `Successor` occurrences; storage persists those prepared
    directional links through the ordinary SmartLink API.
12. Strengthen integrity validation so a MAP `Update` is accepted only when
    `original_action_address` references a `Create` action containing a
    `HolonNode`. An update-to-update chain is invalid in MAP's list topology.
13. Remove `original_id` from the persisted `HolonNode` entry shape. Exact
    version identity and lineage membership come from `VersionMetadata`, while
    immediate ancestry comes from `Predecessor` SmartLinks. Any staging-only
    source identifier remains outside the persisted semantic entry.
14. Remove Holochain action interpretation from non-storage guest code. Signals
    and event construction consume abstract storage results and must not treat
    `Update.original_action_address` as an immediate predecessor.
15. Do not add latest-version, head-selection, revision-history, get-all,
    caching, hydration, or version-graph traversal semantics.

### Likely implementation areas

- `shared_crates/holons_core/src/core_shared_objects/holon/saved.rs` or an
  HDK-independent shared storage type module for `VersionMetadata`
- `shared_crates/type_system/integrity_core_types/src/holon_node_model.rs`
- `happ/crates/holons_guest_integrity/src/holon_node.rs`
- `happ/crates/holons_guest/src/persistence_layer/holon_node.rs`
- `happ/crates/holons_guest/src/persistence_layer/saved_holon_node.rs`
- `happ/crates/holons_guest/src/guest_shared_objects/commit_functions.rs`
- `happ/crates/holons_guest/src/guest_shared_objects/guest_holon_service.rs`
- `happ/zomes/integrity/holons_integrity/src/lib.rs`

### Verification

Storage-focused tests must cover:

- creating and retrieving a root with absent `lineage_id`
- creating two root-addressed updates and retrieving their distinct
  `version_id` values with the same `lineage_id`
- creating sibling updates against one root to prove storage permits branching
- rejection when an update operation is given another update as its root
- `ForCreate` producing a Holochain `Create`
- `ForUpdateNewVersion` producing a Holochain `Update` rooted at the lineage
  `Create`
- a second-generation update retaining the same root rather than pointing to
  its immediate predecessor
- mismatched predecessor lineages failing before publication
- authoritative `Predecessor` and inverse `Successor` continuing through the
  ordinary relationship commit path
- exact retrieval of an existing version
- `None` for a missing action
- positional batch behavior with existing, missing, and duplicate IDs
- explicit failure for an unsupported action or invalid persisted entry
- persisted `HolonNode` bytes contain no `original_id` or `LineageId`
- existing exact-version identity remains the enclosing record's action hash

Merge topology is not a distinct storage operation and is not claimed here. A
merge is established above storage by associating multiple authoritative
`Predecessor` occurrences with one root-addressed update.

### Completion condition

The storage layer persists semantic create intent as a root `Create`, persists
semantic new-version intent as a branch-capable update against the resolved
lineage root, and retrieves every version with complete record-derived
`VersionMetadata`. No Holochain action type, record metadata, or host operation
is exposed outside the storage-layer boundary.

## Storage SL3 - OccurrenceId Persistence Semantics

### Goal

Enable the v1 storage contract to persist multiple SmartLinks with the same
source, target, and relationship as distinct supplied occurrences. SL1 part 1
has already defined and tested the optional wire field; this PR activates its
storage identity semantics. It does not implement duplicate-aware collections
or occurrence assignment.

### Tasks

1. Permit storage writers to supply the optional `OccurrenceId` already
   represented by the v1 codec and storage-boundary types.
2. Include optional occurrence identity in `put_smartlink` identity checks.
3. Preserve every distinct occurrence in all expansion results.
4. Keep storage descriptor-unaware:
   - storage does not resolve `AllowsDuplicates`
   - storage does not require or forbid an occurrence ID based on type policy
   - storage does not generate, preserve, or pair occurrence IDs
5. Continue using `SmartLinkId`, not `OccurrenceId`, for exact physical
   deletion.

### Verification

- storage round trip with and without an occurrence ID
- two otherwise-identical links with different occurrence IDs are both
  inserted and returned
- retrying the same occurrence returns `AlreadyPresent`
- conflicting authoritative content for the same occurrence returns `Conflict`
- a declared and inverse realization can carry the same occurrence ID while
  retaining distinct `SmartLinkId` values
- malformed occurrence flags or lengths remain covered by SL1 part 1 codec
  tests

### Completion condition

Storage can persist and distinguish duplicate occurrences when coordination
supplies valid IDs. Support for duplicate-allowing relationship collections is
not claimed until a separate coordinator PR assigns and preserves those IDs.

## Storage SL4 - Legacy SmartLink Facade Retirement

### Goal

Remove the superseded SmartLink implementation after guest commit and retrieval
call sites have adopted the SL1 part 2 and SL3 storage APIs.

### Entry condition

No guest call site constructs the old `SmartLink`, calls `save_smartlink`,
derives keys through `SmartLink::key`, or depends on `SmartLink::to_pointer`.

### Tasks

1. Remove the old `LinkTagObject` and single `smart_property_values` model.
2. Remove the legacy encoder, decoder, prolog helper, delimiters, reference-type
   character markers, and obsolete constants other than the retained stable
   header and NUL delimiter.
3. Remove `SmartLink::key`, `SmartLink::to_pointer`, and `save_smartlink`.
4. Remove commented-out SmartLink CRUD code.
5. Remove legacy codec tests after ensuring their still-valid determinism and
   prefix assertions exist in v1 tests.
6. Move or remove the remaining `smartlink_adapter.rs` facade so storage has a
   single implementation path under `persistence_layer`.

### Completion condition

There is one SmartLink type, one version 1 codec, and one storage implementation
path. No runtime or test code recognizes the former format.

## Storage SL5 - Obsolete Persistence Index Retirement

### Goal

Remove persistence structures that are not part of the storage algebra once
their coordinator consumers have migrated.

### Entry conditions

- whole-space discovery no longer uses `AllHolonNodes`
- no caller uses latest-version or revision traversal through
  `HolonNodeUpdates`

The coordinator replacement for whole-space discovery is outside this plan.

### Tasks

1. Remove the unconditional `AllHolonNodes` link written by
   `create_holon_node`.
2. Remove `persistence_layer/all_holon_nodes.rs` and its exports.
3. Remove `fetch_links_to_all_holons` and other storage-side consumers of that
   index.
4. Remove `get_all_revisions_for_holon_node` and `get_latest_holon_node`.
5. Remove the `AllHolonNodes` and `HolonNodeUpdates` persistence link types and
   their validation branches.
6. Retain exact action retrieval, deletion/detail helpers, and bootstrap path
   lookup because they serve different persistence concerns.

### Verification

- creating a holon no longer creates a global index link
- exact holon reads and SmartLink expansion remain unaffected
- workspace search finds no live `AllHolonNodes` or `HolonNodeUpdates` usage
- persistence and integration suites pass without get-all or revision indexes

### Completion condition

The persistence layer contains only access paths with an active contract or a
separately documented persistence responsibility.

## Storage Boundary and Higher-Layer Handoffs

The storage layer is the sole Holochain persistence and retrieval adapter
within the guest. This plan uses the following contracts:

1. Shared/core code communicates semantic staged actions such as `ForCreate`
   and `ForUpdateNewVersion`; it does not select or name a Holochain action.
2. Guest commit processing translates staged state into `HolonWriteRequest` and
   supplies exact predecessor `LocalId` values; it does not retrieve or
   interpret Holochain records.
3. Storage selects `Create` or root-addressed `Update`, resolves and validates
   the lineage root, and invokes the corresponding Holochain host function.
4. Storage decodes Holochain records into `StoredHolonNode` and
   `VersionMetadata`; no Holochain `Record` or `Action` escapes storage.
5. Guest commit processing stages authoritative `Predecessor` occurrences and
   relies on ordinary inverse realization for `Successor`; low-level SmartLink
   storage treats both as ordinary directional links.
6. Storage accepts `PreparedSmartLink`; descriptor-aware MAP logic prepares its
   semantic fields without using Holochain types.
7. Storage returns decoded `SmartLink`; coordination may materialize it as a
   reference-layer abstraction.
8. Storage preserves optional `OccurrenceId`; coordination decides when it is
   required and carries it through relationship occurrences.
9. Storage returns optional stored-holon values positionally; coordination
   decides whether missing values fail, remain partial, or are reported.
10. Storage returns unordered links; coordination applies relationship ordering
   and all general filtering, sorting, and limiting.

The separate query-coordinator implementation plan begins with storage read
results and abstract MAP identifiers. It must cover reference materialization,
missing-value policy, ordering, filtering, limiting, and query execution. It
must not include Holochain Create/Update selection, record decoding, lineage
root encoding, or host-function invocation; those remain storage-layer
responsibilities implemented by SL2.
