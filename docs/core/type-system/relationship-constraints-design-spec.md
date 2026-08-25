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

Schema 2.0 represents directional cardinality as a configured first-class
`CardinalityConstraint` holon attached to the relationship descriptor through
the generic additive `Constraints` relationship. It does not model every
relationship semantic as a constraint holon. A concrete relationship descriptor
carries its remaining structural and policy semantics through declared
properties and structural relationships. Consumers use the descriptor kernel's
effective products for that relationship, so inherited semantic fields and
constraints are resolved before policy is applied.

Each direction defines:

- one source-type constraint;
- one target-type constraint;
- `AllowsDuplicates`;
- `IsOrdered`;
- `IsDefinitional`;
- directional `DeletionSemantic`.

These concepts do not all have the same ontological character. Cardinality is a
configured invariant over an occurrence collection; endpoint declarations are
structural typing requirements; orderedness and duplicate policy govern
occurrence shape; definitional and deletion semantics govern relationship
behavior. Their common definition site does not turn them into interchangeable
constraint objects.

## Directionality

A declared relationship and its inverse are separate descriptor holons. Each
direction owns its source and target constraints, cardinality constraint,
duplicate and ordering policy, definitional status, and deletion semantic.

For declared descriptor `R` and its paired inverse descriptor `I`, effective
endpoint constraints must correspond exactly:

    SourceType(I) = TargetType(R)
    TargetType(I) = SourceType(R)

The two descriptors govern opposite traversals of one semantic occurrence
graph. For every semantic occurrence identity `o`:

    SemanticOccurrence(R, source, target, o)
        if and only if
    SemanticOccurrence(I, target, source, o)

Physical realization of the inverse may temporarily be pending only under the
explicit non-complete outcome defined by the relationship persistence
specification.

Directional cardinalities are not required to match. The declared minimum and
maximum apply to the number of targets per declared source; the inverse
minimum and maximum apply to the number of declared sources per declared
target. A graph conforms only when both directional cardinality policies hold.

Other directional values are not inferred by copying the paired descriptor.
In particular, each direction authors and resolves its own `DeletionSemantic`.

## Descriptor validity

A relationship descriptor is valid only when:

- its source and target each resolve to an admissible holon-type constraint;
- it has at least one effective applicable `CardinalityConstraint`;
- every constraint minimum is non-negative;
- an absent constraint maximum means unbounded; and
- every present maximum is non-negative and not less than its constraint minimum;
- its inverse linkage is bijective and its effective endpoint constraints
  mirror the paired direction as defined above; and
- every required semantic property is explicit after completion.

Inheritance follows the general effective-value rules. No relationship-specific
algorithm may bypass the kernel's `InheritanceRules` table or compute a
competing effective contract. The descriptor semantic rules define the
policy-aware effective collection shapes and the ancestor-before-local
contribution order used by `Additive` inheritance.

Source and target constraints, duplicate and ordering policy, definitional
status, and deletion behavior are read from the relationship's effective member
definition rather than directly from local descriptor state. The cardinality
constraint is read from the relationship descriptor's effective `Constraints`
collection and is applicable only to the relationship Instance TypeKind.

## Occurrence conformance

After relationship-name binding, conformance groups declared occurrences by
resolved relationship descriptor identity and considers the complete
policy-aware effective target collection rather than validating serialized
fragments independently. A relationship admitted only by the effective
additional-relationship policy remains unbound and is grouped by its exact
stored name within the relationship namespace.

- The source and every target must satisfy the descriptor's endpoint
  constraints.
- The total target count must satisfy the effective cardinality constraint.
- When duplicates are disallowed, the same semantic target may not appear more
  than once in authored local occurrences. Additive inheritance normalizes
  identity-equal inherited and local contributions to one effective occurrence
  while retaining their provenance.
- When duplicates are allowed, distinct occurrences must retain occurrence
  identity as required by the runtime persistence contract.
- An ordered relationship requires valid authoritative ordering metadata for
  each occurrence; incidental storage or insertion order is not semantic
  order.

### Stored occurrences and effective values

The declared occurrence is the authoritative authored fact. Commit derives
and materializes the paired inverse occurrence for traversal. An inverse
descriptor therefore traverses inverse occurrences corresponding to stored
declared occurrences; it is not an automatic reverse index over virtual edges
introduced by semantic inheritance on the declared descriptor.

The local value collection for an inverse member consists of those materialized
inverse occurrences. Ordinary `EffectiveValues` resolution applies the
kernel-selected rule for that inverse relationship across the inverse source
holon's own `Extends` lineage. It does not reverse the declared direction's
independently resolved `EffectiveValues` collection.

Consequently:

- `Instances` supports discovery because every holon has an explicit
  `DescribedBy` occurrence and commit must materialize its inverse; and
- `KeyRuleForInstancesOf` returns holon types that explicitly populate
  `InstanceKeyRule`, not every descendant type that effectively inherits that
  selection through `Override`.

A query for all types effectively governed by a key rule must evaluate each
candidate type's effective `InstanceKeyRule`; it is not an ordinary inverse
occurrence traversal.

### Deletion semantics status

> **Status: Proposed.** Schema 2.0 requires an effective directional
> `DeletionSemantic` on both declared and inverse descriptors, but the
> operational interaction between the pair is not yet normative.

The final deletion design must specify:

- which directional descriptor is evaluated when either endpoint is deleted;
- whether and when a policy on a derived inverse occurrence blocks deletion;
- the `Allow`, `Block`, and `Cascade` outcome matrix for every declared/inverse
  policy combination and deletion direction;
- cascade-closure construction, occurrence removal, and cycle termination; and
- transaction behavior when a cascade crosses a non-local boundary whose inverse materialization
  is deferred.

Until that design is accepted, validators may require and type-check each
direction's authored value, but must not treat a particular pairwise deletion
algorithm as settled by this specification.

Validation accumulates independently detectable violations as specified by the
[descriptor semantic rules](descriptor-semantics-rules.md).

## Persistence and runtime boundaries

Relationship occurrence identity, forward/inverse commit outcomes, retry, and
repair belong to the
[relationship persistence specification](../transactions/relationship-persistence-design-spec.md).
That specification also owns execution of any eventual deletion plan across
materialized occurrence pairs and transaction boundaries.

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

Relationship endpoint declarations, duplicate policy, ordering policy,
definitional status, and deletion semantics remain descriptor members. This
specification does not introduce a generic `RelationshipConstraint` wrapper for
those heterogeneous concepts, specialized relationship pairs for each
constraint category, or a relationship between `CardinalityConstraint` and a
`ValidationRule`. `DS-CARD-001` remains the stable validation and diagnostic
identity for evaluating the effective cardinality constraint.
