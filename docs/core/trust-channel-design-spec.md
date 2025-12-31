# MAP Trust Channel — Developer Design Spec (Fully Expanded)

## 0. Purpose & Scope
The **Trust Channel** is the MAP core service that encapsulates, transports, and validates **Dance Capsules** whenever an interaction crosses a **membrane boundary** between Spaces. It enforces Agreement-governed security, privacy, and protocol consistency through layered envelopes that correspond to membrane validation gates.

Trust Channels:

- Exist **only** in the Rust runtime; the TypeScript SDK never hosts a Trust Channel.
- Are always governed by an **Agreement**, which defines envelope sequencing, crypto, protocol, and policy parameters.
- During capsule formation, perform **Protocol Negotiation** to dynamically select a compatible **ProtocolSuite** from the candidate protocols authorized by the Agreement. 
- Trigger the transport and validation mechanism for all cross-Space Dances.

The TypeScript↔Rust interface inside a single Tauri process is *not* a membrane boundary and therefore bypasses Trust Channel logic.

---

## 1. Deployment Architecture

### 1.1 System Topology Overview
Each **Agent** in MAP operates within an **Agreement Space**—a space containing all (and only) those Agents that share at least one Agreement. Agents are depicted as spheres connected by a **mycelial web** of Trust Channels representing the live peer-to-peer fabric.

- **Source Container:** Rust runtime of the sending Agent (Space A).
- **Destination Container:** Rust runtime of the receiving Agent (Space B).
- **Trust Channel:** logical and cryptographic conduit linking both membranes.
- **Transport Protocol:** the routing mechanism defined by the Agreement (e.g., DHT gossip, relay, or direct peer link).

When a **DanceRequest** leaves an Agent’s pore, it travels through the Trust Channel across the mycelial web, wrapped in layers of envelopes that perform sequential validation.  
At the receiving pore, the Trust Channel unwraps these envelopes inward, validating routing, signature, encryption, authorization, and dispatch.  
A **DanceResponse** is then re-encapsulated with outbound envelopes in reverse order and sent back through the same path.

### 1.2 Trust Channel Cross-Section
Each Trust Channel is visualized as a **funnel** through the agent’s membrane.  
Envelopes are represented as **gates**, initially closed.  
As validation succeeds layer by layer, each gate opens and the remaining inner capsule drops through to the next gate until only the inner **Dance** remains.  
Outbound responses travel upward through the same funnel, having their envelopes reapplied and gates resealed.

### 1.3 Implementation Layers and Protocol Adapters

Every membrane-crossing exchange follows the same structural flow:

```
┌───────────────────────────────────────────────┐
│  Protocol Adapters (transport-specific)       │
│  ├─ Holochain extern adapter                  │
│  ├─ Direct Wire adapter (future)              │
│  ├─ Relay / HTTP adapter (future)             │
└───────────────┬───────────────────────────────┘
                │  (Capsule ingress / egress)
                ▼
         CapsuleDancer::dance_capsule()
                │
                ▼
           TrustChannel
      (unwrap → validate → dispatch)
                │
                ▼
             Dancer
          (executes the Dance)
                │
                ▼
           TrustChannel
      (wrap → encrypt → sign)
                │
                ▼
         CapsuleDancer::dance_capsule()
```

**Key Points**

- The `#[hdk_extern] fn dance_capsule` in the Holochain build acts as the *Holochain Protocol Adapter*—the membrane pore for that protocol.
- All protocol adapters, present and future, delegate to the same `CapsuleDancer::dance_capsule` function.
- `CapsuleDancer` is protocol-agnostic; it receives inbound capsules and hands them to the `TrustChannel` for envelope handling and dispatch.
- `TrustChannel` performs the actual wrap/unwrap sequence, policy enforcement, suite negotiation, and orchestration of requests and replies.
- `Dancer` executes the validated `Dance` inside the local space after all Trust Channel gates have cleared.

This layering produces a **unified ingress/egress interface** shared across all transports.  
It ensures that Trust Channel logic, envelope validation, and Agreement-based security are applied consistently—no matter which protocol conveys the capsule.

---

## 2. Core Concepts

### 2.0 Narrative Overview

