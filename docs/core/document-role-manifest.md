# MAP Core Document Role Manifest

## Purpose

This manifest defines the target organization, ownership boundaries, and
authority of the MAP Core documentation. It governs where a design claim
belongs; it does not itself define MAP behavior.

The manifest is intended to keep the documentation concise and DRY as the MAP
evolves. Each normative claim should have one authoritative home. Other
documents may summarize that claim, but should delegate to its owner rather
than restating the full rule.

## Target Structure

```text
core/
  type-system/
    guides/
    tdl/
  core-runtime/
    descriptors/
  commands/
  dances/
  map-queries/
  transactions/
  agent-spaces/
  validation/
  adaptive-systems/
```

These are documentation ownership boundaries, not Rust crate or package
boundaries.

Component-specific schema documentation belongs with the component whose
concepts it defines. The physical TDL source files are organized under
`map-holons/schema-src/` by owning schema package.

## Section Responsibilities

| Section | Owns | Does not own |
|---|---|---|
| `type-system/` | Universal schema model, descriptor semantics, extension-schema rules, schema catalog, TDL language, and schema-authoring guidance | General Rust runtime representation or component-specific behavior |
| `core-runtime/` | Holons, references, runtime states, typed wrapper conventions, collections, and cross-cutting runtime contracts | Universal schema semantics or feature-specific execution models |
| `core-runtime/descriptors/` | Runtime descriptor subsystem, graph preparation, completion boundary, descriptor-kernel integration, and descriptor-specific runtime access | The structural schema model or representation-neutral semantic algorithms |
| `commands/` | Command model, dispatch, runtime command structures, undo/redo behavior, and command-owned schema | General runtime infrastructure |
| `dances/` | Dance definitions, invocation and execution behavior, capsules, and dance-owned schema | Generic command or query semantics |
| `map-queries/` | Query model, query engine, planning, execution, distribution, and query-owned schema | General storage or collection contracts except where consumed by queries |
| `transactions/` | Transaction lifecycle, staging, commit, rollback, recovery, occurrence persistence, and transaction-owned schema | Descriptor semantics or generic storage implementation |
| `agent-spaces/` | Agent-space topology, activation, trust channels, and agent-space-owned schema | Generic holon-space or reference behavior |
| `validation/` | Validation architecture, PVL, validation execution, and validation-owned schema | Descriptor-dependent semantics that PVL intentionally excludes |
| `adaptive-systems/` | Extension-schema usage, observation and usage capture, personalization, adaptive evolution, and supporting background activity | Universal rules governing whether and how schemas may extend one another |

## Scoped Authorities

Authority is assigned by concern. No single document is the authority for the
whole type system or runtime.

| Concern | Canonical document or source | Role |
|---|---|---|
| Type-system orientation | `type-system/map-type-system.md` | Concise conceptual overview and navigation |
| Schema locality and ownership | `type-system/schema-design-spec.md` | Normative Schema/Component stewardship boundary and cross-Schema reference model |
| Structural schema model | `type-system/schema-design-spec.md` | Normative meta-model, relationships, declaration surfaces, and structural invariants |
| Descriptor invariants | `type-system/descriptor-semantics-rules.md` | Normative representation-neutral algorithms and stable `DS-*` invariants |
| Value constraints | `type-system/value-constraints-design-spec.md` | Normative value-constraint model and specialized conformance semantics |
| Relationship constraints | `type-system/relationship-constraints-design-spec.md` | Normative relationship constraint surface and conformance boundaries |
| Extension schemas | `type-system/extension-schema-design.md` | Non-authoritative WIP placeholder; no accepted extension-specific ownership, compatibility, or evolution rules yet |
| Schema ripple process | `type-system/schema-ripple-design-spec.md` | Schema-change derivation, impact analysis, and consistency workflow |
| Schema inventory and ownership | `type-system/schema-catalog.md` | Logical schema catalog and mapping to centrally stored TDL sources |
| Exact MAP schema declarations | `map-holons/schema-src/**/*.tdl` | Authoritative type, property, relationship, key-rule, and schema declarations |
| TDL language | `type-system/tdl/tdl-spec.md` | Normative syntax, binding, omission, and translation behavior |
| Schema authoring workflow | `type-system/guides/map-schema-authoring-guide.md` | Operational use of the current schema tooling |
| Core runtime | `core-runtime/core-holonic-runtime-design-spec.md` | Master runtime concepts, invariants, and boundaries |
| Runtime shared types | `core-runtime/runtime-shared-types.md` | Shared Rust/runtime representations and contracts |
| Descriptor runtime | `core-runtime/descriptors/descriptors-design-spec.md` | Master runtime descriptor design and delegation point |
| Descriptor processing layers | `core-runtime/descriptors/layered-desc-arch.md` | Construction, completion, graph preparation, and kernel invocation architecture |
| Default-completion workflow | `core-runtime/descriptors/layered-desc-arch.md` | Normative ownership, deferred-outcome, clone, and bootstrap-backstop contract for descriptor-defined defaults |
| Validation layers and guarantees | `validation/validation-arch.md` | Normative guarantee names, execution layers, and their boundaries |
| Validation dependency placement | `validation/dependency-gravity.md` | Normative dependency classes and placement decision test |
| Commit validation behavior | `validation/commit-validation-design-spec.md` | Normative Commit assessment, outcome, state, and public persistence-gate contract |
| Relationship occurrence persistence | `transactions/relationship-persistence-design-spec.md` | Normative local bucket, paired persistence, concurrency retry, and deferred cross-Space inverse contract |
| Validation rule vocabulary and inventory | `validation/validation-schema-design-spec.md` | Core/extension package boundary, rule identities, bindings, and current/target corpus inventory |
| Commit-validation delivery sequence | `validation/commit-validation-impl-plan.md` | Precursor, capabilities, activation gate, and branch/merge sequencing |
| Component behavior and schema | Owning component section | Component-specific design authority |

