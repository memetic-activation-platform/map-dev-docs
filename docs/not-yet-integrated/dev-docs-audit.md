# Phase 1 Audit: Type-System and Descriptor Documentation

**Status:** Complete
**Scope:** `docs/core/type-system/`, `docs/core/descriptors/`, related archived documents, `mkdocs-core.yml`, and the current Core Schema TDL corpus in `map-holons/schema-src`
**Method:** Repository inventory, terminology scan, authority/overlap analysis, navigation review, and comparison with the accepted Schema 2.0 architecture
**Changes made:** None

## 1. Architectural Baseline

The following decisions are treated as settled for this audit.

### Documentation structure

- `type-system/` owns universal schema concepts, structural rules, descriptor semantics, extension-schema rules, schema catalog information, and TDL.
- `core-runtime/` owns the general holonic runtime representation and behavior.
- Runtime descriptor support is a subsection of `core-runtime/`, not a top-level peer.
- `adaptive-systems/` is a top-level architectural component.
- Commands, dances, queries, transactions, agent spaces, and validation are top-level component areas.
- Component-specific schema definitions are documented with their owning component.
- The physical `.tdl` files remain centralized in `map-holons/schema-src` to support imports and multi-pass loading.

The target high-level shape is therefore:

    type-system/
    core-runtime/
      descriptors/
    commands/
    dances/
    map-queries/
    transactions/
    agent-spaces/
    validation/
    adaptive-systems/

### Descriptor processing architecture

The accepted processing model is:

    Authored, Imported, or Programmatic Input
            |
            v
    Creation Adapter / Completion Stage
      - parse source syntax
      - resolve identities and references
      - expand source-language shorthand
      - determine omitted values from the bound schema
      - materialize applicable defaults
      - produce an explicit holon representation
            |
            v
    Descriptor Kernel
      - validate descriptor semantics
      - compute effective contracts
      - compute effective semantic inheritance
      - validate conformance

The descriptor kernel computes and validates. It does not inject defaults, complete omitted values, or mutate the representation supplied to it.

The existing shared-object/reference-layer representation based on `Holon`, `HolonReference`, `SavedReference`, and related types serves as the semantic representation. A separate Semantic IR is not part of the target architecture.

`LoaderReference` remains a loader-oriented transport/construction representation. It is not the common semantic execution model.

### Effective descriptors

Both effective-descriptor documents have been archived.

- A transient effective-surface holon remains a possible future performance optimization hidden behind the reference layer.
- The persisted DAG-CBOR effective-descriptor artifact associated with descriptor-dependent PVL is abandoned or indefinitely deferred.
- Neither concept belongs in the active design baseline or current implementation roadmap.

### Runtime wrappers

Typed Rust wrappers around `HolonReference` are a general MAP runtime pattern, not the defining purpose of the descriptor subsystem.

A public descriptor trait that exposes the wrapped reference directly undermines wrapper encapsulation and is not an accepted architectural centerpiece.

## 2. Current Inventory

### Type-system documents

| Document | Current role | Audit finding |
|---|---|---|
| `map-type-system.md` | Broad type-system overview and detailed semantics | Retain but substantially compress and delegate |
| `schema-2.0.md` | Schema 2.0 rationale, design, semantics, defaults, and migration comparison | Distill into a current schema design spec; archive the historical proposal/rationale form |
| `tdl/tdl-spec.md` | Normative TDL language specification | Retain as TDL authority |
| `tdl/tdl-impl-plan-v2.md` | Compiler/decompiler implementation plan | Retain as a plan, but reconcile only after design specs stabilize |
| `runtime-shared-types.md` | Runtime representation and shared runtime types | Move to `core-runtime/`; revise obsolete schema terminology |
| `schema-v2-pressure-test-checklist.md` | Schema validation checklist | Archive or rebuild; it encodes a superseded schema model |
| `map-schema-authoring-guide.md` | Operational schema-authoring guide | Retain as a guide after path and workflow validation |
| `meta-value-types-import-guide.md` | Import guide for older meta-value-type design | Rewrite or archive; currently conflicts with Schema 2.0 |

