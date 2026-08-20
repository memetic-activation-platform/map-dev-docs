# MAP Query–Dance Adapter Schema Design TDL (v1.2)

## Change Log

### v1.2

- records the generic Dance affordance and name-addressed binding foundation
  delivered by [map-holons #652](https://github.com/evomimic/map-holons/issues/652)
  through [PR #654](https://github.com/evomimic/map-holons/pull/654)
- keeps descriptor-aware request/response validation and query execution as
  follow-up work

### v1.1

- aligns QueryDance with Issue 17's canonical DanceName, required `HolonSpace`
  affordance, and structural Dance boundary

### v1.0

- unversioned normative Query–Dance adapter schema companion baseline

Status: normative schema-design companion for Dance-mediated query invocation.

This document defines the adapter between the independently usable Query Schema
and MAP's descriptor-afforded Dance layer. Its loadable source is
`map-holons/schema-src/query-dance/schema.tdl`.

The runtime invocation direction is:

```text
Command -> Dance -> QueryDance -> Query -> QueryCore -> Core
(direct peer Rust callers enter at Query)
```

`QueryCore` is an internal direct-execution submodule of `map-query-schema`,
not a loadable schema package. It owns the execution contract and lifecycle,
but every execution still executes a `Query` and direct callers enter the
`Query` API, not a generic QueryCore API.

The schema-import direction is different from runtime dispatch:

```text
Core <- Dance
Core <- Commands
Core <- Query
Dance + Query + Core <- QueryDance
```

`MAP Dance Schema-v0.1.0` is independently loadable after
`MAP Core Schema-v0.0.7`. QueryDance depends explicitly on Dance, Query, and
Core; Dance never imports QueryDance. The declarations below characterize the
implemented TDL 2.0 package design.

## Owned Types

The adapter owns `QueryDance`, `QueryDanceRequest`, and `QueryDanceResponse`.
`QueryDance` extends `DanceType` and is afforded by `HolonSpace` through the
generic Dance Schema `HolonType -[AffordsDance]-> DanceType` relationship.
It does not own `Query`, query expressions, parameters, or execution state;
those are owned by the Query Schema.

`QueryDance` is its canonical DanceName because that is the inherited
`TypeDescriptor.TypeName` of `QueryDance.DanceType`. A transport or API alias
does not participate in Dance resolution. Its invocations require a
`HolonSpace` affording holon through the generic Dance affordance.

## Schema Declaration

```tdl
schema MAP Query Dance Adapter Schema-v0.1.0 {
  depends_on MAP Dance Schema-v0.1.0
  depends_on MAP Query Schema-v0.1.0
  depends_on MAP Core Schema-v0.0.7
}
```

The generated artifact is
`map-holons/generated/json-imports/query-dance/schema.json`. Its `load_with`
entries are relative to that artifact: `../core/root.json`,
`../dance/schema.json`, and `../query/schema.json`.

## Adapter Types And Relationships

```tdl
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

holon QueryDance {
  type MetaDanceType
  extends DanceType

  relationships {
    RequestType
    Response
    DanceAffordedBy
  }
}

def relationship RequestedQuery {
  source QueryDanceRequest
  target Query
  cardinality 1..1
}

def relationship InitialInput {
  source QueryDanceRequest
  target HolonCollection
  cardinality 1..1
}

def relationship RequestParameters {
  source QueryDanceRequest
  target QueryParameterBinding
  cardinality 0..*
}
```

`QueryDance` requires an `AffordingHolon` under the common Dance invocation
contract. The exact TDL property-value syntax follows the compiler's Schema 2.0
authoring rules; this contract does not introduce a second DanceName property.

The adapter asserts that `QueryDance.RequestType` is `QueryDanceRequest`, that
`QueryDance.Response` is `QueryDanceResponse`, that the response body is a
`HolonCollection`, and that `HolonSpace` affords `QueryDance`. The
`HolonSpace` affords `QueryDance` through Dance's generic
`AffordsDance` / `DanceAffordedBy` relationship pair. `QueryDance` participates
as a concrete `DanceType` extension and declares a `DanceAffordedBy` fact
through the inherited generic inverse; the adapter defines no second affordance
relationship.

`HasImplementation` is not declared here: it remains the Dance-owned inverse
of `DanceImplementation.ForDance`.

## Invocation Boundary

The Dance binding foundation resolves canonical `DanceName` to `QueryDance`
through the required affording holon's effective Dance affordances. Full
descriptor-aware validation of `QueryDanceRequest` and the response contract is
deferred to the shared Validation track. The adapter then supplies its selected
`Query`, initial collection, and bindings to the shared Query engine. The engine creates
an `ExecutionInstance` that executes the selected `Query`; it does not execute
the adapter request as a query-domain object. The same engine remains callable
directly by peer Rust objects without importing Dance types.

QueryCore remains internal to `map-query-schema` until another independently
loadable consumer needs the direct-execution contract without Query definitions,
or it requires independent versioning. Either condition is the extraction
trigger for a separate QueryCore package.
