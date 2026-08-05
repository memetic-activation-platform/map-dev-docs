# TDL Implementation Plan v2: Explicit Holon Graph Toolchain

## 1. Purpose

This plan brings the TDL compiler, decompiler, Holon Data Loader, and runtime descriptor services
into conformance with Schema 2.0.

It implements the architecture defined by:

- [`schema-design-spec.md`](../schema-design-spec.md), which defines the normative Schema 2.0
  structural model;
- [`descriptor-semantics-rules.md`](../descriptor-semantics-rules.md), which defines
  normative effective-contract, inheritance, key-rule, default, and conformance semantics;
- [`value-constraints-design-spec.md`](../value-constraints-design-spec.md) and
  [`relationship-constraints-design-spec.md`](../relationship-constraints-design-spec.md), which
  define specialized constraint semantics;
- [`descriptors-design-spec.md`](../../core-runtime/descriptors/descriptors-design-spec.md), which
  defines the runtime descriptor subsystem;
- [`layered-desc-arch.md`](../../descriptors/layered-desc-arch.md), which assigns architectural
  responsibilities; and
- [`validation-arch.md`](../../validation/validation-arch.md), which owns descriptor-aware
  validation orchestration separately from descriptor-independent PVL; and
- [`tdl-spec.md`](tdl-spec.md), which defines TDL v0.8 syntax and lowering.

The retained [`schema-2.0.md`](../schema-2.0.md) records design rationale and comparison history; it
is not the current normative implementation authority. The WIP Extension Schema design is also not
an implementation dependency for this plan.

The implementation starts from `map-holons/main` after the Schema 2.0 Core Schema TDL corpus was
merged. Earlier work on branch 578 is design and test material, not an implementation base.

## 2. Target outcome

TDL and MAP JSON parsers produce the same schema-backed `LoaderRefRep` holon graph. Source
conversion renders either syntax directly from that representation. Holon Loading submits
`LoaderRefRep` through the existing loader client and guest components, which resolve it into the
staged Holons Core representation, materialize applicable descriptor defaults, and invoke commit.
Commit calls the shared Holon Validator before persistence. Descriptor-aware runtime behavior uses
the existing `HolonDescriptor` typed runtime wrapper and reference-layer operations.

```text
TDL --------> TDL parser ----+
                            +--> LoaderRefRep --> MAP JSON or canonical TDL
MAP JSON --> JSON parser ---+         |
                                      v
                              Holon Loader client
                                      |
                                      v
                              guest loader resolution
                                -> staged holons
                                -> default materialization
                                -> commit
                                     -> Holon Validator
                                     -> persist when valid
```

The target does not contain a second mutable semantic representation between loader input and
runtime holons.

`LoaderRefRep` is an architectural name for the existing transient holon graph rooted at
`HolonLoadSet`, including `HolonLoaderBundle`, `LoaderHolon`, `LoaderRelationshipReference`, and
`LoaderHolonReference`. It is not a proposed Rust DTO family, semantic IR, or graph adapter. Host
and guest serialize and use the same holonic representation.

Source conversion and Holon Loading are separate operations. TDL-to-JSON, JSON-to-TDL, and fidelity
comparison operate on `LoaderRefRep` without guest descriptor binding, default materialization, or
descriptor-driven validation. Only a load operation submits that graph to the guest lifecycle.

## 3. Current `main` baseline

### 3.1 Schema source

The `schema-src` directory contains the Schema 2.0 Core Schema TDL corpus. It expresses:

- the unified descriptor hierarchy rooted at `TypeDescriptor`;
- the meta-type branch through `MetaTypeDescriptor Extends HolonType`;
- explicit `DescribedBy` and optional explicit `Extends`;
- separate descriptor self-conformance and descriptor specialization;
- descriptor-defined `DefaultValue` and `InheritanceMode` data; and
- explicit relationship endpoint, cardinality, inverse, and deletion semantics.

This corpus is the primary compiler acceptance fixture.

### 3.2 TDL tooling

`tools/map-schema` currently parses an older TDL generation. Its TDL path constructs
`map_schema_semantic::SemanticModel`, lowers that model into the tool-local `loader_ir`, and renders
JSON. Its JSON path likewise uses `loader_ir` and projects back into `SemanticModel` for semantic
comparison. Neither representation is the existing `HolonLoadSet` graph used by the Holon Loader.

The new Core Schema corpus does not pass the current parser; the first failure is the explicit
`type` clause on a Schema 2.0 descriptor declaration. Existing map-schema corpus tests exercise an
older fixture generation and therefore do not establish v0.8 acceptance.

