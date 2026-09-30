# Path Inspector Design Specification

## Status and current authority

Incomplete specification frame. Existing detailed behavior remains authoritative
in [DAHN Design Specification](../../../../dahn-design-spec.md) and
[Space Navigator Design Specification](../../../../../space-navigator/space-navigator-design-spec.md), subject to the compositional
authority model in DAHN's Design Concept. This frame does not yet supersede
those source sections.

The [existing Path Inspector Interaction Grammar](../../../../../space-navigator/path-inspector-grammar.md) remains the
sole detailed authority for Path Inspector spatial productions.

## Purpose and authority

Path Inspector is a concrete Visualizer in the
[RootedNavigation family](../kind-spec.md). Its specification owns the experiential
realization behind the slot contract it fulfills.

## Contract fulfillment and semantic subject

A compatible root Holon; no intrinsic dependency on HolonSpace. Space Navigator supplies its local HolonSpace when binding its own RootedNavigation slot.

The selecting parent's slot establishes the required contract and participation
constraints. DAHN selection resolves that boundary. Classification as RootedNavigation
is not a claim that this implementation satisfies every conceivable RootedNavigation slot.

## Direct child roles and subject bindings

The following is a framing inventory of existing roles, not a finalized runtime
API. Detailed accepted types and participation contracts remain in the current
sources until reconciled. Each actual child slot is independently substitutable
and resolved through DAHN selection.

| Role | Subject or binding context | Boundary |
| --- | --- | --- |
| Node participation role | The Holon represented by the navigation occurrence | Path Inspector owns the external allocation and participation requirements; the selected Node Visualizer owns its internals. |
| Collection participation role, where directly composed | The collection involved in navigation | Exact direct ownership and binding must be distinguished from collections composed internally by a Node Visualizer. Existing sources require reconciliation. |

## Internal behavior and state

Occurrence topology, lineage, focus, grid projection, compression, overflow, branch operations, and inter-child allocation. Detailed productions remain in the existing interaction grammar.

Authoritative MAP data and staged transaction state remain with MAP/Rust.
This Visualizer's presentation state does not become a second semantic model.

## Parent and child boundaries

The parent owns the external allocation and requirements at its slot boundary.
This Visualizer owns internal realization and directly defined child slots.
It does not prescribe the private composition of selected children. Agent-specific
configuration and usage belong to VisualizerUsage; the Visualizer fulfills the
slot contract.

## Existing detailed sources

- [DAHN Design Specification](../../../../dahn-design-spec.md) — composition, kind classification,
  selection, and currently embedded concrete behavior.
- [Space Navigator Design Specification](../../../../../space-navigator/space-navigator-design-spec.md) — currently embedded
  concrete realization, scenarios, and editing behavior.
- [Path Inspector Interaction Grammar](../../../../../space-navigator/path-inspector-grammar.md) — parent/child spatial
  responsibility and current extent-participation material.
