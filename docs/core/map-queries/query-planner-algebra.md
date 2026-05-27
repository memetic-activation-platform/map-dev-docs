# Appendix: Declarative Planner Compatibility for OpenCypher and GQL (v1.3)

## Purpose

This document is future-facing appendix material for declarative query compatibility.

It explains how OpenCypher, and later GQL, can be planned and compiled into MAP `ExecutionPlan` holons without making Cypher's row-stream execution model the foundational MAP runtime substrate.

The normative MAP runtime model lives in:

- `query-arch.md`
- `simple-algebra-binding-model.md`
- `navigation-algebra.md`

The current MAP implementation target is the interactive route:

    HumanAgent gestures
      -> ExecutionPlan holon
      -> HolonCollection-centered execution

The future declarative route is:

    OpenCypher/GQL
      -> logical declarative plan
      -> descriptor-aware MAP planning
      -> ExecutionPlan holon
      -> HolonCollection-centered execution plus derived views where required

---

## 1. Compatibility Principle

Declarative compatibility means MAP can produce the correct observable semantics for supported OpenCypher/GQL queries.
It does not mean MAP must adopt Cypher's internal row-stream model as its core runtime carrier.

MAP's core execution model remains:

    HolonCollection -> Operation -> HolonCollection

where possible.

When declarative query semantics require correlation, null extension, grouping, path values, or multi-variable results, the planner may require derived views such as:

- pair projections
- partitioned collections
- traversal traces
- path collections
- row-oriented projections
- aggregation views
- binding-relation overlays

These derived views are compatibility and output structures.
They are not the default MAP runtime substrate.

---

## 2. Descriptor-Aware Planning Rule

The planner is not the semantic owner of property, relationship, or value/operator meaning.

Declarative planning must consume descriptor-backed semantics:

- structural lookup from effective descriptors
- relationship-channel legality from relationship descriptors
- property-to-value semantics from property descriptors
- operator compatibility from value descriptors

This prevents a separate query-only semantic system from forming.

For example:

- `MATCH (b:Book)-[:AUTHORED_BY]->(a:Author)` resolves `Book`, `AUTHORED_BY`, and `Author` through descriptor-backed structure.
- `WHERE b.published_year > 2000` validates the property and comparison operator through descriptor-backed value semantics.
- an inverse traversal must preserve declared and inverse relationship meaning.

---

## 3. Declarative Logical Vocabulary

OpenCypher engines commonly reason with a row-stream logical vocabulary.
MAP may use that vocabulary as a planner analysis layer without adopting it as the physical runtime substrate.

Reference logical concepts include:

- record stream
- record or binding row
- scan / seek
- expand
- filter
- project
- aggregate
- distinct
- sort
- skip / limit
- join
- apply
- optional
- semi-apply / anti-semi-apply
- union
- path construction
- eager barrier
- produce results

These concepts help describe declarative semantics and optimization opportunities.
They should compile into operations recorded by MAP `ExecutionPlan` holons and derived views.

---

## 4. Mapping To MAP ExecutionPlan Holons

The planner should translate declarative logical operators into MAP-native execution where possible.

| Declarative concept | MAP target |
| --- | --- |
| label/type scan | `SeedHolons` with descriptor-backed type filtering |
| node seek | `SeedHolons` or specialized seed scope |
| fixed relationship expand | `Expand` over a named relationship channel |
| property filter | `Filter` with descriptor-backed predicate semantics |
| projection | `Project` into a derived view |
| sort | `OrderBy` over `HolonCollection` or derived view |
| skip / limit | `Skip` / `Limit` over the current ordered value |
| distinct | `Distinct` over identity, or derived distinctness where needed |
| path variable | derived traversal trace or path collection |
| `RETURN` | derived output view |

When a declarative operator cannot be represented by the initial interactive algebra, it belongs to future planner work rather than the initial navigation algebra.

Examples:

- `Apply` may require a correlated execution branch.
- `Optional` may require null-extension semantics.
- `Aggregate` may require grouping views.
- `Union` may require compatibility checks between result shapes.
- `Join` may require a binding-relation overlay or planner-specific derived view.

---

## 5. Where Richer Correlation Becomes Necessary

