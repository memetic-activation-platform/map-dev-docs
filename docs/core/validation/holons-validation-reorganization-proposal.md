# Holons Validation Reorganization Proposal

> **Status:** Deferred proposal for reference; not an implementation commitment.
>
> **Repository baseline:** `map-holons` `d0169c37`, reviewed on 2026-10-14.

Reorganize `shared_crates/holons_validation` around assessment orchestration, bound rules, and
configured constraints. Consolidate small supporting modules so the directory structure explains
the execution responsibilities without multiplying files unnecessarily. This work can be undertaken
independently when useful; it is not a prerequisite for Capability 3 or Capability 4.

The [Commit Validation Design Specification](commit-validation-design-spec.md) remains authoritative
for behavior and contracts. The [implementation plan](commit-validation-impl-plan.md) owns capability
delivery. This proposal concerns internal Rust organization and introduces no new validation semantics.

**Why reorganize.** At the reviewed baseline, the crate has 24 Rust files, including four test/support
files. Its production files contain approximately 4,439 lines. The flat directory mixes orchestration,
prepared inputs, rule implementations, findings, and tests. `handlers.rs` mixes conformance rules with
finding construction; `registries.rs` contains invocation contracts as well as static registries.
Together, those two files are only 285 lines, so splitting them into five files would be excessive.

**Proposed structure.** Keep three implementation groups and two shared supporting modules:

```text
src/
  lib.rs
  dispatch.rs
  diagnostics.rs

  assessment/
    mod.rs
    commit.rs
    subjects.rs
    contexts.rs
    descriptor_package.rs
    schema_view.rs
    dependency_groups.rs
    prospective.rs
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
```

- `assessment/` constructs prospective inputs, schedules readiness, traverses subjects, and installs
  completed outcomes. Read-only assessment and controlled outcome installation remain distinct.
- `rules/` implements non-constraint judgments selected through effective `ValidationBindings`.
- `constraints/` assesses constraint declarations and, as capabilities deliver them, evaluates
  configured invariants. Declaration validity remains distinct from subject evaluation support.
- `dispatch.rs` contains shared invocation/contribution contracts and static registry lookup.
- `diagnostics.rs` owns finding construction, collection, observations, and completed reports.
- `tests/` collects existing unit tests and their shared fixtures under explicit test-only wiring.

`lib.rs` and each `mod.rs` contain wiring and re-exports, not business logic or type definitions.

**File mapping.** Preserve existing implementation bodies and descriptive comments while moving them:

| Current file or contents | Proposed destination |
|---|---|
| `commit_assessment.rs` and `assessment_phase.rs` | `assessment/commit.rs` |
| `subject_assessment.rs` | `assessment/subjects.rs` |
| `contexts.rs` | `assessment/contexts.rs` |
| `descriptor_package.rs` | `assessment/descriptor_package.rs` |
| `schema_view.rs` | `assessment/schema_view.rs` |
| `dependency_groups.rs` | `assessment/dependency_groups.rs` |
| `prospective.rs` | `assessment/prospective.rs` |
| `assessment_support.rs` | `assessment/support.rs` |
| `outcomes.rs` | `assessment/outcomes.rs` |
| Conformance rules and native-kind helpers in `handlers.rs` | `rules/conformance.rs` |
| `descriptor_rules.rs` | `rules/descriptor.rs` |
| `schema_rules.rs` | `rules/schema.rs` |
| `constraint_declarations.rs` | `constraints/declarations.rs` |
| `registries.rs`, `commitments.rs`, and subject contracts in `subjects.rs` | `dispatch.rs` |
| `collector.rs`, `report.rs`, and finding helpers in `handlers.rs` | `diagnostics.rs` |
| `subject_assessment_tests.rs` | `tests/subjects.rs` |
| `schema_assessment_tests.rs` | `tests/schema.rs` |
| `constraint_declarations_tests.rs` | `tests/constraint_declarations.rs` |
| `test_support.rs` | `tests/support.rs` |

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
| Additional evaluator variants and compatible invocation routes | `dispatch.rs` |

Keep `dispatch.rs` focused on shared execution contracts and lookup. As relationship inputs become
substantial, place their subject-specific definitions alongside `assessment/relationships.rs` rather
than collecting all prepared products in one shared file.

The proposed `StaticConstraintEvaluator` enum accommodates typed value and relationship-bucket
evaluators. Introducing that contract belongs to evaluator implementation, not to this mechanical
reorganization. Cardinality evaluates a prospective directional bucket, including empty buckets;
it is not an intrinsic check on one relationship occurrence.

Commit and the Reference Layer retain ownership of authoritative bucket retrieval, relationship
delta normalization, paired persistence preparation, and source-chain conflict retries. Relationship
assessment consumes supplied read-only prospective inputs. C4's pre-write PVL checks remain in
Commit persistence orchestration using the existing descriptor-independent PVL implementation;
PVL refusals are not converted into descriptor-semantic findings. See the
[relationship persistence specification](../transactions/relationship-persistence-design-spec.md).

**Naming.** Follow Commit Validation Design Specification §5.2 for new functions: `assess_*` records
findings, `evaluate_*` applies one configured constraint, `dispatch_*` invokes a bound rule handler,
and `prepare_*` / `construct_*` build inputs. Only `validate_commit_candidates` and its controlled
entry-point variant decide and install candidate outcomes. Registry `lookup` follows §5.3's explicit
contract. Suitable constraint names are `StaticConstraintEvaluator` and
`StaticValueConstraintEvaluator`; preserve current names during a purely mechanical move unless a
separate naming change is deliberately included.

**Migration sequence.**

1. Recheck the current crate and update this mapping for any C3/C4 additions since the baseline.
2. Move production modules into the three groups and consolidate the shared contracts and diagnostics.
   Update internal imports, preserving current public crate-root exports and external signatures.
3. Move test files under `tests/`, preserving their fixtures, coverage, and access to crate internals.
   Replace the existing nested `#[path]` wiring with ordinary test-module declarations.
4. Review the diff as a structural change. Preserve finding codes/provenance, dispatch behavior,
   assessment ordering, preparation/readiness boundaries, and operational-error handling.
5. Run existing relevant unit tests, `npm run fmt:check`, and `npm run check`, including hApp/WASM
   reachability. Report unavailable checks. No new behavior tests are required solely for file moves.

The completed reorganization should leave one assessment path, unchanged public exports and
serialization, and no new storage, persistence, or descriptor-resolution surface. Dependency updates,
Unicode testing, array representation, schema activation, and additional evaluator implementations
remain separate work.
