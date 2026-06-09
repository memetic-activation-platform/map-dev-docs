---
name: Enhancement Proposal
about: Suggest an improvement or new feature for the Memetic Activation Platform
title: "[Enhancement] Dance PR3 Descriptor-Afforded Dance Discovery"
labels: enhancement
assignees: <Your Username>
---

### 1. Summary (Required)

**What is the enhancement?**  
Implement Dance PR3 by exposing descriptor-backed dance discovery through `HolonDescriptor`, including flattened inherited `Affords` lookup through `Extends`, and caller-facing access to each discovered dance's `RequestType` and `Response` metadata without introducing a second dance registry.

---

### 2. Problem Statement (Required)

**Why is this needed?**  
The revised dances design makes `HolonDescriptor` the caller-facing owner of dance discovery semantics. The implementation plan scopes Dance PR3 to "descriptor-backed dance discovery" so callers can discover effective afforded dances, inherited through `Extends`, without reconstructing lineage themselves.

The current `map-holons` codebase already has the schema pieces for this posture and already flattens other affordances, but it does not yet expose the corresponding dance surface:

- The dance schema import file already defines `Affords`, `AffordedBy`, `RequestType`, and `Response`.
- `HolonDescriptor` already flattens inherited `AffordsCommand` via `afforded_commands()` and `get_command_by_name()`.
- Inheritance helpers already provide self-first, duplicate-aware flattening through `walk_extends_chain()` and `flatten_related_members()`.
- The runtime still carries old-world dance envelopes (`DanceRequest`, `DanceResponse`, `ResponseStatusCode`, `ResponseBody`) alongside the newer `contract.rs` posture, which increases the risk that dance discovery will stay ad hoc or drift toward a second lookup mechanism if PR3 is not made explicit.

Without this enhancement, new-world callers still need out-of-band knowledge to determine which dances a holon type affords, and Dance PR4 validation and ingress work cannot cleanly rely on a canonical descriptor-owned lookup surface.

---

### 3. Dependencies (Required)

**Does this depend on other issues or features?**  
Yes.

- Dance PR2 / Core Schema and Contract Alignment must already be in place sufficiently for `DanceType`, `RequestType`, `Response`, and revised dance schema imports to be the active target posture.
- Descriptor Phase 2 / descriptor structural runtime surface is a prerequisite because Dance PR3 depends on `HolonDescriptor` being the public affordance surface.
- Dance PR4 depends on this issue because command ingress and target affordance validation are supposed to resolve dances from descriptors rather than from a separate registry or caller-side lineage walk.

This issue should stay bounded to discovery and metadata lookup. It should not absorb Dance PR4 ingress work, Dance PR6 semantic validation, or Dance PR7 implementation activation/selection.

---

### 4. Proposed Solution (Required)

**How would you solve it?**  
Extend the descriptor runtime so dance affordances are exposed with the same inheritance and duplicate-detection posture already used for commands and operators.

Proposed changes:

- Add a caller-facing dance discovery API on `HolonDescriptor`, analogous to `afforded_commands()`, that flattens effective `Affords` relationships through `Extends`.
- Add a lookup helper analogous to `get_command_by_name()` so callers can resolve one effective dance by canonical dance name and receive duplicate inherited declaration errors when appropriate.
- Introduce the minimum wrapper/accessor surface needed to read dance contract metadata from discovered dances:
  - `DanceType`
  - `RequestType`
  - `Response`
- Reuse existing inheritance helpers such as `flatten_related_members()` rather than inventing dance-specific traversal logic.
- Add schema contract tests and sweetests that prove:
  - `Affords` and `AffordedBy` are wired as descriptor relationships
  - effective dance lookup is flattened through multi-step `Extends`
  - duplicates and malformed inheritance produce the expected descriptor errors
  - callers do not need a second dance lookup mechanism
- Keep old-world dance request/response compatibility surfaces in place only as temporary coexistence artifacts; this issue should not expand their role in discovery.

Recommended implementation shape:

- Follow the existing `HolonDescriptor::afforded_commands()` pattern in `shared_crates/holons_core/src/descriptors/holon_descriptor.rs`.
- Reuse the same self-first inheritance semantics already implemented in `shared_crates/holons_core/src/descriptors/inheritance.rs`.
- Add a dance-specific verification test analogous in spirit to `tests/sweetests/tests/execution_steps/command_affordance_verification_executor.rs`, but focused on `Affords`, `AffordedBy`, and flattened dance lookup.

---

### 5. Scope and Impact (Required)

**What does this impact?**  
This enhancement impacts:

- Descriptor runtime APIs in `shared_crates/holons_core/src/descriptors/`
- Core schema-backed dance descriptor imports in `host/import_files/map-schema/core-schema/`
- Dance contract lookup used by later ingress, validation, and dispatch work
- Test coverage for descriptor affordances and inheritance behavior

It should improve:

- Caller ergonomics for dance discovery through `ReadableHolon::holon_descriptor()`
- Conformance with the dances design spec's descriptor-owned affordance model
- Readiness for Dance PR4 target affordance validation and request/response metadata lookup

It should not in this issue:

- implement `DanceV2` ingress routing
- select implementations via `ForDance`
- remove all old-world dance envelopes
- introduce query/navigation dance behavior
- add a second registry, cache, or dance-specific lookup service

---

### 6. Testing Considerations (Required)

**How will this enhancement be tested?**

