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
  accept/reject outcome through that path. The Final Activation Milestone verifies complete
  coverage and remaining ingress convergence; it is not the first point at which descriptor-aware
  validation reaches Commit.
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
  type declares an occurrence of `ValidationBindings` in the same delivered capability as a compatible handler.
  A coverage test requires every active binding to resolve to the static implementation registry.
  An active mandatory binding without a compatible handler fails closed with
  `UnsupportedValidationRule`.
- Each capability adds to the existing validator, rule registry, fixtures, and diagnostics. No
  capability replaces earlier rule selection or result semantics.
- Deliver canonical `Constraints` attachments incrementally, alongside their evaluators. A
  capability adds the `Constraints` occurrences for the constraint types it implements in the same
  delivery as the compatible internal evaluators, Commit integration, and accept/reject tests.
  This mirrors the `ValidationBindings` policy above.
- This is an intentional rollout model, not a restatement of fail-closed deferral. It does not
  weaken the invariant that **every effective attachment that exists must resolve to a compatible
  handler or reject Commit**: an attachment that has not been added yet is genuinely absent from
  the schema rather than present and excused. A successful Commit therefore proves conformance to
  the schema as it currently stands, and every attachment that is present still fails closed when
  unsupported.
- Detaching a constraint weakens the schema; reattaching it later tightens the accepted state.
  Pre-production holons admitted under the weaker schema may become nonconforming when the owning
  capability restores the attachment. That is an accepted pre-production rollout assumption here;
  the same move after production would require explicit schema versioning, migration, or reset.
- Each capability merges to `main` once its own vertical slice — attachments, handlers, Commit
  integration, and tests — passes. The Final Activation Milestone then verifies coverage and
  ingress convergence over the accumulated result.

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

After VAL0, a schema may contain configured constraints and rule identities. Once the final
activation occurs, strict Commit must reject an effective attached constraint for which no
compatible handler is registered.
Constraints apply through their ordinary effective `Constraints` occurrences and are consumed by
governing conformance handlers; a rule becomes active only when a capability supplies a compatible
handler and the corresponding occurrence of `ValidationBindings`. The capabilities below make
those paths operational.

### VAL0 follow-up — superseded rule metadata and inventory removals

VAL0 has landed. The following canonical-corpus edits it implies are outstanding and are tracked
here as VAL0 follow-up work. They are source-and-regeneration changes, not new capability scope.
The metadata and inventory removals must land before the Final Activation Milestone checklist can
be evaluated. The `Constraints` detachment must land before Capability 1, because Capability 1
gates production Commit and the corpus must not carry an attachment whose evaluator has not been
delivered:

- remove the superseded `DefaultSeverity` and `MinimumBlockingBehavior` property descriptors, the
  `ValidationBlockingBehavior` enum value type and its variants, their declarations on the Commit
  rule-family type, and their per-instance values from `schema-src/core/validation.tdl`, leaving
  the four-property metadata closure defined by the
  [Validation Schema Design Specification](validation-schema-design-spec.md);
- remove the five rule instances marked “Remove” in that document's disposition table
  (`CoreAccumulatorsAreAdditive`, `StringLength`, `IntegerRange`, `BytesLength`, and
  `RelationshipCardinality`), taking the seeded inventory from 50 to the target 45;
- detach every canonical `Constraints` occurrence whose constraint type has no delivered
  evaluator, so the corpus asserts only the invariants the current implementation enforces. The
  detached set is defined by constraint type rather than by file: at VAL0 it is every
  `StringLengthConstraint` occurrence, restored by Capability 3, and every `CardinalityConstraint`
  occurrence, restored by Capability 4, wherever either appears under `schema-src/`. Record the
  exact detached set so each owning capability reattaches precisely what was removed. Cardinality
  has no other expression in the corpus — `MinCardinality` / `MaxCardinality` properties are
  already retired — so this detachment genuinely removes relationship cardinality from the schema
  until Capability 4; and
