# Key architectural insights for performance

These lessons synthesize the September 2026 startup and caching investigations.
They describe observed costs and their architectural implications, not new
runtime contracts. The [document role manifest](../document-role-manifest.md)
identifies the authoritative specifications; the linked investigations retain
measurements, limitations, and open questions.

## 1. Shared code does not imply shared execution costs

The host retains state across calls. The coordinator guest starts with a fresh
request-local cache. Integrity validation executes separately through
Holochain/Wasmer. Host cache contents do not automatically serve either guest.
A change to shared core behavior can improve one environment and harm another.

**Implication:** identify the execution context, state lifetime, and actual
beneficiary before changing shared behavior. Test host and guest paths separately.
See [execution responsibilities](schema-load.md#execution-boundaries-and-responsibility)
and the [caching investigation](caching.md).

## 2. The service boundary can express different policies without splitting core mechanics

Core can own cache mechanics while `HolonServiceApi` supplies the policy for its
execution context. The host needs descriptor-driven retention and freshness.
The guest benefits from reuse within its request without fetching descriptors
merely to decide whether to cache a result. Guest caching still matters for
substantial work within a request, including loader and validation workflows.

**Implication:** preserve the existing service boundary rather than scattering
host/guest conditions through reference operations. If guest state ever survives
requests, revisit the lifetime assumptions before retaining this policy.
The contract belongs to [relationship-read policy](../transactions/transactions-design-spec.md#9-relationship-read-policy).

## 3. Self-description can amplify the cost of a simple read

A relationship read can lead to descriptor lookup, inheritance traversal,
inverse discovery, and further reads. A cold cache is particularly vulnerable:
classification can cost more than the membership fetch it governs. A cache that
still resolves descriptors on every hit can retain much of the original cost.

**Implication:** use retained eligibility metadata on valid hits; avoid guest
classification solely for retention; and protect declared definitional reuse
when guarding inverse-policy recursion. Trace the graph work behind an API call,
not just the call count. See [cache regression mechanisms](caching.md#expensive-ways-a-seemingly-helpful-cache-can-regress).

## 4. Relationship semantics determine safe reuse

Declared definitional membership is bound to an immutable saved source version.
Inverse membership can change as other sources add relationships; it cannot
inherit indefinite retention merely because its descriptor is definitional.
Mutable discovery relationships can instead use bounded TTL reuse.

**Implication:** classify the exact relationship and direction. Source-oriented
inverse discovery must reach the correct descriptor and its own policy. TTL
bounds permitted age; it does not establish globally synchronized freshness or
replace execution-time validation. Explicit fresh reads remain meaningful even
within a guest request after persistence. See [TTL findings and limits](caching.md#ttl-implemented-behavior-and-what-it-does-not-prove).

## 5. Semantic traversal and boundary crossings can dominate UI startup

Canvas construction took about a millisecond in the compared profiles, while
theme projection and visualizer realization took seconds. Artifact-byte fetching
was inexpensive relative to realization. Much of the work behind presentation
was graph retrieval, semantic selection, and dance execution.

Canvas recovered from 118.7 seconds to 14–15 seconds with unchanged counts for
key browser commands. This demonstrates a large change in cost beneath those
API calls; it does not isolate TTL's contribution or prove that every repeated
command should have been a cache hit.

**Implication:** distinguish graph traversal and selection from DOM construction,
paint, and artifact transfer. Correlate source identities, cache decisions, and
actual transport work. Investigate fewer boundary crossings only while preserving
bound-reference semantics and Rust-owned selection. See [Canvas measurements](startup-and-canvas.md).

## 6. The host call waits for inline validation and persistence

In the measured Holochain 0.6.3 path, the host does **not** receive the zome-call
result while local inline validation is still running. The host service call
remains pending until that validation and the source-chain flush finish. MAP's
synchronous service adapter waits for this result; returning from the coordinator
WASM function does not release the host caller.

The log label `load_holons_returning` marks the coordinator finishing its function
and handing its result back to the conductor. It does not mean the conductor has
returned the result to the host. The sequence is:

1. Coordinator runs LoadHolons, including MAP descriptor-driven commit validation
   and action creation in Holochain's workspace.
2. Coordinator emits its return marker and returns to the conductor.
3. Conductor awaits native system validation and integrity-zome PVL callbacks.
4. Conductor awaits source-chain flush, then completes the call to the host.

Calling step 2 “guest commit complete” is also misleading: durable source-chain
flush and Holochain's inline validation are still outstanding. Nor is all the
remaining validation “on the guest”: system checks execute natively in the
conductor; PVL executes in integrity WASM. PVL does not retrieve descriptors.

**Implication:** the measured interval after the coordinator marker is still
inside the host's outstanding service call. It must be included in service
latency, with costs attributed to inline validation, integrity runtime setup,
persistence, and response delivery. Prefer “coordinator execution finished”
over “guest returning” when explaining this boundary.

This guarantee concerns local inline validation, not completion of all eventual
DHT integration, publication, or validation by remote peers. Those are separate
workflows and can continue after the host receives a successful response.
See [schema-load boundaries](schema-load.md#execution-boundaries-and-responsibility)
and the authoritative [validation architecture](../validation/validation-arch.md).

## 7. Runtime infrastructure can outweigh domain-rule execution

Sampling found substantial native signature-verification, Wasmer instance-setup,
and memory-growth/copying costs. Those are costs around validation, not evidence
that descriptor retrieval or PVL rule evaluation dominates. CPU sample shares
are not an exact elapsed-time budget.

Increasing integrity WASM initial memory to 4 MiB made the controlled workload
slower: median post-return time rose from 39.3 to 57.7 seconds. Earlier optimized
native builds were faster than unoptimized ones, but still require an
otherwise-identical A/B before claiming an app speedup.

**Implication:** larger allocations and additional caching are hypotheses to
measure, not automatic improvements. Investigate runtime lifecycle and build
configuration while preserving validation and invocation isolation. See
[experiments and decisions](schema-load.md#experiments-and-decisions).

## Applying these lessons

Measure a named phase and its execution boundaries before optimizing it. Keep
correctness, cache eligibility, hit rates, and elapsed-time improvements as
separate claims. A faster Canvas can coexist with slower schema loading, and
several simultaneous fixes do not establish individual causality.

MAP's abstractions remain useful, but can hide graph expansion, repeated
transport crossings, and runtime setup. Make those costs visible within the
existing architecture; do not weaken validation or bypass the reference layer
to improve a timer. Preserve failed experiments and unresolved explanations so
future work starts from evidence rather than repeating assumptions.
