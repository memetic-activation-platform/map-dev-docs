# Reference-Layer-to-Command Exposure Matrix

## Status

**Command TRU1 implementation verification complete. Space Navigator vertical
slices now drive the implementation of any required lower-layer exposure.**

This matrix defines the direction of dependency for the MAP interaction
surface:

```text
Core shared objects and reference layer
  -> MAP Commands (selected IPC wrappers and Dance ingress)
    -> TypeScript MAP SDK (typed wrappers over Commands)
      -> DAHN (experience composition)
```

It is an inventory and exposure decision record, not a proposal to create a
second descriptor, query, or DAHN-specific semantic layer.

## Delivery Rule After Command TRU1

A concrete Space Navigator PR owns the Commands, wire, SDK, Dance, or core
work required by its acceptance criteria. It must add only the lower-layer
surface needed by that slice. A separately reviewable prerequisite is permitted
when necessary, but remains explicitly tied to that Navigator PR rather than
becoming a generic bottom-up Commands expansion.

The first such owner is Space Navigator Phase 0 PR 1 — DAHN TypeScript MAP
Adapter. It owns the thin descriptor/discovery exposure required to inspect a
holon generically. Phase 0 PR 3 owns the later Rust-side visualizer-selection
Command boundary. Effective Dance discovery is owned by the later Phase 1 PR 9
classification slice, not by Phase 0.

## 1. Decision Rules

1. A Command exists only to expose a meaningful core/reference-layer operation
   through the IPC boundary, or to provide canonical Dance ingress.
2. The TypeScript SDK wraps Commands. It must not recreate absent core behavior
   with TypeScript state, inheritance traversal, descriptor projections, or
   query DTOs.
3. If a needed operation is absent from the reference layer, extend the core
   reference layer (and, where necessary, the shared-objects layer) first. Add
   a Command only after that operation has a coherent core contract.
4. Descriptor-effective results are computed views. They need not be eagerly
   materialized as an `EffectiveDescriptor` artifact in order to be exposed.
5. Commands preserve the core operation's semantic result family. In
   particular, plural holon-backed results remain `HolonCollection`; descriptor
   results are descriptor-backed references or handles, not DAHN DTOs.
6. A documented API is not treated as implemented merely because it appears in
   an older guide. The status column records this explicitly.

## 2. Evidence and Status Vocabulary

| Status | Meaning |
| --- | --- |
| **Normative** | Required by a current design specification. |
| **Documented, unverified** | Present in the Rust API guide, which says it needs updating; implementation must be checked in `map-holons`. |
| **Existing Command** | Present in the current Commands target surface. It does not by itself prove implementation. |
| **Expose after core verification** | Candidate Command wrapper once the underlying reference-layer API and IPC result mapping are confirmed. |
| **Do not expose yet** | Deliberately internal, obsolete, or lacking a stable core contract. |

The current descriptor specifications are normative for effective descriptor
semantics. `docs/core/rust-api.md` is useful as an inventory lead, but is
explicitly marked as needing an update and includes superseded query/dance
language.

## 3. Core Principle: Effective Surface Without Materialization

`ReadableHolon::holon_descriptor()` is the instance entry point to the
descriptor runtime. `HolonDescriptor::instance_properties()`,
`instance_relationships()`, `afforded_dances()`, and `afforded_commands()`
return effective results unless their names explicitly say `local_*`.

Therefore the first Navigator does **not** require an `EffectiveDescriptor`
holon or a TypeScript materialization of inherited descriptor state. It needs
Commands which faithfully expose these reference-layer operations after their
concrete Rust and wire result shapes are verified.

## 4. Matrix

### 4.1 Instance resolution and ordinary reads

