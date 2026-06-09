# MAP Type System v2.0 Pressure-Test Checklist

## Purpose

This checklist defines a practical process for pressure-testing the MAP Type System v2.0 design before, during, and after implementation work.

Its goal is to increase confidence that the design is:

- structurally correct
- semantically complete
- implementable without hidden compatibility shims
- resilient under hostile and edge-case specimens

This is not an implementation plan and not a schema-ripple manifest. It is a design-validation discipline for the v2.0 model itself.

---

## When to Use This

Run this checklist when:

- the authoritative core schema changes materially
- TypeKind semantics change
- `DescribedBy` / `Extends` / instance semantics change
- loader resolution strategy changes
- descriptor runtime assumptions are being updated
- new abstract anchors, meta-types, or generic descriptor relationships are introduced

---

## Core Questions

Every pressure-test run should answer these questions clearly:

1. Can the v2.0 model express all intended valid cases?
2. Can it reject invalid structures for crisp reasons?
3. Can loader, descriptor, and validation logic operate on the model without pretending removed v1.1 concepts still exist?
4. Does every removed v1.1 concept have a precise v2.0 replacement?
5. Are there any remaining areas where implementation would need to "figure it out in code" because the design is underspecified?

If any answer is "no" or "not yet", the design is not pressure-tested successfully.

---

## Invariant Ledger

These invariants should be tested explicitly, not assumed.

### Descriptor Graph Invariants

- `DescriptorRoot` is the unique bootstrap root of the descriptor inheritance hierarchy.
- `DescriptorRoot` is never an ordinary runtime instance target.
- TypeKind-specific meta-types extend `DescriptorRoot`.
- Abstract type anchors are described by TypeKind-specific meta-types.
- Concrete descriptors extend exactly one abstract or concrete descriptor parent.
- `Extends` is single-inheritance and acyclic.
- `DescribedBy` and `Extends` are distinct axes and must never be conflated.

### Runtime Typing Invariants

- Ordinary runtime holons are described only by stabilized concrete descriptors.
- Abstract anchors such as `HolonType`, `PropertyType`, `ValueType`, `DeclaredRelationshipType`, and `InverseRelationshipType` are never ordinary runtime instance targets.
- JSON import `type` is treated as shorthand for `DescribedBy`.
- Instance conformance is determined by the concrete descriptor plus its inherited obligations.

### Relationship Invariants

- Generic descriptor relationships target `DescriptorRoot` only when they are truly descriptor-agnostic.
- Inheritance-shaped relationships remain family-specific.
- Relationship descriptors classify cleanly as declared or inverse via their effective `Extends` chain.
- Inverse authoring can be rewritten to declared form without relying on removed v1.1 sentinel nodes.

### Compatibility Invariants

- No implementation surface should require a live `TypeDescriptor` node to resolve descriptor endpoints.
- No implementation surface should require `MetaTypeDescriptor`.
- No implementation surface should require `instance_type_kind` if the active schema uses the v2.0 `type_kind` header model.

---

## Specimen Matrix

Pressure-testing should use both valid and invalid specimen schemas.

| Specimen | Purpose | Must Exercise | Expected Result |
|----------|---------|---------------|-----------------|
| Bootstrap-minimal | Prove ontology bootstrap viability | `DescriptorRoot`, meta-types, abstract anchors, cross-role references | succeeds |
| Core-schema-normalized | Prove the authoritative core schema is structurally sound | full cross-file graph, `DescribedBy`, `Extends`, definitional relationships | succeeds |
| Domain-minimal | Prove ordinary schema authoring works | one schema, two holon descriptors, one property, one relationship | succeeds |
| Descriptor-generic relationship | Prove `DescriptorRoot` is used only where intended | descriptor-agnostic source/target anchors | succeeds |
| Same-family inheritance | Prove additive single inheritance within a TypeKind family | concrete extends parent within same family | succeeds |
| Declared/inverse pair | Prove relationship-direction semantics are coherent | `DeclaredRelationshipType`, `InverseRelationshipType`, `InverseOf` | succeeds |
| Value-constraint family | Prove value-kind and constraint-family classification remains coherent | value descriptor inheritance, constraint family anchors | succeeds |
| Cross-schema dependency | Prove inter-schema references remain bounded and resolvable | `DependsOn`, external anchor references | succeeds |
| Extends-cycle | Prove forbidden inheritance cycle is rejected | cyclic `Extends` | fails |
| Multiple-extends | Prove single-inheritance rule is enforced | more than one `Extends` target | fails |
| Abstract-instance misuse | Prove abstract anchors cannot describe ordinary runtime holons | runtime holon with abstract `type` | fails |
| Wrong-meta-type | Prove TypeKind-specific meta-type discipline is enforced | descriptor described by wrong meta-type | fails |
| Legacy-sentinel dependence | Prove v2.0 does not require `TypeDescriptor` fallback | descriptor endpoint matching without `TypeDescriptor` node | succeeds |
| Legacy-header dependence | Prove v2.0 does not require `instance_type_kind` | descriptor classification from active v2.0 header model | succeeds |

