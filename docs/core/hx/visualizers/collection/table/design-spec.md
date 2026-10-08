# Table Collection Design Specification

## Status and current authority

Draft normative specification for concrete table presentation and interaction.
The Collection kind owns shared subject and mutation semantics; this document
owns rows, columns, sorting, filtering, selection, restoration, and editing controls.

## Purpose and authority

Table Collection is a concrete Visualizer in the
[Collection family](../kind-spec.md). Its specification owns the experiential
realization behind the slot contract it fulfills.

## Contract fulfillment and semantic subject

The supplied collection projection and member bindings. Both Holon and simple-value collections are supported by the common Collection kind; each instance supplies its effective element shape.

The selecting parent's slot establishes the required contract and participation
constraints. DAHN selection resolves that boundary. Classification as Collection
is not a claim that this implementation satisfies every conceivable Collection slot.

## Direct child roles and subject bindings

A delegated value cell is a child-selection boundary. Its subject is the typed
value, not the row Holon or PropertyDescriptor. Each actual child request supplies
the declared slot and its subject to DAHN selection; exact slot names and accepted
type descriptors remain open. Headers and rows are internal layout constructs
unless explicitly declared as independently selected slots.

| Role | Subject or binding context | Boundary |
| --- | --- | --- |
| Value cell participation, where established | A projected property or value for the row member | Declared ValueType anchors selection; optional PropertyDescriptor, row Holon, source affordance, and edit mode provide context. An array element uses its declared element ValueType. |

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

## Participation in Maximize and Restore

When Holon Inspector maximizes its collection region, it owns the redistribution
and the saved region arrangement. Table receives the resulting child allocation
and adapts its internal presentation. Table MUST preserve its mounted child state,
row/member bindings, active sort and filter, selected member, and editing state
through this allocation change and its restoration. Existing sort restoration
rules still require fresh membership data rather than stale membership snapshots.

Restoring the parent region does not reset Table or select another Visualizer.
Table respects the restored allocation supplied by its immediate parent, even
when that allocation differs from the one preceding maximization. It does not
restore the parent’s geometry, Canvas attention, or context grant itself.

