# Space Session Design Specification

## Authority and scope

This specification owns the space-management Session contract: lifetime,
retirement of registered derived state, local-commit reset, and request-capture boundaries.
HolonSpaceManager coordinates the Session for its runtime space proxy. Descriptor
registries and other saved-state caches participate in that lifecycle; they do
not define it. Descriptor-specific payloads and acquisition belong to the
[descriptor runtime specification](descriptors/descriptors-design-spec.md).
Saved-content residency belongs to the
[saved-Holon cache specification](saved-holon-cache-design-spec.md).

## Session identity and ownership

A Session is the adopted registered derived-state lifetime within a runtime
HolonSpaceManager. A manager has one active Session. Sharing its Arc among
references, transactions, and runtime components shares that Session; it does
not establish independent agent Sessions within one manager. Multiple agents
may use the same persistent HolonSpace through separate runtime proxies.

The initial Session begins with activation of the runtime space proxy. The host
may outlive it. A reset ends that Session and establishes its successor without
replacing the manager. Registry ownership and derived payloads populate lazily;
reset does not require eager reconstruction. Registry structures may
be retained while their entries are discarded. Ordinary saved-state caches retain
their independent policies and lifetimes.

Transaction lifetime is separate. Reset does not discard staged edits, commit a
transaction, clear Undo/Redo, or introduce a transaction lifecycle transition.
A Commit retains its ordinary transaction completion behavior.

## Session-stable state and exact identity

Registered derived payloads remain stable until Session reset or termination.
Their computed values and prepared reference collections are stable; all state
reachable through those references is not thereby frozen. Entries populate on
demand and may reflect observations made at different times. This contract
provides neither transaction isolation nor a globally consistent snapshot.

Saved references retain exact descriptor-version identity across reset.
Reconstruction may observe newer relationship membership associated with that
identity, but does not retarget it to a lineage successor. New-version adoption
requires explicit resolution or binding to that version.

## Reset triggers

Local Commit completion preserves the active Session only when the guest supplies
explicit evidence that the completed persistence effects cannot change prepared
descriptor products. The verdict is produced by persistence orchestration, not a
caller-selected exemption. Missing or malformed evidence requires reset whenever
persistence may have occurred. A demonstrably empty attempt and semantic rejection
before persistence preserve the Session. Incomplete or uncertain persistence
conservatively resets: successfully written nodes or relationships are not rolled
back. A relationship-only retry can have effects without adding a SavedHolons member.

Descriptor semantics owns the relationship-input inventory used by this verdict.
Effect accounting covers both physical SmartLink directions and the complete
Nursery persistence scope, including previously committed retry participants.
Any potentially affecting write can reset the whole Session without inspecting
which registry entries depend on it. The predicate adds no descriptor acquisition,
storage read, or inheritance traversal.

Node publication creates new exact identities rather than mutating old property
content. Initializing DescribedBy on an identity successfully published as a root
or new version in this attempt is safe by itself. Graph-only updates and unproven
retry origins cannot use that initialization exception. Other watched writes on
new sources remain potentially affecting. A new version never retargets an existing
saved reference to its successor.

Loading, direct DeleteHolon persistence, and explicit pull retain conservative
whole-Session reset. Remote-change adoption retains its explicit reset contract.

Local reset permits derived reconstruction under normal relationship cache policies;
it does not itself force committed membership to be refetched. Process the
successful Commit response into its transaction before resetting,
and complete reset before reporting successful completion to the caller.
If another reset occurred while a reset-worthy Commit was executing, its success still
resets the currently active Session: entries acquired before that success may
omit its effects. Persistence success must not be represented as a failed
Commit merely because subsequent cache reset encounters an error; stale state
must remain retired and the reset failure must be reported distinctly.

Remote Commits do not automatically reset the Session. Adoption follows explicit
pull/reset. Here pull means whole-session reset, not replacement of a single
descriptor entry while other adopted results remain active. A local reset can
also expose remote changes already available to storage/network reads; it cannot
selectively adopt only the local Commit's effects.

## Shared retirement and recovery

Each Session has one shared runtime retirement token referenced by its registered
derived results. Reset retires the outgoing token and removes its entries;
subsequent acquisitions belong to the new Session. Old allocations may remain
until their references are released, but cannot serve semantic derived reads.
Retirement does not require walking every result to change individual flags.

Every accessor exposing a registered derived result checks retirement and reports
a specific obsolete condition. Ordinary descriptor wrappers recover internally:
discard their obsolete private handle, reacquire, and retry. Only that condition
triggers recovery; ordinary resolution, inheritance, and validation errors retain
their semantics. Direct holders of retired results receive the obsolete condition.
A reset does not retroactively revoke values or collections already returned.

## Typed registry participants

A runtime space proxy coordinates multiple typed registry participants. The
derived-descriptor registry and Visualizer-evaluation registry each retain their
own restricted owner transaction and transient pool; neither is scoped to one
caller's public transaction. They share the space's lifecycle infrastructure, not
a single carrier transaction or a universal payload schema. Registry structures
and private owners are retained by the runtime; the space association must not
create ownership cycles.

Each participant owns its typed indexes, complete sealed products, admitted
identities, and reconstruction policy. Owner transactions permit the existing
derived-state read/construction/sealing operations, not staging, Commit, or public
mutation. Read admission checks the actual participant owner and active Session
before exposing a product. A TemporaryId from one participant cannot be rebound
into another participant or a caller's public transaction.

