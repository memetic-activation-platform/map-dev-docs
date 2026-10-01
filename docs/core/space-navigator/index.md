# DAHN Space Navigator

Space Navigator is a DAHN Dancer for exploring, inspecting, and editing a MAP
Space. It binds its local HolonSpace to direct experience roles, including a
RootedNavigation slot, and coordinates experience actions and transactions.
Selected Visualizers own their internal composition and presentation.

## Reading guide and authority

| Document | Responsibility |
| --- | --- |
| [Concept](space-navigator-concept.md) | Explanatory mental model and initial experience. |
| [DAHN architecture](../hx/dahn-arch.md) and [design](../hx/dahn-design-spec.md) | Shared responsibilities, composition, selection, and runtime contracts. |
| [Space Navigator design](space-navigator-design-spec.md) and [interaction grammar](space-navigator-interaction-grammar.md) | Dancer roles, subject bindings, context, and action coordination. |
| [Path Inspector design](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md) and [grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md) | Concrete two-axis navigation, topology, compression, and recovery. |
| [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md) | Concrete Node presentation and child composition. |
| [Table Collection](../hx/visualizers/collection/table/design-spec.md) | Table presentation, ordering, and collection interaction. |
| [DAHN launch experience](../hx/dahn-launch-experience-design-spec.md) | Application-shell entry narrative, readiness, accessibility, and imagery provenance. |
| [Implementation plan](space-navigator-impl-plan.md) | Derivative delivery sequence and historical implementation status. |

Path Inspector is the initial RootedNavigation realization. Another compatible
Visualizer may use different geometry without changing Space Navigator's direct
roles. Each document is authoritative for its own concern; implementation plans
do not establish new design rules.

## Documentation authority

DOC1–DOC6 establish the family structure, shared authority, and Path Inspector /
Space Navigator separation. Holon Inspector and Table content is reconciled in its
family. Delivery plans and the final navigation/acceptance audit are complete. See the
[refactor plan](../hx/dahn-docs-refactor-impl-plan.md) and
[migration ledger](../hx/dahn-docs-refactor-ledger.md).
