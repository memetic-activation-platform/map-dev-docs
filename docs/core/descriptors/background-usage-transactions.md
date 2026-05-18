# Background Usage Transactions

## Summary

Usage statistics and personalization updates should not be treated as part of the user's primary semantic transaction.

Reads, traversals, and visual gestures may generate adaptive usage signals, but these signals do not need the same transactional guarantees as intentional domain changes.

This suggests a separate transaction pattern:

> User transactions commit semantic changes.  
> Background usage transactions commit adaptive signals.

This distinction allows MAP and DAHN to gather usage and personalization data without turning every read or gesture into a synchronous persistent write.

---

# 1. Core Insight

Every read and every visualization gesture can potentially produce a usage update.

Examples include:

- reading a property value
- traversing a relationship
- navigating from one holon type to another
- selecting a visualizer
- moving a property higher in a form
- hiding or revealing a property
- expanding a relationship
- embedding a target holon within another visualization
- choosing a collection visualizer
- reusing or changing a prior personalization

If every such event required an immediate write to persistent storage, the usage system would create excessive transactional overhead.

Instead, usage updates should be treated as adaptive side effects.

They may be:

- buffered
- coalesced
- aggregated
- delayed
- committed independently
- discarded under pressure
- flushed opportunistically

The cost of occasionally losing usage statistics or recent personalization hints is acceptable.

The cost of blocking or burdening the user's primary transaction is not.

---

# 2. User Transactions vs Usage Transactions

## User transactions

A user transaction contains intentional semantic changes.

Examples:

- creating holons
- updating domain properties
- adding or removing relationships
- creating local descriptor extensions
- changing schema-relevant structure
- accepting or rejecting proposals
- changing commitments
- modifying governance state
- performing explicit application-level writes

These changes should retain normal transaction guarantees.

They are part of the domain meaning of the user's action.

## Usage transactions

A usage transaction contains adaptive signals generated as side effects of interaction or execution.

Examples:

- descriptor access counts
- property access frequency
- relationship traversal frequency
- local cache hit statistics
- smart-link hit statistics
- remote hydration statistics
- visualizer selections
- property ordering gestures
- hide or reveal gestures
- relationship expansion gestures
- embedding affinity metrics
- prefetch effectiveness metrics
- collection visualizer usage
- contextual visualization preferences

These updates do not need to commit in the same transaction as the user's semantic action.

They can be committed later by infrastructure-controlled background transactions.

---

# 3. Transaction Boundary

The core boundary is:

> Usage, statistics, and personalization updates are not part of the user's semantic transaction.

They are adaptive metadata.

They may influence future experience, but they should not determine whether the current user action succeeds.

This leads to three distinct categories:

| Update type | Transaction behavior |
| --- | --- |
| Domain data changes | User-controlled, durable, explicit |
| Ontological or schema extensions | User-controlled, durable, explicit |
| Personalization preferences | Background transaction, durable enough |
| Usage statistics | Background transaction, lossy and coalesced |
| Runtime optimization metrics | Background transaction, highly lossy and coalesced |

The phrase **durable enough** is useful for personalization preferences.

Personalization matters more than raw statistics, but it is usually less critical than a domain edit or schema extension.

Losing the last gesture or two is acceptable.

Losing an intentional local schema extension is not.

---

# 4. Separate Treatment for Schema Extensions

Local schema extensions should not be treated as usage statistics.

A local descriptor extension is a semantic act.

It changes the local ontology or type model by adding structure such as:

- local properties
- local relationships
- local validation rules
- local rendering semantics
- local descriptor refinements

These changes should be committed through normal user-controlled transactions.

They are not safely lossy.

This document is concerned only with:

- usage statistics
- personalization preferences
- visualization metrics
- retrieval metrics
- adaptive runtime hints

It does not apply to ontological extensions.

---

# 5. Runtime Pattern

A plausible runtime architecture is:

1. A user transaction executes normally.
2. Reads, traversals, visual gestures, and runtime events emit lightweight usage observations.
3. Usage observations are routed to an in-memory usage accumulator.
4. The accumulator coalesces and aggregates observations.
5. The infrastructure periodically opens a background usage transaction.
6. Aggregated usage updates are committed.
7. Failed usage commits may be retried, dropped, or merged into a later attempt depending on policy.

This keeps the user's primary transaction clean.

The primary transaction does not need to wait for usage persistence.

---

# 6. Usage Accumulator

## Purpose

The usage accumulator absorbs high-frequency usage signals and converts them into lower-frequency aggregate updates.

It exists to avoid one persistent write per read or gesture.

## Possible aggregation keys

Usage events may be coalesced by keys such as:

- agent
- space
- descriptor
- descriptor version
- property
- relationship
- visualizer
- value visualizer
- collection visualizer
- trust channel
- execution context
- context signature
- application or dance
- time window

## Examples

Instead of writing 100 separate property access events, the accumulator may update one aggregate:

    Property X on Descriptor D was accessed 100 times in Context C.

Instead of writing 20 separate relationship traversal events, the accumulator may update one aggregate:

    Relationship R from Descriptor D was traversed 20 times, with 14 remote hydrations through Trust Channel T.

Instead of writing every property reorder gesture, the accumulator may keep the latest stable preference:

    For Agent A, Property P is now ranked higher in the default visualization of Descriptor D.

---

# 7. Commit Policy

The infrastructure should control usage commit points.

Possible flush triggers:

- elapsed time
- number of accumulated events
- memory pressure
- idle period
- end of session
- shutdown
- application-defined checkpoint
- switch of active space
- switch of active agent
- completion of a dance
- explicit best-effort flush request

Different usage categories may have different policies.