The tooling currently owns separate `Schema`, `TypeDescriptor`, `SemanticReference`,
`LoaderDocument`, `LoaderHolon`, `LoaderReference`, and related types. These are compatibility
artifacts from the retired semantic-IR and loader-IR designs.

### 3.3 Runtime descriptor behavior

`holons_core::descriptors` contains useful Schema 1.2 inheritance and effective-member helpers over
`HolonReference`. Some algorithms and tests remain reusable, but the combined
`effective_descriptor_lineage` behavior is not a Schema 2.0 semantic primitive. Schema 2.0 keeps
describing-type conformance, subtype classification, and inherited populated values separate.

`HolonDescriptor` already provides the typed runtime descriptor surface and effective-surface operations
over `HolonReference`. Schema 2.0 work should extend and correct that existing surface rather than
introducing a separate graph interface or descriptor-semantics representation.

### 3.4 Holon Data Loader

The loader already provides a close structural match to the target creation path:

1. Parse JSON into transient loader holons.
2. Stage target holons with authored properties.
3. Resolve `DescribedBy`.
4. Resolve `Extends`.
5. Resolve remaining relationships.
6. Commit staged holons.

The missing steps are loader-specific descriptor-default materialization after reference resolution
and mandatory Holon Validator invocation by commit.

## 4. Implementation principles

### 4.1 One holonic runtime representation

`Holon`, its transient/staged/saved variants, relationships, and `HolonReference` are the runtime
representation on which descriptor semantics operate. `LoaderRefRep` is a role played by an
existing schema-backed holon graph during loading and source conversion. Source ASTs, source maps,
indexes, rendered output, and comparison signatures may exist as bounded support structures but do
not own semantic behavior or duplicate mutable holon state.

### 4.2 HolonDescriptor is the runtime descriptor surface

Inheritance, effective contracts, semantic inheritance, endpoint compatibility, and key-rule
resolution are implemented through `HolonDescriptor`, its typed descriptor wrappers, and existing
reference-layer helpers. The Holon Validator delegates descriptor-semantic conformance operations
to that same implementation. TDL parsing does not execute descriptor semantics.

### 4.3 Loader materialization mutates; descriptor semantics do not

The Holon Loader's materialization service calls read-only `HolonDescriptor` operations to determine
effective contracts and defaults, then writes materialized values through staged-holon APIs.
`HolonDescriptor`, the Holon Validator, and commit do not apply defaults.

### 4.4 Loader construction is explicit and bounded

Guest loader components construct relationships before full conformance can be checked. Any
construction-scoped mutation capability is limited to the loader, cannot escape to ordinary
mutation callers, and is followed by default materialization and validated commit.

### 4.5 Descriptor data drives behavior

The implementation must not replace Schema 2.0 descriptor data with hard-coded tables of legal
types, members, defaults, enum variants, or effective values. Bootstrap contains only the minimum
representation mechanics needed to enter the reflective graph.

### 4.6 Diagnostics stop the owning operation

Syntax or lowering failures stop TDL/JSON source conversion. Unresolved loader references or failed
default materialization prevent commit from being called. Holon Validator violations cause commit
to persist nothing.

## 5. Target dependency direction

```text
holons_core
    - HolonDescriptor and typed descriptor wrappers
    - existing HolonReference and descriptor helpers

descriptor-aware validation subsystem (coordinator/runtime-safe)
    -> holons_core descriptor semantics
    - reusable Holon Validator, contexts, and validation results

descriptor-independent PVL / Integrity-safe validation
    - remains bounded and descriptor-independent
    - does not depend on HolonDescriptor or coordinator graph services

holons_loader / holons_loader_client
    -> holons_core and descriptor-aware validation subsystem
    - MAP JSON parsing to LoaderRefRep
    - loader-reference resolution
    - loader-specific default materialization
    - commit integration

map-schema
    -> shared LoaderRefRep construction and inspection APIs
    - TDL parsing and lowering
    - TDL/JSON rendering
    - source diagnostics and LoaderRefRep fidelity projections
```

The exact crate placement of the descriptor-aware Holon Validator and shared LoaderRefRep
construction APIs is an implementation decision, but neither may force descriptor dependencies
into Integrity-safe PVL code or create a parallel loader DTO family. `map_schema_semantic` and the
tool-local `loader_ir` are removed after their remaining callers migrate. New semantic rules must
not be added to either during the transition.

### 5.1 Authority-to-delivery traceability

