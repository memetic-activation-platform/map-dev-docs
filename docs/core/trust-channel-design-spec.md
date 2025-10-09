# MAP Trust Channel — Developer Design Spec (Fully Expanded)

## 0. Purpose & Scope
The **Trust Channel** is the MAP core service that encapsulates, transports, and validates **Dance Capsules** whenever an interaction crosses a **membrane boundary** between Spaces. It enforces Agreement-governed security, privacy, and protocol consistency through layered envelopes that correspond to membrane validation gates.

Trust Channels:

- Exist **only** in the Rust runtime; the TypeScript SDK never hosts a Trust Channel.
- Are always governed by an **Agreement**, which defines envelope sequencing, crypto and policy parameters.
- Dynamically select compatible **ProtocolSuites** through **Protocol Negotiation** during capsule formation.
- Trigger the transport and validation mechanism for all cross-Space Dances.

The TypeScript↔Rust interface inside a single Tauri process is *not* a membrane boundary and therefore bypasses Trust Channel logic.

---

## 1. Deployment Architecture

### 1.1 System Topology Overview
Each **Agent** in MAP operates within an **Agreement Space**—a membrane enclosing Agents that share at least one Agreement.  
Agents are depicted as spheres connected by a **mycelial web** of Trust Channels representing the live peer-to-peer fabric.

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

---

## 2. Core Concepts

### 2.1 Dance Capsule
A **Dance Capsule** is a holarchic structure of nested **Envelope** holons surrounding a `Dance` (request or response).  
Each envelope performs one membrane function: routing, authentication, encryption, authorization, dispatch, or filtering.  
Inbound sequence:  
`Transport → AuthN → Crypto → AuthZ → Dispatch → Payload`  
Outbound sequence:  
`Payload → Exfiltration → Crypto → AuthN → Transport`

Each layer exposes progressively unwrapped content to the next validation phase.

### 2.2 Agreement and ProtocolSuite
Each Trust Channel is governed by an **Agreement**, which specifies:
- Allowed **ProtocolSuites** (possible envelope sequences and crypto stacks).
- Mappings between Dances and suites via `DancePolicyMap`.
- Cryptographic and policy relationships (AuthZPolicy, CryptoPolicy, ExfiltrationPolicy, StepUpPolicy).

A **ProtocolSuite** holon defines:
- The ordered envelope sequences for inbound and outbound directions.
- The validator modules for each envelope kind.
- Optional `CanDownshiftTo` relationships for fallback negotiation.

### 2.3 Protocol Negotiation
Protocol negotiation determines which **ProtocolSuite** governs a given capsule exchange.  
It occurs when a sender proposes a suite under the governing Agreement and the receiver accepts or downshifts to another allowed suite.

**Negotiation Steps**
1. **Proposal** — Sender selects a candidate suite from the Agreement’s `DancePolicyMap` or its `DefaultSuite` and records it as `ProposesSuite` in the outer TransportEnvelope.
2. **Validation** — Receiver checks the Agreement’s `AllowedProtocolSuites`. If the proposal is not permitted, it selects a compatible suite from the sender’s `CanDownshiftTo` list.
3. **Response** — Receiver records the final choice as `AcceptedSuite` in the TransportEnvelope.
4. **Pinning** — The capsule pins `PinnedAgreement → Agreement` and `NegotiatedSuite → ProtocolSuite`.
5. **Verification** — Upon receipt, validators confirm that the capsule’s suite matches the pinned Agreement and any downshift path was explicitly allowed.

Example:
```
TransportEnvelope
 ├── ForAgreement → #agr:std
 ├── ProposesSuite → #suite:std-full
 └── AcceptedSuite → #suite:light-authz
```

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

---

## 7. Summary
The Trust Channel provides a **layered, Agreement-driven security framework** for all cross-Space communications.  
Each envelope serves a distinct purpose, from routing and authentication to encryption, authorization, dispatch, and outbound filtering.  
Protocol negotiation guarantees interoperability, while each validation gate enforces sovereignty and trust.  
This layered architecture transforms MAP’s peer-to-peer network into a **self-verifying, self-governing fabric** for secure inter-Space collaboration.