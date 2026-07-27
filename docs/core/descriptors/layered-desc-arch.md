# Layered Descriptor Architecture (Schema 2.0)

## Architectural intent

This architecture establishes a format-neutral path for holon creation, schema authoring, semantic completion, and validation:

    Authored, imported, migrated, bootstrap, or programmatic input
      -> creation adapter
      -> Canonical Holon IR
      -> symbol resolution
      -> descriptor-driven completion using kernel contract resolution
      -> explicit Canonical Holon IR
      -> descriptor-kernel validation
      -> semantic diagnostics
      -> output adapter
      -> loader-facing JSON

The central principle is that schema meaning is defined by descriptor data and shared descriptor semantics, not by TDL-specific rules, JSON-specific rules, programmatic construction conventions, or hard-coded checks for individual Core Schema properties.

Every creation path must pass through descriptor-driven completion before descriptor-kernel validation. The completion stage calls the kernel's read-only contract-resolution operations to determine which values are required and which defaults apply, then produces an explicit representation. The descriptor kernel computes semantics for both completion and validation but does not materialize defaults or otherwise mutate that representation.

This supports multiple creation paths and output formats without contaminating the Canonical Holon IR or semantic kernel with adapter-specific behavior.

## 1. Creation adapters and completion stages

Examples:

- TDL compiler
- JSON import adapter
- Schema bootstrap loader
- Programmatic builder
- Migration tooling
- Runtime holon-creation API
- Future authoring or import formats

### Responsibilities

- Parse concrete source syntax when applicable.
- Report syntax and source-shape errors using source-specific locations when applicable.
- Interpret source-specific keywords, shorthand, and omission conventions.
- Resolve identities and references through the shared symbol-resolution layer.
- Determine omitted property values from the effective descriptor contract.
- Materialize a descriptor-defined default only for an omitted required property.
- Materialize required semantic control values, including the Schema 2.0 default `InheritanceMode.None`, before kernel validation.
- Report a missing-required-property violation when no explicit value or valid default exists.
- Preserve source origin information for later diagnostics.
- Produce an explicit Canonical Holon IR for descriptor-kernel validation.

### TDL-specific responsibilities

TDL lowering expands TDL syntax and shorthand into canonical semantic data. Examples include:

- Type keywords materialize the appropriate `TypeKind`, kind-specific `DescribedBy`, and default descriptor-type `Extends` relationships.
- The `abstract` keyword materializes `is_abstract_type: true`.
- Optional property syntax using the `?` suffix materializes the appropriate property-requiredness value.
- Relationship shorthand materializes explicit cardinality and deletion-semantic values.
- Bootstrap syntax conveniences are expanded into ordinary canonical relationships and properties.

An omitted Boolean does not generically become `false`. It remains absent when optional, receives `false` only when the effective required property declaration defines that default, and otherwise produces a missing-required-property violation.

These are pre-kernel transformations, not exceptions in semantic validation.

### JSON-specific responsibilities

The JSON adapter faithfully lowers authored JSON into Canonical Holon IR while preserving the distinction between explicit values and omissions.

It must not inject TDL-specific conveniences. It must, however, participate in the same descriptor-driven completion stage as every other creation path. Equivalent JSON and TDL inputs interpreted against the same schema version must produce equivalent explicit semantic representations.

### Explicit non-responsibilities

Creation adapters and completion stages do not define shared schema semantics. They must not:

- Reimplement inheritance traversal.
- Hard-code Core Schema property values such as legal `TypeKind` variants.
- Relax semantic requirements based on source format.
- Add source-specific exceptions to shared conformance rules.
- Project directly into another source or output format while bypassing Canonical Holon IR.
- Treat omission as a read-time fallback after creation.

## 2. Canonical Holon IR

Location: `shared_crates/map_schema_semantic`

The Canonical Holon IR is the source-neutral semantic representation shared by all schema adapters.

### Responsibilities