| Core/reference-layer affordance | Evidence status | Current Command exposure | Exposure decision | Space Navigator relevance |
| --- | --- | --- | --- | --- |
| Bind a wire holon identity to an opaque `HolonReference` handle under lifecycle/access rules | Normative reference-layer responsibility | Binding occurs before command execution; no independent read command is specified | Keep as binding/reference behavior. Commands invoke reference-layer capabilities through the handle; they never resolve or transfer an underlying `Holon` object, and TS receives no resolver | Every displayed occurrence is addressed through this handle. |
| `key()` | Documented, unverified | `ReadableHolonAction::Key` | Existing Command | Useful title/identity fallback. |
| `versioned_key()` | Documented, unverified | `ReadableHolonAction::VersionedKey` | Existing Command | Version/provenance display. |
| `holon_id()` | Documented, unverified | `ReadableHolonAction::HolonId` | Existing Command | Stable identity and occurrence bookkeeping. |
| `predecessor()` | Documented, unverified | `ReadableHolonAction::Predecessor` | Existing Command | Version lineage; not required for first read-only navigation. |
| `property_value(name)` | Documented, unverified | `ReadableHolonAction::PropertyValue` | Existing Command | Required generic scalar display once the descriptor has identified the property. |
| `related_holons(name)` | Documented, unverified | `ReadableHolonAction::RelatedHolons` returning `HolonCollection` | Existing Command | Required singular/plural relationship traversal. |
| `all_related_holons()` | Documented, unverified | Explicitly excluded from v0 Commands | Do not expose until a bounded, descriptor-aware bulk-read contract is justified | Avoids an accidental eager graph-load API. |

### 4.2 Effective descriptor access and affordance discovery

| Core/reference-layer affordance | Evidence status | Current Command exposure | Exposure decision | Space Navigator relevance |
| --- | --- | --- | --- | --- |
| `holon_descriptor()` | Implementation verified | None named in current command enum | Phase 0 PR 1 may expose it as a generic reference transport result and typed SDK descriptor handle. | Required to derive generic node structure. |
| `instance_properties()` | Implementation verified | None named | Phase 0 PR 1 may expose ordered descriptor references through the existing plural transport and typed SDK handles when its adapter needs them. | Required to enumerate effective scalar/property affordances. |
| `available_relationships()` | Implementation verified | None named | Phase 0 PR 1 may expose it through ordered `QualifiedRelationshipWire { descriptor: HolonReferenceWire, direction: Declared \| Inverse }`. A plain `HolonCollection` would lose direction. | Required to classify and offer only lifecycle-valid singular/plural traversal, including qualified direction. |
| `instance_relationships()` | Normative effective operation | None named | Defer as static descriptor metadata until a caller needs the declared contract independently of instance availability | It must not cause the Navigator to offer an inverse traversal unavailable in the current reference state. |
| effective property lookup by member name | Normative capability | None named | Expose only if the initial descriptor-handle API needs it; otherwise enumerate then use member names | Useful for incremental/property-focused reads. |
| effective relationship lookup by member name | Normative capability | None named | Expose only if it removes a real round trip or ambiguity | Useful for targeted traversal. |
| `afforded_dances()` | Implementation verified | None named; `DanceV2` executes an already-built invocation | Phase 1 PR 9 may expose it as descriptor discovery, separate from execution. | Required for pre-invocation dance-result classification and later action menus. |
| `afforded_commands()` | Implementation verified | None named | Defer descriptor discovery until the generic command-menu slice (`PRS2+`). | Required for a descriptor-driven action surface, once command affordances are meaningful. |
| descriptor header and member-definition accessors | Normative schema-backed convenience | None named | Expose through thin typed descriptor handles; do not create a bespoke descriptor JSON projection | Required for labels, ordering/presentation metadata, cardinality, and value-type inspection. |
| effective value constraints, key rules, endpoint compatibility, and operator affordances | Normative effective operations | None named | Defer individual wrappers until a concrete caller needs each; preserve descriptor ownership | Needed later for editing, target selection, and query construction—not all for first read-only navigation. |

### 4.3 Mutation and transaction operations

| Core/reference-layer affordance | Evidence status | Current Command exposure | Exposure decision | Space Navigator relevance |
| --- | --- | --- | --- | --- |
| Begin transaction / transaction context creation | Current Commands contract | `SpaceCommand::BeginTransaction` | Existing Command | Required only when entering staged work or when a transaction-scoped read is selected. |
| Create transient holon | Documented, unverified | `TransactionAction::NewHolon` | Existing Command | Later create flow. |
| Stage new holon / clone / version | Documented, unverified | `StageNewHolon`, `StageNewFromClone`, `StageNewVersion`, `StageNewVersionFromId` | Existing Commands | Later edit/create/clone flow. |
| Commit | Documented, unverified | `Commit` | Existing Command | Later canvas-scoped transaction action. |
| Delete staged holon | Documented guide gives lifecycle context; current Commands specifies `DeleteHolon` | `DeleteHolon` | Existing Command | Later staged deletion flow. |
| `with_property_value()` / `remove_property_value()` | Documented, unverified | Corresponding writable holon actions | Existing Commands | Later scalar editing. |
| `add_related_holons()` / `remove_related_holons()` | Documented, unverified | Corresponding writable holon actions using `HolonCollection` at the command boundary | Existing Commands | Later relationship editing. |
| `with_descriptor()` | Documented, unverified | `WithDescriptor` | Existing Command | Core/schema construction concern; not a generic Navigator edit affordance. |
| `with_predecessor()` | Documented, unverified | Excluded from current Commands v0 | Do not expose without a current lifecycle/versioning decision | The guide is older than the present command contract. |
| `populate_defaults()` | Normative writable completion service | None named | Do not expose as a generic UI command; loader/creation orchestration owns it | A later create flow may invoke it through the creation service, not through DAHN. |

