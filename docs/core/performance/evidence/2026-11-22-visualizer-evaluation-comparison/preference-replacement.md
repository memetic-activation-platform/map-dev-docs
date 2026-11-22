# Separate finding: saved preference replacement retains the previous target

The finding 3 registry work exposed an existing persistence defect. This record tracks persistence separately from retained evaluation. No persistence fix is included in this change.

## Reproduction and observed result

1. Load the existing Visualizer preference fixture and establish an Inspector/PropertyMap choice.
2. Publish a successor of `PreferenceTestPreferred.ValueVisualizer`.
3. Use `dahn::preferences::remember` to replace an existing Slot preference with that successor, then Commit.
4. Explicitly reconsider that composition.

The Commit reports `Complete`, but selection reports two members of the required-singular `PreferredVisualizer` relationship. Both the original Slot and a different existing Slot reproduced the problem in diagnostic runs 3 and 4. Ordinary registry acquisition continued to return its previously captured exact choice. The error surfaced when an explicit new evaluation read the updated preference.

The preserved helper is [preference-replacement-reproducer.rs.txt](preference-replacement-reproducer.rs.txt). It belongs in `tests/sweetests/tests/runtime_checks/owner_directed_composition.rs`, after the existing fixture setup. Its corresponding call in `owner_directed_composition_acceptance` reproduces the failure. The failed-adoption source manifest records the tested working-tree file hashes; raw diagnostic logs remain under `/private/tmp/map-holons-finding3-implementation/run-3.log` and `run-4.log`.

## Relevant code

These paths are in the sibling `map-holons` checkout:

- `shared_crates/holons_core/src/dahn/preferences.rs:240`: replacement removes previous staged targets and adds the requested target.
- `shared_crates/holons_core/src/reference_layer/staged_reference.rs:526`: relationship mutation classification follows `IsDefinitional`.
- `schema-src/core/property-types.tdl:108`: `IsDefinitional` defaults to false; the preference relationship does not override it.
- `happ/crates/holons_guest/src/guest_shared_objects/commit_functions.rs:996`: graph-only updates reuse the existing saved source identity.
- `happ/crates/holons_guest/src/guest_shared_objects/commit_functions.rs:745`: an emptied staged collection creates no relationship persistence work.
- `happ/crates/holons_guest/src/guest_shared_objects/commit_functions.rs:1049`: relationship persistence saves remaining members; this path does not apply removed-target deltas to stored links.

A follow-up should apply explicit removal deltas through the existing Reference Layer and persistence boundary, covering forward/inverse memberships, key indexes and retry idempotency. It should preserve metadata-driven versioning and required-singular validation. This finding does not change the [registry decision model](../../../hx/dahn-design-spec.md#1454-runtime-index-and-preparation-validity) or authorize automatic reevaluation.
