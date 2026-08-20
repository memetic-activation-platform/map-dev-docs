# Validation Implementation Plan v2.6 (Non-Descriptor-Dependent PVL)

## Purpose

This document defines an incremental implementation plan for the descriptor-independent Peer Validation Language (PVL) described in the PVL Design Specification (v0.7).

The goal is to deliver a small, deterministic validation kernel suitable for Holochain Integrity validation, implemented as plain pure functions within the layered architecture defined in Section 3.3 of the design spec:

    holons_integrity (zome)          — callback declaration, dispatch, and result projection only
      -> holons_guest_integrity      — substrate adapter (Holochain-aware)
           -> pvl_validation         — pure PVL core (substrate-independent)
                -> core_types / integrity_core_types — shared types and the Tag v1 codec

This plan intentionally excludes descriptor-aware validation.

### Changes from v2.5

- Refined PR 6's SmartLink ownership and error contract: the codec separates typed encode and decode errors and exposes typed structural positions; the single exhaustive decode-error-to-PVL mapper lives in `pvl_validation`; ActionHash-only endpoint validation and link delete-target validation route through the substrate adapter; create validation resolves no dependencies, while `StoreRecord::DeleteLink` uses `must_get_action` and does not re-decode the target tag.
- Allocated `InvalidLinkDeleteTarget` / `MAP-PVL-2004`, and clarified that decoded relationship and target-cache property maps reuse the existing PVL property validators.
- PR 6 establishes SmartLink adapter and Integrity routing. PR 8 builds on that path for coordinator preflight, infrastructure-link cleanup, callback-boundary cleanup, and broad integration coverage; it does not add a second decoder or SmartLink wiring path.
- Adopted design spec v0.7's structural dependency bound. Every descriptor-independent PVL v1 operation follows a fixed zero-or-one DHT-dependency path, pinned by exact-call-count adapter tests. PR 8 removes the unused limit constant, violation variant, SDK mirror member, fixtures, and `MAP-PVL-3001`; it does not add runtime dependency accounting.
- Rescoped PR 8 around the current repository state. PRs 2–6 already provide the substrate adapter, complete HolonNode lifecycle routing, SmartLink create/delete routing, and deterministic PVL result mapping. PR 8 no longer claims “remaining” adapter or lifecycle wiring.
- Located coordinator preflight at the canonical persistence write boundaries: `persist_holon` before `create_entry` / `update_entry`, and `put_smartlink` after one canonical Tag v1 encode but before `create_link`. Preflight maps pure-rule failures to `HolonError::PvlViolation` and submits the same validated bytes.
- Rejected an Integrity-parity claim for preflight. Preflight reuses shared pure rules over coordinator-constructible canonical inputs; arbitrary peer encodings, Holochain op routing, exact target-action classification, dependency resolution, and `UnresolvedDependencies` remain Integrity-only behavior.
- Classified `AllHolonNodes`, `HolonNodeUpdates`, and `LocalHolonSpace` as infrastructure links outside SmartLink Tag v1 PVL. PR 8 removes the scaffold-generated validators from `holons_integrity` but retains or replaces validation according to each link's active storage responsibility; active indexes are not left unvalidated.
- Recorded the landed Storage SL2 state: `PublishVersion` now authors a root-addressed Holochain `Update`, so normal MAP version publication exercises PR 5's lifecycle rule.

The older change sections below record the plan's evolution and may describe repository state that was true at the time. This v2.5 section is the current implementation direction where those notes conflict.

### Changes from v2.1

- Aligned with the [Storage Layer and SmartLink Design Specification](../guest/storage-layer-services/storage-layer-design-spec.md) v1.0 and its implementation plan, which landed after v2.1 was written.
- Removed PR 0 (tag codec relocation and format v2). The canonical SmartLink Tag v1 format, codec, and storage-boundary types are owned and delivered by the storage plan (Storage SL1/SL3); this plan consumes them as an external dependency. The in-flight PR 0 branch is being reworked to implement the SL1 codec.
- Withdrew the SmartLink authorship policy and forward-link-hash provenance (former PR 7 scope) per design spec v0.3 Section 8.5: relationship-write authority is not a descriptor-independent PVL concern, and Tag v1 carries no forward-link reference. Inverse pairing is occurrence identity, whose structural form is validated by the shared codec and PR 6.
- Reframed the key limit as the `MAX_CANONICAL_KEY_BYTES` bound on the mandatory Tag v1 canonical-key segment (design spec Section 8.4); removed the key-property rule from PR 3.
- Adopted the shared tag budget: `MAX_SMART_LINK_TAG_BYTES = 1_024`, matching the Holochain `LinkTag` ceiling and the storage packing budget (provisional; a narrower shared bound is under discussion).
- Weakened the preflight claim: shared pure-core checks are identical for Integrity and preflight by construction; adapter-level checks are Integrity-only unless a preflight adapter is added (PR 8 decision).
- Downgraded limit ratification to "initially measured"; PR 9 now owns re-measurement with the Tag v1 encoder and a committed reproducible measurement artifact.