Paths for documents not yet created or moved describe the target state. Their
presence in this table does not make a placeholder or superseded document
authoritative.

## Document Roles

### Design spec

A design spec defines authoritative intended behavior: concepts, invariants,
relationships, naming, contracts, and boundaries. It states the design without
embedding issue scope, PR sequencing, or implementation checklists.

### Master design document

A master design document establishes a subsystem's purpose, conceptual model,
major contracts, and boundaries. It delegates specialized rules to focused
specs and does not reproduce them.

`core-runtime/descriptors/descriptors-design-spec.md` is the master design
document for the runtime descriptor subsystem. Typed Rust wrappers are part of
the general core-runtime pattern and are included there only where descriptor
behavior specializes that pattern.

### Architecture document

An architecture document explains component and layer composition, data flow,
responsibility boundaries, and integration. It delegates normative domain
semantics to design specs.

### Language specification

A language specification defines source syntax and the meaning of source
constructs. It owns language-specific behavior but delegates schema and runtime
semantics to their respective design specs.

### Catalog

A catalog records identities, ownership, dependencies, versions, and source
locations. It does not redefine the cataloged entities.

### Guide

A guide explains how to perform an operation using the authoritative design.
It may contain examples and commands but does not introduce normative rules.

### Implementation plan

An implementation plan describes the delta from implementation to design,
including sequencing and delivery units. It cites design specs for authority
and must not become the only source of a design decision.

### Checklist

A checklist verifies conformance to named authoritative rules. It is derived
material and must be rebuilt when its governing rules change.

### Archive

Archived documents preserve rationale and superseded designs. They are never
active authority and must not appear in active navigation as current specs.

## Claim Ownership Rules

1. Put each normative claim in the most specific authoritative document named
   by this manifest.
2. Summaries in other documents must link to the authority and avoid copying
   full algorithms, inventories, or rule tables.
3. The TDL corpus owns exact schema declarations. Prose specs own the rules that
   make those declarations meaningful and valid.
4. Generated JSON and loader DTOs are projections or transport forms, not
   schema or semantic authorities.
5. Component schema concepts belong to their component even though their TDL
   files are physically centralized.
6. Cross-component rules belong in `type-system/`, `core-runtime/`, or another
   explicitly cross-cutting section, not in whichever component first needed
   them.
7. Rust API shape belongs in runtime documentation. Representation-neutral
   schema semantics must not depend on a particular Rust wrapper or trait.
8. Implementation status belongs in plans and issues, not in design specs.
9. Historical alternatives belong in the archive or a short rationale section,
   not interleaved with current normative rules.
10. When two active documents conflict, the scoped authority in this manifest
    controls. The conflict must still be removed rather than left for readers
    to resolve.

## Descriptor Boundary

The type system defines what descriptors mean. The runtime descriptor
subsystem defines how the holonic runtime prepares, invokes, and exposes those
semantics.

The descriptor kernel operates on the existing holonic representation. A
separate Semantic IR is not part of the target architecture. Creation adapters
and completion stages may use source- or loader-specific transport structures,
but they must produce an explicit holon representation before descriptor-kernel
validation.

