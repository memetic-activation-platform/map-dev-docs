# Pre-Step A — behavior-preserving characterization

Accounting lives on DevDocs `val-capability-3-working`, alongside the original baseline.
Production map-holons revision: `a3a280d1b59745038b63e9eb84f47b27b2193ff9` (10,000-entry
guest-cache checkpoint). This change adds tests and fixture-only counters, with no production
behavior change. Semantic baseline: `3d053ba8`; instrumentation-only baseline: `95b99663`.
Reviewed decision: DevDocs PR #80 merged `e23c4dd` (approved `1d9865d`). The historical raw
inventory uses `0c033b6b`, not the current cache capacity; its artifact and source hashes remain
in both inventory JSON files. No inventory timings are used as measurements.

## Artifacts and production method

- [read-inventory.md](read-inventory.md): source/call-site inspection of the common assessment
  pipeline, including transitive descriptor-kernel calls, requested-empty memberships, retained
  content, evidence and remaining derivations. Accounts for subject and contextual reads separately.
- [removal-ledger.md](removal-ledger.md): executed exact-source fault controls and blocking controls.
  Final request omissions/decisions remain explicitly pending Step A/C; this phase changes no policy.
- [result-dependency-audit.md](result-dependency-audit.md): source/caller audit of acceptance versus
  interpretation/configuration channels. No new overall check-result prerequisite or incorrect
  consumer/input-matrix **Source today** classification was found, so no decision PR is needed.
- [name-index-link-reads.json](../diagnostics/name-index-link-reads.json): exact `(source, relationship)`
  membership misses inside NameIndexes; same retained raw logs and operation-boundary extraction as
  [name-index-inventory.json](../diagnostics/name-index-inventory.json). No additional guest capture.
- [fixture-membership-reads.json](fixture-membership-reads.json): stable fixture semantic source keys
  mapped from exact saved HolonIds; assessment-only backend membership attempts per candidate mode, excluding
  setup/staging reads. This does not substitute for guest performance observations or logical demand.

The NameIndexes misses are **SourceOf (26–27) and SourceType (49–50)**, 75–77 total per sample.
AffordsDance/AffordsCommand/InstanceKeyRule collections are read earlier in complete-product
construction. Required navigation memberships and member content must be prepared/retained in
Step C; increasing cache capacity is not proof that preparation is complete.

The raw logs are git-ignored and kept locally at `../diagnostics/name-index-raw/`.
The generator can only be rerun where those logs were kept; SHA-256 verification is
mandatory. Missing logs are an unavailable observation, never a measured zero.

The two ignored evidence tests are temporary: run them explicitly now and after Step C.
In the final verification step, delete them and `backend_membership_inventory` when the
generic zero-query test replaces them; keep the `reads_by_source` counter. Step A updates
kept scenario tests in place, changing assertions without renaming them. Add a test only
for behavior not covered by an existing test.

From map-dev-docs, reproduce the tracked JSON:

```sh
python3 docs/core/performance/evidence/2026-10-30-issue-822/characterization/generate-name-index-link-reads.py \
  docs/core/performance/evidence/2026-10-30-issue-822/diagnostics/name-index-raw
```

From map-holons, collect fixture observations (use any local log destination):

```sh
cargo test --manifest-path shared_crates/holons_validation/Cargo.toml \
  preparation_characterization -- --ignored --nocapture > /tmp/822-fixture-reads.log 2>&1
```

Then from map-dev-docs:

```sh
python3 docs/core/performance/evidence/2026-10-30-issue-822/characterization/generate-fixture-membership-reads.py \
  /tmp/822-fixture-reads.log
```

## Characterization scenarios

Tests reside in map-holons `shared_crates/holons_validation/src/`. New baseline controls are in
`preparation_characterization_tests.rs`, included by `subject_assessment_tests.rs`; the unused
constraint/rule control extends `constraint_declarations_tests.rs`. Existing controls below were
retained and rerun, not rewritten as new tests.

