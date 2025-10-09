# MAP Context-Aware Capsulization & Session State Strategies — Design Spec

## 0. Purpose & Scope
This specification defines how MAP determines the **appropriate capsulization strategy** for a given Dance invocation based on the **interaction context**, and how session state is managed across contexts where state continuity cannot be assumed.

It extends the MAP Trust Channel and Security Model specifications by describing:
- Context profiles for different communication topologies.
- How envelope stacks are constructed dynamically.
- How session state (transient holon pools, nursery references) is shipped or resolved.
- How Agreements override or refine these defaults for cross-Space exchanges.

---

## 1. Architectural Overview

### 1.1 Context-Aware Capsuleization
A **capsuleization strategy** determines which envelopes are applied around a Dance payload when building or validating a Dance Capsule.  
The selected strategy depends on:
- The **context boundary** being crossed (in-process, inter-agent, or cross-space).
- The **trust surface** (same process vs. network transport).
- The **state continuity** (whether the callee maintains persistent context).
- The **Agreement** defining additional envelope requirements for cross-space flows.

Capsuleization is governed by **ContextProfiles**, not hard-coded paths.  
Each ContextProfile maps a boundary type to an ordered list of envelope kinds and defines its state-handling strategy.

---

## 2. Context Profiles

### 2.1 Profile Definition

**Holon Type:** `ContextProfile`  
**Key Properties:**
- `src_env` / `dst_env` (TypeScript, RustHost, RustGuest, RemoteSpace)
- `space_boundary` (None | SameSpace | CrossSpace)
- `trust_surface` (InProcess | LocalIPC | LAN | WAN | DHT)
- `state_strategy` (NoShipping | ShipSessionState)
- `default_envelope_set` (ordered list of envelope kinds)
- `gating_policy` (conditions for step-up or extra envelopes)

Relationships:
```
ContextProfile
 ├── UsesEnvelopeType → [EnvelopeType...]
 ├── AppliesStateStrategy → StateStrategy
 ├── UsesStepUpPolicy → StepUpPolicy
 └── OverridesByAgreement → Agreement?
```

Each ContextProfile is itself a holon, discoverable and replaceable by Agreements that define custom profiles.

---

### 2.2 Canonical Profiles

| Context                                      | Boundary   | State Strategy          | Envelope Stack (inbound/outbound)                                                                                                | Notes                                      |
|----------------------------------------------|------------|-------------------------|----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------|
| **TypeScript → Rust (Tauri same process)**   | None       | NoShipping              | [Unlock?], [Payload]                                                                                                             | Not a membrane; minimal capsule.           |
| **Rust Host → Rust Guest (stateless guest)** | SameSpace  | ShipSessionState        | [Unlock?], [AuthZ?], [SessionState], [Payload]                                                                                   | State ping-ponged; optional logical AuthZ. |
| **Space A → Space B (network/DHT)**          | CrossSpace | Configured by Agreement | [Transport, AuthN, Crypto, AuthZ, Dispatch, Unlock?, SessionState?, Payload] / [Payload, Exfiltration, Crypto, AuthN, Transport] | Full capsule sequence.                     |

Each profile defines the **expected validator order** and **transient state behavior** for the trust surface.

---

## 3. CapsuleBuilder & CapsuleValidator

### 3.1 CapsuleBuilder
Constructs Dance Capsules based on a ContextProfile (or Agreement-overridden suite).

Steps:
1. Identify active `ContextProfile` based on src/dst environment.
2. Select the appropriate `ProtocolSuite` from Agreement (if CrossSpace).
3. Build envelope stack using `default_envelope_set`, applying:
    - `UnlockEnvelope` if required by gating_policy.
    - `SessionStateEnvelope` if `ShipSessionState`.
4. Pin `Agreement` and `ProtocolSuite` references.
5. Compute hash chain for envelope integrity.

Output: a complete `DanceCapsule` ready for transport.

### 3.2 CapsuleValidator
Sequentially validates and unwraps envelopes according to the same ContextProfile or pinned ProtocolSuite.

Steps:
1. Read `PinnedAgreement` / `NegotiatedSuite` (outermost layer).
2. Validate envelopes in declared order.
3. Invoke pluggable validators for each envelope type.
4. Rehydrate transient state if a `SessionStateEnvelope` is present.
5. Return the unwrapped `Dance` to the Choreographer.

---

## 4. State Management Strategies

