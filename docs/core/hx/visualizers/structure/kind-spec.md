# Structure VisualizerKind

## Status and authority

Draft normative specification for this kind's semantic subject and common
participation boundary. Concrete Visualizer grammar remains with the selected
implementation's specification. Shared runtime, selection, and allocation
mechanisms remain with the DAHN design specification.

## Semantic subject and classification

Multiple semantic subjects unified by an organizing semantic topology. Structure is distinct from a homogeneous Collection.

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

## Topology boundary

The organizing topology is part of the semantic subject used for applicability
and realization. Structure is not an arbitrary heterogeneous bag of Holons.
Graph, Geospatial, and RootedNavigation are peer specializations with different
topological semantics. Drawing a collection with edges does not automatically
make its kind Graph; the semantic subject, not appearance, determines kind.

## Family

- [RootedNavigation](rooted-navigation/kind-spec.md)

Graph and Geospatial are peer Structure specializations. They have no new
specification shells here until substantive source material warrants them.

## Authority boundary

Concrete layouts, child slot arrangements, gestures, and rendering strategies
belong to individual Visualizer specifications. No concrete family's internal
composition is made a universal requirement by this directory hierarchy.
