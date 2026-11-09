# Saved Holon Cache Design Specification

## Purpose and authority

This specification owns the reusable Rust saved-Holon cache population contract.
It complements [runtime shared types](runtime-shared-types.md) and the
[layered representation architecture](../architecture/holon-layered-representation-design-spec.md).
Descriptor computation, consumer warming policy, and executable Visualizer artifact
caching are separate concerns. Full `Holon` state transfer is permitted here only
as infrastructure hydration; application results remain reference-backed.

## State ownership, identity, and validity

The host saved-Holon cache belongs to its Rust Holon-space runtime and is shared
across requests using that runtime. A request must not replace it with a new cache.
References resolve against this same cache; bulk population introduces no parallel
state store and no TypeScript Holon cache.

Deduplication and lookup use the existing complete `HolonId` within the owning
space/cache capability, including external-space identity where applicable. Keys,
lineage roots, display names, and descriptor occurrence identities do not substitute
for exact saved-version identity. Population does not advance a reference to a
newer lineage head or merge different versions.

A usable hit is saved state that ordinary reference resolution may reuse under
the same space, access context, and validity rules. Population preserves those
rules, recognition requirements, normal authorization, and restricted cache-read
execution. It neither grants access nor substitutes saved state for a staged or
transient reference. Staged changes remain in their existing transaction-owned
stores. Relationship membership freshness, prepared-schema generation, and
saved-node residency remain distinct; warming node state does not mark adjacency
fresh or refresh an effective descriptor snapshot.

## Space Session participation

The [space Session specification](space-session-design-spec.md) owns retirement
of registered derived results. Reset does not clear saved-node residency,
relationship memberships, or their policy/resolution inputs. Ordinary reference
reads continue to enforce their existing policies; bulk warming neither starts
nor ends a Session. In-flight membership fetches retain their ordinary cache
semantics across derived reset. Exact saved-version identity and staged state
remain unchanged.

## Relationship-policy acquisition boundary

