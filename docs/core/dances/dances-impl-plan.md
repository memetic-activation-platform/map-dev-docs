# Dance Implementation Plan (v2.1)
## Delivery Sequence for the Name-Addressed Holonic Dance Model

## Change Log

### v2.1

- aligns the plan with Issue 17's name-addressed Dance contract and clean
  cutover sequence
- makes name-addressed `DanceInvocation` the prerequisite Dance cutover while
  deferring structural contract validation to the shared Validation track
- uses `TypeDescriptor.TypeName` as the canonical `DanceName`, with
  `DanceInvocation.DanceName` as the invocation target
- replaces `DanceInput` / `DanceInputFor` with `RequestType` /
  `RequestTypeFor` and `InvokesDance` / `InvokedBy` with local name resolution
- requires `HolonSpace` affordance for `LoadHolons` and `QueryDance`
- records shared Descriptor-Aware Holon Validation as a follow-up integration,
  not a prerequisite for the name-addressed foundation
- treats the cutover as clean-slate work: no legacy bridge or compatibility
  retention is required
- keeps QueryDance engine execution, dynamic implementation selection, and
  TrustChannel/Agreement authorization as later or separate work

### v2.0

- regenerated the implementation plan from a then-revised Dance specification
- treats Dance `PRO1` as delivered and fixed in scope
- removes the older plan's center of gravity around query-contract cleanup and
  pre-revision envelope evolution
- re-centers implementation work on `DanceInvocation` and `DanceResponseType`
  as transient holons
- re-centers implementation work on `DanceType.RequestType`
- re-centers implementation work on
  `DanceResponseType.ResponseBody -> HolonType`
- re-centers implementation work on `Projection` and `TransientHolonType` for
  projection/query results
- re-centers implementation work on descriptor-afforded lookup through
  `HolonDescriptor`
- re-centers implementation work on
  `DanceImplementation -[ForDance]-> DanceType`
- re-centers implementation work on one common host runtime surface
- treated old-world/new-world coexistence as parallel buildout and test
  migration, not runtime request translation
- moves asynchronous event architecture out of the active implementation scope

This document translates the revised dance design into a practical,
dependency-aware implementation sequence.

It is intended to:

- sequence the work that follows delivered `PRO1`
- identify the schema and runtime deltas implied by the revised spec
- keep the new-world dance model simple while it is being built out
- avoid reopening `PRO1` or reintroducing design surfaces the revised spec has
  now retired
- provide a basis for issue definition, PR sequencing, and test migration

This plan assumes:

- `docs/core/dances/dances-design-spec.md` is the authoritative design spec
  for the name-addressed Dance model
- Dance `PRO1` is complete and fixed in scope
- the Dance cutover may replace `PRO1`-era assumptions without preserving a
  compatibility bridge
- `HolonDescriptor` is the caller-facing surface for afforded dance discovery
- `HolonReference` is the canonical singular holon handle
- `HolonCollection` is the canonical plural holon-backed carrier
- request and response bodies are ordinary holons reached by reference
- dynamically generated invocation and response holons are always transient
- there is no dance-specific caching layer
- there is no runtime translation requirement from the old-world dance model to
  the new-world dance model
- asynchronous event-handling remains deferred

Related references:

- `docs/core/dances/dances-design-spec.md`
- `docs/core/core-runtime/descriptors/descriptors-design-spec.md`
- `docs/core/commands-and-runtime/commands.md`
- `docs/core/map-queries/navigation-algebra.md`
- `docs/core/map-queries/queries-impl-plan.md`
- `docs/roadmap/desc-driven-impl-plan.md`

---

# 1. Delivered Baseline

Dance `PRO1` is treated as done and delivered.

For this plan, that means:

- the implementation sequence starts after `PRO1`
- `PRO1` is not reopened to absorb later design simplifications
- if the revised design differs from `PRO1` assumptions, subsequent phases
  deliver the replacement or supersession work explicitly

