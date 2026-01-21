# Dance Test Refactor – TestCase Authoring Guide

This guide is for **TestCase definers**: people who write test cases using the Dance Test Language.  
It explains what you need to know — and, just as importantly, what you *do not* need to know.

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

Think of a `TestReference` as “the thing this step refers to,” not as a data structure.

---

## 3. The Basic Authoring Pattern

Most TestCases follow a simple pattern:

1. Create or obtain a starting TestReference
2. Apply one or more adders to it
3. Optionally call `commit`
4. Continue with additional steps

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

---

## 7. What You Should Never Do

As a TestCase definer, you should never:

- Inspect the contents of a TestReference
- Clone or mutate snapshots yourself
- Construct TestReferences manually
- Assume anything about internal IDs or references
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

If a TestCase reads clearly, it is probably correct.

---

## 10. Summary

- TestCases are declarative sequences of steps
- TestReferences are opaque handles
- Adders do the hard work
- Commit finalizes changes without breaking flow
- If authoring feels complicated, the design needs improvement

That is the promise of the Dance Test Refactor.