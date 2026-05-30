# MAP Value Type Import Guide (v2.0)

## ChangeLog

### v2.0

- aligns value type import guidance with the MAP Type System v2.0 meta-schema model
- removes the former `TypeDescriptor` / `MetaTypeDescriptor` recursion pattern
- treats `MetaValueType` as the TypeKind-specific meta-type that describes value type descriptors
- treats `ValueType` as the abstract inheritance anchor for value type descriptors
- removes the old non-descriptor constraint-facet pattern from `Extends`
- clarifies that value descriptors use single inheritance and may not extend both `ValueType` and a separate constraint facet

---

## 1. Starting Point: Value Types as Descriptors

In MAP, a value type definition is represented as a type descriptor holon.

A concrete value type descriptor:

- is `DescribedBy` `MetaValueType`
- declares a value-related `TypeKind`, such as `Value(String)` or `Value(Integer)`
- extends exactly one parent in the value descriptor hierarchy
- usually extends the abstract `ValueType` anchor directly
- belongs to exactly one schema through `ComponentOf`

The JSON import field `type` is shorthand for `DescribedBy`.

Example:

```json
{
  "key": "MapStringValueType",
  "type": "#MetaValueType",
  "properties": {
    "type_name": "MapStringValueType",
    "type_kind": "Value(String)",
    "is_abstract_type": false
  },
  "relationships": [
    { "name": "Extends", "target": { "$ref": "#ValueType" } },
    { "name": "ComponentOf", "target": { "$ref": "#MAP Core Schema" } }
  ]
}
```

This means:

- `MapStringValueType` is a value type descriptor because it is described by `MetaValueType`.
- It inherits the general obligations of value type descriptors by extending `ValueType`.
- It is a concrete descriptor and may be referenced by property descriptors.

---

## 2. Example: General and Specialized String Value Types

Consider two value type descriptors:

- `MapStringValueType`: the general MAP string value type
- `PropertyNameValueType`: a string value type specialized for property names

Both represent string-like scalar values, but they may carry different semantic constraints.

The v2.0 pattern is:

```text
MapStringValueType      --[DescribedBy]--> MetaValueType
MapStringValueType      --[Extends]-----> ValueType

PropertyNameValueType   --[DescribedBy]--> MetaValueType
PropertyNameValueType   --[Extends]-----> MapStringValueType
```

`PropertyNameValueType` chooses `MapStringValueType` as its single parent when it is intended to refine the general string value type. If no refinement chain is desired, it may instead extend `ValueType` directly.

The important invariant is that each descriptor has one inheritance parent. A value type descriptor does not extend both `ValueType` and a separate constraint facet.

---

## 3. Constraint Modeling

The earlier value-type guide used examples such as:

```text
MapStringValueType --[Extends]--> StringValueConstraints
```

That pattern is retired in v2.0.

`Extends` is the type inheritance relationship. Its target must be a real type descriptor, and each type may extend at most one other type. A free-floating object such as `StringValueConstraints` cannot be an `Extends` target unless it is itself modeled as a descriptor in the schema.

Use these rules instead:

- Put scalar runtime representation in `BaseValue` and the MAP base type wrappers.
- Put value-category identity in `TypeKind`, such as `Value(String)` or `Value(Bytes)`.
- Put property-to-value binding on property descriptors through the `ValueType` relationship.
- Put reusable semantic refinements in explicit value type descriptors, using a single inheritance chain.
- Introduce new constraint fields only as explicit schema elements governed by the relevant meta-type design, not as anonymous composition facets.

This preserves the simplification introduced by `DescriptorRoot`: description, inheritance, and instantiation stay separate.

---

## 4. How Property Types Refer to Value Types

Property type descriptors are described by `MetaPropertyType`.

They point to value type descriptors through the `ValueType` relationship.

Example:

```text
Description.Property --[DescribedBy]--> MetaPropertyType
Description.Property --[Extends]-----> PropertyType
Description.Property --[ValueType]---> MapStringValueType
```

Validation should confirm that the `ValueType` target is a value type descriptor:

- The target is described by `MetaValueType` or by an allowed future sub-meta-type of `MetaValueType`.
- The target is concrete unless the schema intentionally allows an abstract value-type anchor.
- The target conforms through `Extends` to `ValueType`.

---

## 5. Why Keys Still Matter

Semantic keys remain important for value type imports.

They allow import files to reference descriptors before permanent storage identifiers exist. For example, a property descriptor can refer to `$ref: "MapStringValueType"` before either descriptor has been committed.

Keys support:

- cross-file linkage between staged descriptors
- ID-free `$ref` expressions in JSON
- relationship validation prior to commit
- deduplication and merging of equivalent descriptors
- semantic lookup in distributed storage

Key behavior is declared through `UsesKeyRule`, inherited from the descriptor model rooted at `DescriptorRoot`.

---

## 6. Import Validation Checklist

When importing value type descriptors:

1. Resolve the `type` field as `DescribedBy`.
2. Confirm ordinary value type descriptors are described by `MetaValueType`.
3. Confirm each descriptor has at most one `Extends` target.
4. Confirm concrete value type descriptors ultimately conform to `ValueType`.
5. Reject references to the removed `MetaTypeDescriptor` model.
6. Reject non-descriptor constraint facets as `Extends` targets.
7. Confirm property descriptors reference valid value descriptors through `ValueType`.
8. Confirm key materialization follows the descriptor's `UsesKeyRule`.

---

## 7. Summary

The v2.0 value type model is intentionally simpler:

- `MetaValueType` describes value type descriptors.
- `ValueType` anchors value descriptor inheritance.
- Concrete value descriptors define reusable scalar semantics.
- Property descriptors reference value descriptors through `ValueType`.
- `BaseValue` remains the runtime scalar representation.
- `Extends` is single inheritance, not a general-purpose constraint composition mechanism.
