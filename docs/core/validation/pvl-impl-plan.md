# Validation Implementation Plan v2.2 (Non-Descriptor-Dependent PVL)

## Purpose

This document defines an incremental implementation plan for the descriptor-independent Peer Validation Language (PVL) described in the PVL Design Specification (v0.3).

The goal is to deliver a small, deterministic validation kernel suitable for Holochain Integrity validation, implemented as plain pure functions within the layered architecture defined in Section 3.3 of the design spec:

    holons_integrity (zome)          — validation callbacks only
      -> holons_guest_integrity      — substrate adapter (Holochain-aware)
           -> shared_validation      — pure PVL core (substrate-independent)
                -> integrity_core_types  — shared types and the Tag v1 codec

This plan intentionally excludes descriptor-aware validation.

### Changes from v2.1

- Aligned with the [Storage Layer and SmartLink Design Specification](../guest/storage-layer-services/storage-layer-design-spec.md) v1.0 and its implementation plan, which landed after v2.1 was written.
- Removed PR 0 (tag codec relocation and format v2). The canonical SmartLink Tag v1 format, codec, and storage-boundary types are owned and delivered by the storage plan (Storage SL1/SL3); this plan consumes them as an external dependency. The in-flight PR 0 branch is being reworked to implement the SL1 codec.
- Withdrew the SmartLink authorship policy and forward-link-hash provenance (former PR 7 scope) per design spec v0.3 Section 8.5: relationship-write authority is not a descriptor-independent PVL concern, and Tag v1 carries no forward-link reference. Inverse pairing is occurrence identity, whose structural form is validated by the shared codec and PR 6.
- Reframed the key limit as the `MAX_CANONICAL_KEY_BYTES` bound on the mandatory Tag v1 canonical-key segment (design spec Section 8.4); removed the key-property rule from PR 3.
- Adopted the shared tag budget: `MAX_SMART_LINK_TAG_BYTES = 1_024`, matching the Holochain `LinkTag` ceiling and the storage packing budget (provisional; a narrower shared bound is under discussion).
- Weakened the preflight claim: shared pure-core checks are identical for Integrity and preflight by construction; adapter-level checks are Integrity-only unless a preflight adapter is added (PR 8 decision).
- Downgraded limit ratification to "initially measured"; PR 9 now owns re-measurement with the Tag v1 encoder and a committed reproducible measurement artifact.

---

# External Dependencies

## Design Spec

- `pvl-design-spec.md` v0.3 is the normative source for limits, violations, error codes, and rules.
- Spec open decision 8 (immutable native fields across HolonNode updates) must be resolved before PR 5.
- The shared tag budget (spec Section 8.1) is provisionally 1,024 bytes; if a narrower bound is ratified, the limit constant changes before PR 9 freezes fixtures.

## Storage Layer Plan

The [storage implementation plan](../guest/storage-layer-services/storage-layer-impl-plan.md) delivers, as an external prerequisite to this plan's SmartLink track:

- **Storage SL1** — the pure Tag v1 codec and storage-boundary types (`SmartLink`, `PreparedSmartLink`, `CanonicalKey`, `KeyMatch`, outcome enums) in an HDK-independent shared module, plus the storage read/write algebra and structural integrity validation through the shared decoder.
- **Storage SL3** — optional 16-byte `OccurrenceId` encoding and identity participation.

Division of labor: the storage plan owns the codec, the byte format, and storage-level idempotency; this plan owns the PVL limit contract, the violation and error-code model, entry-level validation, lifecycle validation, and the Integrity/preflight wiring that layers PVL semantics over the shared decoder. SL1's structural decode validation at Integrity entry points and PR 6/PR 8 of this plan must be coordinated so the decode path is wired once, not twice.

## Holochain

Requires:

- Integrity Zome validation callbacks
- `shared_validation` and `integrity_core_types` usable from Integrity WASM
- Existing HolonNode model and the SL1 SmartLink storage model

## Validation Framework

None. This plan deliberately does not consume the layered validation framework defined in the Validation Implementation Plan. See "Relationship to the Validation Implementation Plan" below.

---

# Milestone 0 — Storage Tag v1 Codec (External Prerequisite)

## Outcome

The canonical SmartLink Tag v1 codec exists in Integrity-reachable shared code, delivered by Storage SL1.

This is not a PVL PR. It is tracked here because the SmartLink track (PR 6 onward) cannot start without it. The former PVL PR 0 branch (tag codec relocation and format v2) is being reworked in place to implement the SL1 codec against the storage spec's byte layout; its strict-decode discipline, canonical-ordering enforcement, typed scalar handling, and test suite carry over.

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

- `pvl_limits_v1`: versioned limit constants (including `MAX_CANONICAL_KEY_BYTES` and the shared 1,024-byte tag budget) and pure helper functions
- `PvlViolation` and `PvlMalformedReason` per design spec Sections 10.2–10.3 (no authorship or forward-reference provenance variants)
- error-code registry per design spec Section 14 (no `1116`–`1118`; `2110`–`2119` reserved; `2202` `CanonicalKeyTooLarge`)
- total mapping of the shared Tag v1 codec's decode errors onto `PvlMalformedReason` (every codec error variant has exactly one reason)
- mapping to `HolonError::PvlViolation`
- Integrity-safe organization in `shared_validation`

### Dependencies

- none (the codec-error mapping compiles against the SL1 error enum once it lands; the mapping deliverable may trail in a small follow-up if PR 1 merges first)

### Exit Criteria

- all PVL limits and violation types exist in one versioned location
- Integrity and coordinator preflight compile against the same contract

---

# Milestone 2 — HolonNode Structural Validation

