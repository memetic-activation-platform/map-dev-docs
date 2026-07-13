# Validation Implementation Plan v2.0 (Non-Descriptor-Dependent PVL)

## Purpose

This document defines an incremental implementation plan for the descriptor-independent Peer Validation Language (PVL) described in the PVL Design Specification.

The goal is to deliver a small, deterministic validation kernel suitable for Holochain Integrity validation while maximizing reuse of the layered validation framework defined in the Validation Implementation Plan.

This plan intentionally excludes descriptor-aware validation and depends upon the shared validation framework rather than implementing an independent validation subsystem.

---

# External Dependencies

## Validation Framework

This implementation consumes the layered validation framework defined in the Validation Implementation Plan.

Required dependencies include:

- Validation Foundation Types
- Validation Rule Traits and Contexts
- Validation Results
- Shared Validation Entry Points

Descriptor-aware validators are **not** required.

---

## Holochain

Requires:

- Integrity Zome validation callbacks
- Shared validation crate usable from Integrity WASM
- Existing HolonNode and SmartLink models

---

# Milestone 1 — PVL Foundation

## Outcome

Introduce the fixed infrastructure required by descriptor-independent PVL.

---

## PR 1 — PVL Limits and Version Contract

**Estimate:** 2 pts

### Goal

Introduce the normative versioned limit contract.

### Deliverables

- `pvl_limits_v1`
- versioned limit constants
- pure helper functions
- Integrity-safe crate organization

### Dependencies

- none

### Exit Criteria

- all PVL limits exist in one versioned location
- Integrity and coordinator preflight compile against the same contract

---

## PR 2 — PVL Error Model

**Estimate:** 2 pts

### Goal

Introduce structured PVL violations.

### Deliverables

- `PvlViolation`
- `PvlMalformedReason`
- error code registry
- mapping to `HolonError::PvlViolation`

### Dependencies

- PR 1

### Validation Framework Dependencies

- Validation Foundation Types

### Exit Criteria

- all descriptor-independent violations represented
- stable error code registry established

---

# Milestone 2 — HolonNode Structural Validation

## Outcome

Descriptor-independent validation of native HolonNode structure.

---

## PR 3 — HolonNode Envelope Validation

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
- PR 2

### Validation Framework Dependencies

- Shared Validation Entry Points
- Holon Validator Framework

### Exit Criteria

- malformed or oversized HolonNodes rejected
- valid entries accepted

---

## PR 4 — Property Name Validation

**Estimate:** 2 pts

### Goal

Validate descriptor-independent property names.

### Deliverables

Validation rules for:

- non-empty names
- UTF-8 validity
- whitespace rules
- control characters
- byte-length limit

### Dependencies

- PR 3

### Validation Framework Dependencies

- Property Validator Framework

### Exit Criteria

- property names satisfy native MAP naming rules and PVL limits

---

## PR 5 — Native Property Value Validation

**Estimate:** 5 pts

### Goal

Validate descriptor-independent native property values.

### Deliverables

Validation rules for:

- string size
- enum representation
- integer representation
- boolean representation
- bytes size
- collection limits
- collection homogeneity
- nesting depth
- Option/null representation

### Dependencies

- PR 4

### Validation Framework Dependencies

- Generic Value Validator
- String Value Validator
- Integer/Boolean/Enum/Bytes Validators

### Exit Criteria

- all native PropertyValue variants validated without descriptor lookup

---

# Milestone 3 — Identifier Validation

## Outcome

Validate native identifier representations.

---

## PR 6 — Identifier Validation

**Estimate:** 2 pts

### Goal

Validate Integrity-visible identifier types.

### Deliverables

Validation rules for:

- Holochain hash wrappers
- RemoteObjectId
- identifier length
- identifier shape

### Dependencies

- PR 2

### Validation Framework Dependencies

- Generic Value Validator

### Exit Criteria

- malformed identifiers rejected deterministically

---

# Milestone 4 — Holon Lifecycle Validation

## Outcome

Descriptor-independent validation of create, update, and delete operations.

---

## PR 7 — Holon Update and Delete Validation

**Estimate:** 3 pts

### Goal

Validate native lifecycle rules.

### Deliverables

Validation rules for:

- update target
- immutable native fields
- delete target
- unresolved dependency handling

### Dependencies

- PR 3
- PR 6

### Validation Framework Dependencies

- Shared Validation Entry Points

### Exit Criteria

- lifecycle validation correctly distinguishes Invalid from UnresolvedDependencies

---

# Milestone 5 — SmartLink Structural Validation

## Outcome

Descriptor-independent SmartLink validation.

---

## PR 8 — SmartLink Envelope Validation

