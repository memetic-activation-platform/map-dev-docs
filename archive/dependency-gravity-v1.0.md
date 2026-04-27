# Problem Description

### 🧩 Initial Problem Statement:

In the MAP architecture, validation occurs inside the **integrity zome**, which is compiled to WASM and recorded immutably in the genesis record of each MAP DHT. This enforces a critical design constraint: **any change to the integrity zome requires spinning up a new DHT**. To avoid unnecessary DHT churn, we aim to keep the integrity zome as **stable, minimal, and tightly scoped** as possible.

The MAP defines exactly one `EntryType` (`HolonNode`) and one `LinkType` (`SmartLink`). When the Holochain Conductor triggers validation for operations on these types, the validation logic must ensure that a `HolonNode` is well-formed and valid. At first glance, this appears to be a localized, self-contained operation.

However, the MAP is built on a self-describing schema model. Each `HolonNode` is a `Holon`, and each `Holon` is expected to have a `DESCRIBED_BY` relationship to a `HolonDescriptor`. The `HolonDescriptor` defines the required properties and value types of the holon through additional nested relationships (`INSTANCE_PROPERTIES`, `VALUE_TYPE`, etc.). Validation logic must **resolve and traverse this descriptor graph** in order to enforce schema-derived rules (e.g., required properties, min/max values, string length constraints).

Although the holon being validated is self-contained, its validation depends on descriptor data that must be **fetched and interpreted** — and this is where the problem arises.

In the current MAP architecture:
- The **shared_objects_layer** defines the `Holon` type.
- The **reference_layer** provides typed access to holons through traits like `ReadableHolon`, and manager components like `HolonsCacheManager`, `TransientHolonManager`, and `Nursery`.
- The **core layer** orchestrates operations over these layers, reusing the reference API.

Validation code in the integrity zome needs to resolve descriptors — which pulls in code from the reference layer. But the reference layer is deeply tied to the coordinator-side runtime and caching infrastructure, and thus **cannot safely be imported into the integrity zome**. Attempting to do so introduces a *"gravitational pull"* that threatens the architectural separation between coordinator logic (`holons_core`) and the integrity zome (`holons_guest_integrity`).

---

### ⚠️ Complication: Extensibility and Runtime Validation

