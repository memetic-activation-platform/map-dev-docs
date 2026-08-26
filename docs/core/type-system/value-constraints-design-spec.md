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
hierarchy. Core value constraints are direct descendants of that root; they do
not inherit from string-, integer-, bytes-, or value-array-specific constraint
families merely to obtain configuration members.

A constraint is an ordinary descriptor-backed holon. Its concrete describing
type determines the semantic invariant and parameter contract; its properties
supply the configuration for one type definition. The constraint type declares
the descriptor families to which it is applicable through
`ApplicableToDescriptorTypes`. It does not acquire applicability merely from
its name or from a validator implementation.

Value types attach constraint holons through the generic `Constraints`
relationship. `DS-CONSTRAINT-002` requires every target to be applicable to the
constrained value descriptor through its `Extends` lineage; the generic relationship is not
replaced by family-specific relationship pairs. The kernel's
`InheritanceRules` table assigns `Constraints` the `Additive` rule: subtypes
retain inherited constraints and may add constraints that narrow the accepted-
value set. A local weaker constraint is redundant at best and must be rejected
when it attempts to relax a supertype constraint.

#### DS-CONSTRAINT-001: Constraint monotonicity

`DS-CONSTRAINT-001` is defined generically by the descriptor-kernel semantic
rules. For value constraints, the effective accepted-value set of a subtype
must be a subset of, or equal to, the accepted-value set of its parent. Because
`Constraints` is additive, a subtype cannot remove an inherited constraint;
all inherited and local constraints must pass. A locally authored bound may be
individually broader than an inherited one if the *combined* effective set is
still narrower (for example, an inherited `1..10` range plus local `0..9`
still accepts only `1..9`). Authoring tools may diagnose a dominated or
redundant contribution, but it is not a competing override mechanism.

## Initial normalized constraint types

| Value family | Concrete constraint type | Configuration carried by each constraint holon |
|---|---|---|
| String | `LengthConstraint.ConstraintType` | Optional lower and upper grapheme-cluster bounds, each with its own inclusivity indicator |
| Integer | `NumericRangeConstraint.ConstraintType` | Optional lower and upper integer bounds, each with its own inclusivity indicator |
| Value array | `ItemCountConstraint.ConstraintType` | Optional lower and upper item-count bounds, each with its own inclusivity indicator |
| Value array | `UniqueItemsConstraint.ConstraintType` | Presence of the constraint requires duplicate rejection; it has no enable/disable parameter |

The paired `MinimumLength` / `MaximumLength`, `MinimumValue` / `MaximumValue`,
and `MinimumItems` / `MaximumItems` constraint types are superseded by the
single normalized types above. They must not remain Core executable constraint
types, aliases, or a second authoring representation. The old
`ConstraintLength`, `ConstraintIntegerValue`, `ConstraintItemCount`,
`ConstraintIsInclusive`, and `ConstraintEnabled` one-bound configuration
model is likewise superseded.

### Bound configuration contract

Each bounded normalized constraint holon has this exact Core property contract:

| Property key | Value | Presence |
|---|---|---|
| `Minimum` | non-negative integer lower bound | optional |
| `Maximum` | non-negative integer upper bound | optional |
| `MinimumIsInclusive` | Boolean | required if and only if `Minimum` is present |
| `MaximumIsInclusive` | Boolean | required if and only if `Maximum` is present |

At least one bound is required. When both bounds are present, the minimum must
be less than the maximum, or equal only when both bounds are inclusive. An
exclusive lower bound admits values strictly greater than its configured
minimum; an exclusive upper bound admits values strictly less than its
configured maximum. These conditions are part of the constraint family's
configuration semantics, not an optional validator convention.

For example, the Core type declaration and one configured string constraint
have this shape:

```tdl
holon LengthConstraint.ConstraintType {
  type MetaConstraintType.MetaHolonType
  extends ConstraintType.HolonType
  relationships {
    InstanceProperties -> [
      Minimum.PropertyType,
      Maximum.PropertyType,
      MinimumIsInclusive.PropertyType,
      MaximumIsInclusive.PropertyType
    ]
    ApplicableToDescriptorTypes -> StringValueType.ValueType
  }
}

instance DisplayName.LengthConstraint {
  type LengthConstraint.ConstraintType
  Minimum 1
  MinimumIsInclusive true
  Maximum 120
  MaximumIsInclusive true
}

value DisplayName.StringValueType {
  type MetaStringValueType.MetaValueType
  extends StringValueType.ValueType
  relationships {
    Constraints -> DisplayName.LengthConstraint
  }
}
```

`NumericRangeConstraint.ConstraintType` and
`ItemCountConstraint.ConstraintType` declare the same four bound
properties and are attached through the same generic `Constraints` relation.
Their measurement differs: integer value, array item count, and Unicode
grapheme-cluster length respectively. `UniqueItemsConstraint` instead has no
configuration property: attaching the instance is the affirmative commitment.

Each concrete constraint type declares its actual descriptor-family targets:
`LengthConstraint` targets `StringValueType.ValueType`,
`NumericRangeConstraint` targets `IntegerValueType.ValueType`, and the item-count
and unique-items constraints target `ValueArrayValueType.ValueType`. A broad
constraint may instead target `ValueType.TypeDescriptor`. `DS-CONSTRAINT-002`
uses normal `Extends`-lineage compatibility; it needs no second fixed
representation-compatibility check or capability taxonomy.

The TDL corpus owns these declarations and the runtime owns their static
implementations. Arbitrary descriptor data does not become executable merely
by resembling a constraint. A validation-rule identity may provide stable
diagnostics or dispatch for that implementation, but it does not carry a
second copy of these parameters.

## Constraint validity

A valid constraint declaration satisfies all of the following:

- its concrete describing type is a `ConstraintType` applicable to the value
  descriptor through `ApplicableToDescriptorTypes` and its `Extends` lineage;
- every required bound indicator is present exactly when its bound is present
  and has the declared Boolean value type;
- every bound is a non-negative integer;
- at least one bound is present and a combined minimum and maximum is
  internally consistent under the bound configuration contract; and
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

- Numeric-range, length, and item-count constraints honor each configured
  lower or upper bound and its own inclusive/exclusive indicator.
- String lengths count Unicode 17.0.0 extended grapheme clusters using the default extended
  grapheme-cluster rules of UAX #29. Segmentation operates on the stored string without Unicode
  normalization; canonically equivalent strings may therefore have different stored forms even
  when they produce the same cluster count.
- Value-array item-count constraints apply to the array as represented by its
  value type; `UniqueItemsConstraint` rejects duplicate values under canonical
  MAP value equality.
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
- relationship endpoint type declarations;
- source-language syntax for authoring constraints;
- Rust wrapper or cache representations;
- PVL rules; or
- implementation sequencing.

TDL authoring delegates to the [TDL specification](tdl/tdl-spec.md). Runtime
validation invokes these semantics through the descriptor kernel as described
by the [validation architecture](../validation/validation-arch.md).
