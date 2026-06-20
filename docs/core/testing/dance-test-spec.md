# Dance Test Framework -- Design Specification

The goal of the Dance Test Framework is to make it easier and less error-prone to author and execute test cases. A **Test Case** is composed of a sequence of **Test Steps**.

The framework distinguishes two distinct phases:

1. **Test Case Definition (Fixture Phase)**
2. **Test Case Execution (Execution Phase)**

During the Fixture Phase, a test case is created and test steps are added using a set of **step adders** defined in the Dance Test Language module. These adders are the *authoring-time building blocks* from which Test Cases are composed.

During the Execution Phase, each Test Step is executed by a corresponding **step executor**, which performs the actual operation and validates that the observed result matches the expected result defined during the Fixture Phase.

Thus:

- **Adders** are Fixture Phase building blocks for *describing intent and expectations*.
- **Executors** are Execution Phase building blocks for *performing operations and validating outcomes*.
- The **harness** provides the shared data structures and orchestration that connect these two phases safely and deterministically.

---

## 0. Design Lineage & Rationale

### 0.1 Original Design Intent

The original Dance Test design aimed to:

- Separate **fixture-time test definition** from **execution-time behavior**
- Allow test steps to be chained safely
- Preserve snapshot immutability
- Make TestCase authoring declarative and low-friction

However, some concepts—particularly around **step inputs vs step outputs**—were implicit rather than explicit.

---

### 0.2 Converged Design Principle (Hybrid Model)

The converged design is based on the following principle:

> A test step has both a **starting point** and an **expected result**, and these two roles have different semantics but must travel together as a single, immutable contract.

Rather than modeling separate “input tokens” and “output tokens”, the design models **two roles within a single TestReference**, with clear semantics, strong guardrails, and a clean separation between fixture-time intent and execution-time resolution.

This hybrid approach:

- Preserves the critical insight that steps have two snapshots
- Avoids introducing multiple tokens per step
- Keeps TestCase authoring simple and linear
- Encapsulates complexity inside adders and the harness

---

## 1. Design Goals

The design must:

- Make **TestCase definition easier, faster, and less error prone**
- Allow TestCase authors to **compose test steps declaratively**
- Encapsulate complexity inside **Dance Test Language adders**
- Preserve **immutable snapshot semantics**
- Cleanly separate **fixture-time** from **execution-time**
- Support reuse of prior steps (e.g. delete-after-delete)
- Correctly model **commit** as a multi-entity operation
- Provide clear guidance for future adder and executor authors

---



## 2. Core Concepts

---

## 2.1 Shared Holon State Vocabulary

A single enum defines the **lifecycle state of a holon at a point in time**, shared across fixture-time modeling and execution-time validation.

    pub enum TestHolonState {
        Transient,
        Staged,
        Saved,
        Abandoned,
        Deleted,
        Error,
    }

Though this same structure is used on both the source-side and expected-side, its purpose is very different. On the source-side, it is used during the process of resolving token
This enum is **descriptive, not behavioral**.  
. For example, the TestHolonState is  (fixture-time expectation vs execution-time outcome).

---

## 2.2 TestReference (Step Contract)

A `TestReference` is the **immutable contract for a single Test Step**.

It has **two essential jobs**:

1. **Provide the Test Step executor with a starting point**
2. **Provide the executor with the expected result to validate against**

A TestReference is:

- Immutable once created
- Opaque to TestCase authors and adder authors
- Safe to pass and reuse across steps
- The sole artifact executors receive to understand step intent

Structurally, it contains two conceptual halves:

    pub struct TestReference {
        source: SourceHolon,
        expected: ExpectedHolon,
    }

All fields are private; interaction is via controlled accessors only.

---

## 2.3 SourceHolon (Execution Starting Point)

The **source side** of a TestReference exists to answer the question:

> “What holon should this step operate on at execution time?”

    pub struct SourceHolon {
        reference: TransientReference,
        state: TestHolonState,
    }

    impl SourceHolon {
        pub fn token_id(&self) -> TokenId {
            self.reference.temporary_id()
        }
    }

### Semantics

- Identifies the holon that execution should target
- Carries the *intended lifecycle state* used during execution-time resolution
- Never mutated
- Used only by executors and the harness

