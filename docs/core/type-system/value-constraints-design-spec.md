# Value Constraints Design Spec

## Purpose and authority

This specification defines the Schema 2.0 model and representation-neutral
semantics for constraints that refine the values accepted by a `ValueType`.
Exact descriptor identities and declarations are authoritative in the Core
Schema TDL corpus under `map-holons/schema-src`.

The [schema design specification](schema-design-spec.md) owns the surrounding
structural model. The
[descriptor semantic rules](descriptor-semantics-rules.md) own effective-value
calculation and conformance orchestration. This document owns the specialized
meaning of value-constraint declarations.

## Model

`ValueConstraintType.HolonType` is the abstract root of the constraint-type
hierarchy. Schema 2.0 currently defines family anchors for:

- `StringValueConstraint.ValueConstraintType`;
- `IntegerValueConstraint.ValueConstraintType`;
- `BytesValueConstraint.ValueConstraintType`; and
- `ValueArrayConstraint.ValueConstraintType`.

A constraint is an ordinary descriptor-backed holon. Its concrete describing
type determines the constraint rule, and its properties supply the parameters
for that rule.

Value types attach constraint holons through family-specific `Constraints`
relationships. Each relationship targets the matching constraint family and
uses `InheritanceMode Override`. A local constraint set therefore replaces the
nearest inherited set for that value-type family; constraint sets are not
implicitly unioned across the lineage.

## Current executable constraints

| Value family | Constraint type | Required parameter semantics |
|---|---|---|
| String | `MinimumLength.StringValueConstraint` | `ConstraintLength` is the inclusive minimum character count |
| String | `MaximumLength.StringValueConstraint` | `ConstraintLength` is the inclusive maximum character count |
| Integer | `MinimumValue.IntegerValueConstraint` | `ConstraintIntegerValue` supplies the boundary and `ConstraintIsInclusive` selects inclusive or exclusive comparison |
| Integer | `MaximumValue.IntegerValueConstraint` | `ConstraintIntegerValue` supplies the boundary and `ConstraintIsInclusive` selects inclusive or exclusive comparison |
| Value array | `MinimumItems.ValueArrayConstraint` | `ConstraintItemCount` is the inclusive minimum item count |
| Value array | `MaximumItems.ValueArrayConstraint` | `ConstraintItemCount` is the inclusive maximum item count |
| Value array | `UniqueItems.ValueArrayConstraint` | `ConstraintEnabled` controls duplicate rejection |

The TDL corpus, not this table, owns the exact inventory. Adding another
constraint requires a corresponding schema declaration and recognized semantic
implementation; arbitrary descriptor data does not become executable merely by
resembling a constraint.

## Constraint validity

A valid constraint declaration satisfies all of the following:

- its describing type belongs to the family accepted by the value type's
  `Constraints` relationship;
- every required parameter is present and has the declared value type;
- lengths and item counts are non-negative;
- a combined minimum and maximum is internally consistent; and
- the constraint kind is supported by the semantic implementation that claims
  to execute it.

Invalid constraint declarations make the owning value-type contract invalid.
They are not silently ignored or treated as advisory.

## Value conformance

For a value `V` declared by value type `T`, conformance is evaluated against
the effective constraint set of `T` after ordinary descriptor inheritance and
`Override` semantics have been resolved.

When a property descriptor selects `T`, the property validator obtains that
selection and the applicable property semantics from the property's
`EffectiveMemberDefinition`; it does not assume the property's locally
populated fields are its complete definition. The value type's own effective
constraint set is then resolved independently through its descriptor-authored
inheritance policy.

- Integer minimum and maximum constraints honor their inclusive/exclusive
  flags.
- String lengths count Unicode 17.0.0 extended grapheme clusters using the default extended
  grapheme-cluster rules of UAX #29. Segmentation operates on the stored string without Unicode
  normalization; canonically equivalent strings may therefore have different stored forms even
  when they produce the same cluster count.
- Value-array item constraints apply to the array as represented by its value
  type; enabled uniqueness rejects duplicate values under canonical MAP value
  equality.
- Every applicable supported constraint must pass.

All runtimes must produce identical boundaries for the Unicode 17.0.0
`GraphemeBreakTest.txt` conformance data and shared focused fixtures. The Rust implementation must
pin a Unicode-segmentation dependency whose tables implement that version; upgrading those tables
is a semantic-versioned validation change, not an incidental dependency refresh.

Constraint failures are conformance violations and should identify the value
type, constraint type, configured boundary, and observed value or measure.

## Boundaries

This specification does not define:

- property or relationship cardinality;
- relationship endpoint constraints;
- source-language syntax for authoring constraints;
- Rust wrapper or cache representations;
- PVL rules; or
- implementation sequencing.

TDL authoring delegates to the [TDL specification](tdl/tdl-spec.md). Runtime
validation invokes these semantics through the descriptor kernel as described
by the [validation architecture](../validation/validation-arch.md).
