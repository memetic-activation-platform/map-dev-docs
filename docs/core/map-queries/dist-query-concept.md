# Distributed Data Retrieval in MAP’s Nested Space Topology

## Core Insight

MAP’s distributed retrieval model emerges naturally from its topology of nested belonging.

A `HolonSpace` is not merely another data object. It is also:

- a social boundary
- a trust boundary
- a storage boundary
- an execution boundary
- a Holochain hApp/DHT boundary

This means that MAP’s social topology and execution topology become the same thing.

In conventional distributed systems:

    Data -> partitioned into shards
    Queries -> routed to shards

In MAP:

    Belonging -> creates spaces
    Spaces -> become hApps / DHTs
    hApps -> become execution domains
    Queries -> follow belonging relationships

This gives MAP a distributed query architecture without requiring an initially sophisticated distributed query engine.

## Focal Space vs Query Horizon

A query should not be limited to a single data space merely because it originates from a single standpoint.

Instead, distinguish:

## Focal Space

The focal space is the place from which the query is authorized, interpreted, and presented.

For example:

    Frank's I-Space

The focal space determines:

- who is asking
- under what authority
- from what standpoint
- with what defaults
- how results are ranked and presented

## Query Horizon

The query horizon is the permission-filtered set of spaces that may participate in answering the query.

For example:

    All spaces Frank belongs to
    that also contain Mary
    and that permit Frank to search messages

So a query like:

    Find messages involving Mary.

may originate in Frank’s I-Space, while its query horizon includes:

    Frank-Mary Space
    Frank-Bob-Mary Space
    Frank-Family Space

The focal space is not the same thing as the search scope.

## Example: Messages from Mary

Suppose:

- Frank has an I-Space.
- Frank shares a direct space with Mary.
- Frank also shares a group space with Bob and Mary.
- Messages may have been exchanged in either context.

If Frank asks:

    Show me messages from Mary.

he may not remember whether the message came through the direct Frank-Mary space or the Frank-Bob-Mary group space.

The query should therefore be interpreted as:

    From Frank’s I-Space,
    search all eligible message-bearing spaces
    that Frank shares with Mary,
    and return messages involving Mary.

This requires the system to derive a query horizon from the belonging graph.

## Shared Space as Canonical Message Store

Mary sends Frank a message in the Frank-Mary space or the Frank-Bob-Mary space, and the message canonically lives in that shared space.

In this pattern:

    Query focal space: Frank's I-Space
    Message storage: one or more we-spaces
    Retrieval: federated across spaces

The query must discover and search the relevant shared spaces.

## Holochain Perspective: Each Space as hApp / DHT

From the Holochain perspective, each MAP space is effectively its own hApp/hApp instance with its own DHT.

Each space may involve different compute nodes.

Therefore, cross-space queries are not simply graph traversals inside a single database. They are federated query executions across multiple hApp/DHT execution domains.

This suggests a coordinator pattern:

    1. Frank starts in his I-Space.
    2. The host discovers spaces Frank belongs to.
    3. The host filters those spaces to ones containing Mary.
    4. The host constructs a query execution plan.
    5. The host dispatches subqueries to participating hApps/spaces.
    6. Results are unioned, ranked, streamed, or otherwise merged.

Conceptually:

    Frank I-Space
        -> Frank-Mary Space
        -> Frank-Bob-Mary Space
        -> Frank-Family Space
        -> Work Space

For:

    Find messages involving Mary.

The host computes:

    Eligible Spaces =
        Frank-Mary Space
        Frank-Bob-Mary Space

Then dispatches:

    Query 1 -> Frank-Mary hApp
    Query 2 -> Frank-Bob-Mary hApp

and returns:

    union(Query 1 results, Query 2 results)

## Query as Dance

Distributed search in MAP can be understood as a Dance.

For example:

    Search Dance
        -> Discover Spaces Dance
        -> Dispatch Search Dance
        -> Aggregate Results Dance
        -> Rank Results Dance

