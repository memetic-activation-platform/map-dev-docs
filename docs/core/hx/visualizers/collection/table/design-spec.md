# Table Collection Design Specification

## Status and current authority

Partial normative specification. The table and collection-editing source detail
below has moved from Space Navigator. Further separation of common Collection
promises from table realization remains pending. Concrete table geometry does
not constrain every Collection Visualizer.

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

The following is a framing inventory of existing roles, not a finalized runtime
API. Detailed accepted types and participation contracts remain in the current
sources until reconciled. Each actual child slot is independently substitutable
and resolved through DAHN selection.

| Role | Subject or binding context | Boundary |
| --- | --- | --- |
| Value cell participation, where established | A projected property or value for the row member | Exact slot names, contracts, and bindings are not yet specified by this frame. |

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

## Collection presentation and editing

## Collection Visualizer

### Responsibility

A Collection Visualizer renders a homogeneous multi-valued semantic result.

Its structural behavior SHOULD be independent of whether the collection originated from:

- array property;
- relationship;
- dance.

---

### Selection

An applicable Collection Visualizer is selected through Rust DAHN architecture.

The Table Collection Visualizer is an initial candidate under ordinary DAHN
selection policy. No compatible candidate produces an explicit selection error.

The TypeScript runtime resolves only the implementation supplied with the
selection result. If that implementation is unavailable locally, it reports a
realization error and does not replace the selected Visualizer.

A specialized Collection Visualizer MAY be selected without changing the Space Navigator's collection placement contract.

---

### Geometry

An expanded Collection Visualizer MUST initially have the same width as the Node Visualizer that exposes it.

It appears directly beneath the owning Collection Tab Bar.

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

## Editable Collection Visualizers

A Collection Visualizer MAY become editable when it represents staged state semantically owned by the holon being edited.

The same visualizer is used for inspection and editing.

Editing adds mutation affordances rather than replacing the collection with a separate form.

## Editable Value Arrays

For an editable array-valued property, the Collection Visualizer MAY support:

- add value;
- remove value;
- edit value;
- reorder values where ordering is semantically meaningful and permitted.

Individual values continue to delegate editing to their applicable Value Visualizers.

Changes update Rust-owned staged state.

## Editable Multi-Valued Relationships

For a mutable plural relationship, the Collection Visualizer MAY support:

- add target;
- remove target;
- reorder targets where allowed.

Target selection MAY initially use the simplest generic selection mechanism available.

Relationship membership editing changes the source holon's staged relationship state.

## Dance Result Collection Editability

A collection-valued dance result is not inherently editable merely because it is shown through a Collection Visualizer.

Editability depends on:

- semantic ownership;
- available mutation affordances;
- descriptors;
- permissions.
