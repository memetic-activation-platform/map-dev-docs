# Commit Validation Implementation Plan v3.0
## Descriptor-Aware Commit Validation Delivered as Vertical Capabilities

## Purpose

This plan delivers Descriptor-Aware Holon Validation as a sequence of usable capabilities rather
than as horizontal framework layers. Each delivery unit proves that configured schema-authored
constraints and remaining schema-authored `ValidationRule` commitments can accept or reject real
holons through a consumer-facing validation entry point.

The first capability must establish the complete path:

```text
Core Schema Commit-validation vocabulary
  -> Constraints and ValidationBindings
  -> effective constraint and rule collection
  -> built-in constraint-type and rule dispatch
  -> ValidationResult
  -> blocking consumer decision
```

Subsequent capabilities extend that path with additional Commit rule families. Runtime Recognition,
Dance, Application, Trust, Attestation, and social-validation consumers require separate designs
and implementation plans; they remain outside this implementation sequence.

This plan owns Descriptor-Aware Holon Validation above descriptor-independent PVL. It owns
validation contexts, rule coordination, result accumulation, schema-backed rule applicability,
and reusable consumer entry points. It does not own descriptor retrieval, descriptor-kernel
effective-product computation, default materialization, TypeActivation, or Holochain Integrity
callbacks.

The [Commit Validation Design Specification](commit-validation-design-spec.md)
defines the target design delivered by this plan. The [Validation Architecture](validation-arch.md)
defines validation layers and execution boundaries. The
[Validation Extension Schema Design Spec](validation-schema-design-spec.md) defines the one-way
Validation Schema extension and its holonic object model. The
[Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md) define the
meaning of Schema 2.0 `DS-*` rules. This plan wires those meanings into executable validation; it
must not reimplement descriptor inheritance, effective-contract, endpoint-compatibility, or
conformance algorithms.

## Delivery Principles

- A delivery unit is complete only when it demonstrates an observable accept/reject outcome for a
  real holon through a real consumer path.
- A `Constraint` holon carries configured definitional semantics. An effective occurrence of
  `Constraints` makes it applicable. A `ValidationRule` holon names a remaining fixed or
  contextual commitment, and an effective `ValidationBindings` occurrence makes it applicable.
  A capability must prove both collection paths and their execution.
- Rules execute only where the caller supplies the bounded context they require.
- Every Commit validates every staged holon. `ValidationState` and prior validation diagnostics are
  outputs of an earlier pass, never a cache used to select or skip validation work; each pass
  refreshes validation-originated diagnostics while preserving unrelated Commit errors.
- The descriptor-aware crate consumes caller-supplied descriptor-runtime products. It never pulls
  descriptor-runtime dependencies into descriptor-independent PVL or the Integrity Zome.
- Initial execution uses static function or enum dispatch keyed by concrete constraint type and
  canonical rule identity. Do not introduce per-family trait hierarchies or boxed factories until
  multiple execution engines or extension-authored implementations require them.
- A `ValidationRule` may exist before it is implemented. It becomes active only when an applicable
  type declares an occurrence of `ValidationBindings` in the same delivered capability as a compatible handler.
  A coverage test requires every active binding to resolve to the static implementation registry.
  An active mandatory binding without a compatible handler fails closed with
  `UnsupportedValidationRule`.
- Each capability adds to the existing validator, rule registry, fixtures, and diagnostics. No
  capability replaces earlier rule selection or result semantics.

## Precursor — VAL0: Core Schema/TDL Vocabulary and Non-Strict Load

`VAL0` delivers the source/schema foundation, not runtime enforcement or strict Commit/bootstrap
acceptance. It proves that the target Core and Validation Schema source corpora parse, lower,
round-trip, and load through the available non-strict schema-loading path. An attached constraint
is not silently treated as executable merely because VAL0 can represent it.

- Core TDL and generated JSON for generic `Constraint` / `ConstraintType` /
  `MetaConstraintType`, abstract `Rule`, `RuleOf` / materialized `Rules`, `Constraints`, and the
  authored `ConstraintType -[ApplicableToDescriptorTypes]-> TypeDescriptor` / materialized
  `TypeDescriptor -[HasApplicableConstraintTypes]-> ConstraintType` applicability pair; plus
  the `rule_of "<SchemaKey>"` TDL surface; and
  the initial Core constraint types: `StringLengthConstraint.ConstraintType`,
  `BytesLengthConstraint.ConstraintType`,
  `NumericRangeConstraint.ConstraintType`,
  `ItemCountConstraint.ConstraintType`, `UniqueItemsConstraint.ConstraintType`, and
  `CardinalityConstraint.ConstraintType`; plus `ValidationRule`, Commit rule families, rule
  metadata, and the `ValidationBindings` relationship-contract definition;
