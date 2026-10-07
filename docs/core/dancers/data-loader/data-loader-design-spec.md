# Load Holons Design Specification

## 1. Purpose and Scope

This specification defines the DAHN-based replacement for the legacy Load Holons experience.

The replacement preserves the canonical `LoadHolons` Dance and existing loader semantics while moving initiation, preparation, execution feedback, and result review into selected DAHN Visualizers.

The initial implementation provides:

- Source selection and validation.
- Explicit submission after source review.
- A dedicated loader TransactionContext.
- Execution feedback and authoritative outcome reporting.
- A flat diagnostic collection.
- Review of committed holons through a separate TransactionContext.
- Explicit disposal when the load presentation is dismissed.

The initial implementation does not introduce:

- Cancellation of an executing load.
- Undo of persisted operations or compensating updates.
- Reconnection to transactions whose presentation has been destroyed.
- Interactive repair of staged holons.
- Display of offending source fragments.
- Guest-emitted progress events and subscriptions.
- Transfer of result inspectors into independently owned navigation contexts.

## 2. Architectural Placement

### 2.1 Affording Subject and Initiation Surface

The originating HolonSpace is the affording subject of `LoadHolons`.

HolonInspector discovers the Dance through the bound HolonSpace’s effective descriptor and projects it into its Action Bar.

Load Holons is initiated through that HolonInspector action presentation. It is not a separately defined Canvas-level Dance or a replacement semantic loading protocol.

Host file selection supplies input to the canonical Dance. It does not directly mutate the HolonSpace.

### 2.2 ActionVisualizer Delegation

HolonInspector requests an applicable ActionVisualizer through the normal Selector contract.

The selected Load Holons ActionVisualizer owns presentation of:

- Source choices.
- Source selection.
- Validation and source review.
- Submission controls.
- Execution feedback.
- Outcome summaries.
- Diagnostics and committed-result review.

The generic Action Bar supplies the action affordance, bound subject, slot, and presentation context. It contains no loader-specific file selection, JSON validation, or outcome interpretation.

The runtime supplies authoritative preparation and execution services. The Visualizer presents their state and submits agent intent.

Selection and realization failures are reported explicitly. No component substitutes a hard-coded Visualizer implementation.

## 3. Activation Contract and Ownership

### 3.1 Bound Activation Context

A load activation retains:

| Context | Meaning |
|---|---|
| Originating HolonSpace | The fixed target of preparation and invocation. |
| Selected Dance identity | The canonical Dance selected for this activation. |
| Loader TransactionContext | The context containing loader-related work. |
| Originating HolonInspector occurrence | The specific presentation occurrence that initiated the load. |
| ActionVisualizer occurrence | The presentation owner of the load interaction. |

Changing navigation focus or the active Space does not retarget an existing load.

These bindings describe runtime contracts. They do not independently require new HolonTypes.

### 3.2 Presentation and Runtime Ownership

The Load Holons ActionVisualizer owns the lifetime of the dedicated loader transaction.

The runtime manages the TransactionContext and enforces its operations, including:

- Preparation state.
- Request retention.
- Submission readiness.
- Duplicate-submission prevention.
- Dance invocation.
- Execution state.
- Response, staged holon, and finding retention.
- Explicit disposal.

The ActionVisualizer does not maintain a parallel authoritative copy of holonic state.

The presentation also owns the separate committed-result review TransactionContext described in Section 9.

### 3.3 Readiness

Readiness is distinct from descriptor-defined semantic availability.

| State | Meaning |
|---|---|
| Semantic availability | The effective descriptor establishes that the HolonSpace affords the Dance. |
| Activation readiness | The runtime can establish the required execution context and provide the capabilities needed to begin preparation. |
| Submission readiness | The prepared request satisfies submission requirements and has not already been submitted. |

A runtime limitation does not rewrite the descriptor-defined affordance.

The ActionVisualizer reports readiness and blocking reasons. The runtime enforces readiness when operations are requested.

## 4. Transaction Lifecycle

### 4.1 Creation

Activation begins a dedicated loader transaction before source selection.

Preparation, request construction, invocation, staged holons, diagnostics, and response review all remain associated with this loader TransactionContext.

The transaction remains bound to the originating HolonSpace.

### 4.2 Lifecycle States

The following states describe the interaction lifecycle; they do not replace authoritative loader status values.