- Represent schemas, descriptor holons, properties, relationships, and references without dependence on TDL or loader JSON syntax.
- Preserve descriptor identity and relationship-target multiplicity.
- Preserve explicit literal values supplied by the source adapter.
- Preserve values materialized by the completion stage as explicit state.
- Preserve source-origin metadata for diagnostics.
- Carry unresolved and resolved semantic references.
- Provide a stable input for symbol resolution, validation, semantic comparison, and output projection.

### Explicit non-responsibilities

The IR does not:

- Define or apply source-specific omission conventions.
- Recover defaults as read-time fallbacks.
- Know how JSON fields are encoded.
- Own inheritance or conformance algorithms.
- Contain loader reference types.
- Depend on runtime `HolonReference` objects.
- Contain adapter-specific validation policy.
- Normalize away source information needed for semantic diff or diagnostics.

The IR represents semantic data; it does not define the meaning of that data.

## 3. Symbol indexing and reference resolution

Location: `map_schema_semantic::schema_index`

### Responsibilities

- Build a global symbol table over the Canonical Holon IR.
- Resolve references across files and schema dependencies.
- Detect duplicate symbols.
- Detect unresolved references.
- Detect references to descriptors of an incompatible expected category when that category is structurally known.
- Preserve authored target text for useful diagnostics.

### Explicit non-responsibilities

Symbol resolution does not:

- Decide inheritance semantics.
- Validate descriptor conformance.
- Generate loader references.
- Infer missing source data.
- Hard-code the members of schema-defined enums.

Its concern is identity and reference resolution, not the validity of the resolved holons.

## 4. Descriptor-semantics kernel

Location: `shared_crates/descriptor_semantics`

The kernel is the representation-neutral definition of descriptor semantics shared by Canonical Holon IR and runtime holons.

### Responsibilities

- Traverse `Extends` chains self-first.
- Detect multiple `Extends` parents.
- Detect inheritance cycles using node identity.
- Resolve the exactly-one `DescribedBy` relationship required by semantic validity.
- Compute `SubtypeOf` through reflexive-transitive `Extends`.
- Recognize admissible describing types under either `TypeDescriptor` or `MetaTypeDescriptor` without merging those hierarchies.
- Compute additive `EffectiveInstanceContract` values from local `InstanceProperties` and `InstanceRelationships` declarations.
- Reject local redeclaration of an inherited contract-member identity.
- Reject distinct contract-member identities that claim the same semantic member name.
- Compute `ConformanceContract(H)` from the effective instance contract of `H`'s describing type.
- Resolve populated descriptor values according to the member descriptor's materialized `InheritanceMode`.
- Apply `None`, `Additive`, and `Override` resolution.
- Deduplicate additive effective values by their defined identity or equality rule while preserving all contribution provenance.
- Preserve selected and shadowed contribution provenance under `Override`.
- Evaluate cardinality and applicable constraints against effective values.
- Reject `DefaultValue` on an optional property, and validate each permitted default against the same value constraints as the required property it defaults; either failure is an error on the property descriptor.
- Resolve effective instance key rules.
- Resolve the key rule governing a descriptor holon itself.
- Evaluate representation-neutral property and relationship conformance.
- Derive primitive value policy from descriptor data.
- Evaluate string-length constraints in Unicode grapheme clusters.
- Return neutral semantic violations and graph errors.

### Separate resolution axes

Schema 2.0 does not define one flattened effective lineage.

For any holon `H`:

    ConformanceContract(H)
        =
    EffectiveInstanceContract(DescribingType(H))

This governs the populated properties and relationships that `H` itself must contain.

For any type `T`:

    EffectiveInstanceContract(T)

governs the contract that `T` passes on to the instances it describes. If `T` has parent `P`, it is the additive accumulation:

    EffectiveInstanceContract(T)
        =
    EffectiveInstanceContract(P)
        union
    LocalInstanceContract(T)

Instance-contract inheritance has no `Override` mode. Contract declarations are not set-deduplicated: redeclaration of an inherited member identity and collisions between distinct identities with the same semantic member name are errors.

For a descriptor holon, these two contracts are intentionally separate:

- `DescribedBy` determines descriptor self-conformance through the kind-specific meta-type hierarchy.
- The descriptor's own `Extends` lineage determines classification and the contract passed to described instances.

