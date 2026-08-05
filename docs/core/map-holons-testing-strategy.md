# MAP Holons Testing Strategy

MAP testing uses two test runners:

1. **Sweettests** — Rust integration tests in `tests/sweetests/`, running against an in-process
   Holochain `SweetConductor`. Some of them use [rstest](https://docs.rs/rstest/) parameterization.
2. **Tryorama tests** — Holochain's JavaScript-based
   [Tryorama](https://github.com/holochain/tryorama) framework. Scaffolded under `tests/tryorama/`
   but not yet in use; see [Tryorama Tests](#tryorama-tests) below.

---

## Choosing Where a Test Belongs

Sweettests are written in **two distinct styles**, and picking the wrong one is the most common
authoring mistake. The deciding question is *what layer the assertion is about*, not what feature
is being tested.

| If the assertion is about… | Write a… | Specified in |
|---|---|---|
| Staging, chaining, commit lifecycle, relationship graphs, saved-content equality — anything expressible as a sequence of client operations | **Dance test** (fixture + steps) | [Dance Test Framework](testing/dance-test-spec.md) |
| Which substrate action was authored, whether Integrity fired, the exact consensus-visible rejection message, what a conductor will dispatch | **Conductor test** (direct zome call) | [Conductor Test Framework](testing/conductor-test-spec.md) |

Reaching a guest-side outcome by adding a new `DanceTestStep` is the wrong answer. The dance layer
observes results as a client observes them; guest execution and Integrity validation are not visible
from there.

Below the sweettest layer, prefer **unit tests** in the owning crate for logic that needs no
conductor at all — lineage rules, comparators, encoders. A conductor test should assert that such
logic is *wired* to real substrate behavior, not re-test the logic itself.

---

## Sweettest Contexts

Transaction-scoped execution in MAP flows through `TransactionContext`, obtained from a
`HolonSpaceManager` via its `TransactionManager`. `HolonSpaceManager` is a `holons_core` component,
so the same code backs both client-side and guest-side use; the contexts differ in the services
injected at initialization.

Three contexts are relevant to dance tests.

### fixture_context (client-side)

Created by `init_fixture_context()` and held as `Arc<TransactionContext>` in `TestCaseInit`.

- Fixtures set up the test steps for a test case along with the test data those steps require.
  The fixture context provides the services that resolve the references embedded in that data.
- It is initialized with a `ClientHolonService` and **no** `DanceInitiator` — fixtures cannot
  initiate dances. A default transaction is opened for the fixture's space manager.
- A fresh, empty context is created per fixture and goes out of scope when the fixture ends.
  Fixture contexts are never shipped between client and guest, and their staged holons are never
  committed.

### test runtime and test context (client-side)

Created by `init_test_runtime()`, which builds a `HolonSpaceManager` **with** a `DanceInitiator`
(a `TrustChannel` over the sweettest mock conductor), wraps it in a `RuntimeSession` and `Runtime`,
and begins the first transaction through the real command path —
`Runtime::execute_command(SpaceCommand::BeginTransaction)`.

- Each test case executes within its own runtime. Step executors operate through that runtime
  rather than against a context they construct themselves.
- Transient holons created by the fixture are imported into the initial transaction context, so
  references minted during the Fixture Phase resolve during execution.
- When a step invokes a dance, session state is shipped to the guest and the client-side state is
  restored from the response, so guest-side changes are reflected back.

### guest_context (guest-side)

- The guest context is used by dance implementations that rely on the space manager and its
  services.
- `dance_adapter` receives a `DanceRequestEnvelope` carrying the request and a `SessionStateWire`,
  validates the request at ingress, and hydrates the guest context from that session state.
- The adapter dispatches to the dance function, which may add, remove, update, or clear staged
  state.
- The adapter returns a `DanceResponseEnvelope` carrying the updated session state.

---

## The `rstest_dance_tests` Function

Dance tests are organized around a set of test cases driven by the `rstest_dance_tests` function in
`tests/sweetests/tests/dance_tests.rs`. Conductor tests do **not** go through this function; they
are independent `#[tokio::test]` functions.

```rust
#[rstest]
#[case::simple_undescribed_create_holon_test(simple_create_holon_fixture())]
#[case::simple_add_related_holon_test(simple_add_remove_related_holons_fixture())]
// ... one #[case] per registered fixture

#[tokio::test(flavor = "multi_thread")]
async fn rstest_dance_tests(#[case] input: Result<DancesTestCase, HolonError>)
```

The function is parameterized by `#[case]`, giving selective control over which test cases run in a
given invocation. Each case is invoked asynchronously and independently.

Each case has an associated **fixture function** that sets up the steps and data for that case and
returns a `DancesTestCase`, which is passed in as the input parameter. Every test case follows the
same flow:

1. **Initialization** — sets up tracing, the mock conductor, the test runtime, and the first
   transaction. Note that this context differs from the `fixture_context` used by the fixture and
   the `guest_context` used guest-side during dance execution.
2. **Test Step Execution** — unpack the test case and iterate its steps, matching on the step to
   dispatch the appropriate executor.

Execution-time state is tracked by `ExecutionHolons`, which records the runtime outcome of each
step against its expected-snapshot token so later steps can resolve correctly. See the
[Test Harness Design Spec](testing/test-harness-design-spec.md) for its contract.

---

## Test Fixtures

A fixture function sets up the steps and data for one test case and returns a `DancesTestCase`.
Fixtures may create **transient** holons in the `fixture_context` and supply them to the steps
being added.

Fixtures must **not** stage holons themselves. Transient holons created by a fixture are carried
into the test runtime through `TestSessionState`, so `TransientReference`s minted in the fixture
resolve at execution time. The fixture's staged holons are **not** carried over, so
`StagedReference`s minted in a fixture would not resolve.

---

## Test Data Types

These structures exist to make test cases quick to define. Full semantics are specified in the
[Dance Test Framework](testing/dance-test-spec.md) and the
[Test Harness Design Spec](testing/test-harness-design-spec.md); what follows is orientation only.

### DanceTestStep

Each test case is composed of a sequence of steps. Steps are defined independently so they can be
reused across test cases. `DanceTestStep` is an enum whose variants use **named fields**, so the
contract of each step is readable at the call site. An excerpt:

```rust
pub enum DanceTestStep {
    AbandonStagedChanges {
        step_token: TestReference,
        expected_error: Option<HolonErrorKind>,
        description: String,
    },
    AddRelatedHolons {
        step_token: TestReference,
        relationship_name: RelationshipName,
        holons_to_add: Vec<TestReference>,
        expected_error: Option<HolonErrorKind>,
        description: String,
    },
    Commit {
        saved_tokens: Vec<TestReference>,
        expected_status: ExpectedCommitStatus,
        expected_error: Option<HolonErrorKind>,
        description: String,
    },
    // ...
}
```

Not every variant carries a `TestReference`. Global and assertion steps — `EnsureDatabaseCount`,
`MatchSavedContent`, `LoadCoreSchema`, the `Verify*` family — have no source holon.

### DancesTestCase

```rust
pub struct DancesTestCase {
    pub name: String,
    pub description: String,
    pub steps: Vec<DanceTestStep>,
    pub test_session_state: TestSessionState,
    pub(crate) is_finalized: bool,
}

pub struct TestSessionState {
    transient_holons: SerializableHolonPool,
    fixture_head_index: FixtureHeadIndex,
}
```

`test_session_state` carries fixture-time state into the execution phase: the transient holon pool
(so fixture-minted `TransientReference`s resolve) and the fixture head index (so tokens map to the
correct logical holon heads).

`is_finalized` enforces that `finalize()` is called exactly once, after all steps are added and
before the case is returned. Steps cannot be appended afterward.

A test case is constructed through `TestCaseInit`, which creates the case, the fixture context,
`FixtureHolons`, and `FixtureBindings` together so that authoring cannot begin from a partially
initialized state.

### Referencing Holons Across Steps

Test cases routinely need to refer to holons staged or saved in earlier steps — adding related
holons to a holon staged in a prior step, or cloning a transient, staged, and saved holon in turn.

The fixture cannot know the temporary id the executor will assign to a holon staged during
execution, nor the `HolonId` Holochain will assign on commit. **So how does it pass references to
those holons into subsequent steps?**

The answer is `TestReference`: an **opaque, immutable token** minted by adders during the Fixture
Phase and interpreted by the harness at execution time.

```rust
pub struct TestReference {
    source: SourceSnapshot,     // what the executor should operate on
    expected: ExpectedSnapshot, // what the step should produce
}
```

Authors pass a token into an adder and receive a new one back; they never inspect or construct one.
Logical holon identity across steps is tracked separately by `FixtureHolons`, which is what allows
an older token to remain safe to use after a commit.

The full contract — chaining, head selection, commit semantics, and execution-time resolution — is
specified in the [Test Harness Design Spec](testing/test-harness-design-spec.md).

---

## Tryorama Tests

`tests/tryorama/` currently contains only project scaffolding (`package.json`, `tsconfig.json`,
`vitest.config.ts`). No Tryorama test cases have been written yet, and no scenario coverage should
be assumed from this directory. **(TBD)**
