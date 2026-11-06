# Read and blocking removal ledger — baseline side

Production source revision `a3a280d1`. This records observations before Step A/C; no requests or
blockers have been removed. Final omissions, outcomes and work-count deltas must be filled after
the corresponding implementation. Tests live in `holons_validation/src/` in map-holons.

## Exact incidental membership controls

`preparation_characterization::broad_preparation_incidental_empty_reads_abort_and_preserve_outcomes`
uses a fresh saved fixture per row, explicitly requests a Fresh read policy for that exact pair,
first proves successful assessment and a positive backend counter, then injects a distinct
`InvalidState` at that pair. Both report-only and outcome-installing entrypoints return that same
error; the previously Validated candidate and its empty findings remain intact. Unexpected writes
panic in FixtureStorage. These are empty sets; no malformed-link policy is changed.

| Baseline input / executed call | Injected failure and baseline result | Final consumer justification / omitted request (Steps A/C) | Final decision and regression evidence |
| --- | --- | --- | --- |
| Saved Contract → `ValueType`; package common-edge membership preparation/traversal | Exact pair counter > 0; injected backend error aborts both paths | No consumer needs Contract ValueType; governing payload does not include it | Omitted; `omitted_memberships_do_not_fail_assessment_but_required_reads_do` accepts in both entrypoints with the exact fault armed |
| Saved StringValueType.ValueType → `InstanceProperties`; package common-edge membership preparation/traversal | Exact pair counter > 0; injected backend error aborts both paths | Retained: the complete `effective_schema()` projection acquired through ValueDescriptor still reads InstanceProperties | Required operational failure retained by the paired control; no removal claim |
| Saved StringValueType.ValueType → `RuleOf`; package common-edge membership preparation/traversal | Exact pair counter > 0; injected backend error aborts both paths | Value conformance and binding execution do not consume Schema ownership | Omitted; the same exact-source fault control accepts in both entrypoints |

These three incidental rows are a sample, not the full removal set. The full set is the
before/after difference of `fixture-membership-reads.json` across Step C; retain injected
fault controls only for these sample rows.

These concrete controls represent unjustified category-wide preparation, not permission to drop a
relationship globally. `exact_empty_membership_reads_cover_each_candidate_mode` proves the third
pair executes for instance, definition, mixed, no-op and graph-only input sets. Its graph-only mode
marks an empty delta; populated-delta semantics remain covered by existing graph-only tests.
The fixture counters record `(HolonId, RelationshipName)` including failed/empty attempts; the
control asserts the exact source, not just an aggregate relationship count. No-op/graph-only source
identities remain saved; definition and mixed cases reject their independent definition defects.

**Paired required read:** Title.PropertyType → `DescribedBy` uses the same fault test and preserves
the operational error. It remains necessary for the governing requiredness default even where the
fixture's explicit local flag supplies the immediate requiredness result. Do not delete this demand
as an incidental edge. Existing `encountered_required_definition_read_error_preserves_prior_outcomes`
and `required_binding_role_read_errors_are_preserved_without_retrying_backend_reads` add content
and role-read controls.

## Traversal and derivation retirement accounting

| Baseline operation and execution evidence | Failure / blocking behavior today | Final justification / replacement | Final decision and evidence |
| --- | --- | --- | --- |
| Nine-edge readiness discovery, `commitment_order`; `profiling_observes_preparation_without_changing_the_validation_report` counts Readiness edges | Any required walk error is operational. Not independently fault-isolated from the identical package prefetch | Pending Step A; memberships needed by retained consumers remain | Pending |
| Repeated lineage diagnosis in contract/declaration assessment; independent `ConstraintContributions::resolve`, `UniversalDescriptorContract::from_meta_type` | Required errors stay operational; reuse must not suppress them | Pending Step A shared prepared contributions/diagnosis | Pending |
| NameIndexes `SourceOf`/`SourceType` misses (75–77); generated exact-source JSON | These are required navigation inputs today; no incidental-read deletion claim | Pending Step C acquisition/retention boundary | Pending |
| `authored_targets` Smart branch; only caller passes staged SubjectPreparation.subject | Unreachable from production Commit; no executed failure to inject at that boundary | Pending Step A dead-path deletion; staged enumeration retained | Pending; **no current latency reduction claim** |
| Complete payload construction on every package-reached definition | Broad product work proven by captured 127 definitions / 407 indexes in repeated usage; no independent per-field fault characterization | Pending Step C; acquisition remains complete per selected category | Pending |

## Approved blocking changes characterized before editing expectations

