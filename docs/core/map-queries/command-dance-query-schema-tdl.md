# Command, Dance, and Query Schema TDL

Status: current schema source of truth for the storage-grounded query model.

This document is the prescriptive schema companion for MAP query execution.
Narrative documents may explain behavior, but query state is defined here as
TDL descriptor declarations: holons, properties, values, relationships, inverse
relationships, and relationship attachments.

The current design separates reusable query definition from runtime execution.
`Query` is the reusable definition holon. `QueryDanceRequest` is a concrete
invocation request against that definition. `ExecutionInstance` is runtime state
for the whole query invocation. `QueryExpressionExecution` is runtime state for
one execution of one `QueryExpression`.

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
  depends_on MAP Dance Schema-v0.0.4
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

holon QueryDanceRequest {
  relationships {
    RequestedQuery
    InitialInput
    RequestParameters
  }
}

holon QueryDanceResponse {
  extends DanceResponseType

  relationships {
    ResponseBody
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
    ExecutesRequest
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

`ExecutionInstance` is runtime state for one execution of one
`QueryDanceRequest`. It does not replace the query definition. It records whole
query execution status, owns per-expression execution state, and points to the
final result collection.

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

## Query And QueryDanceRequest Relationships

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
  cardinality 0..32767
}

def relationship RequestedQuery {
  source QueryDanceRequest
  target Query
  cardinality 1..1
}

inverse relationship QueryRequestedBy {
  source Query
  target QueryDanceRequest
  inverse RequestedQuery
  cardinality 0..32767
}

def relationship InitialInput {
  source QueryDanceRequest
  target HolonCollection
  cardinality 1..1
}

inverse relationship InitialInputForQueryDanceRequest {
  source HolonCollection
  target QueryDanceRequest
  inverse InitialInput
  cardinality 0..32767
}

def relationship RequestParameters {
  source QueryDanceRequest
  target QueryParameterBinding
  cardinality 0..32767
}

inverse relationship ParametersForQueryDanceRequest {
  source QueryParameterBinding
  target QueryDanceRequest
  inverse RequestParameters
  cardinality 0..32767
}
```

---

## QueryExpression Relationships

```tdl
def relationship ExpressionParameters {
  source QueryExpression
  target QueryParameterDeclaration
  cardinality 0..32767
  ordered
}

inverse relationship ParametersForQueryExpression {
  source QueryParameterDeclaration
  target QueryExpression
  inverse ExpressionParameters
  cardinality 0..32767
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
one or more `QueryParameterDeclaration` holons. Invocation-specific parameter
bindings belong to `QueryDanceRequest` or `QueryExpressionExecution`.

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
  cardinality 0..32767
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
  cardinality 0..32767
}
```

`QueryParameterDeclaration` is definition state. It names a parameter and points
to the expected binding holon type descriptor.

`QueryParameterBinding` is runtime state. It links back to the declaration it
binds. Concrete binding holon types extend `QueryParameterBinding` and declare
their own value-bearing properties or relationships. This avoids making query
parameters stringly typed and avoids introducing a global generic `Parameter`
holon into the Dances schema.

---

## QuerySubTree Relationships

```tdl
def relationship Subtree {
  source QuerySubTree
  target QueryExpression
  cardinality 1..32767
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

All current expression types consume and produce `HolonCollection`.

Optional, singleton, and multi-valued results are represented by the contents of
the collection, not by separate result carrier types.

Concrete expression types should be introduced as holon types that extend
`QueryExpression`, such as future `Expand`, `Filter`, or storage-specific
expression types. Parameter typing belongs to those concrete expression type
definitions or to their parameter holon types, not to a separate
`ExpressionType` relationship.

---

## Execution Relationships

```tdl
def relationship ExecutesRequest {
  source ExecutionInstance
  target QueryDanceRequest
  cardinality 1..1
}

inverse relationship ExecutedBy {
  source QueryDanceRequest
  target ExecutionInstance
  inverse ExecutesRequest
  cardinality 0..32767
}

def relationship ExpressionExecutions {
  source ExecutionInstance
  target QueryExpressionExecution
  cardinality 0..32767
  ordered
}

inverse relationship ExecutionFor {
  source QueryExpressionExecution
  target ExecutionInstance
  inverse ExpressionExecutions
  cardinality 1..1
}

relationship ExecutionResult {
  source ExecutionInstance
  target HolonCollection
  cardinality 0..1
}

inverse relationship ResultOfExecution {
  source HolonCollection
  target ExecutionInstance
  inverse ExecutionResult
  cardinality 0..32767
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
  cardinality 0..32767
}

def relationship Input {
  source QueryExpressionExecution
  target HolonCollection
  cardinality 1..1
}

inverse relationship InputFor {
  source HolonCollection
  target QueryExpressionExecution
  inverse Input
  cardinality 0..32767
}

relationship Result {
  source QueryExpressionExecution
  target HolonCollection
  cardinality 0..1
}

inverse relationship ResultOf {
  source HolonCollection
  target QueryExpressionExecution
  inverse Result
  cardinality 0..32767
}

def relationship RuntimeParameters {
  source QueryExpressionExecution
  target QueryParameterBinding
  cardinality 0..32767
}

inverse relationship RuntimeParametersFor {
  source QueryParameterBinding
  target QueryExpressionExecution
  inverse RuntimeParameters
  cardinality 0..32767
}
```

`Input` and `Result` are runtime relationships. They are declared on
`QueryExpressionExecution`, not on `QueryExpression`, because a saved
`QueryExpression` definition may be executed many times against different input
collections and may produce different result collections.

---

## Dance Types And Assertions

```tdl
holon QueryDance {
  extends DanceType

  properties {
    DanceDescription
  }

  relationships {
    DanceInput
    Response
    HasImplementation
  }
}
```

TDL currently defines descriptor types, not holon instances. The required
schema assertions are therefore recorded normatively here and should be
represented in the generated schema/import layer:

- `HolonSpace` affords `QueryDance`.
- `QueryDance.DanceInput` is `QueryDanceRequest`.
- `QueryDance.Response` is `QueryDanceResponse`.
- `QueryDanceResponse.ResponseBody` is `HolonCollection`.