The Trust Channel’s terminology and type system are intentionally aligned with the language of Dances.  
Every core trait and struct name was chosen to reflect its role in the lifecycle of a Dance and to make Trust Channel code read semantically true to its purpose.  
This consistency ensures that both developers and auditors can infer each component’s responsibility directly from its name.

| Conceptual Role | Rust Type | Primary Verb | Description |
|-----------------|------------|---------------|-------------|
| **Dance Initiator** | `trait DanceInitiator` | *initiate* | Begins a new Dance across a membrane. The caller works purely with Dances, not Capsules. |
| **Trust Channel** | `struct TrustChannel` | *convey* | Implements `DanceInitiator` and `CapsuleDancer`; orchestrates the wrapping, validation, and transport of Capsules. |
| **Capsule Dancer** | `trait CapsuleDancer` | *dance* | Protocol-agnostic ingress/egress interface invoked by all protocol adapters (Holochain, Wire, HTTP, etc.). |
| **Dancer** | `trait Dancer` | *dance* | Executes the validated `Dance` inside the local space after all Trust Channel gates have cleared. |

#### Narrative Rule
> *Initiators initiate dances;  
> Trust Channels convey dances via capsules;  
> Capsule Dancers dance capsules;  
> and Dancers dance dances.*

This rule serves as the linguistic foundation of the Trust Channel’s architecture.  
The following sections describe how Dances are encapsulated, validated, and conveyed through the membrane layers defined by their governing **Agreements** and **ProtocolSuites**.

### 2.1 Dance Capsule
A **Dance Capsule** is a Russian doll–like structure of nested **Envelopes** that surround a `Dance` (request or response).  
Each envelope performs one membrane function: routing, authentication, encryption, authorization, state transfer, dispatch, or filtering.

**Inbound validation sequence:**  
`Transport → AuthN → Crypto → AuthZ → Dispatch → SessionState → Payload`

**Outbound response sequence:**  
`Payload → SessionState → Exfiltration → Crypto → AuthN → Transport`

For inbound capsules, each layer exposes progressively unwrapped content to the next validation phase until only the inner **PayloadEnvelope** remains, revealing the `Dance` to be executed.  
For outbound capsules, each layer successively rewraps the content, sealing the validated `DanceResponse` for return transport.

The **SessionStateEnvelope** appears immediately inside the Dispatch/Exfiltration boundary.  
It carries transient holon state and nursery references needed for stateless or multi-step executions, ensuring that ephemeral context can safely cross the membrane without persistent storage.

---

### 2.2 Agreement and ProtocolSuite

Each Trust Channel is governed by an **Agreement**, which defines the policies, cryptographic parameters, and procedural rules that bind all participants within its trust domain.  
An Agreement is not a design-time construct; it is a **runtime artifact** produced through the **Promise Weave Protocol**, in which participating agents exchange and mutually sign reciprocal promises.  
Those promises collectively determine the channel’s trust semantics, including the **ProtocolSuite** to be used for all subsequent capsule exchanges.

The resulting ProtocolSuite is **pinned** to the Agreement at the moment the weave completes.  
It defines the complete envelope composition and validation order for the channel, ensuring that all parties share a common, immutable understanding of how capsules are formed, validated, and conveyed.  
Once established, the suite cannot be altered dynamically — only the **transport protocol** that carries the capsules may vary at runtime.

An **Agreement** specifies:

- Its governing **ProtocolSuite** (defining the envelope structure and allowable transport families for this trust domain).
- Mappings between Dances and the suite via `DancePolicyMap`.
- Cryptographic and policy relationships (`AuthZPolicy`, `CryptoPolicy`, `ExfiltrationPolicy`, `StepUpPolicy`).

A **ProtocolSuite** holon defines:

- The ordered envelope sequences for inbound and outbound directions, including whether the **SessionStateEnvelope** is *required* or *optional*.
- The validator modules for each envelope kind.
- The cryptographic, authorization, and state-transfer policies applied at each layer.
- The set of transport protocols supported for runtime selection.

Together, the Agreement and its pinned ProtocolSuite completely determine the membrane behavior for all capsule exchanges within that domain.  
Only the transport protocol remains subject to runtime negotiation.

---

### 2.3 Protocol Negotiation

