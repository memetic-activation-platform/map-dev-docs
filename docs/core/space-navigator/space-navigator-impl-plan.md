# DAHN Space Navigator Implementation Plan v0.2

## Status

Draft implementation plan derived from:

- `space-navigator-arch.md`
- `space-navigator-design-spec.md`

This plan supersedes the earlier Space Navigator implementation plan.

## Purpose

This plan decomposes the Space Navigator into a sequence of small, mergeable PRs that monotonically increase capability while proving the DAHN architecture incrementally.

Each PR should:

- leave the system in a working state;
- introduce one primary behavioral or architectural capability;
- be independently reviewable and testable;
- reuse previously established abstractions;
- avoid introducing speculative infrastructure significantly ahead of its first use;
- be small enough for a single developer working with Codex to understand, implement, validate, and merge confidently.

The implementation plan is derivative.

Architectural decisions belong in `space-navigator-arch.md`.

Normative Space Navigator behavior belongs in `space-navigator-design-spec.md`.

If this plan conflicts with either specification, the upstream specification wins and this plan should be updated.

---

# 1. Delivery Strategy

The implementation should progress through working vertical slices rather than attempting to build the complete DAHN framework before any experience is visible.

At the same time, early implementation MUST preserve several architectural seams that would otherwise become expensive to retrofit:

- visualizer category versus concrete visualizer implementation;
- Rust-side DAHN Selector boundary;
- `VisualizerId`-based TypeScript runtime resolution;
- generic fallback visualizers;
- Rust-owned MAP and staged state;
- TypeScript-owned visualizer occurrence and Canvas state;
- parent-owned layout allocation;
- theme-token-based styling;
- Canvas-scoped transaction controls;
- semantic interaction events rather than direct cross-component manipulation.

The initial implementations behind these seams MAY be deliberately simple.

For example:

- the initial Rust Selector may always return the generic fallback visualizer;
- the initial TypeScript Visualizer Runtime may resolve only locally bundled implementations;
- the initial theme may provide only one token set;
- the initial Canvas layout may use fixed canonical Node dimensions.

The seam matters before the sophisticated implementation behind it does.

---

# 2. PR Sizing Rule

A PR should normally introduce one primary capability.

A useful test is:

> Can the PR be described by one primary behavioral or architectural change and demonstrated independently?

If not, it is probably too large.

Another useful test is:

> Could this PR be reverted without requiring the previous PR to be reverted?

If not, the PR may contain too many intertwined changes.

Split a PR when it begins to combine multiple significant new concerns, for example:

- visualizer selection plus remote visualizer acquisition;
- collection row interaction plus Canvas traversal plus compression;
- staging plus Undo plus Commit;
- relationship editing plus a sophisticated target-search UX;
- adaptive gesture recording plus collective salience aggregation.

---

# 3. Phase 0 — DAHN Runtime Seams

The goal of this phase is not to build generalized infrastructure.

It is to establish the minimum architectural boundaries required before the first reusable visualizers are built.

---

## PR 1 — DAHN TypeScript MAP Adapter

### Goal

Introduce a thin DAHN-facing semantic adapter above the existing TypeScript MAP SDK.

### Scope

Provide the initial adapter boundary for operations needed by the first read-only Space Navigator slices.

Initial operations may include:

- inspect or resolve a holon reference;
- retrieve identifying/scalar projections;
- retrieve effective descriptor information;
- expand a relationship.

The adapter SHOULD:

- normalize async behavior;
- centralize command/SDK translation;
- normalize errors;
- remain independent of Space Navigator geometry.

### Non-Goals

Do not:

- duplicate MAP semantic state in TypeScript;
- introduce a TypeScript holon cache as an authoritative source;
- implement staging or transactions yet;
- implement visualizer selection yet.

### Acceptance Criteria

- Visualizers do not need to call low-level command serialization directly.
- MAP references remain Rust-backed semantic references.
- Adapter tests can run against mocked SDK operations.
- The adapter contains no Canvas placement or rendering decisions.

---

## PR 2 — Visualizer Identity and Runtime Resolution

### Goal

Separate a visualizer category and semantic `VisualizerId` from its TypeScript implementation.

### Scope

Introduce:

- `VisualizerId`;
- visualizer category;
- minimal TypeScript Visualizer Runtime;
- locally bundled implementation resolution;
- explicit generic fallback registration.

Initial registrations may include placeholders for:

- Generic Holon Node Visualizer;
- Table Collection Visualizer;
- generic scalar Value Visualizers.

### Non-Goals

Do not implement:

- Visualizer Commons discovery;
- remote packages;
- version acquisition;
- sandboxing;
- adaptive selection.

### Acceptance Criteria

- TypeScript can resolve a `VisualizerId` into an executable local implementation.
- Visualizer category is distinct from implementation identity.
- Failure to resolve a specialized ID can fall back where an applicable generic fallback exists.
- No Canvas needs to instantiate a concrete visualizer by hard-coded implementation class where the runtime boundary should apply.

---

## PR 3 — Rust DAHN Selector Boundary

### Goal

Establish the architectural boundary in which Rust chooses a visualizer identity.

### Scope

Introduce the minimum Rust-side selector command/API needed to answer a request such as:

    select visualizer for category + semantic subject/context

