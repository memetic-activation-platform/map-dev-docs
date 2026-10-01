# Node VisualizerKind

## Status and authority

Draft normative specification for this kind's semantic subject and common
participation boundary. Concrete Visualizer grammar remains with the selected
implementation's specification. Shared runtime, selection, and allocation
mechanisms remain with the DAHN design specification.

## Semantic subject and classification

Exactly one Holon, with its effective descriptor-derived affordances.

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

## Subject binding and realization boundary

The slot binds an actual Holon. Its identity, type, and effective descriptors
inform selection; its actual data and afforded behavior supply the realization.
The kind does not prescribe a title bar, property pane, rail, tabs, or other
internal slots. Holon Inspector is one Node realization, not the definition of
Node. A parent may require participation capabilities such as bounded allocation
without requiring Holon Inspector's private information architecture.

## Family

- [Holon Inspector](holon-inspector/design-spec.md)

## Authority boundary

Concrete layouts, child slot arrangements, gestures, and rendering strategies
belong to individual Visualizer specifications. No concrete family's internal
composition is made a universal requirement by this directory hierarchy.