The query is not merely run against a database.

It is choreographed across sovereign spaces through trust channels.

This aligns with the MAP architecture:

    Search is not just a database capability.
    Search is a distributed promise choreography.

## Planner Rule: HolonSpace as Execution Boundary

The query planner needs a simple hard-coded rule:

    When a query step's source is a HolonSpace
    or a collection of HolonSpaces,
    create a subquery for each space
    and execute the remaining query graph in that space.

More generally:

    For each HolonSpace in the source set:
        execute the remaining query graph within that space.

This is reasonable because `HolonSpace` is foundational. It is not just another type descriptor.

Most holons are data.

A `HolonSpace` is infrastructure.

Therefore the query planner may have first-class knowledge of spaces without over-generalizing this into metadata-driven behavior.

## Recursive Distributed Execution

This rule can apply recursively.

If a subquery running inside Space A encounters references to further spaces, the same rule may apply:

    Encounter HolonSpace
        -> spawn subquery into that space

Thus a distributed query is simply a query graph whose evaluation crosses one or more space boundaries.

## Two Distributed Retrieval Mechanisms

The conversation distinguished two different mechanisms that both involve cross-space communication but arise at different layers.

## 1. Query-Planned Distribution

This happens when the query planner can see that a step is operating over a space or collection of spaces.

Example:

    Expand(BelongsTo)
        -> [SpaceA, SpaceB, SpaceC]

    Expand(Members)

The planner sees that the source of `Expand(Members)` is a collection of spaces.

It generates:

    SpaceA -> Expand(Members)
    SpaceB -> Expand(Members)
    SpaceC -> Expand(Members)

This is coarse-grained, explicit federation.

The planner can see it.

The host can schedule it.

The execution graph is visible.

This pattern means:

    Move query to data.

## 2. Resolution-Driven Distribution

This happens when ordinary execution encounters unresolved references.

For example:

    Message -> Attachments

returns:

    HolonCollection<
        Ref(A),
        Ref(B),
        Ref(C)
    >

Those references are not materialized.

Only later, when code asks for a property:

    attachment.title()

or:

    attachment.get_property("title")

does resolution occur.

The SmartReference asks the SmartPropertyMap or SmartLink whether the needed value is already present.

If not, it asks the Holon Cache Manager for the holon behind the reference.

If the holon is cached, the property is resolved from cache.

If it is not cached, the cache manager initiates a fetch.

This is runtime-driven, not planner-driven.

It behaves much like a virtual-memory page fault:

    Reference access
        -> cache hit
        -> continue

    Reference access
        -> cache miss
        -> fetch holon
        -> continue

This pattern means:

    Move data to query.

## Separation of Concerns

These two mechanisms should remain distinct.

Query-planned distribution is owned by the planner/host.

Resolution-driven distribution is owned by SmartReferences and the Holon Cache Manager.

The planner reasons about spaces and execution domains.

The cache manager reasons about references, cache hits, cache misses, and fetches.

Do not force the planner to reason about cache misses.

Do not force the cache manager to reason about query semantics.

## Possible Third Layer: Transport Optimization / Pulsing

A future optimization may batch many fine-grained fetches into one bulk request.

Without batching:

    Fetch A
    Fetch B
    Fetch C
    Fetch D

With batching by target space:

    Space X:
        A
        B
        D

    Space Y:
        C

becomes:

    GetHolonsById([A, B, D]) -> Space X
    GetHolonsById([C])       -> Space Y

This can be implemented through pulsing:

    If a fetch is needed for Space X:
        if a scheduled payload for Space X exists:
            add the holon ID to the payload
        else:
            create a scheduled payload for Space X

    When the clock threshold expires:
        send one bulk GetHolonsById Dance

This is a performance optimization, not a semantic requirement.

It can be deferred until evidence shows it is needed.

## Host vs Guest Boundary

A key architectural invariant emerged:

    Guests execute within one space.
    Hosts coordinate across spaces.

Each guest is resident in a single space/hApp/DHT.