If Table offers a request to enlarge its containing region, that request goes
to its immediate composition owner under the
[shared authority contract](../../../dahn-design-spec.md#independent-restoration-and-request-outcomes).
It does not directly change Node, Path Inspector, Canvas, or host geometry.
A refused request leaves the current presentation and restore information usable.
A separate Table-local maximize control or internal maximizable region is not
specified here; exact controls remain a presentation decision.

## Collection presentation and editing

## Collection Visualizer

### Responsibility

Table renders the homogeneous subject defined by the [Collection kind](../kind-spec.md).
Its row/column structure does not depend on whether the subject came from an
array, relationship, or Dance. Provenance still determines semantic editability.

---

### Selection

An applicable Collection Visualizer is selected through Rust DAHN architecture.

The Table Collection Visualizer declares applicability to `HolonCollection.HolonType`.
It is an initial candidate under ordinary DAHN selection policy. If there is no compatible candidate, selection returns an explicit error.

The TypeScript runtime resolves only the implementation supplied with the
selection result. If that implementation is unavailable locally, it reports a
realization error and does not replace the selected Visualizer.

A compatible alternative Collection Visualizer may fill its parent's slot without
adopting Table's internal rows or columns.

---

### Geometry

The parent supplies external allocation; Table lays out its rows and columns
within that budget. Holon Inspector’s [collection allocation](../../node/holon-inspector/design-spec.md#collection-child-activation-and-allocation)
places its child below the tab bar. Other parents may place Table differently.

## Table Collection Visualizer

### Rows

Each collection element corresponds to one row.

For holon collections:

- one row represents one holon.

For simple value collections:

- one row represents one value.

---

### Columns

For holon collections:

- columns correspond to exposed projected properties.
- each column uses one Value Visualizer selected through its PropertyDescriptor
  and declared ValueType in Table's owned Value slot;
- every cell in a column uses that selected definition, with a separate instance
  receiving the cell's value;
- one compact V on the column heading exposes its selected Value Visualizer,
  including display-name tooltip and column-scoped inspection;
- Table owns row presentation: there are no independently selected Row
  Visualizers and no row-specific or per-cell V controls.

Column descriptor bindings are supplied separately from plain projected values.
Synthetic identity columns use the canonical identity-property descriptor.
Projected columns without authoritative descriptor bindings remain Table-owned
until bindings are available; Value Visualizers are not inferred from value tags.
Sorting and row selection preserve both column selection and captured inspection.


For simple scalar collections:

- the initial table normally contains one value column.

---

### Collection Header

The Collection Visualizer SHOULD have a header distinct from column headers.

It may contain:

- collection name;
- element count;
- collection actions;
- alternate visualizer controls;
- projection information;
- state indicators.

---

### Column Operations

Column headers support sorting of eligible columns. Filtering is a separate
collection-view operation and may be delivered incrementally.

#### Column-Oriented Sorting Semantics

A column sort orders complete rows by the values in one active column. It MUST
preserve row identity, cell alignment, member-reference binding, and selection
identity. Sorting MUST NOT mutate semantic collection membership, cardinality,
relationship sequence positions, or navigation topology.

The initial column-oriented sorting contract is:

| Concern | Semantics |
| --- | --- |
| Eligible property value kinds | `StringValue`, `IntegerValue`, and `BooleanValue` |
| Strings | Deterministic, case-sensitive lexicographic ordering; no locale-dependent collation or case folding |
| Integers | Numeric ordering, not ordering of formatted strings |
| Booleans | `false` before `true` in ascending order |
| Sequence | Order by authoritative `SequencePosition` semantics; see [Sequence Column](design-spec.md#sequence-column) |
| Missing values | `null` sorts last in both directions |
| Equal values | Preserve their relative order in the supplied collection projection, including for descending sorts |
| First activation of a column with no active sort | Ascending |
| Activation of the active sort column | Toggle ascending/descending |
| Activation of a different eligible column | Ascending on the newly selected column |
| Number of active sort columns | One |

`EnumValue`, `BytesValue`, and mixed `AnyBaseValue` columns are not initially
sortable. Their displayed labels MUST NOT be used to invent semantic ordering
or a cross-type comparison policy. A future authoritative ordering contract may
extend eligibility.

Sorting compares typed values rather than rendered cell text. The sort MUST
leave the supplied input unchanged and retain a stable association between each
row and its original member occurrence. Header activation MUST NOT select or
inspect a member. Row keyboard navigation follows the displayed row order.

The active sort column and direction MUST be visible and available to assistive
technology. Header controls MUST expose visible ascending and descending choices, be
keyboard-operable, and expose appropriate `aria-sort` state. The active
direction MUST be visibly distinguished. If responsive column fitting hides the active header, the
collection MUST retain a discoverable sort indicator within its allocation.

#### Sort State Lifetime

The active sort belongs to the Collection Visualizer occurrence, not to the
semantic holon, column display label, or Path Inspector grid position. Different
occurrences of the same collection MAY have different sorts.

Tab switching and returning, compression on either or both axes, overflow,
viewport movement, focus changes, and retained-path insertion MUST preserve the
occurrence's sort. Sorting another column MUST leave Sequence values attached to
their original member occurrences.

A valid saved sort takes precedence over the table default in [Table-Level Default Row Ordering](design-spec.md#table-level-default-row-ordering) and is
reapplied after fresh membership projection. If its column disappears or becomes
ineligible, the table MUST return to the applicable table default and update its
sort indicator. Restoring view state MUST NOT substitute stale membership for a
fresh collection read.

### Sequence Column

For a relationship collection, the originating relationship descriptor's
`IsOrdered` property (display name `isOrdered`) is the authoritative indicator
that member order is significant. The applicable declared or inverse descriptor
supplies this policy. No separate manual-order flag is required.

When `IsOrdered` is true, the table MUST expose a read-only **Sequence** column
whose values come from authoritative relationship-occurrence `SequencePosition`
metadata. These values belong to member occurrences, not to properties of the
target holon. Repeated targets, where allowed, retain distinct occurrence identity
and sequence metadata.

Sequence MUST NOT be generated from the current display index or incidental
retrieval order, and sorting MUST NOT renumber it. Ascending Sequence restores
manual order; descending Sequence reverses that order as a view operation only.
Unordered collections MUST NOT acquire a synthetic Sequence column. A target
property with the same display name remains a distinct column identity.

The table consumes ordering policy and occurrence metadata through the public
reference/SDK boundary. It MUST NOT access storage links directly or infer
ordering policy from observed membership order. Missing authoritative metadata
must remain an explicit unavailable/error condition, not fabricated sequence
values.

See [effective collection policy](../../../../type-system/descriptor-semantics-rules.md#36-effective-collection-policy)
and [storage ordering boundaries](../../../../guest/storage-layer-services/storage-layer-design-spec.md#11-filtering-ordering-and-limiting).

### Table-Level Default Row Ordering

The table's default ordering is distinct from the semantics of sorting an
individual column. It applies on initial presentation when no valid saved sort
exists, and as the fallback described in [Sort State Lifetime](#sort-state-lifetime).

Apply the following precedence:

1. **Manually ordered relationship collection (`IsOrdered = true`):** Sequence
   ascending, whether or not the target HolonType defines a key.
2. **Otherwise, a holon collection whose declared element HolonType or concrete
   member HolonTypes define instance keys:** Key ascending, using the
   column-oriented string comparison semantics.
3. **Otherwise:** preserve the supplied collection order without asserting that
   this order has semantic significance. This includes keyless holon collections
   and scalar collections without an applicable ordering contract.

A broad declared target such as `HolonType.TypeDescriptor` may select a keyless
baseline while concrete members have keyed types. This is the case for `Owns`.
When the declared type does not establish keyedness, inspect the concrete
members' describing HolonTypes. If a concrete member type defines keys, use the
Key default; keyless members retain missing Key values and sort last. A broad
keyless target alone MUST NOT suppress this default. Empty collections use the
declared type's policy.

Whether a HolonType defines a key is descriptor-governed: use its
effective `InstanceKeyRule`; `NoneRule.KeyRuleType` denotes explicit keylessness.
Do not infer keyedness from a nonempty sample, an arbitrary property named Key,
or a fallback identity label. Key ordering uses the actual semantic member keys,
not versioned-key or display-label substitutes. Missing key values follow the
column sort's missing-value rule and do not change type-level keyedness.

Sequence and Key defaults MUST expose their active ascending sort indicators.
A user may override either default by selecting another eligible column. A valid
user-selected sort is preserved across ordinary occurrence restoration rather
than being overwritten by the default.

See [instance key rules and explicit keylessness](../../../../type-system/schema-design-spec.md#92-explicit-keylessness).

### Producer Ordering for Value Projections

Action-owned record projections may supply `defaultRowOrder`, an exact permutation
of their stable row IDs, together with a readable `defaultOrderLabel`. Table rejects
incomplete, duplicate, or unknown IDs. This bounded producer default applies only
when no explicit user column sort is active. It does not change the ordinary
Sequence/Key defaults for holon collections, add a compound sort editor, or mutate
membership. Restoring a null sort restores this producer order; restoring a valid
user sort preserves the selected column and direction.

Projected input contains display values only. Row activation reports the stable
row ID to its owner, which retains actual subject bindings separately. A row need
not have a holon subject to support diagnostic detail. The producer may provide a
missing-value label; loader diagnostics use **Not available**. Selection still uses
the declared projection element type and the parent's owned Collection slot.

## Adaptive Presentation Evidence

Column order and visibility, a chosen layout or Value representation, and
repeated explicit sort overrides may provide contextual preference evidence
under the [adaptive reporting contract](../../../dahn-design-spec.md#148-adaptive-interaction-reporting).
Their immediate sort/selection state remains occurrence-local as defined above;
reporting does not make that state durable or shared automatically. Column
prominence may express salience, while an alternate representation may express
preference affinity. A supported personalization interaction does not require
a universal drag handle or prescribe the historical table controls.

Sorting does not reorder stored members. Filtering retains its query/owner
contract and must not be reinterpreted as merely hiding a field or assigning a
salience score. Learning from either operation does not change authorization,
collection membership, or the selected Visualizer without an explicit applicable
selection/lifecycle operation. Persistent column configurations and governed
contributions require their own context matching and consent policy.

## Editable Collection Visualizers

The [Collection mutation contract](../kind-spec.md#mutation-semantics-and-ownership)
owns provenance, permissions, and staged semantics. Table uses the same view for
inspection and editing; editing adds controls without replacing it with a form.
Sort/filter state and row selection remain occurrence-local presentation state.

## Editable Value Arrays

Where the shared contract permits, Table exposes add/remove/edit controls and
semantic reorder controls. Individual values use their selected Value Visualizer.
A sort operation is distinct from a semantic reorder operation.

## Editable Multi-Valued Relationships

Where permitted, Table exposes add/remove-target and semantic reorder controls.
Target selection may initially use a simple generic selection mechanism.
Membership changes update the source Holon, not the displayed targets.

## Dance Result Collection Editability

A result is not editable merely because it appears in Table. The shared contract
requires semantic ownership, available mutation affordances, descriptors, and
permissions; Table presents only the controls those semantics authorize.