| Authority | Primary delivery work |
| --- | --- |
| Schema Design Spec | R1 structural/effective descriptor operations; R4 structural and conformance validation |
| Descriptor-Kernel Semantic Rules | R1 kernel operations; R3 default-materialization inputs; R4 conformance rules |
| Value and Relationship Constraint Specs | R4 specialized constraint validation |
| Runtime Descriptor Subsystem Design | R1 `HolonDescriptor`/typed-wrapper integration; R3 descriptor-backed default access |
| Layered Descriptor Architecture | R3 materialization ownership; R5 load/commit ordering; R6-R7 source boundaries |
| Validation Architecture | R2 Holon Validator framework; R4 rule coordination; R5 commit invocation; PVL separation |
| TDL v0.8 Spec | R6 parsing/lowering; R7 rendering and fidelity |

## 6. Delivery tracks and integration order

R0 establishes the baseline. The runtime track (R1-R5) and source-tooling track (R6-R8) may then
advance in parallel. R5 is the runtime integration point; R8 retires the transitional source
representations only after all source-tooling consumers have migrated. R9 remains downstream of
the stable boundaries and is not required to begin either primary track.

### R0. Establish the executable baseline

Record the current expected failures and protect the new source corpus.

Work:

- Add or retain a smoke test that runs TDL checking against the complete `schema-src` corpus.
- Record the current parser failure as an expected migration test, not as accepted behavior.
- Inventory all callers of `SemanticModel`, tool-local `loader_ir`, Schema 1.2
  `effective_descriptor_lineage`, and direct descriptor-validation helpers.
- Identify branch 578 commits containing reusable kernel algorithms and tests without merging that
  branch wholesale.
- Establish focused test fixtures for defaults, separate hierarchy axes, endpoint compatibility,
  abstract descriptors, and loader pre-commit failure.

Exit condition:

- The migration has a reproducible red baseline tied to Schema 2.0 behavior.

### R1. Align HolonDescriptor with Schema 2.0 semantics

Extend the existing `holons_core::descriptors::HolonDescriptor` surface and supporting descriptor
helpers to implement the Schema 2.0 rules. Port branch 578 algorithms only where they fit this
existing holonic representation and current schema.

Work:

- Preserve `HolonDescriptor` as the main typed runtime surface reached through
  `ReadableHolon::holon_descriptor()`.
- Preserve encapsulation of its wrapped `HolonReference`; add focused accessors instead of a public
  unwrapping path.
- Implement structural traversal, single inheritance, cycle detection, and `SubtypeOf`.
- Implement separate APIs for:
  - `EffectiveInstanceContract`;
  - `ConformanceContract`;
  - semantic inheritance of populated values; and
  - effective endpoint type.
- Report actionable `HolonError` values with descriptor and member provenance.
- Port reusable branch 578 tests only when they agree with Schema 2.0.
- Add explicit regression tests proving that descriptor self-conformance is not flattened into the
  descriptor's own specialization lineage.

Exit condition:

- `HolonDescriptor` and its typed wrappers provide the required Schema 2.0 effective operations
  across transient, staged, and saved references.

### R2. Integrate HolonDescriptor with the shared Holon Validator

Make the Holon Validator the reusable entry point for descriptor-driven holon validation in a
coordinator/runtime-safe validation subsystem.
It delegates Schema 2.0 predicates and conformance algorithms to `HolonDescriptor` and existing
descriptor helpers.

Work:

- Define validation scopes, contexts, results, and deterministic violation accumulation in the
  validation subsystem.
- Use `ReadableHolon::holon_descriptor()` to obtain effective contracts for ordinary and descriptor
  holons.
- Replace Schema 1.2 combined-lineage validation consumers with the appropriate Schema 2.0
  operation.
- Keep descriptor-independent PVL outside this integration.
- Do not add `HolonDescriptor`, Reference Layer, or open-graph dependencies to the Integrity-safe
  PVL implementation or its shared deterministic primitives.
- Verify equivalent validation behavior across transient, staged, and saved graph states.

Exit condition:

- Runtime and Holon Validator behavior share `HolonDescriptor` semantics without duplicate
  inheritance, contract, or conformance implementations.

### R3. Implement loader-specific descriptor-default materialization

Add a modular graph-level materialization service to the guest Holon Loader over writable staged
references.

Work:

- Resolve effective property contracts through `HolonDescriptor`.
- Add the schema-backed `PropertyDescriptor::default_value()` accessor and use it to read declared
  defaults from effective property declarations.
