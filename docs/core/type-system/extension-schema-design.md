# Extension Schema Design

> **Status: Work in progress.** This document is a placeholder for a future
> design effort. It is not an authoritative specification of Extension Schema
> behavior.

## Intended scope

This document will define the universal rules governing schemas that extend
types owned by MAP Core or by another extender. Its intended concerns include:

- cross-schema ownership and identity;
- legal extension and reference relationships;
- schema dependencies and binding;
- compatibility, conflicts, and evolution; and
- the boundary between universal extension rules and component-specific use.

Until those rules are designed and accepted, the
[schema design specification](schema-design-spec.md) governs only the common
Schema 2.0 structure. The documents under
[adaptive systems](../adaptive-systems/index.md) preserve important extension
use cases, but they are not the general authority for Extension Schema
semantics.

No implementation should infer unsettled extension behavior from this
placeholder.

The common structural baseline is nevertheless settled: versioned schema
`DependsOn` relationships form a DAG, and every direct cross-schema descriptor
reference requires a direct dependency on the target schema version. The
future Extension Schema design must build its ownership, compatibility, and
evolution rules on that baseline rather than reintroducing dependency cycles.
