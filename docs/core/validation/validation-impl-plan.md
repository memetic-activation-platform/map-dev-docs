# Validation Implementation Plan v3.0
## Descriptor-Aware Validation Delivered as Vertical Capabilities

## Purpose

This plan delivers Descriptor-Aware Holon Validation as a sequence of usable capabilities rather
than as horizontal framework layers. Each delivery unit proves that real schema-authored
`ValidationRule` commitments can accept or reject real holons through a consumer-facing validation
entry point.

The first capability must establish the complete path:

```text
Validation Schema package
  -> ValidationBinding
  -> effective rule collection
  -> built-in rule dispatch
  -> ValidationResult
  -> blocking consumer decision
```

Subsequent capabilities extend that path with additional rule families and the Nursery and Runtime
Recognition consumers. They do not create parallel validation mechanisms. Dance, Application,
Trust, Attestation, and social-validation consumers remain outside this implementation sequence.

This plan owns Descriptor-Aware Holon Validation above descriptor-independent PVL. It owns
validation contexts, rule coordination, result accumulation, schema-backed rule applicability,
and reusable consumer entry points. It does not own descriptor retrieval, descriptor-kernel
effective-product computation, default materialization, TypeActivation, or Holochain Integrity
callbacks.

The [Validation Architecture](validation-arch.md) defines validation layers and execution
boundaries. The [Validation Schema Design Spec](validation-schema-design-spec.md) defines the
Validation Schema package and its holonic object model. The
[Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md) define the
meaning of Schema 2.0 `DS-*` rules. This plan wires those meanings into executable validation; it
must not reimplement descriptor inheritance, effective-contract, endpoint-compatibility, or
conformance algorithms.

## Delivery Principles

- A delivery unit is complete only when it demonstrates an observable accept/reject outcome for a
  real holon through a real consumer path.
- A `ValidationRule` holon and `ValidationBinding` are commitments, not executable behavior by
  themselves. A capability must prove both selection and execution.
- Rules execute only where the caller supplies the bounded context they require.
- The descriptor-aware crate consumes caller-supplied descriptor-runtime products. It never pulls
  descriptor-runtime dependencies into descriptor-independent PVL or the Integrity Zome.
- Initial execution uses static function or enum dispatch keyed by canonical rule identity. Do not
  introduce per-family trait hierarchies or boxed factories until multiple execution engines or
  extension-authored implementations require them.
- A temporary `PLANNED_RULE_KEYS` static slice identifies known MAP-seeded rules not yet
  implemented. A coverage test keeps the implemented registry and planned set disjoint and requires
  their union to equal the seeded corpus. Enforced or unknown mandatory rules fail closed with
  `UnsupportedValidationRule`; delete the planned set when the seeded corpus is implemented.
- Each capability adds to the existing validator, rule registry, fixtures, and diagnostics. No
  capability replaces earlier rule selection or result semantics.

## Precursor — VAL0: Validation Schema Corpus and Package Load

`VAL0` delivers the schema/data foundation, not runtime enforcement:

- Validation Schema TDL and its generated JSON artifact;
- `ValidationRule`, `ValidationBinding`, `AppliesTo`, and `UsesRule` definitions;
- MAP-seeded `ValidationRule` identities and bindings, including every stable `DS-*` authority;
- single-transaction Core and Validation Schema bootstrap acceptance; and
- documentation of Validation Schema ownership.

The bootstrap follows the dependency and co-staging model defined by the
[Validation Architecture](validation-arch.md).

After VAL0, a schema can declare a validation commitment, but no runtime path yet selects or
executes it. The capabilities below make that corpus operational.

---

# Capability 1 — Basic Descriptor-Aware Holon Conformance

## Outcome

The Holon Data Loader can reject an authored holon because an applicable, seeded Validation Schema
commitment fails. This is the first end-to-end proof of Descriptor-Aware Holon Validation.

## Scope

- Create the WASM-safe `holons_validation` crate, distinct from the PVL/Integrity-focused
  `pvl_validation` crate.
- Define only the typed contexts, result types, entry point, and static dispatch required by this
  capability.
