# Collection VisualizerKind

## Status and authority

Draft normative specification for this kind's semantic subject and common
participation boundary. Concrete Visualizer grammar remains with the selected
implementation's specification. Shared runtime, selection, and allocation
mechanisms remain with the DAHN design specification.

## Semantic subject and classification

A homogeneous collection of Holons or values sharing an effective element
shape. Arrays, plural relationship results, Dance results, and other
collection-producing operations may supply this subject. Its provenance
remains available as context but does not require a provenance-specific renderer.

Homogeneity concerns the effective element shape understood by the Visualizer;
it does not turn a set of subjects unified by an organizing topology into a
Collection. That semantic case belongs to Structure.

A VisualizerKind classifies Visualizers by the semantic shape of their subject.
It does not identify a particular owner-defined VisualizerSlot, spatial region,
or concrete presentation implementation.

## Common promises and slot boundaries

A composition owner
specifies its actual slot contract, subject binding, context, and participation
constraints in its own specification. Kind membership alone does not establish
conformance to every slot requesting that kind.

Selection and runtime realization follow the
[DAHN composition and selection model](../../dahn-design-spec.md).
The selected Visualizer fulfills the slot contract; VisualizerUsage records
agent-relative use and configuration.

## Applicability and presentation freedom

Member type, source affordance, schema, cardinality, available projected columns,
context, and agent preferences may inform selection through the supplied slot.
An empty collection still has its descriptor-defined element shape.

A concrete Collection Visualizer may use table, list, gallery, or other
presentations. No universal contract requires rows, columns, sorting, placement
beneath a Node, or a particular navigation axis. Mutation permissions continue
to depend on the underlying array, relationship, or Dance-result semantics;
presentation does not make all collections equally editable.

## Family

- [Table Collection](table/design-spec.md)

## Authority boundary

Concrete layouts, child slot arrangements, gestures, and rendering strategies
belong to individual Visualizer specifications. No concrete family's internal
composition is made a universal requirement by this directory hierarchy.


## Mutation semantics and ownership

### Editable collections

A Collection Visualizer MAY become editable when it represents staged state semantically owned by the holon being edited.

The same visualizer is used for inspection and editing.

Editing adds mutation affordances rather than replacing the collection with a separate form.

### Value arrays

For an editable array-valued property, the Collection Visualizer MAY support:

- add value;
- remove value;
- edit value;
- reorder values where ordering is semantically meaningful and permitted.

Individual values continue to delegate editing to their applicable Value Visualizers.

Changes update Rust-owned staged state.

### Plural relationships

For a mutable plural relationship, the Collection Visualizer MAY support:

- add target;
- remove target;
- reorder targets where allowed.

Target selection MAY initially use the simplest generic selection mechanism available.

Relationship membership editing changes the source holon's staged relationship state.

### Dance results

A collection-valued dance result is not inherently editable merely because it is shown through a Collection Visualizer.

Editability depends on:

- semantic ownership;
- available mutation affordances;
- descriptors;
- permissions.


Presentation order and semantic sequence are distinct. Sorting a view does not
mutate membership or stored sequence. Editing a relationship’s membership does
not edit the target Holon; editing that target requires its own staged context.
MAP/Rust remains authoritative for staged data and permitted mutations.


## Projected Collection input

A Collection slot may explicitly admit a typed value projection in addition to
an ordinary member-backed collection. The declared element descriptor supplies
selection shape; the actual projected rows supply displayed membership. This is
an existing reusable SDK/runtime adaptation, not an intrinsic requirement on
every Collection Visualizer and not a loader-only semantic collection type.

The current adapter submits an empty member envelope as a declared element-type
witness to ordinary Rust Collection selection, then supplies actual projected
rows separately. Empty witness membership MUST NOT be interpreted as zero display
rows, zero diagnostics, or an authoritative member count. Projection rows retain
stable identities within the retained view across sorting, hiding, and refresh;
actual subject handles are a separate owner-bound activation mapping, not value
columns, guessed keys, or reconstructed semantic references.

The selected implementation must support the declared projected input. A
materialized implementation without that support produces an explicit presentation
failure; it is not replaced with Table or another client-selected renderer. The
slot's input participation and runtime admission check must make this boundary
explicit. The adapter's row/column projection format is a supported input form,
not a universal layout prescription; another capable implementation may render
it differently. Real member-backed collections retain their ordinary membership
semantics and must not be confused with type-witness envelopes.

Rust owns selection; the projection owner owns values, stable identities, actual
handle mapping, and lifetime. Materialization may use a distinct open context from
the semantic subjects. Subject reads continue through their original bound handles.
