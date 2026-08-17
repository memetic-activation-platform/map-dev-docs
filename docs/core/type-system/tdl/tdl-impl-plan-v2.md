# TDL Implementation Plan v3.0
## Schema 2.0 Source Toolchain and LoaderRefRep Fidelity

## Purpose

This plan owns TDL as a source toolchain for Schema 2.0. It accepts TDL and MAP JSON, produces
the common schema-backed `LoaderRefRep` graph, renders either syntax from that graph, and retains
bounded source provenance for diagnostics.

The delivered proof that the Schema 2.0 TDL corpus can compile and load establishes the source
toolchain's handoff boundary. After a graph crosses that boundary and becomes staged holons,
descriptor runtime, default population, validation, and commit are not TDL work.

This plan therefore does not deliver descriptor-aware validation. It also does not own the Holon
Loader lifecycle merely because TDL is one possible source of a loader graph.

## Architecture Boundary

```text
TDL source ------------------+
                             +--> LoaderRefRep --> canonical TDL or MAP JSON
MAP JSON source -------------+          |
                                        | source-toolchain boundary
                                        v
                              Holon Loading and staged holons
                                -> reference resolution
                                -> default population
                                -> Descriptor-Aware Holon Validation
                                -> commit or block
```

`LoaderRefRep` is the existing transient holon graph rooted at `HolonLoadSet`, including
`HolonLoaderBundle`, `LoaderHolon`, `LoaderRelationshipReference`, and `LoaderHolonReference`.
It is not a Rust DTO family, a semantic IR, or a second mutable model of MAP semantics.

TDL-to-JSON, JSON-to-TDL, and fidelity comparison operate entirely on `LoaderRefRep`. A load
operation submits that graph to Holon Loading. The fact that the load eventually invokes a
validator does not make validation part of parsing or lowering.

## Ownership

| Concern | Owner | TDL-track role |
| --- | --- | --- |
| TDL grammar, parser, lowering, rendering, source spans, and source diagnostics | TDL source toolchain | Owns implementation and tests |
| `LoaderRefRep` source representation and JSON/TDL equivalence | TDL source toolchain | Owns implementation and tests |
| Holon staging, reference resolution, construction-scoped writes, default population, and commit wiring | Holon Loading | Consumer of `LoaderRefRep` |
| Effective specification, instance contract, conformance predicates, endpoint compatibility, and inheritance semantics | Descriptor Runtime / `HolonDescriptor` | Source toolchain preserves inputs; it does not compute them |
| `ValidationRule`/`ValidationBinding` collection, rule dispatch, results, and `DS-*` enforcement | Validation track | TDL lowers the Validation Schema as ordinary content |
| Descriptor-independent integrity checks | PVL | No dependency on TDL descriptor semantics |

The [Validation Implementation Plan](../../validation/validation-impl-plan.md) owns all
Descriptor-Aware Holon Validation capabilities. The
[Descriptor-Kernel Semantic Rules](../descriptor-semantics-rules.md) own the meaning of Schema 2.0
descriptor semantics. The runtime descriptor subsystem exposes those products through
`HolonDescriptor`. This plan must neither duplicate nor become an alternative execution path for
any of them.

## Source-Toolchain Rules

- Parse and lower authored syntax; do not execute descriptor semantics.
- Preserve explicit `type`, `extends`, properties, relationships, cardinalities, schema
  dependencies, keys, and literals as authored loader-graph content.
- Do not infer type categories, effective members, enum membership, defaults, relationship
  endpoints, key values, or validation applicability from declaration spelling or local names.
- Keep host-side diagnostics limited to syntax and source-to-`LoaderRefRep` lowering failures.
- Preserve source spans in a bounded sidecar keyed to loader-graph identities. Source provenance is
  not semantic equality and does not require another mutable semantic representation.
- Compile the Validation Schema exactly as ordinary TDL. `ValidationRule`, `ValidationBinding`,
  `AppliesTo`, and `UsesRule` receive no compiler-specific execution behavior.
- Loader, materialization, or validation failures may be presented with source provenance when it
  is available, but remain lifecycle diagnostics rather than TDL compiler errors.

## Baseline

Schema 2.0 TDL-driven holon loading is already proven. The source toolchain has demonstrated that
the Schema 2.0 corpus can become `LoaderRefRep`, traverse the ordinary loading path, and produce a
holonic graph suitable for runtime processing.

That proof is intentionally narrower than descriptor-aware validation. It proves source
conversion and loadability; it does not claim that `DS-*` rules execute while parsing or that all
post-resolution validation has been delivered.

## Delivery Sequence

### T1 — Preserve Schema 2.0 Source Fidelity

Maintain and complete parsing/lowering support for every Schema 2.0 construct used by the active
corpus.

Work:

- Parse declaration and clause forms used by the Schema 2.0 corpus.
- Lower directly into schema-backed `LoaderRefRep` holons and relationships.
- Preserve authored reference keys without host-side ID or symbol resolution.
- Preserve separate property and relationship namespaces, ordering, literal values, quoted keys,
  unbounded cardinality, and explicit versus omitted values.
- Render MAP JSON directly from `LoaderRefRep`.
- Retain syntax and lowering diagnostics with actionable spans.

Exit condition:

