# Layered Descriptor Architecture (Schema 2.0)

## 1. Purpose and authority

This document defines how concrete-syntax parsing, Holon Loading, best-effort default
population, descriptor semantics, validation, and Commit fit together for Schema 2.0.
Construction assists initialization; validation decides acceptance of the resulting explicit state.

Authority is delegated by concern:

- [`schema-design-spec.md`](../type-system/schema-design-spec.md) defines schema structure and
  invariants.
- [`descriptor-semantics-rules.md`](../type-system/descriptor-semantics-rules.md) defines Schema 2.0
  descriptor-semantic algorithms and conformance rules.
- [Runtime Descriptor Subsystem Design Spec](../core-runtime/descriptors/descriptors-design-spec.md)
  defines the runtime descriptor surface.
- [MAP Validation Architecture](../validation/validation-arch.md) defines descriptor-driven Holon
  Validation.
- [PVL Design Specification](../validation/pvl-design-spec.md) defines descriptor-independent
  Integrity Zome validation.
- [`tdl-spec.md`](../type-system/tdl/tdl-spec.md) defines TDL syntax and lowering.

This document defines component boundaries and invocation order. It does not restate the delegated
semantics.

## 2. Architectural decisions

The target architecture follows these decisions:

1. MAP JSON and TDL are concrete syntaxes over the same `LoaderRefRep` representation.
2. `LoaderRefRep` is the actual transient, schema-backed loader holon graph shared by host and
   guest. It is not a parallel DTO model.
3. The existing Holons Core shared-object and Reference Layer representation is the runtime
   holonic representation on which descriptor semantics operate.
4. No separate Semantic IR, canonical descriptor model, or graph-adapter representation is
   required.
5. The existing Holon Loader client and guest components orchestrate Holon Loading. TDL introduces
   another parser, not another loader.
6. The shared writable-reference operation attempts applicable defaults during descriptor
   attachment, construction, staging, and cloning. Holon Loading retains a final default-population
   and enum-materialization pass after reference resolution; see §6.
7. Commit invokes the reusable Holon Validator before persistence. Commit validates but does not
   supply defaults or otherwise mutate staged holons.
8. Descriptor-independent PVL remains a separate Integrity Zome validation level.

## 3. End-to-end flows

### 3.1 Source conversion

Source conversion remains entirely on the host:

```text
TDL ------> TDL Parser ----+
                           +--> LoaderRefRep --> MAP JSON
MAP JSON -> JSON Parser ---+                 --> canonical TDL
```

Source conversion does not require guest submission, default population,
descriptor-driven Holon Validation, or persistence.

### 3.2 Holon Loading

Loading either syntax follows the existing Holon Data Loader path:

```text
MAP JSON or TDL
        |
        v
Concrete-Syntax Parser
    - parse syntax
    - expand syntax-specific shorthand
    - preserve authored values, omissions, keys, and provenance
    - produce LoaderRefRep
        |
        v
Holon Loader Client
    - serialize LoaderRefRep through the normal holon transport
    - submit the loader dance request
        |
        v
Guest Holon Loader
    - stage application holons and authored properties
    - resolve DescribedBy and Extends
    - resolve remaining keyed references
    - produce the fully resolved staged application graph
        |
        v
Descriptor-Default Materialization Service
    - inspect effective PropertyDescriptors
    - write applicable defaults for omitted properties
        |
        v
Commit
    - invoke the reusable Holon Validator
    - persist nothing when blocking violations remain
    - persist the transaction only when validation succeeds
        |
        v
Saved Holon Graph
```

## 4. Representation boundaries

### 4.1 Concrete syntax

TDL syntax trees and parsed MAP JSON are source representations. They may retain formatting,
comments, source spans, shorthand, and other authoring details. They do not own descriptor
semantics.

### 4.2 LoaderRefRep

`LoaderRefRep` is the transient loader holon graph rooted at `HolonLoadSet`. It includes the Core
Schema loader types:

- `HolonLoadSet`;
- `HolonLoaderBundle`;
- `LoaderHolon`;
- `LoaderRelationshipReference`; and
- `LoaderHolonReference`.

Host and guest use this same holonic representation. Authored relationship references remain keyed
because their target IDs may not yet exist. `LoaderRefRep` preserves omissions so the guest can
apply the loader's descriptor-default policy after descriptor binding.

Although `LoaderRefRep` consists of holons, it is a loading and unresolved-reference
representation. It is not the staged application graph validated for commit and does not own
inheritance, effective-specification, or conformance behavior.

