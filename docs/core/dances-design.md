# MAP Design Spec: Dance Types, Implementation & Dispatch

**Status:** Draft  
**Author:** MAP Core / Steve Melville  
**Intent:** Specify how types declare dances, how implementations are bound, and how the host dispatches calls safely and dynamically.    
**Scope:** Type system extensions, import format, governance/validation, runtime dispatch, security, caching, and compatibility with existing MAP/Holochain patterns.  

---

## 0) Foundations & Assumptions

1. **Self‑describing types**
    - All MAP types are holons described by **TypeDescriptor** holons.
    - `InstanceProperties` and `InstanceRelationships` declare expectations for instances.
    - The metaschema already supports declaring new PropertyTypes and RelationshipTypes.

2. **Holon identity & immutability**
    - Instances are immutable; newer versions create new holons.
    - References are stable and do not “go stale”; caches can safely retain instances until memory pressure requires eviction.

3. **Import format conventions**
    - Holon JSON import files use the unified `holons` array, with relationships and properties defined on each holon.
    - `$ref` resolution is strict within the provided file set (no implicit global context).
    - `key` MUST appear before `type` in each holon definition.
    - `type` is shorthand for a `DescribedBy` relationship and should not be duplicated unless rules require exact match.

4. **Key rules**
    - Some holons are keyed, some are keyless, per existing KeyRuleType semantics.
    - Enum Variant holons are keyed and top-level (not embedded).

5. **Governance membranes**
    - Spaces (I‑Spaces / We‑Spaces) enforce admission, attestation, and activation policies for new descriptors and modules.
    - Provenance and attestations are recorded as holons and/or signatures on content hashes.

6. **Runtime execution**
    - Host supports **WASM/WASI** execution and may optionally support:
        - **Process** (spawned executable with stream protocol),
        - **Rust dylib** (FFI with stable ABI),
        - **Builtin** (host-registered functions).
    - Single-threaded isolation for WASM execution is assumed.
    - Modules are addressed by **content hash** and may be fetched via membrane-authorized channels.

---

## 1) Conceptual Model

At its heart, the MAP type system implements a **dynamic dispatch model** in which **every type** — not just `HolonType` — can advertise the behaviors it supports via **fine-grained dispatch tables**. These tables are essentially the per-type registries of “what this type can do,” expressed as relationships from the type descriptor to a set of **DanceTypes**.

In our new terminology, we’re formalizing this as:

```
<TypeDescriptor> —AFFORDS→ <DanceType>
```

### Dynamic Dispatch Tables
- **One per type**:  
  Every `TypeDescriptor` can have its own dispatch table — a set of `Affords` relationships that point to the `DanceType`s it supports. This allows dispatch to be as fine-grained as needed: even closely related types can differ in the set of dances they afford.

- **Any type can afford dances**:  
  We don’t limit affordances to `HolonType`s. `ValueType`s, `RelationshipType`s, even `DanceType`s themselves can have `Affords` links to other dances, enabling compositional and meta-level behaviors.

- **Behavior resolution**:  
  When the system receives a `DanceRequest` for a specific target, the dispatch mechanism:
    1. Identifies the type of the target holon.
    2. Looks up that type’s `Affords` relationships.
    3. Matches the requested dance against the list.
    4. Routes execution to the handler bound to that dance for this type.

### Affordances as First-Class Relationships
- `Affords` is itself a **RelationshipType** holon (like all type descriptors in MAP).
- Concrete instances of `Affords` are **smartlinks** between a type and a dance type.
- Because `Affords` is part of the schema, it can carry **metadata** — version constraints, capability conditions, or even parameter hints — making affordances declarative, inspectable, and extensible.

### Why This Matters
- **Granularity**: Instead of large, monolithic capability declarations, we get fine-grained, composable affordances that can evolve per type.
- **Flexibility**: Adding a new dance is a matter of creating a `DanceType` and linking it via `Affords`; no core code needs changing for schema-driven dispatch.
- **Uniformity**: All affordances are modeled the same way, whether they’re about creating a holon, validating a property, or triggering a real-world workflow.
- **Extensibility**: The dispatch model is naturally open to extension in downstream schemas or spaces without schema rewrites — just add new `Affords` links.

---

## 2) New/Updated Descriptors & Relationships

### 2.1 Descriptors

- **DanceType** *(HolonType, abstract)*  
  The DanceType defines the interface for a single dance. This includes the dance name (by convention, this should be a verb) (e.g., `Render`, `Validate`, `SyncOut`).
    - Properties (examples): `display_name`, `description`, `abi_id` (optional if polymorphic).
    - Relationships:
      - `Request` -- to a HolonType that bundles the input parameters to the DanceRequest. 