The initial implementation MAY deterministically return the appropriate core fallback visualizer.

Return enough information for TypeScript to resolve the selected implementation, such as:

- `VisualizerId`;
- category;
- optional indication that alternatives exist.

### Non-Goals

Do not implement:

- federated Visualizer Commons discovery;
- adaptive scoring;
- personal preference;
- collective salience;
- trend or maturity scoring.

### Acceptance Criteria

- TypeScript requests selection rather than selecting semantic visualizers itself.
- The decision crosses the existing MAP command/IPC boundary.
- Rust returns a stable `VisualizerId`.
- TypeScript resolves that ID through the Visualizer Runtime.
- The fallback-only implementation proves the correct architectural direction.

---

## PR 4 — Theme Token Foundation

### Goal

Prevent the first visualizers from embedding visual style constants that later need to be removed.

### Scope

Introduce the minimum semantic theme-token mechanism required by initial visualizers.

Initial tokens may cover:

- surfaces;
- text;
- borders;
- spacing;
- selected/focus states;
- action treatment.

Provide one default theme.

### Non-Goals

Do not implement:

- theme marketplace;
- multiple sophisticated themes;
- adaptive theme selection.

### Acceptance Criteria

- Initial visualizers consume semantic tokens for theme-owned styling.
- Core visualizer code does not hard-code theme-specific colors or equivalent styling decisions.
- A different token set could later change stylistic expression without changing visualizer semantics.

---

# 4. Phase 1 — Foundational Read-Only Visualizers

---

## PR 5 — Static Table Collection Visualizer

### Goal

Introduce the first concrete generic Collection Visualizer.

### Scope

Implement the Table Collection Visualizer with:

- homogeneous collection input;
- collection header;
- column headers;
- one row per element;
- scalar value collections;
- holon collections using an explicitly supplied property projection.

The visualizer MUST remain independent of collection provenance.

It should not care whether its input came from:

- array property;
- relationship;
- dance result.

### Non-Goals

Do not implement:

- sorting;
- filtering;
- row navigation;
- editing;
- adaptive ordering.

### Acceptance Criteria

- A scalar collection can render as one value column.
- A holon collection can render projected properties as columns.
- One collection implementation works independent of collection origin.
- The visualizer is selected/resolved through the visualizer runtime boundary.

---

## PR 6 — Descriptor-Driven Value Presentation

### Goal

Delegate scalar presentation to Value Visualizers.

### Scope

Introduce the minimum Property/Value Visualizer contracts required to display current scalar types.

Integrate them into:

- table cells;
- future Node property presentation.

### Non-Goals

Do not implement editing yet.

### Acceptance Criteria

- Collection code does not contain a growing switch statement for concrete value types.
- Each supported value type resolves to an applicable Value Visualizer.
- Unknown-but-supported fallback behavior is explicit.
- The same contract can later support edit mode.

---

## PR 7 — Space Navigator Canvas Shell

### Goal

Introduce the Space Navigator as an actual Canvas Visualizer.

### Scope

Create:

- Space Navigator Canvas container;
- pinned Canvas Action Bar shell;
- navigable Canvas content region;
- root visualizer occurrence state;
- viewport/layout root.

The Canvas Action Bar may initially contain no active transaction actions.

### Acceptance Criteria

- Space Navigator exists as a Canvas Visualizer rather than application-global layout.
- The Canvas Action Bar remains pinned above the navigable area.
- Root occurrence state is distinct from semantic holon state.
- Canvas geometry is owned by the Space Navigator.

---

## PR 8 — Basic Generic Holon Node Visualizer

### Goal

Render one arbitrary holon through the selected Node Visualizer.

### Scope

Implement the initial Generic Holon Node Visualizer with:

- Title Bar;
- Node Action Bar shell;
- Property Viewer Pane;
- bottom Collection Tab Bar shell;
- right-side Single-Value Tab Rail shell;
- scalar properties rendered through Property/Value Visualizers.

Use the Rust Selector and TypeScript Visualizer Runtime to select/resolve the Node Visualizer.

### Geometric Requirements

The full initial Node geometry includes:

- main body;
- visible right-side rail;
- visible bottom tab bar.

Neither navigation surface yet opens child content.

### Acceptance Criteria

- Space Navigator asks Rust for a Node Visualizer selection.
- The selected `VisualizerId` resolves through the TypeScript runtime.
- Generic fallback renders an arbitrary supported holon.
- Scalar values use Value Visualizers.
- Both navigation surfaces are visible.
- No domain-specific Node screen is required.

---

## PR 9 — Descriptor-Driven Affordance Classification

### Goal

Populate the Node structure from effective descriptor semantics.

### Scope

Classify:

| Affordance | Shape | Initial Placement |
| --- | --- | --- |
| Property | scalar | Property Viewer |
| Property | array | Collection Tab |
| Relationship | max = 1 | Single-Value Rail |
| Relationship | max > 1 / unbounded | Collection Tab |
| Dance | no result | Node Action classification |
| Dance | single holon | singular-result classification |
| Dance | collection | collection-result classification |

Dance invocation itself is deferred.

### Normative Requirement

Runtime result count MUST NOT alter descriptor-defined cardinality.

### Acceptance Criteria

