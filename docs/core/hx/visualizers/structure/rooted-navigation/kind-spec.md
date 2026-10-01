# RootedNavigation VisualizerKind

## Status and authority

Draft normative specification for this kind's semantic subject and common
participation boundary. Concrete Visualizer grammar remains with the selected
implementation's specification. Shared runtime, selection, and allocation
mechanisms remain with the DAHN design specification.

## Semantic subject and classification

An interaction-derived navigation topology anchored at a compatible root Holon. RootedNavigation is a specialization of Structure, alongside Graph and Geospatial; it is not subordinate to either.

A VisualizerKind classifies Visualizers by the semantic shape of their subject.
It does not identify a particular owner-defined VisualizerSlot, spatial region,
or concrete presentation implementation.

## Common promises and slot boundaries

A composition owner
specifies its actual slot contract, subject binding, context, and participation
constraints in its own specification. Kind membership alone does not establish
conformance to every slot requesting that kind.

Selection and runtime realization follow the
[DAHN composition and selection model](../../../dahn-design-spec.md).
The selected Visualizer fulfills the slot contract; VisualizerUsage records
agent-relative use and configuration.

## Root and realization boundary

The root Holon is an anchor for navigation, not the entirety of the visual
subject. Generic Holon affordances, the root, navigation context/state, and
allocation support realization of the subjects and collections unfolded through
interaction. A conforming generic realization has no intrinsic HolonSpace,
Space Navigator, or AgentSpace dependency.

Space Navigator supplies its local HolonSpace as the initial root binding of
its own slot. Another owner may supply a different compatible Holon. The slot
owner can impose additional participation requirements without owning the
selected Visualizer's internal topology production or spatial grammar.

Two-dimensional inspector/path layout is one realization. Radial, graph-like,
zoomable, or other rooted-navigation realizations remain possible. Horizontal
or vertical lineage, grid bands, and specific compression states are not
kind-wide promises.

## Family

- [Path Inspector](path-inspector/design-spec.md)

## Authority boundary

Concrete layouts, child slot arrangements, gestures, and rendering strategies
belong to individual Visualizer specifications. No concrete family's internal
composition is made a universal requirement by this directory hierarchy.