The initial `Expand` operation can produce a flat target `HolonCollection`.
That is sufficient for many interactive gestures.

Declarative queries often require observable correlation.

Example:

    MATCH (b:Book)-[:AUTHORED_BY]->(a:Author)
    RETURN b, a

The result must preserve each `(Book, Author)` association.
MAP may derive that association from:

- `ExecutionPlan` holon topology
- operation input and output variables
- `RelationshipMap`
- `RelationshipCache`
- traversal provenance
- transaction or snapshot state

The planner should introduce a derived correlation view only when semantics require it.

Common triggers:

- returning multiple variables from the same pattern
- filtering on both source and target variables
- grouping targets by source
- preserving duplicate path semantics
- optional matches with missing targets
- variable-length paths
- joins between separately produced bindings
- aggregations over correlated variables

---

## 6. Apply And Optional

OpenCypher relies heavily on correlated execution.

Reference concepts:

- `Apply`: for each left binding, run a right plan with left variables available
- `Optional`: left outer apply with null extension when the right side has no match
- `SemiApply`: keep left binding when the right side exists
- `AntiSemiApply`: keep left binding when the right side does not exist

MAP should not introduce these into the initial navigation algebra.

Future planner support may compile them into:

- graph-shaped `ExecutionPlan` holon branches
- derived binding-relation overlays
- partitioned collection views
- optional/null result projections

The important rule is that the resulting observable semantics match the declarative query while preserving MAP's holon-centered execution model where possible.

---

## 7. Aggregation And Distinct

Aggregation is a derived-view concern in MAP.

Simple interactive navigation may use `Distinct` over holon identity.
Declarative aggregation needs richer grouping semantics.

Examples:

    MATCH (b:Book)-[:AUTHORED_BY]->(a:Author)
    RETURN b, count(a)

This requires grouping authors by book.
MAP can derive that view from correlation structures rather than making grouped row streams foundational.

Future planner work should define:

- grouping-key semantics
- aggregate function semantics
- null handling
- ordering of aggregate output
- descriptor-backed value/operator compatibility

---

## 8. Path Semantics

Path values are derived traversal traces.
They are not primitive runtime carriers in the initial MAP algebra.

Declarative path queries may require materialized path-observable results.

Examples:

- returning a path variable
- filtering by path length
- evaluating path predicates
- explaining traversal provenance

Future planner work may introduce derived path views using:

- `ExecutionPlan` holon traversal structure
- relationship-channel names
- operation identities
- source and target variables
- transaction or snapshot state

---

## 9. Barriers, Updates, And Mutation

OpenCypher engines include barriers and update operators such as:

- eager materialization barriers
- create
- merge
- set / remove
- delete
- foreach

These are out of scope for the initial MAP navigation algebra.

If MAP later supports declarative mutations, they must be reconciled with MAP command, transaction, validation, and undo/redo semantics.
They should not be imported directly from Cypher execution catalogs as host behavior.

---

## 10. Optimization Surface

Future declarative optimization may include:

- predicate pushdown
- operation reordering
- expand/filter fusion
- branch sharing
- common subplan reuse
- derived-view elimination
- cost-based planning
- distributed planning

Optimization must preserve descriptor semantics and relationship-channel meaning.

An optimized plan is a derived equivalent artifact.
The original interactive or declarative source should remain distinguishable for provenance and explanation.

---

## 11. Non-Normative Operator Inventory

The following OpenCypher-style operator families remain useful as reference vocabulary:

- scans and seeks
- expand
- filter
- projection
- unwind
- aggregate
- distinct
- sort
- top-N
- skip / limit
- hash join
- node hash join
- cartesian product
- apply
- optional
- semi-apply
- anti-semi-apply
- union
- path construction
- procedure calls
- eager barriers
- produce results

This list is an implementation-analysis aid.
It is not the normative MAP operation set.

---

## Summary

OpenCypher and GQL compatibility should compile declarative semantics into MAP `ExecutionPlan` holons.

MAP should preserve its simple runtime center:

    HolonCollection -> Operation -> HolonCollection

and introduce richer correlation, binding, path, aggregate, or row-oriented views only when the declarative semantics or output contract requires them.
