# Key Relationship Parameters — Design Proposal

> **Status: deferred.** General relationship parameters remain a proposal.

[`RelationshipPairRule`](../hx/dahn-design-spec.md#453-themes-and-complete-assignment)
covers the bounded Theme assignment case. `FormatRule` uses ordered property
descriptors for `TemplateParameters`.

A general facility would need to define parameter kinds, exact target selection,
scalar projection, and handling of missing, ambiguous, or keyless targets. Use
the [key composition contract](../type-system/schema-design-spec.md#96-key-composition-and-identity-contract)
as the starting point.

The proposed `IdentifyingInverse` marker, a derived read-only view of staged
inverse occurrences, and changes to physical link ownership each need their own
consumer or persistence justification. A read-only inverse view must preserve
provenance identifying the exact authored forward occurrence. Key composition uses
authored forward occurrences as [declaring-owner evidence](../type-system/schema-design-spec.md#declaring-owner-evidence).