- Resolve the caller-supplied descriptor and its effective contract through descriptor-runtime
  APIs; do not duplicate descriptor-kernel logic.
- Invoke exactly-one `DescribedBy` directly because descriptor binding is required before effective
  bindings can be discovered; use binding collection for the remaining rules.
- Collect seeded `ValidationBinding`s over the `Extends` lineage of each governing descriptor this
  cohort requires: the describing type, each declared property descriptor, and each selected
  ValueType.
- In `holons_validation`, introduce a lightweight `ValidationSession` that carries the current mode
  and bounded context, owns one immutable `ValidationBindingCatalog`, and memoizes effective rule
  sets by governing descriptor identity. Capability 1 constructs it once per loader transaction;
  Capability 5 reuses it in generalized commit and recognition paths.
- Add the static implementation registry, keyed by canonical rule identity and recording required
  mode/context compatibility, plus the temporary `PLANNED_RULE_KEYS` set defined above.
- Dispatch registered rules through plain functions or a small typed handler enum. Block missing
  enforced implementations and unknown mandatory rules.
- Validate the minimum holon-conformance cohort:
  - exactly one `DescribedBy` target;
  - required-property presence;
  - no undescribed populated properties; and
  - BaseValue-versus-ValueType native-kind compatibility.
- Integrate the entry point into the authored-content Holon Data Loader path and return a stable,
  actionable blocking result.
- Add one shared happy-path fixture and focused failing fixtures for each member of the cohort.
- Add the seeded-corpus coverage test defined above.

## Initial loader integration

Capability 1 uses the smallest safe pre-commit integration:

```text
loader resolution
    -> default population
    -> construct binding catalog
    -> validate staged authored holons
    -> return Skipped when blocking violations exist
    -> context.commit() only when validation passes
```

The loader invokes this gate immediately after default population and before `context.commit()` in
`happ/crates/holons_loader/src/controller.rs`. This is transitional: Capability 5 moves the same
reusable validator and transaction-scoped catalog into generalized guest commit orchestration in
`happ/crates/holons_guest/src/guest_shared_objects/commit_functions.rs`.

## Non-goals

- Descriptor-holon self-conformance beyond what is necessary to obtain the supplied descriptor.
- String/range/enum/key constraints, relationship semantics, transaction-wide rules, generalized
  Nursery commit integration, Runtime Recognition, persisted evidence, and dynamic implementation
  dispatch.
- Default materialization. The loader may supply already materialized content, but this capability
  does not create defaults.

## Dependencies

- VAL0 Validation Schema corpus and package-load acceptance.
- Descriptor Runtime Platform APIs that expose the descriptor and effective contract required for
  this cohort.

## Exit demonstration

Given a schema-loaded descriptor whose inherited effective bindings include
`RequiredPropertyPresence.ValidationRule`, loading an otherwise valid holon that omits the required
property produces a blocking `ValidationResult` and prevents commit. Equivalent fixtures prove the
other three rules and one valid holon commits successfully.

---

# Capability 2 — Descriptor Self-Conformance

## Outcome

Descriptor holons themselves are validated against Schema 2.0 structural and effective-contract
invariants through the dispatch, result, and loader path established by Capability 1, with rule
selection determined by invariant scope.

## Scope

- Invoke structural prerequisites directly before descriptor binding or effective-product
  computation that depends on them.
- Select per-descriptor rules through the descriptor holon's describing meta-type lineage
  `L(D(H))`; do not recurse into descriptor self-conformance during ordinary instance validation.
- Invoke schema-, package-, and kernel-scoped rules once over the completed schema closure rather
  than representing them as per-target `ValidationBinding`s.
- Implement the `DS-STRUCT-*` rules for `DescribedBy`, `Extends`, lineage termination, and
  descriptor-root invariants.
- Implement `DS-SCHEMA-*` rules for versioned schema dependency acyclicity, direct
  cross-schema dependency declarations, and Core accumulator baselines.
- Implement `DS-KIND-*` rules for explicit Instance TypeKind anchors, abstract anchors, root
  exceptions, and graph-derived describing-category pairing.
- Implement `DS-CONTRACT-*` rules for inherited-member redeclaration, unique member names,
  well-formed effective members, and member-kind compatibility.
