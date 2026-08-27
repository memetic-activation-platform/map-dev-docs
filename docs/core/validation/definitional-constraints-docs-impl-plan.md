# First-Class Definitional Constraints Documentation Implementation Plan

> **Status:** In progress — DOC3 is complete; DOC6 final consistency/build verification remains
> for [Issue 23](https://github.com/memetic-activation-platform/map-dev-docs/issues/23).

## Purpose

This plan updates MAP's documentation so that Schema 2.0 has one coherent account of
definitional constraints: configured invariants attached to type definitions as first-class
constraint holons. It separates those invariants from `ValidationRule` identities that represent
fixed, structural, contextual, or diagnostic validation obligations.

This is a documentation-only plan. It does not schedule changes to `map-holons`, Core TDL,
generated JSON, Rust dispatch, fixtures, or Commit runtime behavior. Once the documentation
design is accepted, a separate implementation plan must identify the corresponding schema and
runtime migration.

## Progress

- [x] DOC1 — shared vocabulary and classification boundary
- [x] DOC2 — generalized Schema 2.0 constraint semantics
- [x] DOC3 — value and relationship constraint reconciliation, including the Core constraint
  meta-model, normalized concrete types, configuration contracts, and cardinality authoring model
- [x] DOC4 — validation architecture and Commit contracts
- [x] DOC5 — TDL and implementation-planning documentation
- [ ] DOC6 — consistency review and documentation acceptance (rerun after DOC3 correction)

DOC5 includes explicit TDL authoring and lowering contracts, including `rule_of`, in TDL
Specification v0.11 and the revised VAL0/Capability sequence. DOC6 remains pending its final
strict documentation build.

## Desired documentation end state

The updated documents must consistently describe the following model:

```text
TypeDescriptor
  -[Constraints]-> Constraint
  -[ValidationBindings]-> ValidationRule

ConstraintType
  -[ApplicableToDescriptorTypes]-> TypeDescriptor*

Rule
  -[RuleOf]-> Schema
```

`Constraints` names configured, persistent invariants that participate in a type definition.
`ValidationBindings` names the remaining Commit checks that are not represented by a configured
constraint. Both relationships are additive through `Extends`.

A constraint and a validation rule remain ordinary holons. Each is validated through its own
`DescribedBy` type when it is staged for Commit. No relationship between a `Constraint` and a
`ValidationRule` is introduced in this documentation change. Initial execution may dispatch
statically from either canonical identity.

The model does not move descriptor-aware semantics into PVL or make validation behavior
runtime-pluggable.

## Documentation boundaries

The plan distributes normative claims to their existing owners rather than creating a competing
cross-cutting design specification:

| Concern | Authoritative destination |
| --- | --- |
| Generic constraint model, relationships, applicability, inheritance, and bootstrap semantics | `type-system/schema-design-spec.md` and `type-system/descriptor-semantics-rules.md` |
| Value-specific constraint semantics | `type-system/value-constraints-design-spec.md` |
| Relationship cardinality and non-constraint policy boundary | `type-system/relationship-constraints-design-spec.md` |
| Commit rule vocabulary, constraint/rule distinction, and validation execution | `validation/validation-schema-design-spec.md` and `validation/commit-validation-design-spec.md` |
| Layering and PVL boundary | `validation/validation-arch.md`, `validation/dependency-gravity.md`, and `validation/pvl-design-spec.md` only where an explicit non-change must be recorded |
| TDL source meaning, including explicit `rule_of`, and deferred compiler/lowering work | `type-system/tdl/tdl-spec.md` and `type-system/tdl/tdl-impl-plan-v2.md` |
| Future implementation sequencing | `validation/commit-validation-impl-plan.md` and any later `map-holons` plan |

## Documentation delivery sequence

### DOC1 — Establish the shared vocabulary and classification boundary

Update the type-system and validation design documents to define `Constraint`, `ConstraintType`,
and the limited role retained by `ValidationRule`.

The update must include a rule-inventory crosswalk that classifies the currently named Commit
checks into:

- parameterized definitional constraints;
- parameterless definitional constraints, where justified;
- fixed descriptor-kernel or PVL invariants; and
- contextual or aggregate validation.

The crosswalk must at least classify the current value constraints, required-property presence,
native value-kind conformance, `DS-STRUCT-*`, `DS-SCHEMA-*`, `DS-KIND-*`, `DS-CONTRACT-*`,
`DS-BIND-*`, `DS-DEFAULT-*`, `DS-KEY-*`, `DS-REL-*`, `DS-OCC-*`, and `DS-CARD-001`.

Decisions required before subsequent documentation updates:

1. `Constraints` remains the generic relationship name; no parallel
   `DefinitionalConstraints` relationship is introduced.
2. `Constraint` becomes the general root; the existing value-constraint hierarchy becomes a
   specialized branch.
3. `ValidationRule` remains distinct and is not a second store for constraint parameters.
4. `DS-CARD-001` remains a stable validation/diagnostic identity while evaluating an effective
   cardinality constraint.
5. `IsValueRequired`, endpoint declarations, duplicate policy, ordering policy, definitional
   status, and deletion semantics remain structural members unless a later focused design makes
   a case for promoting an individual concept to a constraint.

Exit condition: each term has one definition, each current rule family has a provisional
classification, and no document calls `ValidationBindings` the sole representation of a
definitional invariant.

### DOC2 — Generalize Schema 2.0 constraint semantics

Update `type-system/schema-design-spec.md` and
`type-system/descriptor-semantics-rules.md`.

Required changes:

- generalize the `Constraints` relationship target from the value-only hierarchy to `Constraint`;
- define the inverse relationship and ownership of occurrences;
- retain additive effective-value resolution and define constraint contribution provenance;
- define `ConstraintType -[ApplicableToDescriptorTypes]-> TypeDescriptor*`, whose targets are
  matched through the constrained descriptor's `Extends` lineage;
- define descriptor/schema self-conformance for incompatible attachment, malformed configuration,
  and attempted relaxation of inherited constraints;
- distinguish applicability from validator execution context; and
- define the bootstrap boundary: ordinary typed constraint holons, fixed structural semantics,
  and no recursive dynamic validator resolution.

Exit condition: the core type-system documents can determine whether a constraint attachment is
well formed and whether a subtype has preserved inherited obligations without relying on a
validation implementation plan.

### DOC3 — Reconcile specialized value and relationship semantics

Update `type-system/value-constraints-design-spec.md` and
`type-system/relationship-constraints-design-spec.md`.

Required changes:

- recast the value-constraint document as the value-family specialization of the generic model;
- specify the Core `Constraint` / `ConstraintType` / `MetaConstraintType` model, the initial
  concrete constraint-type inventory, each type's configuration members, and the distinction
  between a constraint-type declaration and an authored configured constraint instance;
- preserve current value semantics, including Unicode length semantics and monotonicity, unless a
  separately accepted design changes them;
- specify the initial normalized constraint inventory where needed, including whether separate
  minimum/maximum types become one optional-bound range or length type;
- move directional relationship cardinality from descriptor scalar properties to a configured
  cardinality constraint in the target design; and
- explicitly retain endpoint, duplicate, ordering, definitional, and deletion declarations as
  relationship descriptor policy rather than treating them as one undifferentiated constraint
  family.

Exit condition: value and relationship documents agree on the generic relationship, applicability
model, inheritance behavior, and what remains non-constraint descriptor structure.

### DOC4 — Reconcile validation architecture and Commit contracts

Update the validation documents after DOC2 and DOC3 establish their semantic inputs:

- `validation/validation-schema-design-spec.md`;
- `validation/commit-validation-design-spec.md`;
- `validation/validation-arch.md`; and
- `validation/dependency-gravity.md`.

Required changes:

- revise Commit discovery so it collects effective constraints and effective validation bindings
  separately;
- specify that a constraint supplies its own configuration while a rule supplies only the
  identity and metadata appropriate to its retained role;
- describe static constraint-type dispatch without implying dynamic implementation loading;
- preserve static validation-rule dispatch for fixed and contextual rules;
- state how staged constraint holons and staged validation-rule holons are themselves validated
  through their governing descriptors; and
- preserve the descriptor-independent PVL boundary without duplicating PVL semantics.

Exit condition: Commit documentation describes one ordered validation flow, does not require a
rule-to-constraint association holon, and does not imply that all validation obligations are
constraints.

### DOC5 — Align language and implementation-planning documentation

Update:

- `type-system/tdl/tdl-spec.md`;
- `type-system/tdl/tdl-impl-plan-v2.md`;
- `validation/commit-validation-impl-plan.md`; and
- dependency references in `docs/roadmap/desc-driven-impl-plan.md`, if the revised VAL0 boundary
  changes stated sequencing.

Required changes:

- state that TDL authors generalized constraint holons, relationships, and explicit `rule_of`
  provenance as ordinary schema content; the specified syntax/lowering implementation remains a
  follow-on concern;
- remove assumptions that `ValidationRule` / `ValidationBindings` are the sole Core vocabulary
  for descriptor-defined Commit semantics;
- replace the current VAL0 description with a documentation-approved target vocabulary and mark
  Core TDL, generated JSON, and runtime work as implementation follow-ons; and
- keep implementation sequencing out of the design specs themselves.

Exit condition: a reader cannot begin VAL0 from the documentation and accidentally implement the
superseded binding-only model.

### DOC6 — Consistency review and documentation acceptance

Perform a final cross-document review.

Verification includes:

- search all active Core documentation for `ValidationBindings`, `ValidationRule`, `Constraints`,
  `ValueConstraintType`, `MinCardinality`, and `MaxCardinality`;
- verify that every remaining use of descriptor cardinality properties is either historical,
  explicitly transitional, or intentionally non-target behavior;
- verify links and the scoped-authority claims against `docs/core/document-role-manifest.md`;
- ensure no active document introduces a new specialized per-constraint relationship family;
- ensure design documents contain no issue-specific delivery checklists; and
- run the repository's applicable Markdown/link validation, if available.

Exit condition: the documents have a single vocabulary and ownership model, and the issue's
documentation acceptance criteria can be evaluated without inspecting `map-holons`.

## Dependencies and ordering

`DOC1` is the decision gate. `DOC2` and `DOC3` may proceed together after it. `DOC4` depends on
their completed semantic model. `DOC5` depends on `DOC4`. `DOC6` is last.

```text
DOC1
 ├── DOC2 ──┐
 └── DOC3 ──┼── DOC4 ── DOC5 ── DOC6
            └─────────────────────┘
```

No `map-holons` implementation work is a dependency of this documentation plan. Conversely, this
plan must complete before a revised Core TDL or Commit-validation implementation plan is treated
as ready for implementation.

## Out of scope

- Editing `map-holons/schema-src`, generated JSON, Rust crates, tests, or fixtures.
- Defining dynamic `ValidationImplementation` selection or executable plugin behavior.
- Changing PVL's fixed Integrity contract.
- Making speculative performance, caching, flattening, or `EffectiveDescriptor` decisions.
- Settling unrelated relationship deletion semantics.

## Documentation definition of done

The Issue 23 documentation work is complete when DOC1 through DOC6 are complete, the active
specifications agree on the target model, and the repository has a clear handoff describing the
subsequent `map-holons` schema/runtime planning work without embedding that implementation plan in
these design documents.
