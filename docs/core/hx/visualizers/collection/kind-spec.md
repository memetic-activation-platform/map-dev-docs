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
