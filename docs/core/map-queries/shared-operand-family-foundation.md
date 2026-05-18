# Shared Operand Family Foundation

This document defines the shared materialized operand family for MAP query-adjacent contract shapes and serialized payloads. It stabilizes shape vocabulary only. It does not introduce descriptor-backed interrogation, planner semantics, distributed behavior, or legacy query-runtime migration.

It does not require eager materialization of row projections as the internal execution model. Execution layers may retain richer bindings, including holon references, and materialize `Value`, `Row`, or `RowSet` only when a contract or operator requires those shapes.

The primary intermediate representational layer is defined separately by the Binding Layer foundation. This document should be read as describing materialized projection and contract shapes, not the primary execution-time binding substrate.

## Operand Family

### `Value`

`Value` is the shared scalar/domain payload family. In this slice it reuses the existing `BaseValue` encoding:

```json
{ "StringValue": "alpha" }
```

Use `Value` for scalar payloads, parameter atoms, and single field results where row structure is not needed.

### `Row`

`Row` is a single materialized row-shaped projection keyed by projection labels serialized as strings. Keys are not descriptor-backed property identifiers in this slice.

```json
{
  "title": { "StringValue": "alpha" },
  "rank": { "IntegerValue": 7 }
}
```

Use `Row` when a result or parameter shape needs multiple named scalar fields in one projection object.

A `Row` is a projection result shape, not necessarily the engine's internal binding representation. Internal execution may retain named holon or relationship bindings and derive row fields lazily at the point of projection, filtering, ordering, aggregation, or serialization.

### `RowSet`

`RowSet` is an ordered collection of rows:

```json
{
  "rows": [
    {
      "title": { "StringValue": "alpha" },
      "rank": { "IntegerValue": 7 }
    },
    {
      "title": { "StringValue": "beta" },
      "rank": { "IntegerValue": 9 }
    }
  ]
}
```

Use `RowSet` when a contract needs a collection of row-shaped projections. `RowSet` preserves row order but does not imply uniqueness, schema, cursoring, streaming, or planner semantics.

`RowSet` is an ordered collection of materialized rows. It describes the shape of a contract result once row projection has occurred; it does not imply when or how those rows were materialized during execution.

## Boundaries

- `Value` is scalar/domain-shaped only.
- `Row` contains projection labels mapped to scalar `Value` payloads only.
- `Row` does not contain nested `Row` or `RowSet` values.
- `RowSet` is collection-shaped only and does not define descriptor, operator, planner, or distributed semantics.
- This operand family defines materialized contract shapes only; it does not require intermediate query state to be stored as rows rather than as richer runtime bindings.
- This operand family should be read beneath, not instead of, the Binding Layer.

## Relationship to Existing `NodeCollection`

`NodeCollection` remains the current relationship-traversal query runtime shape. It models source holons and traversed relationships, not row projections.

This is a non-example:

```json
{
  "members": [
    {
      "source_holon": { "Staged": { "tx_id": 41, "id": "..." } },
      "relationships": null
    }
  ],
  "query_spec": { "relationship_name": "children" }
}
```

That shape is a traversal graph artifact, not a `RowSet`. This operand slice does not replace it.

## Non-Goals

- Descriptor-backed field interrogation
- Predicate or operator legality
- Planner or execution semantics
- Distributed query behavior
- Legacy query module removal or migration
- Defining the internal runtime representation of intermediate bindings or requiring eager projection of those bindings into `Row`
- Final `Record` or `RecordStream` behavior

## Forward Compatibility

This foundation leaves room for later operand families such as `Record` and `RecordStream`, which may carry richer identity, descriptor, or streaming semantics. Those families should build on this vocabulary rather than redefining scalar-vs-row-vs-rowset distinctions.

Future operand families or execution-layer contracts may also distinguish between projection shapes and identity-bearing bindings, for example through binding-layer objects, `HolonReference`-backed records, or other descriptor-aware operands before final projection.