## Outcome

Descriptor-independent validation of native HolonNode structure.

---

## PR 2 — HolonNode Envelope Validation

**Estimate:** 3 pts

### Goal

Validate intrinsic HolonNode structure.

### Deliverables

Validation rules for:

- HolonNode serialized size
- property count
- canonical property map shape
- malformed native representation

### Dependencies

- PR 1

### Exit Criteria

- malformed or oversized HolonNodes rejected
- valid entries accepted

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

**Estimate:** 3 pts

### Entry Criterion

Resolve spec open decision 8: confirm `original_id` update semantics against commit code and record which native fields are immutable.

### Goal

Validate native lifecycle rules.

### Deliverables

Validation rules for:

- update target
- immutable native fields
- delete target
- unresolved dependency handling

### Dependencies

- PR 2
- PR 4

### Exit Criteria

- lifecycle validation correctly distinguishes `Invalid` from `UnresolvedDependencies`

---

# Milestone 5 — SmartLink Structural Validation

## Outcome

Descriptor-independent SmartLink validation over the canonical Tag v1 storage contract.

---

## PR 6 — SmartLink Envelope Validation

**Estimate:** 4 pts

### Goal

Validate intrinsic SmartLink representation using the shared Tag v1 decoder.

### Deliverables

Validation rules for:

- tag size against the shared budget (`SmartLinkTagTooLarge`)
- relationship identifier (empty, UTF-8, NUL, control characters, whitespace, byte length)
- canonical-key bound (`CanonicalKeyTooLarge`; empty keys valid)
- endpoint and payload-flag structure (reserved bits zero, external flag consistent with the fixed-width `OutboundProxyId`, 16-byte occurrence shape when flagged)
- malformed tag structure, mapping codec decode errors through `MalformedSmartLink { reason }`
- link delete-target structure (delete names a SmartLink create-link action)

### Dependencies

- Storage SL1 (shared codec; SL3 for occurrence coverage)
- PR 1

### Exit Criteria

- malformed SmartLinks rejected without descriptor lookup
- one decode path: PVL consumes the shared decoder, no second tag parser exists

---

## PR 7 — Withdrawn

Former scope: SmartLink authorship and forward-link-hash provenance verification.

Withdrawn in design spec v0.3 (Section 8.5): relationship-write authority is not inferable from Holochain action authors, and Tag v1 carries no forward-link reference to verify. Occurrence-identity structural validation is covered by the shared codec and PR 6. The slot is retained for numbering stability; if a future tag field introduces a deterministic forward reference, provenance verification returns here with the reserved `2110`–`2119` codes.

---

# Milestone 6 — Integration

## Outcome

Descriptor-independent PVL connected to Holochain and reused before commit.

---

## PR 8 — Substrate Adapter, Integrity Integration, and Preflight

**Estimate:** 6 pts

### Goal

Wire the pure core to Holochain through the substrate adapter, and reuse it in coordinator preflight.

### Deliverables

- substrate adapter in `holons_guest_integrity`: op-to-lifecycle mapping, exact hash parsing, `must_get_*` dependency resolution, dependency-budget accounting (`MAX_VALIDATION_DEPENDENCIES_PER_OP`, `ValidationDependencyLimitExceeded`)
- `holons_integrity` callbacks delegate to the adapter; deterministic callback mapping (`Invalid` vs `UnresolvedDependencies`); coordinated with SL1's structural validation entry points so the decode path is wired once
- coordinator preflight invokes the pure core directly, mapping to `HolonError::PvlViolation`; decide here whether adapter-level parity warrants a coordinator preflight adapter sharing the substrate adapter's preparation path (design spec Section 3.3)
- sweetest coverage proving malformed commits are rejected through the real conductor path

### Dependencies

- PRs 2–6

### Exit Criteria

- the Integrity zome contains callbacks only, no validation logic
- Integrity and coordinator preflight execute identical shared pure-core validation; the preflight-parity decision for adapter-level checks is recorded
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
- near-limit and malformed fixtures (minimum/maximum HolonNode, maximum property count, maximum string/bytes/canonical key, maximum tag, dependency-budget boundary cases)
- benchmark scenarios per spec Section 12.3
- committed benchmark report
- regression tests over serialized sizes and dependency counts

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

Parallelism: Storage SL1 and PR 1 are independent and can proceed concurrently. Once PR 1 lands, PR 4 and the SmartLink track (PR 6, given SL1) can proceed in parallel with Milestone 2.

---

# Relationship to the Storage Layer Implementation Plan

The storage plan owns the SmartLink byte format, codec, storage algebra, and storage-level idempotency (semantic insertion identity, `AlreadyPresent`/`Conflict`). This plan owns the PVL limit contract, violation model, entry-level and lifecycle validation, and the Integrity/preflight wiring. The seam is the shared decoder and the decoded storage types: PVL validates what the codec decodes and never parses tag bytes itself. SL1's "structural version 1 validation using the shared decoder" and this plan's PR 6/PR 8 are the same wiring viewed from two plans and must land as one coherent path.

---

# Relationship to the Validation Implementation Plan

This plan deliberately does not consume the layered validation framework (validator frameworks, rule traits, contexts) defined in the Validation Implementation Plan. The kernel is a small fixed set of pure functions; introducing rule-dispatch indirection for ~30 permanent checks would put an unbuilt framework on the kernel's critical path without benefit.

If descriptor-aware validation materializes, that framework may wrap or absorb these pure functions. Descriptor-aware validation, descriptor orchestration, and dynamic validation rule dispatch remain the responsibility of the Validation Implementation Plan and are explicitly out of scope here.