| Phase | Behavior |
|---|---|
| Preparing | Sources may be selected, validated, reviewed, and removed. |
| Ready for submission | The request satisfies submission requirements. |
| Executing | The submitted Dance is running; duplicate submission and dismissal are blocked. |
| Reviewing | Execution has ended and available outcomes can be inspected. |
| Disposed | Presentation-owned contexts and retained transient state have been released. |

Preparation failures retain available diagnostics and permit correction or cancellation.

Failures that end invocation without a usable response enter review with an explicit execution failure. They do not acquire an inferred loader status.

### 4.3 Cancellation and Dismissal

| Phase | Cancel or dismiss behavior |
|---|---|
| Before submission | Abandon preparation and dispose of the dedicated transaction and prepared request. |
| During execution | Prevent dismissal and destruction of the owning presentation. |
| After execution ends | Close result inspectors and dispose of retained loader and review state. |

An optional confirmation may explain that dismissal abandons preparation or releases retained results.

Compression, off-viewport placement, and moving navigation focus elsewhere do not constitute dismissal.

Any operation that would destroy the load presentation during execution—including closing an ancestor or replacing its owning inspector—must respect the same dismissal guard.

Disposal does not undo persisted holons.

### 4.4 Execution Completion and Transaction Closure

Execution completion and transaction closure are distinct.

The existing transaction policy closes only a `Complete` load. `Incomplete`, `Rejected`, and `Skipped` do not acquire successful closure merely because execution has ended.

All terminal outcomes remain reviewable until explicit dismissal and disposal.

Commit does not clear the Nursery. Retained staged state remains available for diagnostics and committed-member identification.

## 5. Source Preparation and Review

### 5.1 Source Selection

The initial source choice is **Upload from computer**.

The intended native selection experience supports:

- Explicit file selection.
- Directory selection with recursive discovery.
- Multiple selections.
- Selection without requiring the agent to choose file mode or directory mode in advance.

The supported desktop platforms are **macOS and Linux**. Native source ingress uses
RFD 0.17.2: macOS exposes mixed file/directory selection; the Linux XDG Desktop
Portal backend exposes separate file and directory modes. Both expose multiple
selection. These are inspected API capabilities, not native smoke-test results.
Linux separate-choice selection is an interim limitation; the intended mode-free
mixed selection remains a follow-on requirement. See
[native source verification](data-loader-source-verification.md) for evidence and
remaining verification.

Source discovery follows these policies:

- Recursively include regular files with case-insensitive `.json` extensions,
  including hidden entries; ignore other regular files.
- Sort by normalized absolute path and deduplicate repeated/overlapping paths.
  Preserve distinct hard-link paths. Source identity is the normalized absolute
  path and stays stable through review ordering/removal; content is a retained
  UTF-8 snapshot. Identity is not a persistent filesystem identifier across renames.
- Remove redundant current-directory components; reject relative paths and parent
  traversal. Do not manufacture absolute paths from browser names.
- Skip symbolic links, including selected paths beneath a symbolic-link ancestor,
  and report the exclusion. Do not traverse cycles or special files.
- Retain readable sources alongside path-specific discovery/read issues. Invalid
  UTF-8 content is a read failure; JSON validation belongs to the review step.
  Paths that cannot be represented losslessly as UTF-8 are reported, not loaded.
- Distinguish dismissed selection, confirmed empty discovery, and discovery/read
  failures. RFD's optional selection result cannot distinguish every backend
  failure from dismissal; this backend limitation must remain explicit.
- Map the retained path to `FileData.filename` and retained content to
  `raw_contents`. Selection does not prepare or submit a transaction. Preparation
  remains an explicit call using the existing preparation-only API.


### 5.2 Validation and Review

After selection and discovery, the system performs JSON syntax and JSON Schema validation before presenting the review list.

The review surface contains:

- A scrollable file list.
- Absolute source paths.
- Valid or invalid indicators.
- Available validation diagnostics.
- Selection checkboxes.
- Add Files, Remove selected, Submit selected, and Cancel actions.
- A Select All checkbox with checked, unchecked, and indeterminate states.

If every file is valid, all files are initially selected.

If invalid files exist, only invalid files are initially selected, making removal the immediate bulk action.

Removing a file changes the prepared request; it does not delete the source file.

