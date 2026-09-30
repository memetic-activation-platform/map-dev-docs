# Table Collection Design Specification

## Status and current authority

Incomplete specification frame. Existing detailed behavior remains authoritative
in [DAHN Design Specification](../../../dahn-design-spec.md) and
[Space Navigator Design Specification](../../../../space-navigator/space-navigator-design-spec.md), subject to the compositional
authority model in DAHN's Design Concept. This frame does not yet supersede
those source sections.

## Purpose and authority

Table Collection is a concrete Visualizer in the
[Collection family](../kind-spec.md). Its specification owns the experiential
realization behind the slot contract it fulfills.

## Contract fulfillment and semantic subject

The supplied collection projection and member bindings. Current source material covers both Holon and simple-value collections; the common Collection kind scope needs reconciliation.

The selecting parent's slot establishes the required contract and participation
constraints. DAHN selection resolves that boundary. Classification as Collection
is not a claim that this implementation satisfies every conceivable Collection slot.

## Direct child roles and subject bindings

The following is a framing inventory of existing roles, not a finalized runtime
API. Detailed accepted types and participation contracts remain in the current
sources until reconciled. Each actual child slot is independently substitutable
and resolved through DAHN selection.

| Role | Subject or binding context | Boundary |
| --- | --- | --- |
| Property/Value cell participation, where established | A projected property or value for the row member | Exact slot names, contracts, and bindings are not yet specified by this frame. |

## Internal behavior and state

Rows, columns, headers, sorting/filtering, selection, occurrence-local restoration, and concrete editing presentation. Sorting is presentation state, not a change to semantic collection membership or navigation topology.

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
