# Test Step Authoring Guide (Adder + Executor)

This guide is for authors of **new test steps** and maintainers updating existing ones.

A “test step” always has two halves:

- a **Fixture-phase adder** (in `dance_test_language`) that *specifies and registers* the step, and
- an **Execution-phase executor** (in `execution_steps`) that *runs* the step and *records* its outcome.

The goal is to make TestCase authoring **easy, fast, and safe** by encapsulating subtle correctness requirements inside adders and harness helpers.

---

## 1. Core Concept: A Step Is a Contract

It is a **contract** composed during the Fixture Phase.

That contract specifies:

- **Source intent**: what holon the executor should operate on
- **Expected outcome**: what holon state the step should produce
- **Step parameters**: any additional data needed to perform the operation

This contract is materialized as:

- a `TestReference` (source + expected), and
- a concrete `TestStep` struct holding the TestReference plus step-specific parameters.

---

## 2. Adder Responsibilities (Fixture Phase)

### 2.1 Purpose of an Adder

An adder’s job is to **fully define and register one test step**.

Specifically, an adder must:

- derive the step’s source specification from an input `TestReference`
- compute the expected holon state produced by the step
- mint a new `TestReference` describing that step
- decide whether the step continues an existing logical holon or creates a new one
- **construct the concrete `TestStep`**
- **append that TestStep to the `TestCase`**

Adders exist so TestCase authors never need to reason about snapshot lifetimes, commit semantics, or token redirection.

---

### 2.2 Adder Inputs and Outputs

Conceptually, every adder follows this pattern:

**Inputs**
- a source `TestReference` (unless the step is global, e.g. `commit`)
- step-specific parameters (PropertyMap, relationship ops, flags, etc.)
- mutable access to `FixtureHolons`
- access to the fixture context (for cloning snapshots)

**Outputs**
- a newly minted `TestReference` (except for some global steps like `commit`)
- a fully-constructed `TestStep` appended to the `TestCase`

The adder is the *only* place where TestSteps are created and registered.

---

### 2.3 Canonical Adder Sequence (Critical)

For any step that produces an expected holon snapshot (most steps), the adder **must** follow this exact sequence.

#### Canonical Adder Sequence

1. **Derive the fixture-time source snapshot**
  - Extract the source snapshot from the input `TestReference`.
  - Never mutate this snapshot.

2. **Clone the source snapshot into a working holon**
  - This is the *only* holon the adder may mutate.
  - If the source is Deleted, error unless the step explicitly supports Deleted input.

3. **Apply the step’s effects**
  - Apply property changes, relationship edits, lifecycle transitions, etc.
  - This produces the *expected* post-step holon content.

4. **Freeze the expected output snapshot**
  - The working holon produced by applying the step’s effects becomes the ExpectedHolon snapshot and, due to "tight chaining" may become the SourceHolon snapshot in later TestSteps.
  - Therefore, it **should not be mutated after this point.** 
  - If there is _any_ possibility the working holon could be mutated after this point, the adder must clone it and use the clone as the expected snapshot.

5. **Mint the new TestReference**
  - Construct:
    - `SourceHolon`: derived from the input TestReference
    - `ExpectedHolon`: frozen snapshot + expected lifecycle state
  - Mint the TestReference via `FixtureHolons` helpers only.

6. **Register logical holon identity**
  - Decide whether this step:
    - continues the same logical holon, or
    - creates a new logical holon
  - Call the appropriate `FixtureHolons` registration API.

7. **Construct and append the TestStep**
  - Create the concrete TestStep struct containing:
    - the minted TestReference
    - all step-specific parameters
  - Append it to the `TestCase`.

8. **Return the minted TestReference**
  - Return the newly created TestReference to the caller.
  - This returned reference is what TestCase authors use to chain subsequent steps.

> **It is very important that this exact ordering if followed.** Doing the right operations in the wrong order leads to aliasing bugs, broken chaining, and unpredictable results.

---

### 2.4 Deciding Whether a Step Creates a New Logical Holon