### 4.3 Runtime holonic representation

Guest construction resolves `LoaderRefRep` into ordinary application holons and relationships.
`TransientHolon`, `StagedHolon`, and `SavedHolon` are lifecycle states of this same representation,
read through `HolonReference` and the Reference Layer.

Descriptor semantics operate directly on this representation through `HolonDescriptor`, typed
descriptor wrappers, and existing descriptor helpers. No copied semantic graph or graph-access
adapter sits between them.

### 4.4 Derived tooling state

Source indexes, provenance maps, comparison signatures, and editor projections may be derived for
bounded tooling purposes. They are not mutable semantic authorities and must not reimplement
descriptor semantics.

## 5. Parsing and reference resolution

Each concrete-syntax parser produces `LoaderRefRep`.

A parser owns:

- concrete grammar and syntax diagnostics;
- syntax-specific shorthand expansion;
- lowering authored properties and relationships into loader holons;
- copying authored reference keys into `LoaderHolonReference`s; and
- retaining source provenance required for diagnostics.

A parser does not resolve loader keys to holon IDs, construct the staged application graph,
populate defaults, or perform descriptor-driven validation.

The existing guest `LoaderReferenceResolution` owns keyed-reference resolution against both the
current load and previously saved holons. Loader assembly proceeds in this order:

1. Stage target application holons and authored properties.
2. Resolve `DescribedBy` through `with_descriptor()`, which may populate some defaults against
   a partially assembled contract.
3. Resolve `Extends`.
4. Resolve all remaining authored relationships.
5. Run the final default-population and enum-materialization pass: normalize enum defaults,
   attempt defaults on each staged holon, then materialize its enum properties.

Early attempts do not replace the final pass, which also converts enum tokens copied during
attachment to their native representation before Commit validation.

## 6. Best-effort default population

`WritableHolon::populate_defaults() -> Result<(), HolonError>` is shared construction assistance.
`with_descriptor()` attempts it after successful attachment and release of attachment locks.
`TransientHolonManager` and `Nursery` retain construction, staging, and clone attempts because
these paths can receive an existing descriptor. The loader's final pass is authoritative for loads.

Direct `DescribedBy` authoring through `add_related_holons()` does not itself attempt defaults.
This supports internal assembly and tests needing attachment without population. Normal creation
seeking descriptor-assisted initialization uses `with_descriptor()`. Later staging, cloning,
an explicit `populate_defaults()` call, or the loader's final pass may still populate values.

Attempts establish neither completeness nor validity. Skipped properties are not recorded;
there is no preparation state, scheduled retry, or separate Commit gate. Default attempts never
mark a subject `Validated` or `Invalid`; Commit freshly assesses every live candidate.

For each holon, population:

1. Resolves its describing type as a `HolonDescriptor`.
2. Obtains effective declarations through `HolonDescriptor::instance_properties()`.
3. Preserves every existing property value, including earlier populated defaults.
4. For an absent required property, reads the effective `PropertyDescriptor::default_value()`.
5. Writes an available default through ordinary property mutation, preserving staged lifecycle
   and versioning accounting. Optional properties and required properties without defaults stay
   absent, consistent with `DS-DEFAULT-001`.

Population is idempotent over unchanged inputs. A later explicit attempt can reconsider omissions,
including refilling a removed property. Already populated defaults remain explicit if the descriptor
changes; validation assesses their conformance without replacing them with newer defaults. Cloning
and staging preserve persisted source content.

### Error contract

- Attachment failure is returned without attempting defaults.
- `MissingDescribedBy` on the subject makes population a no-op success. The same error while
  assessing a property skips that property and continues independent work. No finding is created.
- Every other descriptor-read or property-write error propagates immediately, fail-fast per holon.
  The descriptor may already be attached and earlier defaults written; these changes are not
  rolled back. Callers handle the operational error. The loader collects provenance-carrying
  errors across holons; any loader completion error prevents Commit.

Commit assesses actual explicit state and never supplies defaults. Missing required values are
validation findings; reads and restoration do not populate defaults either. Interactive creation
may present a default for confirmation before writing it explicitly.

## 7. Descriptor semantics and runtime access

`HolonDescriptor` is the runtime descriptor facade. Ordinary holons reach it through
`ReadableHolon::holon_descriptor()`. Typed descriptor wrappers expose narrower schema-backed
operations.