- Can it be validated with existing test cases?
  - Existing descriptor tests for inherited affordances provide the pattern but not the dance coverage. In particular, command affordance flattening tests in `shared_crates/holons_core/src/descriptors/holon_descriptor.rs` and `shared_crates/holons_core/src/descriptors/schema_contract_tests.rs` can be mirrored for dances.
- Do new test cases need to be created?
  - Yes.
  - Add unit tests for `HolonDescriptor` dance discovery and single-dance lookup.
  - Add inheritance tests covering self-first ordering, multi-step `Extends`, duplicate effective declarations, cyclic `Extends`, and multiple-parent errors.
  - Add schema verification tests proving the imported `Affords`, `AffordedBy`, `RequestType`, and `Response` descriptors have the expected source/target types and inverse relationships.
  - Add a sweetest or equivalent integration-level check that a caller can discover effective afforded dances through `HolonDescriptor` without manual `Extends` traversal.
- Are there specific areas in the test ecosystem impacted by this enhancement?
  - Yes.
  - Descriptor unit tests in `shared_crates/holons_core/src/descriptors/`
  - Schema contract tests
  - Sweetests covering runtime-visible descriptor affordance behavior

---

### 7. Definition of Done (Required)

**When is this enhancement complete?**  
This enhancement is complete when all of the following are true:

- `HolonDescriptor` exposes effective dance discovery through flattened inherited `Affords`.
- Callers can resolve one effective dance by name without walking `Extends` themselves.
- The discovered dance surface exposes runtime access to `DanceType`, `RequestType`, and `Response` metadata needed by downstream dance ingress and validation work.
- Effective dance lookup follows the same self-first inheritance, duplicate detection, cyclic `Extends`, and multiple-parent error semantics already used by other descriptor affordances.
- Tests cover positive lookup, multi-step inheritance, duplicate declarations, malformed inheritance, and schema descriptor correctness for `Affords` and related dance metadata relationships.
- No new-world caller-facing path added in this issue depends on a second dance registry or ad hoc lineage reconstruction logic.

---

<details>
<summary>Optional Details (Expand if needed)</summary>

### 8. Alternatives Considered

**What other solutions did you think about?**  

- Continue using ad hoc runtime lookup or a dedicated dance registry.
  - Rejected because the design spec explicitly says callers ask `HolonDescriptor` for effective afforded dances and must not rely on a second global registry.
- Defer dance metadata lookup until Dance PR4.
  - Rejected because PR4 depends on descriptor-owned target affordance validation and should build on an existing discovery surface rather than define one implicitly.
- Expose only raw relationship traversal and leave flattening to callers.
  - Rejected because the design spec requires inherited affordances to be flattened and caller-facing.

---

### 9. Risks or Concerns

**What could go wrong?**  

- Terminology drift between old-world runtime types (`DanceType` enum in `dance_request.rs`) and new-world `DanceType` descriptor semantics may confuse implementation unless wrapper and accessor naming is explicit.
- The codebase already retains old-world response surfaces (`DanceResponse`, `ResponseStatusCode`, `ResponseBody`), so discovery work must not accidentally reinforce deprecated execution assumptions.
- If dance metadata lookup is implemented as generic relationship scraping without a stable wrapper surface, PR4 may duplicate logic or reintroduce non-canonical dance semantics.
- Duplicate effective dance declarations across inheritance could remain silent unless the same duplicate-detection posture used for commands is applied here.

---

### 10. Additional Context

**Any supporting material?**  

Authoritative DevDocs sources inspected:

- `docs/core/dances/dances-design-spec.md`
- `docs/core/dances/dances-impl-plan.md`
- `docs/roadmap/desc-driven-impl-plan.md`

`map-holons` template and code grounding used:

- `.github/ISSUE_TEMPLATE/enhancement.md`
- `shared_crates/holons_core/src/descriptors/holon_descriptor.rs`
- `shared_crates/holons_core/src/descriptors/inheritance.rs`
- `shared_crates/holons_core/src/descriptors/schema_contract_tests.rs`
- `shared_crates/type_system/type_names/src/relationship_names.rs`
- `host/import_files/map-schema/core-schema/MAP Schema Types-map-core-schema-dance-schema.json`
- `shared_crates/holons_core/src/dances/contract.rs`
- `shared_crates/holons_core/src/dances/dance_request.rs`
- `shared_crates/holons_core/src/dances/dance_response.rs`
- `tests/sweetests/tests/execution_steps/command_affordance_verification_executor.rs`

Reconciliation notes:

- The imported dance schema already declares the revised descriptor relationships needed by PR3, so the main implementation gap is descriptor runtime exposure rather than schema invention.
- `HolonDescriptor` already exposes flattened command affordances but not dance affordances, which is strong evidence that PR3 should extend an existing pattern rather than introduce a new abstraction family.
- The coexistence of new-world contract types in `contract.rs` with old-world `dance_request.rs` and `dance_response.rs` is expected for parallel buildout, but it increases the importance of keeping discovery anchored to descriptors rather than envelope-era runtime types.

Questions:

- Non-blocking: should this issue introduce a dedicated dance descriptor wrapper now, or keep the initial surface minimal by extending `HolonDescriptor` plus adding only the narrow wrapper/accessor types required for `RequestType` and `Response`?
- Non-blocking: should dance lookup use the dance descriptor `type_name`, `DanceName`, or both for caller resolution? The design leans on stable dance names, so the issue implementation should make the chosen lookup identity explicit and test it.

Recommended sequencing:

- Land this before Dance PR4 and use it as the sole caller-facing discovery dependency for target affordance validation and dance metadata inspection.

---

</details>
