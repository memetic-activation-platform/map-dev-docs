# Comprehensive Cypher Execution Operator Inventory v1.1

This document catalogs the operators that appear in real-world OpenCypher execution engines, including graph access primitives, traversal operators, filtering and predicate evaluators, join variants, aggregation implementations, write operators, subquery controls, runtime barriers, and schema management operations. It reflects the practical execution-layer reality of Cypher systems (e.g., Neo4j, Memgraph), including physical access strategies (index seeks, scans, hash joins), control-flow operators (Apply variants, Subquery boundaries), and transactional enforcement (locking, eager materialization). While not algebraically minimal, it provides a detailed reference model of how declarative Cypher queries are decomposed into executable plan operators.

Descriptor synthesis note:

- this inventory is a reference catalog for planning and execution vocabulary
- it is not the semantic source of MAP value/operator meaning
- MAP-specific operator semantics should come from descriptor-owned value semantics, especially `ValueDescriptor`


## 1. Graph Access & Pattern Expansion

**NodeByLabelScan**  
Scans all nodes that carry a given label. Typically used when no index is available for the starting predicate.

**AllNodesScan**  
Scans every node in the graph. This is the most general and usually most expensive starting operator.

**NodeIndexSeek**  
Uses an index to directly locate nodes matching a property predicate. This is the preferred access path when selective predicates exist.

**NodeIndexScan**  
Scans entries in a node index, often when range predicates are used. More selective than a label scan but less precise than a unique seek.

**NodeUniqueIndexSeek**  
Uses a uniqueness constraint-backed index to retrieve exactly one node. Guarantees at most one match.

**RelationshipByTypeScan**  
Scans relationships of a specific type. Used when matching patterns starting from relationships.

**DirectedRelationshipByIdSeek**  
Retrieves a relationship by its internal ID with direction enforced. Very fast, constant-time access.

**UndirectedRelationshipByIdSeek**  
Retrieves a relationship by ID without constraining direction. Also constant-time lookup.

**NodeByIdSeek**  
Fetches a node directly by its internal ID. This is the fastest possible node access.

**Expand(All)**  
Traverses from a bound node across all matching relationships to neighboring nodes. This is the core traversal primitive.

**Expand(Into)**  
Traverses between already-bound nodes to verify or materialize an existing relationship. Often used to avoid redundant expansion.

**OptionalExpand**  
Performs a traversal but yields `null` when no match exists. Implements `OPTIONAL MATCH` semantics.

**VarLengthExpand**  
Traverses paths of variable length within given bounds. Used for `*1..n` style patterns.

**ShortestPath**  
Computes the shortest path between two nodes according to pattern constraints. Typically implemented using BFS-like strategies.

**MultiNodeIndexSeek**  
Simultaneously seeks multiple indexed predicates and intersects results. Improves selectivity when multiple filters apply.

---

## 2. Filtering & Predicate Evaluation

**Filter**  
Applies boolean predicates to rows and removes those that do not satisfy conditions. Implements `WHERE` logic.

**NodePropertyFilter**  
Filters rows based on node property predicates. Evaluates comparisons like equality or range conditions.

**RelationshipPropertyFilter**  
Filters rows using relationship property conditions. Similar to node property filtering but applied to edges.

**Exists (property existence check)**  
Checks whether a property exists on a node or relationship. Used for existence predicates.

**IsNotNull**  
Ensures a value is not null before allowing the row to pass. Common in optional match pipelines.

**Distinct**  
Removes duplicate rows from the result stream. Implements Cypher’s `DISTINCT` keyword.

**Limit**  
Restricts the number of rows passed downstream. Often pushed down for optimization.

**Skip**  
Discards a specified number of rows before passing results onward. Used for pagination.

---

## 3. Join & Row Combination Operators

**CartesianProduct**  
Combines two independent row streams into all possible pairs. Usually appears when patterns are disconnected.

**NodeHashJoin**  
Joins two streams using node identity equality via hashing. Efficient for equijoins on node variables.

**ValueHashJoin**  
Performs a hash-based join on arbitrary value equality. Used when joining on computed expressions.

**NestedLoopJoin**  
Joins streams by iterating one side for each row of the other. Less efficient but flexible.