Protocol negotiation determines which **transport protocol** will be used for a specific capsule exchange under an established Agreement.  
All higher-level parameters — envelope ordering, policies, and validation gates — are pinned by the Agreement’s ProtocolSuite and cannot vary at runtime.

Negotiation occurs only when sender and receiver must select among the transport mechanisms enumerated in the Agreement.  
This selection allows peers to adapt to transient network conditions such as reachability, latency, or relay availability without altering the trust semantics of the exchange.

**Negotiation Steps**

1. **Proposal** — The sender selects a candidate transport from the ProtocolSuite’s supported set and records it as `ProposesTransport` in the outer `TransportEnvelope`.
2. **Validation** — The receiver confirms that the proposed transport is allowed under the Agreement and compatible with the pinned `ProtocolSuite`.
3. **Response** — The receiver records its choice as `AcceptedTransport`, either confirming the proposal or selecting an alternative from the allowed set.
4. **Pinning** — The capsule pins `PinnedAgreement → Agreement`, `PinnedSuite → ProtocolSuite`, and `NegotiatedTransport → TransportProtocol`.
5. **Verification** — Upon receipt, validators confirm that the negotiated transport matches the Agreement’s definitions and that all pinned parameters remain consistent.

**Example**
```
TransportEnvelope
 ├── ForAgreement → #agr:std
 ├── PinnedSuite → #suite:std-full
 ├── ProposesTransport → DHT
 └── AcceptedTransport → Relay
```

Once transport selection is complete, the capsule exchange proceeds under the pinned `ProtocolSuite`.  
Envelope ordering, cryptographic policies, and validation rules remain invariant throughout the interaction, ensuring that every Trust Channel behaves consistently with the terms of its Agreement.

### 2.4 Session State Envelope
The **SessionStateEnvelope** enables stateful workflows to operate across otherwise stateless environments.  
It serializes transient holons and relationship references needed to resume an in-flight Dance while preventing data persistence outside the membrane.

**Conceptual Purpose**
- Provides transient continuity between asynchronous or multi-step Dances.
- Avoids leaking ephemeral data into long-lived storage.
- Ensures transient state passes through the same validation gates as other envelopes.

**Holon Type and Relationships**
```
HolonType: SessionStateEnvelope
Relationships:
  Wraps → PayloadEnvelope
  CarriesState → [TransientHolonPool, NurseryRefs]
```

**Key Data Fields**
- `state_hash`: integrity checksum of serialized transient data
- `state_length`: size of the transient payload in bytes
- `allowed_types`: whitelist of permitted transient holon types

**Processing Steps**
**Build**
1. Serialize the transient pool and nursery references.
2. Compute and record the state hash and metadata.
3. Attach to the inner `PayloadEnvelope`.

**Validate**
1. Verify hash integrity and payload size.
2. Deserialize the transient pool into local memory.
3. Enforce the `allowed_types` whitelist.

**Expected Outcome**
Transient state is hydrated in the recipient’s runtime context, enabling seamless continuation of execution without permanent storage.