- Preserve explicit values.
- Materialize a valid descriptor-defined default only for an omitted required property.
- Leave optional omissions absent.
- Leave required omissions without defaults for the Holon Validator to report.
- Materialize required control values such as descriptor-defined `InheritanceMode.None`.
- Report failures to determine or apply declared defaults and prevent commit invocation.
- Make materialization idempotent and accumulate independent materialization errors.
- Retain successful writes in the failed staged transaction for diagnostics, then abandon or roll
  back the transaction as a whole.
- Keep authored/materialized provenance in an ephemeral sidecar only; persist no distinction.

Exit condition:

- JSON- and TDL-originated `LoaderRefRep` graphs produce equivalent materialized staged state, and
  the service remains modular enough for possible later reuse outside Holon Loading.

### R4. Complete descriptor-driven Holon Validation

Implement the remaining rules required for the Holon Validator to validate the
default-materialized Schema 2.0 graph through `HolonDescriptor`.

Work:

- Validate exactly one admissible, non-abstract `DescribedBy` target.
- Validate effective property and relationship contracts.
- Validate relationship source and target compatibility through `EffectiveEndpointType`.
- Validate cardinality, ordering, duplicate policy, inverse pairing, and deletion semantics.
- Validate property requiredness, value types, enums, arrays, and value constraints.
- Implement `None`, `Additive`, and `Override` populated-value inheritance with provenance.
- Implement effective instance-key-rule resolution and key conformance.
- Implement abstract-descriptor completeness without exempting supplied invalid values.
- Accumulate all independently discoverable violations in deterministic order; stop only when a
  fatal access or infrastructure failure makes further results unreliable.

Exit condition:

- The Holon Validator can validate the Schema 2.0 Core Schema graph without source-specific rules
  or duplicated descriptor-semantic algorithms.

### R5. Integrate materialization and validated commit into Holon Loading

Insert the shared services after relationship resolution and before commit.

Target flow:

```text
Pass 1: stage properties
  -> Pass 2a: resolve DescribedBy
  -> Pass 2b: resolve Extends
  -> Pass 2c: resolve remaining relationships
  -> Pass 3: materialize descriptor defaults
  -> commit
       -> invoke Holon Validator
       -> persist only when valid
```

Work:

- Expose the fully resolved staged graph to the graph-level materialization service.
- Convert materialization and Holon Validator failures into loader error holons with source
  provenance.
- Do not invoke commit after any materialization failure.
- Make commit invoke the reusable Holon Validator and persist nothing after any blocking violation.
- Ensure construction-scoped relationship writes cannot bypass final validation.
- Test mixed references to new staged and existing saved descriptors.

Exit condition:

- Holon Loading commits only default-materialized, Schema 2.0-conformant staged holon graphs.

### R6. Rebuild TDL parsing over LoaderRefRep

Update parsing and lowering to TDL v0.8, then remove `SemanticModel` from compilation.

Work:

- Parse every declaration and clause used by the merged Schema 2.0 TDL corpus.
- Preserve explicit `type`, optional explicit `extends`, quoted keys, generic `instance`, schema
  dependencies, relationship maps, and unbounded `*` cardinality.
- Lower declaration shorthand directly into schema-backed `LoaderRefRep` holons and relationships.
- Copy authored reference keys into `LoaderHolonReference`s without host-side ID or symbol
  resolution.
- Preserve source spans in a bounded provenance sidecar keyed to loader-graph identities. Explicit
  versus omitted values remain distinguishable in the graph itself; do not create a second mutable
  semantic representation merely to retain source provenance.
- Render MAP JSON directly from `LoaderRefRep`.
- Limit host diagnostics to syntax and source-to-`LoaderRefRep` lowering failures.
- Avoid declaration-kind or name-based semantic inference after lowering.

Exit condition:

- The complete `schema-src` corpus parses into `LoaderRefRep`.
- `map-schema compile schema-src` emits MAP JSON equivalent to that loader graph and accepted by
  the existing Holon Loader client.

### R7. Rebuild decompilation and LoaderRefRep fidelity

Move JSON-to-TDL and round-trip comparison onto `LoaderRefRep`.

Work:

- Parse MAP JSON into the same `LoaderRefRep` produced by TDL.
- Render canonical TDL from loader holons, explicit properties, and keyed relationships.
- Collapse TDL shorthand only when recompilation preserves loader-graph content.
- Derive immutable comparison signatures from `LoaderRefRep`.
- Compare loader keys, descriptor keys, explicit properties, keyed relationships, order, and
  literal values.
- Keep source residue local to fidelity reporting when TDL cannot represent it losslessly.
- Reject comparison when either source cannot lower to a well-formed `LoaderRefRep`.

Exit condition:

- JSON -> TDL -> JSON and TDL -> JSON -> TDL preserve equivalent `LoaderRefRep` graphs over the Core
  Schema corpus and focused fixtures.

