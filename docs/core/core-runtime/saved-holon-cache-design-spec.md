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

## Bulk population contract

`ensure_cached(ids)` accepts a finite collection of saved Holon identities
through the Rust cache-access surface. Its context-bearing cache/service
signatures follow existing `HolonCacheAccess` and `HolonServiceApi` conventions;
ordinary reference APIs remain bound and self-resolving.

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