Therefore a guest may resolve:

- smart-link values
- smart-reference property-map values
- holons local to its own DHT

But a guest should not initiate external trust-channel calls.

Trust channels exist between hosts.

So:

    Guest cache managers may resolve local cache misses.
    Guest cache managers must not initiate external fetches.

External resolution must be coordinated by the host.

## Expand Returns References, Not Materialized Holons

An expand operation generally produces a `HolonCollection`.

A `HolonCollection` contains references, not necessarily materialized holons.

The members of that collection may be heterogeneous:

- local references
- external references
- references into several different spaces
- references whose SmartReference property map contains enough information for some operations
- references requiring later materialization

The expand step itself does not chase every link.

Resolution occurs only when later work requires access to state not already present in the SmartReference or SmartLink.

## Expand-Filter Dyad

A major insight is that `Expand` and `Filter` often form a tightly coupled dyad.

Rather than:

    Expand(Members)
        -> return all members

    Host:
        Filter(name contains "Mary")

the planner should often push the coupled operation into the target space:

    Expand(Members)
    Filter(name contains "Mary")

This allows filtering to happen near storage.

The social organism/space returns only matching references rather than all members.

This is predicate pushdown emerging naturally from the execution topology.

## Example: Searching for Mary Across Groups

From Frank’s I-Space:

    Expand(BelongsTo)
        -> [GroupA, GroupB, GroupC]

Then:

    Expand(Members)
    Filter(name contains "Mary")

Because the source is a collection of spaces, the planner sends the expand-filter pair to each group:

    GroupA:
        Expand(Members)
        Filter(name contains "Mary")

    GroupB:
        Expand(Members)
        Filter(name contains "Mary")

    GroupC:
        Expand(Members)
        Filter(name contains "Mary")

Each group returns only matches:

    GroupA -> []
    GroupB -> [Mary Jones]
    GroupC -> [Mary Smith]

The host unions or otherwise merges the results.

This means MAP avoids dragging all group-member data to a central place merely to filter it.

Filtering is distributed.

## Local and Partial Filter Evaluation

If a guest receives an expand-filter operation, it can evaluate the filter using anything local to its space:

- values embedded in SmartLinks
- values present in SmartReference property maps
- holons local to the guest’s DHT

If the collection contains external references, the guest cannot fetch across trust channels.

Therefore, guest-side filter evaluation may be partial.

For references that cannot be evaluated locally, the host/planner may later group them by external target space and dispatch a filter subgraph to each relevant space.

## Blended Pattern: Opportunistic Local Filtering + External Filter Pushdown

A future optimizer can combine both mechanisms:

    1. Expand locally.
    2. Filter what can be filtered locally.
    3. Identify unresolved external references.
    4. Group external references by target space.
    5. Send the filter subgraph to each foreign space.
    6. Foreign host delegates execution to its guest.
    7. Guest evaluates the filter locally.
    8. Return matching references.
    9. Merge results.

This preserves the distinction between planner-level distribution and cache/runtime resolution while allowing them to cooperate as an optimization.

## Why Not Materialize Everything?

A naive implementation might expand a relationship, materialize every referenced holon, and then filter.

That is expensive because it moves too much data.

MAP’s preferred strategy is:

    Push computation toward the space where the data is local.
    Return references or compact result structures.
    Materialize holons only when needed.

This keeps data movement low and respects space sovereignty.

## Dashboard Use Case: I-Space Landing Page

On a person’s MAP landing page or I-Space dashboard, two relational lists are especially important:

    1. Spaces I belong to.
    2. People I am connected with.

## Spaces I Belong To

This is straightforward.

Starting from my I-Space:

    Expand(BelongsTo)

returns the spaces I belong to.

The UI can display thumbnails or summary cards for those spaces.

Some display fields may be available in SmartLinks or SmartReferences.

Others may require lazy resolution.

The UI should handle both gracefully.

Important caveat:

Do not assume SmartLink semantics are uniform across all relationship types.

