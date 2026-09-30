# Collection VisualizerKind

## Status and current authority

Incomplete specification frame. Detailed existing behavior remains in
[DAHN Design Specification](../../dahn-design-spec.md) and
[Space Navigator Design Specification](../../../space-navigator/space-navigator-design-spec.md) pending extraction.
This frame establishes the intended documentation boundary, not a replacement
for their detailed contracts.

## Semantic subject and classification

A homogeneous collection sharing an effective element shape. Existing sources differ on whether this includes value collections as well as Holon collections; that scope remains explicitly unresolved here.

A VisualizerKind classifies Visualizers by the semantic shape of their subject.
It does not identify a particular owner-defined VisualizerSlot, spatial region,
or concrete presentation implementation.

## Common promises and slot boundaries

Shared kind-level promises belong here when established. A composition owner
specifies its actual slot contract, subject binding, context, and participation
constraints in its own specification. Kind membership alone does not establish
conformance to every slot requesting that kind.

Selection and runtime realization follow the
[DAHN composition and selection model](../../dahn-design-spec.md).
The selected Visualizer fulfills the slot contract; VisualizerUsage records
agent-relative use and configuration.

## Family

- [Table Collection](table/design-spec.md)

## Authority boundary

Concrete layouts, child slot arrangements, gestures, and rendering strategies
belong to individual Visualizer specifications. No concrete family's internal
composition is made a universal requirement by this directory hierarchy.