### Descriptor documents

| Document | Current role | Audit finding |
|---|---|---|
| `descriptor-semantics-rules.md` | Representation-neutral descriptor algorithms and invariants | Retain as the primary semantic authority; move to `type-system/` |
| `descriptors-design-spec.md` | Currently framed as a runtime facade specification | Reconstruct as the master runtime descriptor design document |
| `layered-desc-arch.md` | Cross-layer construction, completion, representation, and kernel architecture | Retain under `core-runtime/descriptors/`; reduce historical detour material |
| `value-constraints-design-spec.md` | Value-constraint schema and validation semantics | Move to `type-system/`; reconcile overlap with the schema and semantic rules |
| `relationship-constraints-design-spec.md` | Relationship semantics, constraints, ordering, and some persistence concerns | Split by ownership or narrow to schema semantics |
| `relationship-persistence-design-spec.md` | Relationship occurrence persistence | Move to transactions/storage; treat as unreviewed rather than established authority |
| `schema-ripple-design-spec.md` | Schema-derived artifact and implementation ripple process | Move to type-system tooling/governance; update its authoritative-source model |
| `adaptive-schema-usage.md` | Extension-schema usage and adaptive evolution | Move to `adaptive-systems/`; preserve its conceptual depth |
| `adaptive-usage-capture.md` | Adaptive usage and personalization capture | Move to `adaptive-systems/`; preserve its conceptual depth |
| `background-usage-transactions.md` | Background transactions supporting adaptive usage capture | Move to `adaptive-systems/`; review current working-tree changes before accepting them |

### Archived documents

| Document | Status |
|---|---|
| `archive/type-definition-semantics.md` | Correctly archived; its special bootstrap-closure model is superseded by multi-pass loading |
| `archive/effective-descriptor.md` | Correctly archived; not an active dependency |
| `archive/effective-descriptor-impl-plan.md` | Correctly archived; not an active roadmap item |
| `archive/descriptors-design-spec-v1.3.md` | Useful historical input when reconstructing the master descriptor design, but not current authority |

## 3. Proposed Authority Model

Authority should be scoped rather than assigned to one monolithic document.

| Concern | Authoritative document |
|---|---|
| Type-system concepts and navigation | `map-type-system.md` |
| Structural meta-schema model and invariants | New `schema-design-spec.md` distilled from `schema-2.0.md` |
| Representation-neutral descriptor evaluation | `descriptor-semantics-rules.md` |
| Extension-schema rules | New `extension-schema-design.md` |
| Exact Core Schema declarations and identities | TDL corpus in `map-holons/schema-src` |
| TDL syntax, binding, omission, and translation rules | `tdl-spec.md` |
| Runtime descriptor subsystem and its boundaries | Reconstructed `core-runtime/descriptors/descriptors-design-spec.md` |
| Construction/completion/kernel layering | `core-runtime/descriptors/layered-desc-arch.md` |
| General runtime shared types | `core-runtime/runtime-shared-types.md` |
| Component-specific schema and runtime behavior | Owning component section |
| Implementation sequencing and deltas | Implementation plans and GitHub issues |
| Operational procedures | Authoring and import guides |

Design specs should not duplicate exact inventories already expressed by the TDL corpus unless the inventory itself is a semantic invariant.

Guides, checklists, and implementation plans must identify their governing specs and must not silently introduce normative semantics.

## 4. Confirmed Consistency Problems

### 4.1 Superseded `DescriptorRoot` model

Active documents still describe `DescriptorRoot` and TypeKind-specific meta-types as the basis of Schema 2.0:

- `runtime-shared-types.md`, especially lines 16 and 67-71
- `schema-v2-pressure-test-checklist.md`, especially lines 51-54, 68, 87-114, and 210
- `meta-value-types-import-guide.md`, especially lines 9, 101, and 141
- Both adaptive documents contain isolated references inherited from the older design

These claims conflict with the current Core Schema TDL and must not survive as active Schema 2.0 rules.

### 4.2 Obsolete key-rule terminology