- regenerate every affected projection under `generated/json-imports/` from TDL through
  `map-schema` — `core/validation.json` for the metadata and rule-inventory removals, and the
  projection of every TDL source the detachment touches — and update the affected loader metrics
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
  so the VAL0 follow-up detachment leaves the corpus with no effective constraint reachable from
  this cohort. The fail-closed `UnsupportedConstraintType` path is proved by an extension-schema
  fixture that attaches an unsupported constraint type deliberately, not by a canonical corpus
  attachment.
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
levels this capability traverses. It is not yet the universal claim that Commit is the sole gate
for every MAP state mutation; that claim depends on the extern/API convergence verified at the
Final Activation Milestone.

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

Given a schema-loaded descriptor whose inherited effective bindings include
`RequiredPropertyPresence.ValidationRule`, a public Commit over an otherwise valid staged holon
that omits the required property is rejected before any write and produces a
`CommitValidationReport` and wire/staged projections. Equivalent fixtures prove the other
implemented rules, collection of an empty effective constraint set, and one accepted Commit that
persists. An extension-schema fixture that attaches a constraint type lacking a registered
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
assessed over persisted-plus-staged components.

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
- Restore every `StringLengthConstraint` occurrence detached by the VAL0 follow-up, reproducing
  exactly the recorded detached set, and regenerate every affected projection under
  `generated/json-imports/` through `map-schema`. Reattachment lands in this capability because it
  is the capability that delivers the evaluator; it tightens the schema for every string-valued
  property, `Length16k` on `MapStringValueType` included.
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
the same public Commit path used by Capability 1.

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
- Restore every `CardinalityConstraint` occurrence detached by the VAL0 follow-up, reproducing
  exactly the recorded detached set, and regenerate every affected projection under
  `generated/json-imports/` through `map-schema`. This restores relationship cardinality to the
  schema, including the `ExactlyOne` commitments that `DescribedBy` and `ComponentOf` rely on, and
  is the point at which existing pre-production holons become subject to cardinality conformance.
- Build prospective views only from authoritative Commit-local relationship buckets, as defined by
  the [Relationship Occurrence Persistence Design Specification](../transactions/relationship-persistence-design-spec.md). Prepare paired
  local declared/inverse deltas for the relationship-persistence plan and cover source-chain
  conflict reload, revalidation, and bounded retry/failure.
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

- Holon-deletion plan execution, including pairwise `Allow` / `Block` / `Cascade` semantics, until
  that design is settled. This does not defer ordinary relationship-occurrence removal from the
  prospective-bucket validation delivered by this capability.
- Convergence of the current direct `DeleteHolon` ingress on Commit. It remains a tracked
  implementation gap for the dedicated deletion capability, not a permanent exception to the
  target sole-gate architecture.
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
supplied, and proves that multiple effective cardinality constraints are conjunctive. Once the
`ConstraintInstanceRule` resolver and `CardinalityConstraint` handler are registered, strict Core
bootstrap and the Core Sweettest fixture succeed without any legacy cardinality-property fallback.
A multi-cell aggregate fixture rejects with `RelationshipCoordinationRequired`; ordinary deferred
remote inverse realization does not make a completed local forward commitment provisional.

---

# Final Activation Milestone — Universal Public Commit Gate

Each capability has already integrated with production Commit for the schema it delivers. This
milestone does not switch validation on. It verifies that evaluator coverage is now complete and
that every public create, update, and relationship-occurrence ingress has converged, upgrading the
scoped per-capability guarantee into the universal claim for those mutations. Holon deletion is
deliberately outside this milestone's claim; see the `DeleteHolon` item below and the closing
paragraph.

The milestone passes when every item below holds:

- every effective Core constraint type reachable in the canonical corpus has a compatible
  registered evaluator, and the canonical `Constraints` occurrences detached by the VAL0 follow-up
  have all been restored by their owning capabilities, reproducing exactly the recorded detached
  set. No attachment remains detached for want of an evaluator;
- every authored `ValidationBindings` occurrence has a compatible registered handler and subject
  family;
