# Descriptor Usage, Local Extension, and Adaptive Schema Evolution

## Summary

MAP descriptors are often stewarded in one space but used in many other spaces.

For example, the core MAP schema may be stewarded in a `MAP Core Stewardship Space`, while holons described by those core descriptors may live in many other agent, community, project, or application spaces.

This creates a recurring architectural pattern:

1. A space uses a descriptor stewarded elsewhere.
2. That local use produces behavioral signals.
3. Those signals can inform runtime retrieval behavior.
4. The local space may extend the descriptor for its own purposes.
5. Repeated local extensions across many spaces may become evidence for stewarded schema evolution.

This document captures three related but distinct concepts:

- **Descriptor Usage**
- **Local Descriptor Extension**
- **Stewarded Descriptor Evolution**

These should remain separate in the model, even though they can inform one another.

---

# 1. Descriptor Usage

## Core idea

A `DescriptorUsage` record lives in the using space, not necessarily in the stewarding space.

If:

- `SCore` stewards a descriptor such as `PersonType`
- `S1` contains holons described by `PersonType`
- `S1` accesses properties and relationships defined by `PersonType`

then `S1` may maintain a local `DescriptorUsage` record for its use of `SCore:PersonType`.

The usage record does not modify the descriptor. It records how that descriptor is actually used within a local context.

In short:

> A descriptor defines possible structure.  
> A descriptor usage records lived structure.

## Example

Assume:

- `SCore` is the stewarding space for core descriptors.
- `S1` is an agent or application space.
- `S1` has a trust channel to `SCore` for accessing descriptors.
- A holon in `S1` is described by a descriptor stewarded in `SCore`.

When `S1` navigates the `DescribedBy` relationship to that descriptor, `S1` may create or update a local usage record.

That record becomes the natural place to accumulate local information such as:

- how often the descriptor is used
- which properties are frequently accessed
- which relationships are frequently traversed
- which properties are usually satisfied locally
- which properties usually require remote hydration
- which relationship traversals tend to co-occur
- which trust channels are involved in resolving related holons
- which access patterns suggest useful prefetches

## Why usage belongs in the using space

The stewarding space defines the descriptor, but it does not necessarily know how that descriptor is used in each local context.

Different spaces may use the same descriptor very differently.

For example, one space may use a `PersonType` descriptor primarily for display and identity resolution, while another may use it primarily for trust-channel routing, membership, credentials, or collaboration workflows.

The usage record is therefore contextual. It belongs to the using space because it reflects that space's own patterns of attention, navigation, salience, and runtime behavior.

---

# 2. Descriptor Usage as an Adaptive Runtime Signal

## The N+1 fetch problem

Descriptor usage becomes especially important when query execution involves many holons described by the same descriptor.

For example, suppose a query accesses the same property across a collection of 100 holons.

If each property access first attempts local smart-link resolution and then falls through to an external fetch on cache miss, the runtime could accidentally produce 100 individual remote requests.

This is the classic N+1 fetch problem, but in MAP the problem is more complex because the expensive boundary may not simply be a database or cache boundary. It may be a membrane or trust-channel boundary.

Expensive crossings may involve:

- trust-channel mediation
- promise validation
- permission filtering
- remote space access
- serialization and deserialization
- smart-link resolution
- provenance checks
- network latency
- cache hydration

The key performance question is therefore not only:

> Is this value cached?

but also:

> What membrane, trust channel, or remote space must be crossed to resolve this value?

## Descriptor usage metrics

A `DescriptorUsage` record can become the aggregate root for adaptive retrieval statistics.

Possible metric categories include:

### Property usage metrics

For each property defined by or inherited through a descriptor:

- access count
- access frequency
- local smart-link hit rate
- local cache hit rate
- remote hydration rate
- average resolution latency
- failed resolution count
- access frequency by execution context
- access frequency by calling app or dance

### Relationship usage metrics

For each relationship defined by or inherited through a descriptor:

- traversal count
- traversal frequency
- average target count
- local target hit rate
- remote target hydration rate
- average traversal latency
- co-traversal patterns with other relationships
- trust-channel distribution for target resolution

### Hydration metrics

For descriptor-related hydration:

- number of holons fetched
- batch sizes
- cache miss rates
- per-trust-channel latency
- per-trust-channel failure rate
- prefetch usefulness
- over-fetch rate
- unused prefetched values

### Traversal pattern metrics

For common navigation paths:

- property co-access patterns
- relationship co-traversal patterns
- descriptor-to-descriptor path frequencies
- common expansion shapes
- likely next-hop relationships
- query execution contexts where these patterns occur