Instead, the UI asks for the properties it wants.

Some may be resolved from the SmartReference. Some may require holon resolution. But because holon's are cached, no holon need be retrieved from its source space more than once.

## People I Am Connected With

This can be approached in two ways.

## Full List

Ask:

    Show me all people I am connected with.

This may produce a very large list and therefore needs pagination/windowing.

## Search or Filtered List

More commonly, the person asks:

    Find Mary.

or:

    Show me people matching some criteria.

This becomes:

    Expand(BelongsTo)
        -> spaces I belong to

    For each space:
        Expand(Members)
        Filter(criteria)

The planner naturally fans out by space.

Each social organism filters locally.

The host merges results.

This gives scalable distributed search over one’s relational field.

## Natural Parallelism from Nested Belonging

If Frank belongs to 10 spaces, a query over those spaces can become 10 parallel subqueries.

If Frank belongs to 1,000 spaces, the same rule still applies.

The planner may later optimize execution by:

- prioritizing recently active spaces
- limiting initial fan-out
- streaming results
- caching prior results
- batching requests
- applying backpressure
- ranking spaces by likelihood of relevance

But the conceptual model does not change.

The natural topology of belonging provides the partitioning and the parallelism.

## Key Design Rules

## Rule 1: Focal Space Is Not Search Scope

A query originates from a focal space, but its scope may include a derived query horizon.

## Rule 2: HolonSpace Is a Distributed Execution Boundary

When a query step’s source is a `HolonSpace` or collection of `HolonSpace`s, the planner creates subqueries for those spaces.

## Rule 3: Guests Execute Locally

Guests operate within a single space/hApp/DHT and should not initiate external trust-channel calls.

## Rule 4: Hosts Coordinate Across Spaces

Hosts manage trust channels, route Dance requests, dispatch subgraphs, and merge results.

## Rule 5: Expand Returns References

Relationship expansion returns a collection of holon references, not necessarily materialized holons.

## Rule 6: Resolve on Demand

SmartReferences resolve state only when needed.

Resolution first checks embedded/smart data, then cache, then local or external fetch depending on context.

## Rule 7: Push Expand-Filter Dyads Down

When an expand is followed by a filter, and both can be executed in the same target space, ship the expand-filter pair to that space.

## Rule 8: Filter Near Storage

Move predicates to the spaces where the relevant data is local whenever possible.

## Rule 9: Keep Query Planning and Cache Resolution Distinct

Planner-driven distribution and cache-miss-driven retrieval are different mechanisms and should remain architecturally separate.

## Rule 10: Optimize Later Without Redesign

Batching, pulsing, prefetching, streaming, prioritization, and query optimization can be added later because the foundational execution model is already compatible with them.

## Robustness Analysis

The emerging model appears robust because it does not require MAP to introduce an unrelated distributed query architecture.

The architecture follows directly from existing commitments:

- agents belong to spaces
- spaces are Holochain hApps/DHTs
- interactions require shared space context
- trust channels connect hosts
- guests are local to spaces
- relationship expansion returns references
- smart references support lazy resolution
- Dances convey executable requests through trust channels

The same primitive that models social belonging also provides:

- partitioning
- locality
- federation
- parallelism
- authority boundaries
- trust boundaries
- storage boundaries
- execution boundaries

This suggests the abstraction is carrying significant architectural weight.

## Summary

MAP can support distributed data retrieval by treating nested belonging as both social topology and execution topology.

A query begins from a focal space, derives a permissioned query horizon, and fans out across relevant spaces when the planner encounters `HolonSpace` execution boundaries.

For set-oriented operations, the planner moves query subgraphs to the spaces where data lives.

For object-oriented access, SmartReferences and the Holon Cache Manager lazily resolve references on demand.

Expand-filter dyads allow filtering to be pushed down into each social organism, minimizing data movement and enabling natural distributed search.

The result is a system where distributed query execution emerges from MAP’s core model rather than being bolted on as a separate layer.