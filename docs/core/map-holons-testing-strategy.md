# MAP testing follows two general approaches:
1. Sweetests leverage Rust's [rstest](https://app.capacities.io/5b8fa8cb-93e4-49ef-a28d-a7b25cd445b4/2ac07cf0-6bba-4698-987a-b289fe408e2b) testing framework.
2. Tryorama tests leverages Holochain's [Tryorama](https://app.capacities.io/5b8fa8cb-93e4-49ef-a28d-a7b25cd445b4/3183dcce-255e-411e-b1c5-0d27153c2faf) JavaScript-based testing framework.

## Sweetest Integration Tests

### Test Contexts

The `HolonsContextBehavior` trait provides access to a space manager.

```
pub trait HolonsContextBehavior {
    /// Provides access to the holon space manager for interacting with holons and their relationships.
    fn get_space_manager(&self) -> Rc<&dyn HolonSpaceBehavior>;
}
```

Concrete implementations of that trait provide access to a HolonSpaceManager that has been configured for either _client-side_ or _guest-side_ use. Note that HolonSpaceManager is a holons_core component, so the source code is the same for both client and guest space managers. They differ in the HolonService they have been injected with upon initialization of their context.


The `HolonSpaceBehavior` trait implemented by HolonSpaceManager provides access to a set of services.

```
pub trait HolonSpaceBehavior {
    fn get_cache_access(&self) -> Arc<dyn HolonCacheAccess>;
    fn get_holon_service(&self) -> Arc<dyn HolonServiceApi>;
    fn get_nursery_access(&self) -> Arc<RefCell<dyn NurseryAccess>>;
    fn get_space_holon(&self) -> Option<HolonReference>;
    fn get_staging_behavior_access(&self) -> Arc<RefCell<dyn HolonStagingBehavior>>;
    fn export_staged_holons(&self) -> SerializableHolonPool;
    fn import_staged_holons(&self, staged_holons: SerializableHolonPool);
    fn get_transient_state(&self) -> Rc<RefCell<dyn HolonCollectionApi>>;
}
```

There are three different contexts relevant to sweetests.

#### fixture_context (client-side)

* Test fixtures are responsible for setting up the test steps for a given test case along with the test data (holons and relationships) those steps require. Notice that relationships are expressed via `HolonReferences`. The `fixture_context` allows access to the actually holon they being references by providing access to the services that resolve them: `CacheAccess` (for `SmartReferences`) or `NurseryAccess` (for `StagedReferences`).

* An empty context is initialized by each fixture and goes out of scope when the fixture ends. _Fixture contexts_ are never shipped between client and guest and their `Nursery's` are never _committed_.

#### test_context (client-side)

* Each test case executes within its own client-side context. Test step executors (i.e., the rust functions that implement test steps), use the test_context to stage holons and their relationships (via the NurseryAccess service) and to get persisted holons and their relationships (via the CacheAccess service).

* an **empty context** is initialized by the `rstest_dance_test` function at the beginning of each test case execution and a reference to it (as a `&dyn HolonsContextBehavior` trait object) is passed as a parameter to each test step executor.
  if a test step invokes a _dance_, its `Nursery` is shipped to the guest-side via the `session_state` field on `DanceRequest`.
* when the dance result is returned the `test_context` is restored from `session_state` so that any changes to the `Nursery` that were made by the guest are now reflected back in the client's `Nursery`.
* the `commit_dance` persists any staged holons in the `Nursery`. Once completed successfully, it clears the staged holons and keyed_index from the Nursery, making it available to stage additional holons and relationships.


#### guest_context (guest-side)

* The guest_context is used by dance implementation functions that rely on the space manager and the services it provides.
* When Dancer's dance function is invoked for a new DanceRequest, it initializes the guest_context from the session_state passed via the DanceRequest.
* The dancer passes a reference to the context (as a `&dyn HolonsContextBehavior` trait object) to the DanceFunction it dispatches to handle the dance request.
* DanceFunctions may perform operations that add, remove, update or clear the Nursery.
* The dancer is responsible for including the updated Nursery via the session_state field in the DanceResponse.

### rstest_dance_tests Function

Sweetests are organized around a set of test cases. Since the external API to the MAP guest is organized around dances, all integration testing is driven from the dances crate -- specifically, the `rstest_dance_tests` function defined in the `dances_tests.rs` module.


```
#[rstest]
#[case::simple_undescribed_create_holon_test(simple_create_holon_fixture())]
#[case::simple_add_related_holon_test(simple_add_remove_related_holons_fixture())]

#[tokio::test(flavor = "multi_thread")]
async fn rstest_dance_tests(#[case] input: Result<DancesTestCase, HolonError>)
```

Notice this function is parameterized by `#[case]`. Preceding the function declaration with one or more `#[case]` statements allows selective control over which test cases are invoked in any given test run. For example, the following code will result in the `rstest_dance_tests` function being invoked twice -- once for the `simple_undescribed_create_holon_test` case and once for the `simple_add_related_holon_test` case. Each test case is invoked asynchronously and independently from other test cases.

Each case has an associated _fixture function_ that sets up the test steps and associated data for that test case and returns a `DancesTestCase` object that is passed as an input parameter to the `rstest_dance_tests` function. Every test case follows the same basic flow:
1. _**Initialization**_ -- sets up tracing, a mock conductor, an empty `HolonsContext`, and an empty `test_state`. Note that `test_context` is different from the `fixture_context` used by the fixture and the `guest_context` used by the back-end (guest-side) during dance execution (as described above).
2. _**Test Step Execution**_. Unpack the test case and iterate through the steps for that test case. Matching on the test step allows different `execute_xxx` functions to be dispatched for each kind of test step.