### R8. Retire the separate semantic IR and tool-local loader IR

Remove transitional types and code after all consumers use the explicit holon graph.

Work:

- Remove `SemanticModel`, `Schema`, `TypeDescriptor`, `SemanticReference`, the tool-local
  `LoaderDocument`/`LoaderHolon`/`LoaderReference` family, and their compatibility re-exports.
- Replace `map_schema_semantic` indexes with `LoaderRefRep`-derived tooling indexes or move non-semantic
  source utilities to an appropriately named tooling crate.
- Remove `schema_to_loader_ir`, obsolete IR adapters, and duplicate conformance paths.
- Remove stale architecture comments and test vocabulary.
- Remove the crate when no bounded source or diagnostic utility remains.

Exit condition:

- No production semantic algorithm consumes the retired IR, and no mutable copy of semantic holon
  state exists outside Holons Core.

### R9. Build derived consumers

Code generation, LSP features, and future editor services consume `LoaderRefRep`, saved holons, or
derived immutable indexes according to their actual boundary.

These consumers may proceed after the loader and validation boundaries are stable. They do not
block retirement of the separate semantic IR and must not introduce another semantic authority.

## 7. Test strategy

### 7.1 HolonDescriptor and Holon Validator tests

Use focused transient and staged holon graphs to test:

- no-parent, linear, cyclic, and multiple-parent `Extends`;
- exactly-one `DescribedBy`;
- separate conformance and specialization axes;
- additive contract inheritance and illegal redeclaration;
- `None`, `Additive`, and `Override` value inheritance;
- endpoint compatibility for ordinary and descriptor holons;
- default validity and requiredness;
- abstract descriptor completeness; and
- effective key rules.

### 7.2 Runtime lifecycle tests

Run equivalent cases through:

- transient references;
- staged references;
- saved references where available;
- Holon Validator invocation outside commit.

Equivalent holons must produce equivalent `HolonDescriptor` and Holon Validator results.

### 7.3 Loader integration tests

Verify:

- unresolved references prevent materialization and commit;
- defaults are physically present before commit;
- missing required values prevent commit;
- semantic violations preserve loader provenance;
- staged-to-staged and staged-to-saved references validate consistently; and
- the Holon Validator invoked by commit accumulates independently discoverable violations, and
  commit persists no invalid graph.

### 7.4 TDL acceptance tests

Use the full `schema-src` corpus for:

- syntax and lowering checks;
- JSON compilation;
- loader acceptance;
- decompilation; and
- round-trip `LoaderRefRep` fidelity.

Focused fixtures remain necessary so a corpus-level failure can be diagnosed without treating the
Core Schema as one indivisible test.

## 8. Migration rules

- Start implementation branches from `main`.
- Do not merge branch 578 as an architectural unit.
- Port individual algorithms and tests only after comparing them with Schema 2.0 rules.
- Do not add new semantic behavior to `map_schema_semantic` or the tool-local `loader_ir`.
- Preserve existing loader JSON compatibility unless Schema 2.0 explicitly changes the format.
- Keep comparison snapshots immutable and derived from `LoaderRefRep`.
- Keep source provenance outside semantic equality.
- Replace behavior vertically: parser through `LoaderRefRep`, and loader input through validated commit, rather
  than building a second parallel semantic stack.

## 9. Initial non-goals

The first implementation sequence does not include:

- migration of persisted Schema 1.2 descriptor data;
- a new loader JSON format;
- changing Holochain substrate commit semantics;
- full incremental validation of syntactically invalid editor documents;
- code generation redesign; or
- LSP feature expansion;
- Extension Schema compatibility and evolution rules; or
- semantic revision of the preserved adaptive-system documents.

These areas may consume the completed architecture later.

## 10. Completion criteria

The migration is complete when:

1. The complete Schema 2.0 TDL corpus parses into `LoaderRefRep`.
2. TDL and MAP JSON produce equivalent `LoaderRefRep` graphs.
3. Holon Loading materializes descriptor defaults after full reference resolution and before commit.
4. `HolonDescriptor` and its helpers own Schema 2.0 effective-semantics algorithms.
5. The Holon Validator delegates descriptor semantics to `HolonDescriptor` without duplication.
6. Commit invokes the Holon Validator and persists no invalid graph.
7. Compile/decompile round trips preserve `LoaderRefRep` content.
8. The separate `SemanticModel` and tool-local `loader_ir` implementations have been retired.
9. Derived tooling consumes loader graphs, saved holons, or immutable projections without redefining
   semantics.