- Structural affordances derive from descriptors.
- Empty singular relationships remain classified singular.
- Plural relationships with zero or one target remain classified plural.
- Dance result shape can be classified before invocation.
- The Node Visualizer does not contain type-specific affordance rules.

---

# 5. Phase 2 — Vertical Collection Exploration

---

## PR 10 — Collection Tab Activation

### Goal

Make plural affordances inspectable.

### Scope

Support activation of:

- array-valued property tabs;
- multi-valued relationship tabs.

On activation:

- retrieve contents lazily where needed;
- request/select a Collection Visualizer;
- render it below the Node;
- reuse the same collection region when switching tabs.

Support:

- unresolved;
- loading;
- loaded empty;
- loaded;
- error.

### Geometry

- Collection Tab Bar width equals owning Node width.
- Expanded Collection Visualizer width equals owning Node width.
- No collection content consumes vertical space before activation.

### Acceptance Criteria

- Array values display through Collection Visualizer.
- Relationship targets display through Collection Visualizer.
- Empty plural relationships display an empty collection state.
- One-target plural relationships still display as collections.
- Switching tabs does not replace the parent Node.

### Milestone

This is the first useful read-only Space Navigator slice:

    inspect holon
        |
    choose plural affordance
        |
    inspect collection

---

## PR 11 — Collection Row Selection

### Goal

Separate collection selection from navigation.

### Scope

Implement:

- single-click row selection;
- selected-row state;
- semantic activation event for navigation, initially via double-click.

The Collection Visualizer emits intent but does not place child Nodes.

### Acceptance Criteria

- Row selection does not itself navigate.
- Row activation emits the selected semantic holon reference.
- Collection code remains independent of Canvas geometry.
- Selected-row state belongs to the collection occurrence.

---

## PR 12 — First Vertical Child

### Goal

Navigate from a collection into one selected holon.

### Scope

On collection-row activation:

- create a child visualizer occurrence;
- select/resolve its Node Visualizer;
- render it beneath the Collection Visualizer;
- preserve source Node and Collection;
- record traversal provenance.

### Acceptance Criteria

- Child Node uses normal Node Visualizer selection and runtime resolution.
- Parent and collection remain present.
- Child occurrence identity is distinct from holon identity.
- Provenance records the collection traversal.
- The same holon may later appear in multiple occurrences.

---

## PR 13 — Vertical Sibling Switching

### Goal

Support efficient exploration of multiple rows without introducing branching complexity.

### Scope

When a collection already has an active child:

- activating another row replaces the active child;
- collection remains open;
- row selection updates;
- provenance updates.

Do not yet retain multiple simultaneous sibling branches.

### Acceptance Criteria

- A person can inspect several collection members in sequence.
- The collection need not be reconstructed.
- Only one active child per collection is required initially.
- Switching children does not corrupt parent state.

---

# 6. Phase 3 — Horizontal Navigation and Provenance Geometry

---

## PR 14 — First Singular Relationship Child

### Goal

Activate the right-side navigation grammar.

### Scope

For max-cardinality-one relationships:

- activate a right-rail entry;
- retrieve target lazily;
- select/resolve target Node Visualizer;
- display it to the right;
- retain source occurrence;
- record provenance.

### Geometry

The first child SHOULD receive the same canonical full Node dimensions as its source where available.

No child width is consumed before rail activation.

### Acceptance Criteria

- Singular relationship navigation opens rightward.
- Runtime population does not alter singular classification.
- Selecting another singular affordance may replace the immediate right-side child.
- Child uses the normal Node Visualizer selection path.

### Milestone

At this point the fundamental two-dimensional grammar exists:

- plural goes down;
- singular goes right.

---

## PR 15 — Recursive Horizontal Navigation

### Goal

Permit continued traversal to the right.

### Scope

A right-side child may itself:

- expose its rail;
- open another child;
- expose its own collection tabs.

Extend occurrence/provenance state to represent a horizontal chain.

### Acceptance Criteria

- A → B → C works.
- Each occurrence retains distinct provenance.
- A horizontally reached node can still navigate vertically.
- Semantic identity and occurrence identity remain separate.

---

## PR 16 — Vertical Compression

### Goal

Introduce Y-axis compression.

### Scope

Allow a Node occurrence to relinquish vertical space while preserving:

- compact identity;
- relevant active Collection Tab;
- active collection context where appropriate;
- restoration.

Prefer simple deterministic/manual compression over sophisticated adaptive rules.

### Acceptance Criteria

- Node can enter and leave Y-compressed state.
- Collection context needed for sibling exploration remains usable.
- Navigation state survives compression.
- Expanded subordinate geometry respects the compressed parent allocation.

---

## PR 17 — Horizontal Compression

### Goal

Introduce X-axis compression.

### Scope

Allow prior horizontal ancestors to relinquish width.

Preserve:

- compact identity;
- relevant singular-navigation context;
- recoverable Node state;
- recoverable collection state.

Any subordinate collection owned by the compressed Node must relinquish the same horizontal real estate.

### Acceptance Criteria

- A prior Node can compress to a narrow vertical representation.
- Continued rightward traversal does not require deleting prior provenance.
- Re-expansion restores context.
- Subordinate content does not retain full old width.

---

## PR 18 — Orthogonal Two-Axis Compression

### Goal

Allow X and Y compression to compose.

### Scope

