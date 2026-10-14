# Issue 816: Commit performance findings

**The largest demonstrated improvement comes from preparing less validation data.**
Database link reads dominate small Commit preparation. For large commits, repeatedly
interpreting the same descriptors also matters—even when every read is in memory.
Caching membership works within a guest call; it does not preserve prepared inputs
between calls.

Investigation: October 12–14, 2026, [map-holons issue #816](https://github.com/evomimic/map-holons/issues/816).
These findings describe experiments and recommendations, not new runtime contracts.
The [Commit validation specification](../validation/commit-validation-design-spec.md)
and [transaction specification](../transactions/transactions-design-spec.md) remain authoritative.

## What we measured

The primary workload creates one VisualizerUsage with a Key and four relationships:
DescribedBy, OwnedBy, UsesVisualizer, and ForSubjectType. Commit timing excludes
bootstrap, staging, and endpoint-name resolution. Each measured variant completes
Commit and verifies persisted forward and inverse links.

| Repeated median | Standard path | Narrow ValidatorPackage | Also bypass ReadinessContext |
| --- | ---: | ---: | ---: |
| Complete Commit command | 13.85 s | 6.38 s | **4.33 s** |
| Validation-input construction | 13.06 s | 5.61 s | 3.58 s |
| Prepared content identities | 127 | 48 | 48 |
| Construction link queries | 420 | 201 | 126 |

The combined experiment reduced command time by **68.8%**, but still falls short of
one second. Each column represents one fresh conductor and three commits: one first
sample and two repeated samples. These are screening results, not production latency
percentiles. A logical link query differs from a backend call: one batched call can
contain several queries. [Measured comparison](evidence/2026-10-issue-816/construction-comparison.json).

## Prepare the validator, the subject, and the descriptor separately

The existing DescriptorPackage follows **Construct → Validate → Use**, but its
construction mixes three different needs:

| Need | Data that belongs to it |
| --- | --- |
| Validate a subject H | H's properties and relationships required by applicable checks |
| Interpret H's governing type Ht | Effective declarations, constraints, validation bindings, and explicitly needed supporting definitions |
| Validate Ht itself | Ht as a subject, including any separately required descriptor or Schema assessment |

The standard path reaches five Schemas although this instance has no affected Schema
assessment. ComponentOf, RuleOf, and DependsOn enlarge the graph without serving
an instance check here. Consumers request just one contract, three binding products,
and three constraint products; that identifies excess preparation, but does not
prove every other supporting definition is unnecessary.

The bounded ValidatorPackage follows relationships needed for the governing type's
instance contract, including inherited semantics and defaults. It avoids whole-Schema
and target-instance expansion. It also supplies an explicit dependency plan: otherwise,
a second broad walk in commitment scheduling would expand the graph again.

Subject retrieval needs the same discipline. For example, a HolonSpace's inverse Owns
collection may be large. Its existence alone should not cause full retrieval; an
applicable check must require it. The current evaluator does **not** implement full
relationship cardinality, endpoint-conformance, and collection-policy validation.
Preserving today's results is therefore not proof of complete future validation coverage.

## Readiness discovery is broader than this case requires

ReadinessContext independently resolves 51 distinct anchor keys through 57 saved-key
lookups. In the unversioned fixture, those cause 57 keyed Owns queries, 57 Successor
queries, and nine additional contract queries: **123 link queries** before package
construction. These are Commit costs, separate from the Loader's earlier reference resolution,
which checks staged collections first.

Only five of the 23 built-in rule identities apply to VisualizerUsage. Applicable
rules are already reachable through the descriptor's effective ValidationBindings.
The experiment uses those references and rule-key strings to dispatch Rust handlers,
with category and family inputs obtained from the encountered graph. It performs
no independent saved-key lookup. Tested results match, and the readiness-only trial
reduces command time from 13.99 s to 12.22 s.

Handler recognition does not establish descriptor validity or authority. Generalization
needs unfamiliar-family, malformed-input, and competing-update coverage, plus versioned
dispatch keys. Existing governing-contract checks remain; prior validity is not assumed.

## Real database reads explain the synthetic/Commit discrepancy

A later capture separates construction time without double-counting nested work: **12.74 of 13.66 seconds (93.3%)** is inside Holochain link-read calls.
Those spans include host-call overhead, database work, and waiting; they do not isolate
SQL alone. Node retrieval, decoding, binding, and remaining preparation are smaller
in this workload. Later controls did not reproduce the initial reported 20.6 seconds literally. [Individual samples and accounting](evidence/2026-10-issue-816/commit-measurements.json).

The isolated retrieval benchmark used a much smaller store. With 512 source links
and 16 requested relationships, Single Prefix Retrieval took about **34 ms**, versus
**8.75 ms** for Single Scan. That did not predict populated-store Commit cost.

In the actual bootstrap database, each authored and DHT store contains 11,472 Action
rows and 34,413 DhtOp rows. The observed query plan selects operations by validation
status, joins actions by their hash, and only then filters by source and tag. Even a
query returning zero links takes roughly **14 ms against one populated database**;
a complete link retrieval can query both stores. Few matching links therefore do
not imply little database work.

Adding an index on `Action.base_hash` alone did not change the selected plan or
demonstrate a Commit speedup: repeated command medians were 15.39 s for control and 15.78 s
with the index. A source-first plan or different planner statistics remains an
unmeasured possibility. [Query plans and SQL samples](evidence/2026-10-issue-816/query-plans.json).

## Retrieval consolidation helps; there is no proven universal threshold

Use these terms consistently:

- **Single Prefix Retrieval:** one query restricted to one relationship tag prefix.
- **Batched Prefix Retrieval:** several prefix queries submitted in one host call.
- **Single Scan:** retrieve a source's SmartLinks once and partition the results into requested relationships.

Prefix selectivity means matching links divided by all source links. That fraction and the number of requested relationships affect the crossover.
Prefix retrieval can win for sparse demand; Single Scan often wins for several
relationships. Neither predicts the overhead of queries that examine the whole store.
Batching prefix queries produced little consistent time saving in the synthetic
trial. It reduces host calls but retains separate queries.

Removing package prefetch without narrowing demand was worse: backend calls rose
from **380 to 1,317**. Preparation can populate multiple membership maps from one
retrieval, including empty maps. The increase was not evidence of lost empty-result
caching. That experiment was rejected.

Strategy selection itself costs time. Count probes consumed **4.05 seconds** in the
exclusive control. A trial that removed them and chose Single Scan for four or more
missing names lowered repeated construction from 13.66 s to 7.91 s. It changed both
the probe and strategy, so the saving cannot be attributed to either alone. The
original heuristic was restored; no general cutoff was established.
[Retrieval comparisons](evidence/2026-10-issue-816/retrieval-comparison.csv),
[earlier prefetch result and retention limits](evidence/2026-10-issue-816/earlier-prefetch-experiment.json).

## Membership caching works; descriptor interpretation repeats

Write preparation resolves an inverse name, then traverses again to obtain forward
and inverse target-binding policies. Cache observations show:

| Workload | Inverse-name resolutions | Membership backend calls | Node retrieval attempts |
| --- | ---: | ---: | ---: |
| One VisualizerUsage | 4 | 9 | 5 |
| Ten VisualizerUsages in one Commit | 40 | **9** | **5** |
| Bootstrap: 957 candidates | 4,706 | **0** | **0** |

The nine reads are four HasInverse and five Extends lookups. No source/name pair
misses twice within these commits; no freshness bypass occurs. Subsequent
target-binding passes make zero backend reads. Bootstrap uses staged data, so its zero calls represent in-memory
access, not saved-cache hits.

Repeated interpretation still costs time: inverse-name and target-binding passes
total approximately **1.13 seconds** for ten subjects: 375 ms in four inverse-name
passes that include first-use retrieval, 522 ms in 36 inverse-name passes without
backend reads, and 230 ms in 40 target-binding passes without backend reads. The
375 ms includes traversal as well as retrieval; internal steps were not separately
timed. Bootstrap's passes total **3.06 seconds**. This suggests reusing interpreted write policies within a Commit,
rather than adding another membership cache.
[Cache audit](evidence/2026-10-issue-816/inverse-cache-audit.json).

For one subject in the warm-probe capture, relationship persistence takes about
757 ms: inverse-name resolution accounts for 384 ms and existing-SmartLink expansion
for 266 ms. Actual action creation totals only 5 ms. These are nested components,
not independent totals, and action-call timing does not measure all durable-write cost.

## Cross-Commit reuse requires architectural support

The warm probe keeps one package, retained cached content, and transaction-bound
references alive within one guest invocation, then repeats checks on the unchanged
subject with fresh findings. Average pass time is approximately **28 ms**, with zero
backend reads and matching findings and rule coverage.

Combining that span with measured non-validation command time gives an optimistic
**811 ms estimate**, not an observed cached Commit. It omits cross-transaction rebinding,
applicability checks, and cold subject reads. Stateless guests cannot retain these
in-memory objects between Commit calls. Practical reuse would need host-supplied or
persisted reusable products, with explicit versioning and trust checks, or multiple
commits grouped into one invocation. [Probe and model](evidence/2026-10-issue-816/warm-reuse-model.json).

## Two follow-up enhancement issues

**Narrow DescriptorPackage to ValidatorPackage.** Replace the broad preparation
scope with the contract needed to validate instances of the governing type. Keep
subject preparation, governing-descriptor validation, and affected-Schema assessment
separate; carry the narrower dependencies into scheduling. Generalize the bounded
prototype while preserving applicable checks and errors. This has the largest
measured benefit: 13.85 s to 6.38 s for the tested instance.

**Retire ReadinessContext.** Replace independent, global anchor-key discovery with
inputs reached from the governing descriptor and applicable validation bindings,
and dispatch handlers by rule key. Generalize beyond VisualizerUsage while preserving
category/family checks and malformed or competing-update behavior. Combined with the
narrow package, the measured command reaches 4.33 s. These are separate enhancement
proposals; detailed implementation scope belongs in their GitHub issues.

Persistent materialized views are deferred. Both enhancements can proceed within
the existing guest architecture without requiring cross-Commit retention.

## Other investigation candidates

- **Try a Commit-local write-policy plan.** Resolve the inverse name and both target
  bindings together, once per effective governing descriptor and relationship in
  the same view of saved and staged changes. Preserve policy errors and replacement selection.
- **Improve populated-store retrieval.** Compare a source-first query plan against
  the current plan with identical results. Separately test cheaper strategy selection
  and Single Scan on representative sparse and dense stores. The index alone did not help.
- **Keep broader architectural options open.** Cross-Commit reuse needs explicit
  versioning, applicability, binding, and trust rules. Parallel modular commits also
  need module boundaries, dependency capture, planning, and host orchestration.
  Neither architecture nor its benefit was demonstrated by #816.

## Confidence and evidence

The bounded validation experiments preserved complete findings and coverage in
focused fixtures and matched six live outcomes, including correction/retry and the
existing missing-Key persistence error. They do not establish general equivalence
for all descriptor, Schema, relationship, or error cases. The full Sweettest suite
was not run. Experimental features remain opt-in; standard artifacts were restored.

Most real Commit variants use one process with two or three timed samples.
The synthetic retrieval trial uses three processes and six rounds per workload.
Builds, logging, store populations, and worktree changes are recorded; timings from
different captures should not be combined into one imaginary run. Independent
component medians need not sum to the median total.

The [evidence inventory](evidence/2026-10-issue-816/README.md) preserves measured samples,
query plans, correctness outcomes, provenance, and selected original markers.
It explicitly identifies historical summaries whose original captures were lost.