| Scenario | Test name | Baseline expectation / future contrast |
| --- | --- | --- |
| Owning Schema cycle | `unstaged_schema_cycle_reaches_the_carrier_and_blocks_its_staged_component` | One exact-owner DS-SCHEMA-001; dependent Component blocked today |
| Saved predecessor beside invalid successor | `saved_book_keeps_title_v1_while_explicit_book_v2_depends_on_invalid_title_v2` | Saved consumer validates in both orders; only explicit successor reference blocked |
| Unrelated referenced ownership defect | `unrelated_staged_ownership_defect_beside_its_consumer` | Only SchemaOwnership on descriptor; dependent blocked in both orders |
| Unusable governing lineage | `malformed_governing_lineage_with_multiple_consumers` | Two-parent saved governor rejects; explaining finding on each consumer in both orders. Fixture bypasses attachment-time default preparation to reach Commit |
| Unusable value selection plus bad sibling value | `unusable_property_selection_beside_invalid_sibling_value` | Candidate blocked; no sibling BaseValueKindMismatch; one saved-governor aggregate. Usable control proves sibling and requiredness checks would fire |
| Required absence (same subject as bad sibling) | `unusable_property_selection_beside_invalid_sibling_value` | Requiredness finding suppressed by broad blocking today |
| Mutual description, later peer failure | `mutual_description_with_later_peer_failure` | Both peer products independently proven usable. B lacks required Title; A gets post-hoc blocker when first, prospective blocker when reversed; exactly two findings |
| Saved supporting contract defects | `unusable_property_selection_beside_invalid_sibling_value` | One generic aggregate, without expanded detailed DS-CONTRACT diagnostics; Step A keeps aggregate but scopes guards |
| Malformed candidate lineage | `malformed_candidate_lineages` | Self-cycle asserts DS-STRUCT-003; two parents assert DS-STRUCT-002, both with candidate Invalid outcome |
| Required backend failure | `encountered_required_definition_read_error_preserves_prior_outcomes`; `required_binding_role_read_errors_are_preserved_without_retrying_backend_reads` | Operational error preserves prior outcomes; required errors stay required |
| Contextual key failure plus dependent | `descriptor_key_failure_blocks_only_explicit_new_definition_consumers` | Exact staged-definition dependent blocked today; saved-reference independence retained |
| Unused staged constraints/rules | `unused_staged_constraint_and_rule_keep_independent_declaration_coverage` | Negative Minimum diagnosed DS-CONSTRAINT-003 without attachment; unattached rule retains ownership check; both orders |
| Shared immutable products, separate outcomes | `shared_definition_product_findings_reach_both_no_op_and_graph_only_candidates`; `no_op_and_graph_only_siblings_are_both_assessed_without_poisoning_saved_definition` | Findings fan out per candidate, candidate-only failure does not poison saved identity |
| Complete assessment lifecycle | `report_only_commit_assessment_preserves_outcomes_and_matches_validation`; `subject_gate_assessment_error_installs_no_partial_outcomes` | Report-only nonmutation and atomic outcome installation |
| Exact incidental reads and retained required read | `broad_preparation_incidental_empty_reads_abort_and_preserve_outcomes` | Three incidental empty pairs and required PropertyType DescribedBy each reach backend; injected errors abort both paths, preserving Validated outcome |
| Five candidate modes | `exact_empty_membership_reads_cover_each_candidate_mode` | Exact saved ValueType RuleOf read in instance, edited definition, mixed, no-op and graph-only assessments; records every saved-source membership attempt |

## Verification

- `cargo test --manifest-path shared_crates/holons_validation/Cargo.toml`: 141 passed, 2 temporary evidence tests ignored; both pass when run explicitly with `--ignored`.
- `npm run fmt:check`: passed (host, hApp and Sweettest formatting).
- `cargo test --manifest-path shared_crates/holons_validation/Cargo.toml preparation_characterization -- --ignored --nocapture`: both temporary evidence tests passed; assessment-only inventory regenerated.
- Both JSON generators ran against retained logs; NameIndexes source hashes match the historical inventory.
- `npm run check -w map-happ`: passed. No new guest capture or Sweettest run.
  The implementation plan's Step A/D integration gates remain required when
  behavior changes. No tests in `tests/sweetests/` were edited.

The scripts are retained beside their generated evidence. The shared fixture has only test-time
source counters; no runtime instrumentation, cache policy or production descriptor preparation was
changed. The implementation plan and reorganization proposal are untouched.
