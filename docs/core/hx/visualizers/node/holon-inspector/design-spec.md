# Holon Inspector Design Specification

## Status and current authority

Incomplete specification frame. Existing detailed behavior remains authoritative
in [DAHN Design Specification](../../../dahn-design-spec.md) and
[Space Navigator Design Specification](../../../../space-navigator/space-navigator-design-spec.md), subject to the compositional
authority model in DAHN's Design Concept. This frame does not yet supersede
those source sections.

## Purpose and authority

Holon Inspector is a concrete Visualizer in the
[Node family](../kind-spec.md). Its specification owns the experiential
realization behind the slot contract it fulfills.

## Contract fulfillment and semantic subject

One Active Holon and its effective descriptor-derived affordances.

The selecting parent's slot establishes the required contract and participation
constraints. DAHN selection resolves that boundary. Classification as Node
is not a claim that this implementation satisfies every conceivable Node slot.

## Direct child roles and subject bindings

The following is a framing inventory of existing roles, not a finalized runtime
API. Detailed accepted types and participation contracts remain in the current
sources until reconciled. Each actual child slot is independently substitutable
and resolved through DAHN selection.

| Role | Subject or binding context | Boundary |
| --- | --- | --- |
| NodeTitleBarSlot | Bound Holon identity/title context | Title/header realization. |
| ActionBarSlot | Applicable executable affordances and invocation context | Action presentation and child composition. |
| VerticalRailSlot | Singular relationship and navigational Dance affordances of the bound Holon | Singular affordance presentation. |
| PropertyMapSlot | Property facet of the bound Holon, derived from its effective descriptor | [PropertyMap](../../property-map/kind-spec.md) owns set-level composition, including label/value pairing; no intervening Property Visualizer. |
| CollectionTabsSlot | Collection-shaped affordances of the bound Holon | Collection affordance index. |
| CollectionViewerSlot | The active collection exposed by the chosen affordance | Selected Collection Visualizer realization. |

## Internal behavior and state

Internal information architecture, affordance projection, local loading/editing presentation, and responsive allocation among its own children. Navigation topology and outer allocation remain with its parent.

Authoritative MAP data and staged transaction state remain with MAP/Rust.
This Visualizer's presentation state does not become a second semantic model.

## Parent and child boundaries

The parent owns the external allocation and requirements at its slot boundary.
This Visualizer owns internal realization and directly defined child slots.
It does not prescribe the private composition of selected children. Agent-specific
configuration and usage belong to VisualizerUsage; the Visualizer fulfills the
slot contract.

## Existing detailed sources

- [DAHN Design Specification](../../../dahn-design-spec.md) — composition, kind classification,
  selection, and currently embedded concrete behavior.
- [Space Navigator Design Specification](../../../../space-navigator/space-navigator-design-spec.md) — currently embedded
  concrete realization, scenarios, and editing behavior.
- [Path Inspector Interaction Grammar](../../../../space-navigator/path-inspector-grammar.md) — parent/child spatial
  responsibility and current extent-participation material.