Meta-type declarations must not leak into ordinary instance contracts, and descriptor-type declarations must not be treated as the descriptor holon's self-conformance contract.

Populated descriptor state is a third concern. For a type `T` and member `M`, `EffectiveValues(T, M)` is resolved across `T`'s own `Extends` lineage according to `InheritanceMode(M)`:

- `None` returns only `LocalValues(T, M)`.
- `Additive` unions inherited and local values.
- `Override` returns the complete local value set from the nearest type in the self-first lineage that locally populates `M`.

`InheritanceMode` is required semantic data. Creation-time completion materializes its default value of `None`; kernel resolution never interprets an absent mode as `None`.

### Describing-type and endpoint admissibility

For a non-abstract describing type `T`, Schema 2.0 admissibility is:

    SubtypeOf(T, TypeDescriptor)
        or
    SubtypeOf(T, MetaTypeDescriptor)

The two roots remain separate; this test does not create inheritance or contract flow between them.

Relationship endpoint checks use the endpoint's semantic category:

- An ordinary holon target `H` satisfies a required type `R` when `SubtypeOf(DescribingType(H), R)`.
- A descriptor target `D` used as a type satisfies a required type `R` when `SubtypeOf(D, R)`.

### Authoring-state distinction

Every semantically valid holon requires exactly one `DescribedBy`.

Runtime or authoring code may inspect the local state of a partially assembled descriptor before that relationship has been attached.

It must not receive a partial effective contract, effective value set, or conformance result. Semantic operations invoke the exact-one-`DescribedBy` gate and fail on malformed or incomplete graph access.

### Key-rule semantics

A direct `T.UsesKeyRule` defines how keys are generated for instances described by `T`.

`UsesKeyRule.DeclaredRelationshipType` declares `InheritanceMode Override`.

For any type `T`:

    instance_key_rule(T)
        =
    the unique target in EffectiveValues(T, UsesKeyRule)

For any holon `H`, including a descriptor holon:

    holon_key_rule(H)
        =
    instance_key_rule(DescribingType(H))

The first step selects the describing type. The second applies ordinary `Override` resolution across that type's `Extends` lineage. Key-rule resolution does not perform an additional fallback through `DescribedBy`.

Keylessness is represented by an explicit `NoneKeyRule` target, not by the absence of `UsesKeyRule`.

This algorithm is defined once in the kernel and consumed by both schema tooling and runtime descriptor APIs.

### Explicit non-responsibilities

The kernel has no knowledge of:

- TDL syntax.
- JSON syntax.
- Filenames or line numbers.
- Loader import structures.
- Runtime transactions or storage.
- Bound runtime references.
- Diagnostic rendering.
- Core Schema property names except relationship/member kinds supplied by an adapter.
- Source-specific defaults or omissions.
- Mutation or completion of the explicit representation supplied for validation.

The kernel operates through a representation-neutral graph interface.

## 5. Representation graph adapters

Examples:

- `CanonicalDescriptorGraph` for Canonical Holon IR
- `HolonReferenceGraph` for runtime holons

### Responsibilities

- Expose representation-specific nodes through the kernel's `DescriptorGraph` interface.
- Supply node identity.
- Return local `Extends`, `DescribedBy`, contract-declaration, property, and relationship targets.
- Expose materialized member-descriptor values such as `InheritanceMode`.
- Identify the `TypeDescriptor` and `MetaTypeDescriptor` roots supplied by the bound schema.
- Expose abstractness and other descriptor-authored data required by kernel rules.
- Translate representation-access failures into kernel graph errors.
- Map kernel errors back into representation-appropriate errors or diagnostics.

### Explicit non-responsibilities

Graph adapters do not own alternative inheritance or conformance algorithms. They provide access to data; the kernel defines how that data composes.

## 6. Canonical descriptor conformance adapter

Location: `map_schema_semantic::descriptor_conformance`

This layer bridges Canonical Holon IR to the representation-neutral kernel.

### Responsibilities

