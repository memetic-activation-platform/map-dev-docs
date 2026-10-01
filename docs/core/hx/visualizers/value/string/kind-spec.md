# String VisualizerKind

## Status and authority

Draft normative specification for this kind's semantic boundary and common
promises. Concrete implementations own their internal grammar. Shared DAHN
selection, runtime, allocation, and state contracts apply; this document does
not create a separate selection authority.

## Semantic subject

One string value, together with the role, interaction mode, and applicable
constraints supplied at the parent's slot boundary. String specializes Value;
a property-name label is one use of String visualization, not a separate kind.

## Presentation and interaction

A selected String Visualizer owns how the string is rendered and, when permitted,
interacted with inside the assigned allocation. Different conforming Visualizers
may use different presentation strategies. The parent supplies role-specific
constraints, while the effective theme/MDS participates in presentation.

Rendering a string does not itself authorize editing it or interpreting it as
markup. Label and editable-value roles can impose different requirements on
implementations within this same family.

## Property-name label role

A [PropertyMap Visualizer](../../property-map/kind-spec.md) may supply a
PropertyName string to a label slot. The PropertyMap owner controls the label's
relationship to the value: pairing, placement, allocation, visibility, and
applicable typography constraints. The selected String Visualizer realizes the
label within that boundary.

The property's actual value is a separate subject selected through a separate
value slot. If that value is also a string, both slots may select from the
String family while carrying distinct roles and interaction constraints.

## Boundaries and concrete realizations

String kind membership does not guarantee applicability to every String slot.
DAHN selection evaluates the actual contract and context. This frame introduces
no mandatory child slots, concrete renderer, editor widget, or fixed typography.
