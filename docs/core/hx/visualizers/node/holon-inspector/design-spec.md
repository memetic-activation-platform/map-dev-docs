# Holon Inspector Design Specification

Draft normative design for a concrete [Node](../kind-spec.md). The opening sections
map actual contracts and dependencies; Section 4 describes this implementation.
Shared selection, Operators, usage and lifecycle rules remain in
[DAHN](../../../dahn-design-spec.md#43-contracts-and-visualizer-fulfillment).

## 1. Slot Contracts Fulfilled

Holon Inspector fulfills compatible owner-defined Node slots, including
[Path Inspector's Node Inspector Slot Contract](../../structure/rooted-navigation/path-inspector/design-spec.md#3-child-slots-and-their-contracts).
Its four-mode realization is the central interaction model:

| Required experience | Holon Inspector's realization |
| --- | --- |
| Properties | PropertyMap/details with singular rail and collection tabs; viewer hidden |
| Collection | Active collection/actions and tabs with visible Properties return control; properties and singular rail hidden |
| Relationship | Singular rail with identity and Restore |
| Compact identity | Recognizable identity and Restore, responsive to aspect ratio |

This is a fulfillment map, not a second definition of the incoming contract.
Inspect resumes remembered Properties or Collection; it is not a fifth mode.
The Slot Contract remains implementable without this document or these private regions.

## 2. Applicable Subject Types

`HolonInspector.NodeVisualizer` declares `ApplicableToType` at
`HolonType.TypeDescriptor`, with subtype behavior under DAHN selection. The same
subject binding can represent saved, staged, newly created or cloned Holons, whether
opened as a root, reached by traversal or returned by a Dance. Additional eligibility
comes from the selecting Slot Contract and supported participation policy.

Semantic applicability does not prove contract fulfillment. This implementation
is an ordinary generic candidate, not a hard-coded fallback. Specialized result
inspectors may use narrower applicability and shared presentation mechanisms; their
binding semantics remain in the specialized specification.

## 3. Child Slots and Their Contracts

The following inventory distinguishes **declared slots** from private regions.
Identifiers describe the inspected schema; it does not create slots to match a diagram.
All declared children use the [shared lifecycle, allocation and failure rules](../../../dahn-design-spec.md#visualizer-operators-and-operations).
The parent supplies the actual subject/context and allocated rectangle; hidden
instances retain meaningful state, and replacement follows ordinary selected-child
admission and disposal. Only slot-specific additions are stated below.

### Declared slot contract map

| Declared identity | Bound subject / presence | Required contract and slot-specific behavior |
| --- | --- | --- |
| `HolonInspector.TitleBarSlot` | The bound Holon and identifying context; one | Accept `TitleBarVisualizer.HolonType`; fulfill the [shared title contract](../../../dahn-design-spec.md#title-bar-participation), including `ApplyTitlePresentation`, unchanged semantic subject and identity/Restore access |
| `HolonInspector.ActionsSlot` | Parent-supplied actions and authorized activation context; one | Accept `ActionBarVisualizer.HolonType`; require [PresentActions](../../../dahn-design-spec.md#action-selection-and-activation-boundary); parent supplies membership through `NodeActions.Contract`, including standard occurrence actions and applicable subject actions |
| `HolonInspector.PropertyMapSlot` | Property facet of the bound Holon; retained while hidden | Accept [PropertyMap](../../property-map/kind-spec.md); own property label/value composition, edit bindings and local scrolling; not the Node's ancestors' sizing |
| `HolonInspector.CollectionsSlot` | Active array, relationship or Dance-result collection; conditional | Accept [Collection](../../collection/kind-spec.md); receive actual membership/context and allocation, preserve collection selection/sort/filter/scroll, emit bound Holon-member navigation; do not allocate destination Nodes |
| `LoadHolons.DiagnosticsSlot` | Workflow diagnostic collection; conditional | Accept Collection; preserve diagnostic evidence and emit bound inspection through the workflow owner under [Data Loader presentation ownership](../../../../dancers/data-loader/data-loader-design-spec.md) |
| `LoadHolons.CommittedHolonsSlot` | Workflow committed-Holon collection; conditional | Accept Collection; inspect retained committed members through their actual reference ownership, within the workflow lifetime defined by the same Data Loader contract |
| `HolonInspector.SingleValueSlot` | Declared child-Node role; no current live binding | Schema accepts `NodeVisualizer.HolonType` and requires `ApplyNodePresentation`. Its owner-specific behavioral contract is incomplete. Actual reached Nodes are owned by Path's repeated Node slot; this declaration must not be portrayed as a realized child or used to infer a second navigation owner. |

The last row is an explicit contract gap, not an invented fulfillment claim. It
needs reconciliation before activation; current navigation continues through the
actual containing owner's Node slot. An accepted Type and Operator do not fill in
missing behavioral requirements.

### Meaningful choice points awaiting schema migration

The following are target child Slot Contracts, independent of the current rail/tab
realizations. They preserve agent choice without claiming that executable slot/type
identifiers already exist. Their structural declarations and callable identities
must be grounded before selection is activated; no schema rename is implied.
In particular, the singular-navigation choice point is not the existing child-Node
`HolonInspector.SingleValueSlot` under a new name.

| Target choice point | Supplied subject/context | Required observable participation |
| --- | --- | --- |
| Singular navigation | The bound Holon's descriptor-derived singular-navigation affordance set, with stable entry identities, labels, availability/existence and supplied navigation bindings | Present accessible singular choices within its allocated region; preserve meaningful ordering, focus and state across updates/hiding; emit the selected bound affordance through owner authority without allocating destination Nodes or invoking an unrelated action |
| Collection index | The bound Holon's collection-shaped affordance set, active selection and availability, including arrays and applicable Dance results | Present accessible collection choices within its allocated region; preserve stable selection/order/focus across updates/hiding; emit a bound local activation intent to the owner, which owns active collection binding and Properties/Collection switching; do not create Path destinations |

Both contracts inherit shared allocation, state-survival, lifecycle and explicit
failure rules. The parent supplies the actual semantic/context bindings and valid
rectangle; a participant adapts internally and never sizes ancestor tracks. Applying
presentation updates does not execute Dances. Selection compatibility must include
the supported contract and callable participation, not just a family label.

Non-normative alternatives include a rail or compact menu for singular navigation,
and tabs or a selectable list for collection indexing. No such rendering is a
requirement of its Slot Contract. Accepted schema Types and Operator identifiers
remain explicit migration questions; do not invent a new kind from a region's name.
Current embedded controls must not be falsely shown as independently selected
children in inspection before that boundary is realized.

### Private implementation details

The Properties return control, layout calculations, DOM wrappers and local spacing
need not be separate Slots. Actions remain components of the selected ActionBar
under its agreed granularity. Shared code helpers do not themselves imply semantic
selection boundaries. This distinction follows substitutability and agent agency,
not a desire to reduce selection calls. Current embedding is not evidence that a
meaningful choice point should be removed or consolidated.

## 4. Internal Design and Interaction

### 4.1 Four-mode realization

Properties and Collection share the **same main content region**. The Node allocates
that region from its parent's grant; selected child content cannot negotiate ancestor
tracks. In Properties, show properties and the singular rail, keep collection tabs
available, and hide the collection viewer. In Collection, hide properties/rail and
show tabs, collection actions and the active viewer. No open collection competes
with a small simultaneous properties pane.

Relationship prioritizes usable singular navigation where available, identity and
Restore. Path may assign it after collection-member traversal when compressing a
shared column; the Collection interface can be hidden without changing traversal
provenance or remembered Collection state. Compact
identity has wide/shallow, narrow/tall and small responsive realizations, not separate
horizontal, vertical and both-axis modes. Extra space can expose identity details
or actions without automatically requesting normal inspection.

The selected identity presentation and the Node's **one ActionBar** may be co-located
in the title band. Standard controls use proper icons with accessible labels and
responsive overflow. Subject and occurrence actions may mix; neither membership
source nor activation target is the bar's concern. The shared membership/helper
mechanism avoids each HX author remembering a list. Presentation updates do not
execute actions; domain/workflow execution remains outside the bar.

### 4.2 Local Properties and Collection switching

A populated collection-tab activation enters Collection in the existing rectangle.
A shallow full-width **Properties** header above the tabs remains visible and returns
to Properties. Both are local operations, even while this occurrence is a navigation
source. They emit no Path event, change no navigation focus and request no parent resize.

A collection activation obtains the membership/result and selects its compatible
Collection presentation after establishing the internal region. Pending, empty,
failure and resolved feedback belong there. Verified empty relationship activation
preserves the current selection and view; arrays and explicitly invoked Dance
results can have meaningful empty presentations. Switching collections reuses the
region and preserves retained child/view state as applicable.

Ordinary member selection remains local; member navigation (currently double-click)
emits a bound request to the containing navigation owner. Only that owner allocates
a destination occurrence. Local collection opening never deletes prior Path history.

### 4.3 Remembered view and Restore

Each occurrence remembers its last full-content view, Properties or Collection,
including the chosen collection. Local switching updates that memory. Relationship
and Compact identity do not. Hiding retains selected child identities, reference
bindings, membership, selection, sort/filter, scroll and edits; hide/show alone does
not refetch or reconstruct content. Hidden regions are inert and outside keyboard
navigation. Semantic invalidation remains a separate data-lifecycle event.

Restore requests usable inspection allocation through the immediate parent and,
after a grant, resumes the remembered view. Refusal preserves the valid current
view with a reason. Do not reset to a default or restore old pixel dimensions.
Path’s [retention and Restore precedence](../../structure/rooted-navigation/path-inspector/interaction-grammar.md#contextual-retention-and-explicit-operations)
controls subsequent explicit assignments. A shared-column enlargement for a restored
sibling does not itself restore this occurrence’s hidden full-content view.
Local return to Properties is distinct from occurrence Restore and has no separate
region-emphasis/maximization state.

### 4.4 Responsive internal allocation

Allocate title/actions, local navigation controls and the main region within the
assigned width/height. Properties uses the main region with owned scrolling;
Collection assigns it to the viewer. Child measurement may wrap controls and manage
local scrolling; no PropertyMap content-height report or measured collection row
count determines ancestor tracks or divides the main region between competing panes.

The singular rail stays right-aligned and capped at its normal Theme-informed
internal width. Surplus lies to its left; narrower grants use wrapping/disclosure
and owned scrolling. Path assigns the column, not rail dimensions. Typography stays
stable instead of shrinking to fit history. Parent policy defines admitted useful
minima; numeric values are not extra modes. Compact always retains recognizable
identity and keyboard Restore, even when direct navigation or a v is suppressed.

Allocation updates alone lay out the current presentation. Explicit parent requests
can change contextual presentation; dimensions do not replay local tab events or
infer a new mode from a large shared-track intersection. Attention/host maximize
remain separate parent-owned operations and do not erase full-content memory.

### 4.5 Descriptor-to-affordance projection

The effective descriptor classifies affordances; this implementation chooses regions.
No compile-time knowledge of each Holon Type is required.

| Effective affordance | Local projection and behavior |
| --- | --- |
| Scalar property (`ValueType` other than `ValueArray`) | PropertyMap/details; selected Value presentation, no hard-coded per-Type renderer or intervening Property Visualizer |
| `ValueArray` property | Collection tab; active values use a Collection; values need not navigate to Holons |
| Singular relationship (maximum at most one) | Singular rail; emit bound singular navigation when a target exists; mutable staged relationships can set/replace/clear |
| Plural relationship (maximum greater than one or unbounded) | Collection tab; selected Holon-member navigation is collection-mediated; edit may add/remove/reorder where allowed |
| Navigational Dance with singular Holon result contract | Singular rail; result/navigation uses the Dance's semantic contract |
| Navigational Dance with plural Holon result contract | Collection tab/result; Holon members can emit member navigation |
| Other applicable Dance | Supplied Action component in the single ActionBar, with authorized execution binding |

Runtime target count and Predicate filtering do not change structural cardinality.
A plural relationship returning one member remains plural; an empty singular stays
singular. Navigational Dance result shape likewise derives from its response contract.
Unknown scalar non-Holon result presentation and exact result-tab styling are bounded
separate presentation questions, not reasons to alter navigation axes.

### Progressive relationship affordances

Normal browsing MUST withhold relationship navigation affordances until runtime
inspection establishes at least one target. Verified empty relationships remain
in descriptor knowledge but are absent from the normal rail and collection tabs.
Unknown, pending, and failed inspection MUST NOT be represented as verified zero.
Discovery failures SHOULD have local diagnostic/retry feedback without presenting
an unverified relationship as a populated navigation destination.

Relationship discovery MUST NOT block initial identity and scalar presentation.
Inspect relationships asynchronously through bounded concurrency and progressively
reveal populated affordances. Preserve descriptor/adaptive/user ordering as results
arrive; completion order does not determine salience. Existence evidence may
precede an exact count: show known collection counts when available, but do not
label a non-empty result as an exact count of one. A singular count can remain
implicit in the rail while its runtime cardinality is retained internally.

Edit mode MUST retain access to mutable empty relationships so a first target can
be set or added. Schema inspection and diagnostics MAY expose defined empty
relationships explicitly. This visibility rule does not apply to array-valued
properties or require speculative Dance invocation.

Automatic discovery and known-count display are the normal browsing defaults;
`Show Counts` and `Hide Empty` controls are not prerequisites. Specialized modes
may retain such controls where useful.

### 4.6 Editing, creation and semantic ownership

Read and edit share one descriptor-driven visual grammar. PropertyMap/Value children
present editable controls where permitted; read-only values remain inspectable.
The staging/commit model, transaction status and semantic operations retain their
own authority. Entering edit does not inherently disable navigation.

### Entering Edit Mode

When the person selects **Edit** on a persisted holon:

1. MAP stages or exposes a new version of that holon;
2. the existing Node Visualizer occurrence remains in place;
3. the visualizer enters edit mode;
4. editable scalar properties become interactive;
5. editable relationship and collection affordances become mutable where allowed;
6. transaction status becomes visible at Space Navigator scope.

Entering edit mode is a state transition, not a navigation transition.

### Compressing Editable Visualizers

When an editable occurrence is compressed:

- staged data remains intact;
- edit state remains known;
- the compact representation SHOULD indicate staged changes;
- re-expansion restores editable presentation.

Compression MUST NOT:

- Commit;
- abandon;
- revert;
- discard staged changes.

### Create

Create SHOULD use the same editable visual structure as Edit.

A preferred generic entry point is an applicable concrete Holon Type descriptor.

When **Create Instance** is invoked:

1. a new staged holon of that type is created in the active Space;
2. defaults are applied where defined;
3. a Node Visualizer presents the new staged holon in edit mode;
4. editing uses normal descriptor-driven PropertyMap, Value and Collection Visualizers, with supplied Action components;
5. the new holon participates in the active transaction.

Create does not require a separate form architecture.

### Clone

When **Clone** is invoked:

1. MAP creates a new staged holon initialized from the source according to clone semantics;
2. the new holon receives its own semantic identity;
3. it is presented in normal edit mode;
4. it participates in the active transaction.

Clone source history is not automatically treated as Space Navigator traversal provenance.

After staged initialization, Clone and Create use the same editing interaction model.

### Delete

Delete is a holon-scoped action.

When invoked:

1. the person receives any required explicit confirmation;
2. deletion is staged according to MAP semantics;
3. the staged deletion participates in the active transaction;
4. Commit later publishes it with other staged changes.

Delete MUST NOT imply physical erasure of historical committed state.

The exact post-Commit presentation of deleted holons remains a design detail to refine.

### 4.7 Specialized loading and configuration

The loader binding supplies authoritative outcome properties, diagnostics, committed
members and navigation context to shared inspector behavior. Its accepted initial
view is Properties with outcome/available diagnostics; selecting result collections
switches locally to Collection. Restore resumes the last view. It does not need a
copied geometry shell or a table-specific navigation contract. The
[Data Loader specification](../../../../dancers/data-loader/data-loader-design-spec.md)
owns workflow semantics and actual reference/context lifetimes.

Property, rail, tab and action ordering can change locally where offered. Persistence,
preferences and collective reporting follow [DAHN usage and adaptation](../../../dahn-design-spec.md#111-visualizerusage).
A reorder or navigation gesture is not itself authorization for durable preference
or background persistence. Shared Visualizer definitions and semantic Holon data
are not modified by local personalization.

### 4.8 Conformance examples

| Event | Local experience | Memory and state | Parent geometry |
| --- | --- | --- | --- |
| Properties→Collection→Properties | Switch the main region's content | Retain collection child, selection/sort/scroll and properties/edits | Unchanged |
| Properties→Relationship→Compact→Restore | Resume Properties after a grant | Properties/edit state retained | Current parent policy, not saved pixels |
| Collection→Compact→Restore | Resume same active Collection | Same selected collection and view state | Current parent policy |
| Compact at different aspect ratios | Responsive identity/Restore | Full-content memory untouched | Do not infer Inspect from surplus space |
| Resize / unrelated shared-track change | Adapt the current experience | Selected children and local view survive | Parent assignment applied without upward content negotiation |

Pure-axis and retained-alternative walkthroughs belong to the
[Path grammar](../../structure/rooted-navigation/path-inspector/interaction-grammar.md#2-pure-vertical-transitions).
These examples do not prove implementation conformance. The four-mode realization
supersedes simultaneous properties/collection sizing and old local-region emphasis;
historical revisions remain in Git history.
