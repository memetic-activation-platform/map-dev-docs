# Relationship Constraints Design Spec

## Purpose and authority

This specification defines the Schema 2.0 constraint surface and
representation-neutral conformance rules for relationship descriptors. Exact
descriptor declarations remain authoritative in the Core Schema TDL corpus
under `map-holons/schema-src`.

The [schema design specification](schema-design-spec.md) owns relationship
descriptor structure. The
[descriptor semantic rules](descriptor-semantics-rules.md) own effective
contracts and conformance orchestration. This document names the specialized
relationship rules and their ownership boundaries.

## Schema 2.0 posture

Schema 2.0 does not model relationship rules as a separate family of
`RelationshipConstraint` holons. A concrete relationship descriptor carries
its relationship semantics through its declared properties and structural
relationships.

Each direction defines:

- one source-type constraint;
- one target-type constraint;
- required `MinCardinality`;
- optional `MaxCardinality`;
- `AllowsDuplicates`;
- `IsOrdered`;
- `IsDefinitional`;
- directional `DeletionSemantic`; and
- `InheritanceMode`.

These concepts do not all have the same ontological character. Cardinality and
endpoint declarations constrain valid occurrences; orderedness and duplicate
policy govern occurrence shape; definitional and deletion semantics govern
relationship behavior. Their common declaration site does not turn them into
interchangeable constraint objects.

## Directionality

A declared relationship and its inverse are separate descriptor holons. Each
direction owns its source and target constraints, cardinality, duplicate and
ordering policy, definitional status, and deletion semantic.

The paired descriptors must be structurally consistent through their declared
inverse relationship, but values are not inferred by swapping or copying the
other direction. In particular, `DeletionSemantic` is resolved independently
for each direction.

## Descriptor validity

A relationship descriptor is valid only when:

- its source and target each resolve to an admissible holon-type constraint;
- `MinCardinality` is non-negative;
- an absent `MaxCardinality` means unbounded;
- a present maximum is non-negative and not less than the minimum;
- its inverse linkage satisfies the Schema 2.0 declared/inverse pairing rules;
  and
- every required semantic property is explicit after completion.

Inheritance follows the general effective-value rules. No relationship-specific
algorithm may bypass `InheritanceMode` or compute a competing effective
contract.

## Occurrence conformance

For a source holon and one semantic relationship name, conformance considers
the complete effective target set rather than validating serialized fragments
independently.

- The source and every target must satisfy the descriptor's endpoint
  constraints.
- The total target count must satisfy effective minimum and maximum
  cardinality.
- When duplicates are disallowed, the same semantic target may not appear more
  than once.
- When duplicates are allowed, distinct occurrences must retain occurrence
  identity as required by the runtime persistence contract.
- An ordered relationship requires valid authoritative ordering metadata for
  each occurrence; incidental storage or insertion order is not semantic
  order.
- Directional deletion behavior follows the effective `DeletionSemantic` of
  the direction being traversed or mutated.

Validation accumulates independently detectable violations as specified by the
[descriptor semantic rules](descriptor-semantics-rules.md).

## Persistence and runtime boundaries

Relationship occurrence identity, forward/inverse commit outcomes, retry, and
repair belong to the
[relationship persistence specification](../transactions/relationship-persistence-design-spec.md).

`SmartLink` encoding, relationship-property storage, target-property caching,
tag budgets, and raw retrieval belong to the
[storage-layer specification](../guest/storage-layer-services/storage-layer-design-spec.md).
`SequencePosition` is authoritative occurrence metadata there; this document
defines only the semantic requirement that ordered occurrences carry valid
order information.

Query and navigation components consume the resulting semantic order but do
not redefine relationship validity. Commands and transactions own mutation
operations such as append, insert, move, and remove.

## Explicit non-model

The earlier proposal for first-class `RelationshipConstraint` holons is not
part of Schema 2.0. It is retained in the archive as design history and must not
be used as the schema or implementation contract.