## Salience

Access frequency can serve as a rough proxy for local salience.

If a space frequently accesses a particular property or traverses a particular relationship, that suggests the property or relationship is important in that space's frame.

This does not mean frequency is the same as meaning. But it is a practical signal.

For example:

> The properties and relationships most often accessed by a space are likely to be among the most operationally salient for that space.

This salience signal can inform:

- UI defaults
- summary views
- card layouts
- query suggestions
- prefetch policies
- cache policies
- schema extension proposals
- descriptor evolution proposals

---

# 3. Trust-Channel-Scoped Batching

## Why batching should be scoped by trust channel

Remote references may point through different trust channels.

A collection of 100 holon references may be partitioned across several external spaces, each mediated by a different trust channel.

Therefore, batching should not simply aggregate all misses globally. It should group them by the trust channel through which they must be resolved.

The natural batching unit is:

> requests to the same trust channel under compatible execution constraints.

This preserves:

- membrane semantics
- trust-channel policy
- authorization boundaries
- backpressure isolation
- per-channel optimization
- local accountability

## Lightweight batching strategy

A relatively simple mitigation strategy is to give each trust channel its own request queue.

When a remote fetch is needed:

1. The runtime attempts local smart-link resolution.
2. If unresolved, it attempts local cache resolution.
3. If still unresolved, it enqueues the request on the relevant trust channel.
4. The trust channel batches queued requests.
5. The batch flushes when one of several conditions is met.

Flush conditions may include:

- the queue reaches a maximum batch size
- a maximum delay expires
- an urgent execution context requires immediate dispatch
- an explicit barrier is reached in query execution
- a dependent computation needs the result

This approach avoids requiring a full query optimizer.

It provides opportunistic batching while preserving lazy property access semantics.

## Urgency-sensitive batching

Batching policy can be influenced by execution context.

For example:

| Execution context         | Suggested behavior                         |
|---------------------------|--------------------------------------------|
| Interactive               | Minimize latency; flush quickly            |
| User waiting in real time | Flush immediately or with very short delay |
| Background task           | Allow longer batching windows              |
| Bulk analysis             | Prefer throughput over latency             |
| Maintenance task          | Batch aggressively                         |
| Prefetch                  | Batch opportunistically and deprioritize   |

The runtime does not need a full query planner to support this. It only needs contextual hints such as urgency, task type, or execution mode.

## Descriptor usage as input to batching

Descriptor usage metrics can improve batching decisions over time.

For example, if a usage record shows that a property is rarely resolved locally and often requires remote hydration, then the runtime may choose to bulk hydrate that property for a set of candidate holons rather than waiting for repeated scalar misses.

Likewise, if a relationship is almost always traversed after a given property is accessed, the runtime may prefetch targets for that relationship.

This allows MAP to begin with a lightweight mechanism and gradually become more adaptive.

---

# 4. Local Descriptor Extension

## Core idea

Descriptor usage should not be confused with descriptor extension.

A `DescriptorUsage` record describes how a space uses a descriptor.

A local descriptor extension describes how a space formally elaborates a descriptor for local purposes.

For example:

- `SCore` stewards `PersonType`
- `S1` defines `LocalPersonTypeExtension`
- `LocalPersonTypeExtension` extends `SCore:PersonType`
- `S1` uses the extension to add local properties or relationships

The local extension may define structure that is meaningful in `S1` but not part of the canonical descriptor stewarded by `SCore`.

## Possible local extensions

A local descriptor extension may add:

- local properties
- local relationships
- local validation rules
- local rendering hints
- local indexing hints
- local retrieval hints
- local classification links
- local semantic annotations
- local workflow-specific relationships

For example, a community space may extend a core `PersonType` descriptor with relationships relevant to local governance, such as:

- membership roles
- circles
- working groups
- consent agreements
- contribution histories
- local trust attestations

These additions may be highly meaningful in that space without belonging in the globally stewarded core descriptor.

## Distinction between usage and extension

The distinction can be summarized as:

> Usage records describe how a foreign descriptor is used locally.  
> Extension descriptors describe how a foreign descriptor is locally elaborated.

These are related, but they should not collapse into the same concept.

A space may use a descriptor heavily without extending it.

A space may extend a descriptor but rarely use the extension.

A space may use local extension usage metrics to decide whether an extension is operationally important.

---

# 5. Stewarded Descriptor Evolution

## Core idea

Local descriptor extensions and descriptor usage records can become evidence for upstream schema evolution.