## Usage statistics

Usage statistics can be highly lossy.

They can be:

- sampled
- aggregated
- delayed
- dropped under pressure
- recomputed over time

## Personalization preferences

Personalization preferences should be more durable than raw statistics.

They can still be written asynchronously, but the system may prefer:

- shorter flush intervals
- best-effort flush on session end
- preservation of latest stable value
- conflict resolution by recency or context

## Runtime optimization metrics

Runtime optimization metrics can be the most lossy.

Examples include:

- prefetch hit rate
- cache miss ratio
- hydration latency
- trust-channel batch size
- overfetch rate

These metrics can be useful but should never become part of the critical path.

---

# 8. Bootstrapping Question

A key design question is:

> Who owns the usage accumulator and the background usage transactions?

Likely candidates include:

- `TransactionContextFactory`
- `ExecutionContext`
- `SpaceRuntime`
- `UsageRuntime`
- DAHN visualization/session runtime
- a broader application runtime layer

The user transaction itself should probably not own usage commit policy.

A cleaner separation is:

> `TransactionContext` emits usage observations.  
> `UsageRuntime` accumulates them.  
> `UsageRuntime` opens background transactions to persist them.

This keeps the transaction model clean while allowing usage collection to remain integrated with execution.

---

# 9. Multiple Transactions in Flight

The current transaction model appears compatible with multiple transactions being active independently.

This supports the distinction between:

- a foreground user transaction
- one or more background usage transactions

The foreground transaction represents intentional work.

The background usage transaction represents adaptive bookkeeping.

These should not block each other unless explicitly required by policy.

For example:

- a failed usage commit should not roll back a user transaction
- a user transaction should not wait for usage metrics to persist
- usage writes should not be able to invalidate the user's semantic write
- usage aggregation may lag behind user-visible interaction

---

# 10. Failure Semantics

Usage persistence should have relaxed failure semantics.

Possible policies:

| Failure type | Possible response |
| --- | --- |
| transient write failure | retry later |
| accumulator overflow | drop low-priority metrics |
| shutdown before flush | lose recent usage |
| conflict on aggregate update | merge or retry |
| stale personalization write | prefer latest timestamp or context |
| unavailable usage store | disable usage persistence temporarily |

The guiding principle is:

> Usage writes should never endanger semantic writes.

---

# 11. Event Records vs Aggregate State

This pattern does not require strong event sourcing.

The system does not need to preserve every usage event as durable history.

Instead, individual gestures and reads may be folded into aggregate state.

For example:

- access counts
- salience scores
- affinity scores
- latest visualization preference
- rolling averages
- decayed metrics
- contextual rankings

This suggests:

> individual gestures become aggregate state, not necessarily durable event records.

That is appropriate for adaptive telemetry.

It is also more privacy-preserving than retaining raw interaction histories by default.

---

# 12. Privacy and Sovereignty

Usage and personalization data may reveal sensitive information about:

- attention
- priorities
- workflows
- relationships
- local practices
- community concerns
- cognitive patterns
- operational dependencies

Therefore, usage persistence and aggregation should remain sovereignty-aware.

Relevant questions:

- Is the usage data stored only locally?
- Is it shared with a community space?
- Is it shared with a descriptor stewarding space?
- Is it aggregated before sharing?
- Is raw event history ever retained?
- Can the agent or space opt out?
- Can different metric categories have different sharing policies?

A likely default:

> Persist local adaptive usage data locally, and share only aggregated or explicitly approved reports with other spaces.

---

# 13. Relationship to Descriptor Usage

Background usage transactions are a persistence mechanism for descriptor usage records.

Descriptor usage records may accumulate metrics such as:

- property access frequency
- relationship traversal frequency
- smart-link hit rate
- cache hit rate
- remote hydration rate
- trust-channel latency
- prefetch usefulness

Those metrics should usually be written through background usage transactions rather than through the user's foreground transaction.

This avoids turning each descriptor read into a synchronous write.

---

# 14. Relationship to Visualization Usage

Background usage transactions are also a persistence mechanism for DAHN-style visualization usage.

Visualization usage records may accumulate metrics such as:

- visualizer selection
- property ordering
- hide and reveal gestures
- inline expansion choices
- embedding preferences
- relationship navigation frequency
- property salience
- relationship affinity
- collection visualizer preferences

These should usually be persisted asynchronously.

A visual gesture can influence future defaults without becoming part of the user's semantic transaction.

---

# 15. Design Principles

## Keep semantic writes authoritative

User-controlled transactions should own domain and ontology changes.

Usage transactions should not interfere with them.

## Keep usage writes off the critical path

Usage writes should not block user interaction or query execution.

## Prefer aggregation over event retention

Store aggregate adaptive state unless raw event history is explicitly required.

## Treat usage data as lossy

Most usage metrics can tolerate loss.

This justifies buffering, coalescing, sampling, and delayed commits.

## Treat personalization as durable enough

Personalization preferences should be more durable than raw usage counters, but still need not be synchronized with every foreground transaction.

## Keep schema extensions separate

Local schema extensions are semantic changes, not usage telemetry.

They require normal transaction guarantees.

## Let infrastructure control commit points

Usage commit timing should be governed by runtime policy, not by every individual read or gesture.

---

# 16. Condensed Framing

The central pattern is:

> Every read and gesture may produce an adaptive signal, but not every signal should become an immediate write.

Or:

> The user transaction is semantic.  
> The usage transaction is adaptive.

Or:

> Usage writes are infrastructure-managed, lossy, coalesced, and independent of the user's primary transaction.

This gives MAP and DAHN a practical path for supporting adaptive behavior without overwhelming the transaction model.