- the normalized Core constraint configuration contracts: optional paired `Minimum` / `Maximum`
  with associated inclusivity properties for length, integer-range, and item-count constraints;
  presence-only uniqueness; and inclusive required `Minimum` plus optional `Maximum` for
  cardinality;
- removal of the legacy one-bound Core constraint types and their `ConstraintLength`,
  `ConstraintIntegerValue`, `ConstraintItemCount`, `ConstraintIsInclusive`, and
  `ConstraintEnabled` configuration model, with no legacy descriptor-property fallback;
- source fixtures proving explicit `ConstraintName`, `rule_of`, explicit `Constraints`
  attachment, direct applicability, inherited effective cardinality, incompatible attachment
  rejection, and extension-schema attachment/reuse; and
- Core configured constraints and classified MAP-seeded `ValidationRule` identities, with no active
  rule binding occurrences until their handlers are delivered. The complete current-rule
  disposition table in `validation-schema-design-spec.md` is the migration authority;
- the re-scoped one-way Validation Schema extension for implementations, rule sets, results,
  `Validate`, and non-Commit rule families; and
- normal Validation-extension source/loading acceptance against Core.

After VAL0, a schema may contain configured constraints and rule identities, but strict Commit
must reject an effective attached constraint for which no compatible handler is registered.
Constraints become active through their ordinary effective `Constraints` occurrences; a rule
becomes active only when a capability supplies a compatible handler and the corresponding
occurrence of `ValidationBindings`. The capabilities below make both paths operational.

---

# Capability 1 — Basic Descriptor-Aware Holon Conformance

## Outcome

Commit can reject a staged holon because an applicable, implemented Core semantic commitment
fails. This is the first end-to-end proof of Descriptor-Aware Holon Validation.

## Scope

- Create the WASM-safe `holons_validation` crate, distinct from the PVL/Integrity-focused
  `pvl_validation` crate.
- Define only the typed contexts, result types, entry point, and static dispatch required by this
  capability.
- Resolve the caller-supplied descriptor and its effective contract through descriptor-runtime
  APIs; do not duplicate descriptor-kernel logic.
- Deliver `effective_relationship_targets(member)`, a public descriptor-runtime effective-member
  API that returns populated effective relationship targets and additive provenance for a named
  member. Deliver `effective_constraints()` and `effective_validation_bindings()` as convenience
  wrappers. Do not rely on an `available_relationships` API that only reports permitted
  relationship names, and do not build parallel catalogs or lineage traversals.
- Treat `holon_descriptor()` as bootstrap navigation. A resolution failure records an error on the
  `StagedHolon` and prevents descriptor-dependent validation; `DescribedBy` cardinality remains
  ordinary relationship validation.
- Add static implementation registries keyed by concrete constraint type and canonical rule
  identity, recording required mode/context compatibility. Dispatch both through plain functions or
  small typed handler enums.
- When an effective attached concrete `ConstraintType` has no compatible handler, produce a
  blocking `UnsupportedConstraintType` finding. It must never be ignored, treated as inactive, or
  satisfied by retired relationship descriptor properties.
- Validate the minimum holon-conformance cohort:
  - required-property presence;
  - no undescribed populated properties; and
  - BaseValue-versus-ValueType native-kind compatibility.
- Invoke the entry point as the first semantic stage of Commit over the complete Nursery and return
  stable, actionable blocking results before any persistence write.
- Add one shared happy-path fixture and focused failing fixtures for each member of the cohort.
- Add active-binding coverage and blocked-Commit tests, including a second Commit attempt over a
  previously `Validated` staged holon and replacement of stale validation diagnostics after
  correction.

## Initial Commit integration

Capability 1 establishes Commit as the first and authoritative validation integration:

```text
complete staged Nursery
    -> Commit begins
    -> validate each staged holon through descriptor-runtime constraints and bindings
    -> validate aggregate local relationship constraints, including every applicable cardinality constraint
    -> return blocking results when violations exist
    -> persist only when validation passes
```