---

## Execution Procedure

### Step 1: Record the Replacement Crosswalk

Before testing implementation behavior, write a simple crosswalk:

| v1.1 concept | v2.0 replacement | Proof artifact |
|--------------|------------------|----------------|
| `TypeDescriptor` | `DescriptorRoot` plus TypeKind meta-types, abstract anchors, and concrete descriptors | specimen + implementation path |
| `MetaTypeDescriptor` | TypeKind-specific meta-types | specimen + implementation path |
| `instance_type_kind` | v2.0 descriptor header model | schema + runtime path |

If any removed v1.1 concept has no precise replacement, stop and resolve that design gap first.

### Step 2: Validate the Invariant Ledger

For each invariant above:

- identify at least one positive proof specimen
- identify at least one negative or hostile counterexample where appropriate
- record the expected result before running tooling or code

### Step 3: Run Positive Specimens

Every positive specimen must:

- parse cleanly
- resolve all references
- satisfy descriptor-graph invariants
- remain explainable without appeal to removed concepts

### Step 4: Run Negative Specimens

Every negative specimen must fail for the intended reason.

Failures should be:

- deterministic
- specific
- structurally meaningful

Vague "invalid schema" failures are not enough if the design is meant to provide crisp doctrine.

### Step 5: Walk Real Implementation Paths

At minimum, pressure-test the actual implementation surfaces that operationalize the design:

- authoritative core schema import files
- descriptor runtime wrappers
- loader relationship resolution
- representative integration fixtures

The design passes only if those surfaces can be aligned without inventing hidden compatibility logic for removed concepts.

### Step 6: Review Completeness

Perform an explicit red-team review:

- What still depends on removed names or sentinel nodes?
- What is still underspecified?
- What is still only "conceptually fine" but not operationally provable?
- What valid use case still feels awkward or unnatural in the model?

---

## Pass/Fail Criteria

The v2.0 design pressure-test passes only if all of the following are true:

- Every invariant in this checklist has at least one positive proof.
- Every hostile specimen fails for the intended reason.
- No critical implementation path requires `TypeDescriptor` or `MetaTypeDescriptor` as active schema nodes.
- No critical implementation path depends on stale header semantics if the active schema has moved to the v2.0 header model.
- Generic descriptor relationships can be modeled without reintroducing a fake universal descriptor node.
- Relationship direction, inheritance, and runtime descriptor resolution remain coherent under the actual v2.0 graph.
- The replacement crosswalk for removed v1.1 concepts is complete and unambiguous.

The pressure-test fails if any of the following occur:

- a valid specimen cannot be represented cleanly
- an invalid specimen is accepted
- implementation requires undocumented compatibility shims to make the design usable
- two different readers can reasonably infer different answers to the same structural question
- a removed v1.1 concept still functions as an unspoken dependency

---

## Recommended Deliverables

A serious pressure-test run should produce:

- an invariant checklist with results
- a specimen inventory with expected outcomes
- a replacement crosswalk from v1.1 to v2.0 concepts
- a short list of unresolved questions or underspecified edges
- a list of implementation surfaces that still require manual reconciliation

---

## Red-Team Questions

Use these questions when the model appears "mostly right" but confidence is still low:

- Can the loader resolve descriptor endpoints without a `TypeDescriptor` sentinel?
- Can bootstrap complete without inheritance ambiguity?
- Can every ordinary runtime holon be validated from a concrete descriptor plus inherited obligations?
- Is `DescriptorRoot` being used only where descriptor-generic targeting is truly intended?
- Are there any places where `Extends` is doing work that really belongs to `DescribedBy`?
- Are any abstract anchors accidentally being treated as runtime instance targets?
- Can the design explain inverse relationship rewriting without borrowing old semantics?
- If a new TypeKind were added, is it obvious where it would fit in the model?

If any answer is unclear, capture that as a design gap rather than deferring it into implementation.

---

## Relationship to Schema Ripple

This checklist pressure-tests the design.

The schema-ripple process operationalizes the consequences of accepted schema changes across implementation surfaces.

The two disciplines complement each other:

- use this checklist to increase confidence that the model is right
- use schema-ripple procedures to make sure accepted model changes are carried through the codebase consistently
