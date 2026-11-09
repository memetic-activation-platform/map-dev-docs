# Key Relationship Parameters — Design Proposal

> **Status: unresolved.** These alternatives are inputs to VAL-C3c-1 design reconciliation,
> tracked in [map-dev-docs #87](https://github.com/memetic-activation-platform/map-dev-docs/issues/87),
> not accepted architecture. Accepted decisions must be recorded in the governing specifications.

## Relationship-parameter alternatives

Consider configured, typed `FormatRule` parameters instead of a theme-specific, unconfigured
`RelationshipPairRule` algorithm. The current `TemplateParameters` contract admits only property
descriptors; relationship inputs would require an explicit vocabulary change. Decide parameter
kind, singularity, scalar rendering, exact selected target version, and errors for missing,
ambiguous, or keyless targets.

One preference is to read an explicitly present target key instead of recursively recomposing it.
Under that approach, targets would be composed first and incomplete or cyclic construction
dependencies would be diagnosed. This is a proposal, not a resolution of composition ordering.

For theme assignments, consider a declared assignment-to-theme input. An alternative is bounded
owner evidence from authored theme-side occurrences. The design must address availability during
standalone staging/runtime composition and bounded ambiguity detection, rather than assume an
inverse that appears only after persistence.

## Descriptor-family policy preferences

The earlier planning preference was to retain `{TypeName}.HolonType` for ordinary holon types and
existing conventions for `ExtendedTypeRule` families. Confirm the describing populations and
consequences for roots and meta-types before accepting policy placement or changing a shared
meta-type's rule. Distinguish the rule on `D(T)` governing descriptor `T` from the rule on `T`
governing its instances, as specified by
[instance-key selection](../type-system/schema-design-spec.md#91-instancekeyrule).

## Accepted boundaries

These questions operate within the descriptor runtime's
[key composition boundary](../core-runtime/descriptors/descriptors-design-spec.md#key-composition-boundary),
`DS-KEY-006`'s rule that mutating a key-producing relationship input is definitional, and the
existing [enum-owner contract](../type-system/schema-design-spec.md#93-descriptor-keys). Which
relationships may supply key inputs, and how their definitional status is declared, is still open
(see [key-producing relationship inputs](../type-system/schema-design-spec.md#key-producing-relationship-inputs)).

The [delivery checklist](../validation/commit-validation-impl-plan.md#val-c3c-1--design-reconciliation-and-harness-feasibility)
tracks reconciliation, harness feasibility, and downstream implementation units.
