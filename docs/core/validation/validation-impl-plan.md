# Validation Implementation Plan v2.0
## Descriptor-Aware Layered Validation Delivery Sequence

## Purpose

This document defines the implementation plan for the shared MAP validation framework.

The goal is to build a reusable, descriptor-aware validation subsystem that can be consumed by:

- Holon Data Loader
- Nursery validation
- coordinator-side preflight validation
- Holochain Integrity adapters (including PVL)
- future runtime validation
- import pipelines
- diagnostics
- developer tooling

The validation framework owns:

- validation rule abstractions
- validation contexts
- layered validator orchestration
- descriptor-aware validation delegation
- shared validation entry points
- validation results
- reusable validation implementations

It deliberately does **not** own:

- descriptor retrieval
- EffectiveDescriptor compilation
- TypeActivation
- Holochain Integrity callback implementation
- descriptor-independent PVL semantics

Those concerns are addressed by the Descriptor Runtime Platform and PVL implementation plans.

---

# Delivery Principles

- Validation is layered.
- Each validation layer owns a distinct validation context.
- Each validation layer exposes a single validation trait.
- Individual validation rules implement that trait.
- Validation delegates downward through the descriptor hierarchy.
- Rule invocation is initially hard-coded.
- Future descriptor-defined rule dispatch must not require validator redesign.
- Validators operate only on the descriptor supplied by the caller.
- Descriptor lookup is outside the validator framework.

---

# Validation Layers

Validation proceeds through four levels.

## Holon

Responsible for validating an entire holon.

Delegates property validation.

---

## Property

Responsible for validating one property.

Delegates value validation.

---

## Generic Value

Responsible for:

- verifying native value kind
- dispatching to type-specific validation

Delegates to value-type validators.

---

## Type-Specific Value

Responsible for validating descriptor-defined constraints for one native value kind.

Examples include:

- String
- Integer
- Boolean
- Enum
- Bytes

---

# Milestone 1 — Validation Foundation

## Outcome

Shared validation infrastructure exists independently of descriptors or Holochain.

---

## PR 1 — Validation Foundation Types

**Estimate:** 2 pts

### Goal

Introduce the shared validation model.

### Deliverables

- ValidationResult
- ValidationSeverity
- ValidationRule identifiers
- validation helper types

### Dependencies

None

### Exit Criteria

Shared validation types are stable and reusable.

---

## PR 2 — Validation Rule Traits and Contexts

**Estimate:** 3 pts

### Goal

Define the layered validation interfaces.

### Deliverables

Validation traits for:

- HolonValidator
- PropertyValidator
- ValueValidator
- type-specific value validators

Validation contexts for each layer.

### Dependencies

- PR 1

### Exit Criteria

Each validation layer has:

- one validation trait
- one validation context

---

# Milestone 2 — Holon Validation

## Outcome

Descriptor-aware holon validation framework exists.

---

## PR 3 — Holon Validator Framework

**Estimate:** 3 pts

### Goal

Implement descriptor-aware holon validation.

### Deliverables

Holon validation rules:

- IsDescribedRule
- RequiredPropertiesRule
- NoUndescribedPropertiesRule

Hard-coded rule orchestration.

Delegation to property validation.

### Dependencies

- PR 2

### Exit Criteria

Holon validation delegates correctly.

---

## PR 4 — Property Validator Framework

**Estimate:** 2 pts

### Goal

Implement property validation.

### Deliverables

Property validation rules:

- RequiredPropertyRule

Delegation to generic value validation.

### Dependencies

- PR 3

### Exit Criteria

Property validation delegates correctly.

---

# Milestone 3 — Generic Value Validation

## Outcome

Generic descriptor-aware value validation exists.

---

## PR 5 — Generic Value Validator

**Estimate:** 2 pts

### Goal

Validate native value kind before type-specific validation.

### Deliverables

Validation rule:

- PropertyValueTypeRule

Dispatch to type-specific validators.

### Dependencies

- PR 4

### Exit Criteria

Incorrect native value kinds are rejected.

Correct kinds delegate.

---

# Milestone 4 — Type-Specific Value Validation

## Outcome

Native MAP value types have reusable validation.

---

## PR 6 — String Value Validator

**Estimate:** 2 pts

### Goal

Implement String validation.

### Deliverables

