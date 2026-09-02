# Layered Descriptor Architecture (Schema 2.0)

## 1. Purpose and authority

This document defines how concrete-syntax parsing, Holon Loading, descriptor-default
completion, descriptor semantics, validation, and commit fit together for Schema 2.0. Initial
construction, deferred default completion, validation, and Commit are separate stages.

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
6. Applicable descriptor-defined defaults are populated by the shared objects layer
   (`core_shared_objects`) when a holon is created or independently cloned, once its governing
   descriptor can be resolved. Holon Loading runs the same completion operation as a bootstrap
   backstop after reference resolution.
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

Source conversion does not require guest submission, descriptor-default completion,
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
complete defaults, or perform descriptor-driven validation.

The existing guest `LoaderReferenceResolution` owns keyed-reference resolution against both the
current load and previously saved holons. Guest construction completes in this order:

1. Stage target application holons and authored properties.
2. Resolve `DescribedBy`.
3. Resolve `Extends`.
4. Resolve all remaining authored relationships.
5. Rerun default completion over the fully resolved staged graph.

Resolving `DescribedBy` alone is not permission to begin completion while other authored
references remain unresolved.

## 6. Descriptor-default completion

Default completion is a shared objects layer concern owned by `core_shared_objects`. The
`TransientHolonManager` and `Nursery` attempt it whenever they create or independently clone a
holon, and the Holon Loader reruns the same operation over its resolved staged graph as a
bootstrap backstop:

```text
populate_defaults(holon)
```

Attempting completion before the governing descriptor can be resolved is a non-fatal deferred
outcome, not a construction failure. Construction never invents a default and never fails
bootstrap solely because a descriptor was unavailable; the loader's completion pass closes that
gap once references resolve. Every non-loader producer that permits omission must invoke the same
completion operation before Commit.

Cloning must not alter historical persisted state. Completion may populate only properties omitted
from the newly created staged clone, under the descriptor governing that clone.

For each staged holon, completion:

1. Resolves its describing type as a `HolonDescriptor`.
2. Obtains effective declarations through `HolonDescriptor::instance_properties()`.
3. Reads each declaration's optional default through
   `PropertyDescriptor::default_value()`.
4. Preserves every explicitly supplied property value.
5. Writes the declared default when the corresponding property is omitted.
6. Leaves an omission without an applicable default absent for the Holon Validator to assess.

Completion does not implement inheritance traversal, replace explicit values, invent defaults,
validate missing required properties, or apply defaults lazily during reads.

Completion is idempotent. Once written, a default is ordinary explicit property state. A producer
may retain ephemeral authored-versus-completed provenance for diagnostics, but commit persists no
such marker. Later changes to a descriptor default do not alter saved holons.

Completion accumulates independent errors where practical. A completion error means failure to
determine or apply a declared default, not ordinary absence of a required value and not a deferred
outcome awaiting descriptor resolution. Any completion error prevents commit from being called.
Successful writes need not be individually reverted; they remain in the uncommitted staged graph
for diagnostics until the producer abandons or rolls back the failed transaction.

Interactive creation may instead display a descriptor default for human confirmation and write the
confirmed value explicitly. Commit requires completed explicit state: Commit and the Holon
Validator never supply defaults.

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
complete defaults, manage transactions, or persist holons.

For each immutable graph snapshot, kernel invocation first computes and memoizes effective
products by product kind and resolved descriptor identity, then validates holons against those
products. Product computation never recursively validates the descriptor whose specification is
being computed. A self-describing descriptor therefore selects an already computed effective
specification rather than creating unbounded semantic recursion. Any graph mutation, including
default completion, invalidates affected products before final validation.

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
- complete defaults;
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
| Failure to determine or apply a declared default | Shared objects layer default completion |
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
| Descriptor-default completion | `core_shared_objects` construction and clone paths, with the loader completion pass as bootstrap backstop |
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
