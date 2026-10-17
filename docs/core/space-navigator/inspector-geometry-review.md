# Inspector Geometry Review

## Current review and authority

The approved outline and clarifications on 2026-10-17 restructure the specifications
around a concise contract map and four-mode experience. This record indexes decisions
and supersession; it is not a parallel normative grammar. Work continues on the
existing documentation branch and review PR, kept unmerged pending review/revisions.
No executable schema, implementation, issue creation or adaptive persistence work
is included in this documentation pass.

| Read for | Authoritative document |
| --- | --- |
| Shared dependency direction and contract-map structure | [DAHN](../hx/dahn-design-spec.md#43-contracts-and-visualizer-fulfillment) |
| Node Inspector requirements independent of a fulfilling implementation | [Path section 3](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#3-child-slots-and-their-contracts) |
| Pure vertical walkthrough first, then horizontal, Restore and alternatives | [Interaction grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md) |
| Four-mode realization, private regions, local switching and view memory | [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md) |
| Delivery/status, naming gaps and remaining bounded work | [Implementation plan section 23](space-navigator-impl-plan.md#23-four-mode-inspector-geometry-revision) |

## Accepted structure and preserved behavior

A selecting Slot Contract is complete independently of any fulfilling implementation.
A Visualizer explains fulfillment, subject applicability and its declared child
contracts before its private design. The opening is a concise map; shared lifecycle,
allocation and failure rules are linked rather than repeated in dossiers.

Path owns the Node Slot Contract in section 3; internal geometry belongs in section 4
and transitions in the grammar. Kinds stay general. Holon Inspector realizes the four
experiences without imposing its properties pane, rail, tabs or table on substitutes.
Inspect resumes remembered Properties or Collection, not a fifth mode.

Preserve top-down shared tracks, independent per-occurrence presentation, local P↔C
switching, remembered state, unconditional Restore, prior insertion/replacement/
retention/reactivation topology, provenance, qualified contextual retention and
viewport recovery. The pure vertical walkthrough shows Compact + Collection +
Properties with labeled channels; horizontal substitutes Relationship context.
Numeric minima require usability/conformance work rather than measured child rows.

The 2026-10-17 restructuring brief permits a parent-assigned reduced collection-context
height where useful and valid. It supersedes the preceding draft's absolute prohibition
on resizing a downward source, while retaining its Collection experience without a
second collapse. No local switch asks Path for space or changes focus. Window resizing
changes valid dimensions without itself selecting a different private mode.

Properties and Collection share the main region. A shallow Properties return header
is the established recovery treatment; detailed styling is bounded presentation work.
The accepted loader default is Properties with authoritative outcome/available
diagnostics. Restore resumes its last full-content view, not a default or saved pixels.

## Composition boundaries and action decisions

Distinguish existing declarations, proposed boundaries and private regions. The
actual child-slot map includes the existing title/actions/properties/collection
and workflow result declarations. The unbound SingleValue slot is an explicit gap.
The rail and tab index currently are embedded realizations of meaningful singular-
navigation and collection-index choice points. Their independent target Slot Contracts
are documented; exact schema declarations and migration remain distinct. A diagram
does not invent a choice point, and selector cost does not remove one.

The accepted common ActionBar uses PresentActions and parent-supplied membership,
combining subject and occurrence actions. A shared helper can add centrally declared
standards. Actions are bar components, with independently defined icons, not mandatory
selected child Visualizers. Standard controls can share the title band, with proper
icons and accessible overflow. This does not require separate title/subject bars.

Conceptual ChildSlots/FulfillsSlotContract labels do not silently migrate HasSlot,
PathInspector.RootNodeSlot or the current usage relationships. Required/offered
Operators and accepted Types are compatibility evidence, not complete behavioral
proof. VisualizerProfile remains proposed; usage/configuration and preference retain
shared DAHN ownership.

## Shared-column compression decision and remaining scope

The A↓B→C width question is resolved: Path compresses A/B's shared column and
explicitly assigns Relationship to both, while C receives Properties with normal
inspection allocation. A retains Collection α and all meaningful local state in
memory; its hidden full-content minimum does not constrain the Relationship grant.
Relationship is independent of traversal cardinality, so A's plural provenance and
connector axis remain unchanged.

The grammar defines contextual retention before the walkthroughs and qualifies it
with this compression operation. Direct Restore grants expanded allocation in A's
existing cell and resumes α; it takes precedence until the next specified retention
operation. A shared-column width increase leaves B in Relationship unless explicitly
reassigned. Rendering, resizing and focus scanning do not recompute retention.
Close still reclaims only wholly empty bands and does not promote alternatives
to fill canonical cells.

Numeric budgets, callable/schema grounding and implementation conformance remain
bounded work; this scenario no longer carries an unresolved geometry decision.

Extended earlier review history is retained in Git. Documentation builds/link checks
report document consistency, never implementation conformance. Runtime contract
migration and geometry delivery remain separate reviewable work.

## Revised composition clarification — 2026-10-17

The project owner refined the earlier warning against creating slots for symmetry:
Slots remain the primary unit of composition. Meaningful substitutability and agent
agency determine internal choice points, not present selection overhead. Preserve
those contracts independently of current fulfilling controls; private mechanics
need not become Slots. Performance belongs in compatible binding reuse, bulk
retrieval, scoped preferences and asynchronous persistence under shared DAHN rules.
This supersedes any earlier wording that treated rail/index embedding as sufficient
reason to classify those roles as permanently private or to remove their target
Slot Contracts. Other approved outline and interaction decisions are unchanged.

The ActionBar granularity decision remains explicit: individual Actions are
components of the selected ActionBar and do not require separate Visualizer
selection. Independently defined icons do not introduce per-Action Slots.