The Holon Data Loader is one producer of staged content. It resolves references and materializes
defaults before invoking Commit, but it does not own a validation gate. APIs, Dances, migrations,
and programmatic callers receive the same validation guarantee because every persistence path
passes through generalized guest Commit orchestration in
`happ/crates/holons_guest/src/guest_shared_objects/commit_functions.rs`.

## Non-goals

- Descriptor-holon self-conformance beyond what is necessary to obtain the supplied descriptor.
- String/range/enum/key constraints, relationship semantics beyond this cohort, Runtime
  Recognition, persisted evidence, and dynamic implementation dispatch.
- Default materialization. The loader may supply already materialized content, but this capability
  does not create defaults.

## Dependencies

- VAL0 Core Commit vocabulary and Validation-extension package-load acceptance.
- Descriptor Runtime Platform APIs that expose the descriptor and effective contract required for
  this cohort.

## Exit demonstration

Given a schema-loaded descriptor whose inherited effective bindings include
`RequiredPropertyPresence.ValidationRule`, committing an otherwise valid staged holon that omits
the required property produces a blocking `ValidationResult` and prevents persistence. Equivalent
fixtures prove the other implemented rules, collection of an empty effective constraint set, and one
valid holon commits successfully. A focused fixture with an effective attached constraint lacking
a registered handler produces a blocking `UnsupportedConstraintType` result.

---

# Capability 2 — Descriptor Self-Conformance

## Outcome

Descriptor holons themselves are validated against Schema 2.0 structural and effective-contract
invariants through the dispatch, result, and Commit path established by Capability 1.

## Scope

- Use the descriptor holon's governing descriptor and effective `Constraints` and
  `ValidationBindings` relationships; do not recurse into descriptor self-conformance during
  ordinary instance validation.
- Run aggregate schema/package rules only where their bounded Commit or schema-load scope is
  explicitly available.
- Implement the `DS-STRUCT-*` rules for `DescribedBy`, `Extends`, lineage termination, and
  descriptor-root invariants.
- Implement `DS-SCHEMA-*` rules for versioned schema dependency acyclicity, direct
  cross-schema dependency declarations, and Core accumulator baselines.
- Implement `DS-KIND-*` rules for explicit Instance TypeKind anchors, abstract anchors, root
  exceptions, and graph-derived describing-category pairing.
- Implement `DS-CONTRACT-*` rules for inherited-member redeclaration, unique member names,
  well-formed effective members, and member-kind compatibility.
- Implement `DS-CONSTRAINT-001` through `DS-CONSTRAINT-003` for monotonicity, attachment
  applicability, and configuration validity.
- Preserve descriptor and member provenance in every accumulated violation.

## Non-goals

- Ordinary-instance property/value/relationship conformance beyond Capability 1.
- A second descriptor structure or effective-contract algorithm.

## Dependencies

- Capability 1.
- Descriptor Runtime Platform effective descriptor and descriptor-kernel products.

## Exit demonstration

Malformed descriptor fixtures fail through the shared entry point with deterministic `DS-*`
diagnostics and provenance. Fixtures explicitly reject incompatible constraint attachments and
attempted effective-state relaxation, while an extension schema proves a valid new constraint type
and a valid adoption of a reusable dependency-owned constraint. Valid Core and Validation-extension
packages continue to load through the appropriate non-strict or implemented strict path.

---

# Capability 3 — Value, Enum, Default, and Key Conformance

## Descriptor-runtime prerequisite — Key-Rule Resolution and Composition

Before key conformance can be validated, Descriptor Runtime must provide a reusable key-rule
resolver and composer. This is an explicit implementation deliverable coordinated by this plan;
it belongs in the Descriptor Runtime boundary, not in `holons_validation` and not in a
Commit-only code path.

### Outcome

Staging, loading, Commit validation, and other coordinator/runtime callers can resolve the
governing key rule for a holon and call `compose_key` on its completed state. Key generation is
therefore available before validation and persistence, rather than being an implementation detail
of `DS-KEY-005` checking.

### Scope

- Expose effective `InstanceKeyRule` selection through `HolonDescriptor`, using the descriptor
  kernel's ordinary `Override`/`EffectiveValues` semantics. Zero or multiple effective targets
  are resolver errors; absence never silently means keyless.