`map-type-system.md` still defines key behavior using:

- `UsesKeyRule`
- `NoneKeyRule`

The current Core Schema and TDL use `InstanceKeyRule` and an explicit `NoneRule.KeyRuleType` target.

The stale terminology appears prominently in `map-type-system.md` lines 392, 551, and 900-952 and also appears in `meta-value-types-import-guide.md`.

This is a normative contradiction, not merely a naming cleanup.

### 4.3 Incorrect schema source of truth

`schema-ripple-design-spec.md` identifies generated/import JSON under `host/import_files/map-schema/core-schema/` as authoritative.

`map-type-system.md` likewise points readers to `host/import_files/map-schema`.

The current source of truth is the TDL corpus in:

    /Users/stevemelville/dev/map-proto/map-dev/map-holons/schema-src

Generated JSON is a projection or interchange artifact, not the schema authority.

The authoring guide also contains commands and paths that must be validated against the current TDL-based workflow.

### 4.4 Descriptor facade overreach

The active `descriptors-design-spec.md` is titled “Runtime Descriptor Facades Design Spec” and makes wrapper APIs its organizing concern.

Its public `Descriptor` trait exposes the wrapped holon reference, which conflicts with the intended encapsulation of typed runtime wrappers.

The document also elevates a runtime pattern used throughout MAP into the defining architecture of descriptors. It cannot currently serve as the master descriptor design document.

### 4.5 Archived effective-descriptor documents remain active in navigation

`mkdocs-core.yml` still links to:

- `descriptors/effective-descriptor.md`
- `descriptors/effective-descriptor-impl-plan.md`

Those paths have been moved to `archive/`. The navigation is therefore stale and presents deferred work as active architecture.

The active descriptor design spec also links to the archived effective-descriptor design as though it were a current derived artifact.

### 4.6 Navigation preserves the old component structure

`mkdocs-core.yml` currently has:

- `Descriptors Runtime Support` as a top-level peer
- Adaptive-system documents under descriptors
- Runtime shared types under type-system
- Relationship persistence under descriptors
- `Commands and Runtime Layer` using `commands-and-runtime/`

This conflicts with the agreed structural blueprint.

### 4.7 Obsolete pressure-test model

`schema-v2-pressure-test-checklist.md` is built around `DescriptorRoot`, TypeKind-specific meta-types, and the old replacement crosswalk.

Because those are foundational assumptions in the checklist, incremental wording changes would not be sufficient. The checklist should be archived and later rebuilt from the final Schema 2.0 invariants.

### 4.8 Mixed document generations

The active set contains material from at least four design generations:

1. The pre-Schema 2.0 descriptor hierarchy.
2. The Schema 1.2 combined-lineage model.
3. The temporary LoaderReference-to-Semantic-IR architecture.
4. The accepted explicit-holon-representation and descriptor-kernel architecture.

Some historical references are correctly marked as retired, particularly in `layered-desc-arch.md` and `tdl-impl-plan-v2.md`. Others remain written as current rules.

## 5. Major Overlaps

### Structural and semantic inheritance

`DescribedBy`, `Extends`, conformance, effective contracts, semantic inheritance, cardinality, and provenance are explained independently in:

- `map-type-system.md`
- `schema-2.0.md`
- `descriptor-semantics-rules.md`
- `layered-desc-arch.md`
- `tdl-spec.md`

Recommended ownership:

- `schema-design-spec.md`: graph structure and invariants
- `descriptor-semantics-rules.md`: evaluation algorithms
- `map-type-system.md`: concise conceptual summary
- `layered-desc-arch.md`: invocation and representation boundaries
- `tdl-spec.md`: source-language consequences and delegation

### Defaults and omission

Creation-time default materialization is repeated across:

- `map-type-system.md`
- `schema-2.0.md`
- `descriptor-semantics-rules.md`
- `descriptors-design-spec.md`
- `layered-desc-arch.md`
- `tdl-spec.md`

Recommended ownership:

- Schema validity of defaults: `schema-design-spec.md`
- Completion/kernel boundary: `layered-desc-arch.md`
- Validation effects: `descriptor-semantics-rules.md`
- TDL omission behavior: `tdl-spec.md`
- Other documents: short summaries with links

### Value and relationship constraints

The constraint specs mix several concerns:

- Schema vocabulary
- Descriptor validity
- Effective inheritance
- Instance validation
- Runtime interfaces
- Persistence representation
- Implementation sequencing

The schema vocabulary and semantic rules belong in `type-system/`. Runtime execution belongs in validation or core runtime. Relationship occurrence storage belongs in transactions/storage.

### Runtime representation

`runtime-shared-types.md`, `descriptors-design-spec.md`, and `layered-desc-arch.md` all discuss `HolonReference`, typed wrappers, semantic access, and runtime projections.

General wrapper and reference-layer rules belong in `core-runtime/`. Descriptor documents should state only descriptor-specific behavior.

### Historical rationale

`schema-2.0.md` combines current design, rejected alternatives, migration comparisons, and final rules. This makes it valuable as rationale but inefficient as an authoritative spec.

Its current rules should be distilled into `schema-design-spec.md`; the full proposal should then be archived as design history.

## 6. Structural Reclassification

The following is the recommended target placement, pending Phase 2 confirmation.

| Current document | Target area |
|---|---|
| `type-system/map-type-system.md` | `type-system/` |
| `type-system/schema-2.0.md` | Distill to `type-system/schema-design-spec.md`; archive original |
| `type-system/tdl/tdl-spec.md` | `type-system/tdl/` |
| `type-system/tdl/tdl-impl-plan-v2.md` | `type-system/tdl/` or implementation-plan area |
| `type-system/runtime-shared-types.md` | `core-runtime/` |
| `type-system/schema-v2-pressure-test-checklist.md` | Archive; later replacement under type-system testing/governance |
| `type-system/map-schema-authoring-guide.md` | `type-system/guides/` |
| `type-system/meta-value-types-import-guide.md` | Archive or rewrite |
| `descriptors/descriptor-semantics-rules.md` | `type-system/` |
| `descriptors/descriptors-design-spec.md` | `core-runtime/descriptors/` |
| `descriptors/layered-desc-arch.md` | `core-runtime/descriptors/` |
| `descriptors/value-constraints-design-spec.md` | `type-system/` |
| `descriptors/relationship-constraints-design-spec.md` | Primarily `type-system/`, with non-schema material split out |
| `descriptors/relationship-persistence-design-spec.md` | `transactions/` or storage |
| `descriptors/schema-ripple-design-spec.md` | `type-system/` tooling/governance |
| `descriptors/adaptive-schema-usage.md` | `adaptive-systems/` |
| `descriptors/adaptive-usage-capture.md` | `adaptive-systems/` |
| `descriptors/background-usage-transactions.md` | `adaptive-systems/` |

Moving the adaptive documents is a structural change only. Their treatment of third-party Extension Schemas and cross-schema adaptation must be preserved during later reconciliation.

## 7. Missing Authoritative Documents

The target architecture exposes several gaps.

### `schema-design-spec.md`

A concise current-state structural specification is missing. It should define:

- Descriptor categories and structural relationships
- `DescribedBy`, `Extends`, and `Instances`
- Meta-types, abstract types, and concrete types
- Declaration surfaces
- Key-rule attachment
- Constraint attachment
- Default validity
- Extension-schema participation
- Structural invariants and boundaries

It should not duplicate descriptor evaluation algorithms or enumerate the full Core Schema.

### `extension-schema-design.md`

Extension Schemas need an explicit type-system specification covering:

- Extension of MAP Core and other extenders’ schemas
- Cross-schema ownership and identity
- Legal extension relationships
- Version and dependency semantics
- Compatibility and conflict rules
- What remains universally valid versus application- or adaptive-system-specific

The adaptive-system documents should consume this specification rather than becoming the sole source of extension-schema semantics.

### `schema-catalog.md`

A catalog is needed to map logical schemas and owning components to their centralized TDL files.

The current corpus contains mutual dependencies:

- MAP Core depends on Key Rule, Dance, and Query schemas.
- Key Rule depends on MAP Core.
- Dance depends on MAP Core and Key Rule.
- Query depends on MAP Core and Dance.

The catalog must therefore describe a multi-pass-loaded corpus, not assume that schema dependencies form a simple DAG.

### Core-runtime overview

The agreed `core-runtime/` section does not yet have a concise architectural entry point establishing:

- Holon and reference-layer representations
- Typed wrapper conventions
- Saved, staged, and transient states
- Projection boundaries
- Descriptor runtime as a subsystem
- Relationships with storage and transactions

## 8. Documents Requiring Special Handling

### Adaptive-system documents

The prior revisions were rolled back because they flattened the extension-schema problem. Phase 2 should initially move these documents without semantic rewriting.

Any Schema 2.0 corrections should be proposed as small, traceable changes and reviewed against the intended extension-schema model.

### Descriptor master design

The current facade-oriented version should not be patched into shape section by section.

The replacement should be reconstructed from:

- The accepted architectural baseline
- `descriptor-semantics-rules.md`
- `layered-desc-arch.md`
- Relevant material from `archive/descriptors-design-spec-v1.3.md`
- The generic runtime-wrapper rules eventually owned by `core-runtime/`

Its purpose should be to define the descriptor runtime subsystem, delegate specialized semantics, and establish boundaries with creation, validation, storage, and other components.

### Relationship persistence

`relationship-persistence-design-spec.md` is newly added and has not yet earned authoritative status. Its claims should be reviewed against the transaction and storage designs before it is retained and relocated.

### Current working-tree provenance

Several audited documents contain uncommitted edits from earlier iterations. Phase 2 must not treat every current modification as an accepted decision.

In particular:

- The facade-oriented descriptor spec has been explicitly challenged.
- The two adaptive documents were restored by the user.
- `background-usage-transactions.md` still contains working-tree changes requiring review.
- The new relationship persistence spec is unreviewed.
- `mkdocs-core.yml` reflects an intermediate structure.

## 9. Phase 1 Conclusions

The current document set is not yet consistent, concise, DRY, or reliably authoritative.

The most serious issues are:

1. Active contradictions with the Schema 2.0 TDL corpus.
2. No concise current schema design authority.
3. Excessive duplication of inheritance, conformance, defaults, and cardinality rules.
4. A descriptor master spec organized around an inappropriate runtime-facade abstraction.
5. Structural placement that obscures ownership.
6. Archived and deferred designs still presented in active navigation.
7. Adaptive-system concerns mixed into the descriptor runtime section.
8. Guides and checklists that encode superseded schema generations.

The strongest current foundation is:

- The Core Schema TDL corpus as exact schema authority.
- `descriptor-semantics-rules.md` as the semantic baseline.
- The accepted portions of `layered-desc-arch.md` defining explicit holon representation, completion, and kernel boundaries.
- `tdl-spec.md` for source-language behavior.
- `schema-2.0.md` as rich source material to be distilled, rather than retained in its current proposal-style form.

## 10. Recommended Phase 2 Order

1. Establish the target directories and document-role manifest.
2. Create `schema-design-spec.md` by distilling current structural rules from `schema-2.0.md`.
3. Move `descriptor-semantics-rules.md` into the type-system authority set.
4. Reconstruct the descriptor master design under `core-runtime/descriptors/`.
5. Tighten `layered-desc-arch.md` around construction, completion, representation, and kernel invocation.
6. Move runtime shared types into `core-runtime/` and reconcile obsolete terminology.
7. Move adaptive documents intact into `adaptive-systems/`.
8. Define `extension-schema-design.md` before semantically revising the adaptive documents.
9. Split or relocate constraint, persistence, and schema-ripple documents according to ownership.
10. Compress `map-type-system.md` into an overview that delegates normative detail.
11. Archive or replace obsolete guides and the pressure-test checklist.
12. Update `mkdocs-core.yml` only after the new authority structure and paths are stable.
13. Reconcile `tdl-impl-plan-v2.md` against the resulting authoritative spec set.