The source side does **not** represent mutable state or expected content.

---

## 2.4 ExpectedHolon (Expected Result)

The **expected side** of a TestReference exists to answer the question:

> “What should the result of this step be?”

    pub struct ExpectedHolon {
        snapshot: Option<HolonSnapshot>,
        state: TestHolonState,
    }

    pub struct HolonSnapshot {
        transient_ref: TransientReference,
    }

### Semantics

- Used only for **validation and chaining**
- Never resolved at execution time
- Snapshot is immutable
- `snapshot == None` if and only if `state == Deleted`

Executors compare actual outcomes against the expected holon; they never attempt to resolve it.

However, fixture-time adders may still interpret a `TestReference` as a handle to
its owning logical FixtureHolon when constructing a new expected graph. In
particular, relationship adders may resolve a target token to the logical
holon's **current expected head snapshot** rather than embedding the literal
historical snapshot carried by the token.

---

## 2.5 Chaining Semantics

Conceptually:

> The expected result of step *N* becomes the starting point for step *N+1*.

This chaining is expressed in fixture-time logic and enforced by adders and the harness, not by TestCase authors manually wiring references.

ExpectedHolon provides a controlled way to derive a new source:

    impl ExpectedHolon {
        pub fn as_source(&self) -> SourceHolon {
            SourceHolon {
                reference: self
                    .snapshot
                    .as_ref()
                    .expect("Deleted holons cannot be used as source")
                    .transient_ref
                    .clone(),
                state: self.state.clone(),
            }
        }
    }

---

## 3. Immutability & Guardrails

### 3.1 Fundamental Invariant

> **Adders must never mutate holons obtained from a TestReference.**

All mutation must occur on **fresh clones** created explicitly inside the adder.

### 3.2 Structural Enforcement

Immutability is enforced by design:

- Adders receive TestReferences, not holons
- Internal references are private
- ExpectedHolon exposes mutation only via explicit cloning

  impl ExpectedHolon {
  pub fn clone_for_mutation(&self) -> Option<TransientHolon> {
  self.snapshot
  .as_ref()
  .map(|s| s.transient_ref.clone_holon())
  }
  }

This makes accidental mutation of prior snapshots difficult or impossible.

---

## 4. Role of Adders and the Dance Test Language

The Dance Test Language exists to **encapsulate complexity so TestCases remain simple**.

Adders are responsible for:

- Obtaining the correct starting snapshot
- Obtaining the correct expected relationship targets when building expected graphs
- Enforcing lifecycle rules
- Preserving immutability
- Managing fixture-time identity
- Encoding commit, delete, and error semantics
- Minting new TestReferences

TestCase authors compose steps; adders absorb nuance and prevent footguns.

> **Adders are the primary abstraction boundary of the framework.**

---

## 5. Fixture-Time Identity: FixtureHolons

TestReferences describe **step results**, but they do not model **entity identity across steps**.

That role is handled by FixtureHolons.

    pub struct FixtureHolon {
        pub id: FixtureHolonId,
        pub state: TestHolonState,
        pub head_token: TokenId,
    }

    pub struct FixtureHolons {
        pub tokens: Vec<TestReference>,
        pub holons: std::collections::HashMap<FixtureHolonId, FixtureHolon>,
        pub token_to_holon: std::collections::HashMap<TokenId, FixtureHolonId>,
    }

### Semantics

- Every TestReference belongs to exactly one FixtureHolon
- Multiple TestReferences may refer to the same FixtureHolon
- FixtureHolon state and head token are authoritative for “current” state

---

## 6. Snapshot Currency and Token Interpretation

A key requirement—especially after commit—is that:

> The token passed to an adder must be treated as a **stable handle to a holon**, not as a guarantee of snapshot currency.

Therefore:

- The literal snapshots carried inside a `TestReference` remain immutable historical facts
- `FixtureHolons` is authoritative for deciding how a token should be interpreted
- Different harness APIs may intentionally interpret the same token differently depending on purpose

In the current model, the important interpretations are:

- **Source derivation**
    - adders use `FixtureHolons` to derive the appropriate next source snapshot
    - when an older token is passed to a later adder after commit, the adder
      mints a new step token whose source reflects the logical holon's current
      fixture-time head