Add Files appends newly discovered sources through the native source adapter and
validates their retained contents without resetting existing selections or
snapshots. Existing normalized source paths are deduplicated: adding an already
reviewed file preserves its original snapshot. To refresh it, remove the old
entry and add the file again. Distinct paths with the same basename remain
separate. Canceling the additional picker leaves the current review unchanged.
Existing selections survive additions; the all-valid/invalid-first selection
rule applies only to newly added entries. Acquisition and validation do not
submit the request, and submission is unavailable while either is pending.
Stale asynchronous completions cannot restore removed entries or mutate a
submitted or disposed review.

Select All applies to all current selectable review entries, including invalid
and discovery-failure entries so they can be removed together. Activating an
unchecked or indeterminate checkbox selects all; activating a checked checkbox
clears all. It is disabled for empty or terminal reviews and supports keyboard
operation. Deselecting an invalid entry never bypasses the submission gate.


Discovery failures participate in review even when no content snapshot was produced.
Unreadable files or directories and invalid paths appear as selectable, removable
blocking error entries. They are initially selected with other invalid entries.
Unchecking them does not permit submission; removal acknowledges excluding that
source from the request and does not delete anything on disk. Intentionally
excluded symlinks and special files appear as non-blocking notices. Non-JSON
regular files are omitted by discovery's JSON-only filter.

Schema acquisition, parsing, or compilation failure blocks the entire interaction;
removing individual entries cannot bypass it. Validation completion is associated
with the current source revision. Replaced/removed sources, cancellation, and
disposal must not receive stale validation updates. Review hands off only selected
validated snapshots, retaining their exact paths and strings. The enclosing action
owns transaction preparation, invocation, and authoritative duplicate prevention.

### 5.3 Submission Requirements

Submission requires:

- At least one selected file.
- No invalid files remaining anywhere in the review list.
- No prior submission of this load interaction.

Unchecking an invalid file does not satisfy the validation requirement. It must be removed from the list.

Explicit submission first retains a typed LoadRequest and its exact source snapshots,
then prepares the canonical `HolonLoadSet` execution payload and invokes `LoadHolons`
through the originating HolonSpace only after preparation succeeds.

The runtime accepts only one submission transition. Disabled controls provide feedback but are not the sole duplicate-prevention mechanism.

## 6. Execution Feedback

During execution, the ActionVisualizer displays a general loading indication and elapsed time.

More specific status is shown only for transitions actually known to the client. Elapsed time must not imply measured completion percentage or knowledge of guest-side stages.

Intermediate guest signals, event declarations, and subscription infrastructure are deferred.

Updates and outcomes remain associated with the bound load presentation, regardless of changes to active navigation.

## 7. Authoritative Outcomes and Counts

### 7.1 Outcome Mapping

| Authoritative status | Primary feedback | Initial result view |
|---|---|---|
| `Complete` | Load complete | Committed Holons |
| `Incomplete`, with some persisted holons | Load incomplete — some holons were saved | Diagnostics; committed results also available |
| `Incomplete`, with no persisted holons | Load incomplete — no holons were saved | Diagnostics |
| `Rejected` | Load rejected | Validation diagnostics |
| `Skipped`, empty input without reported problems | Nothing to load | Empty-state explanation |
| `Skipped`, with operational problems | Load skipped | Diagnostics |

Diagnostic views remain available when diagnostics exist, including on `Complete`.

Semantic rejection must expose validation findings even when `ErrorCount` is zero.

Persistence quantities must come from authoritative evidence. Missing information must not be interpreted as proof that no holons persisted.

### 7.2 Missing or Unreadable Responses

Preparation or invocation failure without a usable response is presented as **Load could not be completed**, with available diagnostics.

If response fields cannot be read:

- Identify the response-reading failure.
- Present any fields that can be read reliably.
- Mark unavailable information explicitly.
- Do not infer an authoritative status.
- Do not claim that nothing persisted.

A result-presentation failure does not change the underlying load outcome.

### 7.3 Counts

Counts are displayed independently using their authoritative response-contract definitions.

| Presentation label | Intended meaning, subject to the response contract |
|---|---|
| Staged | Candidates assembled in the Nursery. |
| Attempted | Candidates for which persistence was attempted. |
| Committed | Candidates confirmed persisted by this submission. |
| No action required | Candidates classified as `NoAction`. |

Counts must not be assumed to form a partition.

In particular:

- Do not derive a failed count by subtracting committed from staged.
- Do not describe `NoAction` candidates as newly committed solely because they required no action.
- Display unavailable counts as unavailable, not zero.
- Make the outcome and committed count prominent; place supporting counts in secondary detail.