Support conceptual states:

| State | Width | Height |
| --- | --- | --- |
| Full | full | full |
| X-compressed | narrow | full-ish |
| Y-compressed | full-ish | short |
| XY-compressed | narrow | short |

### Acceptance Criteria

- X and Y state are independently representable.
- Applying both produces a compact provenance cell.
- Selected affordances and child links survive.
- Restoration recovers prior local state.
- Compression hides presentation, not state.

---

# 7. Phase 4 — Read-Only Collection Refinement

---

## PR 19 — Collection Sorting

### Goal

Add the first collection-view operation.

### Scope

Support:

- eligible-column sorting;
- ascending/descending state;
- preservation within the Collection Visualizer occurrence.

### Acceptance Criteria

- Sort state is visible and persistent within the occurrence.
- Switching tabs and returning restores sort state.
- Compression does not destroy sort state.

---

## PR 20 — Collection Filtering

### Goal

Add column-level filtering.

### Scope

Support:

- basic filters;
- clear filter;
- filter-state preservation;
- composition with sorting.

### Acceptance Criteria

- Filtering changes displayed membership without changing semantic collection cardinality.
- Filter state survives ordinary navigation/compression.
- Sorting and filtering compose predictably.

---

# 8. Phase 5 — Adaptive Ordering and Visualizer Choice

This phase proves the DAHN adaptive seam without yet requiring full collective salience or Visualizer Commons discovery.

---

## PR 21 — Presentation Ordering from Rust

### Goal

Allow Rust to provide initial adaptive presentation ordering.

### Scope

Extend DAHN presentation context with ordering for some or all of:

- properties;
- singular rail entries;
- collection tabs;
- actions.

Initial ordering may remain deterministic/default.

The important requirement is that TypeScript consumes ordering supplied through the Rust-side boundary.

### Acceptance Criteria

- Generic Node presentation does not assume descriptor declaration order is always presentation order.
- Rust can return explicit ordering.
- TypeScript respects that ordering.

---

## PR 22 — Local Reordering and Adaptive Gesture Events

### Goal

Allow the person to personalize visible ordering and report the gesture semantically.

### Scope

Initially support reordering of one or more of:

- properties;
- collection tabs;
- singular rail entries.

On reorder:

1. update TypeScript presentation immediately;
2. emit a semantic adaptive gesture through the MAP adapter.

Persistent scoring may initially be minimal.

### Acceptance Criteria

- UI reorders without waiting for an IPC round trip.
- A semantic adaptive event reaches Rust.
- Local visual state reflects the person's choice.
- Presentation code does not implement aggregate salience itself.

---

## PR 23 — Alternate Visualizer Selection

### Goal

Prove explicit visualizer choice as an adaptive interaction.

### Scope

When Rust reports alternate applicable visualizers:

- advertise alternatives;
- allow selection of another locally resolvable visualizer;
- preserve the occurrence and navigation context where possible;
- emit a visualizer-preference signal.

The candidate set may initially be only core/local visualizers.

### Acceptance Criteria

- Visualizer replacement does not require replacing the semantic subject.
- Selection routes through `VisualizerId`.
- Explicit selection emits an adaptive signal.
- Generic fallback remains recoverable.

---

# 9. Phase 6 — Staged Editing Foundation

---

## PR 24 — Edit Existing Holon: Scalar Properties

### Goal

Introduce staged edit mode while preserving the existing Node occurrence.

### Scope

Add holon-scoped **Edit** action.

On Edit:

- invoke Rust staging for the current holon;
- keep the same visualizer occurrence;
- enter edit mode;
- render eligible scalar properties through editable Value Visualizers;
- update staged property values through MAP operations.

Do not yet implement Commit.

### Acceptance Criteria

- Edit is a state transition, not navigation.
- Staged semantic state remains Rust-owned.
- Eligible scalar properties can be changed.
- Read-only properties remain read-only.
- Navigation still works while editing.
- Compression does not discard staged state.

---

## PR 25 — Canvas Transaction Status and Action State

### Goal

Make the active transaction visible at Canvas scope.

### Scope

Activate the pinned Canvas Action Bar against actual Rust transaction state.

Expose enough state for presentation of:

- transaction active/inactive;
- staged changes present;
- Commit availability placeholder;
- Undo/Redo availability placeholders.

Commit and Undo/Redo behavior are implemented in subsequent PRs.

### Acceptance Criteria

- Transaction state is not inferred separately by each Node.
- Editing one holon causes Canvas-level transaction state to update.
- Canvas Action Bar is the owner of transaction-scoped controls.
- Node Action Bar does not expose Commit.

---

## PR 26 — Meaningful Undo Boundaries

### Goal

Connect editing gestures to Rust transaction snapshot markers.

### Scope

For scalar property editing:

- determine an initial meaningful gesture-completion boundary;
- instruct Rust to establish an Undo marker;
- keep preservation snapshots conceptually separate from user-visible Undo boundaries.

### Acceptance Criteria

- One completed scalar edit can become one Undo step.
- TypeScript determines the UX boundary.
- Rust stores/restores semantic snapshot state.
- TypeScript does not maintain an independent semantic command history.

---

## PR 27 — Canvas Undo

### Goal

Expose semantic Undo from the pinned Canvas Action Bar.

### Scope

Implement:

- enabled/disabled state;
- request to Rust;
- restoration of prior staged transaction snapshot;
- refresh of affected visualizers.

### Acceptance Criteria

- Undo affects staged MAP state, not merely UI control state.
- Affected Node occurrences refresh from restored semantic state.
- Navigation geometry remains intact.
- Undo is not repeated in Node Action Bars.

---

## PR 28 — Canvas Redo

### Goal

Complete transaction history traversal.

### Scope

Implement:

- Redo availability;
- Rust roll-forward;
- affected presentation refresh.

### Acceptance Criteria

- Undo followed by Redo restores the semantic staged state.
- Redo uses the Canvas Action Bar.
- TypeScript does not reconstruct Redo locally.

---

## PR 29 — Canvas Transaction Commit

### Goal

Complete the first staged update lifecycle.

### Scope

Implement transaction-wide Commit from the Canvas Action Bar.

Commit flow:

- validate transaction;
- execute MAP Commit;
- return success/failure;
- refresh affected occurrences.

On success:

- affected visualizers return to read mode;
- navigation provenance remains intact.

On failure:

- transaction remains staged;
- affected visualizers remain editable;
- validation/commit errors remain visible.

### Acceptance Criteria

- Commit is not tied to one Node Visualizer.
- One edited holon can be successfully committed.
- Failed Commit does not discard staged state.
- Successful Commit refreshes committed values.
- Continuous preservation remains distinct from explicit Commit.

### Milestone

This completes the first full read/write flow:

    inspect
      |
    edit staged state
      |
    Undo / Redo
      |
    Canvas Commit
      |
    inspect committed state

---

# 10. Phase 7 — Multi-Holon Transaction Capability

---

## PR 30 — Edit Multiple Existing Holons in One Transaction

### Goal

Prove that the Space Navigator transaction is broader than one visualizer.

### Scope

Allow:

- edit A;
- navigate elsewhere;
- edit B;
- retain both staged changes in the same active transaction.

Ensure both occurrences are reflected in transaction presentation state.

### Acceptance Criteria

- A and B can both be staged concurrently.
- There is still one Canvas-level Commit.
- Undo/Redo operate on the shared transaction history.
- Navigation away from A does not discard A's staged changes.
- TypeScript does not create independent transaction contexts per Node.

---

## PR 31 — Commit Multiple Updated Holons

### Goal

Prove multi-holon Commit end-to-end.

### Scope

Commit a transaction containing staged changes to multiple existing holons.

### Acceptance Criteria

- Full transaction validates together.
- Successful Commit refreshes all affected visible occurrences.
- Failure leaves the shared staged transaction intact.
- Transaction status clears only after successful completion according to MAP semantics.

---

## PR 32 — Multiple Occurrences of One Staged Holon

### Goal

Prevent semantic divergence when one staged holon is visible more than once.

### Scope

Handle:

- same semantic holon displayed through multiple traversal paths;
- one occurrence enters edit mode;
- another occurrence remains visible.

Define an initial presentation synchronization policy.

### Architectural Invariant

There is one authoritative staged semantic state in Rust.

### Acceptance Criteria

- TypeScript does not create independent staged semantic copies.
- Visible occurrences cannot silently diverge semantically.
- Refresh after edit/Undo/Redo/Commit keeps occurrences coherent.
- Occurrence-specific presentation state remains independent.

---

# 11. Phase 8 — Create, Clone, and Delete

---

## PR 33 — Clone Holon

### Goal

Initialize new staged state from an existing holon.

### Scope

Add **Clone** as a holon-scoped action.

Clone:

- creates a distinct staged holon;
- initializes it from the source according to MAP semantics;
- opens it in normal editable Node presentation;
- joins the active transaction.

### Acceptance Criteria

- Clone has a distinct semantic identity.
- No clone-specific editor is introduced.
- Clone source does not automatically become navigation provenance.
- Canvas-level Commit publishes the clone.

---

## PR 34 — Create Instance from Concrete Type

### Goal

Provide generic type-driven creation.

### Scope

When viewing an applicable concrete Holon Type descriptor:

- expose **Create Instance**;
- stage a new holon in the active Space;
- apply defaults;
- present it through ordinary editable Node Visualizer behavior;
- join the active transaction.

### Acceptance Criteria

- Creation is descriptor-driven.
- No type-specific creation form is required.
- New holon can coexist with other staged changes.
- Canvas Commit publishes it.

---

## PR 35 — Stage Delete

### Goal

Add semantic deletion as a transaction participant.

### Scope

Add **Delete** at holon scope where permitted.

Support:

- explicit confirmation;
- staged deletion state;
- Canvas transaction inclusion;
- appropriate staged visual indication.

### Acceptance Criteria

- Delete does not immediately bypass the active transaction.
- Historical erasure is not implied.
- Deletion can coexist with other staged changes.
- Commit publishes deletion according to MAP semantics.
- Undo can restore staged state before Commit where supported by existing transaction semantics.

---

# 12. Phase 9 — Editable Collections and Relationships

---

## PR 36 — Editable Value Arrays

### Goal

Extend staged editing into array-valued properties.

### Scope

For mutable arrays:

- add value;
- remove value;
- edit value;
- reorder where allowed.

Reuse the existing Collection Visualizer.

