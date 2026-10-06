# Load Holons — Replacement Use Case

## Goal

The agent selects local source files, reviews their validation status, submits them for loading into the affording HolonSpace, and inspects the outcome within Space Navigator.

## Entry Point

The agent activates **Load Holons** in HolonInspector's action bar while inspecting
a HolonSpace that affords `LoadHolons.DanceType`. That HolonSpace remains the
semantic owner and explicit invocation target throughout request preparation,
submission, and outcome inspection. Space Navigator supplies the enclosing
exploration context.

Load Holons is the first enabled holon-level action. It establishes the reusable
initiation pattern: activate the bound holon's afforded Dance, prepare its request
through an applicable interaction, submit explicitly, and present execution
feedback and results with the originating holon and Dance retained as context.
The existing disabled actions reflect incremental implementation readiness;
unsupported actions remain disabled until their activation paths are available.

## Main Flow

| Step | Agent action | System response |
|---|---|---|
| 1 | Activates **Load Holons**. | Presents source choices. Initially, **Upload from computer** is the supported choice. |
| 2 | Chooses **Upload from computer**. | Opens the native file-selection dialog. The intended experience supports selecting files or directories, including multiple selections, without first choosing a selection mode. |
| 3 | Selects files and/or directories and confirms. | Includes explicitly selected files and recursively discovers files beneath selected directories. Validates the resulting input files for JSON syntax and JSON Schema conformance before presenting the review list. |
| 4 | Reviews the selected files. | Displays a scrollable list with each file’s absolute path and a valid/invalid indicator. Provides selection checkboxes and **Remove selected**, **Submit selected**, and **Cancel** actions. If all files are valid, all are initially selected and **Submit selected** is enabled. |
| 5 | Adjusts the selection or removes unwanted files. | Updates the list and action availability. **Remove selected** removes files from this load request; it does not delete them from the computer. **Submit selected** requires at least one selected file and no invalid files remaining anywhere in the review list. |
| 6 | Activates **Submit selected**. | Constructs the canonical `HolonLoadSet` request from the selected files and invokes `LoadHolons` through the explicitly bound affording HolonSpace. Displays loading feedback in the action interaction within the enclosing experience. |
| 7 | Waits for completion. | Displays an elapsed-time counter and a general **Loading…** indication. Shows more specific status only when the client actually knows that a transition has occurred. |
| 8 | Reviews the outcome. | Presents full success, partial success, or failure using the outcome flows below. |

## Input-Validation Errors

| Step | Agent action | System response |
|---|---|---|
| V1 | Confirms a selection containing invalid files. | Displays the complete review list, marks invalid files, and initially selects only the invalid files. **Remove selected** is enabled; **Submit selected** is disabled. |
| V2 | Reviews the invalid entries. | Shows available validation diagnostics associated with each file. Diagnostic detail depends on what the validator provides. |
| V3 | Removes the selected invalid files. | Removes those entries from the request and updates action availability. Once no invalid files remain, the agent can select the desired valid files and submit them. |

Unchecking an invalid file is insufficient to enable submission: it must be removed from the review list.

## Full Success

| Step | Agent action | System response |
|---|---|---|
| S1 | Reviews the completed load. | Displays **Load successful** and offers the collection of newly committed holons through a Collection Visualizer. Source-file details do not need to dominate this outcome. |
| S2 | Reviews the committed-holon collection. | Constructs SmartReferences rooted in the committed Holon IDs, using the retained staged holons to identify this load’s committed members. Obtains each committed holon’s key from committed state for collection display. |
| S3 | Selects a committed holon for inspection. | Retrieves it through normal MAP-backed inspection and presents its properties and relationships. |

The Nursery is **not cleared on commit**, whether the outcome is successful or otherwise. Its retained staged property maps must not be presented as retrieved committed properties. The result references initially carry the committed identity and retrieved key; other properties are obtained when needed.

## Partial Success

| Step | Agent action | System response |
|---|---|---|
| P1 | Reviews the completed load. | Displays **Load partially successful**, with available outcome counts, and gives primary attention to the errors. |
| P2 | Reviews the errors. | Presents a flat collection of error holons through a Collection Visualizer. Columns include **key**, **error message**, **source file**, and **source location**, where available. Default ordering is by source file, then location within the file. |
| P3 | Chooses to inspect successful results. | Offers the committed-holon collection using the same identity, key-retrieval, and inspection behavior as the full-success flow. |

The initial error experience reports the problem and its location. Displaying the offending source fragment and repairing staged holons are deferred.

## Failure

| Step | Agent action | System response |
|---|---|---|
| F1 | Reviews an unsuccessful load. | Displays **Load failed** and presents available error holons through the same flat error collection. |
| F2 | Reviews the failure details. | Shows source file and location where known. Reports parser errors even when parsing failed before any staged holon could be identified. |

A load that fails during parsing does not proceed to commit. Error presentation must therefore work without assuming that every error has an associated staged holon.

## Cancellation

The agent may cancel the native picker or the review step without submitting a load.

Cancellation after submission is outside the initial scope.

## Deferred Enhancements

- Additional source choices.
- Display of offending source fragments.
- Interactive repair of staged holons.
- File-grouped error presentation.
- Guest-emitted progress events and subscription support.
- Cancellation after submission.

## Implementation Detail to Verify

Verify whether the host’s native picker supports mixed file/directory selection and multiple directories in a single dialog. That is the intended experience described here.