RelationshipDescriptor acquires its final membership policy from its RelationshipType
derived result; the [descriptor specification](descriptors/descriptors-design-spec.md#146-guest-preparation-and-local-cache-policy)
owns that computation and its bootstrap rules. Establish an entry against the exact
outbound relationship descriptor, including declared/inverse identity, and retain
its resolved policy value. Existing Session preparation can supply that association
before the first membership fetch. Read names and policies from PreparedSchema and
recover exact saved IDs from retained descriptor references; never parse display
identity strings. Complete source reads use the union of effective declared members
and the filtered singular/plural navigation products. This does not hydrate those
descriptor targets, remove declarations omitted by navigation, or reintroduce
maximum-zero inverse navigation.

Named and requested-set reads consult existing preparation only after a membership
miss with no retained policy, using a resident, unexpired DescribedBy association.
They do not fetch DescribedBy or construct a descriptor solely to find a policy.
Descriptor sources whose declared instance contract includes Extends retain guest binding: their own
ancestry can contribute SourceOf candidates beyond their describing type's projection.
Complete source reads can still reuse their prepared names. With no applicable
preparation, the first membership fetch carries the exact descriptor identity and
derived policy alongside the targets in the existing guest response. Guest binding
considers both the source's describing contract and its own descriptor ancestry, as
specified in the descriptor contract. No second host-orchestrated discovery request
is required.

Host policy resolution is entirely local: read the associated descriptor's prepared
policy and retain that scalar in the relationship-cache entry. Usable membership
hits check the scalar directly. Expiry and explicit freshness preserve the descriptor
association and fetch membership without rebinding it. A separate source-type/name
policy table is not an independent authority. Missing ordinary descriptor association
is an explicit error to correct at binding, not a reason to discover schema during
host policy resolution or silently serve indefinitely unretained membership.
Foundational and active-construction recursion breaks remain bounded by the
[descriptor contract](descriptors/descriptors-design-spec.md#146-guest-preparation-and-local-cache-policy).
Cache locks must not span transport or reentrant descriptor acquisition.

MembershipCacheMaxAgeMillis is optional. Its absence yields a resolved Fresh policy
unless declared-definitional membership requires Reuse. An unresolved runtime
policy is distinct from an omitted schema property. Derived-state retirement does
not invalidate retained relationship entries or override their existing policies.

## Complete source relationship reads

A saved source's `all_related_holons` uses its complete described outbound
vocabulary: declared relationships remain included even when presentation navigation
omits them, and available inverse relationships are included. Persisted relationship
membership is governed by this vocabulary; a separate source-wide completeness marker
is unnecessary.

Coverage requires a currently reusable membership collection for every name under the
ordinary policy and generation checks. A known-empty collection counts as fetched;
a missing name, expired collection, or policy-only Fresh entry does not. When coverage
is complete, return the resident collections without a membership-provider request.
Vocabulary discovery remains subject to descriptor lookup and preparation rules.

On a coverage miss, retrieve all physical SmartLinks for that source with one
source-wide query. Select the missing memberships and explicitly complete requested
names absent from that result with empty collections. A host performs this operation
through the existing fetch-all dance; the response carries exact descriptor identities
and policies for unresolved names alongside the memberships. Retained descriptor
associations and policies, including those supplied by existing preparation, need no
rebinding. A prepared association is not a fetched membership or a coverage marker;
Fresh policies still fetch every time and known-empty memberships retain ordinary
expiry rules. Session-guarded projection rejects retired prepared results, while
already retained relationship entries keep their existing policy lifetime.

Bulk and named reads share target-reference construction, canonical key hints,
keyless membership, multiplicity, collection sealing, policy retention, and TTL rules.
Valid resident memberships keep their collection identities. Newly fetched Fresh
memberships are returned for this call without requiring a second fetch and without
retaining them for future reads. A failed fetch, incomplete requested set, or invalid
membership installs none of that fetch's new cache entries. No cache lock spans the
provider operation or descriptor binding.

## Retrieval execution ownership

Saved references remain space-bound, self-resolving handles. Cache residency is a
private cache-manager concern: `get_rc_holon` returns a resident node directly,
without opening a transaction. A miss that requires service retrieval obtains a
short-lived restricted read transaction through the owning space's existing
transaction machinery. The cache manager holds a weak space capability so it does
not form an ownership cycle. The private read guard disposes its context on both
success and error; it does not accumulate public transaction contexts.

Service methods retain their explicit execution-context contract for normal
host-to-guest request construction. Callers of ordinary cache/reference reads do
not supply that context or probe residency. Space-bound read handles delegate to
this same retrieval boundary; they do not retain the transaction that originally
minted a saved reference. This one-call context is distinct from the retained
restricted transaction that owns registered derived results.

## Bulk population contract

`ensure_cached(ids)` accepts a finite collection of saved Holon identities
through the Rust cache-access surface. The cache manager supplies private retrieval
execution when needed; `HolonServiceApi` receives its explicit context internally.
Ordinary reference APIs remain bound and self-resolving.

The operation:

1. Deduplicates requested identities under the cache's identity rules.
2. Inspects usable resident state without initiating retrieval for hits.
3. Joins compatible retrievals already in progress where the runtime supports it.
4. Sends only remaining missing identities in one bulk guest invocation for an
   ordinary bounded batch on a supported route. An empty missing set sends none.
5. Associates every response outcome with its requested identity, validates the
   association and saved-state shape, and populates successful entries through
   the same cache insertion path used for ordinary lazy misses.
6. Returns an error vector; success is implicit. Usable hits and successfully
   populated identities produce no result entries. ID-specific errors identify
   the requested identity and preserve the relevant existing error, including
   absence or unsupported/inaccessible routes. Unexpected response identities
   produce protocol diagnostics identifying those unexpected IDs. A batch
   transport failure may identify all still-unresolved identities in one error
   entry; it does not erase independent successes. An empty error vector means
   population completed successfully, subject to ordinary eviction.

| Distinct requested identities | Usable cached entries | Missing entries | Additional guest invocations |
| --- | ---: | ---: | --- |
| 100 | 0 | 100 | 1 bulk invocation |
| 100 | 85 | 15 | 1 bulk invocation |
| 100 | 100 | 0 | 0 |

These examples assume one supported route, no compatible work already in flight,
and a payload within transport limits. Unsupported external routes must report
errors explicitly rather than bypass routing policy. No numeric batch/payload
limit has been established in the inspected retrieval path. Chunking is justified
only by a verified transport constraint; it must be reported in invocation counts.
One guest invocation need not imply one storage-layer read.

Successful population is shared with subsequent requests until ordinary eviction
or lifecycle disposal. Population returns no retention leases and preserves
existing retained content. A batch can evict its own earlier entries; successful
population does not guarantee simultaneous residency of all requested identities
when the operation returns. Optional population-and-retention support is a
separate capability extension whose lifetime belongs to its consuming operation.
Retention changes residency, not validity, reference semantics, or access authority;
population introduces no permanent pinning.

## Partial results and concurrency

An unavailable or failed target does not prevent independent successes from
being cached. Missing results are not inferred from response order or silently
dropped. Unexpected, duplicate, omitted, mismatched, or non-saved response entries
are reported as protocol errors for affected identities; validated independent
successes remain usable. Absent and failed targets are not negative-cached by
this contract.

A failed population attempt does not invalidate previously usable cache state.
The operation reports errors identifying unresolved identities and preserves
normal lazy reference behavior. A subsequent required read may still surface its ordinary error;
population does not turn absent required data into valid data.

Overlapping warmups and lazy misses reuse compatible in-flight work where such
coordination exists. Cache insertion rechecks residency and preserves a concurrently
installed usable entry, including retained content. Network work must not hold
cache locks across a guest call or introduce reentrant waits on its own retrieval.
A new general saved-state single-flight coordinator is a separate concurrency
extension if the runtime lacks one; batch-local deduplication and bulk population
do not depend on a broad concurrency redesign. Races may then duplicate work
across separate calls, but never within one batch. Guest-reachable shared code
remains WASM-safe.

## Caller policy boundary

`ensure_cached` operates only on the saved identities supplied by its caller.
It does not discover targets, choose relationship groups, traverse a graph, or
select when an application should warm state. Those decisions belong to each
usage of the capability and are specified independently.

The capability does not prescribe an integration point in descriptor construction,
named-member lookup, Inspector projection, or any other application workflow.
No particular caller integration is required to establish this contract. Callers
may choose any explicit finite saved-ID set; the same missing-only population
semantics apply to every set. Ordinary lazy resolution continues independently.

## Observable contract and verification

The examples above express guest-invocation counts for cold, partially resident,
and fully resident requests. Empty requests also make zero guest invocations.
Duplicate identities do not increase retrieval count within a batch. A successful
result is observable through an existing reference to the same saved identity,
including from a subsequent request using the same runtime while the entry remains
resident. Population makes no permanent-residency guarantee beyond existing
retention semantics.

Verification distinguishes partial absence, per-identity failure, batch transport
failure, and invalid response associations. Independent successful entries remain
usable in each applicable case. Exact versions, space capabilities, staged state,
and existing retained content remain distinct and unchanged by population.
Concurrent-call verification covers joining when implemented and preservation of
usable entries installed during retrieval; batch-local uniqueness does not imply
cross-call single-flight coordination.

Capability-level diagnostics expose requested and distinct identity counts,
usable hits, missing identities, joined work when supported, guest invocations,
success and error counts, and elapsed retrieval time. Cold and warm measurements
use the same runtime and explicit input set. Guest-invocation counts remain
separate from underlying storage-read counts. Consumer-specific usefulness metrics
and warming-policy experiments belong to the corresponding usage, not this contract.