If many spaces independently extend the same core descriptor in similar ways, that may indicate a missing property or relationship in the stewarded descriptor.

For example:

- many spaces extend `PersonType` with similar relationships
- usage records show those relationships are frequently traversed
- the terminology differs across spaces
- AI-assisted clustering recognizes the semantic similarity
- a proposal is created for the core stewardship space
- stewards evaluate whether the relationship should become part of the canonical descriptor

This creates a path from local adaptation to shared schema evolution.

## Evolution flow

A possible evolution flow:

1. A stewarding space publishes a descriptor.
2. Other spaces use the descriptor.
3. Using spaces accumulate `DescriptorUsage` records.
4. Some spaces define local descriptor extensions.
5. Usage metrics reveal which extensions are important locally.
6. Similar extensions appear across multiple spaces.
7. AI or human review clusters similar extension patterns.
8. A `DescriptorEvolutionProposal` is created.
9. The stewarding space reviews the proposal.
10. If accepted, the canonical descriptor evolves.
11. Spaces may migrate from local extensions to the updated canonical descriptor.

## Why these matter

These gives MAP a way to support schema evolution that is:

- adaptive
- evidence-informed
- locally grounded
- stewarded rather than centrally imposed
- responsive to actual usage
- able to detect convergence across diverse spaces

The stewarding space does not need to accept every local extension. But it can notice recurring needs and decide whether they belong in the shared descriptor.

---

# 6. Conceptual Model

## DescriptorUsage

A local record of how a descriptor is used within a space.

Under the MAP Type System v2.0 model, generic descriptor-usage relationships
should target `DescriptorRoot` when they are intentionally descriptor-agnostic.
Relationships that mirror inheritance semantics should remain constrained to the
same descriptor family rather than targeting `DescriptorRoot` generically.

Likely properties:

| Property                      | Purpose                                      |
|-------------------------------|----------------------------------------------|
| `descriptor_ref`              | Reference to the descriptor being used       |
| `using_space`                 | Space where the usage record lives           |
| `first_observed_at`           | When usage began                             |
| `last_observed_at`            | Most recent usage                            |
| `usage_count`                 | Aggregate count                              |
| `execution_context_breakdown` | Usage by interactive, background, bulk, etc. |
| `salience_score`              | Derived score based on local usage           |
| `confidence`                  | Confidence in derived metrics                |

Likely relationships:

| Relationship                 | Target                    |
|------------------------------|---------------------------|
| `UsesDescriptor`             | `DescriptorRoot`          |
| `HasPropertyUsageMetric`     | `PropertyUsageMetric`     |
| `HasRelationshipUsageMetric` | `RelationshipUsageMetric` |
| `HasHydrationMetric`         | `HydrationMetric`         |
| `HasTraversalPatternMetric`  | `TraversalPatternMetric`  |
| `InformsRetrievalPolicy`     | `RetrievalPolicy`         |

## PropertyUsageMetric

A usage metric for a property defined by or inherited through a descriptor.

Likely properties:

| Property                | Purpose                                       |
|-------------------------|-----------------------------------------------|
| `property_name`         | Property being observed                       |
| `access_count`          | Number of accesses                            |
| `local_hit_rate`        | Rate resolved locally                         |
| `smart_link_hit_rate`   | Rate resolved through smart link              |
| `cache_hit_rate`        | Rate resolved from cache                      |
| `remote_hydration_rate` | Rate requiring remote fetch                   |
| `average_latency_ms`    | Average resolution latency                    |
| `salience_score`        | Derived local importance                      |
| `prefetch_candidate`    | Whether this property is a prefetch candidate |

## RelationshipUsageMetric

A usage metric for a relationship defined by or inherited through a descriptor.

Likely properties:

| Property                       | Purpose                                           |
|--------------------------------|---------------------------------------------------|
| `relationship_name`            | Relationship being observed                       |
| `traversal_count`              | Number of traversals                              |
| `average_target_count`         | Average number of targets                         |
| `local_target_hit_rate`        | Rate targets resolved locally                     |
| `remote_target_hydration_rate` | Rate targets requiring remote hydration           |
| `average_latency_ms`           | Average traversal latency                         |
| `salience_score`               | Derived local importance                          |
| `prefetch_candidate`           | Whether this relationship is a prefetch candidate |

## HydrationMetric

A usage metric for hydration behavior associated with descriptor usage.

Likely properties:

| Property             | Purpose                                |
|----------------------|----------------------------------------|
| `trust_channel_ref`  | Trust channel involved                 |
| `remote_fetch_count` | Number of remote fetches               |
| `batch_count`        | Number of batches                      |
| `average_batch_size` | Average number of requests per batch   |
| `average_latency_ms` | Average batch latency                  |
| `overfetch_rate`     | Rate of fetched values not used        |
| `prefetch_hit_rate`  | Rate prefetched values were later used |

## DescriptorExtension

A local descriptor that extends a descriptor stewarded elsewhere.

Because extension semantics are TypeKind-specific in v2.0, the relationship
that identifies the stewarded descriptor being extended should target a
descriptor of the same family as the local extension rather than
`DescriptorRoot` generically.

Likely relationships:

| Relationship         | Target                   |
|----------------------|--------------------------|
| `ExtendsDescriptor`  | same-family descriptor   |
| `AddsProperty`       | `PropertyDescriptor`     |
| `AddsRelationship`   | `RelationshipDescriptor` |
| `HasLocalValidation` | `ValidationRule`         |
| `HasUsage`           | `DescriptorUsage`        |

## DescriptorEvolutionProposal

A proposal to modify a stewarded descriptor based on local usage or extension evidence.

Likely relationships:

| Relationship                   | Target                   |
|--------------------------------|--------------------------|
| `ProposesChangeTo`             | `DescriptorRoot`         |
| `SupportedByUsage`             | `DescriptorUsage`        |
| `SupportedByExtension`         | `DescriptorExtension`    |
| `ProposesPropertyAddition`     | `PropertyDescriptor`     |
| `ProposesRelationshipAddition` | `RelationshipDescriptor` |
| `SubmittedTo`                  | `StewardingSpace`        |

---

# 7. Relationship Naming Sketch

Following the MAP pattern of fully qualified relationship names, candidate relationships might include:

| Source                        | Relationship                 | Target                    |
|-------------------------------|------------------------------|---------------------------|
| `DescriptorUsage`             | `UsesDescriptor`             | `DescriptorRoot`          |
| `DescriptorUsage`             | `HasPropertyUsageMetric`     | `PropertyUsageMetric`     |
| `DescriptorUsage`             | `HasRelationshipUsageMetric` | `RelationshipUsageMetric` |
| `DescriptorUsage`             | `HasHydrationMetric`         | `HydrationMetric`         |
| `DescriptorUsage`             | `HasTraversalPatternMetric`  | `TraversalPatternMetric`  |
| `DescriptorExtension`         | `ExtendsDescriptor`          | same-family descriptor    |
| `DescriptorExtension`         | `AddsProperty`               | `PropertyDescriptor`      |
| `DescriptorExtension`         | `AddsRelationship`           | `RelationshipDescriptor`  |
| `DescriptorEvolutionProposal` | `ProposesChangeTo`           | `DescriptorRoot`          |
| `DescriptorEvolutionProposal` | `SupportedByUsage`           | `DescriptorUsage`         |
| `DescriptorEvolutionProposal` | `SupportedByExtension`       | `DescriptorExtension`     |

Using the fully qualified relationship naming convention, these may later become names such as:

| Fully qualified relationship                                                  |
|-------------------------------------------------------------------------------|
| `[DescriptorUsage]-USES_DESCRIPTOR->[DescriptorRoot]`                         |
| `[DescriptorUsage]-HAS_PROPERTY_USAGE_METRIC->[PropertyUsageMetric]`          |
| `[DescriptorUsage]-HAS_RELATIONSHIP_USAGE_METRIC->[RelationshipUsageMetric]`  |
| `[DescriptorUsage]-HAS_HYDRATION_METRIC->[HydrationMetric]`                   |
| `[DescriptorExtension]-EXTENDS_DESCRIPTOR->[SameFamilyDescriptor]`            |
| `[DescriptorEvolutionProposal]-SUPPORTED_BY_USAGE->[DescriptorUsage]`         |
| `[DescriptorEvolutionProposal]-SUPPORTED_BY_EXTENSION->[DescriptorExtension]` |
| `[DescriptorEvolutionProposal]-PROPOSES_CHANGE_TO->[DescriptorRoot]`          |

These names are provisional.

---

# 8. Runtime Implications

## Lazy semantics, vectorized execution

From the perspective of application code or query semantics, property access may remain scalar and lazy.

For example:

- access property value
- follow relationship
- resolve descriptor
- hydrate target if needed

But operationally, the runtime can detect repeated access patterns and vectorize resolution.

This means MAP can preserve a simple mental model while allowing the runtime to batch and prefetch behind the scenes.

In short:

> Property access is semantically scalar but operationally vectorizable.

