# MAP Query–Dance Adapter Schema Design TDL (v1.1)

## Change Log

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

The adapter owns `QueryDance`, `QueryDanceRequest`, `QueryDanceResponse`, and
the concrete `QueryDance.DanceAffordedBy -> HolonSpace` declared relationship,
whose inverse is `HolonSpace.AffordsDance -> QueryDance`. It also owns the
adapter-specific `MetaQueryDanceType` that admits that relationship on
`QueryDance`.
It does not own `Query`, query expressions, parameters, or execution state;
those are owned by the Query Schema.

`QueryDance` is its canonical DanceName because that is the inherited
`TypeDescriptor.TypeName` of `QueryDance.DanceType`. A transport or API alias
does not participate in Dance resolution. Its invocations require a
`HolonSpace` affording holon; the adapter's qualified affordance relationship
is the schema declaration that supports that requirement.

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

holon MetaQueryDanceType {
  extends MetaDanceType

  relationships {
    InstanceRelationships -> [
      (QueryDance)-[DanceAffordedBy]->(HolonSpace)
    ]
  }
}

holon QueryDance {
  type MetaQueryDanceType
  extends DanceType

  relationships {
    RequestType
    Response
    DanceAffordedBy
  }
}

def relationship DanceAffordedBy {
  source QueryDance
  target HolonSpace
  cardinality 0..*
  inverse AffordsDance
}

inverse relationship AffordsDance {
  source HolonSpace
  target QueryDance
  cardinality 0..*
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

`QueryDance` declares `AffordingHolonRequirement = Required` in its DanceType
metadata. The exact TDL property-value syntax follows the compiler's Schema 2.0
authoring rules; this contract does not introduce a second DanceName property.

The adapter asserts that `QueryDance.RequestType` is `QueryDanceRequest`, that
`QueryDance.Response` is `QueryDanceResponse`, that the response body is a
`HolonCollection`, and that `HolonSpace` affords `QueryDance`. The
`DanceAffordedBy` relationship is adapter-defined. Its descriptor identity is
distinct from Dance's generic `DanceAffordedBy` / `AffordsDance` pair despite
the overlapping base names; relationship identity must not be collapsed by base
name.

`HasImplementation` is not declared here: it remains the Dance-owned inverse
of `DanceImplementation.ForDance`.

## Invocation Boundary

The Dance executor resolves canonical `DanceName` to `QueryDance`, structurally
validates its `QueryDanceRequest`, and validates the response contract before
return. The adapter then supplies its selected `Query`, initial collection, and
bindings to the shared Query engine. The engine creates
an `ExecutionInstance` that executes the selected `Query`; it does not execute
the adapter request as a query-domain object. The same engine remains callable
directly by peer Rust objects without importing Dance types.

QueryCore remains internal to `map-query-schema` until another independently
loadable consumer needs the direct-execution contract without Query definitions,
or it requires independent versioning. Either condition is the extraction
trigger for a separate QueryCore package.