The `test_state` accumulates state as the test case progresses and a mutable reference to it is passed into every test step executor.

```
// from dances/tests/shared_test/test_data_types.rs
pub struct DanceTestState {
    pub session_state: SessionState,
    pub created_holons: BTreeMap<MapString, Holon>,
}
```

The `session_state` field holds the state that is ping-ponged back and forth between client and guest. The `created_holons` map allows holons that have been successfully committed during the execution of this test case to be retrieved via their key in later test steps.

```
// from dances/src/session_state.rs
pub struct SessionState {
    staging_area: StagingArea,
    local_holon_space: Option<HolonReference>,
}

// from dances/src/staging_area.rs
pub struct StagingArea {
    staged_holons: Vec<Holon>,         // Contains all holons staged for commit
    index: BTreeMap<MapString, usize>, // Allows lookup by key to staged holons for which keys are defined
}
```

The `session_state` is included as part of the `DanceRequest` by the `build_xxx_` function. It is part of every dance call and is restored from the `DanceResponse` when a response is received.

```let response: DanceResponse = conductor.call(&_cell.zome("dances"), "dance", valid_request).await;
_test_state.session_state = response.state.clone();
```

## Test Fixtures
Each case has an associated fixture function that sets up the test steps and associated data for that test case and returns a `DancesTestCase` object that is passed as an input parameter to the `rstest_dance_tests` function. The fixture can stage a set of holons and relationships in its `fixture_context`. Such holons can be supplied to the `test_steps` the fixture is setting up in order to supply the data required by that `test_step`.

## Test Data Types

We have defined a set of data structures and protocols designed to make it easier to quickly define test cases.

### DanceTestStep

Each test case is composed of a set of test steps. Test steps are defined independently so that may be reused in different test cases. The `DanceTestStep` enum defines the set of available test steps and the data associated with each test step. Here is an excerpt:

```
pub enum DanceTestStep {
  AbandonStagedChanges(StagedReference, ResponseStatusCode), // Marks a staged Holon as 'abandoned'
    AddRelatedHolons(
        StagedReference,
        RelationshipName,
        Vec<HolonReference>,
        ResponseStatusCode,
        Holon,
    ), // Adds relationship between two Holons
    Commit,      
  
}
```

Each test step generally invokes one or more dances.

### DancesTestCase

Each test case is defined by an instance of DancesTestCase:

```
pub struct DancesTestCase {
    pub name: String,
    pub description: String,
    pub steps: VecDeque<DanceTestStep>,
    pub test_session_state: TestSessionState,
}


pub struct TestSessionState {
    transient_holons: SerializableHolonPool,
}
```

Including `test_session_state` in the `DancesTestCase` allows the TransientHolons created by a fixture to be passed from the `fixture_context` into the `test_context`. As part of its initialization sequence, the `rstest_dance_tests` function initializes its `test_context` from the `test_session_state`. This means the `test_context's` TransientHolonManager will start with its HolonPool in the same state as the `fixture_context's` HolonPool. **_Key Takeaway: any TransientReferences created by the fixture are resolvable within the test_context_**. However, the fixtures Nursery is NOT passed into the test context. This means that StagedReferences created in the fixture are NOT resolvable in the `test_context`. For this reason, _**fixtures should NOT, themselves, stage any holons.**_

Notice that the test case defines a sequential set of steps. `DancesTestCase` offers a set of `add_xxx_step` methods that allow test steps to be added to the test case, where xxx specifies a particular a specific test step. For example, the following method adds a stage_holon_step to test case.

```
 pub fn add_stage_holon_step(&mut self, holon: TransientReference) -> Result<(), HolonError> {
        self.steps.push_back(DanceTestStep::StageHolon(holon));
        Ok(())
    }
```

Notice the holon to be staged is identified via its TransientReference. Since this reference will resolve in the test_context, the test_stage_new_holon function can resolve that reference during test execution.

### Referencing Holons Staged or Saved within a Test Case Execution

Some test cases require the ability to refer to holons staged or saved in earlier test steps. For example, suppose I want to add related holons (either staged or saved) to a holon staged in a prior step. Likewise, in the `stage_new_from_clone` test case we want to test the ability so clone a transient holon, staged holon, and saved holon (to make sure all three possibilities are tested).

The fixture doesn't know what temporary id the test executor will assign for the holons staged during the test, nor does it know what HolonId will be assigned by holochain for holons committed to the DHT during the test. **_So how can it pass references to those holon to subsequent steps it is adding to the test case?_**


### Current Approach: Test References and DanceTestExecutionState

Our current solution was implemented prior to the introduction of the TransientHolonManager. This section describes the current approach and is then followed by a proposed approach.

```
pub struct DanceTestExecutionState<C: ConductorDanceCaller> {
    context: Arc<dyn HolonsContextBehavior>,
    pub dance_call_service: Arc<DanceCallService<C>>,
    pub created_holons: BTreeMap<MapString, Holon>,
}
```

### TestReference

`TestReferences` are created by fixtures. They are used to pass references to holons created in prior test steps to be passed into subsequent test steps. For example, the `simple_stage_new_from_clone_fixture`:

1. Stages several holons into the fixture's Nursery
2. Adds a `stage_new_from_clone_step` to the TestCase that (during execution phase) will stage a new holon that is a clone of one of the previously staged holons.
2. Adds a stageClones the staged holon
3. Phase 2 clones a saved holon, changes some of its\n\
   properties, adds a relationship, commits it and then compares essential content of existing \n\
   holon and cloned holon

```
pub enum TestReference {
    SavedHolon(MapString),
    StagedHolon(StagedReference),
    TransientHolon(TransientReference),
}
```


# Tryorama Tests (TBD)