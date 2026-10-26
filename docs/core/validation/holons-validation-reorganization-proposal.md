# Holons Validation Reorganization Proposal

> **Status:** Planned in two steps. Step A ships with VAL-C3a (#811), after readiness retirement
> (#831) lands; Step B follows the package construction and scheduler work (#822).
>
> **Repository baseline:** `map-holons` `245fc402` (after #829), reviewed on 2026-10-27. Rows
> affected by #831 describe the crate as that issue leaves it.

Reorganize `shared_crates/holons_validation` around assessment orchestration, bound rules, and
configured constraints. Consolidate small supporting modules so the directory structure explains
the execution responsibilities without multiplying files unnecessarily. Neither step is a
prerequisite for Capability 3 or Capability 4.

The [Commit Validation Design Specification](commit-validation-design-spec.md) remains authoritative
for behavior and contracts. The [implementation plan](commit-validation-impl-plan.md) owns capability
delivery. This proposal concerns internal Rust organization and introduces no new validation semantics.

**Why reorganize.** At the reviewed baseline, the crate has 29 Rust files, including seven test/support
files. Its production files contain approximately 4,808 lines. The flat directory mixes orchestration,
prepared inputs, rule implementations, findings, and tests. `handlers.rs` mixes conformance rules with
finding construction; `registries.rs` contains invocation contracts as well as static rule metadata.
#831 consolidates that metadata into one registration per built-in rule but keeps both files small,
so splitting them into five files would be excessive.

**Proposed structure.** Keep three implementation groups and two shared supporting modules:

```text
src/
  lib.rs
  commitments.rs
  dispatch.rs
  diagnostics.rs

  assessment/
    mod.rs
    commit.rs
    subjects.rs
    descriptor_package.rs
    schema_view.rs
    dependency_groups.rs
    key_evidence.rs
    graph_only_deltas.rs
    support.rs
    outcomes.rs

  rules/
    mod.rs
    conformance.rs
    descriptor.rs
    schema.rs

  constraints/
    mod.rs
    declarations.rs

  tests/
    mod.rs
    support.rs
    subjects.rs
    schema.rs
    constraint_declarations.rs
    key_uniqueness.rs
    graph_only_deltas.rs
    core_successors.rs
```

- `assessment/` constructs prospective inputs, schedules readiness, traverses subjects, and installs
  completed outcomes. Read-only assessment and controlled outcome installation remain distinct.
- `rules/` implements non-constraint judgments selected through effective `ValidationBindings`.
- `constraints/` assesses constraint declarations and, as capabilities deliver them, evaluates
  configured invariants. Declaration validity remains distinct from subject evaluation support.
- `dispatch.rs` contains shared invocation/contribution contracts, `SubjectLevel`, and the
  per-rule registration: implementation route, subject level, family and declaring roles, native
  kind, diagnostic code, prerequisite flag, and subject applicability. A registration selects
  implementation logic; it does not establish definition identity, authority, or validity.
- `commitments.rs` stays separate: resolved bindings and constraints are prepared inputs, not
  dispatch contracts, and their shape may change with evaluator inputs and package preparation.
- `diagnostics.rs` owns finding construction, collection, observations, and completed reports.
- `tests/` collects existing unit tests and their shared fixtures under explicit test-only wiring.

`lib.rs` and each `mod.rs` contain wiring and re-exports, not business logic or type definitions.

**File mapping.** Preserve existing implementation bodies and descriptive comments while moving them:

| Current file or contents | Proposed destination | Step |
|---|---|---|
| Conformance rules in `handlers.rs` | `rules/conformance.rs` | A |
| `descriptor_rules.rs` | `rules/descriptor.rs` | A |
| `schema_rules.rs` | `rules/schema.rs` | A |
| `constraint_declarations.rs` | `constraints/declarations.rs` | A |
| `registries.rs`, `SubjectLevel` from `contexts.rs`, and subject contracts in `subjects.rs` | `dispatch.rs` | A |
| `collector.rs`, `report.rs`, and finding helpers in `handlers.rs` | `diagnostics.rs` | A |
| `commitments.rs` | unchanged | — |
| `commit_assessment.rs` and `assessment_phase.rs` | `assessment/commit.rs` | B |
| `subject_assessment.rs` | `assessment/subjects.rs` | B |
| Remaining `ValueValidationContext` in `contexts.rs` | `assessment/support.rs` | B |
| `descriptor_package.rs` | `assessment/descriptor_package.rs` | B |
| `schema_view.rs` | `assessment/schema_view.rs` | B |
| `dependency_groups.rs` | `assessment/dependency_groups.rs` | B |
| `key_evidence.rs` | `assessment/key_evidence.rs` | B |
| `graph_only_deltas.rs` | `assessment/graph_only_deltas.rs` | B |
| `assessment_support.rs` | `assessment/support.rs` | B |
| `outcomes.rs` | `assessment/outcomes.rs` | B |
| `subject_assessment_tests.rs` | `tests/subjects.rs` | B |
| `schema_assessment_tests.rs` | `tests/schema.rs` | B |
| `constraint_declarations_tests.rs` | `tests/constraint_declarations.rs` | B |
| `key_uniqueness_tests.rs` | `tests/key_uniqueness.rs` | B |
| `graph_only_deltas_tests.rs` | `tests/graph_only_deltas.rs` | B |
| `core_successor_tests.rs` (replaces `required_anchor_tests.rs` in #831) | `tests/core_successors.rs` | B |
| `test_support.rs` | `tests/support.rs` | B |

`prospective.rs` has no destination: #831 removes its anchor resolution and interim required-anchor
restriction. If anything remains there after #831, map it during Step B.

Step A covers the rule, constraint, dispatch, and diagnostics files. #831 rewrites several of them
(rule registration, native-kind metadata, descriptor forwarding functions, and contract and
constraint roots), so Step A follows #831 to keep the move separate from behavior changes. Step B
covers the construction and scheduling files that #822 is changing, so its rows are provisional. In
particular, #831 removes the `ReadinessResolution` phase, and `assessment_phase.rs` may still warrant
its own module rather than a merge into `commit.rs`.

Keep `PreparedAssessment` and its outcome-installation operations in `assessment/outcomes.rs` rather
than folding them into diagnostics. Grouping reports with collectors does not grant either permission
to mutate staged subjects.

**Capability growth.** Add files when the corresponding functionality exists; do not create empty
placeholders as part of the reorganization.

| Delivered functionality | Natural location |
|---|---|
| C3 scalar evaluators | `constraints/values.rs` |
| C3 enum membership and property conformance rules | `rules/conformance.rs` |
| C3 enum/default definition checks | `rules/descriptor.rs` |
| C4 relationship traversal and bounded aggregate assessment | `assessment/relationships.rs` |
| C4 occurrence and relationship rule implementations | `rules/relationships.rs` |
| C4 configured cardinality evaluation | `constraints/relationships.rs` |
| DS-SCHEMA-002 restoration (#836): subject applicability and rule implementation | registration in `dispatch.rs`; `rules/schema.rs` |
| Additional evaluator variants and compatible invocation routes | `dispatch.rs` |

Keep `dispatch.rs` focused on shared execution contracts and lookup. As relationship inputs become
substantial, place their subject-specific definitions alongside `assessment/relationships.rs` rather
than collecting all prepared products in one shared file.

The proposed `StaticConstraintEvaluator` enum accommodates typed value and relationship-bucket
evaluators. Introducing that contract belongs to evaluator implementation, not to this mechanical
reorganization. Cardinality evaluates a prospective directional bucket, including empty buckets;
it is not an intrinsic check on one relationship occurrence.

EffectiveDescriptor construction belongs with the descriptor kernel or the guest, not in
`holons_validation`. Validation consumes it through its prepared inputs; the reorganization creates
no module for it.

Commit and the Reference Layer retain ownership of authoritative bucket retrieval, relationship
delta normalization, paired persistence preparation, and source-chain conflict retries. Relationship
assessment consumes supplied read-only prospective inputs. C4's pre-write PVL checks remain in
Commit persistence orchestration using the existing descriptor-independent PVL implementation;
PVL refusals are not converted into descriptor-semantic findings. See the
[relationship persistence specification](../transactions/relationship-persistence-design-spec.md).

**Naming.** Follow Commit Validation Design Specification §5.2 for new functions: `assess_*` records
findings, `evaluate_*` applies one configured constraint, `dispatch_*` invokes a bound rule handler,
and `prepare_*` / `construct_*` build inputs. Only `validate_commit_candidates` and its controlled
entry-point variant decide and install candidate outcomes. Rule registration follows §5.3's explicit
contract, as updated by #831. Suitable constraint names are `StaticConstraintEvaluator` and
`StaticValueConstraintEvaluator`; preserve current names during a purely mechanical move unless a
separate naming change is deliberately included.

**Migration sequence.**

1. **Step A**, the first commit of VAL-C3a, after #831 lands: create `rules/`, `constraints/`, `dispatch.rs`, and
   `diagnostics.rs` from the Step A rows, keeping the move separate from evaluator changes. New
   scalar evaluators then land directly in `constraints/values.rs`.
2. **Step B**, after #822 lands: recheck the crate, update the Step B rows for
   any new or replaced construction modules, and decide whether assessment phase metrics belong with
   assessment or diagnostics. Then move `assessment/` and `tests/`, replacing the existing nested
   `#[path]` wiring with ordinary test-module declarations.
3. In each step, update internal imports while preserving public crate-root exports and external
   signatures as they stand after #831, which deliberately removes `StaticRuleRegistry`,
   `resolve_validation_anchor`, `AnchorResolutionError`, `ContractKindRoots`, and
   `ConstraintDeclarationRoots`. Do not reintroduce assessment anchor resolution. Review the diff as
   a structural change. Preserve finding codes/provenance, dispatch
   behavior, assessment ordering, preparation/readiness boundaries, and operational-error handling.
4. In each step, run existing relevant unit tests, `npm run fmt:check`, and `npm run check`, including
   hApp/WASM reachability. Report unavailable checks. No new behavior tests are required solely for
   file moves.

The completed reorganization should leave one assessment path, unchanged public exports and
serialization, and no new storage, persistence, or descriptor-resolution surface. Dependency updates,
Unicode testing, array representation, schema activation, and additional evaluator implementations
remain separate work.
