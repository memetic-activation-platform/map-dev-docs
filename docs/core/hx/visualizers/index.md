# Visualizer Specification Families

## Organization and authority

VisualizerKind provides the organizational parent for Visualizers. It classifies
semantic subject shape; VisualizerSlot is a local composition boundary defined
by a Dancer or Visualizer. A slot's owner supplies its subject binding, required
contract, context, and participation constraints. A selected Visualizer fulfills
that contract and owns its internal experience.

Every Visualizer has one governing VisualizerKind, and every Slot declares one
required VisualizerKind using the same schema enum vocabulary. Kind agreement
provides the grounding linkage between them; the Slot's accepted types and other
participation requirements further constrain eligibility. This vocabulary plays
a role analogous to TypeKind in MAP's descriptor kernel. Its descriptor-level
kind-establishment mechanism is specified by the shared DAHN contract.

Kind specifications describe classification and established shared promises.
They are not substitutes for owner-defined slot contracts. A Visualizer that
fulfills multiple contracts still has one authoritative design specification,
referenced from other applicable families.

## Declarative composition and initial binding

A selected owner's effective Slot descriptors declare the required VisualizerKind,
subject bindings, activation rules, and participation contracts. Shared Rust
interprets those declarations and resolves concrete child Visualizers using
[DAHN prepared bindings and selection policy](../dahn-design-spec.md#145-recursive-selection).
Contributed Visualizers require no Visualizer-specific Rust selection callbacks.
Slots and owners do not prescribe concrete child defaults. Selected children
participate through their own declared composition in turn.

Presentation activation includes all logical constituents irrespective of
viewport clipping; demand activation remains deferred until applicable explicit
interaction. TypeScript submits top-level presentation and semantic interaction
requests and realizes authorized results without orchestrating child selection.
Materialization, verification, loading, and callable admission remain host/client
runtime responsibilities. Preparing reusable metadata does not activate inactive
Slots or retrieve their subject populations.

Automatic defaults require no durable personal Usage. Applicable personal policy
precedes service-prepared defaults and localized discovery. Personal settings
come through the authorized agent/context index or subordinate configuration;
activation preferences remain a separate concern. Exact scope keys, subject
expansion semantics, and runtime evidence follow the shared DAHN contract.

## Specification family

Kind specifications are normative for their semantic boundaries and common
promises. Path Inspector owns its design and adjacent interaction grammar.
Holon Inspector owns concrete Node composition and responsive presentation.
Table Collection owns tabular interaction; Collection kind owns shared subject
and mutation semantics. Underspecified accepted types remain explicit open details.

- [Structure](structure/kind-spec.md)
- [RootedNavigation](structure/rooted-navigation/kind-spec.md)
- [Node](node/kind-spec.md)
- [Collection](collection/kind-spec.md)
- [PropertyMap](property-map/kind-spec.md)
- [Value](value/kind-spec.md)
- [String](value/string/kind-spec.md)
- [Path Inspector](structure/rooted-navigation/path-inspector/design-spec.md)
- [Holon Inspector](node/holon-inspector/design-spec.md)
- [Table Collection](collection/table/design-spec.md)

Graph and Geospatial remain peer specializations of Structure alongside
RootedNavigation. Create kind directories on demand only, when a concrete documentation need
establishes meaningful subject semantics or behavior to specify. Do not preallocate
a directory tree from every ValueType or for symmetry. This index is not the
full kind registry.

## Property and value composition

PropertyMap owns set-level layout, visibility, personalization, and label/value
pairing. It may compose String Visualizers for PropertyName labels alongside
ValueType-specific Visualizers for values. Property is not a separate kind or
selection layer. The DAHN design and kind specs use this model. Historical planning descriptions
and concrete extraction sources are tracked for reconciliation in the ledger.

## Refactor tracking

- [Documentation implementation plan](../dahn-docs-refactor-impl-plan.md)
- [Migration ledger](../dahn-docs-refactor-ledger.md)
