# Path Inspector Design Specification v0.10

## Change Log

### v0.10

Defines the direct Node Inspector child-slot contract, subject binding, repeated
occurrences, allocation/presentation obligations and owner-bound request surface.
Adopts grammar v0.14 independent occurrence intents and local full-content choice.

### v0.9

Adopts grammar v0.13 whole-band insertion, source-adjacent new destinations,
retained-branch promotion/exchange and placement-preserving direct Restore.
Supersedes terminal-append and first-member spatial-anchor behavior.


### v0.8

Uses explicit policy profiles and the capability-only Node presentation Operator.
Supersedes v0.7 rendered-content sizing; grammar §4.4.1 owns the retention matrix,
shared-track aggregation, preferred viewport, fallback, and attention policy.

### v0.7

Allocates initial size from content requirements, retaining the source title, tabs and five collection rows plus controls/header alongside the channel and full target. Supersedes viewport-capacity negotiation in v0.6.

### v0.6

Refines active-frontier attention to preserve the surface origin and immediate collection context. Initial Node budgets support the source/channel/target composition in the usable viewport; forced centering margins are removed.

### v0.5

Aligns with Interaction Grammar v0.9: the active target receives useful expanded allocation and the viewport follows it, preserving immediate source context when possible. Initial experience sizing derives from the two-stage composition instead of requiring resize during traversal.

### v0.4

Aligns with Interaction Grammar v0.8: group anchors replace newest-target source alignment, later members append down/right, and retained history never moves up/left because of new traversal. Each new group takes the canonical source-axis cell and pushes older groups outward while preserving their relative order; repeated traversal appends within its existing group. Preserves traversal provenance, labels, qualifiers, Predicate and Dance refinements, destination-first loading, independent compression/allocation, and close/re-root behavior. Earlier change-log entries describe historical behavior superseded by this revision.

### v0.3

Aligns the Path Inspector experience with Interaction Grammar v0.7 by generalizing connector presentation from relationship-specific labeling to traversal provenance.

- Defines connector labels as **traversal labels**: compact human-readable projections of how a target occurrence was reached.
- Relationship expansion uses the relationship predicate/name as the primary traversal label.
- A relationship Expand may be qualified by an optional Predicate consisting of Filters; the connector may signal this compactly with a funnel icon or equivalent traversal qualifier.
- A navigational Dance uses the Dance name as its primary traversal label.
- Clarifies that traversal labels and qualifiers describe navigation provenance and do not assert new semantic relationships between source and target Holons.
- Aligns retained-group language with equivalent traversal provenance rather than relationship name alone.
- Leaves full Predicate inspection, Filter presentation, Dance parameters, and exact traversal-qualifier styling to future interaction design.
- Preserves the v0.2 source alignment, traversal grouping, terminal insertion, branch-preserving reflow, destination-first behavior, and compression-funded channel allocation.

### v0.2

Aligns the observable Path Inspector experience with Interaction Grammar v0.6.

- Makes source-target axis alignment explicit: a horizontal target opens immediately to the right of its source in the same row; a vertical target opens immediately below its source in the same column.
- Describes relationship-grouped retained alternatives without duplicating the grammar's insertion/reflow algorithm.
- Establishes that a newly traversed member of an existing relationship group appears at that group's terminal position: bottom-most for horizontal traversal groups and right-most for vertical traversal groups.
- Makes labeled traversal channels part of the observable Path Inspector experience, with shared labels permitted for grouped traversals through the same affordance.
- Clarifies that traversal real estate is funded jointly by source compression and traversal-channel allocation rather than by unconstrained surface spreading alone.
- Adds repeated-traversal scenarios demonstrating source alignment, relationship grouping, terminal insertion, and branch-preserving reflow.
- Preserves the interaction grammar as the sole authority for topology, grid placement, lineage routing, group reflow, allocation, compression, overflow, branch closing, and re-root semantics.

### v0.1

Initial Path Inspector design specification defining subject/slot binding, traversal interactions, active-frontier behavior, loading transitions, editing/navigation coexistence, and interaction scenarios.

## Status and authority

Draft normative specification for Path Inspector, a concrete RootedNavigation
Visualizer. The [interaction grammar](interaction-grammar.md) is the sole source
for its topology productions, grid, lineage, allocation, compression, overflow,
branch closing, and re-root semantics. This document binds its subject and child
roles and describes the interactions that use that grammar.

