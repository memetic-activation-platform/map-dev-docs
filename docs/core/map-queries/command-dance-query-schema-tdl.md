# MAP Query Schema Design TDL

Status: normative schema design companion for the storage-grounded query model.

This document prescribes the reusable query-domain descriptor declarations:
holons, properties, values, relationships, inverse relationships, and
relationship attachments. Its authoritative loadable source is
`map-holons/schema-src/query/schema.tdl`, which depends on Core. Core does not
depend on Query.

`QueryDance`, its request and response types, and the `HolonSpace` affordance
belong to the [Query–Dance adapter schema](query-dance-adapter-schema-tdl.md),
which depends on both the Dance layer and this Query Schema.

The blocks below characterize the implemented TDL 2.0 package design.

The current design separates reusable query definition from runtime execution.
`Query` is the reusable definition holon. `ExecutionInstance` is runtime state
for one direct or Dance-mediated invocation of that query.
`QueryExpressionExecution` is runtime state for one execution of one
`QueryExpression`.

Saved query definitions and runtime bindings are separate:

- `QueryExpression` holons define the reusable query tree.
- `QueryParameterDeclaration` holons define the parameters accepted by reusable
  expressions.
- `QueryParameterBinding` holons provide concrete values for one request or one
  expression execution.
- `QueryExpressionExecution` holons bind one expression invocation to its
  runtime input collection, result collection, and resolved parameter bindings.

`QueryTree` is a conceptual name for the definition shape rooted by
`Query.RootExpression`. It is not a separate holon type.

---

## Schema Declaration

```tdl
schema MAP Query Schema-v0.0.2 {
  depends_on MAP Core Schema-v0.0.7
}
```

---

## Core Query Types

```tdl
holon Query {
  properties {
    QueryName
    QueryDescription
  }

  relationships {
    RootExpression
  }
}

holon QueryExpression {
  relationships {
    ExpressionParameters
    Next
  }
}

holon QuerySubTree {
  extends QueryExpression

  relationships {
    Subtree
  }
}

holon QueryParameterDeclaration {
  properties {
    ParameterName
  }

  relationships {
    ParameterBindingType
  }
}

abstract holon QueryParameterBinding {
  properties {
    ParameterName
  }

  relationships {
    BindsParameter
  }
}

```

Concrete query operator types should extend `QueryExpression`. A runtime query
expression holon is classified through its ordinary type descriptor
(`DescribedBy`) relationship, with inverse instance discovery through the normal
descriptor instance relationship. Do not add a separate `ExpressionType`
relationship for that purpose.

---

## Execution State Types

```tdl
holon ExecutionInstance {
  properties {
    ExecutionStatus
  }

  relationships {
    ExecutesQuery
    FocalSpace
    ExpressionExecutions
    ExecutionResult
  }
}

holon QueryExpressionExecution {
  properties {
    ExecutionStatus
  }

  relationships {
    ExecutesExpression
    Input
    Result
    RuntimeParameters
  }
}
```

`ExecutionInstance` is runtime state for one execution of one `Query`. It does
not replace the query definition. It records whole-query execution status, the
required focal `HolonSpace` for local seed scope, per-expression execution
state, and the final result collection. `FocalSpace` is transient invocation
context, not saved query-definition state and not `ExecutionDomain`.

`QueryExpressionExecution` records one runtime invocation of one
`QueryExpression`. This is where runtime `Input`, runtime `Result`, and resolved
runtime parameter bindings live.

---

## Properties And Values

```tdl
property QueryName {
  value MapStringValueType
}

property QueryDescription {
  value MapStringValueType
}

property ParameterName {
  value MapStringValueType
}

property ExecutionStatus {
  value QueryExecutionStatus
}

enum QueryExecutionStatus {
  variants {
    QueryExecutionPending
    QueryExecutionRunning
    QueryExecutionComplete
    QueryExecutionFailed
  }
}
```

---

## Query Relationships

```tdl
def relationship RootExpression {
  source Query
  target QueryExpression
  cardinality 1..1
}

inverse relationship RootExpressionFor {
  source QueryExpression
  target Query
  inverse RootExpression
  cardinality 0..*
}

## QueryExpression Relationships

```tdl
def relationship ExpressionParameters {
  source QueryExpression
  target QueryParameterDeclaration
  cardinality 0..*
  ordered
}

inverse relationship ParametersForQueryExpression {
  source QueryParameterDeclaration
  target QueryExpression
  inverse ExpressionParameters
  cardinality 0..*
}

def relationship Next {
  source QueryExpression
  target QueryExpression
  cardinality 0..1
}

inverse relationship Previous {
  source QueryExpression
  target QueryExpression
  inverse Next
  cardinality 0..1
}
```

`Next` is the declared relationship for sequential execution. `Previous` is only
its inverse relationship.

`ExpressionParameters` belongs to the reusable query definition. It may point to
one or more `QueryParameterDeclaration` holons. Invocation bindings belong to a
direct peer-Rust call or, for Dance ingress, to the Query–Dance adapter request.
Resolved bindings belong to `QueryExpressionExecution`.

---

## Query Parameter Relationships

```tdl
def relationship ParameterBindingType {
  source QueryParameterDeclaration
  target HolonType
  cardinality 1..1
}

inverse relationship ParameterDeclaredBy {
  source HolonType
  target QueryParameterDeclaration
  inverse ParameterBindingType
  cardinality 0..*
}

def relationship BindsParameter {
  source QueryParameterBinding
  target QueryParameterDeclaration
  cardinality 1..1
}

