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
  -> CommitValidationReport
  -> blocking consumer decision
```

Subsequent capabilities extend that path with additional Commit rule families. Runtime Recognition,
Dance, Application, Trust, Attestation, and social-validation consumers require separate designs
and implementation plans; they remain outside this implementation sequence.

This plan owns Descriptor-Aware Holon Validation above descriptor-independent PVL. It owns
validation contexts, rule coordination, result accumulation, schema-backed rule applicability,
and reusable consumer entry points. It does not own descriptor retrieval, descriptor-kernel
effective-product computation, default population, TypeActivation, or Holochain Integrity
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
  Commit discovers rule commitments; governing conformance handlers consume constraints through
  an internal typed evaluator. A capability must prove every path it activates.
- Rules execute only where the caller supplies the bounded context they require.
- Every capability integrates with production Commit. The rules and constraint evaluators it
  delivers run on the real public Commit path, and its exit demonstration is an observable
  accept/reject outcome through that path. The Final Coverage and Convergence Milestone verifies
  complete coverage and remaining ingress convergence; it is not the first point at which
  descriptor-aware validation reaches Commit.
- Every public Commit validates every staged holon. `ValidationState` and prior findings are
  outputs of an earlier pass, never a cache used to select or skip work; each pass replaces
  validation state and findings together while keeping operational errors separate.
- The descriptor-aware crate consumes caller-supplied descriptor-runtime products. It never pulls
  descriptor-runtime dependencies into descriptor-independent PVL or the Integrity Zome.
- Initial execution uses static function or enum dispatch keyed by canonical rule identity, with
  an internal evaluator keyed by concrete constraint type. Do not introduce per-family trait
  hierarchies or boxed factories until multiple execution engines or extension-authored
  implementations require them.
- A `ValidationRule` may exist before it is implemented. It becomes active only when an applicable
  type declares an occurrence of `ValidationBindings` in the same delivered capability as a
  compatible handler.
  A coverage test requires every active binding to resolve to the static implementation registry.
  An active mandatory binding without a compatible handler fails closed with
  `UnsupportedValidationRule`.
- Bind each rule exactly once, at the descriptor family root named by the binding-placement
  convention in the
  [Validation Extension Schema Design Spec](validation-schema-design-spec.md). `ValidationBindings`
  is additive through `Extends`, so one occurrence on a family root activates the rule for every
  descriptor in that family. A capability does not author the same rule on individual member
  descriptors, and never binds on bare `TypeDescriptor`.
- Each capability adds to the existing validator, rule registry, fixtures, and diagnostics. No
  capability replaces earlier rule selection or result semantics.
- Detach a canonical `Constraints` occurrence only when a delivered validator's subject traversal
  would reach it without a compatible evaluator. Reachability, not presence, is what triggers
  fail-closed handling: an occurrence is discovered when a subject validator reads the governing
  descriptor of a subject it actually traverses. An attachment no delivered traversal reaches costs
  nothing to leave in place, and leaving it preserves the declaration for schema readers, authoring
  tools, and later capabilities.
- Where a detachment is required, the capability that delivers the evaluator restores it, in the
  same delivery as the evaluator, Commit integration, and accept/reject tests. This mirrors the
  `ValidationBindings` policy above.
- This is an intentional rollout model, not a restatement of fail-closed deferral. It does not
  weaken the invariant that **every effective attachment a delivered traversal reaches must resolve
  to a compatible handler or reject Commit**: a detached attachment is genuinely absent from the
  schema rather than present and excused, and an attachment outside the delivered traversal is
  outside the coverage that Commit currently claims. A successful Commit therefore proves
  conformance to the schema as it currently stands, over the subject levels the delivered validator
  traverses, and every reachable attachment still fails closed when unsupported.
- Detaching a constraint weakens the schema; reattaching it later tightens the accepted state.
  Pre-production holons admitted under the weaker schema may become nonconforming when the owning
  capability restores the attachment. The same tightening occurs when a capability first traverses a
  subject level whose attachments were left in place. That is an accepted pre-production rollout
  assumption here; the same move after production would require explicit schema versioning,
  migration, or reset.
- Each capability merges to `main` once its own vertical slice — attachments, handlers, Commit
  integration, and tests — passes. The Final Coverage and Convergence Milestone then verifies
  coverage and ingress convergence over the accumulated result.

## Precursor — VAL-PRE: Shared Construction and Dependency-Safe Outcomes

Before schema rule execution begins:

- invoke the existing `WritableHolon::populate_defaults()` from `TransientHolonManager` and
  `Nursery` create/independent-clone paths after descriptor resolution;
- replace bootstrap `MissingDescribedBy` failures with a non-fatal outcome such as
  `DefaultsDeferredNoDescriptor`, and make the loader retry `populate_defaults()` over its resolved
  staged import set;
- require every producer that permits omission to call the shared completion operation; Commit
  must never inject defaults;
- define dependency-light, serializable `CommitValidationViolation` primitives in `core_types`,
  below `holons_core` and above descriptor-independent `integrity_core_types`, without bound
  references;
- add staged identity-only validation findings separate from operational errors and a controlled
  operation that replaces state and findings together; and
- define serializable `CommitValidationReport` projection with derived decision and violation
  count, reserving `HolonError` for unreliable assessment and `ValidationResult` for durable
  evidence.

Clone coverage must prove that completion fills only omissions in the newly created independent
staged clone and never retroactively changes persisted historical state.

This precursor also fixes the narrow `holons_core` facade required by validation: effective
targets with provenance, constraint/binding accessors, subtype compatibility, property snapshots,
native value-kind checking, and controlled outcome replacement.

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
- the reusable Core `ZeroOrMore.CardinalityConstraint`, `ExactlyOne.CardinalityConstraint`,
  `ZeroOrOne.CardinalityConstraint`, and `OneOrMore.CardinalityConstraint` instances, without an
  authoring policy that requires their reuse;
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

After VAL0, a schema may contain configured constraints and rule identities. From Capability 1
onward, production Commit must reject an effective attached constraint for which no compatible
handler is registered.
Constraints apply through their ordinary effective `Constraints` occurrences and are consumed by
governing conformance handlers; a rule becomes active only when a capability supplies a compatible
handler and the corresponding occurrence of `ValidationBindings`. The capabilities below make
those paths operational.

### VAL0 follow-up — superseded rule metadata and inventory removals

VAL0 has landed. The following canonical-corpus edits it implies are outstanding and are tracked
here as VAL0 follow-up work. They are source-and-regeneration changes, not new capability scope.
The metadata and inventory removals must land before the Final Coverage and Convergence Milestone
checklist can be evaluated. The `Constraints` detachment must land before Capability 1, because
Capability 1 gates production Commit and the corpus must not carry an attachment that Capability 1's
subject traversal reaches without a compatible evaluator:

- remove the superseded `DefaultSeverity` and `MinimumBlockingBehavior` property descriptors, the
  `ValidationBlockingBehavior` enum value type and its variants, their declarations on the Commit
  rule-family type, and their per-instance values from `schema-src/core/validation.tdl`, leaving
  the four-property metadata closure defined by the
  [Validation Schema Design Specification](validation-schema-design-spec.md);
- remove the five rule instances marked “Remove” in that document's disposition table
  (`CoreAccumulatorsAreAdditive`, `StringLength`, `IntegerRange`, `BytesLength`, and
  `RelationshipCardinality`), taking the seeded inventory from 50 to the target 45;
- detach every canonical `Constraints` occurrence that a delivered validator's subject traversal
  would reach without a compatible evaluator, so the corpus asserts only the invariants the current
  implementation enforces. **The detached set is exactly one occurrence:
  `MapStringValueType.StringValueType -[Constraints]-> Length16k.StringLengthConstraint` in
  `schema-src/core/concrete-value-types.tdl`, restored by Capability 3.** Record it so Capability 3
  reattaches precisely what was removed.

  The scope is this narrow because reachability, not mere presence, is what triggers fail-closed
  handling. An effective `Constraints` occurrence is discovered when a subject validator reads the
  governing descriptor of a subject it actually traverses. The canonical corpus currently holds 135
  `Constraints` occurrences, and their reach separates cleanly:

  | Occurrences | Attached to | Reached by | Disposition |
  | --- | --- | --- | --- |
  | 1 `StringLengthConstraint` | `MapStringValueType.StringValueType` | Value Validation, delivered by Capability 1 | Detach now; Capability 3 restores |
  | 134 `CardinalityConstraint` | declared and inverse relationship descriptors | Relationship Validation, delivered by Capability 4 | Leave attached |

  The 134 cardinality occurrences are unreachable from the Capability 1 cohort, which traverses
  holon, property, and value subjects only. Capability 2 validates a relationship descriptor holon
  through its own governing meta-type, whose effective `Constraints` are the meta-type's own, not
  the cardinality the descriptor declares about its instances. Nothing before Capability 4 evaluates
  them, so nothing before Capability 4 can fail closed on them.

  Leaving them attached preserves relationship cardinality as schema *declaration* throughout the
  sequence. That matters because cardinality has no other expression in the corpus — the
  `MinCardinality` / `MaxCardinality` properties were retired when the occurrences were mechanically
  migrated from the former TDL `cardinality` syntax — so detaching them would delete the declaration
  itself from 14 files and require restoring it byte-for-byte later, with no enforcement gained in
  return; and
- regenerate every affected projection under `generated/json-imports/` from TDL through
  `map-schema` — `core/validation.json` for the metadata and rule-inventory removals, and
  `core/concrete-value-types.json` for the detachment — and update the affected loader metrics
  fixtures. Do not hand-edit generated JSON.

---

# Capability 1 — Basic Descriptor-Aware Holon Conformance

## Outcome

The shared validator can assess a staged holon, return a serializable `CommitValidationReport`,
and project identity-only findings into staged and wire outcomes. This is the first end-to-end
vertical slice: the delivered cohort gates real public Commit. Rule families and constraint types
owned by later capabilities are not yet attached to the corpus, so they are not yet part of the
schema this Commit enforces.

## Scope

- Create the WASM-safe `holons_validation` crate, distinct from the PVL/Integrity-focused
  `pvl_validation` crate.
- Define only the typed contexts, entry point, collector, report, and static dispatch required by
  this capability; reuse the dependency-safe violation types from VAL-PRE.
- Resolve the caller-supplied descriptor and its effective contract through descriptor-runtime
  APIs; do not duplicate descriptor-kernel logic.
- Deliver `effective_relationship_targets(member)`, a public descriptor-runtime effective-member
  API that returns populated effective relationship targets and additive provenance for a named
  member. Deliver `effective_constraints()` and `effective_validation_bindings()` as convenience
  wrappers. Do not rely on an `available_relationships` API that only reports permitted
  relationship names, and do not build parallel catalogs or lineage traversals.
- Treat `holon_descriptor()` as bootstrap navigation. A resolution failure records a finding on the
  `StagedHolon` and prevents descriptor-dependent validation; `DescribedBy` cardinality remains
  ordinary relationship validation.
- Add a static rule registry keyed by canonical rule identity and an internal constraint evaluator
  keyed by concrete constraint type, recording required mode/context compatibility. Implement both
  through plain functions or small typed handler enums.
- When Capability 1's conformance path encounters an effective attached concrete `ConstraintType`
  with no compatible internal handler, produce a blocking `UnsupportedConstraintType` finding. It
  must never be ignored, treated as inactive, or satisfied by retired relationship descriptor
  properties. Capability 1 proves this fail-closed behavior but does not evaluate cardinality.
- Validate the minimum holon-conformance cohort:
  - required-property presence;
  - no undescribed populated properties; and
  - BaseValue-versus-ValueType native-kind compatibility, migrated from existing checks rather
    than duplicated.
- Author the first active `ValidationBindings` occurrences in canonical Core TDL, at the family
  roots named by the binding-placement convention, and regenerate the affected projections under
  `generated/json-imports/` through `map-schema`. This capability activates exactly the cohort
  above, which is seven occurrences across `schema-src/core/root.tdl` and
  `schema-src/core/abstract-value-types.tdl`:

  | Binding target | Rule |
  | --- | --- |
  | `PropertyType.TypeDescriptor` | `RequiredPropertyPresence.ValidationRule` |
  | `HolonType.TypeDescriptor` | `NoUndescribedProperties.ValidationRule` |
  | `StringValueType.ValueType` | `BaseValueKindMatchesString.ValidationRule` |
  | `IntegerValueType.ValueType` | `BaseValueKindMatchesInteger.ValidationRule` |
  | `BooleanValueType.ValueType` | `BaseValueKindMatchesBoolean.ValidationRule` |
  | `BytesValueType.ValueType` | `BaseValueKindMatchesBytes.ValidationRule` |
  | `EnumValueType.ValueType` | `BaseValueKindMatchesEnum.ValidationRule` |

  These are the first active occurrences in the corpus, so this capability discharges the
  compatibility obligation the Validation Extension Schema Design Spec assigns to the first
  active-binding capability: prove that a compatible rule-family/descriptor-kind pairing is accepted
  and that an incompatible pairing fails as descriptor/schema self-conformance before handler
  dispatch.
- Add staged-finding and wire-report projection. `StagedHolonWire` in `holons_boundary` gains a
  serializable identity-only findings collection alongside its existing `validation_state`, kept
  separate from its operational `errors`; no bound runtime reference may cross that boundary.
- Extend the Commit response surface. `CommitResponse` is a holon whose type is defined in the
  dance extension schema (`schema-src/dance/schema.tdl`), not Core, so this capability adds there:
  a `Rejected` variant on the `CommitRequestStatus` enum value type, a `RejectedHolons` /
  materialized-inverse relationship pair on `CommitResponse.Projection` alongside `SavedHolons`
  and `AbandonedHolons`, and the report projection plus its report-derived violation count.
  Regenerate `generated/json-imports/dance/schema.json` from TDL rather than hand-editing it.
  `Rejected` remains distinct from `Incomplete`: explicit abandonment and operational persistence
  failure keep their existing meanings.
- Route public production Commit through the entry point over a complete Nursery. Commit rejects
  the persistence-candidate set when the delivered cohort produces a finding and proceeds to
  persistence when it does not.
- Add no new `Constraints` occurrences. Capability 1 delivers no configured constraint evaluator,
  and the VAL0 follow-up detachment removes the one canonical attachment this cohort's traversal
  would reach. The 134 canonical `CardinalityConstraint` occurrences remain attached and are
  unreachable here, because this capability traverses holon, property, and value subjects only. The
  fail-closed `UnsupportedConstraintType` path is proved by an extension-schema fixture that
  attaches an unsupported constraint type deliberately, not by a canonical corpus attachment.
- Add a regression test asserting that the Capability 1 traversal discovers an empty effective
  constraint set for the canonical corpus. It is the executable statement that the retained
  cardinality attachments are out of reach, and it must start failing when Capability 4 extends the
  traversal to relationship subjects.
- Add one shared happy-path fixture and focused failing fixtures for each member of the cohort.
- Add active-binding coverage and rejected-report tests, including a second assessment over a
  previously `Validated` staged holon and replacement of stale validation findings after
  correction.

## Production Commit integration

Capability 1 wires the validator into public Commit for the cohort it delivers:

```text
complete staged Nursery
    -> public Commit begins validation
    -> discover effective constraints and dispatch applicable bindings for each staged holon
    -> run the delivered conformance handlers and fail closed on encountered unsupported constraints
    -> reject the persistence-candidate set when violations exist
    -> otherwise prepare the persistence plan and proceed
