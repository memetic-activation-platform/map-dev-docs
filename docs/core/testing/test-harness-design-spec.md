# Test Harness Design Spec

This document is normative for the **dance test** harness: fixture support, execution support, and
the step adders. It does not apply to conductor tests, which use no fixture, no `TestReference`, and
no executor — see the [Conductor Test Framework](conductor-test-spec.md) and the routing rule in the
[Testing Strategy](../map-holons-testing-strategy.md).

---

## TestReference — Normative Definition with Structural & Rust-Level Detail

This section defines **what a TestReference is**, **what it does**, and **how it is represented structurally and in Rust**.  
It is normative for fixture support, execution support, and the dance test language.

---

## What a TestReference Is

A **TestReference** is an **immutable, fixture-time specification of a single test step**.

It is the **sole artifact** passed from the fixture phase to the execution phase that completely specifies:

1. **What holon the step should operate on**, and
2. **What holon state the step is expected to produce**.

A TestReference does *not* represent runtime state, execution results, or mutable entities.  
It is a **declarative contract** describing *intent* (source) and *expectation* (result) for exactly one test step.

---

## Structural Overview

A TestReference consists of **two role-specific components**:

    TestReference
      ├─ SourceSnapshot    (execution input)
      └─ ExpectedSnapshot  (execution expectation)

These two components use a shared lifecycle vocabulary but serve **distinct purposes**.

---

## Snapshot Identity

Snapshots are identified by a dedicated alias rather than by the reference itself:

    pub type SnapshotId = TemporaryId;

Both `SourceSnapshot::id()` and `ExpectedSnapshot::id()` derive their `SnapshotId` from the
underlying `TransientReference`'s temporary id. All harness maps are keyed by `SnapshotId`.

---

## Shared Lifecycle Vocabulary

All fixture-time holon intent is expressed using a shared descriptive enum.

    #[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
    pub enum TestHolonState {
        Transient,
        Staged,
        Saved,
        SavedLookup,
        Abandoned,
        Deleted,
    }

This enum is:

- Descriptive, not behavioral
- Interpreted differently depending on context (source vs expected)
- Used by fixture support and execution support

