# Value VisualizerKind

## Status and authority

Incomplete kind specification frame incorporating the accepted direct
PropertyMap-to-Value composition model. The
[DAHN Design Specification](../../dahn-design-spec.md) remains the source for
selection/runtime mechanisms pending reconciliation. Its intervening Property
Visualizer layer is superseded by the target model in
[PropertyMap](../property-map/kind-spec.md).

## Semantic subject and specialization

One value governed by its declared ValueType and applicable semantic context.
Value Visualizers support diverse ways of presenting and interacting with that
value, including inspection and permitted editing.

ValueType describes the data and its semantics. VisualizerKind classifies a
visualization capability. Specialized Value kinds may reflect stable value-type
semantics, without requiring a mechanically identical hierarchy or a single
renderer per ValueType. This frame retains `Value` as the family name;
“ValueType-specific Visualizer” describes applicability, not a renamed data type.

## Selection and binding

A composition owner defines the slot's required contract, bound value, declared
ValueType, property metadata where applicable, interaction mode, and constraints.
DAHN selection chooses an applicable, conforming Visualizer; the runtime binds
it to the actual value and context. A ValueType is selection input, not a
hard-coded renderer assignment.

PropertyMap Visualizers may directly compose value slots alongside independent
property-name label slots. Other Visualizers may also compose Value slots;
Value visualization has no intrinsic dependency on PropertyMap or on a property.

## Internal authority

The selected Visualizer owns value presentation and interaction within the
parent's allocation and participation constraints. The parent owns placement,
label/value pairing where applicable, and external allocation. A child may
compose further child slots when its realization requires them.

Editability is determined by the supplied role and semantic permissions, not by
the availability of an editor implementation. MAP remains authoritative for
semantic validation and staged mutation. VisualizerUsage records agent-relative
configuration and usage; the Visualizer fulfills the slot contract.

## Specialized families

- [String](string/kind-spec.md) — string presentation and interaction, including
  use in a property-name label role.

Create further kind directories on demand only, when an actual documentation
need establishes a meaningful semantic boundary. Do not preallocate one for
every ValueType. Multiple concrete Visualizers may fulfill a specialized kind.
