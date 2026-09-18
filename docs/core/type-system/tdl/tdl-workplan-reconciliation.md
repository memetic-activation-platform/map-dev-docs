# TDL Workplan Reconciliation

This note reconciles the archived TDL authoring-toolchain workplan with
[`tdl-impl-plan-v2.md`](tdl-impl-plan-v2.md) before updating external development tracking.
It is a tracking bridge, not a normative schema or TDL specification.

## Reconciled release goal

The active implementation goal is Schema 2.0 conformance across TDL, MAP JSON, Holon Loading,
runtime descriptor services, and validation.

The archived plan's Airtable-replacement goal remains valuable, but it is no longer the controlling
near-term release shape. The old plan assumed that the main blocker was moving schema authoring from
Airtable-generated JSON into Git-authored TDL, with source tooling, Rust generation, and IDE support
as the main delivery path. The current plan starts from an already authoritative Schema 2.0 TDL
corpus and treats the main blocker as the ripple effect of the Schema 2.0 representation and
semantic model:

- TDL and MAP JSON lower to the same schema-backed `LoaderRefRep` holon graph.
- Holon Loading resolves `LoaderRefRep` into staged holons.
- Loader-owned default materialization happens after reference resolution and before commit.
- Commit invokes the shared Holon Validator.
- Runtime descriptor semantics live behind `HolonDescriptor` and typed descriptor wrappers.
- The separate `SemanticModel` and tool-local `loader_ir` are retired rather than extended.

## What changed

| Concern | Archived plan | Active v2 plan | Reconciliation |
| --- | --- | --- | --- |
| Release driver | Replace Airtable as the ordinary schema source of truth | Bring the toolchain and runtime into conformance with Schema 2.0 | Track Schema 2.0 conformance first; keep Airtable retirement as downstream documentation/process work |
| Source of truth | Establish `schema-src/**/*.tdl` from JSON | Start from the current Schema 2.0 TDL corpus | Baseline decompile is no longer the first release gate; corpus acceptance is |
| Semantic middle | Shared semantic model and symbol table | Existing holonic `LoaderRefRep` graph, then Holons Core staged/saved graph | Do not track a new mutable semantic model as active work |
| Validation | Host-side TDL semantic validation before JSON generation | Runtime Holon Validator delegates to `HolonDescriptor`; host tooling performs syntax/lowering/fidelity checks | Move rich descriptor semantics to R1-R5; host checks remain source-bound |
| Defaults | Tooling detects obvious default assumptions | Loader materializes descriptor defaults before validated commit | Track default work under R3 and R5, not compiler validation |
| Code generation | Rust enums and typed wrappers are Milestone A unblockers | Codegen is a derived consumer after stable graph/descriptor boundaries | Retain as R9/downstream work, not as a Schema 2.0 conformance prerequisite |
| IDE/LSP | Milestone C language-aware authoring experience | Initial non-goal for the first implementation sequence | Preserve as future derived tooling after R6-R8/R9 |
| CI | Validate TDL, generated JSON, generated Rust, wrappers, suite import | Acceptance tests over parser, LoaderRefRep fidelity, loader acceptance, validation, and commit behavior | Track v2 CI around conformance and round-trip invariants first; generated-artifact freshness can follow |

## Mapping from archived phases

| Archived item | Active disposition |
| --- | --- |
| Phase 0: JSON to TDL baseline decompiler | Partially retained in R7. The old one-time baseline generation goal is superseded; decompile now proves MAP JSON and TDL preserve equivalent `LoaderRefRep` graphs. |
| Phase 1: TDL to JSON compiler | Retained in R6, but rebuilt over `LoaderRefRep` and TDL v0.9/v0.10 syntax rather than `SemanticModel` plus `loader_ir`. |
| Phase 2: Shared semantic model and symbol table | Superseded as architecture. Any lookup tables must be derived support indexes over `LoaderRefRep` or saved holons and must not own mutable semantic state. |
| Phase 3a/3b: Basic and expanded semantic validation | Split. Syntax and lowering diagnostics remain with source tooling in R6-R7; descriptor semantics move to `HolonDescriptor` and the Holon Validator in R1-R5. |
| Phase 4: Semantic diff | Retained as downstream tooling based on immutable `LoaderRefRep` comparison signatures after R7. |
| Phase 5: CI integration | Retained, but near-term checks should follow v2 completion criteria: corpus parse, JSON rendering, loader acceptance, validation, and round-trip fidelity. Generated Rust freshness is downstream. |
| Phase 6: Rust enum/name generation | Deferred to R9 as a derived consumer. Any retained category projections derive from graph-defined Instance TypeKind anchors. |
| Phase 7a/7b: Typed HolonReference and wrapper generation | Deferred to R9. Wrapper admissibility and typed surfaces must consume `HolonDescriptor`/resolved graph identity instead of authored `TypeKind` state. |
| Phase 8: Local developer workflow | Retained as process work after R6-R8 make source conversion reliable; not a blocker for R1-R5 runtime conformance. |
| Phase 9.1-9.8: LSP, editor support, workspace intelligence, refactoring | Deferred. These are derived authoring aids and must not create another semantic authority. |
| Phase 10a/10b: Documentation, migration policy, Airtable deprecation | Retained as downstream contributor/process work once the active schema-authoring path is stable. |