`SavedLookup` marks a saved holon that entered the fixture ledger through lookup rather than
through a commit the fixture performed; see [Saved-Content Comparison Semantics](#saved-content-comparison-semantics).

Failure is deliberately **not** a state in this enum. A step expected to fail declares that through
the step's own expected-outcome parameter, not by placing the holon in an error state.

---

## SourceSnapshot — Execution Input

### Purpose

`SourceSnapshot` specifies the **starting holon** that a test step should operate on.

It exists solely to support **execution-time resolution**.

### Rust Structure

    #[derive(new, Clone, Debug, Eq, PartialEq)]
    pub struct SourceSnapshot {
        snapshot: TransientReference,
        state: TestHolonState,
    }

### Field Semantics

- `snapshot`
    - Identifies a **fixture-time transient snapshot**
    - Serves as the *source snapshot token*
    - Its `TemporaryId` is used to:
        - locate the logical FixtureHolon
        - resolve the execution-time source holon
    - **May be redirected** via fixture-level head advancement (commit)

- `state`
    - Intended lifecycle state when the step executes
    - Guides resolution behavior
    - Never mutated

### Conceptual Meaning

The SourceSnapshot answers:

> “Given everything that has happened so far, which execution-time holon should this step run against?”

It does **not** describe what the step produces.

---

## ExpectedSnapshot — Execution Expectation

### Purpose

`ExpectedSnapshot` specifies the **holon state that should exist after the step executes**.

It is used only for **validation and chaining**.

### Rust Structure

    #[derive(new, Clone, Debug, Eq, PartialEq)]
    pub struct ExpectedSnapshot {
        snapshot: TransientReference,
        state: TestHolonState,
    }

### Field Semantics

- `snapshot`
    - Identifies the **expected snapshot produced by this step**
    - Always present. A `Deleted` expectation still carries a snapshot, but that snapshot conveys
      identity only — its content is not meaningful and must not be compared
    - Not subject to execution-time source redirection
    - Immutable historical fact

- `state`
    - Expected lifecycle state after execution
    - Used only for assertions

### Conceptual Meaning

The ExpectedSnapshot answers:

> “What holon state should exist as a result of this step?”

It is never resolved to a runtime holon.

However, fixture-time adders may still reinterpret a target token through
`FixtureHolons` when constructing a new expected relationship graph. In that
case, the adder embeds the logical target holon's **current expected head
snapshot**, not the literal historical snapshot carried by the token.

---

## TestReference — Combined Contract

### Rust Structure

    #[derive(Clone, Debug, Eq, PartialEq)]
    pub struct TestReference {
        source: SourceSnapshot,
        expected: ExpectedSnapshot,
    }

Both fields are private. `TestReference::new` is crate-internal, so only `FixtureHolons` can mint
tokens. Harness code reads the halves through accessors (`source_snapshot()`, `source_id()`,
`expected_snapshot()`, `expected_id()`, and the corresponding reference accessors).

### Semantics

- Immutable once created
- Opaque to TestCase authors and adder authors
- Safe to pass and reuse across steps
- The sole artifact executors receive to understand step intent

A TestReference binds together:

- **Source intent** (what to operate on)
- **Expected outcome** (what should result)

for exactly one test step.

---

## Tight Chaining Rule (Essential Invariant)

The design enforces **tight chaining**:

> The ExpectedSnapshot produced by step *N* is the conceptual SourceSnapshot for step *N+1*.

This chaining is fixture-time and intent-based.

In Rust terms, this is supported by an explicit conversion:

    impl ExpectedSnapshot {
        pub fn as_source(&self) -> SourceSnapshot {
            SourceSnapshot::new(self.snapshot.clone(), self.state)
        }
    }

`as_source` is total — it never panics, and it does not itself decide whether a `Deleted`
expectation is a usable source. That decision belongs to `FixtureHolon`; see
[Deleted Heads and Source Fallback](#deleted-heads-and-source-fallback).

---

## Fixture-Time Head Advancement (Commit Semantics)

`commit` introduces a critical special case.

- Commit mints **new TestReferences** with new snapshot identities
- These snapshots become the **head** for a logical FixtureHolon
- TestCase authors continue using older TestReferences

As a result, the `SourceSnapshot.snapshot` inside an older TestReference may no
longer be the snapshot a later adder should use as the next source. Adders use
`FixtureHolons` during fixture construction to choose the logical holon's
current head and mint a new TestReference for the later step.

Key constraints:

- Only **SourceSnapshots** participate in fixture-time source derivation
- **ExpectedSnapshots are never used for execution-time source lookup**
- Relationship adders may still resolve target tokens to the current expected
  head snapshot during fixture-time graph construction
- TestReferences themselves are never mutated

This preserves immutability while allowing logical continuity across commit boundaries.

---

## What a TestReference Is Not

A TestReference is **not**:

- a runtime handle
- a mutable reference
- a unique holon identity
- an execution result
- a guarantee that its embedded snapshot will be the execution source

---

## One-Sentence Definition

> A **TestReference** is an immutable fixture-time contract that specifies, for a single test step, the intended source holon to execute against and the expected holon state the step should produce — while `FixtureHolons` separately tracks logical fixture-holon heads so later adders can interpret older tokens correctly after commit.

This definition should be treated as **foundational and normative** across the Dance Test Framework.

## FixtureHolons & FixtureHolon — Normative Definition with Structural & Rust-Level Detail

This section defines **what FixtureHolons and FixtureHolon are**, **why they exist**, and **how they are represented structurally and in Rust**.  
It is normative for fixture support, commit semantics, and fixture-time source and relationship-target selection.

---

## Why FixtureHolons Exist

`TestReference`s describe **individual test steps**.  
They do *not* describe **entity identity across steps**.

However, the Dance Test Framework must reason about:

- which snapshots refer to the *same logical holon*
- which snapshot is the *current head* of that holon
- how `commit` advances holon state across multiple steps
- how older TestReferences remain valid after commit

This requires an explicit fixture-time concept of **logical holon identity**.

That concept is `FixtureHolon`.

---

## FixtureHolon — Logical Holon Identity (Fixture-Time)

### What a FixtureHolon Is

A **FixtureHolon** represents a **single logical holon** as it evolves across multiple test steps during the Fixture Phase.

It is:

- fixture-time only
- mutable
- authoritative for lifecycle state and head selection
- never exposed to TestCase authors or executors

A FixtureHolon answers the question:

> “Across all the snapshots created so far, what is the current state of this logical holon?”

---

### Rust Structure

    #[derive(new, Clone, Debug)]
    pub struct FixtureHolon {
        head_snapshot: ExpectedSnapshot,
        last_live_snapshot: ExpectedSnapshot,
    }

Logical identity is the **map key**, not a field: `FixtureHolonId` is a `Uuid` newtype under which
`FixtureHolons` stores the entry. Lifecycle state is likewise **derived**, not stored — `state()`
returns `head_snapshot.state()`.

---

### Field Semantics

- `head_snapshot`
    - The **authoritative expected snapshot** for this holon
    - Always refers to the most recent snapshot representing the holon’s state
    - Updated whenever:
        - a step mutates the holon
        - a commit advances the holon
    - This is the mechanism that enables fixture-time head selection

- `last_live_snapshot`
    - The most recent snapshot that is **not** `Deleted`
    - Used as the source when the head represents a deleted holon

Lifecycle progressions a FixtureHolon records:

- `Transient` → `Staged` → `Saved`
- `Saved` → `Deleted`
- `Staged` → `Abandoned`

---

### Deleted Heads and Source Fallback

A logical holon whose head is `Deleted` is still a legitimate source for later steps — that is what
makes delete-after-delete and other post-delete assertions expressible.

`FixtureHolon` resolves this internally when an adder asks it for a source:

    fn resolve_snapshot_as_source(&self) -> SourceSnapshot {
        if self.head_snapshot.state() == TestHolonState::Deleted {
            self.last_live_snapshot.as_source()
        } else {
            self.head_snapshot.as_source()
        }
    }

Consequences:

- The `Deleted` head is never converted into a source snapshot
- The step that follows a delete operates against the last live snapshot, carrying its content
- Adders must not implement this fallback themselves; it belongs to `FixtureHolon`

---

## FixtureHolons — Fixture-Time Registry

### What FixtureHolons Is

`FixtureHolons` is the **authoritative fixture-time registry** for:

- all TestReferences ever minted
- all logical FixtureHolons
- the mapping between snapshot tokens and logical holons

It is the *only* component allowed to:

- mint TestReferences
- create FixtureHolons
- advance head snapshots
- interpret commit semantics

---

### Rust Structure

    #[derive(Clone, Debug, Default)]
    pub struct FixtureHolons {
        pub tokens: Vec<TestReference>,
        pub holons: BTreeMap<FixtureHolonId, FixtureHolon>,
        pub snapshot_to_fixture_holon: BTreeMap<SnapshotId, FixtureHolonId>,
    }

---

### Field Semantics

- `tokens`
    - Append-only history of all TestReferences minted during fixture construction
    - Preserves complete fixture-time intent
    - Never mutated or reordered
    - Used for:
        - debugging
        - diagnostics
        - executor coordination

- `holons`
    - Map of logical holon identity → FixtureHolon
    - One entry per logical holon in the test case
    - Authoritative source of:
        - lifecycle state
        - current head snapshot

- `snapshot_to_fixture_holon`
    - Maps **any `SnapshotId`** to its owning FixtureHolon
    - Consulted exclusively when resolving source snapshots; expected snapshots are registered here
      only so they are available for later chaining
    - Enables:
        - interpreting older TestReferences as logical-holon handles when
          deriving later source snapshots
        - resolving target tokens to current expected heads when building
          expected relationship graphs
        - reuse of prior steps (e.g. delete-after-delete)
    - Critical for commit semantics

---

## Head Selection — Where It Actually Lives

**Head selection is not a TestReference concept.**  
It is a **FixtureHolons responsibility**.

### What Head Selection Means

- A TestReference may embed a snapshot token that is no longer current
- The snapshot still identifies the *logical holon*
- FixtureHolons determines the **current head snapshot** for that holon

### How It Works

When an adder derives the source for a later step:

1. The `SnapshotId` is extracted from the TestReference's source side
2. `snapshot_to_fixture_holon` maps it to a `FixtureHolonId`
3. The corresponding `FixtureHolon` selects its source snapshot — the head, or the last live
   snapshot when the head is `Deleted`
4. That snapshot is used to mint the new TestReference's source side

This is what allows:

- commit to mint new snapshots
- older TestReferences to remain valid
- test authors to ignore token churn

### Relationship-Target Expected Resolution

Relationship adders use a different `FixtureHolons` interpretation path from
fixture-time source derivation.

When an adder needs to embed relationship targets into a new expected graph:

1. The target token's expected `SnapshotId` is extracted
2. `snapshot_to_fixture_holon` maps it to the owning `FixtureHolonId`
3. The corresponding `FixtureHolon.head_snapshot` is retrieved
4. That current expected head snapshot is embedded as the relationship target

This prevents stale target snapshots from being frozen into expected graphs when
the fixture author passes an older token for a logical holon whose head has
advanced.

So there are three distinct harness behaviors:

- **fixture-time source derivation** uses the source side of `TestReference`
  as a handle to the logical holon's current head
- **fixture-time relationship-target expected resolution** uses the expected
  side token as a handle to the logical holon's current expected head
- **execution-time source resolution** uses the source side of the step token
  to look up recorded runtime handles through `ExecutionHolons`

Those behaviors are related, but they are not the same operation.

---

## Commit Semantics (Fixture-Time)

`commit` operates over **FixtureHolons**, not TestReferences.

### Commit Responsibilities

For each `FixtureHolon` whose `state()` is `Staged`:

1. Clone the head snapshot
2. Mint a new TestReference with:
    - `ExpectedSnapshot.state` = `Saved`
    - A new snapshot token
3. Update `FixtureHolon.head_snapshot` → the new snapshot. State follows automatically, because it
   is derived from the head
4. Append the new TestReference to `tokens`

Holons in `Abandoned` or `Saved` state are skipped: commit mints a saved-intent token only for a
staged holon whose head is neither already saved nor abandoned.

### Important Constraints

- Commit **must mint new TestReferences**
- Commit **must not mutate existing TestReferences**
- Commit **does not return TestReferences to test authors**
- Head advancement is purely internal to FixtureHolons

---

## Saved-Content Comparison Semantics

`MatchSavedContent` compares saved roots by:

1. essential holon content
2. exact definitional relationship presence/member agreement

Implications:

- non-definitional persisted edges, including commit-generated inverse
  SmartLinks, are intentionally ignored by saved-content equality
- definitional relationship members are matched by saved holon identity where
  the harness has recorded the committed realization
- each saved fixture holon is still compared independently as its own root, so
  nested member content is not recursively revalidated from every relationship
  occurrence

Saved-lookup stubs remain a harness-specific special case for holons created
outside the fixture ledger.

---

## What FixtureHolons Is Not

FixtureHolons is **not**:

- a runtime registry
- an execution cache
- visible to executors
- responsible for validation or assertions

It exists solely to make fixture-time intent coherent and executable.

---

## One-Sentence Definitions

**FixtureHolon**
> A mutable, fixture-time representation of a single logical holon that tracks its lifecycle state and current head snapshot across test steps.

**FixtureHolons**
> The authoritative fixture-time registry that mints TestReferences, tracks logical holon identity, advances head snapshots (especially during commit), and enables adders to derive correct source snapshots and expected relationship targets.

These definitions should be treated as **normative** throughout the Dance Test Framework.
