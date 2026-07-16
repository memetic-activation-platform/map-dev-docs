# Validation Implementation Plan v2.1 (Non-Descriptor-Dependent PVL)

## Purpose

This document defines an incremental implementation plan for the descriptor-independent Peer Validation Language (PVL) described in the PVL Design Specification (v0.2).

The goal is to deliver a small, deterministic validation kernel suitable for Holochain Integrity validation, implemented as plain pure functions within the layered architecture defined in Section 3.3 of the design spec:

    holons_integrity (zome)          — validation callbacks only
      -> holons_guest_integrity      — substrate adapter (Holochain-aware)
           -> shared_validation      — pure PVL core (substrate-independent)

This plan intentionally excludes descriptor-aware validation.

### Changes from v2.0

- Added PR 0. The SmartLink tag codec is currently private to the coordinator-side crate (`holons_guest`), so Integrity cannot decode tags at all, and the format has framing defects. Relocation plus a format revision is a prerequisite for all SmartLink validation.
- Removed the dependency on the layered validation framework. The kernel is a small fixed set of checks implemented as plain pure functions in `shared_validation`. A general rule framework can be extracted later if descriptor-aware validation materializes.
- Consolidated 13 PRs to 10 and reduced scope where code grounding showed rules are satisfied by construction (`BaseValue` is scalar-only; `PropertyMap` has no `Option`).
- Added key-property validation (`MAX_KEY_BYTES`, spec Section 6.9).
- Recorded that limit ratification measurements are complete (spec Section 12.4); the final milestone now delivers the durable regression and benchmark suite only.

---

# External Dependencies

## Design Spec

- `pvl-design-spec.md` v0.2 is the normative source for limits, violations, error codes, and rules.
- Spec open decision 8 (immutable native fields across HolonNode updates) must be resolved before PR 5.
- Spec Section 8.4 (link authorship and inverse-provenance policy) must be ratified at PR review before PR 7.

## Holochain

Requires:

- Integrity Zome validation callbacks
- `shared_validation` usable from Integrity WASM
- Existing HolonNode and SmartLink models

## Validation Framework

None. This plan deliberately does not consume the layered validation framework defined in the Validation Implementation Plan. See "Relationship to the Validation Implementation Plan" below.

---

# Milestone 0 — SmartLink Tag Format Prerequisite

## Outcome

The SmartLink tag format contract lives in the pure core, is decodable by Integrity, and round-trips all supported values.

---

## PR 0 — Tag Codec Relocation and Format v2

**Estimate:** 5 pts

### Goal

Move the SmartLink tag codec into `shared_validation` and revise the format so it can carry the data PVL must validate.

### Deliverables

- Relocate `LinkTagObject`, `encode_link_tag`, `encode_link_tag_prolog`, `decode_link_tag`, and the header/separator constants from `holons_guest` / `holons_integrity` into `shared_validation`, operating on plain bytes (`Vec<u8>` / `&[u8]`) rather than the Holochain `LinkTag` type.
- Format v2:
    - explicit format-version byte after the header
    - length-prefixed framing replacing NUL/separator scanning
    - per-property value-kind discriminant so all `BaseValue` kinds round-trip
    - forward-link provenance field (spec Section 8.4)
    - shape-validated 39-byte proxy id
- `SmartLink`, `save_smartlink`, and the link query functions remain in `holons_guest` and consume the relocated codec.
- Preserve the relationship-name prolog as a deterministic tag prefix (required by `tag_prefix` queries and duplicate suppression).
- Round-trip tests covering integer and bytes values, raw 39-byte hashes containing 0x00, and prefix stability.
- Delete the dead commented-out externs and helpers in `smartlink_adapter.rs` as scoped cleanup.

### Rationale

The current format cannot be validated or reliably decoded by Integrity:

- the codec is private to a coordinator-side crate that Integrity cannot link
- NUL-terminated framing corrupts non-string values and raw hash bytes, both of which can contain 0x00
- decoded smart property values are all assumed to be strings
- there is no field for inverse-link provenance

Once PVL freezes rules about tag bytes, every later format change is a DNA-relevant event. This PR is the one cheap moment to fix the format.

### Dependencies

- none

### Exit Criteria

- Integrity-reachable code can decode every tag the coordinator can encode
- all supported `BaseValue` kinds and raw hash bytes round-trip
- existing sweetest link behavior is unchanged

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