Committed collection membership follows the Saved-state evidence defined in Section 9, rather than arithmetic over these counts.

## 8. Result Composition and Diagnostics

### 8.1 Two Collection Slots

The Load Holons ActionVisualizer declares two distinct Collection slots:

| Slot | Subject and context |
|---|---|
| Diagnostics | Diagnostic projections constructed from the loader TransactionContext. |
| Committed Holons | SmartReferences bound to a separate review TransactionContext. |

Each slot delegates to an applicable Collection Visualizer through normal selection.

HolonInspector hosts the action experience and does not acquire loader-specific result slots.

The two slots may appear as tabs sharing a physical region. Each retains independent selection, ordering, and view state. Outcome mapping determines the initial view.

Each slot boundary supplies its typed collection subject, originating load context, appropriate TransactionContext, and presentation context. Member activation delegates to the owning action presentation, which opens inspection in the context appropriate to that slot.

### 8.2 Retained Load Request and Diagnostic Collection

A typed transient `LoadRequest` records one submitted source snapshot before parsing
begins. It belongs to the dedicated loader TransactionContext and is never staged
or committed as imported content. Its `SubmittedSources` relationship leads to a
typed source set whose `Sources` preserve each filename and exact original content.
These are the reviewed strings supplied for preparation, not later filesystem reads.

Preparation success attaches the actual `HolonLoadSet` through `PreparedLoadSet`.
At the runtime preparation boundary, its transient protocol objects receive
`DescribedBy` links to canonical Core Schema definitions: HolonLoadSet,
HolonLoaderBundle, LoaderHolon, LoaderRelationshipReference, and
LoaderHolonReference. These links describe the loader objects for ordinary
inspection; imported domain types remain relationship-reference data for mapping.
No new descriptor definitions are created. Low-level schema-bootstrap preparation
remains independent of installed Core descriptors.
The LoadHolons Dance continues to accept that prepared execution payload. The
retained request is the inspectable record of the submission attempt; it does not
make partially parsed input executable. Preparation failure leaves the prepared
payload absent and attaches typed diagnostics to the retained request.

When no response exists, the ordinary Path Inspector is rooted at the retained
request. This covers preparation failures and invocation failures. Its properties
report the observed request phase and available failure message. Its Diagnostics
collection preserves supplied error evidence without inventing commit status,
saved counts, a response, or committed membership. A separate diagnostic-report
root is unnecessary.

When an actual response exists, it remains the result Path Inspector root. Its
`LoadRequest` relationship navigates to the retained submission attempt, whose
`LoadResponse` points to that actual response. The links retain bound handles in
the same loader context; they do not serialize or rebind transient evidence.
The invocation carries the optional retained request through its `LoadRequest`
relationship, separately from its canonical `Request` execution payload. The
Commands runtime attaches both navigation links and records Responded inside the
already admitted invocation, before returning the response. Client writes remain
closed after submission, including rejected outcomes; presentation must not try
to attach links or update request status after the response returns. Descriptors
needed for failure evidence are resolved before execution can close the saved
namespace. A runtime invocation failure records typed diagnostics and structured
SourceError evidence in that same admitted operation. The client only reads these
retained diagnostics. If transport fails before execution or loses the returned
result, the client displays the observed failure and retained request without
claiming runtime diagnostics or a terminal request phase that it cannot verify.

LoadRequest occupies a standard Node Visualizer Slot and selects the ordinary
HolonInspector through normal descriptor applicability, both when reached from
a response and when it roots inspection before a response exists. The loader
supplies typed request and diagnostic data; it does not replace the request
PropertyMap, actions, relationship controls, or collection presentation. Request navigation exposes its sources and
prepared payload through ordinary relationships.
The standard HolonInspector owns request PropertyMap allocation and intrinsic
content sizing.
Request relationship collection tabs use population discovery: verified empty
Diagnostics are hidden, populated collections show known counts, and failed
reads retain explicit retry feedback rather than appearing empty.

Request phase is observational: Preparing, Prepared, Invoking, PreparationFailed,
InvocationFailed, or Responded. InvocationFailed records a runtime-observed failure;
it makes no claim about persistence. A transport failure can leave the retained
phase at Invoking when no terminal runtime update is observable. Preparation retry retains source
review and selections, disposes the previous path after pending reads drain, and
creates a new request for the next submitted snapshot. Invocation failure retains
the submitted source review for inspection but does not reopen submission admission
or automatically retry a possibly executed load.


