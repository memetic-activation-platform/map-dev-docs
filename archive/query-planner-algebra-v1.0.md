# Query Planner Algebra for OpenCypher-Compatible Property Graphs

This document defines a practical, implementation-informed logical algebra for property graph query planning, aligned with real-world OpenCypher execution engines while remaining optimizer-friendly and structurally coherent. It standardizes a small set of core operands (RecordStream, Record, Expression, GraphOperand) and organizes operators into logical categories (scan, expand, filter, join, aggregate, apply, update, etc.) suitable for planner construction and cost-based optimization. The algebra abstracts away physical execution strategies while preserving compatibility with production Cypher engines and providing a stable foundation for MAP’s dance abstraction and declarative query compilation.

This document distills the practical logical operators used by OpenCypher execution engines (e.g., Neo4j, Memgraph, Cypher-on-Spark) into a clean algebra suitable for:

1. A logical planner layer
2. A cost-based optimizer
3. A user-facing “dance” abstraction in MAP
4. Serialization to OpenCypher (and eventually GQL)

The emphasis is on implementation reality rather than purely theoretical graph algebra, while preserving sound algebraic structure.

---

# 1. Core Operand Model

Modern Cypher engines converge on a small set of operator inputs and outputs. These should be treated as **standard ports** in the MAP Algebra.

## 1.1 RecordStream

A stream (multiset / bag semantics) of Records.

This is the universal input/output of logical operators.

Signature:
```
RecordStream<Header>
```

Characteristics:
- Ordered or unordered depending on pipeline stage
- May be lazily evaluated
- May be materialized (via Eager barrier)
- Supports null values (three-valued logic)

In MAP:
- `HolonStream` is a specialization of `RecordStream` where at least one variable is a Holon.

---

## 1.2 Record

A binding of variable → value.

Example:
```
{ h: Holon, r: HolonRelationship, h2: Holon }
```

Value types:
- Node (Holon)
- Relationship (HolonRelationship)
- Path
- Scalar (string, integer, boolean, float)
- List
- Map
- Temporal
- Null

---

## 1.3 GraphOperand (Optional but Forward-Looking)

Some Cypher implementations support graph-returning queries.

Signature:
```
GraphOperand
```

Useful for:
- Subgraph derivation
- Graph-to-graph analytics
- Multi-graph pipelines

In MAP:
- `HolonGraph`

---

## 1.4 Expression / Predicate

Side-effect-free computations evaluated per record.

Used in:
- Filter
- Join conditions
- Projection
- Aggregation

Uses three-valued logic:
- true
- false
- null

---

## 1.5 Schema / Header

Each RecordStream carries a header describing:
- Variables
- Their types/kinds
- Optional nullability

Planners propagate headers through operator trees.

---

# 2. Logical Operator Catalog

Operators consume and emit RecordStreams unless noted otherwise.

---

# A. Access / Scan Operators

Seed the pipeline.

## AllNodesScan(label?)

```
∅ → [n]
```

Emit all nodes (optionally constrained by label).

Physical:
- Heap scan
- Label store scan

---

## NodeIndexSeek(label, property, op, value)

```
∅ → [n]
```

Index-based retrieval.

Supports:
- Equality
- Range
- Prefix

---

## RelationshipTypeScan(type)

```
∅ → [r]
```

Scan relationships by type.

---

## RelationshipIndexSeek(type, property, op, value)

```
∅ → [r]
```

Index-based relationship retrieval.

---

# B. Expand (Traversal)

Core graph navigation primitive.

## Expand(kind, n, r, m, type, dir, lenSpec?)

```
[n] → [n, r?, m]
```

From bound node `n`, emit adjacent nodes.

Parameters:
- kind: All | Into
- type: relationship type
- dir: outgoing | incoming | undirected
- lenSpec: fixed length or min..max

Variable-length expansions are implemented with stateful traversal.

Physical:
- Adjacency iteration
- Index nested-loop
- BFS/DFS with pruning

---

# C. Filter

## Filter(predicate)

```
[X] → [X]
```

Keep records where predicate evaluates to true.

Null and false are discarded.

Pushdown-friendly.

---

# D. Projection & Computation

## Project(expressions...)

```
[X] → [Y]
```

- Rename variables
- Compute new expressions
- Drop unused variables

---

## Unwind(listExpr AS x)

```
[X] → [X, x]
```

Turn a list into multiple rows.

---

# E. Aggregation & Distinct

## Aggregate(groupKeys, aggregateFns)

```
[X] → [groupKeys, aggregates...]
```