Beyond static validation logic, the MAP is designed to support **runtime-dispatched validation rules**, defined and extended by application developers (mapp authors).  These rules are modeled as holons (`ValidationRule`, `ValidationRuleSet`) and executed via a standardized `Dance` protocol. Each rule expresses a Promise to perform validation for specific types or schemas. (See Discussion #284 for details on this proposed design).

This means:

- Validation behavior is **not fully hardcoded** in the integrity zome.
- Rules are **holons themselves**, discoverable at runtime and evaluated through the **Dance Dispatch Engine**.
- Rules may be implemented in **WASM**, **Rust**, **JSONLogic**, or other engines, and selected dynamically based on metadata.

This architecture introduces **a second axis of gravity**:

> Not only does the core validation logic want to pull in the reference layer — the **extensibility model** demands that we allow **declarative and dynamic rule dispatch** at runtime.

This presents multiple challenges:
- Holons submitted by external developers may use **custom rule sets**.
- These rules may refer to holons (e.g., scripts or configs) that must be resolved in validation context.
- **Validation cannot be fully hardwired** into static WASM code without violating extensibility goals.
- Rules must be **discoverable, executable, and introspectable** from within the validation runtime.

As a result, even if we resolve static validation through descriptor resolution, we still face the need to:

- Dynamically collect and execute applicable validation rules.
- Safely run those rules inside a **sandboxed, integrity-compatible engine**.
- Avoid baking the full validation surface into the integrity zome's immutable WASM.

This reinforces the need for an **intentional validation dispatch layer** — one that separates:

1. **Static validation rules** (e.g., required properties) resolved through descriptors.
2. **Dynamic validation rules** (e.g., "valid according to an externally published dance") evaluated through rule-based dispatch.

Any architectural solution must support both, without violating the integrity zone's immutability or introducing unsound dependencies.

### ⚠️ Complication: Validation Scope Extends Beyond Single HolonNode or SmartLink

In the initial MAP validation architecture, the integrity zome was responsible for validating operations on two types:

- `HolonNode` (for holons)
- `SmartLink` (for relationships between holons)

Each operation was validated **in isolation**, according to its local structure and schema conformance. This matched Holochain’s native per-entry validation model: each DHT operation is subject to validation before being accepted into the shared ledger.

At that stage, the scope of validation appeared manageable:
- Each `HolonNode` could be checked against its `DESCRIBED_BY` schema descriptor.
- Each `SmartLink` could be checked for consistency with its `RELATIONSHIP_TYPE` descriptor.

But as the MAP validation model matured, it became clear that:

> **Validation often requires awareness of multiple holons, links, and their interdependencies.**

Some examples:
- A `Book` holon may reference an `Organization` as its publisher — we must confirm that the target is valid, present, and of the correct type.
- A `Dance` request may require confirming that the requesting agent holds a role defined in a separate `Agreement`, linked via a `HAS_ROLE` SmartLink.
- A `SmartLink` may express a relationship whose **validity depends on the types of both source and target holons** — which themselves must be resolved.

These cases break the assumption that validation can be performed independently on a single operation.

In short:

> The unit of validation is no longer a single entry — it's a **subgraph of related holons and links**.

This realization drove the need for a broader validation layer — one that can resolve and reason over this connected structure **before** any entries are committed to the DHT.

### ⚠️ Complication: Coordinator-Level Pre-Commit Validation

To address these graph-shaped validations, MAP introduces a **coordinator-level validation stage** that runs **before** committing a `HolonNode`.

This stage can:
- Resolve the full **Descriptor graph** for the holon.
- Collect applicable **static and dynamic validation rules**.
- Evaluate rules using **declarative engines** or **compiled logic**.
- Detect **multi-holon inconsistencies**, **sequencing violations**, or **invalid SmartLinks**.
- **Abort the commit** before reaching the DHT if the object is invalid.

Crucially, coordinator-level validation provides access to the full **reference layer**, **caches**, and **networking stack** — capabilities **not available** in the integrity zome.

However, this raises a question:

> If the coordinator already performs validation, what role is left for the integrity zome?

### ⚠️ Complication: Integrity Zome Validation Still Has a Critical Role

Despite the need for powerful pre-commit validation in the coordinator layer, we cannot eliminate validation in the integrity zome.

Why?

Because Holochain provides **shared validation guarantees** through integrity zome logic:
- Every peer independently validates every operation before accepting it.
- Invalid operations are rejected network-wide.
- These rules are part of the compiled WASM, verifiably enforced by all nodes.

If we **moved all validation out** of the integrity zome:
- Malicious agents could bypass validation by modifying their coordinator code.
- Peers would have no way to detect invalid holons being published to the DHT.
- Shared consistency would break down, and any application logic relying on trusted state would become unsafe.

So we must strike a careful balance:

> Offload **complex, dynamic, and extensible** validation logic to the coordinator level — but enforce **minimal, structural, and cryptographically checkable** rules in the integrity zome.

This has direct design implications:
- The integrity zome must validate *only what it can do safely* — no descriptor graph traversal, no network calls, no dynamic dispatch.
- Yet it must still verify:
    - That entries are properly formed.
    - That key relationships (like `DESCRIBED_BY`) are declared and syntactically valid.
    - That declared validation results (e.g., "pre-validated by Rule X") match cryptographic inputs.

This reinforces the idea of a **proof-carrying validation model**: the coordinator performs deep validation, and **records a signed digest of that validation** within the `HolonNode` — which the integrity zome can verify **without repeating the entire computation**.

This is the foundation for the updated design approach.


# 🧪 Design Options Considered

### ✅ Option 1: Perform Full Validation Inside Integrity Zome

This approach keeps validation logic entirely inside the integrity zome, enforcing schema rules (via Descriptors) and dynamic validation rules directly during DHT commit.

**Benefits:**
- Strong guarantees: everything validated immutably at commit time.
- Simpler trust model — if it's in the DHT, it’s valid.

**Problems:**
- Requires importing complex reference-layer logic into the integrity zome.
- Cannot resolve external descriptors (cross-DHT lookups).
- Cannot support runtime-dispatched validation rules.
- Violates the architectural boundary between core runtime and integrity logic.

**Conclusion:** ❌ Rejected. Impractical and incompatible with MAP’s extensibility model.

---

### ✅ Option 2: Only Validate Minimal Form in Integrity Zome

Instead of enforcing full schema and rule validation, the integrity zome performs **minimal structural validation**:

- Ensures `HolonNode` is well-formed.
- Validates that the committing agent signed the data.
- Optionally validates hash consistency and inclusion of a `descriptor_id`.

**Benefits:**
- Keeps integrity logic extremely stable.
- No dependency on reference-layer or external lookups.
- Allows coordinated pre-commit validation to handle everything else.

**Problems:**
- Integrity zome no longer validates that a `HolonNode` conforms to its Descriptor.
- Shifts trust boundary to coordinator-level validation.
- Requires a mechanism to **record validation results** immutably.

**Conclusion:** ✅ Accepted as a baseline, provided validation results are cryptographically attested.

---

### ✅ Option 3: Record Validation Result as Signed Input Digest

In this model, coordinator-level validation produces a `ValidationInput` that includes:
- A digest of the `HolonNode` contents,
- The `descriptor_id`,
- The validator's version or code hash,
- A digital signature from the validating agent.

This digest is stored as a field on the `HolonNode`.

**Integrity zome then validates:**
- That the signature matches the author.
- That the digest matches the committed data.

**Benefits:**
- Prevents tampering with validation results.
- Enables validator diversity and version tracking.
- Requires no descriptor resolution in the integrity zome.

**Problems:**
- Adds cryptographic complexity.
- Requires including the `descriptor_id` in the `HolonNode` (a departure from current model).

**Conclusion:** ✅ Emerging Preferred Approach.

---

### ✅ Option 4: Store DESCRIBED_BY Inline in HolonNode

A variation of Option 3, this model explicitly stores the `descriptor_id` inside the `HolonNode`, rather than relying on a `SmartLink` to capture the `DESCRIBED_BY` relationship.

**Benefits:**
- Allows the integrity zome to verify that validation occurred against the correct descriptor without needing to resolve the SmartLink.
- Makes validation inputs fully self-contained.

**Problems:**
- Introduces special-case treatment of one relationship (`DESCRIBED_BY`).
- Slightly muddies the model where relationships are stored separately.

**Conclusion:** ✅ Worth adopting as part of Option 3 to keep integrity zome validation local and self-contained.

# 📌 Proposal: Decouple Validation from Integrity Zome Logic

We propose a layered validation architecture that **removes all descriptor-based validation from the integrity zome** and shifts schema-aware and dynamic rule validation into a **coordinator-level pre-commit stage**.

### ✅ Minimal Validation in Integrity Zome
- Validate only basic structure (e.g., JSON well-formedness).
- Optionally check for presence of `descriptor_id` and `validation_result` fields.
- If provided, verify that:
    - The `validation_result` is signed by the author.
    - The input digest matches the HolonNode content.
    - The descriptor ID matches the validated schema.

This allows the integrity zome to remain **small, stable, and free from heavy dependencies** — fulfilling our design goal of reducing DHT churn.

### ✅ Full Validation in Coordinator
- Resolve Descriptor and collect schema-derived rules.
- Load dynamic `ValidationRuleSet` holons.
- Execute rule logic using runtime dispatch or compiled engines.
- Serialize the validation result (descriptor ID, input digest, validator ID).
- Sign the result and include it in the HolonNode before commit.

### 🧲 Resolving the “Dependency Gravity” Problem

This proposal **fully resolves the core problem raised in the Initial Problem Statement**:

> The integrity zome no longer bears responsibility for descriptor resolution or validation.

As a result:
- We no longer need to import the reference layer or shared caches into the integrity zome.
- Validation logic remains DRY — no duplicated logic split between coordinator and integrity.
- We avoid entangling the evolving validation system with the immutable integrity zome WASM.
- Runtime-extensible validation is now first-class and compatible with holonic rules.

By removing the **gravitational attractors** (descriptor resolution and rule dispatch), we preserve the clean separation of roles between the core runtime and the integrity boundary — and create space for a flexible, evolvable validation system that aligns with MAP’s self-describing architecture.

## ✅ Proposal: Coordinator-Validated, Descriptor-Decoupled Architecture

We propose a layered validation architecture that **removes all descriptor-based validation from the integrity zome** and shifts schema-aware and dynamic rule validation into a **coordinator-level pre-commit stage**.

### ✅ Minimal Validation in Integrity Zome
- Validate only basic structure (e.g., JSON well-formedness).
- Optionally check for presence of `descriptor_id` and `validation_result` fields.
- If provided, verify that:
    - The `validation_result` is signed by the author.
    - The input digest matches the HolonNode content.
    - The descriptor ID matches the validated schema.

This allows the integrity zome to remain **small, stable, and free from heavy dependencies** — fulfilling our design goal of reducing DHT churn.

### ✅ Full Validation in Coordinator
- Resolve Descriptor and collect schema-derived rules.
- Load dynamic `ValidationRuleSet` holons.
- Execute rule logic using runtime dispatch or compiled engines.
- Serialize the validation result (descriptor ID, input digest, validator ID).
- Sign the result and include it in the HolonNode before commit.


### 🔓 Key Idea

By moving all complex validation logic — especially anything involving cross-space descriptor resolution or rule execution — into the coordinator layer, we:

- Prevent the integrity zome from needing access to shared type definitions.
- Avoid duplicating rule logic across runtime layers.
- Maintain Holochain's guarantee of self-validating DHT entries.
- Enable evolvable, pluggable validation mechanisms at runtime.

---

### 🧩 Problem Checklist

| ❓ **Validation Challenge**                                      | ✅ **Resolution**                                                                 |
|------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| Integrity zome needs access to Descriptors to validate Holons    | Descriptor resolution happens **in coordinator**, not in the integrity zome       |
| Descriptors may live in other HolonSpaces                        | Cross-space lookups are **only performed by coordinator**, never in validation ops |
| Integrity zome cannot execute dynamic or extensible rules        | All such rules are executed in **coordinator pre-commit validation**              |
| HolonNode has no access to its Descriptor directly               | `descriptor_id` is stored **within HolonNode**, no SmartLink resolution required  |
| Integrity zome cannot resolve complex SmartLinks or dependencies | Validation only checks **internal fields + signature**, no relationship chasing   |
| Risk of faking validation results                                | `ValidationResult` is **signed digest** over HolonNode + descriptor + validator   |
| Coordinator validates — but integrity zome can’t confirm         | Integrity zome checks **digest match + agent signature** to verify results        |
| Need to avoid core logic duplication                             | **Zero descriptor logic** exists in integrity zome — no MAP core coupling         |

---

This proposal preserves the Holochain architecture’s layered validation guarantees while enabling MAP’s graph-shaped and evolving validation logic. It solves the original "dependency gravity" problem by **removing the gravitational pull** — i.e., there is **no longer any reason** for the integrity zome to depend on core schema.

## 🛠️ Implementation Plan

To realize the proposed architecture, we will implement the following phases:

### Phase 1: Integrity Zome Simplification
- [ ] Remove all descriptor resolution and schema-derived validation from `holons_guest_integrity`.
- [ ] Define a minimal `validate_holon_node(op: Op)` implementation:
    - Parse and check HolonNode format.
    - Verify optional `validation_result` signature and descriptor match.
- [ ] Establish test coverage to confirm stability and minimal coupling.

### Phase 2: Coordinator-Level Validation Engine
- [ ] Introduce `HolonValidationEngine` in `holons_core`.
- [ ] For each `HolonNode` commit:
    - Resolve full descriptor graph.
    - Collect applicable static and dynamic rules.
    - Execute rule logic (via Rust or pluggable engines).
    - Generate and sign a `ValidationResult` holon.
    - Attach result to `HolonNode` before commit.

### Phase 3: Rule Infrastructure
- [ ] Finalize and publish `ValidationRule`, `ValidationRuleSet`, and `ValidationResult` schema.
- [ ] Implement runtime rule dispatch infrastructure (initially Rust-only).
- [ ] Support configuration of default validation sets for core types.
- [ ] Ensure Dance-based validation invocation is supported in later phases.

### Phase 4: Holon Import / JSON Validation Flow
- [ ] Integrate coordinator validation into the JSON import pipeline.
- [ ] Return structured `ValidationResult` feedback for each imported holon.
- [ ] Abort invalid commits preemptively at the coordinator level.

### Phase 5: Runtime Extensibility
- [ ] Extend rule engine to support JSONLogic or WASM-based validators.
- [ ] Support `ValidationRule.engine` selection and dispatch.
- [ ] Allow third-party authors to publish and register rules.

---

## ❓ Open Questions

Several design choices remain open for refinement:

### 1. **Validation Result Format**
- Should `ValidationResult` be its own holon?
- Should it be embedded or linked from `HolonNode`?
- What is the minimal information it must include (e.g., digest, descriptor, validator ID, timestamp, result summary)?

### 2. **Signature Model**
- Who signs a `ValidationResult`?
    - Coordinator? Agent? ValidationService?
- Is signature required for all results, or only for those committed with the HolonNode?

### 3. **Pre-commit Hooks**
- Should the validation engine be a hardcoded pre-commit hook?
- Or should it be optional/configurable per space or agent?

### 4. **Trust Model**
- How do other agents validate that a `ValidationResult` was trustworthy?
- Should we add provenance metadata or verifiable credentials?

### 5. **Batch Validation & Graph Cycles**
- Can we validate graphs of holons in batch during import?
- How do we handle validation dependencies and cycles (e.g., circular SmartLinks)?

---

These questions will shape how we finalize the architecture for maximum flexibility, verifiability, and evolvability — without compromising the MAP’s membrane guarantees or self-describing model.