- **DanceImplementation** *(Holon)*  
  A concrete binding of a `DanceType` for a specific `TypeDescriptor`.
    - Properties (required unless noted):
        - `Engine` *(Enum)*: `WasmWasi` | `Process` | `RustDylib` | `Builtin`
        - `ModuleRef` *(String)*: content address (e.g., `b3:…` multihash, URL with hash, capability address)
        - `Entrypoint` *(String)*: export/function name (WASM symbol, FFI symbol, command name)
        - `ABI` *(String)*: *stable ABI signature id* the host supports (e.g., `map.dance.v1`)
        - `Version` *(String)*: semver or content-hash pin
        - `CompatRange` *(String, optional)*: semver range allowed
        - `ActivationStatus` *(Enum)*: `proposed` | `active` | `disabled`
        - `Scope` *(Enum)*: `Builtin` | `SchemaDefault` | `SpaceOverride`
        - `ModuleHash` *(String)*: cryptographic hash of the content (if not implicit in ModuleRef)
    - Relationships:
      - `DanceType`->DanceType -- The Dance being implemented.
      - `AffordingType`-> TypeDescriptor (?) the type on whose behalf this dance is being implemented

- **(optional) DanceParameterSchema** *(Holon)*  
  Describes structured inputs/outputs for ABI validation.

### 2.2 Relationships

- **Affords** *(DeclaredRelationshipType)*  
  `(TypeDescriptor) -[Affords]-> (DanceType)`  
  Declares that instances of the type afford/expose the dance.

- **ImplementsDance** *(DeclaredRelationshipType)*  
  `(TypeDescriptor) -[ImplementsDance]-> (DanceImplementation)`  
  Binds concrete implementations available to the dispatcher.

- **ForDance** *(DeclaredRelationshipType)*  
  `(DanceImplementation) -[ForDance]-> (DanceType)`  
  The interface this implementation satisfies.

- **(optional) ParametersSchema** *(DeclaredRelationshipType)*  
  `(DanceType) -[ParametersSchema]-> (DanceParameterSchema)`

> All descriptors follow the foundational rule: `type: "#TypeDescriptor"` with `Extends` pointing at the appropriate meta-type, and they adopt MAP import conventions (key before type, unified relationships block, etc.).

---

## 3) Import File Additions & Examples (Illustrative)

**Note:** Examples are schematic and omit boilerplate. Use your established keys/type shorthands and naming patterns. (No code fences here; the following is raw markdown text with indentation.)

Example A: Declaring a DanceType and parameter schema
- key: `Render.DanceType`
- type: `#DanceType`
- properties: `display_name="Render"`, `description="Produce a representation"`
- relationships: `ParametersSchema -> #Render.Params.Schema` (optional)

Example B: A TypeDescriptor that supports and implements a dance
- key: `BookType.TypeDescriptor`
- type: `#TypeDescriptor`
- relationships:
    - `Affords -> #Render.DanceType`
    - `ImplementsDance -> #BookType.Render.WasmImpl` (below)

Example C: A DanceImplementation bound to `BookType` for `Render`
- key: `BookType.Render.WasmImpl`
- type: `#DanceImplementation`
- properties:
    - `Engine="WasmWasi"`
    - `ModuleRef="b3hash:Qm..."`
    - `Entrypoint="render_book"`
    - `ABI="map.dance.v1"`
    - `Version="1.2.0"`
    - `CompatRange="^1.0.0"`
    - `ActivationStatus="active"`
    - `Scope="SchemaDefault"`
    - `ModuleHash="sha256:abcd..."`
- relationships:
    - `ForDance -> #Render.DanceType`

**Space-scoped override**  
A We‑Space can introduce a second implementation with `Scope="SpaceOverride"` and `ActivationStatus="active"`. Resolution rules (Section 5) ensure overrides take precedence without mutating the schema default.

---

## 4) ABI (Application Binary Interface)

### 4.1 Goals
- Stable contract between host and implementation irrespective of engine.
- Enable content-addressed modules to be swapped/upgraded safely.
- Keep functions **stateless and deterministic** (inputs → outputs), with side effects routed through explicit host calls (capability-gated).

### 4.2 Core shape (`map.dance.v1`)
- **Inputs**
    - `dance_type_id` (ref)
    - `type_descriptor_id` (ref)
    - `instance_refs` (list of holon ids or $ref proxies)
    - `parameters` (bytes or canonical JSON/CBOR)
    - `context` (agent id, space id, capability token, call chain, clock)