Use Value Visualizers for individual element editing.

Establish suitable Undo boundaries.

### Acceptance Criteria

- No separate array-editing form exists.
- Mutation updates Rust-owned staged state.
- Undo/Redo covers array changes.
- Compression preserves staged presentation state.
- Canvas Commit publishes changes.

---

## PR 37 — Generic Relationship Target Selection

### Goal

Introduce the minimal reusable mechanism needed to choose a relationship target.

### Scope

Provide a simple generic selector suitable for:

- setting singular relationship targets;
- adding plural relationship targets.

Keep the first implementation intentionally narrow.

### Non-Goals

Do not build a generalized rich search/navigation subsystem unless required.

### Acceptance Criteria

- A valid target can be selected generically.
- Selection returns semantic holon reference.
- Selector is reusable by singular and plural relationship editing.
- Target-selection UI does not own relationship mutation semantics.

---

## PR 38 — Editable Multi-Valued Relationships

### Goal

Allow relationship membership mutation through Collection Visualizers.

### Scope

For mutable plural relationships:

- add target;
- remove target;
- reuse the generic target selector;
- preserve normal collection navigation;
- respect descriptor constraints.

### Acceptance Criteria

- Relationship membership edits source holon staged state.
- Target properties are not implicitly edited.
- Undo/Redo covers membership changes.
- Canvas Commit publishes changes.

---

## PR 39 — Editable Single-Valued Relationships

### Goal

Add set/replace/clear semantics to singular relationship affordances.

### Scope

For mutable singular relationships:

- set target;
- replace target;
- clear target;
- continue ordinary rightward navigation.

### Acceptance Criteria

- Relationship remains structurally singular.
- Empty state remains represented.
- Target editing is distinct from target-holon editing.
- Undo/Redo works.
- Canvas Commit publishes the change.

---

# 13. Phase 10 — Dances

---

## PR 40 — Effective Dance Actions

### Goal

Populate Node actions from effective available dances.

### Scope

Support:

- directly declared dances;
- inherited dances;
- effective permission/role filtering;
- generic Action Visualizer presentation;
- invocation plumbing.

Result rendering may initially be limited.

### Acceptance Criteria

- Raw type hierarchy is not blindly displayed.
- Effective available dances drive actions.
- Node does not need domain-specific action code.
- Dance invocation goes through existing semantic MAP operations.

---

## PR 41 — Single-Holon Dance Results

### Goal

Route singular dance results into the existing rightward navigation grammar.

### Scope

For a dance whose response descriptor declares one holon:

- invoke;
- receive target;
- create/select Node occurrence to the right;
- record dance-result provenance.

### Acceptance Criteria

- Result shape is known from descriptor before execution.
- Normal Node selection/runtime resolution is reused.
- No special dance-result panel is introduced.

---

## PR 42 — Collection Dance Results

### Goal

Route plural dance results through Collection Visualizers.

### Scope

Support:

- holon collections;
- homogeneous value collections.

Expose using the existing Collection Tab / Collection Visualizer grammar.

### Acceptance Criteria

- No separate dance-result table implementation exists.
- Sorting/filtering apply where appropriate.
- Collection visualizer selection is reused.
- Provenance identifies dance result source.

---

## PR 43 — Scalar and No-Result Dances

### Goal

Complete the initial dance-result matrix.

### Scope

First resolve the open design decision for scalar results, then implement:

- scalar result presentation;
- no-result execution feedback.

### Acceptance Criteria

- Behavior is consistent with the finalized design specification.
- Neither result form requires a parallel visual architecture.

---

# 14. Phase 11 — Action Personalization

---

## PR 44 — Reorder Node Actions

### Goal

Extend adaptive ordering into Node action presentation.

### Scope

Allow permitted actions to be reordered.

On gesture:

- update presentation immediately;
- report adaptive event to Rust.

### Acceptance Criteria

- Immediate action order changes locally.
- Adaptive meaning is persisted through Rust boundary.
- Action behavior remains unchanged by presentation order.

---

## PR 45 — Canvas Action Personalization

### Goal

Apply the same adaptive principles to the pinned Space Navigator Action Bar.

### Scope

Where permitted, support changes to:

- ordering;
- prominence;
- overflow position.

### Acceptance Criteria

- Canvas retains ownership of its standard action set.
- User customization changes presentation rather than transaction semantics.
- Adaptive signals cross the normal Rust boundary.

---

# 15. Phase 12 — Visualizer Commons and Adaptive Selection Expansion

These PRs may occur later than the core Space Navigator release if the current milestone is focused on proving generic local visualizers first.

---

## PR 46 — Accessible Visualizer Commons Discovery

### Goal

Replace the fallback-only candidate source with federated MAP-native discovery.

### Scope

Discover Visualizer Commons reachable through applicable Space relationships.

Return eligible Visualizer Descriptors as candidate inputs to the Rust Selector.

### Acceptance Criteria

- Candidate population is not a centralized MAP-team registry.
- Accessible Commons are resolved through MAP semantics.
- TypeScript does not retrieve the full ecosystem simply to make selection decisions.

---

## PR 47 — Semantic Applicability over Discovered Visualizers

### Goal

Filter discovered candidates by visualizer category and semantic applicability.

### Scope

Use Visualizer Descriptor metadata to identify applicable candidates.