- **Relationship-target expected resolution**
    - relationship adders resolve target tokens through `FixtureHolons`
    - this embeds the target logical holon's **current expected head snapshot**
      in the new expected relationship graph
- **Execution-time resolution**
    - executors use the source side of `TestReference`
    - runtime resolution remains a separate concern from fixture-time graph construction

This behavior is embedded in harness APIs, not exposed as a new token type.

Consequences:

- Passing an older token after commit is safe when the receiving adder uses
  `FixtureHolons` to interpret it as a logical fixture-holon handle
- TestCase authors do not need to update references
- Adders do not need to reason about commit explicitly when deriving sources
- Relationship adders must not assume that embedding a token's literal expected
  snapshot is the right target behavior

Terminology rule:

- “Head” and “current” are fixture-time concepts
- Prefer “derive” or “select” for fixture-time head decisions, and
  “resolve” for execution-time runtime-reference lookup. Existing helper names
  may use “resolve” for fixture-time target selection, but the surrounding text
  should make the phase explicit.

---

## 7. Commit

### 7.1 Why Commit Is Special

Commit does not operate on a single TestReference.

At runtime, commit:

- Iterates over the holon pool
- Attempts to commit all staged, non-abandoned holons

At fixture time, the commit adder mirrors that global shape through
`FixtureHolons`:

> **Commit reasons over FixtureHolons, not tokens.**

---

### 7.2 Commit Behavior (Fixture Phase)

During the Fixture Phase, the commit adder:

1. Iterates over all FixtureHolons
2. Selects those in `Staged` state
3. Predicts commit outcomes
4. Updates FixtureHolon state to `Saved` or `Error`
5. Mints **new head TestReferences** so the post-commit expected state is represented

These new head tokens:

- Are recorded internally
- Are not returned to TestCase authors
- Are consulted later through `FixtureHolons` when adders derive sources or
  relationship-target expectations

This allows commit to be global without breaking linear authoring.

---

## 8. Execution-Time Resolution

At execution time, TestReferences are mapped to runtime holon references through
the execution registry, not through `FixtureHolons`.

Execution-time resolution:

- Uses the source side of TestReference
- Looks up the recorded execution result for that source snapshot via
  `ExecutionHolons`
- Interprets intended lifecycle state
- Chooses the appropriate runtime representation
- Extracts saved holon IDs when required (e.g. delete)

ExpectedHolon is **never resolved** at execution time.

Fixture-time interpretation of relationship target tokens is separate from this:
relationship adders may use `FixtureHolons` to select the current expected head
snapshot for graph expectations, but that does not mean the `ExpectedHolon`
itself is execution-resolved.

---

## 9. Saved-Content Comparison Semantics

`MatchSavedContent` does not require exact equality across every persisted edge.

Instead, saved roots are compared by:

1. essential holon content
2. exact definitional relationship presence/member agreement

Under this rule:

- non-definitional persisted edges, including commit-generated inverse
  SmartLinks, are intentionally ignored by saved-content equality
- definitional relationship members are compared by saved holon identity where
  applicable
- each saved fixture holon is still compared independently as its own root, so
  nested relationship member content is not recursively revalidated from every
  occurrence of every edge

Implication for test authors:

- use `MatchSavedContent` to assert saved structural identity
- use targeted traversal/assertion steps when a test needs to verify
  non-definitional navigational edges explicitly

---

## 10. Delete Semantics

- Delete requires a saved holon identity
- Saved identity is obtained from execution-time resolution
- Deleted expected holons contain no snapshot

Delete-after-delete scenarios are supported by reusing appropriate source TestReferences and validating expected outcomes.

---

## 10. Conceptual Summary

- **TestReference** is the step contract: starting point + expected result
- **SourceHolon** defines what execution operates on
- **ExpectedHolon** defines what should result
- **FixtureHolon** defines entity identity across steps
- **Head token** defines snapshot currency
- **Adders** encapsulate complexity
- **Commit** advances lifecycle globally
- **Execution** resolves and validates

This hybrid design preserves implementation insights, keeps authoring simple, and prevents subtle lifecycle and aliasing bugs.

---

## 11. Status

This document reflects the **current converged design** of the Dance Test Framework and should be used as the conceptual foundation for implementation, review, and onboarding.