The load response retains the original Commit response through `LoadCommitResponse`
when Commit was attempted. Its `RejectedHolons` retain their structured staged
findings; its `HasValidationFinding` carriers retain findings without a staged
subject. These remain separate destinations, not duplicate copies of the same
findings. Public SDK reads preserve finding kind, rule identity/code, severity,
structured subject, optional descriptor identity, and message. Missing or
inconsistent diagnostic evidence is a read error, not an empty successful report.

`HasValidationSource` carries input provenance linked by `ValidationSourceSubject`
to the exact staged reference produced by the mapper. It preserves filename,
loader key, and byte offset when supplied; it does not infer line/column positions
or associate unstaged subjects by matching display keys. Source carriers and Commit
carriers remain owned by the loader transaction and expire with its disposal.

Diagnostics form one homogeneous collection of typed transient
`LoadDiagnostic.Projection` holons in the loader context. Each row activates its
actual diagnostic handle as an ordinary Node occurrence. Operational errors,
staged findings, unattached findings, parser issues, and no-response invocation
failures preserve their categories and supplied structure. Scalar evidence is
stored as described properties; nested error values use typed navigable evidence
holons preserving object fields, array indices, scalar kinds, empty containers,
and null. An opaque JSON string is not the diagnostic representation.

`DiagnosticEvidence` links the actual original carrier when one exists.
`DiagnosticSubject` links only a supplied affected-subject handle. Neither is
inferred from filenames, keys, or error-carrier identity. These presentation
holons remain transient and do not become imported content.

Collection rendering uses action-owned typed value columns and stable row
identities. The projection element type is a selection witness, not the displayed
membership. Diagnostic activation, evidence traversal, and affected-subject
traversal retain loader-bound handles. Saved committed members remain bound to
committed review. Visualizer materialization uses an independently open
presentation context bound to the captured Space, even after Complete closes the
loader and when committed review cannot initialize. Read-only selection uses the
selected subject's owning context.

Dismissal first cancels navigation, discovery, and collection activation. It drains
loader-owned descendant work before releasing the presentation contexts that work
may still use, then drains review/presentation work and releases those contexts.
Retained loader evidence is released only after all presentation reads and
materialization have finished. Preparation retry follows the same path-disposal
ordering while keeping the source review and loader context alive.


Sources include:

- Operational loader errors.
- Staged semantic validation findings.
- Unattached validation findings.
- Parser diagnostics.

The minimum projection contains:

| Field | Meaning |
|---|---|
| Diagnostic identity | Stable identity within the retained load review. |
| Category | The diagnostic’s original category. |
| Message | The reported explanation. |
| Subject reference, when available | A StagedReference belonging to the loader context. |
| Subject key, when available | A display identifier for the affected subject. |
| Source identity and path, when available | The originating input source. |
| Source location, when available | Location evidence in its reported representation. |
| Load provenance | Originating loader transaction, HolonSpace, and Dance. |

For partial commits, diagnostic subjects may include Saved holons accessed through their StagedReferences.

Parser diagnostics do not require a staged subject or response holon. Their transient presentation holons preserve the available parser evidence in the owned loader/preparation context; their table projections are derived from that evidence.

Preparation carries parser failures through the existing `LoaderParsingError`
category as a structured payload with a readable summary and individual issues.
Each issue retains filename, original category, message, optional underlying error,
and optional original-file location. Decoder coordinates use a one-based line and
UTF-8 byte column (column zero can occur at early end-of-input); slice coordinates
are translated against the retained original contents. Structural rules without
location evidence leave location absent. Public SDK `readParserDiagnostics(error)`
projects this evidence without requiring wire imports or parsing summary text.
Any failed preparation, including mixed valid/invalid input, returns no usable
prepared execution payload and does not invoke loading or Commit. The retained
LoadRequest remains available for diagnostic and source inspection. Partial transient preparation state
remains owned by the dedicated transaction until disposal.


### 8.3 Display and Ordering

Default diagnostic ordering compares source path, coordinate representation, then
numeric coordinates. Within a source, byte offsets precede line/UTF-8-byte-column
coordinates; missing locations follow both. Missing source paths sort last. Byte
offsets and each line/column component compare numerically; ties preserve producer
order. This deterministic representation order does not claim positional equivalence.
The producer supplies a stable row-ID permutation and readable default-order label;
explicit user column sorting overrides it without changing membership or identities.