The delivered `PRO1` baseline is still useful because it established early
new-world dance momentum. The remaining work now needs to bring that momentum
into conformance with the revised holonic design.

---

# 2. Delivery Principles

The post-`PRO1` implementation sequence follows these rules:

- descriptors own dance affordance semantics
- callers discover dances through `HolonDescriptor`, not a second global
  registry
- `DanceInvocation` and `DanceResponseType` are transient execution holons
- request and response bodies are referenced holons, not embedded payload DTOs
- `DanceType.RequestType` is the type-level request contract
- `DanceInvocation.Request` is the invocation-level request instance
- `DanceImplementation` binds to `DanceType` through `ForDance` only
- implementation selection is by dance, not by target-type-specific method
  dispatch
- multiple active implementations for one dance must be semantically
  interchangeable under that dance's contract
- query and navigation operations are ordinary dances
- `Projection` and `TransientHolonType` are the projection/result-shape posture
- dance-side validation consumes descriptor-owned value and operator semantics
- one common host runtime surface is used for query/navigation and
  side-effecting dances
- old-world/new-world coexistence is handled by test migration, not by runtime
  translation adapters
- no dance-specific caching layer, no durable invocation/response storage, and
  no event architecture work should be introduced unless the revised spec
  explicitly calls for it

---

# 3. Phase Overview

The recommended post-`PRO1` sequence is:

1. Name-Addressed Schema and Binding Foundation
2. Descriptor-Afforded Dance Discovery Hardening
3. QueryDance Adapter Delivery
4. Dynamic Implementation Activation and Selection

Recommended PR / issue sequence:

1. Dance PR2 — Name-Addressed Schema and Binding Foundation
2. Dance PR3 — Descriptor-Afforded Dance Discovery Hardening
3. Dance PR5 — QueryDance Adapter Delivery
4. Dance PR7 — Dynamic Implementation Activation and Selection

Each phase below defines:

- goal
- major deliverables
- why the phase exists
- dependencies
- exit criteria

---

# 4. Phase 1 — Name-Addressed Schema and Binding Foundation

## Goal

Establish the schema and runtime foundation for name-addressed Dance binding.
This is intentionally smaller than the DAHN → TS SDK → Commands → Dance
vertical slice: it preserves existing client and command flows without making
their full cutover part of Dance PR2. Structural validation remains a separate
shared Validation-track integration.

## Major Deliverables

