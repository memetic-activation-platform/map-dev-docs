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
callbacks. Where a capability depends on new work in those components, such as key resolution
or keyless persistence in Capability 3, this plan sequences that work; the owning component
keeps its design authority.

Corpus counts in this plan, such as attachment, rule, and finding totals, are snapshots of an
evolving schema. Re-check them before implementing each capability rather than treating them as
fixed targets.

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
  Commit discovers rule commitments. Subject traversal evaluates every reached effective
  constraint through an internal typed evaluator, independently of any binding. A capability must
  prove every path it activates.
- Rules execute only where the caller supplies the bounded context they require.
- Every capability integrates with production Commit. A capability may span ordered issues when
  the earlier issue delivers independently testable scaffolding and the final issue completes the
  vertical slice. The rules and constraint evaluators it delivers run on the real public Commit
  path by the capability's completion, and its exit demonstration is an observable accept/reject
  outcome through that path. The Final Coverage and Convergence Milestone verifies complete
  coverage and remaining ingress convergence; it is not the first point at which descriptor-aware
  validation reaches Commit.
- Every public Commit validates every live validation and node-persistence candidate derived from
  the complete Nursery. `Abandoned` and already `Committed` entries are not candidates.
  Already committed staged entries remain eligible for the existing relationship-persistence retry.
  `ValidationState` and prior findings are outputs of an earlier pass, never a cache used to select
  or skip candidate work; each pass replaces validation state and findings together while keeping
  operational errors separate.
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
- A multi-issue capability is complete only when its final issue closes the vertical slice —
  attachments, handlers, Commit integration, and tests. The Final Coverage and Convergence
  Milestone then verifies coverage and ingress convergence over the accumulated result.

## Precursor — VAL-PRE: Shared Construction and Dependency-Safe Outcomes

Before schema rule execution begins:

- retain shared best-effort `WritableHolon::populate_defaults()` attempts in construction,
  staging, and clone paths; descriptor attachment through `with_descriptor()` also attempts defaults;