## Purpose and contract fulfillment

Path Inspector realizes rooted navigation as an opinionated two-dimensional,
two-axis experience. Its root may be any compatible Holon; it has no intrinsic
HolonSpace or Space Navigator dependency. Space Navigator is one Dancer that
binds its local HolonSpace to a RootedNavigation slot.

It fulfills the [RootedNavigation kind](../kind-spec.md) plus the selecting
owner's participation requirements. Other RootedNavigation implementations may
use different geometry. Path Inspector's child requirements do not become
requirements of every RootedNavigation or Node Visualizer.

## Subject and direct child slots

Path Inspector's semantic subject is the root Holon of the exploration. Its direct
semantic child role is Node Inspector, repeated for the root and reached navigation
occurrences. Holon Inspector and Load Holons Inspector are candidate implementations
of that role; Path Inspector does not require either implementation by name.

### Node Inspector slot declaration

| Contract element | Declaration |
| --- | --- |
| Owner | Path Inspector |
| Role | Node Inspector; a role, distinct from the concrete Holon Inspector implementation |
| Existing semantic slot identity | `PathInspector.RootNodeSlot`, declared through Path Inspector's `HasSlot` relationship |
| Accepted Visualizer type | `NodeVisualizer.HolonType` |
| Required local Operator | `ApplyNodePresentation`, with the presentation participation contract in [grammar §4.4.1](interaction-grammar.md#441-node-inspector-slot-compression-contract) |
| Occurrences | One realization for each navigation occurrence, including the root; repeated occurrences use the same declared slot role |
| Bound semantic subject | The Holon represented by that occurrence, with its effective descriptor and execution context; not the Path Inspector, a traversal record or a geometry wrapper |
| Allocating owner | Path Inspector; the child receives its shared-column width and shared-row height together with its own presentation assignment |
| Internal composition owner | The selected Node inspector, which allocates and manages its own immediate child slots |

`PathInspector.RootNodeSlot` is the existing schema identifier. Its name does not
restrict this contract to the root occurrence, or require a separate contract for
horizontal versus vertical destinations. Node Inspector is the role vocabulary;
this specification does not introduce a second slot identifier through a naming
change. Distinct occurrences of the same semantic Holon retain distinct local
presentation state, even when the selected Visualizer choice is shared by context.

DAHN resolves this declared slot under the
[slot-directed selection policy](../../../../dahn-design-spec.md#1421-slot-directed-descriptor-selection).
Accepted kind alone is insufficient. Rust-owned eligibility checks required/offered
Operator compatibility and the supported participation profile before selection;
materialization verifies callable bindings. The selected participant promises the
complete supported allocation contract. A subsequent refusal of a valid grant does
not initiate reselection or a new sizing negotiation.

### Downward allocation and presentation contract

Path Inspector supplies one coherent assignment through the required local Operator:

| Assignment concern | Path Inspector's obligation | Node participant's obligation |
| --- | --- | --- |
| Dimensions | Allocate finite width/height within the admitted policy profile; all cells share their column width and row height | Allocate internal child regions within that rectangle; use responsiveness and owned overflow without painting into siblings |
| Inspect | Request ordinary inspection of the bound subject | Present the occurrence's remembered full-content view; ordinary and loader initial views are Properties |
| Singular-navigation context | Enter context for the latest horizontal source on the focused ancestry | Keep singular navigation usable, with recognizable identity and Restore; Holon Inspector realizes Relationship mode |
| Collection-navigation context | Enter context for the latest vertical source on the focused ancestry | Retain navigation and already-active collection content on entry; Holon Inspector realizes Collection mode and permits subsequent local Properties/Collection switching |
| Compact identity | Retain recognizable context for an older occurrence | Keep subject identity and operable Restore, even in a wide or tall shared cell |
| Allocation update | Preserve the distinction between new context entry and reapplication during resizing or unrelated navigation | Recompute internal geometry without resetting a permitted local view choice or replaying context entry |

Presentation requirements belong to occurrences. Shared-track dimensions MUST NOT
combine intents or force richer presentation. At most the latest source on each
axis retains navigation context; retained alternatives outside focused ancestry
add no further obligation. The grammar owns the exact track aggregation, profile
bounds, context-entry semantics, explicit outcomes and worked mixed-path rules.

The slot contract does not expose concrete private Properties, rail or collection
pane identifiers. A substitute can realize the semantic requirements differently.
For participants with multiple local full-content views, switching them stays within
the current allocation and does not require a parent request. Geometry application
must not fetch or reconstruct content merely to calculate layout.

### Upward intents and owner-bound requests

Path Inspector binds requests to the actual child occurrence. These are local
presentation/navigation interactions, not new Dances or Commands. The request
surface describes behavior; the concrete adapter and executable contract encoding
must preserve these semantics without exposing another occurrence's authority.

| Child interaction | Bound request information | Path Inspector's response |
| --- | --- | --- |
| Navigate a singular target | Source occurrence, activated affordance, resolved target and traversal provenance | Establish target existence, then apply horizontal placement/retention, source context, final destination allocation and pending presentation |
| Navigate a collection member | Source occurrence, source collection, selected member and traversal provenance | Apply vertical placement/retention and final destination allocation; the source already presents the collection, so no extra collapse is needed to expose it |
| Restore occurrence | Requesting occurrence and its retained local full-content state | Focus/reveal it in place, recompute shared-track allocations and grant inspection before restoring its remembered view; do not promote branches or discard descendants |
| Request attention / release attention | Requesting occurrence and requested attention operation | Apply or release the grammar's bounded attention projection without transferring topology or native-window authority to the child |
| Close occurrence/branch | Requesting occurrence | Apply the grammar's branch-close rules and explicit availability/guard outcome; closure authority is not inferred from the subject Holon |
| Explore from here | Requesting occurrence and its bound subject | Delegate a new rooted exploration to the owning experience under the re-root contract |
| Inspect selected Visualizer | Actual requesting occurrence's selected participant | Open inspection for that participant, with its actual child composition; do not confuse subject identity with Visualizer identity |

These operations are delivered through the established runtime and selected Title
Bar/Action bindings where applicable. Standard action membership remains declared
once in the shared title contract. Subject-level actions remain with the selected
Node's own action composition. A title action can target an occurrence without
changing the Title Bar's semantic subject from its Holon.

Restore and allocation requests follow the
[immediate-parent protocol](../../../../dahn-design-spec.md#coherent-assignments-and-parent-requests).
A refused or invalid request preserves the last valid presentation and gives an
explicit reason. A child cannot enlarge a Path track by reporting preferred
rendered content. Local Properties/Collection switching is not an upward request.

### State, lifecycle and failure obligations

The bound subject retains its actual reference and transaction ownership; placement
does not rebind it. Path owns occurrence identity, topology, focus and outer layout.
The selected Node owns its local full-content memory and meaningful child state.
Compression, hiding, resizing and restoration preserve selected child identities,
references, edits and navigation/collection state. Mere hide/show neither refetches
nor reconstructs content. Replacing the selected participant is a separate explicit
selection/materialization operation, not an effect of a grant change.

Pending, failed and realized destinations occupy the same Path-owned rectangle.
A missing callable fails admission; failure to honor a valid assignment is a local
contract violation with an owner-provided recovery path. Neither failure licenses
child-driven extent negotiation or silent substitution. Compact and failed cells
must retain a recoverable Restore/inspection exit. Path disposal releases its
occurrence realizations and associated bindings through the established lifecycle;
it does not claim disposal ownership of borrowed semantic contexts.

### Direct-slot boundary and nested composition

Title Bar, PropertyMap, Actions, singular-navigation and Collection presentations
are children of a selected Node inspector, according to that implementation's
[own slot declarations](../../../node/holon-inspector/design-spec.md#direct-child-roles-and-subject-bindings).
They are not direct Path Inspector slots. Collection-mediated traversal binds its
source collection and member as provenance but does not promote the CollectionViewer
slot to a child of Path Inspector. Any future direct Collection slot needs its own
explicit subject binding, allocation and participation contract.

Lineage channels, traversal labels, viewport and view controls are Path-owned
composition machinery in this contract, not additional declared semantic child
Visualizer slots. Inspectable implementation regions do not by themselves create
`HasSlot` declarations. This distinction does not preclude a future deliberate
migration of those regions to selected child slots.

## State and host boundaries

Navigation occurrence identity, topology, focus, layout, and view remain distinct
from semantic Holon identity and MAP staged state. Path Inspector owns its
navigation state and surface operations within the host's allocation. It does
not own the Canvas, Window Manager, or Dancer's transaction actions.

Close removes a branch according to [grammar §2.9](interaction-grammar.md#29-close-branch).
Re-root requests an additional rooted exploration from its owning experience under
[grammar §2.7](interaction-grammar.md#27-re-root). Space Navigator realizes this as
a sibling exploration tab within the same Dancer experience. It preserves the source by
default; it does not imply transaction abandonment or a new occurrence schema.

## Active Traversal Frontier

At any point, Path Inspector has an **active traversal frontier**: the visualizer occurrence currently receiving primary interaction and spatial priority.

Path Inspector SHOULD preferentially allocate its
Canvas-provided real estate toward this frontier.

Prior contexts progressively compress away from it under the
[bounded protection and aggregation policy](interaction-grammar.md#shared-track-aggregation-and-mixed-paths).
Other Rooted Navigation realizations may choose different focus, allocation,
and history policies.

> **Path Inspector allocates its Canvas-provided
> space toward the active traversal frontier and compresses provenance behind it.**

## Applying the Interaction Grammar

The [interaction grammar](interaction-grammar.md) owns spatial productions.
The following describes how semantic navigation intents from children invoke
those productions. Rail/tab/row examples describe the Holon Inspector and Table
realizations; a conforming substitute can supply the same intent differently.

### Initial Allocation and Active Frontier

The [grammar's Node-slot policy](interaction-grammar.md#441-node-inspector-slot-compression-contract)
is the authority for track budgets, per-occurrence intents, explicit profiles,
shared-track aggregation, and the moving preferred viewport. The selected Node
receives dimensions and required capabilities together; it does not report
rendered content to size ancestor tracks. Path owns tracks and connectors, not
Node-private regions. Pending, error, and materialized participants occupy the
same policy-allocated rectangle.

Navigation policy, pixel geometry, and DOM application are distinct concerns.
A deterministic layout helper may compute track dimensions, rectangles, connector
geometry, and surface extent from explicit topology/projection, states, profile,
and viewport inputs. Budget reduction uses one common factor per axis from the fixed profile reference
composition under the grammar's stable-state/useful-minimum bounds, never actual
historical-span interpolation.
It is a mechanism of Path's allocation authority. Implement the reviewed logical
placement rules from the grammar, preserving reference/occurrence semantics. Child internals and DOM
measurements and history-dependent stabilization are not geometry inputs.

Each containing owner adds framing to a desired viewport request. Actual grants
flow down normally; ordinary traversal never requires native-window growth.
Viewport movement reveals the active target and immediate source where they fit,
then recovers older history by pan/scroll. Preferred extent expresses the bounded policy composition, rather than the
actual bounding span of selected or retained history; see the [worked cases](interaction-grammar.md#worked-protection-and-aggregation-examples). A constrained viewport may reduce
profile budgets to useful limits without changing semantic track states. Beyond
those limits the surface overflows rather than shrinking useful inspection.

Automatic frontier reveal and Actual Size recovery align an inspector taller
than the viewport at its top edge, preserving the header and restoration
controls. They must not vertically center that oversized inspector and hide
its top. Horizontal reveal and explicit user pan remain available.

### Horizontal Navigation

Activating a structurally singular rail entry invokes the Grammar's horizontal
rule: first-time destination placement inserts a whole column immediately right
of the source, across every row. A new selection uses the source-adjacent cell,
replacing an untraversed destination or retaining/displacing an explored continuation.
Selecting a retained destination through its source reuses/promotes that branch
and exchanges positions when the outgoing branch is also explored. Direct Restore
expands/reveals in place without changing topology or the selected continuation.

### Vertical Traversal

Activating a structurally plural affordance exposes its selected Collection.
Member navigation invokes the symmetric vertical rule: first-time destination
placement inserts a whole row below the source stage, across every column.
Replacement, retained-branch displacement and reactivation follow the single
[placement/retention authority](interaction-grammar.md#24-branch-and-retained-alternative-insertion).
The Collection preserves sibling context; provenance groups do not impose terminal
append or first-member spatial anchoring.


### Recursive Exploration and Traversal Provenance

Every reached Node may invoke either traversal rule. Path Inspector MUST distinguish
semantic holon identity from visualizer occurrence identity, and traversal
provenance SHOULD record how each occurrence was reached. The same holon may
appear in multiple occurrences with different traversal provenance, local
selection, focus, visualizer, and collection state.

Traversal provenance is more general than relationship expansion. The Path
Inspector experience anticipates at least:

- expansion of a relationship;
- expansion of a relationship qualified by an optional Predicate consisting of
  Filters;
- invocation of a navigational Dance.

The connector presents a compact **traversal label** derived from that
provenance. For relationship expansion, the relationship predicate/name is the
primary label. For a navigational Dance, the Dance name is the primary label.

A Predicate-qualified Expand remains an expansion of the same relationship. The
Predicate constrains the traversal result rather than creating a new semantic
relationship. The traversal label MAY therefore carry a compact qualifier, such
as a funnel icon, indicating that filtering was applied.

The connector need not display the full Predicate, its Filters, Dance
parameters, or other detailed provenance. Exact interaction for inspecting that
detail is deferred. The interaction grammar remains authoritative for connector
routing, grouping identity, label sharing, and qualifier placement.

## Compression and Editing

Compression applies only to projection and presentation. It MUST NOT discard
the selected collection tab, selected rail affordance, child links, sort/filter
state, selected row, edit mode, staged-state reference, or selected Visualizer
identity. Re-expansion SHOULD restore prior local context where feasible.

Opening a traversal SHOULD obtain part of the real estate required for its
destination and labeled traversal channel by compressing the source occurrence
under the grammar's allocation policy. Traversal therefore does not merely push
the destination farther away: prior context yields presentation space as focus
moves outward. The exact compression state, channel extent, row/column
allocation, and any required surface growth remain grammar-owned decisions.
Displacement preserves existing row/column and channel dimensions independently
of explicit compression or allocation changes. Compression cannot justify
pulling retained grid positions upward or left.

The Grammar's parent-owned allocation rule applies while editing: visualizer
content may maximize locally within its allocation, but neither editing nor
maximization changes navigation topology or claims sibling space.

## Loading States

Descriptor knowledge remains available internally before population is known;
relationship affordance visibility follows the [Holon Inspector rules](../../../node/holon-inspector/design-spec.md#progressive-relationship-affordances).

Path Inspector SHOULD distinguish:

- not loaded;
- loading;
- loaded empty;
- loaded with contents;
- failed.

Discovery state and destination realization state are distinct. Before structural
navigation, establish that the requested traversal produces a valid destination.
For relationship expansion, use current existence evidence or inspect the
relationship; a Predicate-qualified Expand applies its Predicate to determine
the traversable result. A navigational Dance uses its own result contract. If
the resulting traversal has zero targets, indicate that outcome locally and
leave source extent, focus, and existing destination unchanged. An invalid
singular cardinality follows validation/error semantics.

For a valid destination, establish its region first under
[Path Inspector destination-first rule](interaction-grammar.md#28-destination-first-transitions).
The final destination region is the source-adjacent cell after the grammar
applies insertion, retention or branch reactivation. Later
members are not temporarily shown source-aligned and then moved. Any later-group
displacement proceeds down/right before pending presentation appears. A lightweight temporary presentation MUST occupy that final region
before the actual visualizer appears. For example, show `Opening DescribedBy…`
in the immediately right-hand Node slot or `Opening selected Order…` in the
destination Node cell reached by member navigation. Collection loading itself is
owned by the selected Node/Collection contract. This communicates destination and
intent; it need not
expose technical progress or be a separately named Visualizer Commons role.

Resolve/load the destination and select/materialize its visualizer, then replace
the pending presentation in-place without relocating the destination. Cached or
prefetched data MUST NOT bypass the visible structural ordering; no fixed delay
is required. Source compression, region opening, and pan/reflow should communicate
the navigation topology without abrupt title/content swaps. Respect reduced motion
while retaining the sequence and localized feedback.

After allocation, realization failure is shown in that destination with retry
feedback under the existing selection/error contract. If a target disappears
during resolution, show the changed/empty outcome there and refresh discovery;
do not fabricate a target. This race differs from knowingly opening an empty
relationship. Superseded requests MUST NOT overwrite a newer destination or
restore stale counts after context changes.

## Editing While Navigating

Entering edit mode MUST NOT inherently disable navigation.

The person may continue to:

- inspect collections;
- navigate vertically;
- navigate horizontally;
- open other holons;
- edit additional holons.

Staged work remains intact.

## Focus ownership

Path Inspector tracks the active navigation occurrence. Focus is distinct from
visibility and may affect the traversal frontier, keyboard target, and allocation
priority. Dancer-level contextual interactions use the relevant semantic context
without controlling internal row/column geometry. A fully compressed or overflowed
occurrence remains recoverable under the grammar's restoration rules.

## Structural cardinality and traversal

Path Inspector derives traversal shape from the structural contract of the
navigational affordance, not merely the number of returned targets.

For relationship expansion, descriptor-declared cardinality determines the
axis. Applying a Predicate does not change that structural cardinality: a
Predicate-qualified plural relationship remains collection-mediated and
vertical even if filtering leaves one member; a singular relationship remains
structurally singular when empty, and target-existence guards prevent creation
of a fabricated destination.

A navigational Dance likewise supplies a structural result contract independent
of incidental runtime population. A Dance whose navigational result is
structurally plural remains collection-mediated and vertical when one Holon is
returned; a structurally singular Dance result traverses horizontally.

Value arrays need not produce Holon navigation.

The selected Node owns the affordance presentation. Holon Inspector's rail,
collection tabs, and collection viewer are one realization; Path Inspector
receives the corresponding semantic navigation intent rather than owning those
private regions.

## Interaction scenarios

These are examples of the current Path Inspector composition with Holon
Inspector and a Collection Visualizer. Child UI details are illustrative;
the grammar owns topology transitions, and the child owns its presentation.

### Navigate Through a Collection

Given Node A and Collection C:

1. select or double-click row B for navigation;
2. establish B's source-adjacent destination below the source stage using
   whole-band insertion, replacement/retention or branch reactivation;
3. allocate the labeled traversal channel and apply source compression/reflow as
   required by the grammar;
4. create the Node Visualizer occurrence for B in that established destination;
5. preserve A and C;
6. record provenance;
7. preserve C so sibling rows remain accessible.

### Follow a Singular Relationship

Given Node A and singular relationship R:

1. discovery establishes R has a target and reveals it in the right rail;
2. activate R and establish valid target existence;
3. partially compress expanded A and establish B's source-adjacent right-hand
   destination under the grammar's insertion/retention/reactivation rules;
4. allocate the traversal channel between A and B and identify it as R;
5. show `Opening R…` in B's established destination;
6. resolve B and select/materialize its Node Visualizer in-place;
7. preserve provenance from A through R and the grammar's focus/retention rules.

### Follow a Predicate-Qualified Relationship

Given Node A, relationship R, and Predicate P:

1. invoke Expand for R with P as an optional traversal constraint;
2. establish the valid constrained destination/result before changing topology;
3. preserve R as the primary traversal label;
4. add a compact filter qualifier, such as a funnel icon, to signal that the
   traversal result was constrained;
5. establish the destination under the same horizontal or vertical rule implied
   by R's structural cardinality;
6. preserve R and P in traversal provenance even though the connector presents
   only their compact label/qualifier projection.

The Predicate does not create a new RelationshipType and filtering does not
change the traversal axis merely because the resulting population is smaller.

### Follow a Navigational Dance

Given Node A and navigational Dance D:

1. invoke D from A and establish a valid navigational result;
2. derive the traversal axis from D's structural result contract;
3. establish the destination under ordinary source-adjacent insertion/retention,
   retained-branch reactivation and destination-first rules;
4. use D's Dance name as the primary traversal label;
5. preserve the Dance invocation as traversal provenance;
6. resolve/materialize the returned Node or collection-mediated result in the
   established destination.

The connector records that the target was reached through D; it does not imply
that D corresponds to a stored semantic relationship between A and the target.

### Continue Horizontally

Given:

    A -> B

if B opens C:

- C becomes the active frontier;
- B may retain immediate singular-navigation context;
- A may compress more aggressively;
- prior subordinate geometry compresses with its owner.

Repeated horizontal traversal progressively compresses leftward provenance.

### Revisit a Horizontal Relationship

Given retained branches:

    H1 --R1--> H1.1 --R2--> ...
    H1 --R3--> H1.2 --Rn--> ...

if H1 selects a new H1.3 through R1, H1.3 takes the source-adjacent right-hand
cell. Replace the outgoing destination if untraversed; otherwise move its explored
continuation downward intact. Equivalent R1 provenance does not force terminal
append or spatial contiguity with H1.1. Existing explored alternatives retain their
identity/state and relative order during outward displacement. Selecting a retained
H1.1 through H1 instead reuses/promotes it and exchanges branch positions when the
outgoing continuation must be retained. Direct Restore does not rearrange branches.

### Continue Vertically

Given:

    A
      |
      C
      |
      B

if B descends again:

- lower context receives vertical allocation;
- B may vertically compress;
- distant ancestors may compress into horizontal provenance bars;
- immediate collection context remains recoverable.

### Revisit a Vertical Relationship

A repeated plural-member selection uses the source-adjacent destination below
the source stage. Replace an untraversed outgoing destination; retain and move an
explored continuation rightward. Reuse/promote an already-retained member and
exchange branch positions if the outgoing continuation must also be retained.
Provenance grouping does not override these rules or require terminal append.
Directly restoring a retained member in its displayed region leaves placement alone.
Occurrence identity, meaningful state, provenance and descendant attachment survive.

### Mixed Traversal

A node reached horizontally may descend through a collection.

A node reached vertically may open a singular reference.

The same rules apply recursively.

An occurrence may therefore become compressed in both axes.

### Compress While Editing

Given staged A:

1. traversal requires space;
2. A compresses normally;
3. staged state remains authoritative in Rust;
4. compact A indicates staged state;
5. re-expansion restores editing context.

## Open presentation decisions and settled grammar

### Sibling History

Sibling retention and traversal grouping are settled by grammar §§2.4 and
3.3–3.6: replace an untraversed destination; retain explored alternatives attached
to their original sources. New destinations take source-adjacent cells, retained
source selections promote/exchange branches, and Close reclaims whole-empty bands.
Grouping records equivalent provenance without overriding those placement rules.
Matching visible label text alone does not establish group equivalence.
Additional history beyond those invariants remains open.

### Traversal Provenance Detail

Connector labels and qualifiers intentionally provide a compact account of
traversal provenance. Future design may define how a person inspects richer
details such as:

- the Predicate applied to an Expand;
- the Filters composing that Predicate;
- Dance parameters or other invocation context;
- additional future traversal-operation qualifiers.

That richer inspection experience MUST preserve the distinction between
navigation provenance and semantic relationships.

### Compression Thresholds

Exactly when should a visualizer become:

- partially compressed;
- fully compressed?

This should be informed by implementation experiments and available geometry.

### Horizontal Overflow

Layout overflow and off-viewport placement follow grammar §7.4; surface growth,
pan/zoom, and recovery follow §§4.6–4.7. Exact controls and thresholds remain
presentation decisions. They cannot override preserved topology or minimum
useful extent.

### Vertical Overflow

Layout overflow and off-viewport placement follow grammar §7.4; surface growth,
pan/zoom, and recovery follow §§4.6–4.7. Exact controls and thresholds remain
presentation decisions. They cannot override preserved topology or minimum
useful extent.

### Branch Closing

Branch pruning and focus recovery are defined in grammar §2.9; the old question
of whether closing is supported is superseded. Exact controls remain open.

### Focus Presentation

Define the visual treatment of the active frontier.

## Invariant authority

The [grammar invariants](interaction-grammar.md#10-grammar-invariants) own axis
semantics, lineage preservation, traversal-provenance grouping, occurrence
identity, connector presentation, and geometry. Child
private regions, table ordering, and shared MAP state semantics do not become
Path Inspector invariants merely because they participate in this composition.


Internal property and collection allocation is owned by the [selected Node](../../../node/holon-inspector/design-spec.md#responsive-realization-under-path-inspector), not Path track sizing.