- Enforce the exact-one-`DescribedBy` validity gate.
- Enforce non-abstract, two-root describing-type admissibility.
- Obtain `ConformanceContract(H)` from the kernel.
- Obtain `EffectiveInstanceContract(T)` where described-instance semantics are needed.
- Obtain `EffectiveValues(T, M)` for populated descriptor members.
- Convert canonical literal values into neutral conformance values.
- Read descriptor fields such as requiredness, cardinality, openness, and value type.
- Build kernel conformance inputs.
- Invoke shared conformance evaluation.
- Convert neutral violations into structured MAP diagnostics with source origins.

### Explicit non-responsibilities

This adapter must not:

- Reimplement inheritance.
- Add source-specific omission behavior.
- Materialize defaults during validation.
- Hard-code validation for named Core Schema properties.
- Maintain a second definition of effective contracts or effective values.
- Turn a collection of validation failures into one concatenated error string.

## 7. Semantic validation orchestration

Location: `map_schema_semantic::validator`

### Responsibilities

- Sequence model-wide validation passes.
- Run descriptor-driven conformance.
- Validate graph-wide invariants that require coordinated access to multiple descriptors.
- Validate separation of the meta-type and descriptor-type `Extends` hierarchies.
- Validate inverse relationship pairing.
- Validate required relationship-descriptor fields.
- Validate effective key generation using kernel-resolved key rules.
- Aggregate independent failures into a `Vec<Diagnostic>`.
- Preserve enough context to identify the offending holon, property, relationship, target, and source location.

Where a rule is already expressed by descriptor data, validation must derive the rule from those descriptors rather than restating it in Rust.

### Explicit non-responsibilities

The validator does not:

- Repair malformed source.
- Apply source-specific shorthand.
- Materialize descriptor defaults after kernel validation has begun.
- Hard-code enum variants such as `TypeKind.Holon`.
- Reimplement effective contracts, semantic inheritance, or subtype classification.
- Collapse multiple diagnostics into a single opaque error.

## 8. Semantic diff

Location: `tools/map-schema/src/lib.rs`

### Responsibilities

- Lower both inputs into Canonical Holon IR.
- Require diagnostic-free semantic inputs before comparison.
- Compare canonical semantic content independently of source syntax.
- Ignore non-semantic origin differences.
- Compare source residue locally where needed to detect information not represented in the typed semantic projection.
- Report meaningful differences in descriptors, properties, relationships, and preserved literal content.

Residue comparison remains local to the tooling layer. It does not expand the semantic meaning of the IR or add adapter concerns to `schema_ir.rs`.

## 9. Output adapters and projections

Example: Canonical Holon IR to loader JSON.

Locations:

- `tools/map-schema/src/schema_to_loader_ir.rs`
- Loader JSON renderer

### Responsibilities

- Project validated Canonical Holon IR into a concrete output representation.
- Choose output-specific reference encoding.
- Render loader document metadata.
- Preserve semantic identities and relationship targets.
- Produce deterministic, human-inspectable output.
- Reject or report semantic content that the target format cannot represent faithfully.

### Explicit non-responsibilities

Output adapters do not:

- Define schema validity.
- Complete omitted values or materialize defaults.
- Re-run a separate inheritance implementation.
- Modify semantic meaning to satisfy output-format constraints.
- Introduce loader types into Canonical Holon IR.

## 10. Holon Data Loader

The Holon Data Loader consumes loader JSON as holon data.

### Responsibilities

- Parse loader import documents.
- Lower imported JSON through the JSON creation adapter.
- Run descriptor-driven completion before descriptor-kernel validation when the input format permits omission.
- Validate the resulting explicit holons against the descriptors available in the loaded schema.
- Detect invalid property values, missing required fields, invalid relationships, unresolved targets, and other descriptor-prescribed errors.
- Stage and commit valid holons through the established transaction and reference layers.
- Return a `HolonReference` to a `HolonLoadResponse.DanceResponseType` holon.
- Return individual load failures through the multi-valued `HasLoadError` relationship to `HolonLoadError` holons.

### Explicit non-responsibilities

The loader does not:

- Parse TDL.
- Apply TDL conventions.
- Serve as the TDL semantic validator.
- Recover defaults as read-time fallbacks.
- Maintain loader-specific descriptor semantics.
- Receive concatenated schema-validation failures as a substitute for structured load errors.
- Act as the canonical schema IR for format conversion.