### Changes from v2.2

- Adopted the ratified shared tag ceiling: `MAP_SMARTLINK_V1_MAX_BYTES = 512` (the MAP SmartLink v1 validity ceiling), defined alongside the Tag v1 codec and consumed by `pvl_limits_v1`. The Holochain 1,024-byte `LinkTag` ceiling is a platform fact never duplicated as a MAP constant, and the initial 512-byte packing budget is storage writer policy that may be lowered without narrowing validity (storage spec Section 9).
- Replaced the PR 5 decision-8 gate. The Knowledge Evolution Architecture and Storage SL2 remove `original_id` from the persisted `HolonNode` entry shape and make updates root-addressed: `Update.original_action_address` references the lineage-root `Create`, and update-to-update chains are invalid. PR 5 enforces that contract and is sequenced against Storage SL2.
- Recorded confirmed ownership: issue #590 (Storage SL1 part 1) completes under its current identity as the shared codec foundation; the remaining storage workstream (SL1 part 2, SL2 onward) proceeds independently in the storage plan.

### Changes from v2.3

- Reshaped PR 2 into a vertical slice. It delivers the pure-core HolonNode envelope rules **and** the initial substrate-adapter entry point, the Integrity wiring for the HolonNode entry arms, the explicit violation-to-`Invalid` mapping, and one negative conductor test. PR 8 no longer claims that initial wiring; it generalizes the seam PR 2 establishes (remaining op-to-lifecycle mapping, dependency-budget accounting, coordinator preflight, broad sweetest coverage).
- Recorded two PR 2 implementation decisions. Entry size is measured on the raw app-entry bytes and enforced **before** typed deserialization and before any dependency request, so an oversized entry never buys decode or `must_get_*` work. Canonical property-map shape is enforced by re-encoding the decoded model and byte-comparing against the stored entry bytes (`MalformedHolonNode { NonCanonicalEncoding }`): serde map decoding is last-wins for duplicate keys, so a post-decode check alone would be empty, and the byte comparison doubles as the guest/preflight serialization-parity guarantee.
- Corrected the rejection-semantics rationale. Holochain (0.6 line) converts `Guest`/`Serialize`/`Deserialize` wasm errors returned from validate callbacks into definitive `ValidateCallbackResult::Invalid`; there is no indeterminacy defect. The explicit mapping exists so the consensus-visible message is exactly the `MAP-PVL-<code>` contract rather than a substrate-wrapped error string.
- Recorded SL2 timing. Storage SL2 is not expected to land within this plan's horizon. PR 2 therefore validates the current entry shape (`original_id` present) and pins model/entry serialization parity with tests that SL2 must revisit when it removes `original_id` and activates root-addressed updates. Commit processing keeps `ForUpdateNewVersion` on `create_entry` for now, with breadcrumb comments marking the anticipated SL2 switch; the Holochain `Update`-op validation arms are wired by PR 2 but remain unexercised by MAP writes until SL2. PR 5 remains gated on SL2.

### Changes from v2.4

- **Removed PR 5's Storage SL2 entry criterion.** The gate rested on the claim that early activation "would reject every current update." That is incorrect against the current code: `ForUpdateNewVersion` calls `create_entry`, and no MAP write path calls `update_entry` anywhere in the workspace, so PVL sees no Holochain `Update` to reject. PR 5 lands now as proactive hardening against peer-authored `Update` operations, and Storage SL2 inherits an already-enforced contract. This supersedes the v2.3 note that "PR 5 remains gated on SL2."
- Recorded the corresponding storage-plan change: SL2 task 12 verifies and reuses PR 5's validation instead of implementing a second check. The "wired once" requirement is unchanged; only the order is.
- Removed the "immutable native fields" deliverable from PR 5. Decision 8 resolved lifecycle validation to the root-addressed contract, the current entry shape carries no cross-version invariant, and SL2 removes the only candidate field. `ImmutableNativeFieldChanged` / `MAP-PVL-1302` is reserved and unused (design spec Section 10.2).
- Enumerated PR 5's operation arms. Update semantics reach validation through three flattened arms (`StoreEntry::UpdateEntry`, `RegisterUpdate::Entry`, `StoreRecord::UpdateEntry`) and delete semantics through two (`RegisterDelete`, `StoreRecord::DeleteEntry`). All five are wired, following PR 2's precedent of routing every HolonNode arm through one entry point.
- Recorded the lifecycle pure-core/adapter seam (design spec Section 3.3) and the dependency-resolution form (Section 9.2): a substrate-free lifecycle-facts type owned by `pvl_validation`, `must_get_valid_record` for the update target, `must_get_action` for the delete target, and no deserialization of the target entry in either case.
- Recorded PR 5's coverage model. The update rule cannot be exercised through a conductor — no MAP path authors an `Update` — and `HolonNode` is this DNA's only app entry type, so negative delete targets are equally unconstructible in-DNA. Negative coverage is unit-level over the pure facts type and synthetic ops; the conductor test is a positive regression that legitimate deletes still commit.
- Recorded the `InvalidUpdateTarget` field rename (design spec Section 10.2) and its fan-out to the hand-maintained TypeScript SDK mirror.