### 4.4 Collections, query, and dances

| Core/reference-layer affordance | Evidence status | Current Command exposure | Exposure decision | Space Navigator relevance |
| --- | --- | --- | --- | --- |
| `HolonCollection` iteration/membership helpers | Documented, unverified | Returned/accepted as a shared runtime type, not remote methods | Keep local to the receiving runtime representation; do not make each helper a Command | Collection visualizers consume returned collections. |
| Direct query execution | Normative Query runtime peer API | No first-class `Query` command | Do not expose directly through Commands | Commands enter query behavior only through `QueryDance`. |
| `QueryDance` | Normative Dance adapter | `TransactionAction::DanceV2(DanceInvocation)` | Existing canonical ingress once Dance invocation construction is delivered | Needed when the Navigator selects reusable query semantics, not for a simple named relationship read. |
| Dance invocation binding/execution | Normative Dance runtime operation | `DanceV2` | Existing canonical ingress | Later node actions and dance-result navigation. |
| Dance discovery and response-shape inspection | Normative descriptor operation | No Command wrapper yet | Expose descriptor handles/discovery before adding DAHN dance UI; keep invocation separate | Needed to classify actions and result shape before execution. |
| Legacy `run_query(QueryExpression) -> NodeCollection` | Documented, unverified and superseded | Removed from target Commands | Do not expose | Must not re-enter via SDK or DAHN. |

## 5. First Read-Only Navigator Command Set

The minimal command set is intentionally narrower than a descriptor portfolio:

1. Existing ordinary reads: identity, named property value, and named related
   holons.
2. New wrappers only for verified reference-layer descriptor operations:
   `holon_descriptor`, effective instance properties, available relationships,
   and the typed descriptor/member access needed to interpret them.
3. Effective Dance discovery and typed Dance request/response metadata only
   when Phase 1 PR 9 reaches descriptor-driven action/result classification.
   Dance invocation remains separate.
4. `DanceV2` only when the shared host-side invocation builder and response
   lifecycle are delivered.

The set deliberately excludes a materialized `EffectiveDescriptor` transfer,
`all_related_holons`, a standalone query command, client-side inheritance
merging, and TypeScript-owned semantic caches.

## 6. Verification Work Before Creating New Commands

For every row marked **Expose after core verification**, verify in
`map-holons`:

1. the concrete trait/wrapper signature and error behavior;
2. lifecycle and access-control behavior for transient, staged, and saved
   references;
3. whether the result already has a canonical wire-safe representation;
4. whether the operation is a stable caller-facing affordance rather than an
   internal helper; and
5. the corresponding `MapResult` / `MapResultWire` decoding rule.

If any operation fails step 1 or 4, extend the reference/shared-objects layer
first. The resulting Command must remain a thin adapter; it must not calculate
effective descriptor state, authorization, query semantics, or UI projections.

## 7. Consequences for the Commands and Dance Plans

- The Commands plan should be organized around verified core-affordance
  exposure, not a DAHN-specific descriptor API.
- Descriptor-afforded command and dance discovery are reference-layer products
  exposed through Commands; they are not replacement command-routing systems.
- `DanceV2` remains the sole new-world Dance ingress.
- `QueryDance` remains the sole Command-mediated query path; no
  `TransactionAction::Query` migration path should remain in the plan.
- The TypeScript SDK plan follows this matrix mechanically after Command result
  mapping is specified.

## References

- [MAP Runtime Descriptor Subsystem Design Spec](../core-runtime/descriptors/descriptors-design-spec.md)
- [Descriptor Facades and Effective Access Specification](../descriptors/descriptors-design-spec.md)
- [MAP Commands Specification](commands.md)
- [MAP Dances Design Specification](../dances/dances-design-spec.md)
- [MAP Query Architecture](../map-queries/query-arch.md)
- [MAP Rust-API Developer Guide](../rust-api.md) — inventory lead only; not
  current normative authority.