## Usage-informed prefetch

Descriptor usage records can inform prefetch decisions.

For example:

- if property `display_name` is accessed in 95% of `PersonType` renderings, prefetch it
- if relationship `MemberOf` is traversed after `PersonType` access in 80% of cases, prefetch likely targets
- if a property frequently misses local smart-link resolution, bulk hydrate it earlier
- if a relationship usually crosses a particular trust channel, batch by that channel

This allows the runtime to improve gradually without introducing a heavyweight query optimizer.

## Avoiding premature query planning

A full query optimizer may eventually be useful, but it should not be required early.

The first step can be:

- trust-channel-scoped request queues
- urgency-sensitive batch windows
- descriptor usage metrics
- simple adaptive prefetch heuristics

This is lighter than a global cost-based query planner and better aligned with MAP's federated, trust-mediated architecture.

---

# 9. Design Principles

## Keep usage, extension, and evolution distinct

These concepts are related but not interchangeable.

| Concept                       | Lives in                      | Purpose                                  |
|-------------------------------|-------------------------------|------------------------------------------|
| `DescriptorUsage`             | Using space                   | Records how a descriptor is used locally |
| `DescriptorExtension`         | Extending space               | Adds local schema structure              |
| `DescriptorEvolutionProposal` | Proposing or stewarding space | Proposes canonical schema change         |

## Let local spaces adapt without fragmenting the commons

Local spaces should be free to adapt descriptors to their own purposes.

At the same time, recurring local adaptations should be visible as possible signals for commons-level schema evolution.

This avoids two extremes:

- rigid centralized schema control
- uncontrolled schema fragmentation

## Use observed behavior as evidence

Usage metrics should not automatically determine schema changes.

However, they provide useful evidence.

Repeated access, repeated extension, and repeated traversal patterns can help identify which schema elements are operationally important across contexts.

## Preserve stewarded authority

The stewarding space remains responsible for canonical descriptor evolution.

Local usage and extension patterns can inform stewardship, but they do not override it.

## Make adaptation incremental

MAP does not need to begin with a sophisticated query optimizer or schema evolution engine.

A practical path is:

1. Capture local descriptor usage.
2. Use usage metrics for local runtime adaptation.
3. Support local descriptor extension.
4. Detect recurring extension patterns.
5. Generate descriptor evolution proposals.
6. Let stewarding spaces evaluate and accept or reject proposals.

---

# 10. Open Questions

## Scope of DescriptorUsage

Should there be one `DescriptorUsage` per using space and descriptor pair?

Possible key:

    using_space + descriptor_ref

Or should usage be further scoped by:

- application
- dance
- execution context
- agent
- role
- trust channel
- time window

A likely answer is to start with one aggregate usage record and allow subordinate metric records to carry finer-grained dimensions.

## Privacy and disclosure

If local usage records become evidence for upstream schema evolution, what is shared?

Options include:

- raw usage records
- aggregated statistics
- anonymized patterns
- explicit proposals only
- human-curated summaries

Because usage patterns may reveal local priorities or workflows, disclosure should likely be explicit and promise-mediated.

## Metric decay

Should usage metrics decay over time?

Without decay, old usage patterns may dominate even after a space changes behavior.

Possible approaches:

- rolling windows
- exponential decay
- periodized metrics
- version-specific usage records
- separate historical and current salience scores

## Descriptor versioning

Usage records should likely be version-aware.

If `SCore:PersonType` evolves from version 1 to version 2, usage metrics may need to distinguish between:

- usage of v1
- usage of v2
- migrated usage
- extension compatibility across versions

## Local extension migration

If a local extension is later absorbed into the canonical descriptor, how should the local space migrate?

Possible migration paths:

- keep the local extension but mark it superseded
- map the local property to the canonical property
- convert local relationships to canonical relationships
- retain local aliases for compatibility
- generate migration proposals

---

# 11. Condensed Framing

The core pattern can be summarized as:

> A descriptor defines possible structure.  
> A descriptor usage records lived structure.  
> A descriptor extension formalizes local structure.  
> Descriptor evolution reconciles recurring local structure into stewarded shared structure.

Or, in runtime terms:

> Descriptor usage is where a space learns how it actually uses a descriptor.

Or, in schema-governance terms:

> Local adaptation becomes evidence for stewarded evolution.

This pattern gives MAP a way to combine:

- local autonomy
- adaptive runtime behavior
- trust-channel-aware retrieval
- schema extensibility
- evidence-informed commons stewardship
- gradual evolution of shared ontologies