## Tracking-sheet update basis

Use the active v2 plan as the source for near-term `Waves Progress` rows:

| Wave | Track | PR key | Description | Dependency posture |
| --- | --- | --- | --- | --- |
| R0 | TDL / Schema 2.0 baseline | R0 | Establish executable red baseline, corpus guards, implementation inventories, and branch-578 reusable-test inventory | Starts first |
| R1 | Runtime descriptor kernel | R1 | Align `HolonDescriptor` and typed wrappers with Schema 2.0 effective semantics | After R0 baseline fixtures exist |
| R2 | Validation | R2 | Integrate `HolonDescriptor` with the shared Holon Validator and keep PVL separation | After enough R1 surface exists |
| R3 | Loader defaults | R3 | Implement loader-specific descriptor-default materialization over staged references | After enough R1 effective contract access exists |
| R4 | Validation | R4 | Complete descriptor-driven Holon Validation for Schema 2.0, including dependency DAG and conformance rules | Depends on R1-R3 surfaces |
| R5 | Loader integration | R5 | Insert materialization and validated commit into Holon Loading | Depends on R2-R4 |
| R6 | TDL tooling | R6 | Rebuild TDL parsing/lowering and JSON rendering over `LoaderRefRep` | Can proceed in parallel after R0 |
| R7 | Source fidelity | R7 | Rebuild JSON decompile and round-trip fidelity over `LoaderRefRep` | Depends on R6 graph output |
| R8 | Tooling cleanup | R8 | Retire `SemanticModel`, tool-local `loader_ir`, obsolete adapters, and legacy category surfaces | Depends on R6-R7 migration of consumers |
| R9 | Derived consumers | R9 | Reintroduce codegen, wrappers, diff, CI polish, local workflow, and LSP as consumers of stable graph/runtime boundaries | Downstream of stable R1-R8 boundaries |

When updating the sheet, existing completed rows should remain historical ledger entries. Non-done
rows from the archived Airtable/LSP plan should be reconciled as follows:

- Rows about compiler/decompiler round-trip work should be renamed or mapped to R6/R7.
- Rows about semantic model, symbol table, or `loader_ir` expansion should be closed, superseded,
  or rewritten as `LoaderRefRep`-derived support-index work.
- Rows about rich semantic validation should move to R1-R5 unless they are strictly source syntax
  or lowering diagnostics.
- Rows about generated Rust enums, wrappers, semantic diff, CI generated-artifact checks, local
  authoring workflow, and LSP should move to R9/downstream status rather than near-term Schema 2.0
  conformance.
- Rows whose only purpose was replacing Airtable as a source of truth should become documentation
  or process cleanup, because the active docs now treat the TDL corpus as authoritative.

## Near-term sheet intent

The next sheet sync should make the release plan read as one coherent Schema 2.0 ripple plan rather
than a mixed Airtable-replacement plus IDE roadmap. The first three actionable clusters should be:

1. R0 baseline and inventories.
2. R1-R5 runtime, validation, loader materialization, and validated commit.
3. R6-R8 source conversion over `LoaderRefRep` and retirement of transitional representations.

R9 should be present as a downstream holding row or small group of holding rows only if the sheet
needs to preserve visibility for codegen, wrappers, diff, CI polish, workflow docs, and LSP work.

## 2026-08-10 sheet reconciliation

Use `S2-*` task IDs for new TDL rows so the historical `TDL R1` through `TDL R4` IDs remain
reserved for the completed or superseded pre-reconciliation work.

The current implementation has already bundled the new plan's R0, R6, R7, and R8 source-tooling
work into a completed issue. The remaining active tracking rows therefore collapse to:

- `S2-R1` through `S2-R5` for the Schema 2.0 runtime, validation, default materialization, and
  loader integration work; and
- three downstream R9 holding rows:
  - `S2-R9a` for derived tooling, codegen, diff, CI, workflow, and contributor ergonomics;
  - `S2-R9b` for LSP and editor services; and
  - `S2-R9c` for retiring Airtable as source of truth for MAP Core Schema.

The old `TDL R5`, `TDL R6`, `TDL R7a`, `TDL R7b`, and `TDL R8` rows should be abandoned rather than
rewritten in place. Their intent is carried forward by the `S2-*` rows, while their historical IDs
remain readable as part of the earlier plan lineage.
