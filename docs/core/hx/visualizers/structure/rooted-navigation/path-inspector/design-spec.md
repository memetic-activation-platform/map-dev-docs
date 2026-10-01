# Path Inspector Design Specification v0.1

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
Re-root requests a new context through the host chain under
[grammar §2.7](interaction-grammar.md#27-re-root). It preserves the source by
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
traversal rule. The target Node opens to the right of the source occurrence.
Switching eligible rail entries follows [Activation](../../../node/holon-inspector/design-spec.md#activation): an untraversed leaf MAY be
replaced; a traversed child and its continuation MUST be displaced and retained
through horizontal alternative insertion under the Path Inspector grammar.

### Vertical Navigation

Activating a structurally plural affordance exposes its Collection Visualizer.
Navigating a holon row invokes the Grammar's vertical traversal rule and opens
the child Node beneath that Collection. The Collection keeps sibling context available. Active member changes obey the
grammar's retained-path rules: a traversed continuation is not discarded merely
because another member becomes active.

### Recursive Exploration and Provenance

Every reached Node may invoke either traversal rule. Path Inspector MUST distinguish
semantic holon identity from visualizer occurrence identity, and provenance
SHOULD record how each occurrence was reached. The same holon may appear in
multiple occurrences with different local selection, focus, visualizer, and
collection state.

## Compression and Editing

Compression applies only to projection and presentation. It MUST NOT discard
the selected collection tab, selected rail affordance, child links, sort/filter
state, selected row, edit mode, staged-state reference, or selected Visualizer
identity. Re-expansion SHOULD restore prior local context where feasible.

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
navigation, use current existence evidence or inspect the relationship. If the
result is zero, indicate locally that it has no targets, refresh its browse
visibility, and leave source extent, focus, and existing destination unchanged.
An invalid singular cardinality follows validation/error semantics.

For a valid destination, establish its region first under [Path Inspector destination-first rule](interaction-grammar.md#28-destination-first-transitions).
A lightweight temporary presentation MUST occupy the final destination region
before the actual visualizer appears. For example, show `Opening DescribedBy…`
in the right-hand Node slot or `Opening Orders…` in the collection region. This
communicates destination and intent; it need not expose technical progress or
be a separately named Visualizer Commons role.

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

Path Inspector derives traversal shape from descriptor-declared cardinality,
not the number of returned targets. A plural relationship or navigational Dance
returning one Holon remains collection-mediated and vertical. A singular
relationship remains structurally singular when empty; target-existence guards
prevent creation of a fabricated destination. A singular target traverses
horizontally. Value arrays need not produce Holon navigation.

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
2. create a Node Visualizer occurrence for B below C;
3. preserve A and C;
4. record provenance;
5. preserve C so sibling rows remain accessible;
6. optionally compress A vertically.

### Follow a Singular Relationship

Given Node A and singular relationship R:

1. discovery establishes R has a target and reveals it in the right rail;
2. activate R and establish valid target existence;
3. partially compress expanded A and allocate the right-hand destination;
4. show `Opening R…` in that slot;
5. resolve B and select/materialize its Node Visualizer in-place;
6. preserve provenance from A through R and the grammar's focus/retention rules.

### Continue Horizontally

Given:

    A -> B

if B opens C:

- C becomes the active frontier;
- B may retain immediate singular-navigation context;
- A may compress more aggressively;
- prior subordinate geometry compresses with its owner.

Repeated horizontal traversal progressively compresses leftward provenance.

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

Sibling retention is settled by grammar §§2.4 and 3.3–3.6: an untraversed leaf
may be replaced; a traversed continuation is retained and displaced under the
appropriate alternative-insertion rule. Additional history beyond those
invariants remains open.

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
semantics, lineage preservation, occurrence identity, and geometry. Child
private regions, table ordering, and shared MAP state semantics do not become
Path Inspector invariants merely because they participate in this composition.