**Estimate:** 3 pts

### Goal

Validate intrinsic SmartLink representation.

### Deliverables

Validation rules for:

- tag size
- relationship identifier
- endpoint representation
- malformed tag structure

### Dependencies

- PR 2

### Validation Framework Dependencies

- Relationship Validator Framework

### Exit Criteria

- malformed SmartLinks rejected without descriptor lookup

---

## PR 9 — SmartLink Authorship and Provenance

**Estimate:** 5 pts

### Goal

Validate deterministic SmartLink authorship and inverse-link provenance.

### Deliverables

Validation rules for:

- link authorship
- inverse-link provenance
- dependency counting
- unresolved dependency handling

### Dependencies

- PR 8

### Validation Framework Dependencies

- Relationship Validator Framework

### Exit Criteria

- authorship and provenance rules enforced deterministically

---

# Milestone 6 — Dependency Budget Enforcement

## Outcome

Prevent unbounded Integrity validation work.

---

## PR 10 — Validation Dependency Budget

**Estimate:** 2 pts

### Goal

Implement deterministic dependency accounting.

### Deliverables

- dependency counter
- maximum dependency enforcement
- `ValidationDependencyLimitExceeded`
- UnresolvedDependency handling

### Dependencies

- PR 7
- PR 9

### Validation Framework Dependencies

- Shared Validation Entry Points

### Exit Criteria

- dependency requests remain within configured PVL limits

---

# Milestone 7 — Integrity Integration

## Outcome

Connect descriptor-independent PVL to Holochain.

---

## PR 11 — Integrity Zome Integration

**Estimate:** 3 pts

### Goal

Invoke shared descriptor-independent PVL from Integrity callbacks.

### Deliverables

- create validation
- update validation
- delete validation
- SmartLink validation
- deterministic callback mapping

### Dependencies

- PRs 3–10

### Validation Framework Dependencies

- Shared Validation Entry Points

### Exit Criteria

- Integrity callback delegates to shared PVL implementation
- deterministic callback results returned

---

# Milestone 8 — Coordinator Preflight Integration

## Outcome

Reuse PVL before commit.

---

## PR 12 — Coordinator Preflight Validation

**Estimate:** 2 pts

### Goal

Reuse descriptor-independent PVL outside Integrity.

### Deliverables

- coordinator preflight adapter
- mapping to `HolonError::PvlViolation`
- shared execution path

### Dependencies

- PR 11

### Validation Framework Dependencies

- Shared Validation Entry Points

### Exit Criteria

- Integrity and coordinator execute identical descriptor-independent validation

---

# Milestone 9 — Fixtures and Benchmarks

## Outcome

Ratify limits and prevent regressions.

---

## PR 13 — PVL Fixtures and Benchmarks

**Estimate:** 3 pts

### Goal

Validate proposed limits against representative data.

### Deliverables

Fixtures for:

- minimum HolonNode
- maximum HolonNode
- maximum property count
- maximum string
- maximum bytes
- maximum collection
- maximum SmartLink tag
- malformed entries
- dependency-budget boundary cases

Benchmarks for:

- validation execution time
- serialized sizes
- dependency counts

### Dependencies

- PRs 1–12

### Validation Framework Dependencies

- Validation Diagnostics and Fixtures

### Exit Criteria

- proposed limits validated against real fixtures
- benchmark report committed
- regression suite established

---

# Critical Path

1. PR 1 — PVL Limits and Version Contract
2. PR 2 — PVL Error Model
3. PR 3 — HolonNode Envelope Validation
4. PR 4 — Property Name Validation
5. PR 5 — Native Property Value Validation
6. PR 6 — Identifier Validation
7. PR 7 — Holon Update and Delete Validation
8. PR 8 — SmartLink Envelope Validation
9. PR 9 — SmartLink Authorship and Provenance
10. PR 10 — Validation Dependency Budget
11. PR 11 — Integrity Zome Integration
12. PR 12 — Coordinator Preflight Validation
13. PR 13 — PVL Fixtures and Benchmarks

# Relationship to the Validation Implementation Plan

This implementation plan intentionally builds on the layered validation framework rather than duplicating it.

Specifically, it reuses:

- Validation Foundation Types
- Validation Rule Traits and Contexts
- Holon Validator Framework
- Property Validator Framework
- Generic Value Validator
- Type-Specific Value Validators
- Relationship Validator Framework
- Shared Validation Entry Points
- Validation Results
- Validation Diagnostics and Fixtures

Descriptor-aware validation, descriptor orchestration, and dynamic validation rule dispatch are explicitly out of scope for descriptor-independent PVL and remain the responsibility of the Validation Implementation Plan.