- the target 45-rule inventory and five removals match canonical TDL and generated projections;
- an extern/API inventory enumerates the actual production coordinator exports recorded in
  `happ/coordinator-surface.toml` and records, for each, its current call path — either the route
  by which it reaches generalized guest Commit, or the point at which it bypasses Commit and
  writes directly — together with whether it is converged, internal, read-only, retired, or
  explicitly deferred with a named owning follow-up. A disposition asserted without its call path
  does not satisfy this item. It baselines
  against the surface reductions already delivered by `map-holons` PR 623 and issue #622 rather
  than assuming every historical extern remains exposed — `create_holon_node` and
  `create_path_to_holon_node` are already removed. The inventory covers at minimum:

    - `dance` and `dance_adapter` (`supported`) — the primary mutation ingress;
    - `holon_storage_persist` (`supported`) — must accept only prepared Commit plans;
    - `smartlink_put` and `smartlink_delete` (`supported`) — same, per Capability 4;
    - `delete_holon_node` (`legacy_ingress`) — the asserted `DeleteHolon` gap; see below;
    - the remaining `legacy_ingress` reads (`get_holon_node_by_path`, `get_all_holon_nodes`,
      `get_original_holon_node`, `get_original_holon_node_with_details`,
      `get_all_deletes_for_holon_node`, `get_oldest_delete_for_holon_node`), recorded as read-only
      and therefore outside the mutation gate rather than left unaccounted.

  The inventory creates no `*_for_test` exemption category. PR 623 already established that
  test-only functions are absent from packaged production coordinator artifacts by construction:
  every `*_for_test` symbol is classified `test_only` under the loose `holons_test_probes` zome,
  which no production DNA or hApp manifest references, and `npm run check:happ-artifacts` enforces
  that boundary in CI. Test probes are therefore outside the production surface being inventoried,
  not excused within it;
- every public production create, update, and relationship-occurrence add/remove path converges on
  generalized guest Commit, while internal persistence and SmartLink operations accept only
  prepared Commit plans;
- `LocalHolonSpace` bootstrap is documented and tested as the sole intended permanent exception;
- the `DeleteHolon` gap is named and scoped rather than asserted generically. It is the
  `delete_holon_node` export classified `legacy_ingress` in `happ/coordinator-surface.toml`: a
  scaffolded raw HolonNode deletion ingress that does not route through a prepared Commit plan.
  It is owned by a dedicated deletion capability that has no tracking issue yet; one must be
  opened before this item can be evaluated, following the pattern of the `map-holons` ingress
  retirements #622 and #634. That capability must retire or converge the export and remove its
  manifest row. Until then it is the one known unconverged public mutation path, and the reason
  this milestone's claim excludes deletion;
- Commit responses project `Rejected`, `RejectedHolons`, the report, and its derived violation
  count while keeping rejection, explicit abandonment, and operational failure distinct;
- complete-Nursery, affected-Schema, local relationship-bucket, conflict-retry, and second-pass
  replacement tests pass; and
- root checks, formatting, unit tests, WASM checks, and relevant Sweettests pass.

The validator is already wired into public production Commit from Capability 1 onward. What this
milestone establishes is the universal claim: that Commit is the sole gate for create, update, and
relationship-occurrence mutation, over a corpus whose every effective attachment has a compatible
evaluator. The broader target claim for every MAP state mutation becomes true only when the
dedicated deletion capability also routes holon deletion through a prepared Commit plan. Each
capability has already merged to `main` on its own; this milestone adds the coverage and
convergence verification rather than a deferred activation switch.

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
| Universal-coverage verification and loader/API convergence | Final Activation Milestone |

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
   proceed in parallel with the capabilities but must land before the activation checklist.
3. Capability 1: basic descriptor-aware holon conformance gating production Commit.
4. Capability 2: descriptor and affected-Schema aggregate conformance.
5. Capability 3 descriptor-runtime prerequisite: key-rule resolution and composition.
6. Capability 3: value, enum, default, and key conformance.
7. Capability 4: locally authoritative relationship conformance and the strict
   Core-bootstrap/Sweettest gate.
8. Final Activation Milestone: complete evaluator coverage, restored `Constraints` attachments,
   extern/API convergence, and the universal public Commit claim.
Capabilities 3 and 4 may proceed in parallel once their shared Capability 1/2 dependencies and
the necessary descriptor-runtime products are available.