Default materialization belongs to creation and completion. The descriptor
kernel computes and validates; it does not fill omitted values or mutate the
representation supplied to it.

## TDL Corpus and Logical Ownership

All authoritative MAP schema TDL files are physically stored by package under:

```text
map-holons/schema-src/
  core/
    root.tdl
    abstract-value-types.tdl
    concrete-value-types.tdl
    keyrules.tdl
    loader-types.tdl
    operator-types.tdl
    property-types.tdl
    relationship-types.tdl
    value-constraint-types.tdl
  dance/schema.tdl
  commands/schema.tdl
  query/schema.tdl
  query-dance/schema.tdl
  validation/schema.tdl
  test/book-person-inverse.tdl
```

Generated JSON mirrors this layout under `map-holons/generated/json-imports/`.
Physical organization makes package ownership and direct dependencies visible;
it does not transfer conceptual ownership to the type-system section. For
example, query types remain owned and explained by `map-queries/`, while their
exact declarations remain in the Query package.

Every declared relationship descriptor and its inverse belong to the same
owning schema package. A package appends an affordance occurrence through its
own inverse descriptor rather than re-declaring a Core holon. This preserves
Core-side discovery after the owning package is loaded without moving its
symbols into Core.

## Implemented Schema 2.0 Package Layout

The following package identities, direct dependencies, and source paths are
the implemented Schema 2.0 layout. Runtime dispatch is a separate concern and
does not reverse these import directions.

| Package | Identity | Direct dependencies | Source |
|---|---|---|---|
| Core | `MAP Core Schema-v0.0.7` | None | `core/` |
| Dance | `MAP Dance Schema-v0.1.0` | Core | `dance/schema.tdl` |
| Commands | `MAP Commands Schema-v0.1.0` | Core, Dance | `commands/schema.tdl` |
| Query | `MAP Query Schema-v0.0.2` | Core | `query/schema.tdl` |
| QueryDance | `MAP Query Dance Adapter Schema-v0.1.0` | Core, Dance, Query | `query-dance/schema.tdl` |
| Validation | `MAP Validation Schema-v0.1.0` | Core | `validation/schema.tdl` |
| Test | `BookAuthorInverseSchema` | Core | `test/book-person-inverse.tdl` |

Core owns the schema-backed loader representation: `HolonLoadSet`,
`HolonLoaderBundle`, `LoaderHolon`, `LoaderRelationshipReference`,
`LoaderHolonReference`, and `HolonLoadError`. It contains no Dance or Command
symbols, relationship descriptors, or affordance occurrences.

Dance owns generic Dance descriptors and metadata, the generic
`AffordsDance` / `DanceAffordedBy` pair, Dance implementation relationships,
`LoadHolons`, `HolonLoadResponse`, and `HasLoadError` / `LoadErrorOf`.
Query imports no Dance symbols and declares no Dance entry point. QueryDance
owns its concrete adapter types and declares `QueryDance.DanceAffordedBy ->
HolonSpace` through the generic Dance relationship pair. It does not define a
second relationship pair even where their base relationship names
overlap.

`type-system/schema-catalog.md` will provide the stable map between:

- logical schema identity and version;
- owning architectural component;
- TDL source files;
- declared schema dependencies; and
- generated or imported projections.

## Migration Status

This manifest establishes the target structure before content migration.
Existing documents remain at their current paths until they are reviewed,
moved, split, reconstructed, or archived in later refactor phases.

In particular:

- `docs/core/descriptors/` remains a temporary source directory;
- `docs/core/commands-and-runtime/` remains active until its documents move to
  `docs/core/commands/`;
- adaptive-system documents have moved intact to `adaptive-systems/`;
- the Extension Schema design remains an explicitly non-authoritative WIP;
- constraint, relationship-persistence, and schema-ripple documents now reside
  with their owning sections, with superseded constraint proposals archived;
- `type-system/map-type-system.md` is now a concise conceptual overview that
  delegates normative detail to the scoped authorities in this manifest;
- the obsolete pressure-test checklist and meta-value import guide are
  archived, and the schema-authoring guide now treats TDL as authoritative;
- `type-system/tdl/tdl-impl-plan-v2.md` is reconciled with the authority set and
  current `map-holons/main` implementation baseline;
- the current descriptor facade document is not promoted by this manifest;
- archived effective-descriptor designs remain outside the active architecture;
  and
- navigation is updated incrementally as canonical documents reach their target
  paths.