- **Outputs**
    - `status` (OK | Error(code))
    - `result` (bytes or canonical JSON/CBOR)
    - `emitted_events` (optional; for telemetry)
- **Host imports**
    - `holon_fetch(id)` → bytes
    - `relationship_query(query)` → ids
    - `attest(proof)` → receipt
    - `emit(event)` → ack
    - (All host functions are capability-gated and audited.)

### 4.3 Serialization & determinism
- Canonical encoding (CBOR or JSON Canonical Form).
- No host clock access except via provided `context`.
- No ambient I/O except via host-imported capabilities.

---

## 5) Dispatch Algorithm (Host)

Given a request `(T, D, ctx)`:

1. **Affordance check**: Ensure `T Affords D`; otherwise fail with `NotSupported(T,D)`.
2. **Collect candidates**: `C = { impl | T ImplementsDance impl ∧ impl ForDance = D ∧ impl ActivationStatus=active }`.
3. **Select binding** (deterministic precedence):
    - Prefer `Scope="SpaceOverride"` in `ctx.space` > `SchemaDefault` > `Builtin`.
    - Prefer exact `Version` pin > satisfied `CompatRange` > latest compatible by semver.
    - Optional: apply policy filter (agent role, license/flowshare rules, allowlist).
    - If multiple remain, choose lexicographically by `(Version, ModuleHash)` or policy-defined tiebreaker.
4. **Load & cache**:
    - Fetch module by `ModuleRef` (verify `ModuleHash`, signatures, provenance).
    - Instantiate per engine; reuse cached instance if ABI/spec allows (see lifecycle).
5. **Invoke**:
    - Marshal inputs to ABI.
    - Call `Entrypoint`.
    - Enforce time/memory fuel limits and capability quotas.
6. **Validate & return**:
    - Check ABI contract on outputs.
    - Apply membrane “exfiltration filter” (response validation & redaction as promised).
    - Return `DanceResponse`.

**Error handling:** Produce structured errors: `NotSupported`, `NoActiveImpl`, `ABIIncompatible`, `ModuleFetchFailed`, `SignatureInvalid`, `PolicyDenied`, `EngineError`, `Timeout`, `MemoryLimit`, `ResultValidationFailed`.

---

## 6) Module Lifecycle, Caching, Eviction

- **Cache keys**: `(Engine, ModuleHash, ABI)`; instance-specific caches may include `(SpaceId)` when overrides alter host imports.
- **Warm**: LRU or LFU for frequently used modules; prewarm on activation if policy allows.
- **Evict**: Under memory pressure, evict least-recently-used; keep provenance index regardless.
- **Isolation**: WASM instances single-threaded; no shared mutable state across invocations.
- **Pure-function posture**: Dances are stateless; all state arrives as inputs or accessed through explicit host capabilities.

---

## 7) Governance, Licensing, and Flowshare Hooks

- **Activation workflow**:
    - A `DanceImplementation` arrives with `ActivationStatus="proposed"`.
    - Membrane policy may require **two-key attest** (Steward of `T` + Space Admin) and automated checks (hash, signature, license).
    - On success, flip to `active` (space-scoped or schema default).

- **Flowshare attachment**:
    - Implementations/Types may declare a **ValueFlowPolicy** holon that expresses revenue/reciprocity terms (e.g., non-extractive use-permitted; reciprocal flowshare when vital capitals exchanged).
    - Dispatcher records `(T, D, impl_id)` in telemetry for downstream settlement.

- **Non-extractive licensing posture**:
    - Free use in non-commercial/gift contexts remains unaffected.
    - When reciprocal value flows are detected (per policy integration), contributors participate according to warrants/agreements.

---

## 8) Validation Rules (Import-time and Activation-time)

**Import-time (schema-level)**
- `supports-impl-consistency`: If `(T ImplementsDance impl)` then `(impl ForDance) ∈ (T Affords)`. Error otherwise.
- `single-active-impl`: For each `(T, D, scope)`, at most one `ActivationStatus="active"`. Error otherwise.
- `engine-fields-required`: Property presence by engine:
    - `WasmWasi` ⇒ `ModuleRef`, `Entrypoint`, `ABI`
    - `Process` ⇒ `ModuleRef`, `ABI` (and `Entrypoint` if multiplexed)
    - `RustDylib` ⇒ `ModuleRef`, `Entrypoint`, `ABI`
    - `Builtin` ⇒ `Entrypoint`, `ABI`