- Preserve descriptor and member provenance in every accumulated violation.

## Non-goals

- Ordinary-instance property/value/relationship conformance beyond Capability 1.
- A second descriptor structure or effective-contract algorithm.

## Dependencies

- Capability 1.
- Descriptor Runtime Platform effective descriptor and descriptor-kernel products.

## Exit demonstration

Malformed descriptor fixtures fail through the shared entry point with deterministic `DS-*`
diagnostics and provenance; valid Core and Validation Schema packages continue to load.

---

# Capability 3 — Value, Enum, Default, and Key Conformance

## Outcome

The loader validates completed ordinary and descriptor holons against effective property contracts,
value constraints, enum declarations, default declarations, and key rules.

## Scope

- Extend the existing property and value delegation path; do not introduce separate validators for
  each consumer.
- Implement `DS-CONFORM-*`, `DS-BIND-*`, and `DS-PROP-*` beyond Capability 1's minimum cohort.
- Implement type-specific constraint evaluation, including string-length behavior pinned to
  Unicode 17.0.0 UAX #29 extended grapheme clusters without normalization, with shared native and
  WASM fixtures.
- Implement `DS-ENUM-*` unique effective member-name, exact-token-membership, and
  token-non-retroactivity checks.
- Implement validation of `DS-DEFAULT-*` declarations and completed explicit values. Default
  materialization remains the loader's responsibility.
- Implement `DS-KEY-*` effective selection, explicit keylessness, key presence, computed key
  value, and package/dependency-scope uniqueness when the supplied context can establish it.

## Non-goals

- Default materialization or an alternative key computation algorithm.
- Open-world uniqueness checks beyond the bounded package/dependency scope supplied by the
  validation context.

## Dependencies

- Capability 1.
- Capability 2 where a rule validates descriptor declarations.
- Loader default-materialization support for fixtures that require completed defaults.

## Exit demonstration

Loader fixtures demonstrate accepted and rejected string, enum, default, and key cases through
the same schema binding and result path used by Capability 1.

---

# Capability 4 — Relationship Conformance

## Outcome

Descriptor-aware relationship declarations and occurrences validate through the shared validator.
Rules requiring a transaction or graph view run only when that view is supplied.

## Scope

- Implement `DS-REL-*` inverse pairing, mirrored effective endpoints, and directional deletion
  semantic declarations.
- Implement `DS-OCC-*` occurrence grouping by resolved descriptor identity, endpoint
  compatibility, ordering/duplicate policy, and additional-relationship policy.
- Register `DS-CARD-001` as compatible only with contexts containing the required bounded Nursery
  or graph snapshot.
- Add relationship-specific result provenance and fixtures alongside the shared result model.

## Non-goals

- Pairwise execution of `Allow`/`Block`/`Cascade` deletion semantics until that design is settled.
- Open-world cardinality claims without a bounded, explicit graph context.

## Dependencies

- Capabilities 1 and 2.
- Descriptor Runtime Platform relationship products.
- Transaction or graph snapshot support for cardinality coverage.

## Exit demonstration

The loader validates bounded relationship declarations and occurrences. A transaction-aware
fixture additionally proves cardinality failure only when the required staged view is supplied.

---

# Capability 5 — Nursery and Runtime Recognition Adoption

## Outcome

Nursery commit orchestration and Runtime Recognition invoke one validation surface and interpret
the same deterministic results without changing semantic rule implementations.

## Scope

- Generalize the Capability 1 loader entry point into reusable holon and completed-schema-closure
  validation entry points. Operation and available context are session inputs, not separate
  validation engines.
- Move the transaction validation gate and binding-catalog construction from the loader into the
  generalized guest commit orchestration in `holons_guest`; validation must complete before the
  first persistence write.
- Support only `ValidationMode::Nursery` and `ValidationMode::RuntimeRecognition`. Each mode
  supplies its bounded context and interprets the shared report; no general profile framework is
  required.
- Reuse one session/catalog per Nursery transaction or activated recognition snapshot rather than
  rebuilding rule applicability for each holon.