- The active Schema 2.0 corpus parses into `LoaderRefRep`, and its emitted MAP JSON represents an
  equivalent graph accepted by the ordinary loader client.

### T2 — Canonical Rendering and Round-Trip Fidelity

Make TDL and MAP JSON alternate renderings of the same `LoaderRefRep` content.

Work:

- Parse MAP JSON into the same `LoaderRefRep` used by TDL.
- Render canonical TDL from loader holons, explicit properties, and keyed relationships.
- Collapse TDL shorthand only when recompilation preserves loader-graph content.
- Derive immutable comparison signatures from `LoaderRefRep`.
- Keep source-only residue local to fidelity reporting where TDL cannot represent it losslessly.

Exit condition:

- JSON → TDL → JSON and TDL → JSON → TDL preserve equivalent `LoaderRefRep` graphs across the
  Core and Validation Schema corpora and focused fixtures.

### T3 — Retire Transitional Source Representations

Remove source-tooling representations that duplicate the loader graph after all source-tooling
consumers use `LoaderRefRep`.

Work:

- Remove `SemanticModel`, tool-local `loader_ir`, their compatibility adapters, and duplicate
  conformance paths.
- Replace their indexes with immutable `LoaderRefRep`-derived tooling indexes or move bounded
  source utilities into an appropriately named tooling crate.
- Remove stale comments and vocabulary that imply a TDL-owned semantic runtime.
- Do not replace a retired IR check with TDL-owned descriptor validation.

Exit condition:

- No production source-tooling path maintains a mutable copy of holonic semantic state outside
  `LoaderRefRep` and Holons Core.

### T4 — Derived Source Tooling

Code generation, diffing, CI support, editor services, and contributor workflow tooling may consume
`LoaderRefRep` and immutable derived indexes after T1–T3 provide stable boundaries.

Exit condition:

- Derived tooling does not introduce a third semantic authority or take ownership of runtime
  descriptor validation.

## Loader and Validation Integration Contract

The TDL toolchain has one integration contract with Holon Loading:

> An equivalent TDL and MAP JSON input must produce equivalent `LoaderRefRep` graphs. When each
> graph is submitted to the same loader lifecycle, it must receive the same lifecycle outcome.

This contract permits an end-to-end smoke test, but assigns the work correctly:

| Step after `LoaderRefRep` submission | Responsible track |
| --- | --- |
| Stage holons and resolve references | Holon Loading |
| Compute descriptor products | Descriptor Runtime |
| Populate applicable defaults | Holon Loading |
| Select and execute descriptor-aware rules | Validation |
| Convert blocking results into loader failure and prevent persistence | Holon Loading, consuming Validation |

The TDL test proves equivalence of source paths. It must not assert a separate TDL-specific rule,
produce a separate validation outcome, or make source compilation depend on a descriptor-aware
validator.

## Validation Schema Corpus

The Validation Schema source corpus is
`map-holons/schema-src/map-validation-schema.tdl`; its generated loader artifact is
`map-holons/generated/json-imports/map-validation-schema.json`.

The TDL toolchain parses and lowers this corpus using ordinary Schema 2.0 facilities. Its package
load acceptance is a source and loader compatibility test. Stable rule identities, seeded
bindings, effective binding collection, wrapper dispatch, and `DS-*` execution are owned by
[validation-impl-plan.md](../../validation/validation-impl-plan.md), not by this plan.

## Test Strategy

### Source-toolchain tests

- Grammar and lowering fixtures for every active Schema 2.0 construct.
- Complete Core and Validation Schema corpus compilation.
- TDL-to-JSON emission from `LoaderRefRep`.
- JSON-to-TDL rendering and bidirectional fidelity comparison.
- Focused diagnostic fixtures for syntax and lowering failures.

### Boundary smoke tests

- Submit equivalent TDL- and JSON-originated `LoaderRefRep` graphs to the same loader ingress.
- Verify their source-independent lifecycle result is equivalent.
- Verify loader failures can cite available source provenance without changing their classification
  into compiler errors.

Descriptor-runtime product tests, default-population tests, validation-rule fixtures, blocked
commit tests, and transaction-aware relationship/cardinality tests belong to their owning tracks.

## Non-goals

This plan does not include:

- descriptor-aware validation implementation, rule coverage, or result aggregation;
- `ValidationRule` wrapper dispatch, `ValidationBinding` traversal, or validation profiles;
- descriptor-kernel algorithms or `HolonDescriptor` runtime integration;
- default materialization or validated-commit wiring;
- descriptor-independent PVL behavior or Integrity callback changes;
- full incremental semantic validation of syntactically invalid editor documents;
- migration of persisted Schema 1.2 data; or
- a new loader JSON format.

## Completion Criteria

The TDL source-toolchain migration is complete when:

1. The active Schema 2.0 Core and Validation Schema corpora parse into `LoaderRefRep`.
2. TDL and MAP JSON produce equivalent `LoaderRefRep` graphs.
3. TDL and MAP JSON round trips preserve that graph content.
4. The Validation Schema compiles as ordinary source content with no TDL-specific semantic
   behavior.
5. No retired semantic or loader IR remains a production source-tooling semantic authority.
6. Equivalent TDL and JSON input can be handed to the ordinary loader path without a TDL-specific
   lifecycle or validation branch.
