# Path Inspector Interaction Grammar v0.16

This concrete grammar owns traversal, placement, presentation assignment,
backtracking, alternatives and viewport movement. The
[Node Inspector Slot Contract](design-spec.md#3-child-slots-and-their-contracts)
is defined in the design spec, independently of its fulfilling implementations.

## 1. Small State Model

- **Occurrence:** one presentation of a bound Holon, with distinct occurrence identity,
  selected implementation and local state even when another occurrence shows the same Holon.
- **Topology:** the root, recorded parentage and retained continuations, separate from grid coordinates.
- **Focus:** the active navigation occurrence; visibility alone does not change it.
- **Projection:** shared columns/rows, sparse cells, channel geometry and rectangles.
- **Presentation assignment:** an occurrence's semantic presentation requirement,
  distinct from its rectangle and its child's private layout/state.
- **Viewport:** the visible part of the retained surface; pan and zoom are view operations.

Traversal provenance records source occurrence, axis and affording relationship or
Dance, with relevant Predicate/parameters and collection/member identity. A traversal
group records equivalent provenance and ordered alternatives, not first-member
spatial ownership. Matching label text alone does not establish equivalent provenance. Connectors display provenance, not newly asserted Holon relationships.

Properties and Collection are full-content experiences; Relationship and Compact
identity retain the remembered full-content view. Inspect resumes that view.
Neither shared-track aspect ratio nor history length determines a child's mode.

## 2. Pure Vertical Transitions

Selecting a collection tab opens/switches that collection locally. Properties and
Collection use the same Node rectangle; the operation emits no Path event.
Ordinary member selection remains local. Member navigation (currently double-click)
emits an occurrence-bound request through an already-open collection.

Path verifies the destination, applies the placement rules, reserves its rectangle
below the source and reveals it before showing resolved content. The source already
presents its collection: do not collapse it again merely to expose that collection.
It stays in Collection while the parent may assign the explicit collection-context
height from policy. This is a parent allocation operation, not a child size request.
The destination opens in Properties with normal inspection allocation.

Further downward traversal makes older context Compact and advances the viewport,
while retaining topology, provenance and child state. A local return to Properties
remains permitted in a contextual source's existing rectangle, without Path focus
or allocation changes.

### Pure vertical walkthrough

`W` is the shared column width; `Hi`, `Hc`, `Hk` are explicit inspection,
collection-context and compact row budgets. `Hc` may equal `Hi`; a reduced value
must still support the slot's permitted local switching. Channels occupy separate
space. These symbols are policy values, not measured child extents. In memory columns,
α/β/γ denote remembered Collection views, not just collection identifiers.

| Event | Occurrence presentation | Remembered view | Allocated rectangle | Preserved state |
| --- | --- | --- | --- | --- |
| Open A | A:Properties | A:Properties | A:W×Hi | Bound subject and selected children |
| Open collection α | A:Collection | A:Collection α | Unchanged | Hidden properties/edits |
| Click Properties | A:Properties | A:Properties | Unchanged | α's child, selection, sort and scroll |
| Reopen α | A:Collection | A:Collection α | Unchanged | Same collection state |
| Navigate to B | A:Collection; B:Properties | A:α; B:Properties | A:W×Hc; B:W×Hi | No second source collapse; pending/final B share a rectangle |
| Open B's collection β | A:Collection; B:Collection | A:α; B:β | Unchanged | Hidden B properties |
| Navigate to C | A:Compact; B:Collection; C:Properties | A:α; B:β; C:Properties | A:W×Hk; B:W×Hc; C:W×Hi | A retains α despite compaction |
| Open C's collection γ | A:Compact; B:Collection; C:Collection | A:α; B:β; C:γ | Unchanged | Local switching only |
| Navigate to D | A,B:Compact; C:Collection; D:Properties | A:α; B:β; C:γ; D:Properties | A,B:W×Hk; C:W×Hc; D:W×Hi | History and local state retained |

The mature preferred visible footprint is Compact identity + labeled connector +
Collection context + labeled connector + Properties inspection. A can move offscreen.
All occurrences share W, including Compact ones: width does not upgrade presentation.

## 3. Pure Horizontal Transitions

A structurally singular affordance emits singular navigation. After establishing
existence, Path assigns the source its singular-navigation column budget, requests
Relationship presentation and reserves the rightward destination in Properties.
The source no longer presents properties or its collection interface. This operation
belongs to Path, not to the child's internal rail.

| Event | Occurrence presentation | Remembered view | Allocated rectangle | Preserved state |
| --- | --- | --- | --- | --- |
| Open A | A:Properties | A:Properties | Wi×H | Subject/children |
| A navigates to B | A:Relationship; B:Properties | A,B:Properties | A:Wr×H; B:Wi×H | A's hidden full-content state |
| B navigates to C | A:Compact; B:Relationship; C:Properties | A,B,C:Properties | A:Wk×H; B:Wr×H; C:Wi×H | Occurrence identities and provenance |
| C navigates to D | A,B:Compact; C:Relationship; D:Properties | A,B,C,D:Properties | A,B:Wk×H; C:Wr×H; D:Wi×H | Retained history; advance viewport |

H is shared across the row. The preferred visible footprint is Compact identity +
labeled connector + Relationship context + labeled connector + Properties inspection.
A compact occurrence remains Compact even when that row is tall.

## 4. Restore and Backtracking

Direct Restore requests expanded inspection from the immediate parent, reveals the
occurrence and resumes its remembered Properties or Collection view after the grant.
It preserves topology, row/column placement and the source's selected continuation.
It never restores saved pixel dimensions or promotes an alternative branch.
Pan alone can reveal an offscreen occurrence without changing its presentation.

| Event | Occurrence presentation | Remembered view | Allocated rectangle | Preserved state |
| --- | --- | --- | --- | --- |
| Restore B in the vertical walkthrough | B:Collection β | B:Collection β | Current policy inspection grant, in B's existing cell | β's selected child, selection, sort, scroll and edits |
| Restore B in the horizontal walkthrough | B:Properties | B:Properties | Current policy inspection grant, in B's existing cell | Properties/edits and provenance |
| Restore a Properties→Relationship→Compact occurrence | Properties | Properties | Newly granted rectangle | Same meaningful local state |
| Restore a Collection→Compact occurrence | Same active Collection | Collection | Newly granted rectangle | Same collection state |

Backtracking through a source to an existing destination is branch reactivation
under section 5, not direct Restore. Scanning an existing lineage changes focus/view
without replacing topology, parentage or provenance. Explicit presentation changes
follow the operation; resize does not replay earlier navigation or local-tab events.

### Close and re-root

Close removes the selected occurrence and its descendants subject to dismissal,
active-workflow and state-safety guards. Shared ancestors and unrelated branches,
including other occurrences of the same Holon, survive. If focus is removed, focus
moves to the nearest surviving ancestor or clears. Closing the root leaves an empty
navigation topology, not an implicitly destroyed top-level context.

Reclaim only wholly empty rows/columns, shifting subsequent bands together.
Partially occupied bands and legitimate sparse cells survive; do not repack unrelated
Nodes into holes or promote an alternative just to fill a canonical cell. Closing
presentation must not discard external staged edits, Nursery state or Undo history.

Re-root requests a **new** exploration context anchored at the occurrence's Holon.
The source topology and descendants remain intact. Space Navigator delegates this
to its owning Dancer under its [new-context contract](../../../../../space-navigator/space-navigator-interaction-grammar.md#23-new-exploration-context-requests).
Replacing the current root is a separately named operation. Neither action implicitly
transfers, commits or abandons semantic state.

## 5. New and Retained Alternatives


`branch(anchor, continuation)` retains an additional continuation from an existing anchor when the continuation currently selected from that anchor has already been traversed onward.

A new destination selection from the same source replaces its current untraversed
destination, subject to the existing dismissal and state-safety guards. Once
navigation has continued through that destination, the occurrence and its
continuation are retained history and MUST NOT be overwritten by another selection
from the source. Retain that destination with its descendants as an alternative.
Restoring an already retained destination is distinct from creating a replacement.

### Whole-band insertion for first-time destinations

When establishing a source's rightward destination for the first time, insert a
whole column immediately right of the source. Shift all existing columns at or
beyond the insertion point rightward, across every row, then place the destination
in the new column at the source row. Establishing its downward destination for
the first time inserts a whole row immediately below the source stage: shift all
existing rows at or beyond that point downward, across every column, and place
the destination in the new row at the source column.

Insert the band even when the target intersection in an existing band is empty.
An empty intersection does not authorize reuse of that band. Preserve occurrence
identity and provenance as whole-band coordinates shift. A replaced untraversed
destination reuses its established cell. Retained-alternative displacement and
source-driven branch reactivation follow the rules below, rather than allocating
a new forward band for every repeated selection.

For A→B with an older A↓X, first B↓C inserts a row immediately below A/B.
C occupies the new row under B; X's entire row moves down. C and X do not share
a row merely because they could fit at different column intersections.

### Source-adjacent placement of a new destination

Every newly created destination takes the source-adjacent canonical position:
immediately right of its source in the source row for horizontal traversal, or
immediately below its source stage in the source column for vertical traversal.
This applies even to another selection through the same relationship or equivalent
traversal provenance. A traversal group does not reserve that position for its
first member or force a new destination to a terminal append position.

If the previous destination is untraversed, replace it under the state-safety
rule above. If it has been traversed onward, retain its occurrence and descendants
as an alternative. Move the retained horizontal continuation downward, or the
retained vertical continuation rightward, as needed to free the canonical position.
Preserve branch identity, provenance, contracted state and internal relative
geometry. Existing retained alternatives keep their relative order during that
outward displacement. Grouping records semantic provenance; it must not override
source-adjacent placement of a new destination.

For A→B→C, selecting a new D from A places D immediately right of A and moves
the retained B→C continuation down intact. The vertical counterpart moves an
explored prior continuation rightward while the new destination takes the cell
immediately below the source stage. New destination creation never pulls retained
history upward or left to manufacture room. Whole-band insertion and direct occurrence restoration follow their explicit
rules here and in the Restore and closure rules.

### Selecting a retained destination through its source

When a source selects an already-retained destination, reuse that occurrence and
its retained continuation rather than creating a duplicate or reinitializing its
state. Bring that continuation back to the source-adjacent canonical position.
If the currently selected destination is untraversed, replace it under the ordinary
safety rule. If it has been traversed onward, exchange the two continuations'
branch positions: the outgoing branch takes the alternative position vacated by
the incoming branch. It does not move above or left of the source.

A branch-position exchange is not a promise of identical rectangular footprints.
Unequal footprints may require outward reflow to preserve a valid non-overlapping
grid. Preserve each branch's occurrence identity, provenance, meaningful state and
internal structure. This explicit reactivation can move the incoming retained
branch inward; it is distinct from new-destination creation, whose retained-history
displacement remains outward.

Selecting a destination through its source is distinct from directly restoring
an occurrence in its existing region. Direct Restore preserves topology and
row/column placement; it changes focus, allocation and view as needed to reveal
and expand the occurrence where it already sits. It does not promote a retained
branch or change its source's selected continuation.

This rule supersedes terminal-append and first-member spatial anchoring.
Chronological group membership remains provenance, not a placement override.

> **Replace an eligible leaf; otherwise retain its explored continuation and give
> the new destination the source-adjacent position.**


## 6. Placement and Connector Rules

Each horizontal lineage stays on its projected row and each vertical lineage on
its projected column, with sparse cells where required by truthful topology.
A first horizontal destination is immediately right in the source row; a first
vertical destination is immediately below in the source column. Section 5 owns
whole-band insertion and later replacement/displacement. Sparse intersections are
not occurrences and do not authorize reusing an existing forward band.

Reflow preserves occurrence identity, parentage, group order and descendant
attachment. Connectors follow recorded provenance across sparse cells; geometric
adjacency does not establish navigation parentage. Shared labels may group equivalent
traversals but must keep each destination's attachment understandable.

Use relationship predicate/name or navigational Dance name as the traversal label.
A Predicate-qualified expansion retains its qualifier (for example an inspectable
funnel indicator); filtering does not change structural cardinality or axis.
Runtime zero/one membership does not make a plural affordance singular. Value-array
members need not be Holons and do not inherently emit Holon navigation.

### Destination-first transitions

Establish existence before changing focus, replacing a leaf, inserting a band or
allocating a destination. Verified empty results leave source and existing destination
unchanged with local feedback. Unknown/failed discovery is not empty. Invalid singular
multiplicity follows cardinality error semantics; do not choose an arbitrary target.

For a valid navigation request:

1. Apply section 5 and determine the final source-adjacent destination.
2. Apply the axis-specific presentation/allocation operation, reserve the channel
   and final rectangle, and move the viewport to reveal it.
3. Show localized pending feedback in that rectangle.
4. Replace it with the resolved selected participant, or failure/retry feedback, in place.

Cached content may be ready immediately; no artificial delay is required. Reduced
motion may omit animation but preserves this ordering. A disappearing target is
reported in its allocated destination and discovery refreshed. A superseded request
cannot overwrite a newer destination. Opening a collection inside a Node is local;
it neither creates a Path destination nor discards retained navigation.

## 7. Preferred Footprint and Constrained Viewports

Track and channel dimensions come from the [owner's allocation policy](design-spec.md#42-shared-track-allocation).
Preferred footprints describe a bounded current experience, not the bounding box
of all history:

- Vertical: compact height + channel + collection-context height + channel + inspection height.
- Horizontal: compact width + channel + singular-context width + channel + inspection width.

For the same viewport, Theme and policy, default budgets are stable as history grows.
Reduce padding/channel slack and policy budgets toward declared useful minima when
the actual grant requires it. At minima use owned scrolling and viewport movement;
do not repeatedly shrink all history to keep it visible. No rendered row count or
child content-height report determines ancestor dimensions. A universal number of
visible collection rows is not required.

Apply each resolved dimension to the whole track. Per-occurrence presentation stays
independent: a Compact occurrence can occupy a wide column or tall row. Deliver
final dimensions with explicit presentation requests, without inferring extra
capabilities or forcing both navigation contexts at an intersection.

Advance the viewport to reveal the destination and immediate context where possible.
Older top rows and left columns may leave view. Inbound arrowheads cue actual offscreen
provenance; they do not count hidden Nodes. Where no inbound edge exists, actual empty
channel space may cue more surface. Do not fabricate arrows, leading padding or a
breadcrumb/space reservation for every hidden occurrence.

Pan can recover history, followed by Restore where navigation is unavailable in Compact.
If the target is taller than the viewport, align its top so identity and Restore remain
reachable. Zoom to Fit is an explicit view-only operation. Each composition owner adds
its framing once to preferred-extent requests; a request is not a grant.

## 8. Mixed Paths: Specific Contract Questions

The settled rules remain: latest-source-per-axis retention on the focused ancestry;
no accumulated claims from retained alternatives outside it; shared tracks; independent
occurrence presentations; local full-content switching; and no implicit fifth mode.
A node does not need both contexts merely because its rectangle is wide and tall.

| Concrete scenario | Settled presentation/state | Conflicting requirements and missing decision |
| --- | --- | --- |
| A→B↓C | A:Relationship, B:Collection, C:Properties; A/B share a row | The row must support both context experiences. Exact shared-row budget is policy configuration subject to each minimum, not another mode. |
| A↓B→C | A retains its local full-content view, B:Relationship, C:Properties; A/B share a column | A's admitted collection/full-content minimum can exceed the requested relationship-only column width. The policy must explicitly decide how to reconcile that width: a wider shared column with B's internal navigation capped, or a separately reviewed context change. No silent invalid grant or inferred mode switch. |
| Alternating turns with retained off-ancestry branches | Keep latest contextual source per axis; older unprotected occurrences Compact; alternatives retain state | No new retention rule is missing. If those supported requirements have no valid shared-track assignment, identify the exact policy bounds and occurrences before proposing a change. |
| Direct Restore versus choosing a retained branch | Restore expands in place; source-driven reactivation exchanges branches under section 5 | No topology decision is missing. Any further presentation question must identify the affected occurrence and incompatible grant; it cannot reopen branch promotion or reset memory. |

The width conflict above is an explicit review item, not permission to require
simultaneous Properties and Collection, restore the old partial/partial matrix,
probe descendant content or introduce speculative presentation-history machinery.
A proposed budget is established by the parent and conformance work, not by a child's
late report that it cannot comply. Pure-axis behavior does not depend on resolving it.

## 9. Essential Invariants and Conformance Examples

| Event | Occurrence presentation | Remembered view | Allocated rectangle | Preserved state |
| --- | --- | --- | --- | --- |
| Properties→Collection→Properties | Only the local full-content view changes | Latest chosen full-content view | Unchanged | Selected children, edits and collection view |
| Resize / another occupant enlarges a shared track | Current presentation remains | Unchanged | New valid track intersection | Subject, selected implementation and meaningful local state |
| Compact at wide/shallow, narrow/tall or small aspect ratios | One Compact experience, differently realized | Unchanged | Parent-assigned rectangle | Recognizable identity and Restore |
| Navigation realization fails | Explicit recoverable failure at reserved destination | Prior valid state retained where safe | Pending/failure/final allocation identical | Source and unrelated branches |

These tables are examples of the rules, not independent normative definitions or
proof of runtime conformance. A different Node implementation must be testable from
[the Slot Contract](design-spec.md#3-child-slots-and-their-contracts) alone.

This revision replaces the nine-state capability matrix, intersection overprovisioning,
content-driven allocation and simultaneous properties/collection sizing. It preserves
settled topology and provenance. Prior change histories remain in Git history.