The adder author must explicitly decide whether the step yields:

#### Same logical holon (continue existing FixtureHolon)

Examples:
- with_properties
- add_relationship
- remove_relationship
- abandon_staged
- delete_saved
- many “modify in place” lifecycle steps

Rule of thumb:
- If the step conceptually modifies or transitions the same entity, reuse the FixtureHolon.

#### New logical holon (allocate new FixtureHolon)

Examples:
- stage_new_holon
- stage_new_from_clone (when treated as creating a new entity)
- explicit “create new” steps

Rule of thumb:
- If the step creates an independently identifiable entity, allocate a new FixtureHolon.

This decision is enforced through `FixtureHolons`; adders should not manage identity manually.

---

### 2.5 Special Step: Commit Adder

`commit` is special because it does **not** operate on a single source TestReference.

Adder responsibilities for commit:

1. Append a Commit step to the `TestCase`
2. Ask `FixtureHolons` to:
  - iterate over logical holons
  - identify holons in `Staged` state
  - mint new **Saved** head snapshots (new TestReferences)
  - advance each holon’s head snapshot
3. Ensure commit does **not** require TestCase authors to capture new TestReferences

Key rule:

> Commit advances heads internally. TestCase authors keep using the same TestReference handles.

---

## 3. Executor Responsibilities (Execution Phase)

### 3.1 Purpose of an Executor

An executor must:

1. Resolve the correct execution-time source holon
2. Perform the operation
3. Validate actual vs expected outcome
4. Record the execution result for chaining

Executors never mint tokens and never consult `FixtureHolons`.

---

### 3.2 Canonical Executor Sequence (Critical)

Every executor must follow this exact order:

1. **Resolve execution-time source holon**
  - Use harness helper (e.g., `execution_holons.resolve_source_reference`)
  - Provide the step’s `TestReference`

2. **Execute the operation**
  - Perform create / update / stage / delete using real holon APIs
  - Capture the resulting runtime reference (or Deleted)

3. **Validate the outcome**
  - Compare lifecycle state vs `ExpectedHolon.state`
  - If live, compare content vs ExpectedHolon snapshot
  - If deleted, ensure deletion semantics match expectation

4. **Record the result**
  - Record the outcome against the **ExpectedHolon snapshot token**
  - Use harness helper (e.g., `execution_holons.record_resolved`)
  - Do not record against source tokens

This recording step is what enables subsequent steps to resolve correctly.

---

### 3.3 Special Executor: Commit

Commit executor behavior:

- Iterates over staged holons
- Commits them, producing saved IDs
- Records execution results for **each commit-minted TestReference**

This is why the commit adder must mint those TestReferences in advance.

---

## 4. Step Parameters and Expected Outcomes

### 4.1 Step-specific parameters

`TestReference` contains **only** source and expected holon specifications.

All step-specific parameters belong in the `TestStep` struct, for example:
- PropertyMap
- relationship references
- flags and modes

---

### 4.2 Expected test outcome vs expected holon outcome

Some steps assert failure or error conditions.

These expectations:
- are **not** part of TestReference
- belong in the TestStep struct (e.g., `ExpectedStepOutcome`)

This is required because:
- some steps have no source TestReference (commit)
- some steps fail without producing a meaningful holon

---

## 5. Common Footguns (Explicitly Forbidden)

### Adders must not:
- mutate snapshots from input TestReferences
- mint tokens without `FixtureHolons`
- infer commit effects from token history
- append incomplete TestSteps

### Executors must not:
- mint fixture tokens
- consult `FixtureHolons`
- record results against source snapshot tokens
- bypass harness resolution helpers

---

## 6. Summary Invariants

- Every adder produces exactly **one complete TestStep**
- Every TestStep has exactly **one TestReference**
- Adders follow clone → apply → freeze → mint → register → append
- Executors follow resolve → execute → validate → record
- Commit advances heads internally; authors reuse old references

These rules are **foundational**.  
New test steps must follow them to remain compatible with commit semantics, head redirection, and tight chaining.
