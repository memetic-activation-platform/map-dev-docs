# Caching: execution context, correctness, and performance

**Status:** implementation lessons from the September 2026 startup investigation;
future options are explicitly separated below. The authoritative cache and
freshness contract remains [Relationship-read policy in Transactions](../transactions/transactions-design-spec.md#9-relationship-read-policy).
This page records why those distinctions mattered in performance diagnosis.

## The central lesson: policy follows lifetime and responsibility

Shared core code executes in very different environments. Changes expected to
help the host can add substantial work to the guest, and vice versa. Core should
own cache mechanics while the existing `HolonServiceApi` supplies the
execution-context policy; avoid scattering host/guest conditionals through
reference operations.

| Context | Useful reuse | Performance consequence |
|---|---|---|
| Host saved-state cache | Space-scoped, across calls | Descriptor-driven retention and freshness matter |
| Coordinator guest saved-state cache | Within one request only | Reuse avoids repeated work; resolving descriptor policy solely to retain a one-shot fetch adds cost |
| Staged/transient references | Authored transaction-local state | Do not force saved-state descriptor policy onto unfinished bootstrap data |
| Integrity PVL | Separate validation execution | Host/coordinator descriptor caches do not eliminate native checks or integrity invocations |

The guest remains useful as a cache during substantial LoadHolons/validation
work. “It starts empty on every request” is not a reason to remove it. It is a
reason not to pay for cross-request freshness classification that cannot deliver
cross-request reuse. In the investigated implementation, the guest reuses fetched
membership for the request without descriptor or clock lookup; explicit fresh
reads remain available when persistence changes what that request needs to see.
Possible future shared memory would change the lifetime assumptions and require
revisiting the policy. It is not an available optimization in these measurements.

## Expensive ways a seemingly helpful cache can regress

1. **Descriptor amplification on a cold guest.** A fetch can trigger descriptor
   retrieval merely to decide whether to retain its result. That can recursively
   expand a graph before returning one relationship collection. A regression
   test specifically covers a one-shot guest read without fetching a descriptor
   graph; retain that protection.
2. **Suppressing definitional reuse while guarding recursion.** Declared
   definitional membership is version-bound. A broad inverse-policy recursion
   guard must not classify every nested relationship as fresh. Declared
   classification must remain available while inverse policy is being resolved.
3. **Looking up policy before checking a valid hit.** Cache eligibility metadata
   should allow a hit without repeating expensive descriptor discovery. Otherwise
   “cached” membership can retain most of the original lookup cost.
4. **Reintroducing obsolete inverse discovery.** The investigation found a path
   inconsistent with the intended source-oriented discovery model and corrected
   it. The thread questioned whether unshelving restored it; that historical
   cause was not proven. Protect the architecture with tests instead of relying
   on a past cleanup or issue number.

## Policy discovery must match the relationship being read

Outbound inverse descriptors are discovered from `SourceOf` indexes on the
source's describing type and its `Extends` ancestry. Traversing `TargetOf`, the
opposite endpoint contract, or `HasInverse` to infer policy can add unrelated
work or miss the intended descriptor. Each direction owns its policy.

Bootstrap schema alignment also mattered: descriptor holons must be licensed by
the appropriate meta-type endpoints. The investigation corrected `ForDance` and
`HasImplementation` endpoint declarations to use `MetaDanceType.MetaHolonType`.
A policy present in generated data is not proof that runtime discovery reaches
that descriptor. Trace source type → effective relationship → policy value.

The user inspected `AffordsDancer`, while the discussed TTL declaration was for
`AffordsDance`. These similar names identify different relationships. Always
verify the exact name and direction rather than borrowing the opposite or a
similarly named declaration's policy.

## TTL: implemented behavior and what it does not prove

The host gained descriptor-driven `MembershipCacheMaxAgeMillis`, with an initial
30,000 ms allowance on `AffordsDance`, `HasApplicableVisualizer`, and
`HasImplementation`. The latest app trace included `MaxAgeMillis(30000)` policy
decisions. Functional tests exercised reuse, expiry, forced refresh, and empty
collections; a real-schema integration test passed. This establishes that the
policy is read and applied, not its isolated contribution to the Canvas speedup.

Important distinctions from the owning contract:

- Declared definitional membership can be retained with its immutable saved
  source version. An inverse descriptor's definitional flag is not a license
  for indefinite inverse-membership reuse.
- Mutable host membership defaults to fresh reads unless a positive TTL is
  configured. Missing/zero policy is not an implicit global TTL.
- Bounded age starts before fetching; slow transport must not extend permitted
  freshness. Hits do not renew the age. Empty collections are cacheable results.
- Explicit `RequireFresh` bypasses cached membership and successful refreshes
  replace eligible cached results. Fetch failures do not silently serve stale
  data. A fresh read is not a globally synchronized DHT snapshot.
- Named and all-relationship reads share policy. The all-relationship path
  assembles named reads rather than also fetching the full persisted map.
- Returned saved collections remain sealed; retention must not introduce a
  mutable alias or change reference-layer semantics.

A TTL helps only when the same cache key is reused within its lifetime. A cold
one-shot traversal of many different sources may still fetch each once. Report
hit/miss/expiry counts per source and relationship alongside latency; aggregate
command counts cannot answer whether bounded retention helped.

## Forward-looking options, not implemented conclusions

| Option | Potential value | Question to resolve first |
|---|---|---|
| Signal-driven invalidation | Keep useful host entries longer while reacting to changes | How are missed signals, remote changes, and reconnects handled? |
| Background refresh | Reduce foreground waits for frequently read membership | What staleness and failure behavior does the caller accept? |
| Caller-specific maximum ages | Express different freshness needs per workflow | How do overrides interact with descriptor policy and explicit freshness? |
| Fewer boundary crossings/batched reads | Reduce overhead for many distinct first reads | Can the existing reference/transaction semantics be preserved? |

The first three were retained as future extensions in the transaction document.
Batching is a measurement-led follow-up, not a completed optimization. None
justifies weakening validation, bypassing bound references, or treating TTL as
execution-time authorization.

## Regression evidence to preserve

Keep tests for guest reuse without descriptors, cold request boundaries,
explicit freshness, declared definitional reuse during inverse classification,
source-oriented discovery, TTL expiry without renewal, empty results, sealed
collections, and coherent named/all reads. Measure host and guest separately
when changing shared core behavior. See the [startup evidence](startup-and-canvas.md)
for observed recovery and the [schema investigation](schema-load.md) for costs
that cache changes did not explain.


### Visualizer slot acceptance

AcceptsVisualizerType is definitional: accepted child Visualizer types belong to
the slot's composition contract. Its declared membership uses existing definitional
reuse rather than fresh retrieval for every selection. HasApplicableVisualizer
retains its explicitly configured 30,000 ms discovery-membership policy. Selection
must obtain accepted identities from the supplied slot, avoiding repeated canonical
role-name lookups; this does not authorize caching bound handles across transactions.
