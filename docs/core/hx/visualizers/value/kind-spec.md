# Value VisualizerKind

## Status and authority

Draft normative specification for this kind's semantic boundary and common
promises. Concrete implementations own their internal grammar. Shared DAHN
selection, runtime, allocation, and state contracts apply; this document does
not create a separate selection authority.

## Semantic subject and specialization

One value governed by its declared ValueType and applicable semantic context.
Value Visualizers support diverse ways of presenting and interacting with that
value, including inspection, permitted editing, validation feedback, compact
representation, and specialized interaction. Semantic validation stays with MAP.

ValueType describes the data and its semantics. VisualizerKind classifies a
visualization capability. Specialized Value kinds may reflect stable value-type
semantics, without requiring a mechanically identical hierarchy or a single
renderer per ValueType. This specification retains `Value` as the family name;
“ValueType-specific Visualizer” describes applicability, not a renamed data type.

## Selection and binding

A composition owner defines the slot's required contract, bound value, declared
ValueType, property metadata where applicable, interaction mode, and constraints.
DAHN selection chooses an applicable, conforming Visualizer; the runtime binds
it to the actual value and context. A ValueType is selection input, not a
hard-coded renderer assignment. Compatible occurrences can reuse an established
binding without fresh candidate discovery, including a Rust-validated,
subject-dependent developer default. Automatic/default rendering creates no
durable personal Usage by itself.

A person can retain a preferred date interactor once at agent/context scope,
including localization and calendar behavior where supported, across compatible
experiences. Composition-specific configuration can override it locally without
replacing that cross-cutting preference. Read-only dates, editable dates, and
date ranges can require different contracts: preference never waives eligibility.
Configuration applicability uses indexed personal records and available ancestry
metadata under [DAHN §11.1](../../dahn-design-spec.md#111-visualizerusage), not
repeated backend Usage-discovery walks for each value.

PropertyMap Visualizers may directly compose value slots alongside independent
property-name label slots. Other Visualizers may also compose Value slots;
Value visualization has no intrinsic dependency on PropertyMap or on a property.

## Internal authority

The selected Visualizer owns value presentation and interaction within the
parent's allocation and participation constraints. The parent owns placement,
label/value pairing where applicable, and external allocation. A child may
compose further child slots when its realization requires them.

Editability is determined by the supplied role and semantic permissions, not by
the availability of an editor implementation. MAP remains authoritative for
semantic validation and staged mutation. VisualizerUsage records agent-relative
configuration and usage; the Visualizer fulfills the slot contract.

## Specialized families

- [String](string/kind-spec.md) — string presentation and interaction, including
  use in a property-name label role.

Create further kind directories on demand only, when an actual documentation
need establishes a meaningful semantic boundary. Do not preallocate one for
every ValueType. Multiple concrete Visualizers may fulfill a specialized kind.
