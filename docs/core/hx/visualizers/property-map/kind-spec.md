# PropertyMap VisualizerKind

## Status and authority

Draft normative specification for this kind's semantic boundary and common
promises. Concrete implementations own their internal grammar. Shared DAHN
selection, runtime, allocation, and state contracts apply; this document does
not create a separate selection authority.

## Semantic subject

The property facet of one Holon, interpreted through its effective property
descriptors and bound property values. PropertyMap is a set-level visualization
capability, distinct from presenting one value.

“Properties Viewer” is a presentation label for this capability, not a separate
VisualizerKind. PropertyMap Visualizers may support both inspection and editing.

## Composition authority

A selected PropertyMap Visualizer owns layout, visibility, ordering, grouping,
and personalization for the presented set of properties. Validation feedback and
editing affordances belong to its presentation; MAP retains semantic validation
and mutation authority. It owns the pairing
of names with values and their relative placement and allocation. Typography
and presentation constraints participate in the applicable theme/MDS contract.
Concrete decisions belong to the particular PropertyMap Visualizer.

Property is not an independent VisualizerKind or an intervening selection
boundary. A property row or grouping may be an internal layout construct.
The PropertyDescriptor remains semantic input for names, ValueTypes, and
applicable metadata; it does not imply a separately selected Property renderer.

## Label and value composition

A PropertyMap Visualizer can compose the two parts independently:

| Child role | Bound subject | Selection and context |
| --- | --- | --- |
| Property-name label | PropertyName string | A conforming String Visualizer, with label-role and presentation context. |
| Property value | Actual property value | A conforming Value Visualizer applicable to the declared ValueType, with property descriptor, mode, and relevant Holon context. |

This is the established composition direction, not a mandatory concrete slot
naming scheme or a requirement that every PropertyMap realization use identical
internal slots. Each slot actually defined is an independent DAHN selection
and substitutability boundary. The PropertyMap owner supplies the subject and
constraints; selected children own their internal realization within them.

The label's use of a String Visualizer does not make the PropertyName editable.
Allowed interaction follows the label role's contract. Editing a property's
value is distinct from changing its descriptor-defined name.

## Related kinds and boundaries

- [Value](../value/kind-spec.md) owns classification of value visualization.
- [String](../value/string/kind-spec.md) specializes Value for string subjects,
  including property-name labels.
- The parent Node Visualizer owns the PropertyMap slot's external allocation.
- MAP retains authoritative property, descriptor, and staged-state semantics.

Concrete PropertyMap implementations may differ in arrangement and interaction
without changing these semantic boundaries. No concrete implementation design
is defined by this kind frame.
