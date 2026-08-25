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

`ConstraintType.HolonType` is the abstract root of the generic constraint-type
hierarchy. `ValueConstraintType.HolonType` is its value-family specialization.
Schema 2.0 currently defines value-family anchors for:

- `StringValueConstraint.ValueConstraintType`;
- `IntegerValueConstraint.ValueConstraintType`;
- `BytesValueConstraint.ValueConstraintType`; and
- `ValueArrayConstraint.ValueConstraintType`.

A constraint is an ordinary descriptor-backed holon. Its concrete describing
type determines the semantic invariant and parameter contract; its properties
supply the configuration for one type definition. The constraint type declares
the Instance TypeKinds to which it is applicable through
`ApplicableToInstanceTypeKinds`. It does not acquire applicability merely from
its name or from a validator implementation.

Value types attach constraint holons through the generic `Constraints`
relationship. `DS-CONSTRAINT-002` requires every target to be applicable to the
value type's effective Instance TypeKind; the generic relationship is not
replaced by family-specific relationship pairs. The kernel's
`InheritanceRules` table assigns `Constraints` the `Additive` rule: subtypes
retain inherited constraints and may add constraints that narrow the accepted-
value set. A local weaker constraint is redundant at best and must be rejected
when it attempts to relax a supertype constraint.

#### DS-CONSTRAINT-001: Constraint monotonicity

`DS-CONSTRAINT-001` is defined generically by the descriptor-kernel semantic
rules. For value constraints, it requires the effective accepted-value set of a
subtype to be a subset of, or equal to, the effective accepted-value set of its
parent. A locally authored constraint that is weaker than an inherited
constraint for the same semantic boundary is an attempted relaxation and is
invalid, even though additive resolution would otherwise retain the inherited
constraint. An equal contribution is redundant and may be diagnosed by
authoring tools.

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
resembling a constraint. A validation-rule identity may provide stable
diagnostics or dispatch for that implementation, but it does not carry a
second copy of the constraint parameters.

## Constraint validity

A valid constraint declaration satisfies all of the following:

- its concrete describing type is a `ConstraintType` applicable to the value
  type's effective Instance TypeKind;
- every required parameter is present and has the declared value type;
- lengths and item counts are non-negative;
- a combined minimum and maximum is internally consistent; and
- the constraint kind has the semantic implementation required by the
  applicable validation context.

Invalid constraint declarations make the owning value-type contract invalid.
They are not silently ignored or treated as advisory.

## Value conformance

For a value `V` declared by value type `T`, conformance is evaluated against
the effective constraint set of `T` after ordinary descriptor inheritance and
the kernel's `Additive` rule have been resolved.

When a property descriptor selects `T`, the property validator obtains that
selection and the applicable property semantics from the property's
`EffectiveMemberDefinition`; it does not assume the property's locally
populated fields are its complete definition. The value type's own effective
constraint set is then resolved independently through the kernel inheritance
table.

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

- generic constraint applicability or bootstrap semantics;
- relationship cardinality or other non-value constraint families;
- relationship endpoint constraints;
- source-language syntax for authoring constraints;
- Rust wrapper or cache representations;
- PVL rules; or
- implementation sequencing.

TDL authoring delegates to the [TDL specification](tdl/tdl-spec.md). Runtime
validation invokes these semantics through the descriptor kernel as described
by the [validation architecture](../validation/validation-arch.md).
