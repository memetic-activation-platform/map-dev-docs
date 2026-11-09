# TestCase Authoring Guide

This guide is for **TestCase definers**: people who write test cases using the Dance Test Language.  
It explains what you need to know — and, just as importantly, what you *do not* need to know.

> **First, check you want a dance test.** Dance tests assert client-side semantics — staging,
> chaining, commit, relationships, saved content. If your assertion requires direct evidence of Integrity execution
> or the substrate record itself, write a
> [conductor test](conductor-test-spec.md) instead; none of the machinery below applies to it.

If you find yourself worrying about snapshot cloning, execution-time resolution, or holon lifecycle edge cases, that is a sign the test language needs improvement, not that you need to work harder.

---

## 1. Your Role as a TestCase Definer

Your job is to:

- Describe **what should happen**
- In a clear, readable sequence of steps
- Using the provided Dance Test Language adders

You are **not** responsible for:

- Managing holon lifecycles
- Cloning or mutating snapshots
- Handling fixture-time vs execution-time differences
- Resolving IDs or references
- Dealing with commit internals

Those concerns are intentionally encapsulated by the test language.

---

## 2. What You Work With

You primarily work with:

- **TestReferences**
- **Dance Test Language adders** (functions that add test steps)

A `TestReference` is an **opaque handle**:

- You pass it into adders
- You receive a new one back
- You do not inspect it
- You do not modify it

It is best to think of a `TestReference` as a handle to a **logical fixture
holon**, not as a promise that the literal snapshot inside the token is always
the exact snapshot every later harness operation will use.

Think of a `TestReference` as “the thing this step refers to,” not as a data structure.

---

## 3. The Basic Authoring Pattern

Most TestCases follow a simple pattern:

1. Open with `TestCaseInit::new(name, description)`, destructuring the test case, fixture context,
   `FixtureHolons`, and `FixtureBindings`
2. Create or obtain a starting TestReference
3. Apply one or more adders to it
4. Optionally call `commit`
5. Continue with additional steps
6. Close with `finalize()` — exactly once, after the last step and before returning the case

Steps 1 and 6 are a matching pair. `finalize()` is what carries your fixture-time transient holons
into the execution phase, so a case that skips it will not resolve the references you minted. It
also locks the case: adders called afterward will fail.

Conceptually:

- Each adder represents a test step
- Each step builds on the previous one
- The sequence reads top-to-bottom like a story

You should be able to read a TestCase and understand it without knowing anything about the test harness internals.

---

## 4. Chaining Steps

When you call an adder:

- You pass in a TestReference
- The adder returns a new TestReference
- That returned reference is what you use for the next step

You do not need to think about:
- how the reference was constructed
- whether it represents a staged or saved holon
- how snapshots are cloned

The rule is simple:

**Always use the most recently returned TestReference for that holon.**

Why this still matters even though older tokens remain usable:

- it keeps the test readable
- it keeps your intent aligned with the latest expected state
- it avoids relying on subtle harness behavior around head advancement and
  relationship-target interpretation

---

## 5. Understanding Commit (at a High Level)

`commit` is a special step that finalizes staged changes.

As a TestCase definer:

- You call `commit` when you want staged changes to be saved
- `commit` does not return a TestReference
- After `commit`, you continue using the same logical reference

You do **not** need to:
- capture a new reference after commit
- update your variables
- reason about which holons were committed

The test framework ensures that subsequent steps operate on the committed state.

One important nuance:

- after `commit`, older tokens remain safe to use as logical handles
- but you should still prefer the newest returned token for readability and to
  keep your fixture aligned with the latest expected state

---

### Saved-content and bounded graph checks

Use `add_match_saved_content_step()` after Commit to compare fixture-established
properties and definitional content. For graph scenarios, set
`test_case.verify_committed_workset = true` during authoring. Complete Commit then
verifies the declared workset's persisted memberships, inverse occurrences, and
exact lineage, retaining expectations through Incomplete retries. Do not repeat
those guarantees with a separate `VerifyPersistedGraph` step. Use standalone graph
assertions only for an explicit requirement outside the shared Commit contract.
See [bounded persisted verification](test-harness-design-spec.md#bounded-persisted-verification-at-commit)
for partial lookup subjects, inverse bindings, and the limits of automatic checks.

Compatible cases can share a suite's committed bootstrap while retaining separate
transactions and fixture registries. Order cases and their steps explicitly when
an assertion requires an initially absent membership. Cases requiring a fresh host
Session or cache must establish that boundary separately; sharing a conductor does
not require sharing those host objects. Keep fault-injection scenarios on probe
conductors, separate from ordinary runtime suites.

---

## 6. Delete and Error Scenarios

You can author tests that:

- Delete a holon
- Attempt to delete an already-deleted holon
- Expect failures or errors

You do this by:

- Using the same TestReference
- Applying the appropriate adder
- Declaring the expected outcome via the adder

You do not need to:
- check current state before calling delete
- guard against invalid operations manually

The test language exists to make these scenarios safe and expressive.

The same general principle applies to relationship steps:

- pass the logical target holon token you mean
- let the harness decide how that token should be interpreted
- do not try to reason about whether the token carries the “right” historical
  snapshot

---

### Bounded checks for rejected creates

For a rejection scenario containing new keyed roots, use
`add_commit_step_with_rejection_checks(&fixture_holons, unchanged_relationships, description)`
when the relevant existing saved collections are known. The adder captures the full staged
fixture workset; do not list just the candidate expected to carry a validation finding.

Declare affected existing collections with `NamedRelationshipSubject { source, relationship }`.
For instance, guard each saved descriptor's `Instances` collection when new instances refer to
it through `DescribedBy`. Continue using `add_verify_commit_rejection_step` to specify exact
findings, then correct the staged holon using the ordinary adders and retry Commit.

This contract requires unique, nonempty keys and supports new-root creates only. Existing Commit
entrypoints retain their current behavior. The test-step guide describes the
[authoring contract](test-step-authoring-guide.md#26-fixture-scoped-rejection-checks) and
[persisted observation rules](test-step-authoring-guide.md#34-executing-fixture-scoped-rejection-verification).

---

## 7. What You Should Not Do

As a TestCase definer, you should never:

- Inspect the contents of a TestReference
- Clone or mutate snapshots yourself
- Construct TestReferences manually
- Assume anything about internal IDs or references
- Assume old tokens universally “follow the head” in every context
- Bypass the Dance Test Language to “do it yourself”

If you feel tempted to do any of the above, it likely means a missing or insufficient adder should be added instead.

---

## 8. When You Need Something New

Sometimes you will need to express a test step that does not yet exist.

When that happens:

- Do **not** hack around the test language
- Instead, request or define a **new adder**

Adder authors are responsible for:
- encapsulating complexity
- preserving invariants
- keeping TestCase authoring simple

Your TestCase should remain clean and declarative.

---

## 9. Mental Model to Keep in Mind

- You are writing a **story**, not a program
- Each step says “do this, then expect that”
- The framework handles the mechanics
- Clarity and intent matter more than mechanics

Two practical consequences of that model:

- When an adder returns a new token, keep chaining with it.
- When a step needs to verify saved database structure, prefer
  `MatchSavedContent` for structural saved-state checks and use targeted
  traversal/assertion steps when you need to verify non-definitional
  navigational edges explicitly.

If a TestCase reads clearly, it is probably correct.

---

## 10. Summary

- TestCases are declarative sequences of steps
- TestReferences are opaque handles
- Adders do the hard work
- Commit finalizes changes without breaking flow
- If authoring feels complicated, the design needs improvement

That is the promise of the Dance Test Refactor.