### Acceptance Criteria

- Applicability is descriptor/semantic driven.
- TypeScript implementation classes are not the source of applicability.
- Generic fallback remains available.

---

## PR 48 — Personal Visualizer Preference

### Goal

Use prior explicit choices in Rust-side visualizer selection.

### Scope

Persist and apply a user's visualizer preference signals.

### Acceptance Criteria

- Explicit visualizer replacement can influence later selection.
- Personal state remains Rust/MAP-owned.
- TypeScript does not reproduce preference scoring.

---

## PR 49 — Initial Collective Salience

### Goal

Introduce the first aggregate adaptive signal into selection or ordering.

### Scope

Choose one narrow aggregate signal rather than implementing the full future salience model.

Examples:

- aggregate visualizer preference;
- aggregate property ordering.

### Acceptance Criteria

- Aggregate state influences a selection/order result.
- Personal and collective inputs remain distinguishable.
- The scoring model is testable and documented.

---

## PR 50 — Explore/Exploit Selection Controls

### Goal

Prove that selection policy can vary between familiarity/stability and novelty/discovery.

### Scope

Introduce initial selector policy inputs for a constrained subset such as:

- personal versus collective weight;
- maturity preference;
- novelty/randomness.

### Acceptance Criteria

- Selector behavior changes predictably with policy.
- Policy remains Rust-side.
- Individual visualizers do not implement explore/exploit logic.

---

# 16. Phase 13 — Navigation and Transaction Hardening

---

## PR 51 — Staged-State Indicators Through Compression

### Goal

Make staged state unmistakable in compressed provenance.

### Scope

For X-, Y-, and XY-compressed occurrences:

- indicate staged state;
- indicate staged deletion where applicable;
- restore full edit context on expansion.

### Acceptance Criteria

- Compression never conceals the existence of staged work.
- Indicator is driven from authoritative transaction/staged context.
- Expansion restores editable presentation.

---

## PR 52 — Branch Closing and Pruning

### Goal

Allow explicit removal of unneeded traversal context.

### Scope

Define and implement:

- close child;
- prune descendants;
- interaction with staged occurrences;
- interaction with collection state.

### Acceptance Criteria

- Closing presentation does not silently abandon staged semantic state.
- Remaining provenance stays coherent.
- Canvas can intentionally reclaim space.

---

## PR 53 — Transaction Abandon/Revert

### Goal

Resolve and implement the design's transaction-abandon semantics.

### Scope

After the Design Specification resolves the open question, implement the chosen transaction-wide behavior.

### Acceptance Criteria

- User-facing semantics are explicit.
- Staged work is never silently lost.
- Canvas and visible occurrences refresh coherently.
- Behavior is testable across multiple staged holons.

---

## PR 54 — Deleted Holon Presentation

### Goal

Finalize staged and committed deleted-state presentation.

### Scope

Implement the design decision for:

- staged deletion;
- post-Commit deleted holon appearance;
- existing provenance paths containing deleted holons.

### Acceptance Criteria

- Deleted state remains semantically clear.
- Provenance can remain coherent.
- History is not confused with physical erasure.

---

# 17. Recommended Milestones

## Milestone A — First Dynamic Read-Only Node

PRs 1–9.

Delivers:

- DAHN adapter;
- Visualizer Runtime;
- Rust Selector boundary;
- theme foundation;
- Collection Visualizer;
- Value Visualizers;
- Space Navigator Canvas;
- Generic Node Visualizer;
- descriptor-driven affordance classification.

Result:

    semantic holon
         |
    Rust selects Node Visualizer
         |
    TypeScript resolves implementation
         |
    Space Navigator renders generic node

This proves the fundamental DAHN selection/composition seam before navigation becomes complex.

---

## Milestone B — First Useful Vertical Exploration

PRs 10–13.

Result:

    inspect holon
        |
    select plural affordance
        |
    inspect collection
        |
    select member
        |
    inspect child holon

This is the first meaningful user-facing Space Navigator loop.

---

## Milestone C — Two-Dimensional Space Navigator

PRs 14–18.

Result:

- singular traversal goes right;
- plural traversal goes down;
- occurrences preserve provenance;
- context compresses along both axes.

This establishes the defining Space Navigator navigation grammar.

---

## Milestone D — Read-Only Usability and Initial Adaptation

PRs 19–23.

Result:

- sorting;
- filtering;
- Rust-provided ordering;
- personal reordering gestures;
- alternate visualizer choice.

This proves that DAHN is not merely dynamic but begins to expose the adaptive architecture.

---

## Milestone E — First Complete Update Flow

PRs 24–29.

Result:

    inspect
      |
    Edit
      |
    staged scalar changes
      |
    Undo / Redo
      |
    Canvas Commit
      |
    inspect committed state

This is the first complete staged editing transaction.

---

## Milestone F — Multi-Holon Transaction

PRs 30–32.

Result:

    edit A
      |
    navigate
      |
    edit B
      |
    shared transaction
      |
    shared Undo / Redo
      |
    one Commit

This proves the Canvas-level transaction model rather than a conventional one-form/one-save workflow.

---

## Milestone G — Generic Lifecycle Operations

PRs 33–39.

Result:

- Clone;
- Create;
- Delete;
- editable arrays;
- editable singular relationships;
- editable plural relationships.

