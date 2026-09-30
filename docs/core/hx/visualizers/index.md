# Visualizer Specification Families

## Organization and authority

VisualizerKind provides the organizational parent for Visualizers. It classifies
semantic subject shape; VisualizerSlot is a local composition boundary defined
by a Dancer or Visualizer. A slot's owner supplies its subject binding, required
contract, context, and participation constraints. A selected Visualizer fulfills
that contract and owns its internal experience.

Kind specifications describe classification and established shared promises.
They are not substitutes for owner-defined slot contracts. A Visualizer that
fulfills multiple contracts still has one authoritative design specification,
referenced from other applicable families.

## Current frames

These are incomplete extraction destinations. Source specifications and the
existing Path Inspector grammar retain detailed authority until content moves.

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
selection layer. Existing source sections that describe that layer await
reconciliation; the new PropertyMap and Value frames record the accepted target.

## Refactor tracking

- [Documentation implementation plan](../dahn-docs-refactor-impl-plan.md)
- [Migration ledger](../dahn-docs-refactor-ledger.md)