- Provide shared result aggregation, outcome classification, fixtures, and diagnostics. Nursery
  blocks before commit; Runtime Recognition reports recognized, rejected, or indeterminate without
  turning recognition into a persistence gate.
- Retain explicit blocking behavior for enforced or unknown unsupported mandatory rules in the
  Nursery commit path.

## Non-goals

- Descriptor-independent PVL implementation or Integrity callback changes.
- Dynamic execution of arbitrary ValidationImplementation holons.
- Consumers excluded by this plan's scope, generic profiles, durable evidence, and receipts.

## Dependencies

- Capabilities 1–4, according to the rule families each consumer needs.
- Transaction infrastructure for Nursery validation.
- Activated descriptor and bounded runtime-read products for Runtime Recognition.

## Exit demonstration

Generalized guest commit orchestration and Runtime Recognition invoke the same reusable validator
with mode-specific bounded contexts. Nursery blocks before any persistence write, while recognition
returns a deterministic recognized, rejected, or indeterminate decision. The Capability 1 loader
gate is no longer a separate validation path.

---

# Rule-Family Delivery Map

| Rule family | First executable capability | Context limit |
| --- | --- | --- |
| Exactly-one `DescribedBy`, required/undescribed properties, native kind | Capability 1 | Supplied holon and descriptor/effective contract |
| `DS-STRUCT-*`, `DS-SCHEMA-*`, `DS-KIND-*`, `DS-CONTRACT-*` | Capability 2 | Resolved descriptor graph and kernel products |
| `DS-CONFORM-*`, `DS-BIND-*`, `DS-PROP-*`, `DS-ENUM-*`, `DS-DEFAULT-*`, `DS-KEY-*` | Capability 3 | Completed staged holon and bounded key scope where required |
| `DS-REL-*`, `DS-OCC-*`, `DS-CARD-001` | Capability 4 | Relationship/graph view; transaction snapshot for cardinality |
| Nursery and Runtime Recognition integration and diagnostics | Capability 5 | Transaction or activated-recognition snapshot |

# Superseded Horizontal Decomposition

The former separate foundation, context-family, holon, property, generic-value, type-specific
value, relationship, commitment-shape, descriptor-rule-coverage, orchestration, entry-point, and
consumer-integration units are no longer independently shippable milestones.

Their useful implementation tasks are retained within the smallest capability that needs them:

| Former concern | New home |
| --- | --- |
| Foundation types, typed contexts, descriptor-aware crate, static dispatch | Capability 1 |
| ValidationRule identity, seeded bindings, package bootstrap | VAL0; Capability 1 consumes them |
| Effective binding collection and unsupported-rule handling | Capability 1 |
| Descriptor structure and contract coverage | Capability 2 |
| Property/value/type-specific rule coverage | Capabilities 1 and 3 |
| Relationship validator and rule coverage | Capability 4 |
| Descriptor orchestration and shared entry points | Capability 1, generalized in Capability 5 |
| Loader integration | Capability 1 |
| Nursery and Runtime Recognition integration and diagnostics | Capability 5 |

This mapping is intentionally not a one-to-one migration of prior work-item identifiers. The MAP
Dev Tracking Sheet and cross-track dependency references must be reconciled to the five
capabilities before new implementation issues are opened.

# Relationship to Descriptor-Independent PVL

Descriptor-aware validation has no implementation dependency on the PVL implementation plan.
PVL remains a small, fixed, descriptor-independent set of integrity-safe functions and does not
consume this validator framework. The descriptor-aware crate may reuse compatible pure utilities
only where that does not make PVL depend on descriptor runtime, schema-loaded rules, dynamic
dispatch, or consumer contexts.

# Critical Path

1. VAL0: Validation Schema corpus and package-load acceptance.
2. Capability 1: basic descriptor-aware holon conformance through the loader.
3. Capability 2: descriptor self-conformance.
4. Capability 3: value, enum, default, and key conformance.
5. Capability 4: relationship conformance.
6. Capability 5: Nursery and Runtime Recognition adoption.

Capabilities 3 and 4 may proceed in parallel once their shared Capability 1/2 dependencies and
the necessary descriptor-runtime products are available.