A TDL compiler validates TDL-derived schema semantics. The loader independently validates the resulting JSON as holon data using the same representation-neutral descriptor semantics. Both creation paths complete permitted omissions before kernel validation.

## 11. Runtime descriptor layer

Location: `shared_crates/holons_core/src/descriptors`

### Responsibilities

- Expose descriptor behavior over bound runtime `HolonReference` values.
- Delegate subtype classification, effective contract resolution, `InheritanceMode`-based effective values, duplicate handling, provenance, conformance, and key-rule resolution to the descriptor-semantics kernel.
- Convert kernel results into runtime descriptor wrappers and `HolonError` values.
- Retain runtime-only behavior involving bound references, transaction context, mutation state, and relationship navigation.

### Explicit non-responsibilities

The runtime descriptor layer must not maintain a divergent definition of semantics already owned by the kernel or expose one merged descriptor/conformance lineage.

Runtime-specific navigation remains in `holons_core`; representation-neutral rules belong in `descriptor_semantics`.

## 12. Diagnostics and error transport

### Compiler and semantic diagnostics

Compiler validation returns independent structured diagnostics.

Each diagnostic should identify, where available:

- Validation layer.
- Diagnostic kind.
- Holon or descriptor.
- Property or relationship.
- Offending value or target.
- Source file and location.

### Loader errors

Loader failures are domain data represented as `HolonLoadError` holons related to the `HolonLoadResponse`.

Compiler diagnostics and loader errors have different transports, but both preserve individual failures rather than combining them into an opaque string.

## 13. Validation ownership summary

| Concern                                                   | Owning layer                       |
|-----------------------------------------------------------|------------------------------------|
| TDL grammar                                               | TDL creation adapter               |
| TDL shorthand and omission conventions                    | TDL lowering                       |
| JSON parsing and faithful field preservation              | JSON creation adapter              |
| Descriptor-defined default materialization                | Pre-kernel completion stage        |
| Source-neutral schema representation                      | Canonical Holon IR                 |
| Symbol identity and reference resolution                  | Symbol index                       |
| `SubtypeOf` and describing-type admissibility             | Descriptor-semantics kernel        |
| Effective instance-contract resolution                    | Descriptor-semantics kernel        |
| `None`, `Additive`, and `Override` effective values        | Descriptor-semantics kernel        |
| Contract redeclaration and semantic-name collision errors | Descriptor-semantics kernel        |
| Effective-value duplicate handling and provenance         | Descriptor-semantics kernel        |
| Effective key-rule resolution                             | Descriptor-semantics kernel        |
| Neutral property and relationship conformance             | Descriptor-semantics kernel        |
| Canonical IR graph access                                 | Canonical descriptor graph adapter |
| Runtime holon graph access                                | Runtime descriptor graph adapter   |
| Diagnostic projection and aggregation                     | Semantic validation layer          |
| Canonical semantic comparison                             | Semantic diff tooling              |
| Loader JSON encoding                                      | Loader output adapter              |
| JSON holon validation and persistence                     | Holon Data Loader                  |
| Runtime descriptor navigation and mutation integration    | `holons_core` descriptor layer     |

## 14. Deferred semantic areas

Schema 2.0 defines no general `TypeKind` compatibility rule across `Extends`. `TypeKind` must not be used as a provisional substitute for hierarchy membership, `SubtypeOf`, or kind-specific `DescribedBy` conformance.

Advanced descriptor-driven value-constraint conformance beyond the established primitive, enum, cardinality, range, and grapheme-cluster string policies remains deferred where its semantics are not yet authoritative.

Initial kernel implementations may also defer enforcement of explicitly identified schema-authoring invariants, such as cross-hierarchy `Extends` prohibition, to bootstrap and schema-authoring tooling. Deferral of enforcement does not change the normative rule.

Deferred rules must not be replaced with provisional hard-coded heuristics. Once resolved, representation-neutral portions belong in the descriptor-semantics kernel and must be consumed through the existing graph adapters.