- `instance-type-kind-matches-extended-meta-type-name`: Continue enforcing your existing meta/type-kind rules.

**Activation-time (runtime policy)**
- `abi-compat`: `impl.ABI` supported by host.
- `module-integrity`: `ModuleHash` matches fetched bytes; signatures and attestations verified.
- `policy-eligibility`: Space policy permits activation (governance roles, allowlists, flowshare acceptance).
- `parameters-schema-match` (optional): `parameters` conform to `DanceParameterSchema`.

---

## 9) Security, Provenance, and Audit

- **Content addressing**: `ModuleRef` and `ModuleHash` cryptographically bind code identity.
- **Signatures**: Contributors sign module manifests; Spaces countersign activation.
- **Reproducibility**: Prefer reproducible builds; include build-info holon.
- **Supply chain**: Maintain provenance graph from source → build → artifact; store as holons.
- **Audit trail**: Every dispatch logs `(timestamp, agent, space, T, D, impl_id, module_hash, status, duration, fuel_used)`.

---

## 10) Engines & Host Integrations

- **WASM/WASI (preferred)**:
    - Deterministic execution with resource caps (fuel, memory).
    - Host imports expose capability-guarded functions.
    - Versioned ABI adapters `map.dance.v1`, `v2`, … allow evolution.

- **Process**:
    - IPC over stdin/stdout with canonical envelope.
    - Strong isolation; higher overhead.

- **Rust dylib**:
    - Stable FFI surface identical to ABI envelope.
    - Platform coupling; reserved for controlled deployments.

- **Builtin**:
    - Registered host handlers for critical hot paths.
    - Still declared as `DanceImplementation` with `Scope="Builtin"` for traceability.

---

## 11) Performance Considerations

- **Cold-start**: Prewarm frequently-used `(T,D)` in background when allowed by policy.
- **Batching**: Allow vectorized invocation (`Render` for many instances) when ABI supports arrays.
- **Streaming**: Optional chunked results for large outputs (with exfiltration filter applied per chunk).
- **Caching**: Separate caches for (a) holons (state), (b) modules (code), (c) relationships (indices).

---

## 12) Compatibility & Migration

- **Holochain conductor**:
    - Aligns with zome WASM loading (single-threaded WASM, dynamic dispatch).
    - This spec generalizes beyond zomes by attaching behavior to *any* TypeDescriptor.

- **Incremental rollout**:
    1) Introduce descriptors/relationships with validators, no runtime usage.
    2) Implement host-side dispatcher with `WasmWasi` only.
    3) Add governance activation path and telemetry.
    4) Add overrides (`SpaceOverride`) and precedence rules.
    5) (Optional) Add `Process`/`RustDylib` engines.

---

## 13) Open Questions

- **ABI evolution**: Which fields must be strictly stable vs. adapter-shimmed?
- **Parameter schemas**: Standardize on JSON Schema vs. ValueType holons?
- **Multi-impl composition**: Should a dance support ordered pipelines/compose-many?
- **Sandbox capability surface**: Minimum viable host imports per dance category?
- **Flowshare metering**: Best trigger points to detect “reciprocal value” reliably and fairly?

---

## 14) Acceptance Criteria

- Types can declare `Affords` and bind one or more `DanceImplementation`s.
- Host can resolve `(T,D)` to an active implementation deterministically and execute it through `map.dance.v1` ABI.
- Import-time validators catch misconfigurations; activation-time checks enforce integrity and policy.
- Telemetry records every dispatch with provenance, enabling governance and (optional) flowshare settlement.

---

## 15) Risks & Mitigations

- **Complexity creep** → Keep dispatcher minimal; push variability to data + ABI.
- **Security of third-party code** → Content hashing, signatures, sandboxing, capability gates, resource caps.
- **Version skew** → Semantic ranges with explicit pins; strong precedence rules; safe fallbacks.
- **Memory growth** → LRU/LFU eviction, per-engine instance pooling, prewarm limits.

---

## 16) Next Steps

1. Add new descriptors and relationships to the metaschema & base-core import files.
2. Implement import-time validation rules listed above.
3. Define `map.dance.v1` ABI envelope precisely (field names, encoding, error codes).
4. Build the host dispatcher (WASM/WASI path first) + module cache.
5. Implement governance activation flows and attest capture.
6. Instrument telemetry and add audit holons.
7. Ship example: `BookType` with `Render` dance (schema default) and a Space-scoped override.

---