---

# External Dependencies

## Design Spec

- `pvl-design-spec.md` v0.7 is the normative source for limits, violations, error codes, and rules.
- Decision 8 is resolved: lifecycle validation enforces the root-addressed update contract established by the Knowledge Evolution Architecture (spec Section 10.2), and carries no sequencing constraint against Storage SL2.
- The shared tag ceiling (spec Section 8.1) is ratified: `MAP_SMARTLINK_V1_MAX_BYTES = 512`, defined alongside the Tag v1 codec and consumed — not re-declared — by `pvl_limits_v1`.

## Storage Layer Plan

The [storage implementation plan](../guest/storage-layer-services/storage-layer-impl-plan.md) delivers, as external prerequisites to this plan:

- **Storage SL1** — the pure Tag v1 codec and storage-boundary types (`SmartLink`, `PreparedSmartLink`, `CanonicalKey`, `KeyMatch`, outcome enums) in an HDK-independent shared module, plus the storage read/write algebra and structural integrity validation through the shared decoder. SL1 is delivered in two slices: part 1 (map-holons issue #590) lands the codec — including the 16-byte `OccurrenceId` byte round-trip, since the occurrence flag is a defined v1 flag a strict decoder must accept — plus the facade cutover and Integrity structural validation; part 2 lands the storage persistence API (`put_smartlink` outcomes, `KeyMatch` expansion, exact deletion).
- **Storage SL3** — occurrence identity participation and persistence semantics (the occurrence byte encoding itself ships with the SL1 part 1 codec).
- **Storage SL2 (landed)** — version-aware holon persistence now authors root-addressed native Holochain updates and has removed `original_id` from the persisted entry shape. `PublishVersion` exercises the Create/Update contract PR 5 already wired; SL2 did not add a parallel lifecycle validator.

Division of labor: the storage plan owns the codec, the byte format, and storage-level idempotency; this plan owns the PVL limit contract, the violation and error-code model, entry-level validation, lifecycle validation, and the Integrity/preflight wiring that layers PVL semantics over the shared decoder. SL1's structural decode validation at Integrity entry points and PR 6/PR 8 of this plan must be coordinated so the decode path is wired once, not twice.

## Holochain

Requires:

- Integrity Zome validation callbacks
- `pvl_validation`, `core_types`, and `integrity_core_types` usable from Integrity WASM
- Existing HolonNode model and the SL1 SmartLink storage model

## Validation Framework

None. This plan deliberately does not consume the layered validation framework defined in the Validation Implementation Plan. See "Relationship to the Validation Implementation Plan" below.

---

# Milestone 0 — Storage Tag v1 Codec (External Prerequisite)

## Outcome

The canonical SmartLink Tag v1 codec exists in Integrity-reachable shared code, delivered by Storage SL1.

This is not a PVL PR. It is tracked here because the SmartLink track (PR 6 onward) cannot start without it. The former PVL PR 0 branch is being reworked in place as SL1 part 1 (map-holons issue #590) to implement the codec against the storage spec's byte layout; its strict-decode discipline, canonical-ordering enforcement, typed scalar handling, and test suite carry over. The storage plan confirms this slice completes under issue #590's current identity; the remaining storage workstream (SL1 part 2 onward) proceeds independently on top of it.

---

# Milestone 1 — PVL Foundation

## Outcome

The fixed infrastructure required by descriptor-independent PVL.

---

## PR 1 — Limits, Version Contract, and Error Model

**Estimate:** 3 pts

### Goal

Introduce the normative versioned limit contract and structured PVL violations.

### Deliverables

- `pvl_limits_v1` in `pvl_validation`: versioned PVL-owned limit constants (including `MAX_CANONICAL_KEY_BYTES`) plus pure serialized-byte measurement helpers; consumes `MAP_SMARTLINK_V1_MAX_BYTES` from the codec (the SmartLink tag-size check itself lands in PR 6)
- the violation contract in `integrity_core_types/src/pvl_error.rs`, beside `HolonError` (dependency-cycle constraint, design spec Section 15 decision 10): `PvlViolation`, `PvlMalformedReason`, and the owned serializable `PvlField` enum (exhaustive for the v1 grammars, externally tagged, no `String` catch-all) per design spec Sections 10.2–10.3 (no authorship or forward-reference provenance variants), re-exported from `pvl_validation` for the pure-core import path; a serialization round-trip test covering each materially distinct payload shape pins the wire form the SDK mirror depends on
- error-code registry per design spec Section 14 (`1116` `EmptyEnumValue`, `1117` `MalformedPropertyValue`, `1118` free; `2110`–`2119` reserved; `2202` `CanonicalKeyTooLarge`), co-located with `PvlViolation` as a deterministic per-variant code
- `HolonError::PvlViolation(PvlViolation)` and its exhaustive-match fan-out: a `HolonErrorKind` arm and `From<&HolonError>` mapping, and a `From<HolonError> for ResponseStatusCode` classification (validation failures are a client/validation class, not `ServerError`)
- the `HolonErrorWire` TypeScript SDK mirror (wire variant, type guard, fixture, and test) — the SDK enumerates `HolonError` variants by hand and Rust compilation will not flag an omission; if not delivered here, deferred with a tracked follow-up (see CI note below)

### Dependencies

- none

### Exit Criteria

- the PVL limit contract (`pvl_validation`) and the violation contract (`integrity_core_types`) exist in their designated Integrity-safe crates, re-exported so PVL code has one import path
- Integrity and coordinator preflight compile against the same contract
- adding the new `HolonError` variant leaves host, hApp, and TypeScript SDK builds green

### Note: `HolonError` wire drift

`HolonErrorWire` in the TypeScript SDK is a hand-maintained mirror of the Rust `HolonError` enum; a Rust build does not detect a missing or stale TS variant. This PR adds the first PVL variant, so it is the point at which the drift risk becomes concrete. Whether the SDK mirror ships in this PR or a tracked follow-up, the durable fix is a CI guard that fails when the Rust and TypeScript variant sets diverge (generation from a single source, or a cross-checking test). Track this as a standalone CI task rather than expanding PR 1's scope indefinitely.

---

# Milestone 2 — HolonNode Structural Validation

## Outcome

Descriptor-independent validation of native HolonNode structure.

---

## PR 2 — HolonNode Envelope Validation (Vertical Slice)

**Estimate:** 4 pts

### Goal

Validate intrinsic HolonNode structure end to end: pure-core rules, the initial substrate-adapter entry point, and Integrity wiring for the HolonNode entry arms.

### Deliverables

- pure-core envelope rules in `pvl_validation` returning `Result<(), PvlViolation>`, applied in deterministic order — raw size, then decode/canonical encoding, then property count:
    - serialized size vs `MAX_HOLON_NODE_BYTES` → `HolonNodeTooLarge`
    - property count vs `MAX_PROPERTY_COUNT` → `TooManyProperties`
    - canonical-encoding mismatch → `MalformedHolonNode { NonCanonicalEncoding }`
- raw pre-decode size enforcement: the adapter measures the raw app-entry bytes and rejects oversized entries before typed deserialization and before any dependency request (in the StoreRecord update arm, before its existing `must_get_valid_record`)
- canonical-encoding check: re-encode the decoded model and byte-compare with the stored entry bytes; a mismatch (duplicate map keys, non-canonical ordering or integer widths, ignored fields) is rejected. This is what makes the shape rule non-empty — serde map decoding is last-wins for duplicate keys — and it doubles as the guest/preflight serialization-parity guarantee
- one substrate-adapter envelope entry point in `holons_guest_integrity`; all five HolonNode dispatch arms in `holons_integrity` route through it, eliminating the current double validation in the StoreRecord update arm (create and update share the same envelope rules in this PR)
- explicit violation mapping: `Err(PvlViolation)` → `ValidateCallbackResult::Invalid(violation.to_string())` in the `MAP-PVL-<code>` Display format, replacing reliance on Holochain's implicit Guest-error-to-`Invalid` conversion whose message wraps substrate formatting
- saturating width conversions into violation payloads (`u32` byte lengths, `u16` counts) per the design-spec field-width convention
- one negative conductor (sweetest) test proving an envelope violation reaches the author as a rejection carrying the exact `MAP-PVL` code
- serialization-parity tests that Storage SL2 preserves when switching version publication to the now-landed root-addressed `update_entry` path

### Dependencies

- PR 1

### Exit Criteria

- malformed or oversized HolonNodes rejected with deterministic `MAP-PVL-<code>` messages; the current core-schema corpus accepted
- oversized entries rejected without paying decode or dependency cost
- the Integrity zome contains callbacks and mapping only; envelope logic lives in the adapter and pure core

---

## PR 3 — Property Name and Native Value Validation

**Estimate:** 4 pts

### Goal

Validate descriptor-independent property names and native property values.

### Deliverables

Validation rules for:

- property names: non-empty, UTF-8 validity, whitespace rules, control characters, byte-length limit (`PropertyName` has no validating constructor; these rules are new PVL logic)
- string size
- enum representation
- integer representation
- boolean representation
- bytes size
- regression tests pinning the satisfied-by-construction rules (no collections, no nesting, no present-`None`) so a future `PropertyValue` representation change surfaces as a test failure

### Dependencies

- PR 2

### Exit Criteria

- all native `PropertyValue` variants validated without descriptor lookup
- property names satisfy native MAP naming rules and PVL limits

---

# Milestone 3 — Identifier Validation

## Outcome

Validate native identifier representations across both layers.

---

## PR 4 — Identifier Validation

**Estimate:** 2 pts

### Goal

Validate Integrity-visible identifier types per the Section 3.3 layering.

### Deliverables

- pure core: shape and role checks for hash-shaped identifiers, including the 39-byte ActionHash-shaped `LocalId` (new shape check; no validating constructor exists today)
- substrate adapter: exact Holochain hash parsing where `holo_hash` types are available
- `RemoteObjectId` bounds, if present in an Integrity-visible structure

### Dependencies

- PR 1

### Exit Criteria

- malformed identifiers rejected deterministically
- no `holo_hash` dependency in the pure core

---

# Milestone 4 — Holon Lifecycle Validation

## Outcome

Descriptor-independent validation of create, update, and delete operations.

---

## PR 5 — Holon Update and Delete Validation

**Estimate:** 4 pts

### Sequencing

PR 5 landed before Storage SL2 and established the Create/Update contract independently: an update's `original_action_address` must reference a lineage-root `Create` carrying the `HolonNode` entry type, and update-to-update chains are invalid. Storage SL2 has since landed and `PublishVersion` now authors that root-addressed Holochain `Update`, reusing PR 5's check rather than wiring a second one.

### Goal

Validate native lifecycle rules for HolonNode updates and deletes, through a pure-core rule over substrate-free target facts and a substrate adapter that resolves them.

### Deliverables

- pure-core lifecycle module in `pvl_validation` holding a substrate-free description of a resolved lifecycle target (its action kind and its entry kind, each with fixed diagnostic tokens in the manner of PR 4's identifier-kind constant) and the two rules over it:
    - update target: action kind must be `Create` and entry kind must be `HolonNode`, else `InvalidUpdateTarget`; a target `Update` is rejected even when it carries a `HolonNode`
    - delete target: action kind must be `Create` or `Update` and entry kind must be `HolonNode`, else `InvalidDeleteTarget` (design spec Section 10.2 states why both action kinds are valid delete targets)
    - each rule checks action kind before entry kind so the diagnostic names the axis that failed
- substrate adapter in `holons_guest_integrity` resolving the target and mapping it to the facts type, per design spec Section 9.2: `must_get_valid_record` for the update target (the lineage root is a structural parent, so inductive validity is wanted; root-addressing bounds it at one hop), `must_get_action` for the delete target. Both read the target's entry type from its **action**; neither deserializes the target entry
- Integrity wiring for all five arms — `StoreEntry::UpdateEntry`, `RegisterUpdate::Entry`, `StoreRecord::UpdateEntry`, `RegisterDelete`, `StoreRecord::DeleteEntry` — replacing three arms that currently accept unconditionally, the `StoreRecord` update arm that accepts a `Create` **or** an `Update` original, and its `to_app_option` decode of the original entry
- lifecycle checks run after the PR 2 raw-op envelope guard, preserving that PR's exit criterion that an oversized entry pays no decode or dependency cost; the guard must remain the first thing `validate` does
- `InvalidUpdateTarget` field rename to `expected_target_kind` / `actual_target_kind` (design spec Section 10.2), fanning out to `integrity_core_types/src/pvl_error.rs`, its round-trip test, and the hand-maintained `HolonErrorWire` TypeScript SDK mirror and type guard
- retirement of the superseded delete path this PR replaces: `validate_delete_holon_node`, the no-op `validate_delete_holon` in `pvl_validation`, both `PersistenceDelete::new` construction sites, and the now-orphaned `PersistenceDelete` struct. `PersistenceAction`, `PersistenceCreate`, and `PersistenceUpdate` are already dead but are not orphaned by this PR; the `Persistence*Link` types belong to PR 6. Leave those in place with the intent recorded rather than sweeping them up here
- `ImmutableNativeFieldChanged` is deliberately not implemented; add a comment at its definition recording that it is reserved and unused

### Coverage model

The update rule is now exercised positively through the conductor by Storage SL2's normal `PublishVersion` path. Invalid update targets and negative delete targets remain difficult or impossible to construct through production coordinator APIs, so coverage is:

- exhaustive unit tests over the pure facts type, covering every action-kind × entry-kind combination for both rules — the reason the pure core takes a narrow enumerated input rather than a substrate mirror
- adapter tests over synthetic `Op` values, reusing PR 2's op-construction fixtures, proving each of the five arms routes to the right rule and maps violations to the `MAP-PVL` message
- positive sweetests proving a root-addressed version update and a legitimate delete commit

The `Invalid` vs `UnresolvedDependencies` distinction is not conductor-provable here. It is a code-level invariant (design spec Section 11): the adapter must never intercept a `must_get_*` short-circuit and convert it into a violation. Enforce it through the `ExternResult<Result<T, PvlViolation>>` shape PR 2 established, and check it in review.

### Dependencies

- PR 2 (envelope guard ordering and adapter seam)
- PR 4 (identifier-kind diagnostic-token convention)

### Exit Criteria

- an update targeting anything other than a `Create` carrying a `HolonNode` is rejected as `MAP-PVL-1301`; a delete targeting anything other than a `Create` or `Update` carrying a `HolonNode` is rejected as `MAP-PVL-1303`
- all five lifecycle arms route through the adapter; the Integrity zome contains callbacks and mapping only
- no lifecycle path deserializes the target entry, and each op resolves at most one dependency
- no dependency-resolution failure is reachable as a `PvlViolation`
- the superseded delete path is removed rather than left beside the new one

---

# Milestone 5 — SmartLink Structural Validation

## Outcome

Descriptor-independent SmartLink validation over the canonical Tag v1 storage contract.

---

## PR 6 — SmartLink Envelope Validation

**Estimate:** 5 pts

### Goal

Validate intrinsic SmartLink representation using the shared Tag v1 decoder.

### Deliverables

Validation rules for:

- raw tag size against the shared 512-byte v1 ceiling before decode (`SmartLinkTagTooLarge`)
- relationship identifier (empty, UTF-8, NUL, control characters, whitespace, byte length)
- canonical-key bound (`CanonicalKeyTooLarge`; empty keys valid)
- decoded relationship-property and target-cache property maps reuse the PR 3 property-name and native-value validators, in deterministic map and section order
- ActionHash-only endpoint structure: base, Holochain target, and present `OutboundProxyId` are parsed exactly by the substrate adapter; unsupported `AnyLinkableHash` kinds use `UnsupportedSmartLinkEndpointKind`
- payload-flag and occurrence structure remains codec-owned (reserved bits zero, fixed-width external `OutboundProxyId`, 16-byte occurrence shape when flagged)
- SmartLink tag-size enforcement consumes or re-exports the codec-adjacent `MAP_SMARTLINK_V1_MAX_BYTES`
- malformed tag structure, mapping codec decode errors through `MalformedSmartLink { reason }` in one pure-core mapper shared by Integrity and preflight; the pure validator returns the validated decoded tag so adapters do not decode it again
- split the storage-owned codec error into `SmartLinkTagEncodeError` and `SmartLinkTagDecodeError`, and replace field-bearing string payloads with a codec-owned typed structural-position enum; the pure mapper projects decode positions into `PvlField`. The codec must not depend on PVL types, and its byte format and decode behavior remain unchanged
- exhaustive mapping of `SmartLinkTagDecodeError` onto exactly one `(PvlMalformedReason, PvlField?)` pair or the specified shape/resource violation, per the normative mapping table in design spec Section 10.3 (`TagTooLarge` maps to `SmartLinkTagTooLarge`; `InvalidHashLength` on the supplied link target surfaces as `InvalidSmartLinkEndpoint`); encode-only errors do not participate, and tests exercise every decode error through the real decoder
- one SmartLink adapter create path and one delete path, wired through `RegisterCreateLink`, `RegisterDeleteLink`, `StoreRecord::CreateLink`, and `StoreRecord::DeleteLink`; `RegisterDeleteLink` carries its resolved `CreateLink` and requests no dependency, while `StoreRecord::DeleteLink` resolves only `must_get_action`, preserving `UnresolvedDependencies`. Scoped link type selects the applicable validator rather than constituting a delete-target failure axis
- link delete-target structure: a delete names a `CreateLink`, otherwise `InvalidLinkDeleteTarget`; the actual enforcement point is `StoreRecord::DeleteLink` because `RegisterDeleteLink` satisfies the rule by construction
- extend the PVL violation contract with `InvalidLinkDeleteTarget` / `MAP-PVL-2004`, including its serialization round-trip and the hand-maintained `HolonErrorWire` TypeScript SDK mirror, type guard, fixture, and test
- retire the superseded `validate_create_smartlink_helper` / `validate_delete_smartlink_helper` route, the Integrity-zome SmartLink wrappers, and the now-orphaned `Persistence*Link` bridge family (`hc_action.rs` and `link_types.rs`)

### Dependencies

- Storage SL1 part 1 (shared codec, including occurrence-byte round-trip)
- PR 1
- PR 4 (ActionHash diagnostic-token convention)

### Exit Criteria

- malformed SmartLinks rejected without descriptor lookup
- one decode path: PVL consumes the shared decoder, no second tag parser exists
- SmartLink callback wiring contains no legacy persistence-action bridge or free-form validation error path

---

## PR 7 — Withdrawn

Former scope: SmartLink authorship and forward-link-hash provenance verification.

Withdrawn in design spec v0.3 (Section 8.5): relationship-write authority is not inferable from Holochain action authors, and Tag v1 carries no forward-link reference to verify. Occurrence-identity structural validation is covered by the shared codec and PR 6. The slot is retained for numbering stability; if a future tag field introduces a deterministic forward reference, provenance verification returns here with the reserved `2110`–`2119` codes.

---

# Milestone 6 — Integration

## Outcome

Descriptor-independent PVL connected to Holochain and reused before commit.

---

## PR 8 — Coordinator Preflight, Infrastructure-Link Cleanup, and Integration Coverage

**Estimate:** 6 pts

### Goal

Reuse the completed pure-core and Integrity-adapter paths before coordinator writes, replace scaffold-generated infrastructure-link validators without weakening active access paths, finish the callback-layer boundary, and prove the integrated behavior through the real conductor path.

PRs 2–6 already provide the HolonNode envelope and lifecycle adapters, SmartLink create/delete adapters, flattened-op routing, and deterministic violation mapping. PR 8 consumes and cleans up those paths; it does not create another substrate adapter or validation route.

### Deliverables

- HolonNode coordinator preflight at the canonical `persist_holon` write boundary:
    - serialize the exact `HolonNode` model about to be wrapped for persistence
    - run the pure size and decoded-model rules in their established order immediately before `create_entry` or `update_entry`
    - map `PvlViolation` to `HolonError::PvlViolation`
- SmartLink coordinator preflight at the canonical `put_smartlink` write boundary:
    - encode Tag v1 exactly once
    - run `validate_smartlink_envelope` over the source identity, target identity, and produced bytes immediately before `create_link`
    - submit those same validated bytes, with no second encoder or decoder path
    - preserve storage-writer errors such as packing-budget failure and insertion conflict as storage errors rather than inventing PVL equivalents
- direct `pvl_validation` dependency from the coordinator crate that owns these write boundaries; do not route coordinator preflight through the HDI/op adapter merely to simulate Integrity parity
- explicit preflight contract documentation: shared pure rules are reused for coordinator-constructible canonical inputs, while arbitrary raw encoding, exact Holochain hash-kind and action facts, flattened-op routing, dependency availability, and `UnresolvedDependencies` remain Integrity-only
- removal of the unused runtime-budget artifacts from the pre-release contract and all mirrors: `MAX_VALIDATION_DEPENDENCIES_PER_OP`, `ValidationDependencyLimitExceeded`, `MAP-PVL-3001`, serialization tests, TypeScript wire union/type guard members, and fixtures
- structural dependency-bound tests:
    - every PVL adapter entry point pins its exact `must_get_*` count at zero or one
    - callback-routing tests cover every applicable flattened operation
    - no user collection, loop, retry, or graph traversal can drive dependency requests
- replacement of the scaffold-generated functions in `holons_integrity/src/holon_node.rs` with explicit infrastructure-link handling in the Holochain-aware adapter:
    - `HolonNodeUpdates`: reject new creates because native updates supersede the index; permit cleanup deletion until the type and remaining readers are retired together
    - `AllHolonNodes`: retain fixed path-base, empty-tag, and HolonNode-target validation and reject deletes while the active legacy index remains
    - `LocalHolonSpace`: retain fixed path-base, empty-tag, and HolonNode-target validation and allow deletion
    - keep these rules separate from SmartLink Tag v1 PVL and do not add descriptor-independent `PvlViolation` variants for infrastructure indexes
- `holons_integrity` reduced to callback declaration, operation/link-type dispatch, and callback-result projection; PVL policy, dependency resolution, and infrastructure-link rules live outside the zome callback module
- sweetest coverage proving representative HolonNode and SmartLink violations are rejected through the real conductor path with exact stable `MAP-PVL` messages; use narrowly scoped test authoring probes where typed production APIs cannot construct malformed raw bytes
- preflight tests proving invalid coordinator-owned values fail with `HolonError::PvlViolation` before the Holochain write host function is invoked, plus positive tests proving valid root, version, and SmartLink writes remain unchanged

### Dependencies

- PRs 2–6

### Exit Criteria

- every canonical coordinator HolonNode and SmartLink write crosses exactly one preflight boundary and maps pure-rule failures to `HolonError::PvlViolation`
- preflight validates the exact canonical bytes subsequently submitted to Holochain, without claiming adapter-level parity
- the Integrity zome contains callback declaration, dispatch, and result projection only; no PVL policy or dependency-resolution implementation remains there
- no active infrastructure access path loses Integrity validation when the scaffold-generated validators are removed
- every descriptor-independent PVL adapter path has a tested structural dependency count of zero or one; no runtime counter or active dependency-limit violation remains
- sweetest integration suite passes

---

# Milestone 7 — Regression Fixtures, Benchmarks, and Ratification

## Outcome

Durable protection of the limits against regressions, and a reproducible ratification artifact.

---

## PR 9 — PVL Regression Suite, Benchmarks, and Re-Measurement

**Estimate:** 4 pts

### Goal

Convert the one-time measurements (spec Section 12.4) into a committed, reproducible measurement and regression suite, re-run against the Tag v1 encoder.

### Deliverables

- committed measurement program that serializes the corpus with the real `HolonNode` entry encoding and the shared Tag v1 encoder, recording the corpus commit and generating the report (replaces the uncommitted 2026-07 scratch tool)
- re-measured Section 12.4 results, including Tag v1 tags with canonical keys, occurrence identity, and packed cache candidates
- near-limit and malformed fixtures (minimum/maximum HolonNode, maximum property count, maximum string/bytes/canonical key, maximum tag, and all zero-or-one dependency operation shapes)
- benchmark scenarios per spec Section 12.3
- committed benchmark report
- regression tests over serialized sizes and the structural zero-or-one dependency counts

### Dependencies

- Storage SL1/SL3, PRs 1–8

### Exit Criteria

- regression suite established and passing
- measurement artifact and benchmark report committed; spec Section 12.4 updated from "initially measured" to ratified values

Note: ratification must be re-run once representative content holons exist, before the limits freeze into a production DNA.

---

# Critical Path

1. Storage SL1 — Tag v1 codec and storage vertical slice (external prerequisite)
2. PR 1 — Limits, Version Contract, and Error Model
3. PR 2 — HolonNode Envelope Validation
4. PR 3 — Property Name and Native Value Validation
5. PR 4 — Identifier Validation
6. PR 5 — Holon Update and Delete Validation
7. PR 6 — SmartLink Envelope Validation
8. PR 8 — Substrate Adapter, Integrity Integration, and Preflight
9. PR 9 — PVL Regression Suite, Benchmarks, and Re-Measurement

Parallelism: Storage SL1 and PR 1 are independent and can proceed concurrently. Once PR 1 lands, PR 4 and the SmartLink track (PR 6, given SL1) can proceed in parallel with Milestone 2. No PVL PR is gated on Storage SL2.

---

# Relationship to the Storage Layer Implementation Plan

The storage plan owns the SmartLink byte format, codec, storage algebra, and storage-level idempotency (semantic insertion identity, `AlreadyPresent`/`Conflict`). This plan owns the PVL limit contract, violation model, entry-level and lifecycle validation, and the Integrity/preflight wiring. The seam is the shared decoder and the decoded storage types: PVL validates what the codec decodes and never parses tag bytes itself. PR 6 replaced SL1's interim direct structural-validation route with the one PVL pure-core mapper and adapter path; PR 8 invokes that same path on the once-encoded bytes immediately before storage writes rather than wiring it again. The same rule applies to lifecycle: PR 5 owns the root-addressed update check, and the landed Storage SL2 write path exercises it without adding a second validator.

---

# Relationship to the Validation Implementation Plan

This plan deliberately does not consume the layered validation framework (validator frameworks, rule traits, contexts) defined in the Validation Implementation Plan. The kernel is a small fixed set of pure functions; introducing rule-dispatch indirection for ~30 permanent checks would put an unbuilt framework on the kernel's critical path without benefit.

If descriptor-aware validation materializes, that framework may wrap or absorb these pure functions. Descriptor-aware validation, descriptor orchestration, and dynamic validation rule dispatch remain the responsibility of the Validation Implementation Plan and are explicitly out of scope here.