| Baseline blocker / test | Observed attribution and suppressed checks | Final accounting |
| --- | --- | --- |
| Owner Schema cycle: `owning_schema_cycle_and_staged_component_are_assessed_independently` | DS-SCHEMA-001 aggregate on exact owner; Component receives UnresolvedLocalDependency | Pending Step A; Component must continue |
| `unrelated_staged_ownership_defect_beside_its_consumer` | SchemaOwnership on referenced staged descriptor, generic dependent blocker in either input order | Pending Step A; usable consumers continue |
| `unusable_property_selection_beside_invalid_sibling_value` | One saved-governor aggregate; candidate blocked; sibling Key kind mismatch absent | Pending Step A scoped member guard |
| `unusable_property_selection_beside_invalid_sibling_value` | Candidate blocked; required Title absence check absent | Pending Step A; requiredness continues independently |
| `malformed_governing_lineage_with_multiple_consumers` | Saved governor with two parents rejects with an explaining UnresolvedLocalDependency on each candidate in either order | Pending structural diagnosis/guards; distinguish diagnosed authored defect from required backend failure |
| `mutual_description_with_later_peer_failure` | Both peer products are usable; B lacks required Title. A gets post-hoc blocker when assessed first, prospective-commitment blocker in reverse order | Pending Step A; B rejects independently, A stays unblocked |
| `saved_predecessor_and_staged_successor_consumers_are_assessed_independently` | Saved predecessor consumer validates; explicit successor consumer blocked; stable under reversed candidates | Pending scoped guards; exact predecessor behavior preserved |
| `descriptor_key_failure_blocks_only_explicit_new_definition_consumers` | DS-KEY-006 remains on claimant; dependent blocker only for exact staged definition | Pending scoped guards; contextual evidence retained |

No broad blocking rule is inferred to be intended merely because it passes these tests. The
reviewed interpretation-guard inventory governs replacements. Broader combinations and exact
post-change diagnostics must be verified in Step A/D, without weakening operational error controls.

## Step A implementation reconciliation

See [Step A implementation and checkpoint status](../step-a-checkpoint/README.md).
The scheduler walk/grouping, reverse propagation, package acceptance gate and post-hoc blockers
are removed. Required memberships in the broad package closure remain, so no sampled incidental
membership-fault control is retired yet. The complete before/after membership removal set stays
Step C work. The dead saved-subject authored_targets path is removed without a latency claim.

The kept tests now assert continued independent checks for ownership, Schema cycles, DS-KEY-006,
invalid staged successors and mutual peers. The unusable-property control now observes the required
absence and independent Key kind mismatch alongside a scoped ValueType explanation. Saved
supporting contracts retain the single aggregate. Malformed governing lineages explain each
consumer; required operational errors preserve outcomes. Staged defects lacking compatible bound
handlers get local incomplete-assessment explanations instead of the scheduler's acceptance
fallback. No overall check-result dependency was found or added to the reviewed inventory.

The later [user-run matched checkpoint](../step-a-checkpoint/analysis.md) verifies unchanged package
counts and removed readiness observations. Preparation is slower and backend/node counts are
unchanged; there is no claimed latency improvement. The initial sandbox failure is preserved
separately and no longer describes the current checkpoint's availability.

Graph-only target-binding interpretation now also checks name ambiguity before first-match lookup.
Conflicting relationship identities or unnamed declarations fail closed and explain live overlap
participants; the saved relationship population is not read. Its regression covers both candidate
orders. Invalid TargetBinding operational/error behavior remains covered by the existing control.

## Step C preparation reconciliation

See [Step C implementation](../step-c-implementation.md) for demand seeds, instrumentation scope,
retained payload costs, regression coverage, and pending guest evidence. The two ignored baseline
evidence tests remain unchanged until Phase 10; their baseline-positive assertions intentionally do
not describe the narrowed implementation. The active omitted-membership control supersedes their
sampled fault assertions for Step C.

| Remaining baseline operation | Final omitted request and resulting decision |
| --- | --- |
| Complete products for ordinary staged subjects, Schema owners/dependencies, constraints, rule instances/families and endpoint types | No product from discovery alone. Retain content/identity/diagnosis or explicitly required memberships for the named consumer. Full payloads are acquired only for product demands. |
| Common-edge ValueType on arbitrary definitions; ComponentOf/RuleOf on every reached definition | Omitted. Local property selection and bounded ownership worksets retain their own demand. Removing these speculative faults can permit an otherwise valid Commit to succeed. |
| Unknown binding DescribedBy and family graphs | Omitted for execution; dispatch key rejects before family reads. Staged subjects still receive their independent declaration/conformance assessment. Existing unknown-binding fault tests cover this. |
| Navigation SourceOf/SourceType misses | Retained and prefetched for HolonType navigation consumers, including saved governors. NameIndexes are skipped for PropertyType/ValueType. |
| Property inherited IsValueRequired and legacy IsRequired | Omitted. Local IsValueRequired or exact governing meta-type default determines requiredness; local ValueType selection is independent. Concrete-declaration regression covers both. |
| Repeated role walk for binding placement | Omitted. Shared diagnosed role evidence supplies placement, including encountered roles on rootless supporting definitions. |
| Subject-phase kind acquisition, schema construction/restoration and structural diagnosis | Omitted. Native kinds and interpretation facts are prepared; sealed diagnoses reject missing demand. The existing post-construction controls assert no derivation and no backend reads. |

Complete payload collection reads on demanded descriptors remain required even when a particular
validation check does not use that field. Their faults are not incidental removals. Endpoint and
constraint identities remain ordinary bound references; required content failures are still errors.