**Apply**  
Feeds each row from the left side into the right-side operator. Fundamental to pattern chaining and correlated execution.

**SemiApply**  
Returns rows from the left side only if the right side produces at least one match. Implements existential semantics.

**AntiSemiApply**  
Returns rows from the left only if the right side produces no match. Implements negated existential semantics.

**LetSemiApply**  
Like SemiApply but binds additional variables from the right side. Combines filtering with projection.

**LetAntiSemiApply**  
Like AntiSemiApply but allows binding when no match exists. Supports negated pattern conditions.

**ConditionalApply**  
Executes the right side only if a condition holds. Used in conditional query constructs.

**RollUpApply**  
Executes a subquery per row and aggregates its results into a collection. Supports pattern comprehensions.

---

## 4. Projection & Transformation

**Projection**  
Computes and selects expressions to pass forward. Implements `RETURN` and `WITH` expressions.

**ProduceResults**  
Final operator that emits results to the client. Terminates the execution pipeline.

**With (pipeline boundary)**  
Introduces a logical pipeline break with projection and optional aggregation. Controls variable scope.

**Unwind**  
Expands a list into multiple rows. Converts collections into row streams.

**Foreach**  
Executes updates for each element of a list. Primarily used for write-side iteration.

**LoadCSV**  
Reads rows from a CSV file into the execution pipeline. Supports bulk data ingestion.

---

## 5. Aggregation & Grouping

**Aggregation**  
Groups rows by key expressions and computes aggregate functions. Implements Cypher grouping semantics.

**OrderedAggregation**  
Performs aggregation assuming sorted input for efficiency. Reduces memory overhead.

**EagerAggregation**  
Materializes all input rows before aggregating. Used when streaming aggregation is unsafe.

**Count**  
Counts rows or non-null values. Implements `count()`.

**Sum**  
Computes the numeric sum of values. Implements `sum()`.

**Avg**  
Computes the arithmetic mean of numeric values. Implements `avg()`.

**Min**  
Finds the smallest value in a group. Implements `min()`.

**Max**  
Finds the largest value in a group. Implements `max()`.

**Collect**  
Aggregates values into a list. Implements `collect()`.

**PercentileCont**  
Computes a continuous percentile using interpolation. Used in statistical queries.

**PercentileDisc**  
Computes a discrete percentile from observed values. Returns an actual data point.

**StdDev**  
Computes sample standard deviation. Implements `stDev()`.

**StdDevP**  
Computes population standard deviation. Implements `stDevP()`.

---

## 6. Ordering & Pagination

**Sort**  
Orders rows based on specified expressions. Implements `ORDER BY`.

**Top**  
Returns the top N rows after ordering. Optimized limit-with-sort operator.

**TopN**  
Variant of Top optimized for streaming scenarios. Minimizes sorting cost.

**PartialSort**  
Sorts only necessary portions of input. Used when full ordering is not required.

---

## 7. Subqueries & Procedure Calls

**CallSubquery**  
Executes an inline subquery per input row or once globally. Supports query modularization.

**SubqueryStart**  
Marks the beginning of a subquery execution context. Establishes isolated scope.

**SubqueryEnd**  
Marks the end of subquery execution. Returns results to the outer pipeline.

**ProcedureCall**  
Invokes a stored procedure. Extends Cypher with custom logic.

**Yield**  
Projects procedure outputs into the query pipeline. Similar to a projection step.

---

## 8. Data Modification (Write Operators)

**Create**  
Creates nodes and/or relationships as specified by a pattern. Implements `CREATE`.

**CreateNode**  
Allocates and initializes a new node. Sets labels and properties.

**CreateRelationship**  
Creates a relationship between bound nodes. Assigns type and properties.

**Merge**  
Matches a pattern or creates it if absent. Combines read and conditional write semantics.

**MergeCreate**  
Executes the creation branch of a `MERGE`. Runs when no match exists.

**MergeMatch**  
Executes the match branch of a `MERGE`. Runs when a match is found.

**SetProperty**  
Assigns or updates a property value. Implements `SET`.

**SetNodeProperty**  
Updates a property on a node. Specialized form of SetProperty.