At this point the Space Navigator supports generic manipulation of MAP holons without introducing domain-specific forms.

---

## Milestone H — Full Initial Dance Integration

PRs 40–43.

Result:

- effective dances;
- singular dance results;
- collection dance results;
- scalar/no-result behavior.

Dances now participate in the same visual grammar as properties and relationships.

---

## Milestone I — Adaptive Visualizer Ecosystem

PRs 44–50.

Result:

- adaptive action ordering;
- Visualizer Commons discovery;
- semantic applicability;
- personal visualizer preference;
- initial collective salience;
- explore/exploit selector behavior.

This begins exercising DAHN as an open federated adaptive ecosystem rather than only a locally bundled generic browser.

---

# 18. Capabilities Intentionally Deferred

The initial Space Navigator implementation does not require full solutions for:

- remote arbitrary visualizer-code execution;
- production sandboxing;
- package signing;
- generalized dependency isolation;
- rich third-party package acquisition;
- all collective salience rubrics;
- sophisticated selector explanations;
- every explore/exploit control;
- every theme;
- arbitrary free-form Canvas layout;
- persistent collaborative Canvas sessions;
- complete mobile layout;
- full keyboard navigation;
- unlimited simultaneous sibling branching.

These capabilities should remain architecturally possible without becoming prerequisites for the first useful Space Navigator.

---

# 19. Cross-PR Implementation Principles

## 19.1 Preserve Architectural Seams Early

Simple implementations are acceptable.

Bypassing the intended boundary because the first implementation is simple is not.

For example:

- fallback-only selection still goes through Rust Selector;
- locally bundled visualizers still resolve through `VisualizerId`;
- one default theme still goes through theme tokens.

---

## 19.2 One Semantic Source of Truth

Do not duplicate authoritative MAP state into TypeScript.

This includes:

- staged holons;
- transaction state;
- Undo history;
- adaptive preference state.

---

## 19.3 One Experience Occurrence Model

Do not use holon identity as Canvas occurrence identity.

Navigation state belongs to visualizer occurrences.

---

## 19.4 One Node Grammar

Do not introduce separate Node implementations merely because a node was reached:

- horizontally;
- vertically;
- through a dance;
- through creation;
- through cloning.

Visualizer selection may choose a different semantic visualizer, but placement does not define a new category.

---

## 19.5 One Collection Grammar

Do not create separate collection frameworks for:

- arrays;
- relationships;
- dance results.

They converge on Collection Visualizers.

---

## 19.6 Read and Edit Share the Visual Tree

Do not introduce a separate form framework for editing.

Editing changes interaction mode and staged semantic state.

---

## 19.7 Commit Belongs to the Transaction

Do not add Commit buttons to individual Node Visualizers.

One Canvas transaction may contain changes to many holons.

---

## 19.8 Undo Is Semantic

Do not implement Undo by replaying TypeScript UI state.

TypeScript defines the boundary.

Rust owns the recoverable transaction snapshot.

---

## 19.9 Personalization Is Immediate; Learning Is Durable

TypeScript should make drag/reorder/select interactions feel immediate.

Rust should persist and interpret the adaptive signal.

---

## 19.10 Parent Owns Placement

Child visualizers emit semantic events.

The parent Canvas or visualizer determines placement.

---

## 19.11 Compression Preserves State

Compression may hide:

- properties;
- actions;
- collections;
- rails.

It MUST NOT silently destroy:

- provenance;
- selections;
- staged state;
- transaction participation.

---

## 19.12 Prefer Working Slices

New infrastructure should be introduced close to the PR that first exercises it through visible behavior.

Avoid constructing speculative generalized systems several phases before any use.

---

# 20. Overall Capability Progression

The intended progression is:

    DAHN MAP adapter
        |
    VisualizerId runtime
        |
    Rust Selector boundary
        |
    theme tokens
        |
    generic Collection Visualizer
        |
    generic Value Visualizers
        |
    Space Navigator Canvas
        |
    generic Node Visualizer
        |
    descriptor-driven affordances
        |
    inspect plural collections
        |
    navigate down
        |
    navigate right
        |
    compress provenance
        |
    sort / filter
        |
    adaptive ordering
        |
    explicit visualizer choice
        |
    edit staged scalar values
        |
    Canvas transaction state
        |
    Undo / Redo
        |
    Canvas Commit
        |
    edit multiple holons
        |
    Clone / Create / Delete
        |
    edit arrays and relationships
        |
    invoke dances
        |
    personalize actions
        |
    discover Visualizer Commons
        |
    adaptive federated selection
        |
    harden navigation and transactions

Each increment extends the same architecture and visual grammar rather than replacing it.

---

# 21. Handoff to GitHub Issues

Each PR section in this plan is intended to become a separate GitHub enhancement issue.

When generating those issues, each issue SHOULD:

- link to the relevant Architecture Specification section;
- link to the relevant Design Specification section;
- state the narrow behavioral goal;
- state explicit non-goals;
- identify upstream PR dependencies;
- include acceptance criteria;
- avoid re-specifying architectural decisions already owned by the source specifications.

The issue should answer:

> What increment are we implementing now?

The Architecture and Design Specifications should continue to answer:

> Why is the system structured this way, and what behavior is required?