Validation rules:

- LengthValidationRule

### Dependencies

- PR 5

### Exit Criteria

Descriptor-defined string constraints enforced.

---

## PR 7 — Integer, Boolean, Enum, and Bytes Validators

**Estimate:** 3 pts

### Goal

Implement remaining native value validators.

### Deliverables

Validation rules including:

- RangeValidationRule
- LegalVariantRule
- native Boolean validation
- bytes-length validation

### Dependencies

- PR 5

### Exit Criteria

All supported native value kinds validated.

---

# Milestone 5 — Relationship Validation

## Outcome

Relationship validation framework exists.

---

## PR 8 — Relationship Validator Framework

**Estimate:** 3 pts

### Goal

Implement descriptor-aware relationship validation.

### Deliverables

Relationship validation trait.

Relationship validation context.

Initial descriptor-aware relationship rules.

### Dependencies

- PR 3

### Exit Criteria

Relationship validation framework exists.

Higher-order relationship semantics remain deferred.

---

# Milestone 6 — Descriptor-Orchestrated Validation

## Outcome

Validation execution is descriptor-driven.

---

## PR 9 — Descriptor-Orchestrated Validation

**Estimate:** 5 pts

### Goal

Move validator orchestration to descriptor-defined rule lists.

### Deliverables

Descriptor-driven validator selection.

Temporary Rust dispatch table.

Hard-coded Rust implementations retained.

### Dependencies

- PRs 3–8
- Descriptor Runtime Platform

### Exit Criteria

Descriptors determine which validators execute.

Rust remains the execution engine.

---

# Milestone 7 — Shared Validation Entry Points

## Outcome

All consumers invoke one validation surface.

---

## PR 10 — Shared Validation Entry Points

**Estimate:** 2 pts

### Goal

Provide shared validation APIs.

### Deliverables

Shared entry points for:

- create
- update
- delete
- relationship validation

Operation-specific validation contexts.

### Dependencies

- PR 9

### Exit Criteria

All consumers share one validation implementation.

---

# Milestone 8 — Consumer Integration

## Outcome

Validation framework is reused across MAP.

---

## PR 11 — Holon Data Loader Integration

**Estimate:** 3 pts

### Goal

Use shared validation during type loading.

### Deliverables

Descriptor-aware loader validation.

Shared test fixtures.

### Dependencies

- PR 10

### Exit Criteria

Loader uses shared validation.

---

## PR 12 — Nursery Validation Integration

**Estimate:** 3 pts

### Goal

Use shared validation during staged transaction validation.

### Deliverables

Nursery validation integration.

Transaction-aware validation contexts.

### Dependencies

- PR 10
- Transaction infrastructure

### Exit Criteria

Nursery delegates descriptor-aware validation.

---

## PR 13 — Validation Results and Evidence

**Estimate:** 2 pts

### Goal

Provide reusable validation reporting.

### Deliverables

ValidationResult aggregation.

Validation outcome classification.

Evidence model.

### Dependencies

- PR 10

### Exit Criteria

Validation results reusable across consumers.

---

## PR 14 — Validation Diagnostics and Fixtures

**Estimate:** 3 pts

### Goal

Provide regression fixtures and diagnostics.

### Deliverables

Shared fixtures.

Validation diagnostics.

Regression suite.

### Dependencies

- PRs 10–13

### Exit Criteria

Validation behavior is observable and regression-tested.

---

# Relationship to the PVL Implementation Plan

The shared validation framework has no implementation dependency on the PVL implementation plan.

Instead, the descriptor-independent PVL implementation consumes selected components of this framework, including:

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

Descriptor-independent PVL supplies its own:

- Integrity-safe validation contexts
- resource-limit rules
- native structural validation
- Holochain callback integration
- dependency-budget enforcement

while reusing the common validation infrastructure wherever appropriate.

---

# Critical Path

1. Validation Foundation Types
2. Validation Rule Traits and Contexts
3. Holon Validator Framework
4. Property Validator Framework
5. Generic Value Validator
6. Type-Specific Value Validators
7. Relationship Validator Framework
8. Descriptor-Orchestrated Validation
9. Shared Validation Entry Points
10. Holon Data Loader Integration
11. Nursery Validation Integration
12. Validation Results and Evidence
13. Validation Diagnostics and Fixtures