- Expose a typed `KeyRuleDescriptor` facade for the selected concrete strategy or configured
  key-rule holon.
- Expose `compose_key` as a public descriptor-runtime operation over a caller-supplied completed
  holon state. `NoneRule.KeyRuleType` returns explicit keylessness; all other supported rules
  return the semantic key they compose.
- Implement the built-in Core strategy evaluation required by the active Schema 2.0 corpus,
  including type-name, schema-name, enum-variant, relationship, extended-type,
  described-type, constraint-instance, and configured-format rules, plus explicit keylessness.
- Use the same resolver for descriptor keys and ordinary holon keys: the governing rule for a
  holon is the effective `InstanceKeyRule` of its direct `DescribedBy` descriptor.
- Make composition read-only. The caller that is staging or loading a holon decides whether and
  when to write the returned key; the resolver does not mutate staged state or persist data.
- Return actionable resolution/composition errors for incomplete inputs, unsupported configured
  rules, ambiguous effective selection, and invalid format parameters. Validation consumes those
  errors as semantic findings; it does not reimplement or translate them into a second algorithm.

### Non-goals

- Key uniqueness enforcement, key presence checking, or persistence decisions; those remain
  Commit-validation and Commit responsibilities.
- Retroactive recomposition of persisted keys after a schema/key-rule change.
- Schema-qualified key namespace and collision behavior deferred by the Extension Schema identity
  design.

### Dependencies

- Descriptor Runtime Platform effective-value and descriptor facade products.
- Core KeyRule schema corpus. `ConstraintInstanceRule` is implemented by this prerequisite before
  callers rely on strict key validation; it is not a VAL0 strict-bootstrap precondition.
- Loader reference resolution and default materialization only for callers that require completed
  references or defaulted values as key inputs.

### Exit demonstration

A staging caller can resolve a holon's governing `KeyRuleDescriptor`, call `compose_key`, and
write the resulting key before Commit. Commit validation of the same completed holon uses the same
operation and accepts that key; a changed input, an ambiguous effective rule, or a mismatched
persisted/staged key produces the corresponding deterministic failure.

---

## Outcome

Commit validates completed ordinary and descriptor holons against effective property contracts,
value constraints, enum declarations, default declarations, and key rules.

## Scope

- Extend the existing property and value delegation path; do not introduce separate validators for
  each consumer.
- Implement `DS-CONFORM-*`, `DS-BIND-*`, and `DS-PROP-*` beyond Capability 1's minimum cohort.
- Implement type-specific constraint evaluation by concrete constraint type, including
  `StringLengthConstraint` behavior pinned to Unicode 17.0.0 UAX #29 extended grapheme clusters
  without normalization and separate `BytesLengthConstraint` byte-length behavior, with shared
  native and WASM fixtures.
- Implement `DS-ENUM-*` unique effective member-name, exact-token-membership, and
  token-non-retroactivity checks.
- Implement validation of `DS-DEFAULT-*` declarations and completed explicit values. Default
  materialization remains the loader's responsibility.
- Consume Descriptor Runtime's `KeyRuleDescriptor::compose_key` operation to implement
  `DS-KEY-*` effective-selection diagnostics, explicit keylessness, key presence, composed-key
  equality, and package/dependency-scope uniqueness when the supplied context can establish it.

## Non-goals

- Default materialization or a second key computation algorithm.
- Open-world uniqueness checks beyond the bounded package/dependency scope supplied by the
  validation context.

## Dependencies

- Capability 1.
- Capability 2 where a rule validates descriptor declarations.
- The Descriptor-Runtime Key-Rule Resolution and Composition prerequisite above.
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
  or graph snapshot, and evaluate every effective applicable `CardinalityConstraint` rather than a
  legacy descriptor-property pair.
- Add relationship-specific result provenance and fixtures alongside the shared result model.

### Cardinality-constraint runtime handoff

The Schema 2.0 TDL migration represents relationship cardinality through effective attached
`Constraints`, not `MinCardinality` / `MaxCardinality` properties on relationship descriptor
holons. Runtime descriptor and Commit-validation consumers must resolve the effective constraint
collection and interpret every applicable `CardinalityConstraint` according to `DS-CARD-001`.

More than one effective applicable cardinality constraint may govern a relationship; all must
pass. A runtime API must not silently retain a legacy single-property cardinality model. This
handoff does not authorize restoring relationship-level cardinality properties or having the TDL
compiler synthesize constraints, identities, ownership facts, or `Constraints` occurrences.