Effective operations use `HolonDescriptor` and existing descriptor helpers to implement the
descriptor-kernel rules, including effective contracts, inheritance, subtype classification,
endpoint compatibility, key rules, and conformance predicates. The wrapped `HolonReference`
remains an implementation detail; consumers must not bypass descriptor accessors to create
independent semantic traversals.

The descriptor kernel is a logical ownership boundary for the pure algorithms defined by
`descriptor-semantics-rules.md`; it is not a second representation or a required standalone crate.
Kernel operations compute and validate. They do not parse syntax, resolve loader references,
populate defaults, manage transactions, or persist holons.

For each immutable graph snapshot, kernel invocation first computes and memoizes effective
products by product kind and resolved descriptor identity, then validates holons against those
products. Product computation never recursively validates the descriptor whose specification is
being computed. A self-describing descriptor therefore selects an already computed effective
specification rather than creating unbounded semantic recursion. Any graph mutation, including
default population, invalidates affected products before final validation.

`DescribedBy` has no transitive-closure semantic and therefore has no convergence or unique-cycle
rule. A descriptor may be self-describing when it satisfies the same describing-type compatibility
and conformance rules as every other descriptor. `Extends` remains acyclic. Schema dependency
closure and other descriptor-permitted relationship graphs use identity-based visited sets where
their own semantics require traversal. The versioned schema `DependsOn` graph is itself acyclic;
multi-pass loading resolves circular references only among components owned by the same schema.

## 8. Validation and commit

The Holon Validator is the reusable entry point for descriptor-driven validation of ordinary and
descriptor holons. It owns validation scope, context, rule coordination, result accumulation, and
reporting. It delegates Schema 2.0 semantic predicates and conformance algorithms to the descriptor
kernel through the runtime descriptor surface rather than reimplementing them.

The Holon Validator is callable outside Holon Loading. For persistence, commit must invoke it over
the staged transaction before writing any state.

Validation accumulates all independently discoverable violations. Fatal reference access or
infrastructure failures may stop validation when further results would be unreliable. Commit
persists nothing when any blocking violation or fatal validation failure remains.

Commit does not:

- construct or resolve the graph;
- populate defaults;
- repair invalid state; or
- weaken validation based on source syntax.

PVL is separate. Holochain triggers descriptor-independent PVL through Integrity Zome callbacks.
PVL does not resolve descriptors, invoke `HolonDescriptor`, or execute descriptor-kernel semantics.

## 9. Diagnostics and provenance

Diagnostics retain their owning boundary:

| Diagnostic | Owner |
| --- | --- |
| Malformed syntax or lowering failure | Concrete-syntax parser |
| Duplicate loader key or unresolved keyed reference | Guest Holon Loader |
| Failure to determine or apply a declared default | Shared writable-reference default population |
| Descriptor-driven holon violation | Holon Validator |
| Descriptor-independent DHT admissibility failure | PVL |

Parser and loader provenance may enrich guest errors with filenames and source offsets. Provenance
does not affect holon identity or semantic equality.

## 10. Ownership summary

| Concern | Owner |
| --- | --- |
| TDL grammar and shorthand | TDL parser |
| MAP JSON grammar and loader metadata | JSON parser / loader client |
| `LoaderRefRep` schema and transport | Holon Data Loader |
| Keyed-reference resolution | Guest Holon Loader |
| Runtime holonic state | Holons Core shared objects and Reference Layer |
| Runtime descriptor access | `HolonDescriptor` and typed descriptor wrappers |
| Schema 2.0 semantic algorithms | Descriptor kernel implemented through runtime descriptor helpers |
| Best-effort default population | Shared writable-reference operation used by attachment, construction, staging, cloning, and the loader's final pass (§6) |
| Descriptor-driven validation orchestration | Holon Validator / validation framework |
| Commit validation invocation and persistence atomicity | Transaction commit |
| Descriptor-independent Integrity validation | PVL |
| TDL/JSON source projection and fidelity | Source tooling over `LoaderRefRep` |

## 11. Excluded and deferred concerns

The target architecture excludes the retired `SemanticModel`, Canonical Holon IR, loader DTO IR,
and graph-adapter designs. Migration code may remain temporarily, but new descriptor semantics,
completion, or validation behavior must not be added to it.

The following are deferred without changing these boundaries:

- interactive default-confirmation workflows;
- effective-surface caching behind `HolonDescriptor`;
- editor handling of syntactically invalid partial documents;
- migration of persisted Schema 1.2 data; and
- code-generation projections.
