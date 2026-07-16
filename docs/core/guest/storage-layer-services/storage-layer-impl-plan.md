# Storage Layer and SmartLink Implementation Plan

## Purpose

This plan decomposes the
[Storage Layer and SmartLink Design Specification](storage-layer-design-spec.md)
into independently reviewable pull-request units for `map-holons`.

The plan is intentionally limited to the storage layer. It does not implement
coordinator or reference-layer policy.

There have been no production deployments and no persisted SmartLinks require
migration. The implementation may therefore make a clean cutover to the
version 1 format without a legacy decoder, dual-write behavior, or data
migration tooling.

## Layer Boundary

### In scope

The storage implementation owns:

- canonical storage-boundary types for `HolonNode`, `SmartLink`, and prepared
  SmartLink writes
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
- general property filtering, ordering, limiting, planning, or query execution

Storage accepts a fully prepared request and validates only its wire-level and
storage-level invariants. A separate coordinator implementation plan must cover
the policies and runtime structures needed to construct that request.

## Delivery Strategy

The new storage API should initially be additive. This allows each storage PR
to compile and be tested without changing coordinator behavior in the same PR.
The existing coordinator-facing SmartLink facade may remain temporarily, but
the new decoder must never accept the old tag format.

After a coordinator PR adopts the new storage contract, the final storage
cleanup PRs remove the temporary facade and obsolete persistence indexes.

| PR unit | Layer | Dependency | Ratchet |
| --- | --- | --- | --- |
| Storage SL1 - SmartLink V1 Storage Vertical Slice | Storage | None | Adds the complete non-duplicate v1 codec and SmartLink read/write algebra |
| Storage SL2 - Exact and Positional Holon Retrieval | Storage | None; may follow or run beside SL1 | Adds the canonical `HolonNode` read algebra |
| Storage SL3 - OccurrenceId Persistence Support | Storage | SL1 | Extends v1 storage identity and encoding to distinct duplicate occurrences |
| Storage SL4 - Legacy SmartLink Facade Retirement | Storage | Coordinator adoption of SL1-SL3 | Removes superseded SmartLink code paths |
| Storage SL5 - Obsolete Persistence Index Retirement | Storage | Coordinator no longer uses global get-all or revision lookup | Removes `AllHolonNodes` and `HolonNodeUpdates` |

## Storage SL1 - SmartLink V1 Storage Vertical Slice

### Goal

Land SmartLink encoding and its associated retrieval and mutation operations as
one coherent storage capability. This PR supports set-style relationships,
where `occurrence_id` is absent. SL3 adds the optional occurrence field without
changing the version number.

### Tasks

1. Add canonical storage-boundary types in an HDK-independent shared module
   available to both coordinator and integrity code:
   - `SmartLinkId`
   - `RelationshipName`
   - `CanonicalKey`
   - `CanonicalKeyPrefix`
   - `SmartLink`
   - `PreparedSmartLink`
   - `TargetPropertyCacheCandidate`
   - `KeyMatch`
   - `PutSmartLinkOutcome`
   - `DeleteSmartLinkOutcome`
2. Preserve separate `relationship_property_values` and
   `target_property_values` maps in every decoded `SmartLink`.
3. Implement a pure version 1 codec shared by coordinator-side persistence and
   integrity validation:
   - stable header, relationship name, and mandatory canonical-key segment
   - payload version and reserved-bit validation
   - local and external target routing data
   - typed relationship-property and target-property TLV sections
   - canonical property-name ordering
   - strict malformed-input rejection
4. Implement deterministic tag-budget packing:
   - mandatory prefix, routing, and authoritative fields must fit
   - optional target cache candidates are considered in supplied priority order
   - admitted target cache entries are encoded in canonical name order
   - properties are admitted or omitted whole, never truncated
   - duplicate cache-candidate names are rejected
5. Implement the SmartLink read surface:
   - `expand_all_from_source`
   - `expand_from_source`
   - `expand_from_source_by_key` with exact and starts-with matching
6. Construct query prefixes from the canonical grammar rather than by encoding
   and truncating a full tag.
7. Capture each Holochain create-link action hash as `SmartLinkId` during
   insertion and decoding.
8. Fail an entire expansion with `InvalidWireFormat` and the offending
   `SmartLinkId` when any matching live link is malformed.
9. Implement `put_smartlink` for an absent occurrence ID:
   - compare semantic identity by source, target, relationship, and absent
     occurrence
   - return `Inserted`, `AlreadyPresent`, or `Conflict`
   - ignore optional target-cache differences for idempotency
   - never create two live links with the same insertion identity
10. Implement exact, idempotent `delete_smartlink` by `SmartLinkId`.
11. Replace no-op SmartLink integrity checks with structural version 1
    validation using the shared decoder.
12. Keep the new API descriptor-unaware. It must not inspect relationship
    policy or infer any missing prepared field.

### Likely implementation areas

- `shared_crates/type_system/integrity_core_types/src/` for shared storage
  types and the pure codec
- `happ/crates/holons_guest/src/persistence_layer/` for Holochain storage
  operations
- `happ/zomes/integrity/holons_integrity/src/smartlink.rs` for validation
  entry points
