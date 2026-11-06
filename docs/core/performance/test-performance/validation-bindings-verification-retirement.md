# Retiring the bespoke ValidationBindings inventory verification

## Decision and scope

On 2026-11-06, remove the `VerifyValidationBindingsDescriptorContract` dance step
from `bootstrap_operational_schema`, together with its adder, variant, runner arm,
and executor. The change does not alter schema declarations or Commit validation.

The step duplicated a fixed inventory of 24 local bindings on nine owners in Rust.
It asserted their persisted forward and inverse collections, two empty collections,
and an aggregate absence check over every loaded holon. Its descriptor-pair checks
also repeated the authored names, endpoints, and inverse pairing.

The user explicitly chose declarative semantic enforcement and reuse of existing
fixture/verification mechanisms over maintaining this separate inventory oracle.
No new batched inventory step replaces it. This intentionally retires the literal
inventory assertions; it does not claim every assertion has an identical replacement.

The profile in [ValidationBindings and inverse-traversal cost](validation-bindings-profile.md)
measured 472.621 seconds for this step, including 452.695 seconds for the exhaustive
scan. These are historical measurements of the removed work, not a measured speedup
of the changed suite. The diagnostic batching control remains historical evidence.

## Coverage and responsibility audit

Paths below are relative to the sibling map-holons repository.

| Removed assertion | Existing mechanism or evidence | Coverage boundary |
| --- | --- | --- |
| Literal forward/inverse descriptor names and endpoints | Core TDL in `schema-src/core/validation.tdl` declares the pair. Generic compiler relationship tests in `tools/map-schema/src/tdl_compiler.rs` exercise endpoint and inverse emission; the remaining core descriptor executor exercises relationship access on representative pairs. | No replacement hard-coded ValidationBindings pair snapshot is introduced. Exact schema vocabulary is no longer independently asserted by this dance step. |
| Persisted forward collections | `add_match_saved_content_step` compares fixture-owned properties and definitional content with the expected transient graph. `add_verify_persisted_graph_step` can assert exact named target collections. | These are reusable capabilities, not a claim that bootstrap currently constructs a complete expected fixture graph for all 24 bindings. |
| Persisted inverse collections and multiplicity | `add_verify_persisted_graph_step` supports separately declared inverse collections. `commit_lineage_fixture.rs` exercises forward/inverse replay; `commit_incomplete_fixture.rs` verifies exact fresh forward/inverse collections after retry. | Generic SmartLink behavior remains covered. No separate inventory of the 24 binding inverses is retained in the dance suite. |
| Inherited rule applicability and rejection behavior | `commit_validation_fixture.rs` rejects a missing required Title, verifies the rule finding, corrects the subject and commits. `commit_strict_contract_fixture.rs` checks undescribed property/relationship rejection. `commit_key_uniqueness_fixture.rs` checks historical key claims. | Behavioral fixtures exercise enforcement instead of counting schema edges. They are not a complete behavioral audit of every rule. |
| Effective binding derivation and dispatch | `shared_crates/holons_core/src/descriptors/inheritance.rs` checks inherited contributions and declaring origins. `shared_crates/holons_validation/src/subject_assessment_tests.rs` covers required properties, bytes kind mismatch, incompatible/unsupported bindings, and prerequisite behavior; `schema_assessment_tests.rs` covers schema dependency cycles. | These check descriptor and validation machinery; they do not impose a closed global binding inventory. |
| Exactly 24 occurrences and no other source populated | Removed without replacement. | No independent requirement for a globally closed inventory was established. Valid schema extensions should be governed by declarative contracts rather than this count. |

## Explicit enforcement gaps and remaining procedural checks

1. **Required binding retention is not established declaratively.** The authored
   `ValidationBindings` relationship has `ZeroOrMore.CardinalityConstraint`. No
   declarative requirement enforcing the exact 24 placements was located in this
   audit. Compatibility checking of a binding that is present does not establish
   that an omitted binding is required. This is a capability/coverage gap to resolve
   through the validation and constraint design, not a justification for restoring
   the inventory scan. A specific binding-removal Commit was not executed here;
   this note does not claim such a Commit has been demonstrated to succeed.
2. **Generic prerequisites are a distinct mechanism.**
   `descriptor_rules.rs::emit_prerequisites` deliberately reports universal
   prerequisites even when a describer cannot inherit their bindings. The test
   `prerequisite_products_remain_reported_without_compatible_bindings` covers that
   behavior. This is not evidence of a general declarative binding-retention rule.
3. **Other procedural inventory assertions still exist.**
   `tools/map-schema/tests/validation_binding_inventory.rs` contains a handwritten
   canonical placement/family inventory and mutation checks; it also contains
   independent ownership/dependency tests. The validation crate has
   `registrations_match_independent_core_placement_expectations`. They are not
   changed by this bounded dance-step removal and should be reviewed separately
   against the same declarative-enforcement principle. Their continued presence
   must not be described as having solved the language gap.

Issue 853 registry retention is separate work. This removal neither implements its
lifecycle contract nor establishes its performance or correctness.

## Validation

Focused checks passed on the working tree containing the concurrent Issue 853 work:

- `nix develop --command npm run test:unit:sweetests`: 56 harness unit tests and
  four fixture-authoring tests passed, including authoring every registered fixture.
- `nix develop --command cargo test --manifest-path tests/sweetests/Cargo.toml
  --test dance_tests --no-run`: the modified runner and executor compiled.
- `nix develop --command npm run fmt:sweetests:check`: passed.
- Scoped `git diff --check`: passed; no remaining references to the removed step
  were found under `tests/sweetests`.

The post-removal `pristine_bootstrap_and_loader` conductor test passed at
map-holons checkpoint `b6f2cd23`: one test passed, zero failed, 14 filtered out,
201.18 seconds including bootstrap and both fixtures. Command:

```sh
nix develop --command bash scripts/test-run.sh cargo test \
  --manifest-path tests/sweetests/Cargo.toml --test dance_tests \
  pristine_bootstrap_and_loader -- --exact --nocapture
```

Local result log: `/private/tmp/map-852-checkpoint-pristine.log`; retained wrapper
log: `/Users/stevemelville/.cache/map-holons/test-runs/run-SueGAHnf/test.log`.
This used existing built production artifacts verified during the Issue 853
checkpoint. It is a focused correctness run with ordinary warning-level logging,
not a matched repetition of the earlier timestamp-profile capture. No full npm
test was run for the removal. Issue 853's separate evidence is recorded in the
Descriptor Implementation Plan.
