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

## Developer declarations and initial binding

A slot contract states the obligations every replacement must fulfill. An HX
developer may separately declare a preferred concrete child default, including
subject-dependent choices; Rust resolves and validates it. Do not encode a
concrete fallback in TypeScript or narrow accepted types merely to protect the
incumbent. Compatible personal choices take precedence, and independently
contributed alternatives remain eligible for exploration.

Use [DAHN prepared bindings](../dahn-design-spec.md#145-recursive-selection)
for initial rendering. Slot substitution boundaries do not require independent
candidate discovery per occurrence. Rust first reuses eligible Slot Usages and
performs broad discovery only on a miss. Missing default Usage is recorded at
the selected Visualizer's declared applicability type and reused across subtypes;
it is not a personal preference merely because it is persisted. Obtain personal
settings through Rust's authorized context. Declaration schema and exact scope keys remain open. Runtime artifact
verification and admission still apply.

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