- retain the loader's final default-population and enum-materialization pass after assembly.
  Commit assesses actual explicit state and never injects defaults; use the current
  [construction contract](../descriptors/layered-desc-arch.md#6-best-effort-default-population);
- define dependency-light, serializable `CommitValidationViolation` primitives in `core_types`,
  below `holons_core` and above descriptor-independent `integrity_core_types`, without bound
  references;
- add staged identity-only validation findings separate from operational errors and a controlled
  operation that replaces state and findings together; and
- reserve `HolonError` for assessment that cannot complete reliably and `ValidationResult` for
  durable evidence. `CommitValidationReport` is not defined here: it never crosses a boundary, so
  it needs no serialization and no home below `holons_core`, and arrives with the validator in
  Capability 1.

**Superseded construction proposal:** the former `DefaultsDeferredNoDescriptor` outcome,
state-driven retries, and requirement that every producer complete defaults before Commit are
historical only. Best-effort attempts create no preparation state or separate acceptance gate.

Clone coverage must prove that population fills only omissions in the newly created independent
staged clone and never retroactively changes persisted historical state.

This precursor also delivers the controlled staged-outcome replacement used by validation.
Capability 1 completes the remaining narrow `holons_core` facade: effective targets with
provenance, constraint/binding accessors, subtype compatibility, semantic undescribed-property
detection, `EnforceMinimum`, and native value-kind classification.

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
Constraints apply through their ordinary effective `Constraints` occurrences whenever subject
traversal reaches them, independently of bindings; a rule becomes active only when a capability
supplies a compatible handler and the corresponding occurrence of `ValidationBindings`. The
capabilities below make those paths operational.

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
  governing descriptor of a subject it actually traverses. At VAL0, the canonical corpus's
  `Constraints` occurrences separated cleanly by reach (counts are a VAL0 snapshot):

  | Occurrences | Attached to | Reached by | Disposition |
  | --- | --- | --- | --- |
  | 1 `StringLengthConstraint` | `MapStringValueType.StringValueType` | Value Validation, delivered by Capability 1 | Detach now; Capability 3 restores |
  | 158 `CardinalityConstraint` | declared and inverse relationship descriptors | Relationship Validation, delivered by Capability 4 | Leave attached |

  The 158 cardinality occurrences are unreachable from the Capability 1 cohort, which traverses
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

The shared validator can assess a staged holon, return a `CommitValidationReport`, and project
identity-only findings into staged and wire outcomes. This is the first end-to-end
vertical slice: the delivered cohort gates real public Commit. Rule families and constraint types
owned by later capabilities are not yet attached to the corpus, so they are not yet part of the
schema this Commit enforces.

Capability 1 is delivered through two ordered issues. VAL-C1a delivers the validator core, active
bindings, compatibility proof, and clean whole-corpus conformance without changing production
Commit behavior. VAL-C1b completes the vertical slice by integrating that validator with public
Commit and its rejection surface. Capability 2 is not a prerequisite for VAL-C1b.

## VAL-C1a — Validator Core and Corpus Conformance

- Rename the existing descriptor-independent `shared_validation` crate to `pvl_validation` and
  update its workspace registrations and consumers before introducing the distinct
  descriptor-aware crate.
- Create the WASM-safe `holons_validation` crate, distinct from the PVL/Integrity-focused
  `pvl_validation` crate.
- Define only the typed contexts, entry point, collector, report, and static dispatch required by
  this capability; reuse the dependency-safe violation types from VAL-PRE.
- Resolve the caller-supplied descriptor and its effective contract through descriptor-runtime
  APIs; do not duplicate descriptor-kernel logic.
- Publish `equals_or_extends`, `EffectiveRelationshipMember`, and the canonical
  `effective_relationship_targets(descriptor, member)` descriptor-runtime API. It returns populated
  effective relationship targets with `declared_on` provenance in ancestor-before-local order.
  Deliver `effective_constraints()` and `effective_validation_bindings()` as convenience wrappers.
  Do not publish a duplicate effective-member algorithm, rely on an `available_relationships` API
  that only reports permitted relationship names, or build parallel catalogs or lineage traversals.
- Add `ReadableHolon::undescribed_property_names()` as a semantic descriptor-runtime operation;
  keep raw property and relationship enumeration private.
- Add the `EnforceMinimum` computation used by required-property validation: concrete holons enforce
  every required effective member, while abstract descriptor holons may omit category-specific
  members but must still satisfy the universal descriptor contract. Derive the universal member
  set from the effective contract of `MetaTypeDescriptor.HolonType`, reusable once per validation
  run, and use existing descriptor wrappers and identities rather than a parallel contract model.
- Add a kind-only descriptor API, separate from `ValueDescriptor::is_valid()`, that classifies by
  identity through `equals_or_extends` rather than descriptor-name strings. Preserve all existing
  classifications, including `AnyBaseValue`, `ValueArray`, and `Unsupported`, while exposing the
  five native families required by this cohort.
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
  - required-property presence using `EnforceMinimum`;
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
- Add no new `Constraints` occurrences. Assert that the Capability 1 traversal discovers an empty
  effective constraint set over the manifest-selected canonical corpus; retained relationship
  cardinality attachments remain outside its holon/property/value subject traversal.
- Regenerate `generated/json-imports/core/root.json`,
  `generated/json-imports/core/abstract-value-types.json`, and the operational bootstrap bundle and
  resource copies from TDL through `map-schema`; do not hand-edit generated JSON.
- Run the cohort in report-only mode over every holon in Core and every manifest-selected extension
  package, including descriptor holons. Assert that all seven binding identities are discovered,
  every cohort handler is dispatched, and the run produces zero findings. Fix every corpus defect
  in VAL-C1a; a clean corpus is part of the issue's completion criteria.
  [map-holons #803](https://github.com/evomimic/map-holons/issues/803) later retired this
  Sweettest run, which assessed saved holons through a non-production traversal. Strict bootstrap
  Commit now gives the zero-findings evidence. A static `map-schema` test inventories the bound
  rules, and a unit test covers the Bytes binding.
- Add shared happy-path and focused failing fixtures, fail-closed unsupported-rule and
  unsupported-constraint coverage, native-kind coverage, active-binding registry coverage, and
  staged/transient/smart-reference coverage for semantic undescribed-property detection.

## Obsolete open-member policy removal

`AllowsAdditionalProperties` and `AllowsAdditionalRelationships` are retired. Every populated
instance property and independently authored relationship must bind to the holon's effective
descriptor contract. Additive `InstanceProperties` and `InstanceRelationships` remain ordinary
`Extends` behavior; any future restriction on subtype additions is a separate design concern.

Capability 2 owns removal of the obsolete properties from the Core Schema, runtime accessors and
validation exemptions, TDL syntax and tooling, generated imports, and affected tests. The fixed
Commit authored-name check below already rejects populated undeclared relationships; that
prerequisite does not complete the broader relationship-conformance contract in Capability 4.

## Delivered follow-up: declared authoring and phase-specific cloning

[map-holons #717](https://github.com/evomimic/map-holons/issues/717) /
[PR #720](https://github.com/evomimic/map-holons/pull/720) implements the common pre-write
source-contract check: every populated authored relationship name must be effective and declared.
Inverse and unknown names produce `RuleViolation { code: "UndeclaredRelationship" }` with exact
source/name/target subjects. This is a fixed Commit preparation invariant, not an activated rule.
The loader preserves raw assembled input and delegates semantic rejection to Commit. Operational
loader failures remain distinct. Saved clones require descriptors and retain only declared
relationships; transient/staged clones preserve authored input. See the
[transaction specification](../transactions/transactions-design-spec.md#8-semantic-cloning-and-staging).

This delivers part of DS-BIND-002 enforcement ahead of the broader relationship capability. It does
not implement endpoint conformance, ordering/cardinality constraints, property binding completion,
or subtype-extensibility enforcement. Do not restore target-side inverse classification or the
superseded dedicated inverse finding. [#719](https://github.com/evomimic/map-holons/issues/719) is
closed: its `AllowsAdditional*` description work was absorbed by the obsolete open-member policy
removal above, and its remaining retry-scope and clone/finding verification is recorded by the
Capability 2 exit demonstration and the convergence milestone rather than by the issue. This
follow-up is not a Capability 2 dependency. PR merge status and the current implementation remain
the delivery-status evidence.

## VAL-C1b — Commit Integration

- Consume VAL-PRE's staged identity-only findings, wire projection, and controlled outcome
  replacement. No new validation result transport model is introduced here; the staged pool
  exported as session state carries per-holon findings to the client on the same round trip that
  returns the Commit response.
- Extend the Commit response surface. `CommitResponse` is a holon whose type is defined in the
  dance extension schema (`schema-src/dance/schema.tdl`), not Core, so this capability adds there:
  a `Rejected` variant on the `CommitRequestStatus` enum value type, a `RejectedHolons` /
  materialized-inverse relationship pair on `CommitResponse.Projection` alongside `SavedHolons`,
  and the report-derived violation count. Remove the misleading `AbandonedHolons` /
  `AbandonedByCommit` pair: abandonment remains represented by staged state and operationally
  failed holons remain live candidates with errors rather than being classified as abandoned.
  `CommitsAttempted` counts live validation and node-persistence candidates and excludes
  `Abandoned` and already `Committed` entries.
  Regenerate `generated/json-imports/dance/schema.json` from TDL rather than hand-editing it.
  `Rejected` remains distinct from `Incomplete`; the latter retains its operational persistence
  failure meaning.
- Add `Rejected` to `LoadCommitStatus.MapEnumValueType` and its Rust status representation, then
  update the transaction, loader, and Sweettest status consumers. Rejection means attempted and
  refused, not skipped.
- Keep the response surface minimal by relying on the staged-pool delivery path. Per-holon findings
  are stored on the staged holon and carried outward in its wire projection when a dance response
  restores session state, so the response does not need to re-deliver them. `RejectedHolons`
  identifies which staged holons to inspect; the findings themselves arrive with the pool.
- Capability 1 had no unattached finding to transport. Capability 2 adds transient
  `CommitValidationFinding.Projection` carriers through `CommitResponse.HasValidationFinding`,
  following the loader's `HasLoadError` pattern. Findings remain in one flat report and are
  materialized only at response construction. `ValidationViolationCount` includes both staged
  and carrier findings; no report is serialized into a string property.
- Keep `CommitValidationReport` guest-internal and in memory; expose neither a serialized report
  property nor bound references.
- Gate the existing public production Commit persistence path with assessment of the complete
  Nursery. The Nursery and its `StagedHolon` states remain the authoritative Commit workset; this
  capability introduces no separate Commit-plan representation. Rejection performs zero writes,
  leaves the transaction open with its staged candidates and replacement findings, and returns
  `Rejected`; acceptance continues through existing Commit behavior. Operational persistence
  failure remains `Incomplete` and retains its distinct partial-write semantics.
  Classify live candidates through a reference-layer helper. Use that set for validation, response
  accounting, and node persistence, but retain the existing complete Pass 2 scan so already
  committed staged entries can retry relationship persistence. Do not let an empty live-candidate
  set bypass pending Pass 2 work. Identical SmartLink replay remains an idempotent success;
  conflicting canonical keys or authoritative relationship properties remain operational failures.
  Record Pass 1 and Pass 2 failures on `StagedHolon.errors` without changing their staged state to
  `Abandoned`.
- Assess all candidates before installing outcomes. If assessment fails operationally, install no
  partial validation outcomes. After a completed assessment, replace state and findings together
  per staged holon while preserving operational errors; this does not require transaction-wide
  atomic mutation.
- Add end-to-end public Commit fixtures for an accepted Commit; inherited required-property
  rejection; zero node and SmartLink writes; rejection status, count, and `RejectedHolons`;
  staged-pool finding projection; corrected retry; abandoned and committed workset behavior;
  operational `Incomplete`; loader rejection accounting; and clean Core bootstrap. VAL-C1a's rule,
  registry, unsupported-handler, and corpus tests remain the proof of cohort-wide validator
  coverage; duplicating every rule through public Commit is not required here.
- Migrate existing Sweettest fixtures that commit undescribed holons. Describe fixtures whose
  purpose requires successful persistence or transaction lifecycle behavior, preferably with
  scenario-specific builders instead of the broad Book/People/Publisher setup. Keep purely
  pre-Commit staging fixtures undescribed where useful. Repurpose one direct Commit case and one
  loader case to assert semantic rejection, and remove or repurpose cases whose only claim was that
  undescribed persistence succeeds. Audit every staged passenger in mixed fixtures, not only the
  fixture's primary subject.

## Production Commit integration

VAL-C1b wires the VAL-C1a validator into public Commit for the cohort Capability 1 delivers:

```text
complete staged Nursery
    -> public Commit begins validation
    -> discover effective constraints and dispatch applicable bindings for each staged holon
    -> run the delivered conformance handlers and fail closed on encountered unsupported constraints
    -> reject the persistence-candidate set when violations exist
    -> otherwise proceed through the existing Commit persistence path
```

The guarantee this establishes is scoped to the schema as it currently stands and to the subject
levels this capability traverses. It is not yet the complete claim that Commit is the sole gate
for create, update, and relationship-occurrence mutation; that claim depends on the extern/API
convergence verified at the Final Coverage and Convergence Milestone. Holon deletion remains outside this
plan's gate claim.

The Holon Data Loader is one producer of staged content. It resolves references and attempts
defaults before Commit, but it does not own a validation gate.

## Non-goals

- Descriptor-holon self-conformance beyond `EnforceMinimum` and the first-active-binding
  compatibility proof required in VAL-C1a.
- String/range/enum/key constraints, relationship semantics beyond this cohort, Runtime
  Recognition, persisted evidence, and dynamic implementation dispatch.
- Default population, which belongs to VAL-PRE rather than Capability 1.

## Dependencies

- VAL0 Core Commit vocabulary and Validation-extension package-load acceptance.
- VAL-PRE construction assistance, dependency-safe findings, staged/wire result projection, and controlled
  outcome replacement.
- The dance extension schema, for the `CommitResponse` rejection surface above.

VAL-C1a owns the remaining descriptor-runtime façade and native-kind prerequisites needed by this
cohort. VAL-C1b depends on VAL-C1a, but neither issue depends on Capability 2.

## Exit demonstration

VAL-C1a demonstrates all seven active bindings and all cohort handlers over the complete
manifest-selected canonical corpus, including descriptor holons, with zero findings and an empty
effective constraint set at its delivered subject levels. Its fixtures also prove compatible and
incompatible family binding before dispatch and fail-closed unsupported rule and constraint paths.

VAL-C1b demonstrates that a public Commit over an otherwise valid staged holon that omits a
required property is rejected before any node or SmartLink write and produces a
`CommitValidationReport` and wire/staged projections. The rule reaches that holon through
inheritance alone:
`RequiredPropertyPresence.ValidationRule` is bound
once on `PropertyType.TypeDescriptor`, and the property descriptor governing the omitted property
inherits it additively through `Extends` with no binding of its own. One accepted Commit persists.
Response fixtures show a rejected assessment projecting `Rejected`, `RejectedHolons`, and its
derived violation count distinctly from an operational failure, prove that the rejected holon's
identity-only findings arrive with the returned staged pool, and prove correction and retry.
Workset fixtures prove that abandonment remains visible only through staged state and is excluded
from `CommitsAttempted`, while already committed entries can complete relationship persistence on
retry. Loader fixtures map rejection distinctly without creating operational load errors, and the
canonical Core bootstrap remains accepted. VAL-C1a's tests remain authoritative for all seven
bindings, every delivered handler, and unsupported rule and constraint handling. Strict bootstrap
Commit is the clean-corpus evidence.

---

# Capability 2 — Descriptor Self-Conformance

## Outcome

Descriptor holons themselves are validated against Schema 2.0 structural and effective-contract
invariants through the dispatch, result, and assessment path established by Capability 1.

## Scope

- Remove `AllowsAdditionalProperties` and `AllowsAdditionalRelationships` completely: delete their
  Core property descriptors and defaults, remove them from meta-type contracts and `LoaderHolon`,
  remove runtime accessors and the `no_undescribed_properties` exemption, retire their TDL syntax
  and compiler/decompiler handling, and update affected tests. Regenerate all affected imports and
  resource copies through `map-schema`; do not hand-edit generated JSON. With the exemption gone,
  `DS-BIND-001` and `DS-PROP-003` reject undeclared populated properties unconditionally.
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
  compatible evaluator for its concrete `ConstraintType`. This is what lets the 158 retained
  `CardinalityConstraint` occurrences be declaration-checked here and first evaluated in
  Capability 4.
- Preserve descriptor and member provenance in every accumulated violation.

### DS-CONTRACT-003 enforcement boundary

The full normative requirement remains unchanged: every effective member field must satisfy its
own value, endpoint, collection, and constraint policies. Enforcement is delivered incrementally
through C2–C4; C2 does not claim complete enforcement of `DS-CONTRACT-003`.

| Enforcement owner | Delivered checks |
| --- | --- |
| Existing validation, retained by C2 | Required property presence, native value kinds, missing/multiple `DescribedBy` findings, and the existing undeclared authored-relationship gate. C2's removal of `AllowsAdditional*` also makes undeclared-property rejection unconditional. |
| C2 effective-definition structure | Required singular fields resolve exactly once and optional singular fields at most once within the C2 cohort; effective member identity/name checks and `DS-CONTRACT-004` category compatibility. Enumerate the covered effective fields in implementation traceability; this is not an unrestricted singularity checker that imports later rule families. |
| C2 constraint declarations | Attachment applicability, inherited-obligation preservation, and configuration validity, including bound presence and types, non-negative bounds (narrowed by VAL-C3a to length, item-count, and cardinality families), interval consistency, and family-specific requirements. |
| C3 value semantics | Configured value evaluation and remaining property-binding, enum, default, and key conformance, including descriptor fields. Effective `InstanceKeyRule` resolution and integrity remain here. |
| C4 relationship semantics | Relationship descriptor integrity, inverse pairing and endpoint correspondence, occurrence endpoint compatibility, ordering/duplicate policies, and occurrence cardinality, including relationships authored by descriptor holons. |

Checking a cardinality declaration is C2; evaluating governed occurrence counts is C4. Checking
member categories under `DS-CONTRACT-004` is C2; general relationship endpoint compatibility is C4.
Use the shared C3/C4 validators rather than introducing separate evaluators for descriptor fields.

This delivery boundary does not weaken existing fail-closed behavior: an already-active subject
traversal that reaches an unsupported mandatory constraint still rejects. Declaration checking
alone does not require that constraint's subject evaluator. After C2, acceptance establishes the
delivered checks, not compliance with policies whose enforcement arrives in C3 or C4.

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
pass the same public Commit path and persist. A semantically rejected Commit leaves Pass-2
persistence intent unchanged: the staged round trip preserves each candidate's
`relationship_commit_scope` and `touched_relationship_names`, so the accepted retry persists exactly
the relationship set an unrejected attempt would have. Rule-to-test traceability enumerates the
effective fields covered by C2 and distinguishes completed structural/declaration checks under
`DS-CONTRACT-003` from policy evaluation assigned to C3/C4; C2 acceptance does not claim the latter.


### VAL-C2 Phase 7 — declaration execution mapping

The declaration pass is separate from subject constraint evaluation. One
`ConstraintDeclarationAssessment` is created per prospective Schema assessment, over its unchanged
reader snapshot. It checks configured constraints reached through descriptor attachments and owned
constraints without attachments. Reusable dependency-owned constraints are checked once in each
relevant Schema scope; declaration assessment never changes `RuleOf` or `ComponentOf` ownership.

| Semantic check | Execution mapping | Isolated runtime proof |
| --- | --- | --- |
| `DS-CONSTRAINT-001` | `InheritedValueConstraintNonRelaxation.ValidationRule`, prepared on the constrained descriptor for dispatch at `MetaTypeDescriptor.HolonType` | `broader_local_constraints_preserve_inherited_obligations_and_check_reusable_rules_once`; `malformed_effective_state_cannot_remove_or_reattribute_an_inherited_constraint` |
| `DS-CONSTRAINT-002` | Fixed declaration check on the constrained descriptor; no seeded rule identity | `invalid_declarations_accumulate_attachment_findings_and_fresh_assessment_accepts_correction`; `extension_owned_constraint_and_dependency_owned_reuse_do_not_change_ownership` |
| `DS-CONSTRAINT-003` | Fixed declaration check on the configured constraint holon; no seeded rule identity. A future binding would belong at `ConstraintType.HolonType` | `bounded_configuration_boundaries_are_declarations_without_evaluators`; `cardinality_and_presence_only_uniqueness_have_distinct_configuration_contracts` |

**Phase 8 collector and installation contract.** This pass uses one Schema-scoped collector,
never the per-candidate collector supplied to range-based outcome installation. A configured
constraint's first encounter emits findings against that constraint, even when reached through a
different descriptor; subsequent encounters reuse its result. Before installing outcomes, route
findings by their structured subject identity to the corresponding live staged candidate. Findings
without a staged subject carrier go to the transaction-wide carrier. Never install the entire
Schema collector on the candidate that happened to encounter the constraint first. The regression
`shared_invalid_constraint_findings_keep_their_subject_in_either_candidate_order` pins subject
attribution; Phase 8 must additionally test installation in both candidate orders, including an
unstaged shared constraint.

**Related rule findings.** Declaration parameter membership (`DS-CONSTRAINT-003`) and C1's
`NoUndescribedProperties` (`DS-PROP-003`) are independent rules. After activation, both may report
the same populated undeclared parameter on the same constraint holon. This is permitted by the
issue's finding-provenance policy allowing related findings without cross-rule deduplication; it
is not permission to execute either assessment twice. Retain both rule identities/codes and
complete messages. Phase 8/9 orchestration must reuse prerequisite results and avoid repeating a
rule through prerequisite and binding dispatch. Declaration checking must remain usable for
reusable constraints without requiring a subject evaluator merely to check their configuration.

The kernel supplies parent and child effective constraint contributions before normalization. The
preservation check compares selected constraint identities and original declaring descriptors; it
does not compare each local interval with its parent's interval. Retaining inherited obligations
makes a broader local contribution valid. A negative preservation fixture must explicitly corrupt
the effective product, since additive authoring has no removal or override operation.

Declaration observations use `constraint_attachment_count` and `constraint_declaration_count`.
The first measures effective attachments actually visited; the second measures distinct configured
holons checked in the Schema scope. Corpus totals are derived from visited contributions rather
than a fixed cardinality-attachment inventory. Neither increments `effective_constraint_count`,
which remains exclusive to subject evaluation. The
`declaration_acceptance_does_not_enable_an_unsupported_subject_evaluator` test covers both paths:
a valid declaration requires no evaluator, while a subject traversal reaching an unsupported
mandatory constraint still rejects.

The configuration pass checks prospective declared parameter membership and the normalized
non-negative integer bounds (VAL-C3a narrows this to non-signed families), conditional Boolean
inclusivity, cardinality exception, and presence-only uniqueness configuration. Own-contract requiredness and native-kind checks remain
with the shared C1 validators in the readiness pass. This is C2 structural/declaration coverage of
`DS-CONTRACT-003`; value, enum, default and key policies remain C3, and relationship endpoint,
collection and occurrence/cardinality policies remain C4. No occurrence counts are evaluated here.

Malformed readable declarations produce findings; dependent attachment checks report blocking
findings where necessary. Operational read failure invalidates the whole assessment and its
collector. A corrected retry creates a fresh scope and recomputes declarations, including staged
replacements selected through the prospective reader.

Phase 7 supplies isolated APIs, a registered monotonicity handler and tests. Commit scheduling
arrives in Phase 8; the new binding roots and fixed declaration path activate with canonical
bindings and projections in Phase 9. Cardinality attachments remain attached, and `Length16k`
remains detached throughout this phase.

---

# Capability 3 — Value, Enum, Default, and Key Conformance

## Outcome

The shared validator assesses completed ordinary holons and descriptor holons against effective
property contracts, scalar value constraints, enum definitions and tokens, default declarations,
and key rules. Descriptor fields use the same value path as ordinary instance fields, completing
the C3 portion of `DS-CONTRACT-003` deferred by C2.

Descriptor Runtime supplies one key-rule resolver and read-only composer for staging, loading,
schema tooling, and Commit. At capability exit, public Commit rejects C3 semantic violations
before any node or SmartLink write. Descriptor-independent PVL checks still run during
persistence, so a PVL failure can still leave a partial write; Capability 4 moves them ahead of
writes.
Acceptance establishes the narrower key guarantee that this Commit introduced no conflicting key
claim; it does not certify that all visible Space keys are already collision-free.

## Delivery structure

Capability 3 is delivered through seven sequential issues. Scalar constraints come first, followed
by enums and defaults. Key work has a separate design/spike issue before resolver implementation,
corpus alignment, producer support, and Commit activation. No issue depends on parallel delivery.

[map-holons #803](https://github.com/evomimic/map-holons/issues/803) lands before VAL-C3a and
changes no behavior. It retires the non-production validator traversal and adds the report-only
`assess_commit_candidates` entry. It also applies the validator naming rules in Commit Validation
Design Spec §5.2, so C3 evaluators are built against one path. Report-only runs over the whole
corpus belong to the VAL-C3c-1 harness and the VAL-C3c-2 standalone report; both can call that
entry.

| Issue | Delivers | Production Commit effect |
| --- | --- | --- |
| VAL-C3a | Scalar evaluators, explicit property/value execution contract, signed numeric bounds, `Length16k` restoration | Activates scalar rejection |
| VAL-C3b | Enum definition/token rules, default-declaration rules, remaining property/holon conformance | Activates enum and default rejection |
| VAL-C3c-1 | Key decision record, execution map, native corpus-harness spike | None; closes design gates |
| VAL-C3c-2 | Descriptor Runtime key resolution/composition, TDL semantic-name correction, standalone corpus report | None; report-only scaffolding |
| VAL-C3d | Manifest-selected corpus key alignment and source-scope gate | None; corpus and regeneration only |
| VAL-C3e | Compose-and-set producer helper, coherent staged key lookup, committed keylessness | Keyless candidates persist and can be read correctly; no new key-validation rule |
| VAL-C3f | Key conformance and key-introduction uniqueness in Commit; capability exit | Activates key rejection |

VAL-C3c-1 through VAL-C3e are independently testable scaffolding under the Delivery Principles.
Their completion does not claim the key vertical slice; that slice closes at VAL-C3f.

## Decision record

These decisions govern the work in this capability. Changes to enduring semantics must land in
the governing specifications with the issue that first depends on them, before activation.

| Decision | Resolution |
| --- | --- |
| String length | Count Unicode 17.0.0 default extended grapheme clusters under UAX #29, without normalization. Pin the Rust segmentation dependency exactly and test the official conformance data. TypeScript/browser counts are advisory unless they execute the same versioned implementation. |
| Scalar constraints | String length, byte length, and integer range share one typed evaluation path for ordinary and descriptor fields. Every effective applicable contribution must pass. |
| Bound signedness | `NumericRangeConstraint` admits signed integers. Length, item-count, and cardinality bounds remain non-negative. Signedness belongs to each family's `DS-CONSTRAINT-003` configuration contract, not to the shared `Minimum` / `Maximum` property descriptors. |
| Empty accepted sets | Preserve the ordered-bound configuration contract; do not add a general satisfiability solver. An ordered integer interval such as `(0, 1)` may accept no integer. Comparisons must not overflow at the limits of the integer representation. |
| Constraint activation | A reached effective attachment is mandatory independently of `ValidationBindings`, as Commit Design Spec §7 already requires. `PropertyValueConformance` neither activates constraints nor executes them a second time. |
| Arrays | Defer runtime array representation and evaluators. Array value types remain declarable; populated array values are not supported. Reached `ItemCountConstraint` or `UniqueItemsConstraint` attachments fail closed with `UnsupportedConstraintType`. Declaration assessment alone does not require an evaluator. |
| Defaults | Defaults are construction assistance. Commit validates explicit state and never fills omissions. A default belongs only to a required property and must satisfy its effective value type, enum membership where applicable, and constraints. Assess the declaring definition even when no instance populates the property. |
| Enum representation | `BaseValue::EnumValue` carries an exact string token matching a variant's local `TypeName`. Keys, qualified keys, display names, case-folded strings, and normalized spellings do not substitute for tokens. |
| Enum token evolution | A variant's local `TypeName` is immutable within its version lineage. A replacement token requires a new variant lineage. Ordinary Commit does not prove that value migration has completed or assess the migration consequences of variant removal. |
| Keys and lineage | Keys may change across versions. Persisted lineage identity comes from record-derived lineage-root metadata, never from keys or `ProspectiveIdentity`. A new lineage has a distinct assessment-local identity until its record exists. |
| Key-policy execution boundary | Apply `DS-KEY-004` and `DS-KEY-005` to new immutable versions: `ForCreate` and `ForUpdateNewVersion`. Do not recompose or retrospectively apply a changed key policy to existing versions reused by `ForUpdateGraphOnly` or `ForUpdate`. Descriptor declarations still receive their applicable readiness checks. |
| Producer boundary | Composition is read-only. An explicit writable-reference helper composes and sets a staged key. Loader imports preserve authored keys because those keys are also reference handles. Commit validates keys and never rewrites them. |
| Keylessness | Keep `NoneRule.KeyRuleType`; semantic keylessness is an absent `Key`, not an empty string. A type may instead use an explicit stable-identifier property. Keyless persistence and reads must work before key validation activates. |
| Key comparison and shape | Compare exactly, without normalization or case folding. Keyed results must be nonempty, NUL-free, and within the existing `MAX_CANONICAL_KEY_BYTES` limit. Do not duplicate or change that limit. |
| Template spelling | Use `{0}`, `{1}`, … with `{{` / `}}` for literal braces. Migrate `$0`; do not retain both spellings. Parameter rendering has a specified canonical representation, not a generic `Display` implementation. |
| Key-introduction uniqueness | Reject newly introduced conflicting claims across distinct lineages in the local Space's prospective visible-head view. Multiple heads of one lineage are a resolution ambiguity, not a lineage collision. Preserve read-time `MultipleLineageHeads` checks. |
| Source-scope binding | Within a package and its dependency closure, binding an authored key selects exactly one version. Two versions of one lineage still violate this source-binding requirement. This is separate from Commit's lineage-uniqueness rule. |

### Shared execution and assessment scope

All ordinary semantic resolution uses the unchanged C2 prospective reader snapshot. Extend the
existing descriptor facades with reader-aware operations for enum variants, constraint
configuration, key-rule selection, parameters, and ownership evidence; do not introduce a second
resolver. A staged replacement must affect every dependent result consistently. The intentional
exception is comparison with a recorded saved source: enum-token immutability and source-key
comparison read that exact immutable version through the Reference Layer, without prospective
replacement selection.

Definition assessment is bounded: assess relevant definitions in each affected Schema workset and
the descriptor dependencies actually consumed by the delivered traversal. This includes an
unstaged property or enum definition whose default or token contract the assessment relies on.
It does not revalidate every saved definition or instance in the Space. Extend readiness dependency
collection as new inputs become semantically relevant. Reuse assessment-local products, preserve
subject/provenance attribution, and report an unavailable mandatory prerequisite explicitly.
Operational read failures remain `HolonError`s and invalidate the assessment rather than becoming
semantic findings or installing partial validation outcomes.

#### DescriptorPackage preparation demand

Commit assessment consumes the assessment-scoped DescriptorPackages defined in the
[Commit Validation Design Specification](commit-validation-design-spec.md#assessment-scoped-descriptorpackages).
Package construction prepares only the schema-side demand of the delivered checks, so every
capability that reads a new schema input must extend that demand in the same delivery. The
construction edge list and role-specific additions currently cover only the C2 inputs listed in
the package preparation follow-up below. A C3 or C4 check must not read an unprepared definition
or relationship after construction; the post-construction zero-backend-query regression remains a
completion criterion for each issue. Keep preparation demand separate from readiness
dependencies: preparing an input does not schedule its target for validation.

Anticipated additions, to be confirmed by each issue:

| Issue | Additional prepared demand |
| --- | --- |
| VAL-C3a | Configuration properties of reached constraints, and their concrete constraint-type lineage, for subject evaluation rather than only declaration checks |
| VAL-C3b | `Variants` and variant `TypeName` evidence; recorded saved sources of staged variant successors; `DefaultValue` declarations and the effective value types they are assessed against |
| VAL-C3c-2 / VAL-C3f | `InstanceKeyRule` and key-rule target lineage; configured rule parameters such as `TemplateParameters`; key-input relationships and their selected target versions; enum-variant owner evidence |
| Capability 4 | Declared and inverse relationship descriptors, `HasInverse`, endpoint declarations, and effective `CardinalityConstraint` configuration for occurrence assessment |

### Key design gates closed by VAL-C3c-1

The design issue records each resolution in the governing specifications before VAL-C3c-2 starts.

1. **Semantic names in TDL.** Declaration keys remain authored independently of `TypeName`.
   Define explicit semantic-name syntax and the shorthand retained where source syntax already
   supplies the name, such as a nested variant label or relationship endpoint declaration. Lower
   shorthand mechanically; do not invert runtime key rules in the parser. Correct both abstract
   variant anchors, `EnumVariantValueType.ValueType` and
   `MapEnumVariantValueType.EnumVariantValueType`. Specify compiler/decompiler round trips and
   retention of relationship endpoint consistency checking.
2. **Descriptor-family key policy.** Map governing `InstanceKeyRule` placement for ordinary holon
   types, roots/kind anchors, meta-types, specialized describing meta-types, key-rule/projection
   families, and value descriptors with immediate-parent keys. Distinguish the rule on `D(T)`
   that governs the key of descriptor `T` from the rule on `T` that governs its instances.
   Ordinary holon types should retain `{TypeName}.HolonType`; established `ExtendedTypeRule`
   families should retain their convention. Prove how describing populations are distinguished
   before changing a shared meta-type's rule; no placement may silently rekey roots or meta-types.
3. **One resolver and native corpus harness.** Spike a native harness that stages the
   manifest-selected corpus through real loader assembly and final enum/default completion into
   an in-memory transaction, then uses real descriptor facades and the validator in report-only
   mode. Confirm execution-context and dependency feasibility rather than assuming the guest
   loader can be imported into a host workspace. If this route is infeasible, record a feasible
   reuse boundary that preserves one assembly/completion path and one semantic resolver.
   Composition formatting stays pure and WASM-safe over typed, already-resolved inputs; semantic
   input gathering stays in Descriptor Runtime. Do not restore a separate semantic IR or put the
   resolver in `map_schema_semantic`.
4. **Claims and prospective heads.** Formalize `DS-KEY-006` using the predicate below, root
   metadata, indexed lineage discovery, and a publication overlay consistent with established
   lineage-head traversal. Specify predecessor supersession, historical branches, retained
   sibling heads, rekeys, and key reuse within one Commit. Exact-source `ProspectiveIdentity` is
   insufficient for lineage identity. Fix the local Space scope and keep the distinct
   package/dependency-closure source-binding rule.
5. **Relationship parameters and ownership.** Prefer configured, typed `FormatRule` parameters
   over a theme-specific unconfigured `RelationshipPairRule` algorithm. The current
   `TemplateParameters` contract admits only property descriptors; relationship inputs require
   an explicit vocabulary change. Specify parameter kind, singularity, scalar rendering, exact
   selected target version, and errors for missing, contested, or keyless targets. Prefer reading
   an explicitly present target key over recursive recomposition; targets are composed first,
   with incomplete/cyclic construction dependencies diagnosed. Key-producing relationship inputs
   belong to the keyed holon's definition so changing them creates a new immutable version.
   Version classification reads `IsDefinitional` from the relationship descriptor, so each such
   relationship must be declared definitional; otherwise a change stays graph-only and leaves the
   key stale.
   A later rekey of a target does not implicitly rekey referencing holons.

   For theme assignments, prefer a declared assignment-to-theme input; otherwise define bounded
   evidence from authored theme-side occurrences. Do not depend on an inverse that appears only
   after persistence. Enum-variant keys retain `{EnumKey}.{VariantTypeName}`. Their owner evidence
   comes from the declaring enum's authored `Variants` occurrence, not inherited membership.
   Specify equivalent evidence for standalone staging/runtime composition, bounded ambiguity
   detection, and treatment of abstract variant-family anchors.
6. **Execution map and baseline invariant.** Confirm compatibility of every seeded rule family,
   subject level, route, binding root, and supplied context. Reclassify descriptor-definition
   rules where necessary before authoring bindings. Split `DS-KEY-003`: assert the kernel's
   `Override` table entry as a kernel invariant, while runtime schema assessment verifies the
   singular/required relationship declaration and explicit root `NoneRule` selection. The
   data-dependent portion cannot be replaced by a table assertion. Record its binding or fixed
   declaration-check route without executing it twice.

`TypeNameRule.KeyRuleType` is unused in the current corpus. It remains supported vocabulary;
retirement would be a separate decision.

### Key-introduction predicate

For a new keyed immutable version with key `K`, identify its lineage `L` independently of `K`.
It makes a claim when it creates a lineage, changes the exact saved source's key, or publishes
`K` for `L` when no visible pre-Commit head of `L` currently holds `K`. The third case is essential:
`A1(K) -> A2(J)`, followed by another lineage acquiring `K`, must not allow a branch from
historical `A1` to republish `K` merely because its exact source also had `K`.

Assess claims against the complete prospective visible-head overlay, preserving unrelated
branches and removing only heads actually superseded by publication. A claim conflicts with a
prospective head or another live prospective claim holding `K` in a distinct lineage. Define
visibility consistently for any publication superseded within the same workset. Key release and
reuse, including a swap between lineages, are assessed against the resulting view rather than
candidate iteration order. Multiple heads within `L` remain a separate ambiguity.

This predicate deliberately permits a same-key continuation of an existing visible association
without certifying or repairing old cross-lineage collisions. Checking every newly published
keyed version would be a stronger alternative: it would require more key lookups and could block
ordinary updates after an existing concurrent collision. This plan adopts the introduction rule.
Concurrent writes outside local visibility remain possible.

## Specification corrections and plan reconciliation

| Document or source | Correction | Lands with |
| --- | --- | --- |
| `value-constraints-design-spec.md`; `descriptor-semantics-rules.md` `DS-CONSTRAINT-003` | Family-specific signedness, versioned Unicode policy, empty-interval policy, declarable but uninstantiable array types | VAL-C3a |
| Core TDL descriptions of `Minimum` / `Maximum` and bounded constraint families | Remove universal non-negativity and inaccurate inclusive-only wording; regenerate projections | VAL-C3a |
| `descriptor-semantics-rules.md` §1.9 and `DS-ENUM-003` | Exact `EnumValue` token representation and lineage token immutability | VAL-C3b |
| Validation Schema spec and canonical rule metadata | Descriptor-definition subject/family corrections and explicit property-conformance execution ownership | VAL-C3a / VAL-C3b |
| `descriptor-semantics-rules.md` key sections; new `DS-KEY-006` | Family policy map, key shape/evolution, version-state boundary, introduction predicate, enum-variant key form, source scope | VAL-C3c-1 |
| `core-schema-bootstrap-design-spec.md`; `tdl-spec.md` | `{0}` format spelling, authored semantic names/shorthand, declared-only owner evidence | VAL-C3c-1 |
| Validation Schema Design Specification | `DS-KEY-006` rule identity, Commit-only context compatibility, updated inventory/execution map | VAL-C3c-1 |

Commit Design Spec §7 already makes attached constraints unconditional; preserve that invariant.
Clarify diagnostic ownership where `PropertyValueConformance` is named, without making its
binding a constraint activation gate. Its stable identity may identify a constraint finding even
when its non-constraint handler is not bound.

Adding `DS-KEY-006` grows the seeded rule inventory by one. Track seeded identities, active
bindings, fixed checks, and implemented handlers separately; a seeded identity is not
necessarily a bound rule.

## Corpus baseline

The following counts are provisional results of an ad-hoc probe on 2026-10-07 over generated
imports, not verified counts over the manifest-selected assessment scope. VAL-C3c-2 replaces
them with a reproducible native report. VAL-C3d resolves every finding or records a disposition
that does not excuse an unsupported reachable strategy or a conformance violation.

| Provisional finding | Count | Notes |
| --- | --- | --- |
| Keyed holons whose effective rule is `NoneRule` | 151 | Includes 48 `ValidationRule` instances, 63 `DesignToken` instances, and dahn/dancer/theme/meta-design-system instances; several have no name property |
| Holons governed by extension-defined `RelationshipPairRule` | 126 | `ThemeTokenAssignment`; authored keys are internally inconsistent |
| `ExtendedTypeRule` mismatches | 39 | 36 are holon types keyed `{TypeName}.HolonType` under an intermediate parent |
| Enum-variant keys differing from documented `{EnumName}.{Variant}` | 63 | Corpus/compiler use `{EnumKey}.{Variant}`; correct the documentation |
| `FormatRule` template spellings | 2 instances | `HolonSpaceNameRule` uses `$0`; `ImplementationName` uses `{0}` |
| Compiler-derived `TypeName` defects | At least 2 confirmed anchors | Both abstract variant anchors require correction; full inventory comes from the report |
| Enum tokens / default declarations | 295 / 11 | Probe reported conformance; verify through the delivered evaluator |

Preserve code-referenced `ValidationRule` keys unless their change is deliberate and propagated
to `type_names` and all consumers. The corpus scope comes from the bootstrap manifest, not a
recursive scan of every generated file.

## Rule execution map

Use existing rule families and binding-placement conventions. Reclassify the seeded family and
level for descriptor-definition rules before binding; do not bind a value-family rule below its
family root to force a holon-definition check. Register canonical rule identity and context
compatibility explicitly. A mandatory contextual check with missing context fails closed.

| Rule identity | Semantics and subject | Family / level | Route and binding target | Issue |
| --- | --- | --- | --- | --- |
| `PropertyValueConformance` | `DS-PROP-002`; present effective property value, including conflicting contributions | Property / Property | Property validation at `PropertyType.TypeDescriptor`; reuse the shared value outcome | C3a |
| `EnumTokenMembership` | `DS-ENUM-002`; stored enum value | EnumValue / Value | Value validation at `EnumValueType.ValueType` | C3b |
| `EnumMemberNamesUnique` | `DS-ENUM-001`; enum definition | Holon / Holon | Descriptor self-conformance at `MetaEnumValueType.MetaValueType` | C3b |
| `EnumTokenNonRetroactivity` | `DS-ENUM-003`; variant successor and exact saved source | Holon (`Contextual` determinism) / Holon | Descriptor self-conformance at `MetaEnumVariantValueType.MetaValueType`; recorded-source context required | C3b |
| `DefaultsRequireRequiredProperties`, `DefaultValueConformance` | `DS-DEFAULT-001/002`; property-descriptor definition | Holon / Holon | Descriptor self-conformance at `MetaPropertyType.MetaTypeDescriptor`; shared value assessment | C3b |
| `UniquePropertyMemberBinding`, `ConcreteDescribingType`, `AbstractMemberMinimumEnforcement` | `DS-BIND-001`, `DS-CONFORM-001/002`; property or holon | Existing compatible Property/Holon families | Audit and complete actual handlers at convention roots; reuse prior prerequisite results | C3b |
| `EffectiveKeyRuleSelection`, `KeyRuleTargetCompatibility` | `DS-KEY-001/002`; holon-type descriptor | Holon / Holon | Descriptor self-conformance at `MetaHolonType.MetaTypeDescriptor` through the key resolver | C3f |
| `ExplicitKeylessBaseline` | `DS-KEY-003`; kernel table and canonical root declarations | Holon / Holon for runtime portion | Kernel assertion plus the root-aware declaration route recorded by C3c-1 | C3f |
| `ExplicitKeylessness`, `KeyPresenceAndValue` | `DS-KEY-004/005`; new immutable holon version | Holon / Holon | Holon validation at `HolonType.TypeDescriptor`, using `compose_key` | C3f |
| New key-introduction uniqueness identity | `DS-KEY-006`; live prospective claim | Holon (`Contextual` determinism) / Holon | Commit aggregate validation at `HolonType.TypeDescriptor`; local Space/Nursery context required | C3f |

Fixed subject traversal discovers attachments, resolves evaluator compatibility, and evaluates
supported constraints once per subject/contribution. Discover unsupported attachments even when
a native-kind failure prevents evaluating a supported constraint. Never evaluate a supported
constraint against the wrong native representation. Preserve the constrained subject, configured
constraint, concrete constraint type, and declaring-descriptor provenance in findings.

`PropertyValueConformance` owns the property-level `DS-PROP-002` assessment: effective-value
singularity and use of the selected value descriptor. It incorporates the shared value result
without repeating native-kind or constraint evaluation. Existing native-kind handlers own their
kind checks; attachment traversal owns scalar evaluation. Define result reuse and diagnostic
attribution explicitly in C3a so binding and delegation cannot assess the same subject twice.

---

## VAL-C3a — Scalar Value Constraints

- Land the signed-bound corrections before activation. Update C2's declaration check so only
  length, item-count, and cardinality families require non-negative bounds. Confirm that shared
  `Minimum` / `Maximum` value descriptors admit negative integers, update canonical TDL
  descriptions, and regenerate affected projections. Retain conditional bound inclusivity checks.
- Pin `unicode-segmentation = "=1.13.2"` directly in the evaluating shared crate for Unicode
  17.0.0. Verify compatibility with the Holochain-required toolchain, including its Rust 1.85.0
  minimum. Align affected host/hApp resolutions deliberately; use a targeted lockfile update,
  not a broad dependency update. Future Unicode-table upgrades are versioned validation changes.
- Implement the shared typed evaluators for `StringLengthConstraint`, `BytesLengthConstraint`,
  and signed `NumericRangeConstraint`. Honor each bound's inclusivity and every effective
  applicable contribution. Supply actual values and prospective configuration products to the
  evaluator; native-kind facts alone are insufficient.
- Complete `PropertyValueConformance` under the execution contract above, author its compatible
  binding, and regenerate through `map-schema`. Prove constraint rejection with that binding
  absent as well as present. No binding absence may suppress a reached attachment.
- Restore exactly the detached occurrence
  `MapStringValueType.StringValueType -[Constraints]-> Length16k.StringLengthConstraint`
  in `schema-src/core/concrete-value-types.tdl`. Regenerate its JSON, bootstrap bundle, and
  resource projections through the established tooling.
- Keep arrays without a runtime representation or handler. Prove that declaration checking alone
  accepts a valid deferred array constraint, but reaching its attachment in subject evaluation
  rejects with `UnsupportedConstraintType`.

PVL currently limits strings to 16,384 UTF-8 bytes, while `Length16k` limits grapheme count.
Every grapheme consumes at least one byte, so `Length16k` cannot be the deciding rejection for a
value PVL would accept. Restore it for semantic fidelity, but prove scalar rejection with tighter
schema-authored bounds that stay within PVL. No grapheme bound implies a byte bound, so the
byte-ceiling case belongs to Capability 4's pre-write PVL preflight.

**Tests and exit:** vendor Unicode 17.0.0 `GraphemeBreakTest.txt` and verify complete boundary
positions, not merely counts. Cover combining sequences, emoji ZWJ, regional indicators,
canonically equivalent stored strings, byte/grapheme divergence, signed and exclusive boundaries,
empty integer intervals, and integer extrema. Public Commit rejects tighter scalar violations and
out-of-range signed integers before writes; boundary cases persist. The manifest-selected corpus
has zero findings for the activated cohort. Validate shared-crate WASM reachability with
`npm run check -w map-happ`.

## VAL-C3b — Enums, Defaults, and Remaining Property Conformance

- Land the `EnumValue` wording and lineage token-immutability correction before activation.
- Implement `DS-ENUM-001` on enum definitions and `DS-ENUM-002` on enum values. Build one
  prospective-reader-aware variant product preserving distinct variant identities, local tokens,
  and declaring provenance. Do not collapse to a token set before detecting duplicates. Reuse
  this product for membership and definition checks; key/display-name spelling never matches.
- Implement `DS-ENUM-003` for a staged variant successor. Read its recorded saved source as an
  exact immutable version through the Reference Layer and compare local `TypeName`. Changing
  the token is a violation; a replacement token uses a new lineage. An ordinary newly created
  variant has no source comparison. Missing required source evidence for a successor is an
  explicit inability to assess, not a silent exemption.
- Implement `DS-DEFAULT-001/002` on the declaring property descriptor. Check requiredness and
  assess the default against that property's effective value type using the common native-kind,
  enum, and scalar-constraint path. Do not validate only against the broad value type of the
  `DefaultValue` field. Assess unused definitions and consumed unstaged definitions within the
  bounded readiness scope, including prospective dependency changes that invalidate a default.
- Audit remaining `DS-CONFORM-*`, `DS-BIND-*`, and `DS-PROP-*` against actual C1/C2 behavior and
  registered handlers. `ConcreteDescribingType`, `UniquePropertyMemberBinding`, and
  `AbstractMemberMinimumEnforcement` are not complete merely because an earlier readiness check
  looks related. Add missing behavior and isolated negative proofs, map existing behavior to
  identities, and reuse results without repeating assessment. Preserve the fixed declared-
  relationship name gate; endpoint/cardinality/aggregate semantics still belong to C4.
- Correct seeded rule families/levels before authoring the definition bindings in the execution
  map. Extend readiness dependencies and regenerate all affected canonical projections.

**Exit:** public Commit rejects an undeclared token, key/display-name token spellings, duplicate
effective member names, a same-lineage token change, an optional property default, and a default
violating its selected kind, enum membership, or constraints. Unused and consumed unstaged
definitions are covered. Correction/retry succeeds, explicit omissions remain omissions, and the
manifest-selected corpus stays at zero findings for all activated C3 value rules.

## VAL-C3c-1 — Key Decisions and Native Harness Spike

Close gates 1–6 and land their specification corrections before resolver implementation or corpus
alignment. Record the native harness spike, reuse boundary, execution-context/dependency result,
and how loader final completion is reused without copying its algorithms. Produce a concrete
family-policy map and a fixture matrix for source/lineage identity, historical branching,
relationship parameters, owner evidence, template errors, and key shape. Name the new
`DS-KEY-006` identity and specify its Commit-only context.

**Exit:** the governing specs contain every gate decision and the implementation issue has no
unresolved family-placement or ownership strategy. A minimal native load/complete/resolve proof
or a demonstrated alternative establishes feasibility of the standalone corpus report. No key
rule is newly activated in public Commit.

## VAL-C3c-2 — Descriptor Runtime Key Resolution and Composition

This issue belongs to Descriptor Runtime, not `holons_validation` or a Commit-only API.

- Extend the existing `HolonDescriptor::effective_key_rule` and `KeyRuleDescriptor` facades,
  with current/prospective reads sharing one implementation. Effective `InstanceKeyRule` follows
  the kernel's ordinary `Override` / `EffectiveValues` semantics. Zero/multiple selections and
  abstract/unsupported targets are typed errors; absence never silently means keyless.
- Expose read-only `compose_key` over completed holon state, returning an explicit keyed result,
  explicit keylessness, or a typed composition error. Cover incomplete/ambiguous inputs, invalid
  parameters/placeholders, missing/contested/keyless relationship targets, owner ambiguity,
  construction cycles as specified, unsupported strategies, and invalid key shape. Operational
  reads stay errors. Subsume `derive_constraint_instance_key`; do not keep a second algorithm.
- Implement the active corpus strategies: type-name, schema-name, enum-variant, relationship,
  extended-type, described-type, constraint-instance, configured format/relationship parameters,
  and explicit keylessness. Input gathering uses descriptor facades; formatting remains pure,
  typed, and WASM-safe. Standalone and enum-side composition use equivalent declaring-owner
  evidence. The resolver reports a relationship key parameter whose relationship is not
  definitional.
- Correct TDL semantic-name lowering according to gate 1, including both abstract variant
  anchors and explicit `TypeName` handling. Test compiler/decompiler fidelity and endpoint
  consistency. This is syntax lowering, not descriptor-semantic execution in the parser.
- Deliver the fast standalone native report over the manifest-selected corpus through the
  agreed harness. Assess key conformance and single-version source binding in each package's
  dependency closure. Emit reproducible subjects, governing rules, expected/authored keys, and
  dispositions. Report-only findings do not stop loader assembly or rewrite keys.

**Exit:** fixtures cover every strategy and typed failure. The corpus report runs without Nix,
replaces the provisional baseline, and demonstrates the same result as runtime facade composition.
Key findings are not yet a production Commit gate. Corpus edits remain limited to fixtures and
required compiler-generated semantic-name corrections; policy/key alignment belongs to VAL-C3d.
`map-schema check` may invoke the same report as a separate post-lowering phase. Language-server
integration is a follow-up, not a capability prerequisite or a second resolver.

## VAL-C3d — Corpus Key Alignment and Source Gate

- Apply the decided family-policy map to canonical Core and every manifest-selected extension.
  Give keyed types an appropriate governing rule and explicit name or stable-identifier inputs
  where needed. Cover Validation Rules, design tokens, visualizers/dancers/canvases, themes,
  meta-design-system instances, and theme assignments.
- Preserve code-referenced keys unless deliberately changed with all consumers. Correct
  mismatches and references; migrate `$0` to `{0}` and align relationship-derived key inputs,
  declaring each key-input relationship definitional.
- Regenerate affected JSON, bootstrap bundles, and resource copies through `map-schema`. Update
  loader metrics and any deliberately changed `type_names` constants.
- Make the standalone manifest-selected report a CI gate for key conformance and package/closure
  single-version source binding. Do not defer this source gate until Commit uniqueness activates.

**Exit:** no key-conformance or source-binding findings remain; every provisional baseline row has
a verified resolution or scope disposition. Canonical bootstrap still loads. Public Commit key
activation remains deferred to VAL-C3f.

## VAL-C3e — Producer Helper and Committed Keylessness

- Add an explicit compose-and-set helper on the established writable-reference surface. It uses
  the shared composer, sets the composed key or removes a stale key for explicit keylessness,
  and changes no unrelated state. Equal state is a no-op; a real key change uses ordinary
  definitional mutation/version classification. No construction path composes implicitly.
- Make staged key lookup coherent after setting, changing, or removing a key. Inspect the
  Nursery/pool and relevant collection index behavior; insertion-time indexing alone cannot
  satisfy the helper contract. Define index maintenance through the existing mutation path,
  with tests for initial key assignment, rekey, key removal, and duplicate-key ambiguity rather
  than a helper-only lookup surface.
- Fix keyless Commit Pass 1. Today it requires a key after persisting the node, which can produce
  a partial write with an `Incomplete` outcome. Produce an ID-bound saved reference for keyless
  nodes, retain ordinary ownership and relationship processing, retain unkeyed `Owns`
  relationships, and emit keyed `Owns` index entries only for semantic keyed results.
- Support keyless saved holons in affected read/hydration paths, including relationship loading
  that currently expects every SmartLink to carry a key. Keep physical empty-key encoding
  separate from semantic keylessness. Preserve loader authored keys; keyless loader input
  remains unsupported because loader references are key-based.

**Exit:** a caller explicitly composes and sets a key before public Commit. A programmatically
staged `NoneRule` holon commits, appears in `SavedHolons`, and has correct ownership/relationships
without a keyed index entry. A fresh transaction can read it by ID, enumerate ownership, traverse
relationships, and update it. Helper mutations preserve staged key lookup and phase semantics.

## VAL-C3f — Key Conformance in Commit and Capability Exit

- Implement and bind `DS-KEY-001/002` through the shared resolver. Implement the decided
  runtime/kernel split for `DS-KEY-003`. Resolver/composer semantic failures become findings
  with no second algorithm; operational failures remain errors.
- Activate `DS-KEY-004/005` for new immutable versions, including descriptor holons.
  `NoneRule` requires absent semantic `Key`; keyed rules require exactly the composed result
  and valid shape. Historical graph-only/no-action versions are not recomposed or retroactively
  checked against a changed policy. Test both sides of this version-state boundary.
- Implement `DS-KEY-006` with the introduction predicate and prospective-head overlay above.
  Obtain lineage-root metadata through the Reference Layer. Discover indexed lineages once per
  distinct assessed key, reuse established head traversal, and cache assessment-local products.
  Read the candidate lineage's pre-Commit heads when needed to recognize reintroduction from a
  historical source. Overlay all publications before deciding conflicts; do not use a
  single-result key lookup that conflates multiple heads with distinct lineages.
- Register the uniqueness rule only for compatible Commit context with the required local
  Space/Nursery authority. Test new roots, rekeys, same-key continuations, historical branches,
  retained sibling heads, key release/reuse and swaps, distinct-lineage candidate conflicts,
  and same-lineage multiple heads. Preserve read-time ambiguity detection and explicitly show
  that a preexisting collision need not be repaired by an unrelated accepted Commit.
- Add loader and public-Commit cases for each C3 family using the existing rejection/retry,
  saved-content, disposition, and fresh-transaction graph assertions. Keep bytes constrained
  through typed programmatic staging: JSON loader bytes encoding is a separate ingress decision,
  not an implicit prerequisite or a string-to-bytes conversion in the validator.
- Run the standalone gated corpus check and the whole manifest-selected corpus through the
  report-only validator with zero findings. Reconfirm strict canonical bootstrap acceptance.

## Non-goals

- Default population in Commit, runtime array values/evaluators, or a second key/constraint
  interpretation in tooling.
- Proof that enum-token/key migration has completed, or revalidation of every saved Space
  definition and instance.
- Retroactive recomposition of immutable keys, cascading rekeys, or key checks on a reused
  historical version solely because a graph-only change is committed.
- Global/concurrent uniqueness, repair of all preexisting collisions, and schema-qualified key
  namespaces deferred to Extension Schema identity design.
- Keyless loader input, a new JSON bytes encoding, or mandatory language-server integration.
- Changing PVL limits, moving descriptor semantics into PVL/Integrity, or promising rollback
  and atomic persistence after operational failures.

## Dependencies

- Completed Capabilities 1 and 2, including public Commit gating, prospective reading, and
  Schema-scoped declaration assessment. C3a deliberately corrects C2's bound-signedness check.
- Descriptor Runtime effective products and facade operations, extended with prospective reads
  as needed; no parallel inheritance or effective-contract implementation.
- Shared best-effort default population and loader final completion for construction fixtures.
  Commit remains an assessor of explicit state.
- Record-derived lineage metadata, keyed `Owns` discovery, and established head traversal for
  Commit uniqueness.

## Exit demonstration

Public Commit fixtures demonstrate accepted and rejected string, byte, and signed numeric values;
enum definitions/tokens and lineage token immutability; default declarations; key selection,
shape, keylessness, equality, and introduction conflicts. Loader fixtures cover the families its
authored representation supports; bytes and keyless holons use typed programmatic staging.

Every C3 semantic rejection happens before any node or SmartLink write, including a multi-candidate workset with a later invalid node. Correction and
retry preserve persistence intent. Accepted cases persist explicit state, with fresh-transaction
evidence for keyless ownership and relationships. A new immutable version obeys creation-time key
policy; an existing immutable version is not retrospectively recomposed. Key uniqueness evidence
states exactly that the accepted Commit introduced no conflicting locally visible claim.

The manifest-selected corpus has zero findings in the native key/source gate and report-only
validator. `Length16k` is restored exactly as detached, while tighter fixtures prove independent
scalar rejection within PVL limits. Canonical Core bootstrap remains accepted. Report native and
WASM checks, focused unit/conformance checks, and public-Commit/Sweettest evidence separately,
including any environment-dependent check that could not run.

---

# Capability 4 — Relationship Conformance

## Outcome

Descriptor-aware relationship declarations and occurrences validate through the shared validator.
Rules requiring a transaction or graph view run only when that view is supplied.

## Scope

- Implement `DS-REL-*` inverse pairing, mirrored effective endpoints, and directional deletion
  semantic declarations. Apply the delivered relationship checks to descriptor holons as well as
  ordinary instances, completing the endpoint/collection/relationship-constraint policy portion of
  `DS-CONTRACT-003` deferred by C2.
- Implement `DS-OCC-*` occurrence grouping by resolved descriptor identity, endpoint
  compatibility, ordering/duplicate policy, and rejection of unbound independently authored
  relationships.
- Register `DS-CARD-001` as compatible only with contexts containing the required bounded Nursery
  or graph snapshot, and evaluate every effective applicable `CardinalityConstraint` rather than a
  legacy descriptor-property pair.
- Make Capability 4 the first and exclusive capability that evaluates relationship cardinality;
  its relationship conformance handler consumes effective cardinality constraints through the
  internal constraint evaluator.
- Reach, rather than restore, the canonical `CardinalityConstraint` occurrences. The VAL0 follow-up
  left all 158 attached because no earlier traversal could reach them, so this capability requires
  no corpus reattachment and no regeneration for cardinality. Extending the traversal to relationship
  subjects is itself the tightening event: it is the point at which the retained `ExactlyOne`
  commitments that `DescribedBy` and `ComponentOf` rely on begin to be evaluated, and at which
  existing pre-production holons become subject to cardinality conformance. Recount the attached
  cardinality occurrences before delivery and explain any drift from the VAL0 snapshot rather than
  silently absorbing it.
- Build prospective views only from authoritative Commit-local relationship buckets, as defined by
  the [Relationship Occurrence Persistence Design
  Specification](../transactions/relationship-persistence-design-spec.md). Prepare paired local
  declared/inverse deltas for persistence and cover source-chain conflict
  reload, revalidation, and bounded retry/failure.
- Add Commit's pre-write PVL preflight after assessment. Apply the existing PVL checks to the exact
  `HolonNodeModel` of every `ForCreate` / `ForUpdateNewVersion` candidate, including total node
  size, and to every prepared SmartLink tag. Refuse the whole Commit before its first write.
  PVL stays descriptor-independent, with unchanged rules, limits, precedence, and
  `HolonError::PvlViolation` contract. Project the refusal publicly without fabricating a `DS-*`
  finding or reporting a partial write. Storage keeps its defensive checks, and preflighted and
  persisted encodings must agree. The preflight does not imply rollback or conductor acceptance.
- Preserve Capability 3's version classification: adding or removing an occurrence of a
  definitional key-input relationship produces a new version whose key is checked.
- Route relationship-occurrence removal through the same prospective-bucket validation and
  persistence path as occurrence creation. Storage-level SmartLink deletion becomes an
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

### Extension-schema rule dispatch (design possibility)

*Not yet committed scope. Finalize while planning Capability 4's details after Capability 3 is
implemented.*

The [Validation Schema Design Spec](validation-schema-design-spec.md#extension-authoring) permits
extension-authored `ValidationRule` holons, provided Commit has a compatible static handler.
No capability delivers that path yet. `StaticRuleRegistry::lookup` resolves only keys accepted by
`CoreValidationRuleName::from_key`, so a bound extension rule always fails closed with
`UnsupportedValidationRule`, even when a handler could be compiled in.

The Theme schema illustrates the need. It declares `ThemeTokenAssignmentPairUniqueness`
(`THEME-001`), `ThemeTokenAssignmentDesignTokenType` (`THEME-002`), and
`ThemeCompleteDesignTokenCoverage` (`THEME-003`) as `HolonValidationRule` instances, with no
bindings or handlers. `THEME-003` compares the token set defined by the Theme's
`ForMetaDesignSystem` target with its assignment targets. It therefore needs the Commit-local
prospective relationship view this capability delivers, and scheduling of affected Themes when
only an assignment or its `ForDesignToken` target changes.

One possible approach:

- **Rule ownership.** An extension rule stays in the schema that owns the governed vocabulary
  and binds at that family's root, for example `Theme.HolonType`. It does not move into Core or
  the Validation extension, which cannot reference extension types without inverting schema
  dependencies.
- **Static composition.** Compose the Core registry with extension rule sets compiled into the
  guest. Each rule set owns its rule-name identities and handlers and resolves full canonical
  rule keys. Dispatch remains static; this is not the deferred dynamic-implementation
  mechanism. Extension handler crates must be WASM-safe and reachable from the hApp workspace.
- **Coverage.** Extend binding-coverage tests to every manifest-selected package, not only Core.
  Reject duplicate rule keys across composed rule sets, because rule keys are not yet
  schema-qualified.
- **Semantics.** A handler of this kind runs only with its required context. For `THEME-003`,
  that is the bounded prospective view, a defined policy for finding affected Themes, and a
  pinned MDS version: a Theme realizes the version its `ForMetaDesignSystem` link targets, so
  an MDS revision does not reassess existing Themes. Deliver `THEME-002` alongside it, since
  `PresentationValue`'s string type does not establish conformance to the `DesignTokenType`.

Questions to settle:

- Whether extension rule sets ship within this capability or as a dependent Theme conformance
  slice.
- Where composition occurs.
- How affected-aggregate scheduling generalizes beyond Schema and Theme.

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

- Capabilities 1, 2, and 3, including Capability 3's `ConstraintInstanceRule` key resolver.
- Descriptor Runtime Platform relationship products.
- DescriptorPackage construction extended with the relationship-descriptor and cardinality
  demand noted under Capability 3's DescriptorPackage preparation demand.
- Transaction or graph snapshot support for cardinality coverage.

## Exit demonstration

Public Commit assesses bounded relationship declarations and occurrences. A transaction-aware
fixture proves cardinality failure only when the required Commit-local prospective view is
supplied, rejects before any relationship write, and proves that multiple effective cardinality
constraints are conjunctive. An accepted fixture persists the prepared local relationship
directions. With the `ConstraintInstanceRule` resolver from Capability 3 and the
`CardinalityConstraint` handler registered, strict Core
bootstrap and the Core Sweettest fixture succeed without any legacy cardinality-property fallback.
A multi-cell aggregate fixture rejects with `RelationshipCoordinationRequired`; ordinary deferred
remote inverse realization does not make a completed local forward commitment provisional.
Multi-candidate worksets with a later PVL failure (a string within its grapheme bound but over the
byte ceiling, an oversized node, and an oversized SmartLink tag) write nothing.

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
  restored by Capability 3, reproducing exactly what was removed; and the retained
  `CardinalityConstraint` occurrences are now reached by the Capability 4 traversal. No attachment
  remains detached for want of an evaluator, and no attachment remains unreachable for want of a
  traversal. Array constraint types remain deferred: they have no evaluator, and any reached
  attachment fails closed with `UnsupportedConstraintType`;
- every authored `ValidationBindings` occurrence has a compatible registered handler and subject
  family, sits at the family root named by the binding-placement convention, and no occurrence is
  authored on bare `TypeDescriptor`;
- the seeded rule inventory, including `DS-KEY-006`, and the five VAL0 removals match canonical TDL
  and generated projections; seeded identities, active bindings, fixed checks, and implemented
  handlers are reported separately;
- the standalone corpus key and source-binding check runs as a CI gate over the manifest-selected
  corpus;
- deterministic node and SmartLink PVL failures stop public Commit before any write, and the
  response distinguishes that refusal from semantic rejection;
- the following extern/API inventory matches the current production coordinator exports recorded
  in `happ/coordinator-surface.toml`. It baselines against the surface reductions already delivered
  by [`map-holons` PR 623](https://github.com/memetic-activation-platform/map-holons/pull/623)
  and [`map-holons` issue 622](https://github.com/memetic-activation-platform/map-holons/issues/622)
  rather than assuming historical externs remain exposed:

  | Production export | Current call path | Milestone disposition |
  | --- | --- | --- |
  | `dance` | compatibility alias to `dance_adapter` | Supported; follows the `dance_adapter` disposition. |
  | `dance_adapter` | bind request, then `dispatch_dance`; Commit requests call `commit_dance` → `TransactionContext::commit` → `GuestHolonService::commit_internal` → `commit_functions::commit` | Supported; every create, update, and relationship-occurrence mutation dispatched here must use Commit. |
  | `holon_storage_persist` | `holon_storage_externs::holon_storage_persist` → `holon_storage::persist_holon` | Direct Commit bypass; internalize it or restrict it to the Commit persistence path before this milestone passes. |
  | `smartlink_put` | `smartlink_externs::smartlink_put` → `smartlink::put_smartlink` | Direct Commit bypass; internalize it or restrict it to Capability 4 Commit execution. |
  | `smartlink_delete` | `smartlink_externs::smartlink_delete` → `smartlink::delete_smartlink` | Direct Commit bypass; internalize it or restrict it to Capability 4 Commit execution. |
  | `delete_holon_node` | internal storage primitive reached through `dance_adapter` → `dispatch_dance` → `delete_holon_dance` → `MutationFacade::delete_holon` → `GuestHolonService::delete_holon_internal` → `delete_holon_node`; it authors Holochain's native Delete action for one structural head | No coordinator extern exposes this write. Native deletion retains MAP topology and historical ownership/index facts; active discovery interprets the visible Delete action. |
  | `holon_storage_get`, `holon_storage_get_many`, `smartlink_expand`, `smartlink_expand_all`, `smartlink_expand_by_key` | direct storage-read helpers | Supported and read-only; outside the mutation gate. |
  | `get_holon_node_by_path`, `get_original_holon_node`, `get_original_holon_node_with_details`, `get_all_deletes_for_holon_node`, `get_oldest_delete_for_holon_node` | direct legacy read helpers | `legacy_ingress` and read-only; outside the mutation gate. `get_all_holon_nodes` was retired with the `AllHolonNodes` index. |

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
  generalized guest Commit, while internal persistence and SmartLink operations are reachable only
  through that path;
- `LocalHolonSpace` bootstrap is documented and tested as the sole intended permanent exception;
- `delete_holon_node` remains explicitly inventoried as the current out-of-scope deletion surface,
  rather than being misclassified as an activation gap or assigned to an invented capability;
- Commit responses project `Rejected`, `RejectedHolons`, and the derived violation count while
  keeping rejection and operational failure distinct; abandonment remains visible only through
  staged state, and per-holon findings reach clients with the returned staged pool;
- complete-Nursery, affected-Schema, Commit-local relationship-bucket, and second-pass replacement
  tests pass, and conflict-retry coverage proves that `RelationshipCommitScope` governs a retry's
  Pass 2 as recorded, since Pass 1 does not re-run for an already committed holon: both scopes
  survive projection, bind, rebind, and committed-state restoration without broadening; an already
  committed graph-only retry with zero live validation candidates retains touched-only work; an
  interrupted version-producing retry retains `Full`, including the Commit-generated `Predecessor`
  edge; missing and invalid scope values are rejected in both Rust decoding and the SDK guards; and
  empty collections produce no descriptor-resolution or persistence work under either scope; and
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
| Descriptor-resolution handling, `DS-CONFORM-002`, required/undescribed properties, native kind | Capability 1 (VAL-C1a core; VAL-C1b Commit integration) | Supplied holon and descriptor/effective contract |
| `DS-STRUCT-*`, `DS-SCHEMA-*`, `DS-KIND-*`, `DS-CONTRACT-001/002/004`, `DS-CONSTRAINT-*` | Capability 2 | Resolved descriptor graph and kernel products |
| `DS-CONTRACT-003` | Capability 2 structural/declaration checks; completed through Capabilities 3 and 4 | Existing conformance checks plus the explicit C2–C4 enforcement boundary above; descriptor fields use shared value and relationship validators |
| Effective `InstanceKeyRule` resolution and `compose_key` | Capability 3 (VAL-C3c-2, Descriptor Runtime) | Completed holon state and descriptor-runtime products |
| Remaining `DS-CONFORM-*`, `DS-BIND-*`, `DS-PROP-*`, configured value constraints, `DS-ENUM-*`, `DS-DEFAULT-*`, `DS-KEY-001`–`005` | Capability 3 | Completed staged holon and `compose_key`; recorded saved source for `DS-ENUM-003` |
| `DS-KEY-006` key-introduction uniqueness | Capability 3 (VAL-C3f) | Local Space prospective lineage-head view; Commit only |
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
| Generic KeyRule resolution and key composition | Capability 3 (VAL-C3c-2) |
| Property/value/type-specific rule coverage | Capabilities 1 and 3 |
| Relationship validator and rule coverage | Capability 4 |
| Descriptor orchestration and production Commit integration | Capability 1 (VAL-C1a / VAL-C1b) |
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

From Capability 4, Commit runs the existing PVL node and SmartLink tag checks over its whole
publication workset before any write. PVL keeps ownership of those rules and
limits; storage retains its defensive checks.

# Critical Path

1. VAL-PRE: best-effort default population and dependency-safe outcome
   contracts.
2. VAL0 (landed): Core constraint/rule source vocabulary, TDL/JSON fidelity, and non-strict
   Validation-extension package-load acceptance. Its follow-up `Constraints` detachment and
   regeneration must land before Capability 1; its metadata and rule-inventory removals may
   proceed in parallel with the capabilities but must land before the final checklist.
3. Capability 1:
   - VAL-C1a: descriptor-aware validator core, active bindings, compatibility proof, and clean
     canonical-corpus conformance;
   - VAL-C1b: production Commit integration and observable rejection, completing the vertical slice.
4. Capability 2: descriptor and affected-Schema aggregate conformance.
5. Capability 3 (VAL-C3a–f, sequential): value, enum, default, and key conformance, including
   Descriptor Runtime key resolution (VAL-C3c-2) and keyless persistence (VAL-C3e).
6. Capability 4: Commit-local relationship conformance and the strict
   Core-bootstrap/Sweettest gate.
7. Final Coverage and Convergence Milestone: complete evaluator coverage over every reachable
   `Constraints` attachment, extern/API convergence, and the scoped public Commit claim.


### C2 prospective reference substrate — implementation traceability

The prospective reader and its diagnostic preparation are available before C2 activation. Public
Commit competition rejection activates with readiness orchestration; schema-dependent bindings and
new mandatory roots activate with the canonical schema. No binding-count change belongs to this
substrate phase. The active C1 path remains on the current reader.

| Concern | Focused regression coverage |
| --- | --- |
| Ordinary phase identity versus prospective replacement identity | `saved_lineage_recognizes_staged_replacement_root`; `nearest_anchor_wins_and_foreign_transaction_is_rejected` |
| Full ancestry, distinct creates, contested content | `selection_uses_full_ancestry_and_blocks_ambiguous_source_reads` |
| Selected parent content, cycles, kind anchors | `replacement_parent_content_governs_lineage_and_cycles` |
| Ownership, applicability, contribution provenance | `prospective_ownership_constraints_and_contributions_share_selection` |
| Graph-only competition, lifecycle exclusions, fresh attempt | `graph_only_competitors_block_reads_and_retry_excludes_finished_entries` |
| Operational read and foreign-reference failures | `prospective_reads_preserve_operational_errors_and_reject_foreign_mutable_refs` |
| One selection per visited lineage node | `lineage_selects_each_visited_reference_once` |
| Saved bindings and staged roots; split bootstrap | `split_saved_schema_and_staged_binding_roots_are_compatible` |
| Changed rule family and concrete constraint type | `binding_family_and_constraint_type_use_replacement_content` |
| Bounded findings, deterministic order, outcome replacement | `competition_diagnostics_are_deterministic_bounded_and_replaceable` |
| Typed schema incompatibility, present and saved new anchor | `missing_new_validation_anchor_is_a_deliberate_schema_incompatibility` |

The lifecycle test uses explicit saved/update snapshots; the public zero-write and cross-Commit
branch-persistence demonstrations remain acceptance work for activation and Commit integration.


## Assessment-scoped package preparation follow-up

Issue [map-holons #753](https://github.com/evomimic/map-holons/issues/753) delivers
the DescriptorPackage contract in the Commit validation design specification after C2.
Sequence: measure existing behavior; add complete requested-set cache preparation;
construct the assessment registry and effective products; schedule commitment groups;
consume prepared contracts for instance validation; verify and benchmark.

Preparation includes DescribedBy/Extends, effective members, ValueType, SourceType and
TargetType, Constraints and applicability, ValidationBindings and canonical anchors,
old/prospective ownership, affected Components/Rules, DependsOn, dynamically declared
schema relationships, and the universal descriptor contract. Keep demand separate from
readiness dependencies and preserve C2 coverage. Existing static dispatch is retained.

Regression coverage must assert zero schema-side backend relationship queries after
construction, with instance reads distinguished. Cover saved/staged bootstrap, competition,
corrected retry, malformed links, known-empty sets, mutual description, invalid cycles,
independent findings, operational errors, and zero writes on rejection. Compare repeated
import and commit-conflict runs, including sparse/high-fanout demand; report timing,
backend calls, link volume, and memory where feasible without a fixed numerical target.

Module runtime/acceptance, query migration, cross-assessment reuse, and C3/C4 activation
are deferred. Module architecture is coordinated in DevDocs #52.
