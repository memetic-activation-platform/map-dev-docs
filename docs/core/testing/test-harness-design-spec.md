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
      ├─ SourceHolon    (execution input)
      └─ ExpectedHolon  (execution expectation)

These two components use a shared lifecycle vocabulary but serve **distinct purposes**.

---

## Shared Lifecycle Vocabulary

All fixture-time holon intent is expressed using a shared descriptive enum.

    #[derive(Clone, Copy, Debug, Eq, PartialEq)]
    pub enum TestHolonState {
        Transient,
        Staged,
        Saved,
        Abandoned,
        Deleted,
    }

This enum is:

- Descriptive, not behavioral
- Interpreted differently depending on context (source vs expected)
- Used by fixture support and execution support

---

## SourceHolon — Execution Input

### Purpose

`SourceHolon` specifies the **starting holon** that a test step should operate on.

It exists solely to support **execution-time resolution**.

### Rust Structure

    #[derive(Clone, Debug, Eq, PartialEq)]
    pub struct SourceHolon {
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

The SourceHolon answers:

> “Given everything that has happened so far, which execution-time holon should this step run against?”

It does **not** describe what the step produces.

---

## ExpectedHolon — Execution Expectation

### Purpose

`ExpectedHolon` specifies the **holon state that should exist after the step executes**.

It is used only for **validation and chaining**.

### Rust Structure

    #[derive(Clone, Debug, Eq, PartialEq)]
    pub struct ExpectedHolon {
        snapshot: Option<TransientReference>,
        state: TestHolonState,
    }

### Field Semantics

- `snapshot`
    - `Some(snapshot)` for all non-deleted outcomes
    - `None` iff `state == TestHolonState::Deleted`
    - Identifies the **expected snapshot produced by this step**
    - **Never redirected**
    - Immutable historical fact

- `state`
    - Expected lifecycle state after execution
    - Used only for assertions

### Conceptual Meaning

The ExpectedHolon answers:

> “What holon state should exist as a result of this step?”

It is never resolved to a runtime holon.

---

## TestReference — Combined Contract

### Rust Structure

    #[derive(Clone, Debug, Eq, PartialEq)]
    pub struct TestReference {
        source: SourceHolon,
        expected: ExpectedHolon,
    }

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

> The ExpectedHolon snapshot produced by step *N* is the conceptual SourceHolon snapshot for step *N+1*.

This chaining is fixture-time and intent-based.

In Rust terms, this is supported by an explicit conversion:

    impl ExpectedHolon {
        pub fn as_source(&self) -> SourceHolon {
            SourceHolon {
                snapshot: self
                    .snapshot
                    .as_ref()
                    .expect("Deleted holons cannot be used as source")
                    .clone(),
                state: self.state,
            }
        }
    }

---

## Head Redirection (Commit Semantics)

`commit` introduces a critical special case.

- Commit mints **new TestReferences** with new snapshot identities
- These snapshots become the **head** for a logical FixtureHolon
- TestCase authors continue using older TestReferences

As a result:

- The `SourceHolon.snapshot` inside a TestReference is **not authoritative**
- At execution time:
    1. The source snapshot token identifies a logical FixtureHolon
    2. The FixtureHolon’s **current head snapshot** is used as the true execution source

Key constraints:

- Only **SourceHolon snapshots** are subject to head redirection
- **ExpectedHolon snapshots are never redirected**
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

> A **TestReference** is an immutable fixture-time contract that specifies, for a single test step, the intended source holon to execute against and the expected holon state the step should produce — with execution-time source resolution mediated by fixture-level head redirection when commit intervenes.

This definition should be treated as **foundational and normative** across the Dance Test Framework.

## FixtureHolons & FixtureHolon — Normative Definition with Structural & Rust-Level Detail

This section defines **what FixtureHolons and FixtureHolon are**, **why they exist**, and **how they are represented structurally and in Rust**.  
It is normative for fixture support, commit semantics, and execution-time source resolution.

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

    #[derive(Clone, Debug)]
    pub struct FixtureHolon {
        pub id: FixtureHolonId,
        pub state: TestHolonState,
        pub head_snapshot: TransientReference,
    }

---

### Field Semantics

- `id`
    - Stable fixture-time identity for this logical holon
    - Used only internally by the harness
    - Multiple TestReferences may map to the same `FixtureHolonId`

- `state`
    - Current lifecycle state of the holon at fixture time
    - Authoritative summary derived from the latest head snapshot
    - Updated by adders and by `commit`
    - Examples:
        - `Transient` → `Staged` → `Saved`
        - `Saved` → `Deleted`
        - `Staged` → `Abandoned`

- `head_snapshot`
    - The **authoritative snapshot token** for this holon
    - Always refers to the most recent snapshot that represents the holon’s state
    - Updated whenever:
        - a step mutates the holon
        - a commit advances the holon
    - This is the mechanism that enables **head redirection**

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

    pub struct FixtureHolons {
        pub tokens: Vec<TestReference>,
        pub holons: BTreeMap<FixtureHolonId, FixtureHolon>,
        pub snapshot_to_holon: BTreeMap<TransientReference, FixtureHolonId>,
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

- `snapshot_to_holon`
    - Maps **any snapshot token** to its owning FixtureHolon
    - Enables:
        - resolving older TestReferences to current heads
        - reuse of prior steps (e.g. delete-after-delete)
    - Critical for commit semantics

---

## Head Redirection — Where It Actually Lives

**Head redirection is not a TestReference concept.**  
It is a **FixtureHolons responsibility**.

### What Head Redirection Means

- A TestReference may embed a snapshot token that is no longer current
- The snapshot still identifies the *logical holon*
- FixtureHolons determines the **current head snapshot** for that holon

### How It Works

When a SourceHolon is resolved at execution time:

1. The SourceHolon snapshot token is extracted from the TestReference
2. `snapshot_to_holon` maps it to a `FixtureHolonId`
3. The corresponding `FixtureHolon.head_snapshot` is retrieved
4. That head snapshot is used to resolve the execution-time holon

This is what allows:

- commit to mint new snapshots
- older TestReferences to remain valid
- test authors to ignore token churn

---

## Commit Semantics (Fixture-Time)

`commit` operates over **FixtureHolons**, not TestReferences.

### Commit Responsibilities

For each `FixtureHolon` whose `state == Staged`:

1. Clone the head snapshot
2. Mint a new TestReference with:
    - ExpectedHolon.state = `Saved`
    - A new snapshot token
3. Update:
    - `FixtureHolon.head_snapshot` → new snapshot
    - `FixtureHolon.state` → `Saved`
4. Append the new TestReference to `tokens`

### Important Constraints

- Commit **must mint new TestReferences**
- Commit **must not mutate existing TestReferences**
- Commit **does not return TestReferences to test authors**
- Head advancement is purely internal to FixtureHolons

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
> The authoritative fixture-time registry that mints TestReferences, tracks logical holon identity, advances head snapshots (especially during commit), and enables correct execution-time source resolution.

These definitions should be treated as **normative** throughout the Dance Test Framework.