Location comparisons must respect the reported coordinate representation. Missing coordinates must not be invented to create a sort key.

Missing display values are shown as **Not available**.

A missing subject key does not prevent inspection when a subject reference exists.

`StartUtf8ByteOffset` is displayed as **UTF-8 byte offset: N**. It must not be relabeled as a line or column without an actual conversion.

### 8.4 Empty States and Presentation Failures

A result tab with a confirmed zero count is hidden. If both result collections are empty, the root retains its summary and relationship rail with an explicit no-results explanation. Unknown counts and read failures remain visible and must not be treated as zero.

Collection Visualizer selection and realization failures receive explicit presentation errors. They do not trigger a hard-coded Table fallback or alter authoritative loader status.

Diagnostic inspectors depend on the presentation context and, where they reference retained loader evidence, the loader TransactionContext. They close when the load presentation is dismissed.

## 9. Committed-Holons Review

### 9.1 Membership Evidence

The committing transaction’s Nursery is the source of committed-member identities.

The runtime:

1. Iterates the Nursery’s StagedReferences.
2. Calls `ReadableHolon::holon_id()` on each staged holon.
3. Includes only members for which that method returns a HolonId.

The method returns a HolonId only when the staged holon is in Saved state, indicating that it has been committed.

This rule applies to both complete and partial outcomes. Neither the presence of a staged reference nor aggregate counts independently establish committed membership.

### 9.2 Separate Review Context

The ActionVisualizer obtains a separate review TransactionContext bound to the originating HolonSpace.

SmartReferences are constructed from the Saved members’ HolonIds in that review context and assembled into the committed-result HolonCollection.

The loader context remains the authority for staged diagnostics. The review context supplies committed-state inspection.

The public SDK entry point is `MapTransaction.openCommittedReview()`, available
once `invokeLoadHolons` has returned a usable response on the dedicated loader
transaction. It discovers that transaction's Saved Nursery membership through
the ordinary `GetCommittedHolons` command, then creates and owns a fresh review
transaction. Space binding is verified before returning the review. An unsuccessful
review initialization releases the newly acquired context and reports any cleanup
failure explicitly.

`CommittedHolonsReview.collection` is a DescribedHolonCollection with common
`HolonType.TypeDescriptor` element type; members retain their concrete descriptors.
It retains identity-only SmartReferences with no
staged or cached property map copied from the loader. `readMembers()` retrieves
committed keys and concrete descriptors, reporting per-field access failures while
retaining every member's identity and reference. Missing keys remain absent rather
than excluding a member. Other committed properties and relationships are read
through these ordinary bound references. Review lookup failures do not alter the
load outcome or claim complete relationship persistence.

The caller owns the returned review and disposes it explicitly. Review disposal
waits for its own pending member reads; it does not dispose the loader transaction.
The enclosing presentation remains responsible for releasing both owners. Visible
Collection presentation and inspector wiring are delivered separately.


### 9.3 Retrieval

These SmartReferences initially identify holons not yet cached in the review context. Iteration triggers DHT retrieval as a by-product of resolving them.

Successful retrieval verifies that the saved holons can be read and supplies committed properties, including keys.

Retained staged property maps must not substitute for retrieved committed properties.

Keyless holons remain inspectable by identity.

Retrieval failures remain visible as saved members whose retrieval failed. They do not silently remove members, substitute staged values, or rewrite the load outcome.

### 9.4 Review Lifetime

The ActionVisualizer owns the review TransactionContext for the lifetime of the load presentation.

Inspectors opened from the committed-result collection retain review-bound subjects;
artifact materialization uses the independently open presentation context.

Dismissing the load presentation:

- Closes diagnostic and committed-result inspectors.
- Releases the result collections.
- Drains work before disposing loader, committed-review, and presentation contexts
  and their retained transient state.

Persisted holons remain accessible through ordinary Space navigation.

Transfer to an independently owned navigation context is deferred.

### 9.5 Result Presentation and Navigator Refresh

The load presentation retains separate Diagnostics and Committed Holons views.
Tabs display Diagnostics (n) and Committed Holons (n), using actual collection
membership counts and hiding only confirmed zeros. Unknown or partial counts
retain explicit read/loading feedback and retry. Complete outcomes initially
select committed results; other outcomes initially select diagnostics, falling
back to the remaining visible tab when the preferred collection is empty. Switching views and returning from inspection retains the
mounted collection and its selection, sort, and scroll state.

