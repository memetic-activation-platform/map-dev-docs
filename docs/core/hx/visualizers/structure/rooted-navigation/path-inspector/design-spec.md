# Path Inspector Design Specification v0.11

Draft normative design. The first three sections map contracts and dependencies;
Section 4 describes this implementation. The [grammar](interaction-grammar.md)
owns navigation transitions and spatial projection, not the child Slot Contract.
Shared mechanisms remain in [DAHN](../../../../dahn-design-spec.md#43-contracts-and-visualizer-fulfillment).

## 1. Slot Contracts Fulfilled

Path Inspector belongs to the [RootedNavigation family](../kind-spec.md).
It fulfills a selecting owner's compatible RootedNavigation Slot Contract, such
as [Space Navigator's contract](../../../../../space-navigator/space-navigator-design-spec.md#43-rootednavigation-slot-boundary).
Kind membership alone does not establish fulfillment of every containing slot.

| Required concern | Path Inspector's realization |
| --- | --- |
| Rooted exploration | Preserve the supplied root binding and present interaction-derived navigation topology |
| Allocated space | Allocate its own tracks, channels and child rectangles within the containing grant |
| Recoverable context | Retain provenance, alternatives and meaningful occurrence state; expose viewport recovery |
| Parent interactions | Delegate new rooted contexts and preferred-extent/attention requests to the immediate owner |

Selection, admission, lifecycle and failure use the [shared DAHN mechanisms](../../../../dahn-design-spec.md#visualizer-operators-and-operations).
This document adds only the Path-specific obligations below.

## 2. Applicable Subject Types

The current `PathInspector.RootedNavigationVisualizer` declares `ApplicableToType`
at `HolonType.TypeDescriptor`. Supported subtype applicability follows DAHN's
Type/selection rules and the selecting slot's additional requirements. It has no
intrinsic HolonSpace, Space Navigator or AgentSpace dependency.

The supplied Holon's Type classifies the **anchor**. The structural subject is
the rooted navigation topology unfolded through interaction, not just that one
Holon. Reaching the same semantic Holon again can produce a distinct occurrence.

## 3. Child Slots and Their Contracts

### 3.1 Node Inspector slot

`NodeInspector.VisualizerSlot` is the conceptual role name. The existing declared
identity is **`PathInspector.RootNodeSlot`**, owned through `HasSlot`; this text
introduces no schema rename. Its accepted Type is `NodeVisualizer.HolonType`.
The role repeats once per navigation occurrence, including the root. Each binds
the represented Holon and its real reference/execution context, not a geometry
wrapper or the Path Inspector's own subject.

The following contract is authoritative independently of any concrete fulfilling
Node. It does not require a particular child composition or layout.

### 3.2 Presentation participation

| Presentation experience | Observable obligation |
| --- | --- |
| Properties | Inspect the bound Holon's properties/details and retain access to applicable singular and collection navigation |
| Collection | Present the active collection and its navigation/actions; retain an accessible return to Properties |
| Relationship | Keep singular navigation usable, with recognizable identity and Restore |
| Compact identity | Preserve recognizable identity and keyboard-accessible Restore; adapt to the rectangle's aspect ratio |

These four experiences are slot-specific, not universal Node-kind requirements.
A substitute need not have a properties pane, vertical rail, tabs or table.
**Inspect is a request to resume the remembered Properties or Collection view,
not a fifth mode.** Singular-navigation context requests Relationship; compact
context requests Compact identity. Collection-navigation context preserves usable
collection access and an existing active collection, with local Properties/Collection
switching permitted in that same allocation.

Local switching updates per-occurrence memory. Relationship and Compact identity
do not overwrite it. New ordinary occurrences start in Properties. Specialized
defaults require an explicit binding; Restore resumes memory rather than restarting
the default. A child need not report its private mode or replay its local history
to the parent. Allocation updates alone preserve the current presentation.

### 3.3 Allocation and callable participation

Path supplies one coherent assignment: the final shared-column width and
shared-row height, together with any explicit presentation request owned by the
operation. Dimensions-only delivery retains the current view. No independently
mutable axis-state, capability-set and private-mode triple is required.

The required local presentation Operator is conceptually `ApplyNodePresentation`.
Its revised input domain is this contract; incompatible existing signatures require
explicit migration rather than relabeling. It is a Visualizer Operation, not a Dance.
The [DAHN invocation mechanism](../../../../dahn-design-spec.md#visualizer-operators-and-operations)
owns declaration, selection, binding and generic failure semantics.

Applying the assignment validates it completely before publication, accepts it
synchronously or returns an explicit refusal preserving the last valid view.
Acceptance is not a browser-paint guarantee. Applying geometry does not discover
content, invoke Dances, request enlargement or reselect a Visualizer. Ordinary
interaction/data binding may load content through its existing authorities.

The owner-declared participation policy specifies supported default and minimum
width/height budgets for these experiences, local switching and connector channels.
Eligible participants promise those obligations before selection; accepted Types,
offered Operators and callable admission are evidence of compatibility, not proof
of complete behavioral conformance. A failure on a valid grant is a contract
violation with explicit recovery, not late minimum negotiation or automatic reselection.

### 3.4 Outputs, state and recovery

| Child output | Path responsibility |
| --- | --- |
| Singular navigation / member navigation | Apply the [grammar's destination transition](interaction-grammar.md#destination-first-transitions) with bound occurrence and provenance |
| Restore | Grant usable inspection allocation and reveal the occurrence; child resumes remembered full-content view |
| Preferred extent / attention | Decide within current authority or delegate through the immediate parent |
| Close / new rooted context | Apply the grammar's guarded closure or delegate a new context; do not dispose borrowed semantic state |
| Inspect selected participant | Inspect the actual occurrence and selected Visualizer, independently of its Holon identity |

Local Properties/Collection switches emit no Path event, change no Path focus and
request no track resize. All outputs are bound to the actual requesting occurrence;
a child cannot resize a sibling or claim another occurrence's authority.

Subject, occurrence identity, selected implementation, references, edits, active
collection and meaningful child state survive resizing, hiding and restoration.
Hide/show alone does not refetch or recreate selected children. Hidden content is
inert. Pending, failed and realized destinations use the same allocated rectangle.
A compact or failed occurrence must retain an owner-provided recovery route;
offscreen recovery may require Pan followed by Restore.

### 3.5 Shared occurrence actions

Explore-from-here, Close, Expand/Restore and Show Visualizer are centrally declared
standard occurrence actions, supplied through shared composition rather than a
handwritten list in each Node. Their bindings retain real occurrence authority
and explicit availability/reasons. Show Visualizer targets that Node occurrence;
each other selected participant has its own actual inspection identity.

The contract requires accessible behavior, not a title-specific action renderer.
A common ActionBar may mix these with subject actions through the
[shared ActionBar contract](../../../../dahn-design-spec.md#action-selection-and-activation-boundary).
Legitimate unavailability does not remove required membership. Direct v display
may be responsive; every v that is shown has one unambiguous inspection target.

## 4. Internal Design and Interaction

### 4.1 Occurrence composition and authority

    containing RootedNavigation slot
      <- Path Inspector
        -> repeated Node Inspector slot
          <- a compatible selected Node
            -> that Node's declared child slots

This describes actual selection boundaries, not all visible regions. Track
calculations, coordinate transforms, connector routing and DOM wrappers are
private implementation mechanisms. Meaningful additional choice points require independent Slot Contracts, with
actual declarations and migration status stated honestly. Private geometry alone
does not create another choice point; current selector cost does not remove one.

Path owns topology, occurrence identity, navigation focus, tracks, connectors and
view. The selected Node owns its internal allocation, local view memory and child
state. Path does not contract directly with a Node's grandchildren. Semantic data,
transaction participation and Undo remain under their existing owners.

### 4.2 Shared-track allocation

Path assigns widths to columns and heights to rows. Every occurrence in a column
receives that width, every occurrence in a row that height; their intersection is
the allocated rectangle. Node implementations allocate their own immediate children.
Rendered descendant content never sets ancestor tracks through upward negotiation.

Path computes shared-track geometry separately from per-occurrence presentation.
A Compact identity occurrence remains Compact in a wide column or tall row.
Shared dimensions do not force Inspect or simultaneous navigation contexts.
Internal measuring, wrapping, responsive choices and owned scrolling remain valid.

Use explicit default/minimum budgets resolved from parent policy and applicable
Theme/MDS inputs. Numeric values are configuration, not modes or child-reported
content heights. Prefer comfortable slack; reduce it toward useful minima when
needed, then retain usable geometry and move the viewport. Typography stays stable.
The grammar owns [preferred footprints and constrained viewports](interaction-grammar.md#7-preferred-footprint-and-constrained-viewports).

### 4.3 Parent requests, Restore and view

A preferred extent is a request, not a grant, and passes through immediate parents.
Each composition owner accounts for its own outer framing once. Normal navigation
does not require native-window growth. Path never bypasses Canvas/Window Manager
ownership to resize a host window.

Restore, branch reactivation, Close and re-root are distinct operations under
[grammar section 4](interaction-grammar.md#4-restore-and-backtracking) and
[section 5](interaction-grammar.md#5-new-and-retained-alternatives).
Direct Restore expands/reveals in place; it does not promote an alternative.
Panning changes view, not topology or remembered child state. Zoom to Fit is
explicit and view-only. An oversized target is revealed at its top so identity
and recovery controls remain reachable.

Occurrence attention is a separate immediate-parent operation. A granted bounded
attention rectangle can temporarily hide/inert ordinary-grid presentations while
retaining the same mounted participant, topology and stored tracks. It does not
resize an individual grid cell or a native window. Restore uses the current grant,
not stale pixels; inability to support useful inspection returns to the ordinary
recoverable surface. It does not introduce another Node presentation mode.

### 4.4 Loading and semantic state

Use the [destination-first sequence](interaction-grammar.md#destination-first-transitions).
Discovery, destination existence and realization are distinct. Unknown or failed
inspection is not verified zero; empty navigation preserves the existing destination.
A target disappearing after allocation produces local changed/empty feedback there.
Superseded requests cannot overwrite newer destinations or counts.

Editing does not inherently disable navigation. Compression, Close and re-root
must not commit, abandon, revert or dispose externally owned staged work. Releasing
an occurrence releases its presentation bindings, not borrowed transactions.

## References and revision

Transition examples and unresolved concrete allocation cases are in
[grammar sections 8–9](interaction-grammar.md#8-mixed-paths-specific-contract-questions).
The current four-mode design supersedes the nine-state capability matrix,
simultaneous properties/collection allocation and content-driven track sizing.
Earlier revisions remain in Git history; documentation is not proof of implementation
conformance or authorization to migrate runtime contracts.