Common coordination provides attachment, disposal, publication against retirement,
and coherent request capture. Each captured participant retains its own owner
TxId, root, and pool. Restore it in the request-local runtime space and rebuild
its typed indexes without changing ownership. Operations capture only required
participants; this generalizes the descriptor-specific capture contract rather
than transporting every registry on every request. Commit still consumes its
restricted descriptor products; guest composition must explicitly carry the
Visualizer products it needs. No process-global registry or extensible plugin
framework is required.

Separate transactions do not by themselves establish separate reset semantics.
The existing Space Session reset still retires admitted derived projections.
Descriptor reconstruction follows its current rules. Visualizer established
decisions can survive as owner-held recipes under the next section: descriptor
retirement is not a Visualizer reconsideration request. Runtime-space termination
disposes all participants and their retained owners.

## Captured decisions and reconstruction recipes

Session retirement applies to registered derived results and their read capabilities.
A typed registry owner may retain a compact reconstruction recipe independently
of retired entries. For example, [DAHN evaluation results](../hx/dahn-design-spec.md#1454-runtime-index-and-preparation-validity)
capture exact selected versions, configuration, and binding scope. A recipe is
owner state, not an admitted semantic result or a public transaction handle.
Retaining it does not freeze the Space graph or extend a retired TemporaryId's life.

After reset, reconstruction publishes a newly admitted result in the active
Session, preserving the captured decision without selection or successor adoption.
Capture contributing relationship facts when exact identities alone cannot
reproduce that decision. Missing inputs cause explicit reconstruction failure.
Domain policy owns deliberate reconsideration; cache reset and payload eviction
do not imply it. This changes no reset triggers, descriptor reacquisition rules,
or relationship-cache freshness policies, and requires no new durable store or
automatic recovery after process termination.

## Registered-result read admission

The registry's retained transaction is a private owner, not a public read capability
for every transient in its pool. Published results are admitted explicitly. Generic
Holon read commands, including SDK collection reads, check admission and the shared
Session token before and after the operation, even when routed through that owner's
transaction. These checks require no schema discovery or storage reads.

Reset revokes all admitted identities from the outgoing Session, including results
superseded by later publications. Unpublished construction envelopes and registry
roots remain internal. Typed narrowing recovers the selected result's retirement
metadata rather than granting a new lifetime. This boundary uses the same shared
token as typed semantic accessors; it does not add per-result validity flags or a
space-wide synchronization barrier.

## Relationship cache policies and independent input lifetimes

Reset retires registered derived results; it does not clear or invalidate
relationship memberships, their retained descriptor/policy associations,
or saved-node content. It does not tag those inputs with the derived Session token
or override their existing validity rules. Reacquisition uses ordinary reference
reads and trusts the relationship cache policy to determine reuse and retrieval.

Fresh membership is fetched on each read. Bounded-age membership remains reusable
until expiry. Reuse membership remains reusable until its own existing lifecycle
or invalidation rules say otherwise. A newly constructed derived payload can
therefore contain the same membership as its predecessor; that is valid under
this contract, not grounds for a defensive cache flush. An explicit freshness
hint, where supported, is a separate caller requirement, not a side effect of reset.

This rule applies after both local-Commit resets and explicit resets following
remote changes. Reset promises reconstruction under normal read semantics, not
a forced newer storage/network observation. Relationship cache consistency belongs
to that subsystem; derived acquisition does not compensate for suspected policy
or commit-cache consistency defects.

An in-flight relationship read may complete and populate its cache according to
its ordinary policy across a derived Session reset. In contrast, a derived
construction from a retired Session cannot publish a registered result into the
new Session. Coordinate that narrow publication/capture boundary without adding
per-relationship dependency graphs or a universal operation drain.

## Commit-local execution

Commit transports the agent transaction state and the descriptor participant's
restricted registry-owning transaction state as distinct inputs. Prepared graphs remain in
their owner's transient pool; they are not cloned into the agent transaction for
transport. Capture observes one coherent selected registry and owner state or
retries against the next Session. Reset cannot dispose the owner mid-capture.

Guest ingress restores both transactions in the same request-local space, binds
the registry to its restored owner, and installs it on that space. Rebuild its
exact descriptor-ID indexes once from transported results, without storage reads
or inheritance computation. This descriptor-participant transport and
reconstruction occurs for Commit requests. Other participants use their explicitly
defined operation boundaries; this rule does not prohibit Visualizer-registry
capture for composition requests. Descriptor accessors use the normal space-bound
acquisition path to find saved-derived products; they need not infer a caller's
transaction context. The descriptor specification owns root/result details.

Guest execution is stateless across requests. Later host Session reset cannot
alter the state already received by an in-flight Commit; no additional cross-request
isolation mechanism or whole-validation drain is required. Additional guest
storage reads still obey normal policy, not a global storage snapshot. Response
handling does not republish an older received registry into the host Session.

The agent TransactionContext separately marks the frozen validation phase, starting
before preparation and ending on every assessment exit. A shared scope token
controls candidate-derived reuse for that immutable input graph. It does not end
the host space Session or clear relationship caches. Rejection permits editing
and a fresh validation scope on retry. Constructing derived output remains allowed;
there is no blanket transient mutation prohibition. Descriptor acquisition,
identity, and memo recovery within that scope are specified in
[the descriptor runtime contract](descriptors/descriptors-design-spec.md#1481-frozen-validation-scope).

Ordinary separate reads have no operation-wide snapshot guarantee. An operation
requiring stable prepared inputs must capture them explicitly; automatic wrapper
recovery alone does not provide that guarantee.