```

The guarantee this establishes is scoped to the schema as it currently stands and to the subject
levels this capability traverses. It is not yet the complete claim that Commit is the sole gate
for create, update, and relationship-occurrence mutation; that claim depends on the extern/API
convergence verified at the Final Coverage and Convergence Milestone. Holon deletion remains outside this
plan's gate claim.

The Holon Data Loader is one producer of staged content. It resolves references and completes
defaults before Commit, but it does not own a validation gate.

## Non-goals

- Descriptor-holon self-conformance beyond what is necessary to obtain the supplied descriptor.
- String/range/enum/key constraints, relationship semantics beyond this cohort, Runtime
  Recognition, persisted evidence, and dynamic implementation dispatch.
- Default population, which belongs to VAL-PRE rather than Capability 1.

## Dependencies

- VAL0 Core Commit vocabulary and Validation-extension package-load acceptance.
- Descriptor Runtime Platform APIs that expose the descriptor and effective contract required for
  this cohort.
- The dance extension schema, for the `CommitResponse` rejection surface above.

## Exit demonstration

A public Commit over an otherwise valid staged holon that omits a required property is rejected
before any write and produces a `CommitValidationReport` and wire/staged projections. The rule
reaches that holon through inheritance alone: `RequiredPropertyPresence.ValidationRule` is bound
once on `PropertyType.TypeDescriptor`, and the property descriptor governing the omitted property
inherits it additively through `Extends` with no binding of its own. A companion fixture proves the
same for a descriptor holon in a different family, so family-root activation is shown to be general
rather than incidental to one fixture. Equivalent fixtures prove the other implemented rules,
collection of an empty effective constraint set over the canonical corpus, and one accepted Commit
that persists. An extension-schema fixture that attaches a constraint type lacking a registered
evaluator produces a blocking `UnsupportedConstraintType` finding and rejects Commit. Response
fixtures show a rejected assessment projecting `Rejected`, `RejectedHolons`, the report, and its
derived violation count, distinctly from explicit abandonment and from an operational failure.

---

# Capability 2 — Descriptor Self-Conformance

## Outcome

Descriptor holons themselves are validated against Schema 2.0 structural and effective-contract
invariants through the dispatch, result, and assessment path established by Capability 1.

## Scope

- Use the descriptor holon's governing descriptor and effective `Constraints` and
  `ValidationBindings` relationships; do not recurse into descriptor self-conformance during
  ordinary instance validation.
- When any descriptor is staged, schedule its owning Schema once and assess the prospective
  persisted-plus-staged `Components` collection, even when the Schema holon was not staged.
- Implement the `DS-STRUCT-*` rules for `DescribedBy`, `Extends`, lineage termination, and
  descriptor-root invariants.
- Implement `DS-SCHEMA-001` and `DS-SCHEMA-002` for versioned schema dependency acyclicity and
  direct cross-schema dependency declarations. Enforce `DS-SCHEMA-003` only in the descriptor
  kernel with an exhaustive inheritance-table unit test for every named non-local member and the
  local fallback; do not create a rule handler or binding for it.
- Implement `DS-KIND-*` rules for explicit Instance TypeKind anchors, abstract anchors, root
  exceptions, and graph-derived describing-category pairing.
- Implement `DS-CONTRACT-*` rules for inherited-member redeclaration, unique member names,
  well-formed effective members, and member-kind compatibility.
- Implement `DS-CONSTRAINT-001` through `DS-CONSTRAINT-003` for monotonicity, attachment
  applicability, and configuration validity.
- Under `DS-CONSTRAINT-003`, enforce all constraint-family-specific and conditional configuration
  presence rules. Do not infer such requiredness from the shared configuration `PropertyType` or
  introduce per-binding requiredness.
- Validate constraint *declarations* without requiring their evaluators. `DS-CONSTRAINT-001`
  through `DS-CONSTRAINT-003` assess whether an attachment is applicable to the constrained
  descriptor, whether its configuration is well formed, and whether a subtype relaxed an inherited
  applicable constraint. None of that requires the ability to evaluate the constraint against a
  subject, so this capability does not emit `UnsupportedConstraintType` for a well-formed attachment
  whose evaluator a later capability delivers. `UnsupportedConstraintType` remains reserved for the
  point of evaluation: a subject validator that reaches an effective attachment and cannot resolve a
  compatible evaluator for its concrete `ConstraintType`. This is what lets the 134 retained
  `CardinalityConstraint` occurrences be declaration-checked here and first evaluated in
  Capability 4.
- Preserve descriptor and member provenance in every accumulated violation.

## Non-goals

- Ordinary-instance property/value/relationship conformance beyond Capability 1.
- A second descriptor structure or effective-contract algorithm.

## Dependencies

- Capability 1.
- Descriptor Runtime Platform effective descriptor and descriptor-kernel products.

## Exit demonstration

Malformed descriptor fixtures reject public Commit with deterministic `DS-*` diagnostics and
provenance. Fixtures explicitly reject incompatible constraint attachments and
attempted effective-state relaxation, while an extension schema proves a valid new constraint type
and a valid adoption of a reusable dependency-owned constraint. Valid Core and Validation-extension
packages continue to load through the appropriate non-strict or implemented strict path. A focused
fixture stages only a descriptor and proves that its owning Schema aggregate is nevertheless
assessed over persisted-plus-staged components. A valid staged descriptor and its affected Schema
pass the same public Commit path and persist.

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
- Reference resolution and shared-objects-layer default completion for callers that require completed
  references or defaulted values as key inputs.

### Exit demonstration

A staging caller can resolve a holon's governing `KeyRuleDescriptor`, call `compose_key`, and
write the resulting key before Commit. Commit validation of the same completed holon uses the same
operation and accepts that key; a changed input, an ambiguous effective rule, or a mismatched
persisted/staged key produces the corresponding deterministic failure.

---

## Outcome

The shared validator assesses completed ordinary and descriptor holons against effective property
contracts, value constraints, enum declarations, default declarations, and key rules.

## Scope

- Extend the existing property and value delegation path; do not introduce separate validators for
  each consumer.
- Implement `DS-CONFORM-*`, `DS-BIND-*`, and `DS-PROP-*` beyond Capability 1's minimum cohort.
- Have `PropertyValueConformance.ValidationRule` consume effective value constraints through the
  internal constraint evaluator. Implement type-specific evaluation by concrete constraint type,
  including
  `StringLengthConstraint` behavior pinned to Unicode 17.0.0 UAX #29 extended grapheme clusters
  without normalization and separate `BytesLengthConstraint` byte-length behavior, with shared
  native and WASM fixtures.
- Restore the single `Constraints` occurrence detached by the VAL0 follow-up —
  `MapStringValueType.StringValueType -[Constraints]-> Length16k.StringLengthConstraint` in
  `schema-src/core/concrete-value-types.tdl` — and regenerate `core/concrete-value-types.json`
  through `map-schema`. Reattachment lands in this capability because it is the capability that
  delivers the evaluator, and it tightens the schema for every value typed by
  `MapStringValueType`.
- Implement `DS-ENUM-001` unique effective member-name and `DS-ENUM-002` exact-token-membership
  checks. Keep `EnumTokenNonRetroactivity.ValidationRule` unbound until this capability makes the
  `DS-ENUM-003` execution decision. The indicated preference is an unconditional enum-variant
  lineage rule, not optional binding or execution-selection policy.
- Implement validation of `DS-DEFAULT-*` declarations and completed explicit values. Default
  completion remains at the shared objects layer as established by VAL-PRE.
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
- Shared-objects-layer default-completion support, including the loader bootstrap backstop, for fixtures
  that require completed defaults.

## Exit demonstration

Loader fixtures demonstrate accepted and rejected string, enum, default, and key cases through
the same public Commit path used by Capability 1. Rejected cases fail before any write; an
accepted case persists its completed state.

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
- Make Capability 4 the first and exclusive capability that evaluates relationship cardinality;
  its relationship conformance handler consumes effective cardinality constraints through the
  internal constraint evaluator.
- Reach, rather than restore, the canonical `CardinalityConstraint` occurrences. The VAL0 follow-up
  left all 134 attached because no earlier traversal could reach them, so this capability requires
  no corpus reattachment and no regeneration for cardinality. Extending the traversal to relationship
  subjects is itself the tightening event: it is the point at which the retained `ExactlyOne`
  commitments that `DescribedBy` and `ComponentOf` rely on begin to be evaluated, and at which
  existing pre-production holons become subject to cardinality conformance. Verify the retained set
  against the 134-occurrence count recorded by the VAL0 follow-up before delivery, so a corpus drift
  between VAL0 and this capability is caught rather than silently absorbed.
- Build prospective views only from authoritative Commit-local relationship buckets, as defined by
  the [Relationship Occurrence Persistence Design
  Specification](../transactions/relationship-persistence-design-spec.md). Prepare paired local
  declared/inverse deltas for the relationship-persistence plan and cover source-chain conflict
  reload, revalidation, and bounded retry/failure.
- Route relationship-occurrence removal through the same prospective-bucket validation and
  prepared relationship plan as occurrence creation. Storage-level SmartLink deletion becomes an
  internal execution operation rather than an independently callable mutation path.
- Emit the `Error`-severity blocking `RelationshipCoordinationRequired` finding whenever an
  applicable rule requires unavailable multi-cell aggregate authority. Do not treat DHT reads as a
  serializable cross-cell snapshot.
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

- Holon deletion, including the current immediate `DeleteHolon` paths and pairwise `Allow` /
  `Block` / `Cascade` semantics. Descriptor-independent PVL continues to validate the structural
  deletion target; a separate deletion-semantics design will decide whether deletion is staged or
  routed through Commit. This plan neither closes that path nor treats it as an activation gap.
  This does not defer ordinary relationship-occurrence removal from the prospective-bucket
  validation delivered by this capability.
- Open-world cardinality claims without a bounded, explicit graph context.
- Cross-cell Relationship Coordination and remote inverse realization; Capability 4 only preserves
  their explicit boundary.

## Dependencies

- Capabilities 1 and 2.
- Descriptor Runtime Platform relationship products.
- Transaction or graph snapshot support for cardinality coverage.

## Exit demonstration

Public Commit assesses bounded relationship declarations and occurrences. A transaction-aware
fixture proves cardinality failure only when the required Commit-local prospective view is
supplied, rejects before any relationship write, and proves that multiple effective cardinality
constraints are conjunctive. An accepted fixture persists the prepared local relationship
directions. Once the
`ConstraintInstanceRule` resolver and `CardinalityConstraint` handler are registered, strict Core
bootstrap and the Core Sweettest fixture succeed without any legacy cardinality-property fallback.
A multi-cell aggregate fixture rejects with `RelationshipCoordinationRequired`; ordinary deferred
remote inverse realization does not make a completed local forward commitment provisional.

---

# Final Coverage and Convergence Milestone

Each capability has already integrated with production Commit for the schema it delivers. This
milestone does not switch validation on. It verifies that evaluator coverage is now complete and
that every public create, update, and relationship-occurrence ingress has converged, upgrading the
scoped per-capability guarantee into the complete gate claim for those mutations. Holon deletion
is deliberately outside this milestone's claim and is inventoried below without becoming an
activation prerequisite.

The milestone passes when every item below holds:

- every effective Core constraint type reachable in the canonical corpus has a compatible
  registered evaluator; the single `Constraints` occurrence detached by the VAL0 follow-up has been
  restored by Capability 3, reproducing exactly what was removed; and the 134 retained
  `CardinalityConstraint` occurrences are now reached by the Capability 4 traversal. No attachment
  remains detached for want of an evaluator, and no attachment remains unreachable for want of a
  traversal;
- every authored `ValidationBindings` occurrence has a compatible registered handler and subject
  family, sits at the family root named by the binding-placement convention, and no occurrence is
  authored on bare `TypeDescriptor`;
- the target 45-rule inventory and five removals match canonical TDL and generated projections;
- the following extern/API inventory matches the current production coordinator exports recorded
  in `happ/coordinator-surface.toml`. It baselines against the surface reductions already delivered
  by [`map-holons` PR 623](https://github.com/memetic-activation-platform/map-holons/pull/623)
  and [`map-holons` issue 622](https://github.com/memetic-activation-platform/map-holons/issues/622)
  rather than assuming historical externs remain exposed:

  | Production export | Current call path | Milestone disposition |
  | --- | --- | --- |
  | `dance` | compatibility alias to `dance_adapter` | Supported; follows the `dance_adapter` disposition. |
  | `dance_adapter` | bind request, then `dispatch_dance`; Commit requests call `commit_dance` → `TransactionContext::commit` → `GuestHolonService::commit_internal` → `commit_functions::commit` | Supported; every create, update, and relationship-occurrence mutation dispatched here must use Commit. |
  | `holon_storage_persist` | `holon_storage_externs::holon_storage_persist` → `holon_storage::persist_holon` | Direct Commit bypass; internalize it or restrict it to prepared Commit plans before this milestone passes. |
  | `smartlink_put` | `smartlink_externs::smartlink_put` → `smartlink::put_smartlink` | Direct Commit bypass; internalize it or restrict it to Capability 4 prepared plans. |
  | `smartlink_delete` | `smartlink_externs::smartlink_delete` → `smartlink::delete_smartlink` | Direct Commit bypass; internalize it or restrict it to Capability 4 prepared plans. |
  | `delete_holon_node` | direct extern deletes matching `LocalHolonSpace` links and then the HolonNode entry; supported dispatch also follows `dance_adapter` → `dispatch_dance` → `delete_holon_dance` → `MutationFacade::delete_holon` → `GuestHolonService::delete_holon_internal` → `delete_holon_node` | Current immediate deletion surface, outside this plan's gate claim. PVL validates the structural deletion target; future deletion-semantics design owns any convergence decision. |
  | `holon_storage_get`, `holon_storage_get_many`, `smartlink_expand`, `smartlink_expand_all`, `smartlink_expand_by_key` | direct storage-read helpers | Supported and read-only; outside the mutation gate. |
  | `get_holon_node_by_path`, `get_all_holon_nodes`, `get_original_holon_node`, `get_original_holon_node_with_details`, `get_all_deletes_for_holon_node`, `get_oldest_delete_for_holon_node` | direct legacy read helpers | `legacy_ingress` and read-only; outside the mutation gate. |

  `create_holon_node` and `create_path_to_holon_node` are already removed. A future inventory update
  must continue to record both call path and disposition; a disposition without its call path is
  insufficient.

  The inventory creates no `*_for_test` exemption category. [`map-holons` PR
  623](https://github.com/memetic-activation-platform/map-holons/pull/623) already established that
  test-only functions are absent from packaged production coordinator artifacts by construction:
  every `*_for_test` symbol is classified `test_only` under the loose `holons_test_probes` zome,
  which no production DNA or hApp manifest references, and `npm run check:happ-artifacts` enforces
  that boundary in CI. Test probes are therefore outside the production surface being inventoried,
  not excused within it;
- every public production create, update, and relationship-occurrence add/remove path converges on
  generalized guest Commit, while internal persistence and SmartLink operations accept only
  prepared Commit plans;
- `LocalHolonSpace` bootstrap is documented and tested as the sole intended permanent exception;
- `delete_holon_node` remains explicitly inventoried as the current out-of-scope deletion surface,
  rather than being misclassified as an activation gap or assigned to an invented capability;
- Commit responses project `Rejected`, `RejectedHolons`, the report, and its derived violation
  count while keeping rejection, explicit abandonment, and operational failure distinct;
- complete-Nursery, affected-Schema, Commit-local relationship-bucket, conflict-retry, and
  second-pass replacement tests pass; and
- root checks, formatting, unit tests, WASM checks, and relevant Sweettests pass.

The validator is already wired into public production Commit from Capability 1 onward. What this
milestone establishes is the complete claim for the delivered mutation scope: Commit is the sole
gate for create, update, and relationship-occurrence mutation over a corpus whose every effective
attachment has a compatible evaluator. It makes no target claim for holon deletion; a future
deletion-semantics design owns that decision. Each capability has already merged to `main` on its
own; this milestone adds coverage and convergence verification rather than a deferred activation
switch.

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
| Effective binding discovery, internal constraint-evaluator foundation, and fail-closed unsupported handling | Capability 1 |
| Descriptor structure and contract coverage | Capability 2 |
| Generic KeyRule resolution and key composition | Capability 3 descriptor-runtime prerequisite |
| Property/value/type-specific rule coverage | Capabilities 1 and 3 |
| Relationship validator and rule coverage | Capability 4 |
| Descriptor orchestration and production Commit integration | Capability 1 |
| Complete-coverage verification and loader/API convergence | Final Coverage and Convergence Milestone |

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

1. VAL-PRE: default property completion at the shared objects layer and dependency-safe outcome
   contracts.
2. VAL0 (landed): Core constraint/rule source vocabulary, TDL/JSON fidelity, and non-strict
   Validation-extension package-load acceptance. Its follow-up `Constraints` detachment and
   regeneration must land before Capability 1; its metadata and rule-inventory removals may
   proceed in parallel with the capabilities but must land before the final checklist.
3. Capability 1: basic descriptor-aware holon conformance gating production Commit.
4. Capability 2: descriptor and affected-Schema aggregate conformance.
5. Capability 3 descriptor-runtime prerequisite: key-rule resolution and composition.
6. Capability 3: value, enum, default, and key conformance.
7. Capability 4: Commit-local relationship conformance and the strict
   Core-bootstrap/Sweettest gate.
8. Final Coverage and Convergence Milestone: complete evaluator coverage over every reachable
   `Constraints` attachment, extern/API convergence, and the scoped public Commit claim.
Capabilities 3 and 4 may proceed in parallel once their shared Capability 1/2 dependencies and
the necessary descriptor-runtime products are available.