### 4.1 NoShipping
**Use when:** both ends share live memory context (e.g., TypeScript↔Rust).
- Only references are passed; no state serialization.
- All resolution occurs in host context.

### 4.2 ShipSessionState
**Use when:** the recipient is stateless (e.g., Rust Guest or remote Space).
- Serialize the **TransientHolonPool** and **NurseryRefs** into a `SessionStateEnvelope`.
- Validate integrity via content hash and policy (e.g., allowed reference types).
- On receive, hydrate these pools in the callee’s transient context.

**Holon Type:** `SessionStateEnvelope`  
Relationships:  
`CarriesState → [TransientHolonPool, NurseryRefs]`

Validation rules:
- `state_hash` must match computed digest.
- Only whitelisted transient holon types may be shipped across a membrane.
- State size thresholds enforced by policy.

---

## 5. Gating and Step-Up Policies

Each ContextProfile references a `StepUpPolicy`, which governs whether a local unlock is required.

Triggers:
- Dance sensitivity (Elevated | Critical)
- Behavioral risk score ≥ threshold
- Explicit `require_step_up` flag from Agreement

If triggered, an `UnlockEnvelope` is inserted before the Payload.  
The validator checks that the active **Second Factor Session (SFS)** is valid, unexpired, and not revoked.

**Holon Type:** `UnlockEnvelope`  
Relationships:  
`VerifiedBy → StepUpPolicy`

---

## 6. Agreement Overrides

Agreements can override ContextProfiles for cross-space interactions.

**Mechanism:**
- Agreement declares a `UsesContextProfile` relationship.
- During capsule creation, the Trust Channel uses this Agreement-specific profile instead of the default one.
- This allows different spaces to negotiate alternate envelope sets or state strategies.

Example:
```
Agreement ──UsesContextProfile──► ContextProfile: secure-bridge-v2
ContextProfile.secure-bridge-v2:
   EnvelopeStack: [Transport, AuthN, Crypto, AuthZ, Dispatch, Payload]
   StateStrategy: NoShipping
   StepUpPolicy: AlwaysRequire
```

---

## 7. Session State Envelope Flow Example

**Rust Host → Rust Guest (stateless guest):**

DanceCapsule  
├── UnlockEnvelope (if Sensitive or risky)  
│   └── SessionStateEnvelope  
│       ├── CarriesState → TransientHolonPool  
│       └── Wraps → PayloadEnvelope  
│           └── HasPayloadDance → Dance  
│               └── HasRequest → LoaderHolonSegment

Validation sequence:
1. UnlockEnvelope → verify SFS.
2. SessionStateEnvelope → validate state integrity.
3. PayloadEnvelope → execute Dance with hydrated transient context.

---

## 8. State Resolution Rules

### 8.1 TransientHolonPool
- Contains staged holons awaiting persistence or relationship resolution.
- Used for Pass 1–2 data loader operations.
- Must not contain persistent identifiers or DHT addresses.

### 8.2 NurseryRefs
- Lightweight handles for deferred relationship resolution.
- Hydrated during guest execution; discarded afterward.

### 8.3 Security Implications
- State shipping must respect Agreement-defined data-sharing limits.
- Certain value types (e.g., MapBytesValueType, MapIdValueType) may be redacted or masked when crossing membranes.
- Session state is never persisted; it expires at end of Dance execution.

---

## 9. Context Selection Logic

Algorithm for capsuleization:
1. Determine context (TS→Rust, Host→Guest, Space↔Space).
2. Load corresponding ContextProfile.
3. If Agreement present:
    - Override profile with Agreement’s `UsesContextProfile` if specified.
    - Use `ProtocolSuite` from Agreement to determine final envelope set.
4. Apply gating_policy → insert UnlockEnvelope if required.
5. Apply state_strategy → add SessionStateEnvelope if needed.
6. Assemble and send capsule.

This algorithm ensures **capsuleization is adaptive**, not static — matching security, performance, and state requirements to context.

---

## 10. Summary

Context-aware capsuleization allows MAP to:
- Optimize in-process Dances (minimal envelopes, no overhead).
- Support stateless guests via controlled state shipping.
- Enforce Agreement-defined envelope sequences for cross-space trust.
- Dynamically add authentication layers when sensitivity or behavioral risk warrants it.

By encoding these strategies as holons (`ContextProfile`, `StateStrategy`, `StepUpPolicy`), capsule formation and validation remain fully **data-driven, extensible, and discoverable** — consistent with MAP’s self-describing architecture.