inverse relationship ParameterBoundBy {
  source QueryParameterDeclaration
  target QueryParameterBinding
  inverse BindsParameter
  cardinality 0..*
}
```

`QueryParameterDeclaration` is definition state. It names a parameter and points
to the expected binding holon type descriptor.

`QueryParameterBinding` is runtime state. It links back to the declaration it
binds. Concrete binding holon types extend `QueryParameterBinding` and declare
their own value-bearing properties or relationships. This avoids making query
parameters stringly typed and avoids introducing a global generic `Parameter`
holon into MAP schema packages.

---

## QuerySubTree Relationships

```tdl
def relationship Subtree {
  source QuerySubTree
  target QueryExpression
  cardinality 1..*
  ordered
}

inverse relationship Parent {
  source QueryExpression
  target QuerySubTree
  inverse Subtree
  cardinality 0..1
}
```

`Subtree` is implementation containment, not execution continuation. The first
ordered `Subtree` expression is the implementation entry expression. Terminal
subtree expressions with no `Next` relationship are exits. Multiple exits are
allowed; their merge or selection rule belongs to the parent expression's
concrete query expression type.

---

## QueryExpression Type Semantics

Operand-consuming expression types consume and produce `HolonCollection`.
Source-producing roots may produce a collection without an `Input` relationship.

Optional, singleton, and multi-valued results are represented by the contents of
the collection, not by separate result carrier types.

`Input` is optional in the base execution schema because root expression types
determine whether they are source-producing or operand-consuming. `SeedHolons`
is root-only, declares no parameters, and requires no input; supplied input is
an error. A root `Expand` requires exactly one `HolonCollectionReference`.
Non-root `Expand` receives its predecessor result. A direct-call helper may
normalize one holon reference into a transient singleton collection before
dispatch; the schema itself has no singular-or-collection input union.

Concrete expression types should be introduced as holon types that extend
`QueryExpression`, such as future `Expand`, `Filter`, or storage-specific
expression types. Parameter typing belongs to those concrete expression type
definitions or to their parameter holon types, not to a separate
`ExpressionType` relationship.

### QRY2 Expand Predicate Attachment

QRY2 declares `SeedHolons` and `Expand` as concrete `QueryExpression` types.
It also declares an abstract `QueryPredicate` plus optional
`SeedHolons.SeedPredicate -> QueryPredicate` and
`Expand.ExpansionPredicate -> QueryPredicate` relationships. These are
intentional payload hooks, not a filter implementation: QRY2 provides no
concrete `QueryPredicate` subtype, operator, composition form, evaluator, or
storage-pushdown contract. The payloads are definition state and do not alter
the collection-input rules for either expression.

The later predicate/operator track owns the concrete grammar and construction
API. It must start from effective operators supplied by each value type; a
security-aware `available operators` layer is deliberately not part of this
schema contract yet.

---

## Execution Relationships

```tdl
def relationship ExecutesQuery {
  source ExecutionInstance
  target Query
  cardinality 1..1
}

inverse relationship ExecutedBy {
  source Query
  target ExecutionInstance
  inverse ExecutesQuery
  cardinality 0..*
}

def relationship FocalSpace {
  source ExecutionInstance
  target HolonSpace
  cardinality 1..1
}

inverse relationship FocalSpaceFor {
  source HolonSpace
  target ExecutionInstance
  inverse FocalSpace
  cardinality 0..*
}

def relationship ExpressionExecutions {
  source ExecutionInstance
  target QueryExpressionExecution
  cardinality 0..*
  ordered
}

inverse relationship ExecutionFor {
  source QueryExpressionExecution
  target ExecutionInstance
  inverse ExpressionExecutions
  cardinality 1..1
}

def relationship ExecutionResult {
  source ExecutionInstance
  target HolonCollection
  cardinality 0..1
}

inverse relationship ResultOfExecution {
  source HolonCollection
  target ExecutionInstance
  inverse ExecutionResult
  cardinality 0..*
}
```

---

## QueryExpressionExecution Relationships

```tdl
def relationship ExecutesExpression {
  source QueryExpressionExecution
  target QueryExpression
  cardinality 1..1
}

inverse relationship ExpressionExecutedBy {
  source QueryExpression
  target QueryExpressionExecution
  inverse ExecutesExpression
  cardinality 0..*
}

def relationship Input {
  source QueryExpressionExecution
  target HolonCollection
  cardinality 0..1
}

inverse relationship InputFor {
  source HolonCollection
  target QueryExpressionExecution
  inverse Input
  cardinality 0..*
}

def relationship Result {
  source QueryExpressionExecution
  target HolonCollection
  cardinality 0..1
}

inverse relationship ResultOf {
  source HolonCollection
  target QueryExpressionExecution
  inverse Result
  cardinality 0..*
}

def relationship RuntimeParameters {
  source QueryExpressionExecution
  target QueryParameterBinding
  cardinality 0..*
}

inverse relationship RuntimeParametersFor {
  source QueryParameterBinding
  target QueryExpressionExecution
  inverse RuntimeParameters
  cardinality 0..*
}
```

`Input` and `Result` are runtime relationships. They are declared on
`QueryExpressionExecution`, not on `QueryExpression`, because a saved
`QueryExpression` definition may be executed many times against different input
collections and may produce different result collections.

---

## Package Boundary

The Query Schema has no dependency on Dance descriptors and defines no Dance
entry point. A peer Rust caller may invoke a `Query` directly with its runtime
input and bindings. The Query–Dance adapter maps a `QueryDanceRequest` onto the
same direct query-execution contract.

`HasImplementation` is owned by Dance infrastructure as the inverse of
`DanceImplementation.ForDance`; it is not a Query-to-Core or Query-to-Dance
binding.
