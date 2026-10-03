# Path Inspector Design Specification v0.3

## Change Log

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

| Role | Bound subject | Participation boundary |
| --- | --- | --- |
| Node slot | Holon represented by that navigation occurrence, with effective descriptor and context | Accepted Node Visualizer type plus the existing two-axis extent/state protocol in grammar §4.4.1. |

DAHN resolves each actual child slot under the
[slot-directed selection policy](../../../../dahn-design-spec.md#1421-slot-directed-descriptor-selection).
Node kind membership alone does not prove compatibility with the Node slot's
participation requirements. Path Inspector supplies the selected axis states
and allocation; the child owns its internal realization. This specification
states observable participation obligations without defining new contract-type
schema, invocation vocabulary, or occurrence persistence.

Collection-mediated navigation records the source collection and selected
member as provenance. In the Holon Inspector composition, the Node owns its
CollectionViewerSlot and binds its active collection. That nested Collection
slot does not become a direct Path Inspector slot merely because Path Inspector
coordinates traversal from a member-selection intent. A future direct Collection
slot would need its own explicit contract and subject binding.

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

The Rooted Navigation Visualizer SHOULD preferentially allocate its
Canvas-provided real estate toward this frontier.

Prior contexts progressively compress away from it.

> **The Rooted Navigation Visualizer allocates its Canvas-provided
> space toward the active traversal frontier and compresses provenance behind it.**

## Applying the Interaction Grammar

The [interaction grammar](interaction-grammar.md) owns spatial productions.
The following describes how semantic navigation intents from children invoke
those productions. Rail/tab/row examples describe the Holon Inspector and Table
realizations; a conforming substitute can supply the same intent differently.

### Horizontal Navigation

Activating a structurally singular rail entry invokes the Grammar's horizontal
traversal rule. The target Node opens immediately to the right of the source
occurrence and shares its row. The intervening traversal channel exposes the
affordance through which the target was reached.

Switching eligible rail entries follows
[Activation](../../../node/holon-inspector/design-spec.md#activation): an
untraversed leaf MAY be replaced. When retained alternatives must coexist,
targets reached through the same affordance remain spatially grouped; a newly
traversed target becomes the bottom-most member of its relationship group while
remaining row-aligned with its source. Existing groups and their retained
branches reflow under the Path Inspector grammar rather than being discarded or
reattached.

### Vertical Navigation

Activating a structurally plural affordance exposes its Collection Visualizer.
Navigating a holon row invokes the Grammar's vertical traversal rule and opens
the child Node immediately below the source navigation stage in the same column.
The intervening traversal channel exposes the affordance through which the
target was reached. The Collection keeps sibling context available.

Active member changes obey the grammar's retained-path rules: a traversed
continuation is not discarded merely because another member becomes active.
When retained alternatives through the same affordance coexist, they remain
spatially grouped; a newly traversed target becomes the right-most member of its
relationship group while remaining column-aligned with its source. Existing
groups and their retained branches reflow under the grammar.

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
The final destination region is the source-aligned position derived by the
grammar, including any relationship-group reflow required to make that position
available. A lightweight temporary presentation MUST occupy that final region
before the actual visualizer appears. For example, show `Opening DescribedBy…`
in the immediately right-hand Node slot or `Opening Orders…` in the collection
region beneath the source. This communicates destination and intent; it need not
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
2. establish B's destination immediately below the source navigation stage and
   in the same column;
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
3. partially compress expanded A and establish B's destination immediately to
   A's right in the same row;
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
3. establish the destination under the ordinary source-alignment,
   destination-first, grouping, and reflow rules;
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

if H1 traverses R1 again to H1.3:

1. H1.3 opens immediately to the right of H1 and in H1's row;
2. H1.3 joins the existing R1 relationship group as its bottom-most member;
3. the retained H1.1 branch remains in the R1 group and may move upward;
4. the R3 group, including H1.2 and its retained descendants, may move downward;
5. the R1 targets remain contiguous and may share the R1 traversal label;
6. occurrence identity, provenance, and descendant attachment remain unchanged.

The visible reflow expresses relationship grouping without changing the
navigation topology.

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

The horizontal grouping rule has an orthogonal vertical counterpart. If a
source traverses again through a plural affordance for which retained member
branches already exist:

1. the new target opens immediately below the source navigation stage and in
   the same column;
2. it becomes the right-most member of that relationship group;
3. existing members of the same group may move left;
4. later relationship groups and their retained branches may move right;
5. same-affordance targets remain contiguous and may share their traversal
   label;
6. occurrence identity, provenance, and descendant attachment remain unchanged.

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
3.3–3.6: an untraversed leaf may be replaced; retained alternatives remain
attached to their original sources, are grouped by equivalent traversal
provenance, and reflow under the appropriate group-aware insertion rule.
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