## Non-goals

- Pairwise execution of `Allow`/`Block`/`Cascade` deletion semantics until that design is settled.
- Open-world cardinality claims without a bounded, explicit graph context.

## Dependencies

- Capabilities 1 and 2.
- Descriptor Runtime Platform relationship products.
- Transaction or graph snapshot support for cardinality coverage.

## Exit demonstration

Commit validates bounded relationship declarations and occurrences. A transaction-aware fixture
proves cardinality failure only when the required current-Space prospective view is supplied, and
proves that multiple effective cardinality constraints are conjunctive. Once the
`ConstraintInstanceRule` resolver and `CardinalityConstraint` handler are registered, strict Core
bootstrap and the Core Sweettest fixture succeed without any legacy cardinality-property fallback.

---

# Rule-Family Delivery Map

| Rule family | First executable capability | Context limit |
| --- | --- | --- |
| Descriptor-resolution handling, required/undescribed properties, native kind | Capability 1 | Supplied holon and descriptor/effective contract |
| `DS-STRUCT-*`, `DS-SCHEMA-*`, `DS-KIND-*`, `DS-CONTRACT-*`, `DS-CONSTRAINT-*` | Capability 2 | Resolved descriptor graph and kernel products |
| Effective `InstanceKeyRule` resolution and `compose_key` | Capability 3 descriptor-runtime prerequisite | Completed holon state and descriptor-runtime products |
| `DS-CONFORM-*`, `DS-BIND-*`, `DS-PROP-*`, configured value constraints, `DS-ENUM-*`, `DS-DEFAULT-*`, `DS-KEY-*` | Capability 3 | Completed staged holon, `compose_key`, and bounded key scope where required |
| `DS-REL-*`, `DS-OCC-*`, effective `CardinalityConstraint`, `DS-CARD-001` | Capability 4 | Relationship/graph view; transaction snapshot for cardinality |

# Superseded Horizontal Decomposition

The former separate foundation, context-family, holon, property, generic-value, type-specific
value, relationship, commitment-shape, descriptor-rule-coverage, orchestration, entry-point, and
consumer-integration units are no longer independently shippable milestones.

Their useful implementation tasks are retained within the smallest capability that needs them:

| Former concern | New home |
| --- | --- |
| Foundation types, typed contexts, descriptor-aware crate, static dispatch | Capability 1 |
| Constraint/rule identities, Core constraint types, seeded unbound rules, package bootstrap | VAL0; Capability 1 consumes them |
| Effective constraint/binding collection and unsupported semantic handling | Capability 1 |
| Descriptor structure and contract coverage | Capability 2 |
| Generic KeyRule resolution and key composition | Capability 3 descriptor-runtime prerequisite |
| Property/value/type-specific rule coverage | Capabilities 1 and 3 |
| Relationship validator and rule coverage | Capability 4 |
| Descriptor orchestration and Commit entry point | Capability 1 |
| Loader path through Commit | Capability 1 |

This mapping is intentionally not a one-to-one migration of prior work-item identifiers. The MAP
Dev Tracking Sheet and cross-track dependency references must be reconciled to the four
capabilities before new implementation issues are opened.

# Relationship to Descriptor-Independent PVL

Descriptor-aware validation has no implementation dependency on the PVL implementation plan.
PVL remains a small, fixed, descriptor-independent set of integrity-safe functions and does not
consume this validator framework. The descriptor-aware crate may reuse compatible pure utilities
only where that does not make PVL depend on descriptor runtime, schema-loaded rules, dynamic
dispatch, or consumer contexts.

# Critical Path

1. VAL0: Core constraint/rule source vocabulary, TDL/JSON fidelity, and non-strict
   Validation-extension package-load acceptance.
2. Capability 1: basic descriptor-aware holon conformance through Commit.
3. Capability 2: descriptor self-conformance.
4. Capability 3 descriptor-runtime prerequisite: key-rule resolution and composition.
5. Capability 3: value, enum, default, and key conformance.
6. Capability 4: relationship conformance and the strict Core-bootstrap/Sweettest gate.
Capabilities 3 and 4 may proceed in parallel once their shared Capability 1/2 dependencies and
the necessary descriptor-runtime products are available.