Physical:
- Hash aggregate
- Sort aggregate

---

## Distinct(keys)

```
[X] → [keys]
```

Deduplication.

Equivalent to Aggregate without aggregate functions.

---

# F. Ordering & Pagination

## Sort(orderSpec)

```
[X] → [X]
```

---

## TopN(orderSpec, N)

```
[X] → [X]
```

Partial sort optimization.

---

## Skip(k)

```
[X] → [X]
```

---

## Limit(k)

```
[X] → [X]
```

Pushdown-friendly.

---

# G. Join & Apply Family

Cypher relies heavily on Apply variants for correlated execution.

---

## CartesianProduct

```
[L], [R] → [LR]
```

Cross join.

---

## HashJoin(condition)

```
[L], [R] → [LR]
```

Equi-join.

---

## NodeHashJoin(variable)

Specialized join on node identity.

---

## Apply(rightPlan)

```
[L] → [LR]
```

For each left row, execute right plan with bound variables.

Equivalent to correlated nested loop.

---

## Optional(rightPlan)

```
[L] → [LR?]
```

Left outer apply.

Implements OPTIONAL MATCH.

---

## SemiApply(rightPlan)

```
[L] → [L]
```

Keep rows where right yields at least one match.

Implements EXISTS.

---

## AntiSemiApply(rightPlan)

```
[L] → [L]
```

Keep rows where right yields no matches.

Implements NOT EXISTS.

---

# H. Path & Pattern Utilities

## PathConstruction(vars → path)

```
[X] → [X, path]
```

Materialize path value.

---

## PatternPredicate(pattern)

Logically compiles to SemiApply / AntiSemiApply.

---

# I. Set Operations

## UnionAll

```
[A], [B] → [C]
```

---

## UnionDistinct

```
[A], [B] → [C]
```

Followed by deduplication.

---

# J. Update Operators

Side-effecting but logically composable.

---

## Create(spec)

```
[X] → [X, newBindings]
```

---

## Merge(pattern, onMatch?, onCreate?)

Find-or-create semantics.

Often decomposes into:
- SemiApply existence check
- Conditional Create

---

## Set / Remove

Mutate properties or labels.

---

## Delete / DetachDelete

Remove entities.

---

## Foreach(var IN list | updates)

Iterative side-effects.

---

# K. Subqueries & Procedures

## CallSubquery(plan)

Encapsulated logical subtree.

Usually implemented via Apply.

---

## ProcedureCall(name, args)

External computation producing RecordStream.

---

# L. Runtime Barriers

## Eager

```
[X] → [X]
```

Materialization barrier.

Used to:
- Separate updates
- Prevent interference
- Control memory

---

## ProduceResults(vars)

Final output operator.

---

# 3. Minimal Logical Signatures

A planner-friendly minimal set:

- AllNodesScan
- NodeIndexSeek
- RelationshipTypeScan
- Expand(All | Into)
- Filter
- Project
- Unwind
- Aggregate
- Distinct
- Sort
- TopN
- Skip
- Limit
- HashJoin
- NodeHashJoin
- CartesianProduct
- Apply
- Optional
- SemiApply
- AntiSemiApply
- UnionAll
- UnionDistinct
- Create
- Merge
- Set / Remove
- Delete / DetachDelete
- Eager
- ProduceResults

With these operators, virtually all OpenCypher queries can be expressed.

---

# 4. MAP Alignment

In MAP:

- Holon ≅ Node
- HolonRelationship ≅ Relationship
- HolonCollection ≅ RecordStream with single Holon column
- Dances ≅ Algebraic operators

Each dance:

```
HolonStream → HolonStream
```

or

```
HolonStream → HolonGraph
```

This allows:

1. Gesture composition
2. Algebra tree construction
3. Optimization rewrites
4. Serialization to OpenCypher
5. Replay and explanation

---

# 5. Implementation Priorities for MAP

Recommended initial subset:

1. NodeByLabelScan / NodeIndexSeek
2. Expand (fixed-length)
3. Filter
4. Project
5. Aggregate
6. Sort / Limit
7. Apply
8. Optional
9. SemiApply
10. UnionAll

Add cost-based planning once statistics are available.

---

# 6. Conceptual Model Summary

OpenCypher in practice reduces to:

- Stream algebra over records
- Traversal as specialized join
- Apply-based correlated execution
- Hash/sort-based grouping
- Barrier-based update control

MAP can adopt this operator set directly while exposing each operator as a first-class user “dance,” enabling:

algebra → calculus (Cypher serialization) → optimized algebra

without losing expressive power.