Committed rows use the review's authoritative membership and bound references.
The presentation may supply a typed value projection of committed keys and
per-member read failures to the selected Collection Visualizer. Missing keys
remain absent, and failed members remain selectable by identity. Retry refreshes
saved-state reads without resubmitting the load.

`CommittedHolonsReview.transaction` exposes the owned review context for normal
Visualizer selection and inspection. The review remains its disposal owner.
The invoking Navigator supplies its selected RootedNavigation presentation and
Node slot context. When a response exists, that actual load response is the root
subject of one ordinary Path Inspector instance, including rejected and
incomplete outcomes. No universal result wrapper is introduced. Rust selects its Node Visualizer against
`HolonLoadResponse.DanceResponseType`, using the existing
[slot-directed descriptor selection](../../hx/dahn-design-spec.md#1421-slot-directed-descriptor-selection)
contract: inspect the concrete type's local applicability declarations, then
follow `Extends` only when there is no eligible candidate, stopping at the
TypeKind boundary. An ambiguous eligible set is an explicit selection failure,
not a reason to continue upward.

`LoadHolons.NodeVisualizer` selects for the actual response and presents compact
property/value chips, counted result collections, and ordinary singular relationships.
The retained LoadRequest selects the standard HolonInspector as described in §8.2.
Collection expansion hides the summary and rail while retaining the collection's
state; restoration returns the ordinary composition. Additional inspector height
goes to the collection viewport rather than empty summary space.

The response retains its loader-bound reference. Read-only Visualizer selection
is permitted against that retained evidence after commit. It does not reopen the
loader transaction. All Visualizer materialization and artifact retrieval use
an independently open presentation context, rebinding only saved Visualizer and slot references:
materialization creates invocation holons and must never run in the committed
loader context. Committed collection members
retain their review-bound saved references. The root collection adapter supplies
stable result-role provenance to the ordinary Path Navigator; activating a
committed member creates or restores a vertical occurrence in that same path.
Descendant reads and node selection use each subject's owning loader or
committed-review context. Collection selection and saved slot lookup use the
independently open presentation context, since they require transaction-scoped
saved lookup after the loader transaction has committed. Collection selection
uses the saved element descriptor with an empty member envelope as a type witness;
actual collection membership, member reads, and row activation retain their
original bound references. Transient and staged members are never rebound into
presentation ownership. Root path creation does not wait for committed-review initialization,
membership retrieval, or per-member reads. Those failures affect the committed
collection and its retry feedback while response and diagnostic navigation remain
available. Collection tab changes
retain existing path occurrences and revoke activation from hidden collections.
The specialized root participates in the same Node allocation and restoration
contract as other Nodes; it supplies summary chips and bounded collection regions,
while Path Inspector owns traversal, occurrence placement, and compression.
Both axes follow the ordinary Path Inspector interaction grammar, including
combined compression and restoration. Partial-height collection traversal
retains the title, tabs, and useful Collection Viewer allocation (controls,
header, and five rows under the shared grammar); the properties body yields
space. Selected child visualizers own internal composition. Compression does
not discard relationships, collection state, or occurrence provenance.
The load owner disposes the path and drains all participating work before releasing
its presentation, committed-review, and loader contexts.
No second mutation workflow or independent exploration ownership is introduced.
Diagnostic rows remain projections of retained loader evidence; their detail
presentation must not rebind staged evidence into the saved-state review.

Without a response, the retained request roots ordinary inspection as specified
in §8.2. Preparation retry drains and disposes the old path before a new attempt.

After Complete or Incomplete outcomes, the invoking Navigator invalidates its
semantic reads without recreating exploration. Relationship discovery and open
collections request membership with the public `requireFresh` option before
reading described collection envelopes. The fresh read updates the relationship
cache used by the described read. Failures remain visible in the affected view
and do not change the load outcome. Existing navigation topology is retained.


## 10. Specification Ownership and Delivery

| Document | Responsibility |
|---|---|
| Load Holons use case model | Agent intentions, action/response flows, and alternatives. |
| Load Holons Design Spec | Loader-specific interaction, ownership, lifecycle, outcomes, diagnostics, and review contracts. |
| DAHN Design Spec | Reusable action activation, Visualizer selection, and composition contracts. |
| Space Navigator Design Spec | HolonInspector initiation and navigation integration. |
| Owning transaction specifications | Generic transaction, Nursery, reference, closure, and disposal semantics. |
| Loader implementation plan | Delivery sequence, dependencies, boundaries, and acceptance checks. |

Reusable contracts must be recorded in their owning specifications and referenced here rather than independently redefined.

Space Navigator PR 40.a delegates loader delivery to DL-01–DL-14. The plans must avoid duplicate accounting for the same work.

Existing Canvas-scoped initiation language must be reconciled with the HolonSpace-afforded, HolonInspector-initiated model.

DL-05 retains the native picker feasibility investigation.

## 11. Required Reconciliation Checks

Before implementation is considered aligned:

- Normal, partial, rejected, parser-failure, and no-response flows must identify the ActionVisualizer presentation owner and relevant TransactionContext.
- Destruction of the owning presentation must be blocked during execution.
- Only `Complete` must receive the existing successful transaction-closure behavior.
- Diagnostics must remain rooted in the loader context.
- Committed-result membership must come from Nursery Saved-state evidence.
- Committed inspection must use the separate review context.
- Disposal must release transient state without implying undo of persisted operations.
- Generic Action Bar code must contain no loader-specific interaction logic.
- Visualizer failures must remain explicit, without hard-coded fallbacks.
- Use cases and delivery plans must reference the final design contracts rather than retain superseded ownership or dismissal rules.

## Action presentation and host lifecycle contract

The ActionBar is a Visualizer that allocates uniform slots for the actions available
in its bound context. Each slot contains a separately selected ActionVisualizer;
that action owns its label, theme-dependent icon presentation, and interaction.
Groups remain cohesive layout units, may have separators, and will move as units
when personalization is introduced. Personalization is outside the initial loader slice.

The Node selects an `ActionBar` using the affording holon as subject. The selected
bar owns an action slot accepting `ActionVisualizer.HolonType`. Each `Action`
request uses the available Dance descriptor itself as subject, with the selected
bar and its owned slot. Applicability follows that descriptor's Extends lineage;
it must not project to the Dance descriptor's describing meta-type. Normal Rust
selection and materialization remain authoritative. A registered generic disabled
action presentation can apply at the Dance TypeKind boundary; it is not a client
fallback for failed selection.

The selected Load Holons action opens a neighboring Navigator tab. Source review,
progress, diagnostics, committed results, and normal inspection share that tab,
using the available workspace allocation. Switching tabs retains load state.
The load presentation acts as a specialized node: summary properties appear as
chips, with Diagnostics and Committed holons collection tabs and no singular
relationship rail. Collection members occupy a bounded vertical allocation;
activating a member expands inspection below the collection without replacing
the summary or requiring a Back to results transition.
This supersedes the earlier modeless pop-up placement. Its host adapter explicitly
mounts and destroys the Angular source-review view and subscriptions. A dedicated
transaction is created and the captured persisted HolonSpace is checked against
its Space authority before native source selection. Navigation never retargets it.

The Commands runtime records the latest successfully prepared request and atomically
admits at most one canonical LoadHolons submission per transaction. A preparation
failure permits correction; a submitted invocation, including a no-response failure,
never re-enables submission. Readable response and staged evidence remain retained.
Runtime command leases exclude explicit disposal while any admitted command is active.
`Dispose` releases transaction pools, recovery state, and active/archived session
ownership; it neither rolls back nor deletes persisted holons. Removed transactions
cannot be rebound through Commands. This is distinct from successful commit and archive.

Pre-submit cancellation waits for pending transaction creation/binding to settle,
then disposes it and ignores late picker results. Preparation/submission execution
blocks dismissal at the load tab, owning Node, branch replacement, exploration tab,
and experiential context. Focus changes and retained off-screen presentations are
not dismissal. Terminal review permits explicit release. Loading feedback reports
only client-observed preparation, invocation, and response-reading transitions with
elapsed time; status and counts come from the authoritative response.

Submitting replaces the source review contents with a distinct “Load in progress”
view in the same load tab: indeterminate activity, parsing/preparation and execution feedback,
submitted file count, and elapsed time. Phase changes are announced accessibly;
timer ticks are not repeated live announcements, and motion respects the agent's
reduced-motion preference. Review controls are absent during loading. This does
not add guest progress measurement or cancellation. A preparation failure restores
the retained review selection for correction/retry; a usable response or invocation
failure replaces pending content with the corresponding terminal review.