- Dance PR2 / name-addressed schema and binding foundation
  ([map-holons #652](https://github.com/evomimic/map-holons/issues/652),
  implemented in [PR #654](https://github.com/evomimic/map-holons/pull/654))

- `DanceType.RequestType -> HolonType`
- `DanceInvocation.DanceName` resolving to exactly one Dance through the
  affording holon's effective afforded dances
- `DanceInvocation.Request -> HolonType`
- `DanceResponseType.ResponseBody -> HolonType`
- `Projection.HolonType` as a shell that extends `HolonType`, with concrete
  property-map shapes represented by extensions of `Projection`
- required `DanceInvocation.AffordingHolon`, whose effective descriptor's
  `AffordsDance` relationship defines the unique DanceName resolution scope
- `LoadHolons` and `QueryDance` using an affording `HolonSpace`
- no Dance-local structural validator; shared descriptor-aware validation is a
  follow-up integration once supplied by the Validation track
- removal of `DanceInput`, `InvokesDance`, and superseded response and bridge
  schema/runtime surfaces with their callers and tests
- runtime and wrapper removal of `ResponseStatusCode` as an active response
  concept
- runtime and wrapper removal of `OutcomeOf` as an active response concept
- retirement of any active implementation assumptions that still require
  per-target implementation applicability
- explicit transient lifecycle posture for dynamically generated invocation and
  response holons
- existing client and Command flows remain nominal without a one-off loader
  path; their complete public vertical-slice cutover remains separate work

## Why This Phase Exists

The revised spec changed some of the names and boundaries that the older plan
still assumed. Those changes need to become concrete first, or later dispatch,
validation, and query work will keep building on the wrong contract.

This is also the point where implementation work should stop acting as if:

- dance-level request schema and invocation-level request instance share the
  same relationship name
- response bodies require a special response-body root type
- response status and invocation back-pointers are part of the active response
  model

## Dependencies

- `dances-design-spec.md`
- core schema governance
- delivered `PRO1`

## Exit Criteria

- the active schema and wrappers use `RequestType` for dance-level request
  contract declaration
- invocation identity is required `DanceName`, never a direct Dance descriptor
  reference
- the foundation does not introduce a Dance-local structural validator;
  shared request and response conformance remains deferred to the Validation
  track
- every invocation requires an affording holon and resolves its DanceName through
  that holon's effective afforded dances
- response-body references target ordinary holon types
- `Projection` exists as the base shell for projection/property-map holon types
- response handling no longer depends on `ResponseStatusCode` or `OutcomeOf`
- invocation and response lifecycle is explicitly transient in runtime code and
  tests

---

# 5. Phase 2 — Descriptor-Afforded Dance Discovery

## Goal

Make descriptor-backed dance discovery real through `HolonDescriptor` and
flattened inherited affordance lookup.

## Major Deliverables

- Dance PR3 / descriptor-backed dance discovery

- caller-facing lookup of afforded dances on `HolonDescriptor`
- inherited/flattened effective dance lookup through `Extends`
- runtime access patterns for `DanceType`, `RequestType`, and `Response`
  metadata
- no caller-side affordance reconstruction logic
- no second registry for dance existence

## Why This Phase Exists

The revised design is explicit that descriptors own dance existence and lookup
semantics. Until this phase lands, the new-world dance model still depends on
out-of-band knowledge or ad hoc lookup code.

## Dependencies

- Phase 1 / core schema and contract alignment
- descriptor structural runtime surface

## Exit Criteria

- callers can discover effective afforded dances through `HolonDescriptor`
- inherited affordances are flattened and caller-facing
- dance request/response metadata is discoverable from the dance descriptor
- no new-world caller needs a second dance lookup mechanism

---

# 6. Command and SDK Vertical Slice Remains Separate

## Goal

The original PR4 ingress and SDK work is not part of the narrowed Dance PR2
foundation. It follows the name-addressed affordance and binding substrate while
preserving existing client and Command flows during the transition.

## Major Deliverables

- follow-up vertical slice / `DanceV2` ingress and static execution alignment

- shared canonical `DanceInvocation` builder/factory in the host dance layer
- TS SDK `DanceV2` helper built on top of the shared canonical builder/factory

- command ingress accepts a `HolonReference` to `DanceInvocation`
- ingress stamps `InvocationSource` internally; it is never API input
- dispatch binds a typed `DanceInvocation` wrapper from its reference
- request validation uses the uniquely resolved `DanceType.RequestType`
- request presence/absence rules are enforced structurally
- target affordance validation uses descriptor-backed `AffordsDance`
- implementation resolution uses `ForDance` only
- zero or multiple `ForDance` candidates fail hard
- response handling returns `HolonReference` to a `DanceResponseType`-derived
  response holon
- response validation confirms the returned holon conforms to the invoked
  dance's declared `Response` descriptor
- invocation and response holons remain transient in execution
- one common host runtime surface is used for both query/navigation and
  side-effecting dances
- `DanceRequest` and `DanceResponse` are removed, not retained as
  transitional bridge shapes

## Why This Phase Exists

This is the point where the revised holonic model becomes executable end to
end. It also locks in a simpler execution posture:

- no per-target implementation applicability layer
- no separate read-only ABI tier
- no durable execution-log semantics baked into invocation/response holons
- no Trust Channel adoption work beyond shared-core readiness in this issue

## Dependencies

- Dance PR2 / name-addressed schema and binding foundation
- Phase 2 / descriptor-afforded dance discovery
- command/runtime integration posture

## Exit Criteria

- new-world dance execution is driven by `DanceInvocation`
- request and response conformance integrate the shared validation capability
  when it is delivered
- dispatch uses uniquely resolved DanceName, descriptor-backed affordance
  validation, and `ForDance`
- response bodies are returned by reference, not payload expansion
- runtime code no longer assumes invocation/response persistence
- the shared canonical `DanceInvocation` builder/factory exists in the host
  dance layer and is reusable by Commands and Trust Channels
- the TS SDK exposes a first-class `DanceV2` helper that hides command
  building, invocation construction, and response handling

---

# 7. Phase 4 — Query and Navigation Dance Delivery

## Goal

Implement the Query–Dance adapter over the independently invocable Query
engine and its holonic result posture.

## Major Deliverables

- Dance PR5 / query/navigation dance delivery

- `QueryDance`, `QueryDanceRequest`, and `QueryDanceResponse` in the
  Query–Dance adapter schema
- the `HolonSpace` to `QueryDance` affordance, without a Core-to-Query schema
  dependency
- adapter invocation of the direct Query engine; query expressions remain
  Query-owned rather than Dance-owned
- `HolonCollection` as the plural result carrier
- concrete extensions of `Projection` for core projection/property-map results
- `TransientHolonType` usage for projection shapes defined only at runtime
- no row-shaped query result contracts
- no Query engine dependency on Dance request/response types
- no query-only runtime operand family reintroduced through dance work

## Why This Phase Exists

The revised design keeps Query independently reusable while providing the same
invocation, dispatch, and response-body model as other Dances for Dance ingress.

## Dependencies

- Dance PR2 / name-addressed schema and binding foundation
- QRY0 Query Schema and Query–Dance adapter package load
- direct Query execution seam

## Exit Criteria

- Dance-mediated query flows execute through the adapter and invoke the direct
  Query engine
- plural results use `HolonCollection`
- projected records use holons described by concrete extensions of `Projection`,
  including `TransientHolonType` extensions for dynamic query projections
- no new query envelope or row DTO family appears in the Query engine

---

# 8. Shared Descriptor-Aware Validation Dependency

## Goal

Provide the shared descriptor-aware conformance capability that Dance PR2 calls
at ingress and response egress. Dance does not implement a local validator.

## Major Deliverables

- Validation Capability work / shared descriptor-aware validation

- request value validation via `ValueDescriptor`
- operator support checks via descriptor-backed semantics
- projection/result validation against concrete holon descriptors
- explicit failure on unsupported operators
- no handwritten dance-local predicate semantics where descriptor semantics
  already exist

## Why This Phase Exists

The revised spec keeps value and operator semantics outside the dance layer.
Once query/navigation and other structured dances are executing, this phase
prevents the runtime from drifting into a second, implicit semantic system.

## Dependencies

- Validation implementation plan and descriptor-runtime products
- descriptor value/operator semantics

## Exit Criteria

- dance-side validation uses descriptor-owned semantics
- filter and comparison behavior is descriptor-backed
- projected/result holons are validated against their concrete descriptors
- dance logic no longer duplicates value/operator meaning

---

# 9. Phase 6 — Dynamic Implementation Activation and Selection

## Goal

Add the revised spec's activation-time checks and deterministic implementation
selection on top of the simpler `ForDance` execution model.

## Major Deliverables

- Dance PR7 / dynamic implementation activation and selection

- use of `Engine`, `ModuleRef`, `Entrypoint`, `AbiId`, `Version`, `Compat`, and
  `DanceSummary`
- activation-time validation for:
  - `abi-compat`
  - `module-integrity`
  - `policy-eligibility`
  - `engine-readiness`
  - `shape-conformance`
- deterministic selection across multiple active implementations of the same
  dance
- explicit semantic interchangeability requirement for multiple active
  implementations of one `DanceType`
- no target-type-specific method dispatch layer added back into the model

## Why This Phase Exists

The revised design still allows multiple implementations, but only as
interchangeable executables for the same dance contract. This phase should be
delivered after the simpler static path is stable so the runtime can evolve
without reopening the contract model.

## Dependencies

- Phase 3 / command ingress and static execution alignment
- Phase 5 / descriptor-semantic validation

## Exit Criteria

- activation-time checks are explicit
- implementation selection is deterministic
- multiple active implementations are treated as interchangeable realizations of
  one dance contract
- no per-target implementation applicability layer exists in schema or runtime

---

# 10. Phase 7 — Test Migration and Old-World Drawdown

## Goal

Move behavior coverage from old-world tests to new-world tests when the
new-world model can fully express that behavior.

## Major Deliverables

- Dance PR8 / test migration and old-world drawdown

- mapping of old-world dance tests to new-world equivalents
- migration of tests once the new-world path is feature-complete for the tested
  behavior
- removal of old-world-only assertions from areas already fully covered by the
  new-world model
- explicit non-goal: no runtime adapter layer whose purpose is to translate
  old-world requests into new-world invocation holons

## Why This Phase Exists

The revised spec treats old-world/new-world coexistence as a temporary buildout
posture, not as a backward-compatibility contract. Tests are the right place to
manage that transition.

## Dependencies

- the relevant behavior must already exist in the new-world path
- earlier phases as needed by the specific test area

## Exit Criteria

- new-world tests exist for behavior the revised model can fully express
- old-world tests remain only where the new-world implementation is not yet
  feature-complete
- no runtime translation layer has been introduced just to keep old-world tests
  green

---

# 11. Cross-Phase Dependency Summary

## Critical Path

1. Dance PR2 name-addressed schema and binding foundation
2. Shared descriptor-aware validation and Dance validation integration
3. Descriptor-afforded dance discovery hardening
4. QueryDance adapter delivery
5. Dynamic implementation activation and selection

## Key Dependency Rules

- do not reopen `PRO1`
- do not block Dance PR2's binding foundation on the shared structural validator;
  integrate the validator when the Validation track provides it
- Dance PR2 owns final caller-facing invocation routing; do not retain an
  alternate path for sequencing convenience
- query/navigation work should use the same invocation and response-body model
  as other dances
- validation should consume descriptor semantics rather than precede them
- dynamic implementation selection should be layered on top of stable
  `ForDance` dispatch
- test migration should follow new-world feature completeness, not drive runtime
  adapter work

---

# 12. Parallel Work Guidance

## Safe Earlier Work

- schema delta review against the revised spec
- runtime wrapper design for `DanceInvocation`, `DanceResponse`, and
  `DanceImplementation`
- issue definition for descriptor-backed dance discovery
- command/runtime review for transient invocation/response lifecycle

## Safe Once Phase 1 Is Stable

- descriptor-afforded discovery work
- command ingress refactoring around `RequestType`
- query/navigation dance surface planning

## Safe Once Phase 3 Is Stable

- core query/navigation dance implementation
- descriptor-semantic validation work
- test migration for behaviors already expressible in the new-world path

## Safe Once Phase 5 Is Stable

- dynamic module activation and deterministic implementation selection

---

# 13. Recommended Issue / PR Sequence

1. Dance PR2
   Align schema names and runtime wrappers to the revised contract:
   `RequestType`, direct `ResponseBody -> HolonType`, `Projection`, and removal
   of active `ResponseStatusCode` / `OutcomeOf` assumptions.
2. Dance PR3
   Expose descriptor-backed afforded dance discovery through `HolonDescriptor`
   with inherited/flattened lookup.
3. Dance PR5
   Implement the Query–Dance adapter over the direct Query engine, preserving
   `HolonCollection` responses and the Query/Core dependency boundary.
4. Dance PR7
   Add activation-time validation and deterministic selection across multiple
   interchangeable implementations of the same dance.

---

# 14. Deferred Work

The following areas are intentionally deferred and should not be pulled into
active implementation scope unless the design changes:

- asynchronous event-handling architecture
- `DanceEvent`
- dance-specific caching layers
- durable storage of dynamically generated invocation/response holons
- runtime translation from old-world dance requests to new-world invocation
  holons
- target-type-specific implementation applicability layers