- `shared_crates/shared_validation/src/validation_helpers.rs` if validation
  remains delegated through the shared helper layer

The current
`happ/crates/holons_guest/src/guest_shared_objects/smartlink_adapter.rs` may
remain as a temporary facade for existing callers, but new storage behavior
should live under `persistence_layer` rather than accumulate more coordination
concerns in `guest_shared_objects`.

### Verification

Pure codec tests must cover:

- deterministic round trips for local and external targets
- an empty canonical key for keyless targets
- exact-key and key-prefix byte construction, including empty-key exact match
- every supported scalar value type
- deterministic property ordering
- target cache admission, skipping, and canonical reordering
- duplicate cache-candidate rejection
- mandatory-content overflow
- malformed UTF-8, delimiters, lengths, flags, versions, sections, and values
- rejection of the former prolog format

Storage integration tests must cover:

- all three expansion operations
- unordered, unhydrated decoded results
- `Inserted`, `AlreadyPresent`, and `Conflict`
- cache-map differences returning `AlreadyPresent`
- exact deletion and repeated deletion
- malformed matching links failing the complete expansion

### Completion condition

The new storage API can create, retrieve, decode, and delete version 1
SmartLinks with no occurrence ID. It is directly testable without materializing
`SmartReference` or `HolonCollection` values. Existing coordinator behavior is
unchanged.

## Storage SL2 - Exact and Positional Holon Retrieval

### Goal

Land the `HolonNode` portion of the storage read algebra independently of
SmartLink and coordinator behavior.

### Tasks

1. Expose exact-version `get_holon(&LocalId)` returning
   `Result<Option<HolonNode>, HolonError>`.
2. Expose `get_holons(&[LocalId])` returning one positional result for every
   supplied ID.
3. Preserve input order, duplicate IDs, missing entries, and result
   cardinality in batch retrieval.
4. Distinguish not-found results from persistence and decoding failures.
5. Reuse the current exact-action fetch behavior while retiring the misleading
   `get_original_holon_node` name from the new API.
6. Do not add latest-version, revision-history, get-all, caching, or hydration
   semantics to these operations.

### Likely implementation areas

- `happ/crates/holons_guest/src/persistence_layer/holon_node.rs`
- persistence-layer exports and storage-focused tests

### Verification

- exact retrieval of an existing action
- `None` for a missing action
- positional batch behavior with existing, missing, and duplicate IDs
- error propagation for an invalid persisted entry

### Completion condition

The storage layer exposes the complete `HolonNode` read contract from Section 4
of the design spec without choosing coordinator missing-value policy.

## Storage SL3 - OccurrenceId Persistence Support

### Goal

Extend the v1 storage contract so multiple SmartLinks with the same source,
target, and relationship can remain distinct by supplied occurrence identity.
This PR implements persistence capability only. It does not implement
duplicate-aware collections or occurrence assignment.

### Tasks

1. Add the opaque, exactly 16-byte `OccurrenceId` newtype.
2. Add `Option<OccurrenceId>` to `SmartLink` and `PreparedSmartLink`.
3. Encode and decode the version 1 occurrence-present flag and fixed-width
   occurrence bytes.
4. Include optional occurrence identity in `put_smartlink` identity checks.
5. Preserve every distinct occurrence in all expansion results.
6. Keep storage descriptor-unaware:
   - storage does not resolve `AllowsDuplicates`
   - storage does not require or forbid an occurrence ID based on type policy
   - storage does not generate, preserve, or pair occurrence IDs
7. Continue using `SmartLinkId`, not `OccurrenceId`, for exact physical
   deletion.

### Verification

- round trip with and without an occurrence ID
- two otherwise-identical links with different occurrence IDs are both
  inserted and returned
- retrying the same occurrence returns `AlreadyPresent`
- conflicting authoritative content for the same occurrence returns `Conflict`
- a declared and inverse realization can carry the same occurrence ID while
  retaining distinct `SmartLinkId` values
- malformed occurrence flags or lengths fail strict decoding

### Completion condition

Storage can persist and distinguish duplicate occurrences when coordination
supplies valid IDs. Support for duplicate-allowing relationship collections is
not claimed until a separate coordinator PR assigns and preserves those IDs.

## Storage SL4 - Legacy SmartLink Facade Retirement

### Goal

Remove the superseded SmartLink implementation after the coordinator has
adopted the SL1-SL3 storage API.

### Entry condition

No coordinator call site constructs the old `SmartLink`, calls
`save_smartlink`, derives keys through `SmartLink::key`, or depends on
`SmartLink::to_pointer`.

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

## Coordinator Handoff Points

This plan deliberately stops at the following contracts:

1. Storage accepts `PreparedSmartLink`; coordination prepares it.
2. Storage returns decoded `SmartLink`; coordination may materialize it as a
   reference-layer abstraction.
3. Storage preserves optional `OccurrenceId`; coordination decides when it is
   required and carries it through relationship occurrences.
4. Storage returns optional `HolonNode` values positionally; coordination
   decides whether missing values fail, remain partial, or are reported.
5. Storage returns unordered links; coordination applies relationship ordering
   and all general filtering, sorting, and limiting.

These handoffs should be used as inputs to a separate coordinator-layer
implementation plan rather than expanded into this one.