**SetRelationshipProperty**  
Updates a property on a relationship. Specialized property mutation.

**SetLabel**  
Adds a label to a node. Modifies node classification.

**RemoveProperty**  
Deletes a property from an entity. Implements `REMOVE`.

**RemoveLabel**  
Removes a label from a node. Alters node classification.

**Delete**  
Deletes a node or relationship. Fails if node still has relationships.

**DetachDelete**  
Deletes a node and all its relationships. Ensures referential cleanup.

**Foreach (write variant)**  
Performs write operations for each element in a list. Used for batch-style updates.

---

## 9. Union & Result Composition

**Union**  
Combines results of multiple queries and removes duplicates. Implements `UNION`.

**UnionAll**  
Combines results without removing duplicates. Implements `UNION ALL`.

---

## 10. Execution Control / Pipeline Management

**Argument**  
Introduces externally bound variables into a pipeline stage. Common in subqueries.

**Eager**  
Forces full materialization of intermediate results. Prevents unsafe interleaving of reads and writes.

**ProduceResults**  
Finalizes and streams results to the client. Ends execution.

**EmptyResult**  
Produces no rows intentionally. Used in control-flow scenarios.

**LockNodes**  
Locks nodes for transactional safety during writes. Ensures isolation guarantees.

---

## 11. Schema Operations (Administrative)

**CreateIndex**  
Creates an index on label/property combinations. Improves read performance.

**DropIndex**  
Removes an existing index. May impact query performance.

**CreateConstraint**  
Defines uniqueness or existence constraints. Enforces data integrity.

**DropConstraint**  
Removes an existing constraint. Relaxes enforced invariants.

---

## Operands

### Core Runtime Data Model

#### Row Stream

All Cypher algebra operators (except schema-only operations) consume and/or produce a:

```
RowStream = Sequence<Row>
```

A row is defined as:

```
Row = Map<VariableName, Value>
```

---

#### Value Domain

```
Value ::=
    Node
  | Relationship
  | Path
  | Scalar
  | List<Value>
  | Map<String, Value>
  | Null
```

---

#### Node

```
Node = {
    id: NodeId,
    labels: Set<Label>,
    properties: Map<String, Scalar>
}
```

---

#### Relationship

```
Relationship = {
    id: RelationshipId,
    type: RelType,
    startNodeId: NodeId,
    endNodeId: NodeId,
    properties: Map<String, Scalar>
}
```

---

#### Path

```
Path = {
    nodes: List<Node>,
    relationships: List<Relationship>
}
```

---

#### Scalar Types

```
Scalar ::=
    Integer
  | Float
  | Boolean
  | String
  | Temporal
  | Duration
  | Point
```

---

### Operand Categories

Cypher operators consume and/or produce combinations of the following operand types:

- RowStream
- GraphStore (implicit global operand)
- Expression
- Predicate
- Pattern
- AggregationFunction
- SortKey
- SchemaDefinition

---

### Execution Context

All non-schema operators execute within:

```
ExecutionContext = {
    GraphStore,
    Transaction,
    Parameters,
    RowStream
}
```

At the most abstract level:

```
Operator : ExecutionContext × RowStream
         → ExecutionContext × RowStream
```

- Read-only operators preserve `GraphStore`.
- Write operators mutate `GraphStore`.
- Schema operators mutate `SchemaState`.

---

### Join Operand Model

Join-family operators consume:

```
LeftStream
RightStream
JoinCondition
```

and produce:

```
RowStream (merged rows)
```

---

### Aggregation Operand Model

Aggregation operators consume:

```
RowStream
GroupingExpressions
AggregationFunctions
```

and produce:

```
RowStream (one row per group)
```

Aggregate functions consume:

```
List<Scalar | Value>
```

and produce:

```
Scalar | List<Value>
```

---

### Write Operand Model

Write operators consume:

- RowStream
- GraphStore (mutable)
- Pattern or Entity binding

They produce:

- Updated RowStream

and have side effects on the GraphStore.

---

### Schema Operand Model

Schema operators consume:

- SchemaDefinition
- GraphStore (metadata layer)

They produce:

- Updated SchemaState

and mutate the database schema (indexes, constraints).