*Current Implementation Status:*  
The Session State Envelope is the only Trust Channel layer realized in the initial implementation (**Issue #308**).  
All other envelopes remain stubbed for future iterations once cross-Space communication is activated.

---

### 2.4 Roles, Traits, and Naming Narrative

MAP adopts consistent nouns and verbs so that Trust Channel code reads like the story it represents.  
Each trait name and its primary verb mirror the narrative logic of a Dance.

| Conceptual Role     | **Rust Type**                                                             | **Key Function(s)**                                | **Primary Verb** | **Operates On**                | **Description**                                                                                  |
|---------------------|---------------------------------------------------------------------------|----------------------------------------------------|------------------|--------------------------------|--------------------------------------------------------------------------------------------------|
| **Dance Initiator** | `trait DanceInitiator`                                                    | `async fn initiate_dance(&self, context, request)` | *initiate*       | `DanceRequest ↦ DanceResponse` | Begins a new Dance across a membrane. The caller sees only Dances, not Capsules.                 |
| **Trust Channel**   | `struct TrustChannel` *(implements `DanceInitiator` and `CapsuleDancer`)* | `initiate_dance()` / `dance_capsule()`             | *convey*         | `Capsule`                      | Governs envelope wrapping/unwrapping, validation, and transport orchestration.                   |
| **Capsule Dancer**  | `trait CapsuleDancer`                                                     | `fn dance_capsule(&self, capsule)`                 | *dance*          | `Capsule ↦ Capsule`            | Protocol-agnostic ingress/egress interface called by all adapters (Holochain, Wire, HTTP, etc.). |
| **Dancer**          | `trait Dancer`                                                            | `async fn dance(&self, request)`                   | *dance*          | inner `Dance`                  | Executes the validated Dance inside the local space once all Trust Channel gates have cleared.   |

#### Narrative Rule
> *Initiators initiate dances;  
> Trust Channels convey dances via capsules;  
> Capsule Dancers dance capsules;  
> and Dancers dance dances.*

These naming conventions preserve conceptual clarity, separate transport concerns from trust logic, and ensure that function names describe their precise role in the Dance lifecycle.

---


## 3. Envelope Layer Reference (Expanded)
*(Each layer acts as a gate in the membrane funnel.)*

---

### 3.1 Transport Envelope
**Summary:** The outermost envelope governing routing, Agreement pinning, and protocol negotiation.

#### Conceptual Purpose
The **TransportEnvelope** establishes the routing and trust context for the capsule. It ensures that the message travels only between agents authorized by the governing Agreement and that both peers agree on the ProtocolSuite governing this exchange.

#### Holon Type and Relationships
```
HolonType: TransportEnvelope
Relationships:
  Wraps → AuthNEnvelope
  ForAgreement → Agreement
  ProposesSuite → ProtocolSuite?
  AcceptedSuite → ProtocolSuite
  SenderAgent → Agent
  RecipientAgent → Agent
```

#### Key Data Fields
- `sender_id`: Agent identifier of initiator
- `recipient_id`: target Agent identifier
- `agreement_ref`: reference to Agreement ID and version hash
- `transport_protocol`: protocol to be used (DHT, relay, direct)
- `timestamp`: for replay detection
- `routing_signature`: optional checksum or route proof

#### Processing Steps
**Build:**
1. Fetch Agreement metadata; confirm peer is an authorized participant.
2. Select candidate `ProtocolSuite` and record as `ProposesSuite`.
3. Compute and store routing metadata and Agreement hash.
4. Attach the next envelope as payload.

**Validate:**
1. Verify Agreement hash matches local record.
2. Check recipient field corresponds to the local Agent.
3. Confirm `AcceptedSuite` belongs to Agreement’s allowed suites.
4. Resolve routing path via Agreement transport settings.

#### Expected Outcome
Validated routing context and pinned Agreement; the capsule is confirmed to have arrived at the correct membrane pore under the proper governance framework.

#### Developer Guidance
Rust developers should implement this as the first validator in the inbound pipeline. TransportEnvelope validation failures typically indicate misrouting or incompatible Agreements.

---

### 3.2 Authentication Envelope (AuthN)
**Summary:** Establishes the authenticity and integrity of the capsule.

#### Conceptual Purpose
The **AuthNEnvelope** confirms that the message was genuinely sent by an authorized participant and that its contents have not been modified since transmission.

#### Holon Type and Relationships
```
HolonType: AuthNEnvelope
Relationships:
  Wraps → CryptoEnvelope
  SignerAgent → Agent
  UsesCryptoPolicy → CryptoPolicy
```

#### Key Data Fields
- `signature_scheme`: algorithm identifier (e.g., Ed25519)
- `signature`: base64 signature of inner envelope hash
- `signer_public_key_ref`: pointer to sender’s public key within Agreement
- `signed_hash`: computed SHA-256 or BLAKE3 digest

#### Processing Steps
**Build:**
1. Serialize the inner envelope and compute hash.
2. Sign the hash using the sender’s private key via Lair.
3. Attach signature and metadata.

**Validate:**
1. Retrieve sender’s public key from Agreement.
2. Recompute hash of the inner envelope.
3. Verify signature using declared algorithm.
4. Log outcome to telemetry for risk analysis.

#### Expected Outcome
Message integrity and sender authenticity confirmed. If verification fails, the capsule is discarded.

#### Developer Guidance
Use the `ring` or `ed25519_dalek` crates for signing/verification; keys must always be accessed through Lair interfaces. Avoid holding private keys in process memory longer than necessary.

---

### 3.3 Cryptography Envelope (Crypto)
**Summary:** Provides confidentiality by encrypting the inner payload.

#### Conceptual Purpose
The **CryptoEnvelope** ensures that only the intended recipient can read the inner payload. It also provides tamper protection and payload freshness via nonces.

#### Holon Type and Relationships
```
HolonType: CryptoEnvelope
Relationships:
  Wraps → AuthZEnvelope
  RecipientAgent → Agent
  UsesCryptoPolicy → CryptoPolicy
```

#### Key Data Fields
- `cipher_suite`: e.g., XChaCha20-Poly1305
- `nonce`: unique per message
- `encrypted_payload`: ciphertext of next envelope
- `key_ref`: recipient public key or shared secret identifier

#### Processing Steps
**Build:**
1. Serialize inner envelope.
2. Generate random nonce.
3. Encrypt payload with recipient’s public key or derived shared secret.
4. Attach cipher suite metadata.

**Validate:**
1. Fetch recipient private key from Lair.
2. Decrypt payload using declared cipher suite.
3. Verify authentication tag integrity.
4. Replace ciphertext with plaintext inner envelope.

#### Expected Outcome
Payload decrypted successfully; the next layer is now readable only by authorized recipient.

#### Developer Guidance
Follow the crypto policy declared in Agreement. Ensure nonce uniqueness per sender-recipient-session to prevent replay attacks.

---

### 3.4 Authorization Envelope (AuthZ)
**Summary:** Enforces role- and scope-based permission checks.

#### Conceptual Purpose
The **AuthZEnvelope** ensures the request is permitted under the Agreement’s role, scope, and timing rules. It acts as a programmable contract verifying that the sender’s authority matches the Dance being requested.

#### Holon Type and Relationships
```
HolonType: AuthZEnvelope
Relationships:
  Wraps → DispatchEnvelope
  ForAgreement → Agreement
  EvaluatedBy → AuthZPolicy
```

#### Key Data Fields
- `role`: sender’s role within Agreement
- `scope`: access scope or resource domain
- `policy_tag`: identifier for specific AuthZPolicy
- `valid_from` / `valid_until`: temporal constraints
- `policy_signature`: optional policy binding proof

#### Processing Steps
**Build:**
1. Query Agreement for sender’s role and applicable AuthZPolicy.
2. Embed policy tag and validity window.
3. Sign policy tag if required.

**Validate:**
1. Fetch AuthZPolicy from Agreement.
2. Evaluate role-scope alignment against requested Dance.
3. Check time window validity.
4. Verify policy signature if provided.

#### Expected Outcome
Authorization confirmed. Capsule can proceed to dispatch. If denied, validation stops with `HolonError::UnauthorizedRole`.

#### Developer Guidance
The AuthZ layer is where governance logic is enforced. Ensure policies are declarative holons so they can evolve without code changes.

---

### 3.5 Dispatch Envelope
**Summary:** Controls membrane handoff to local execution.

#### Conceptual Purpose
The **DispatchEnvelope** represents the moment a capsule transitions from inter-Space validation into intra-Space execution. It validates the target I-Space, ensures that the Dance type is known locally, and checks that any declared target matches an available handler.

#### Holon Type and Relationships
```
HolonType: DispatchEnvelope
Relationships:
  Wraps → PayloadEnvelope
  TargetSpace → Space
```

#### Key Data Fields
- `target_space`: identifier of destination I-Space or subcontext
- `execution_context`: optional environment variables
- `dispatch_signature`: integrity hash of routing parameters

#### Processing Steps
**Build:**
1. Determine target I-Space based on Agreement routing.
2. Compute dispatch hash.
3. Attach as header to envelope.

**Validate:**
1. Confirm that `target_space` matches local identifier.
2. Check that Dance type exists and is callable.
3. Log dispatch acceptance event.

#### Expected Outcome
Local execution context prepared; control passed to Choreographer.

#### Developer Guidance
Implement DispatchEnvelope validation as the final gate before local code execution. Validation failures should never trigger automatic retries.

---

### 3.6 Payload Envelope
**Summary:** Contains the actual DanceRequest or DanceResponse.

#### Conceptual Purpose
The **PayloadEnvelope** is the innermost layer, containing the semantic content of the interaction. At this point all membrane gates have been cleared.

#### Holon Type and Relationships
```
HolonType: PayloadEnvelope
Relationships:
  HasPayloadDance → Dance
```

#### Key Data Fields
- `payload_type`: Request or Response
- `payload_model`: descriptor name
- `payload_digest`: hash for integrity
- `content_encoding`: optional compression scheme

#### Processing Steps
**Build:**
1. Serialize Dance into canonical format.
2. Compute payload hash.
3. Embed descriptor metadata.

**Validate:**
1. Verify hash matches payload content.
2. Deserialize Dance into model.
3. Pass to Choreographer.

#### Expected Outcome
Validated and deserialized Dance ready for execution.

#### Developer Guidance
This envelope rarely fails validation except for integrity mismatches. Any schema errors should be handled by the Choreographer.

---

### 3.7 Exfiltration Envelope (Outbound)
**Summary:** Filters outbound data per Agreement’s ExfiltrationPolicy.

#### Conceptual Purpose
The **ExfiltrationEnvelope** ensures that responses leaving a Space comply with that Space’s data sharing rules. It enforces outbound privacy and ensures that only agreed-upon data crosses the membrane.

#### Holon Type and Relationships
```
HolonType: ExfiltrationEnvelope
Relationships:
  Wraps → CryptoEnvelope
  AppliesPolicy → ExfiltrationPolicy
```

#### Key Data Fields
- `policy_tag`: identifier of applied ExfiltrationPolicy
- `allowed_fields`: whitelist of fields
- `thresholds`: quantitative limits (e.g., max records)
- `sanitization_map`: redaction rules

#### Processing Steps
**Build:**
1. Retrieve ExfiltrationPolicy from Agreement.
2. Filter or redact prohibited fields.
3. Record policy tag and transformation metadata.

**Validate:**
1. Confirm policy tag exists and matches Agreement.
2. Verify filtered payload complies with declared thresholds.
3. Hash sanitized payload for audit.

#### Expected Outcome
Outbound data sanitized, ready for encryption.

#### Developer Guidance
Developers must implement serialization filters at this layer. Avoid policy logic in business code; always reference ExfiltrationPolicy holons.

---

### 3.8 Unlock Envelope (Optional)
**Summary:** Captures Second-Factor Session (SFS) verification for sensitive Dances.

#### Conceptual Purpose
The **UnlockEnvelope** adds human-level verification to the cryptographic stack. It confirms that the user controlling the device has recently authenticated through a configured second factor before performing sensitive or high-risk operations.

#### Holon Type and Relationships
```
HolonType: UnlockEnvelope
Relationships:
  Wraps → NextEnvelope
  VerifiedBy → StepUpPolicy
  SessionBelongsTo → Agent
```

#### Key Data Fields
- `session_id`: UUID of SFS
- `verified_method`: biometric | PIN | hardware_key
- `expires_at`: timestamp
- `issued_at`: timestamp

#### Processing Steps
**Build:**
1. Verify an active SFS exists for this Agent.
2. Record method and expiry.
3. Link to StepUpPolicy.

**Validate:**
1. Fetch SFS from secure store.
2. Check TTL and idle timeout.
3. Confirm cryptographic binding to Agent ID.

#### Expected Outcome
Step-up authentication confirmed; the Dance may proceed.

#### Developer Guidance
UnlockEnvelope creation and validation should integrate with the device OS authentication APIs. Never store SFS secrets in application memory.

---

### 3.9 SessionState Envelope (Optional)
**Summary:** Transports transient holon state for stateless executions.

#### Conceptual Purpose
The **SessionStateEnvelope** allows stateful workflows to execute in stateless environments by serializing necessary transient holons and relationship references. It ensures the guest process has enough context to continue processing without permanent data leakage.

#### Holon Type and Relationships
```
HolonType: SessionStateEnvelope
Relationships:
  Wraps → PayloadEnvelope
  CarriesState → [TransientHolonPool, NurseryRefs]
```

#### Key Data Fields
- `state_hash`: integrity checksum
- `state_length`: size in bytes
- `allowed_types`: whitelist of permitted transient types

#### Processing Steps
**Build:**
1. Serialize transient pool and nursery references.
2. Compute hash and record metadata.
3. Attach to next envelope.

**Validate:**
1. Verify hash integrity.
2. Deserialize transient pool.
3. Enforce allowed_types filter.

#### Expected Outcome
State hydrated in recipient’s transient context; execution can proceed seamlessly.

#### Developer Guidance
Keep transient pools small. This mechanism is not intended for bulk data transfer. Always validate deserialized objects before use.

---

## 4. Lifecycle Overview
1. **Outbound Request:** Select suite, negotiate, build, transmit.
2. **Inbound Validation:** Validate sequentially (Transport→AuthN→Crypto→AuthZ→Dispatch→Payload).
3. **Response:** Apply outbound envelopes in reverse order and send back.

---

## 5. Error Handling
| Error                        | Description               |
|------------------------------|---------------------------|
| `InvalidAgreementRef`        | Agreement hash mismatch.  |
| `ProtocolSuiteMismatch`      | Suite not permitted.      |
| `InvalidProtocolProposal`    | Proposed suite invalid.   |
| `SuiteDownshiftNotPermitted` | Unauthorized fallback.    |
| `SignatureInvalid`           | AuthN failure.            |
| `DecryptionFailed`           | Crypto validation failed. |
| `UnauthorizedRole`           | AuthZ check failed.       |
| `DispatchDenied`             | Target invalid.           |
| `ExfiltrationDenied`         | Policy violation.         |
| `RequiresSecondFactor`       | Missing SFS.              |
| `SessionStateUnavailable`    | Missing transient data.   |

---

## 6. Implementation Notes
- All envelopes and policies are holons declared in the Meta-Schema.
- Validators and builders are modular and referenced dynamically via descriptors.
- Use Lair for all key operations; private keys never exposed.
- Emit telemetry for every validation result to support audit and behavioral analysis.
- Agreements may define multiple suites per sensitivity tier for flexible negotiation.

### 6.1 Packaging and Dependency Isolation

Protocol-specific dependencies—such as Holochain’s `hdk`—are confined to **adapter crates**.  
The Trust Channel and Capsule Dancer remain pure Rust libraries, enabling protocol pluggability and independent evolution.

**Recommended Crate Layout**
```
map_core/                ← holons, agreements, policies
map_trust_channel/       ← DanceInitiator, CapsuleDancer, TrustChannel
map_holochain_adapter/   ← Holochain externs (depends on `hdk`)
map_wire_adapter/        ← future direct P2P adapter
map_http_adapter/        ← future relay / gateway adapter
```

**Key Principles**
- Core and trust-channel crates contain no direct dependency on `hdk` or any host framework.
- Each adapter crate provides its own membrane interface (e.g., `#[hdk_extern] fn dance_capsule`) and delegates to the same `CapsuleDancer` implementation.
- This encapsulation enables testing and reuse of the Trust Channel in multiple environments and ensures that only the outermost adapter layer needs updating when a transport changes.

---

## 7. Summary
The Trust Channel provides a **layered, Agreement-driven security framework** for all cross-Space communications.  
Each envelope serves a distinct purpose, from routing and authentication to encryption, authorization, dispatch, and outbound filtering.  
Protocol negotiation guarantees interoperability, while each validation gate enforces sovereignty and trust.  
This layered architecture transforms MAP’s peer-to-peer network into a **self-verifying, self-governing fabric** for secure inter-Space collaboration.


### Appendix A — Unified Ingress / Egress Summary

**Unified Capsule Flow**

```
Protocol Adapter  →  CapsuleDancer::dance_capsule()
                         ↓
                     TrustChannel
               (unwrap → validate → dispatch)
                         ↓
                        Dancer
               (executes the Dance logic)
                         ↓
                     TrustChannel
               (wrap → encrypt → sign)
                         ↓
                CapsuleDancer::dance_capsule()
                         ↓
                 Protocol Adapter (reply)
```

**Benefits**
- **Single ingress/egress interface:** All protocols converge on `CapsuleDancer::dance_capsule`.
- **Security consistency:** Every request and response passes through the same validation gates.
- **Isolation of dependencies:** Framework bindings remain in adapter crates only.
- **Extensibility:** New protocols can be added without altering Trust Channel logic.
- **Narrative clarity:** Code reads naturally—initiators initiate, dancers dance, and capsules are danced through the Trust Channel.