- `pvl_limits_v1`: versioned limit constants (including `MAX_KEY_BYTES`) and pure helper functions
- `PvlViolation` and `PvlMalformedReason`
- error-code registry (including `MAP-PVL-1116` through `MAP-PVL-1118`)
- mapping to `HolonError::PvlViolation`
- Integrity-safe organization in `shared_validation`

### Dependencies

- none

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
- key property values (spec Section 6.9: string kind, non-empty, `MAX_KEY_BYTES`)
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

Descriptor-independent SmartLink validation.

---

## PR 6 — SmartLink Envelope Validation

**Estimate:** 3 pts

### Goal

Validate intrinsic SmartLink representation using the relocated codec.

### Deliverables

Validation rules for:

- tag size
- relationship identifier
- endpoint representation
- malformed tag structure

### Dependencies

- PR 0
- PR 1

### Exit Criteria

- malformed SmartLinks rejected without descriptor lookup

---

## PR 7 — SmartLink Authorship and Provenance

**Estimate:** 5 pts

### Entry Criterion

Spec Section 8.4 authorship policy ratified at PR review.

### Goal

Validate deterministic SmartLink authorship and inverse-link provenance.

### Deliverables

Validation rules for:

- forward-link authorship (base author policy)
- inverse-link provenance verification against the referenced forward link
- link delete author policy
- dependency counting and unresolved dependency handling

### Dependencies

- PR 6

### Exit Criteria

- authorship and provenance rules enforced deterministically

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
- `holons_integrity` callbacks delegate to the adapter; deterministic callback mapping (`Invalid` vs `UnresolvedDependencies`)
- coordinator preflight invokes the pure core directly, mapping to `HolonError::PvlViolation`
- sweetest coverage proving malformed commits are rejected through the real conductor path

### Dependencies

- PRs 2–7

### Exit Criteria

- the Integrity zome contains callbacks only, no validation logic
- Integrity and coordinator preflight execute identical descriptor-independent validation
- sweetest integration suite passes

---

# Milestone 7 — Regression Fixtures and Benchmarks

## Outcome

Durable protection of the ratified limits against regressions.

---

## PR 9 — PVL Regression Suite and Benchmarks

**Estimate:** 3 pts

### Goal

Convert the one-time ratification measurements (spec Section 12.4) into a committed regression and benchmark suite.

### Deliverables

- near-limit and malformed fixtures (minimum/maximum HolonNode, maximum property count, maximum string/bytes/key, maximum tag, dependency-budget boundary cases)
- benchmark scenarios per spec Section 12.3
- committed benchmark report
- regression tests over serialized sizes and dependency counts

### Dependencies

- PRs 0–8

### Exit Criteria

- regression suite established and passing
- benchmark report committed

Note: ratification should be re-run once representative content holons exist, before the limits freeze into a production DNA.

---

# Critical Path

1. PR 0 — Tag Codec Relocation and Format v2
2. PR 1 — Limits, Version Contract, and Error Model
3. PR 2 — HolonNode Envelope Validation
4. PR 3 — Property Name and Native Value Validation
5. PR 4 — Identifier Validation
6. PR 5 — Holon Update and Delete Validation
7. PR 6 — SmartLink Envelope Validation
8. PR 7 — SmartLink Authorship and Provenance
9. PR 8 — Substrate Adapter, Integrity Integration, and Preflight
10. PR 9 — PVL Regression Suite and Benchmarks

Parallelism: PR 0 and PR 1 are independent and can proceed concurrently. Once PR 1 lands, PR 4 and the SmartLink track (PR 6 onward, given PR 0) can proceed in parallel with Milestone 2.

---

# Relationship to the Validation Implementation Plan

This plan deliberately does not consume the layered validation framework (validator frameworks, rule traits, contexts) defined in the Validation Implementation Plan. The kernel is a small fixed set of pure functions; introducing rule-dispatch indirection for ~30 permanent checks would put an unbuilt framework on the kernel's critical path without benefit.

If descriptor-aware validation materializes, that framework may wrap or absorb these pure functions. Descriptor-aware validation, descriptor orchestration, and dynamic validation rule dispatch remain the responsibility of the Validation Implementation Plan and are explicitly out of scope here.
