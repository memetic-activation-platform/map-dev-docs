# MAP Security Model — Technical Specification (Modern Structure)

**Version:** 1.0  
**Status:** Draft  
**Audience:** MAP Core Developers, Security Architects, Holochain Integration Engineers  
**Last Updated:** October 2025

---

## 1. Overview

### 1.1 Purpose
This document specifies the **security architecture and operational controls** of the Memetic Activation Platform (MAP).  
It defines the trust foundations, threat mitigations, and adaptive enforcement mechanisms that ensure **data sovereignty, agent integrity, and membrane-level trust** across the platform.

### 1.2 Scope
The specification applies to all MAP runtimes (client, host, and interspace) and covers:
- **Identity and key management**
- **Authentication, authorization, and accountability**
- **Membrane security and Trust Channels**
- **Adaptive risk and behavioral enforcement**
- **Space lensing and contextual visibility**
- **Governance and data exfiltration controls**
- **Operational resilience and resource protection**

### 1.3 Guiding Principles
- **Sovereignty by Design:** Each Agent owns its identity, keys, and data.
- **Defense in Depth:** Security enforced at device, membrane, and agreement layers.
- **Contextual Enforcement:** Risk, sensitivity, and lens determine protection level.
- **Zero Central Trust:** No MAP component requires global or third-party trust.
- **Transparency and Traceability:** Every security decision is auditable and policy-driven.

---

## 2. System Architecture

### 2.1 Core Security Domains
| Domain              | Description                                                       | Enforcement Mechanism                        |
|---------------------|-------------------------------------------------------------------|----------------------------------------------|
| **Agent Identity**  | Cryptographically unique entities (one per device).               | Holochain keypairs managed by Lair keystore. |
| **Space Membranes** | Sovereign boundaries governing holon data and execution.          | Trust Channels and Agreement policies.       |
| **Agreements**      | Policy layer defining roles, protocols, and data rights.          | AuthZPolicy, CryptoPolicy, StepUpPolicy.     |
| **Trust Channels**  | Secure communication conduits between Spaces.                     | Multi-envelope capsule architecture.         |
| **Risk Layer**      | Adaptive defense system analyzing behavioral and contextual data. | RiskPolicy + StepUpPolicy enforcement.       |
| **Lens Layer**      | Contextual visibility management within Spaces.                   | ActiveSpace + AsSelfEnvelope.                |

### 2.2 Layered Architecture Diagram
```
Device Layer  →  Agent Layer  →  Space Membrane Layer  →  Agreement Layer
      ↕                  ↕                        ↕                       ↕
Local Authentication   Key Custody          Trust Channel Validation   Policy & Risk Control
```

---

## 3. Identity and Key Management

### 3.1 Agent Keys
Each device acts as an **Agent** with a unique cryptographic keypair:
- Keys are stored in **Lair Keystore** (Holochain secure enclave).
- Public keys are registered with relevant **Agreements**.
- Keys never leave the device; signing and decryption happen in-process only.

### 3.2 Key Lifecycle
| Phase           | Action                                             | Enforcement                     |
|-----------------|----------------------------------------------------|---------------------------------|
| **Creation**    | Device generates new keypair via Lair.             | Requires local OS unlock.       |
| **Association** | Key registered to user’s I-Space.                  | Cryptographically signed claim. |
| **Revocation**  | Compromised keys revoked by user or I-Space admin. | Propagated via DHT gossip.      |
| **Rotation**    | New keypair replaces revoked key.                  | Updates signed linkage chain.   |

### 3.3 Optional Key Splitting
For critical data, MAP supports XOR or threshold-based key partitioning.  
Each fragment is stored across separate devices or vaults, requiring quorum reconstruction.

---

## 4. Authentication and Authorization

### 4.1 Authentication Sources
- **Device Trust:** Biometric/PIN unlocks the operating system.
- **Agent Trust:** Lair keystore confirms agent keypair control.
- **Space Trust:** Agreement-based verification within the Space membrane.
- **Step-Up Trust:** Secondary verification for sensitive Dances (SFS session).

### 4.2 Authorization Model
Authorization follows a **role → scope → policy** chain:
1. The active **Agreement** defines permissible roles.
2. Roles map to **AuthZPolicy** objects specifying allowed Dances and data scopes.
3. The **Space membrane** enforces these via the Trust Channel’s AuthZEnvelope.

### 4.3 Permission Types
| Permission Type | Description                                    | Example Enforcement                    |
|-----------------|------------------------------------------------|----------------------------------------|
| **Read**        | Retrieve data within allowed visibility scope. | Lens filtering via ExfiltrationPolicy. |
| **Write**       | Modify or propose changes to Space data.       | AuthZEnvelope validation.              |
| **Execute**     | Trigger a Dance or system action.              | DispatchEnvelope routing.              |
| **Exfiltrate**  | Send data beyond membrane.                     | Outbound ExfiltrationEnvelope.         |

---

## 5. Trust Channels and Membrane Security

### 5.1 Purpose
Trust Channels provide the **secure envelope architecture** that protects all cross-Space Dances.  
Each message is encapsulated in a **Dance Capsule** comprising sequential validation layers:
`Transport → AuthN → Crypto → AuthZ → Dispatch → Payload (→ Exfiltration)`

### 5.2 Enforcement Objectives
- Guarantee message authenticity and origin.
- Prevent unauthorized decryption or replay.
- Enforce Agreement policies cryptographically.
- Maintain auditability of all exchanges.

### 5.3 Key Functions
| Envelope         | Function                                          | Validation Output              |
|------------------|---------------------------------------------------|--------------------------------|
| **Transport**    | Routing, Agreement pinning, protocol negotiation. | Confirmed target membrane.     |
| **AuthN**        | Verify sender’s signature.                        | Proven identity and integrity. |
| **Crypto**       | Decrypt payload.                                  | Confidentiality enforced.      |
| **AuthZ**        | Check sender’s role and permissions.              | Scoped authorization granted.  |
| **Dispatch**     | Deliver payload to local I-Space.                 | Safe local execution.          |
| **Exfiltration** | Filter outbound data.                             | Controlled data exposure.      |

### 5.4 Protocol Negotiation
When Spaces exchange data, they negotiate which **ProtocolSuite** to use:
1. Sender proposes a suite from the Agreement’s `DancePolicyMap`.
2. Receiver validates or downshifts to a compatible suite.
3. The final choice is **pinned** in the capsule (`NegotiatedSuite`).
4. Both sides verify suite compatibility and envelope sequence integrity.

---

## 6. Risk Enforcement Framework

### 6.1 Overview
The **Risk Enforcement Framework** introduces adaptive, behavior-driven protection.  
It monitors usage patterns and dynamically enforces **step-up authentication** or throttling when contextual risk increases.

### 6.2 Core Components

**RiskPolicy Holon**
```
RiskPolicy
 ├── ConsumesTelemetry → [RiskEventType...]
 ├── UsesStepUpPolicy → StepUpPolicy
 └── MapsSensitivityToThresholds → [SensitivityThresholdMap...]
```

**StepUpPolicy**
- Defines acceptable second-factor methods (biometric, PIN, hardware key).
- Establishes TTL, idle timeout, and re-verification frequency.

### 6.3 Sensitivity and Scoring
Each DanceDescriptor defines a sensitivity tier:
| Tier | Description | Typical Enforcement |
|------|--------------|---------------------|
| **None** | Low risk | No step-up required |
| **Elevated** | Confidential | Require active SFS |
| **Critical** | Governance or high value | Always require step-up |

A **Risk Engine** aggregates telemetry (e.g., failed auth, anomalies, location shifts) into a dynamic risk score.  
If score ≥ threshold or sensitivity = Critical → the capsule builder inserts an `UnlockEnvelope`.

### 6.4 Behavioral Monitoring
The Risk Engine collects and evaluates:
- Frequency and velocity of actions.
- Deviations from normal temporal patterns.
- Device or network changes.
- Recent revocations or policy breaches.

Triggered responses:
- Insert `UnlockEnvelope` before next Dance.
- Suspend session or throttle request rate.
- Emit `RiskPolicyViolation` for audit and governance action.

### 6.5 Developer Integration
- Step-up enforcement occurs client-side (Tauri layer).
- Applications must query risk state and prompt user for confirmation if required.
- Telemetry events should be submitted for ongoing learning.

---

## 7. Space Lens and Access Semantics

### 7.1 Concept
MAP introduces **Space lenses** to define the contextual visibility of data.  
At any time, an Agent operates within one **ActiveSpace** that determines which holons they can see, modify, or invoke.

### 7.2 ActiveSpace
- A single Space context is active per user session.
- Switching ActiveSpace updates the active Agreement set and available Trust Channels.
- Cached views and permissions are lens-bound—switching lenses resets them.

### 7.3 Lens Filtering
- The membrane automatically filters holon visibility.
- External holons are visible only through Agreement-approved projections.
- ExfiltrationPolicy determines which properties or relationships can be seen.
- Filtered results are cached per proxy for low-latency reuse.

### 7.4 Acting As vs. Accessing Through
| Mode                  | Description                                                  | Trust Source                              |
|-----------------------|--------------------------------------------------------------|-------------------------------------------|
| **Acting As**         | Changing ActiveSpace, adopting that Space’s governance role. | New Space’s Agreement.                    |
| **Accessing Through** | Remaining in I-Space but querying remote data.               | Cross-Space Agreement and outbound proxy. |

### 7.5 AsSelfEnvelope
For scenarios where an agent temporarily acts as themselves while within another Space:
```
AsSelfEnvelope
 ├── SubjectAgent → Agent
 ├── AuthenticatedIn → SourceSpace
 └── VerifiedBy → Agreement
```
This explicitly asserts the user’s I-Space identity.  
Validation ensures only permitted personal data is accessible and filters are applied per Agreement.

### 7.6 UX and Developer Considerations
- Interfaces must clearly show the current lens.
- Switching lenses must re-evaluate role, Agreement, and risk context.
- Caches should isolate per ActiveSpace to avoid privilege bleed-through.

---

## 8. Data Protection and Exfiltration

### 8.1 ExfiltrationPolicy
Controls outbound data leaving a Space:
- Whitelists permitted fields and relationships.
- Defines quantitative thresholds (record count, payload size).
- Redacts or aggregates sensitive attributes.

### 8.2 Enforcement
Implemented via the **ExfiltrationEnvelope** in the Trust Channel.  
Validated before encryption to ensure no sensitive data leaves the membrane.

### 8.3 Audit and Provenance
All exfiltrations are logged as signed `ExfiltrationEvents`, storing:
- Policy tag used
- Payload digest
- Destination Space and Agreement
- Timestamp and responsible Agent ID

---

## 9. Operational Security and Resilience

### 9.1 Immutable State Model
All persisted holons are immutable; updates create new versions.  
This eliminates state tampering and ensures full provenance.

### 9.2 Sustainer Role
The **Sustainer** monitors device and Space resources (memory, compute, bandwidth).  
When thresholds approach limits, it can:
- Prune caches.
- Slow gossip replication.
- Temporarily halt new inbound capsules.

This makes **resource sustainability** a security function preventing denial-of-service conditions.

### 9.3 Audit Logging and Observability
- Every validation gate in the Trust Channel emits a signed audit event.
- Events are recorded in append-only DHT logs.
- Audit holons are queryable by Agreement participants for forensic review.

---

## 10. Threat Model

| Threat                    | Vector                          | Primary Mitigation                       | Secondary Mitigation                              |
|---------------------------|---------------------------------|------------------------------------------|---------------------------------------------------|
| **Device Theft**          | Lost or stolen device           | Revoke key, data encrypted at rest       | Step-up gating, key rotation                      |
| **Man-in-the-Middle**     | Network interception            | Capsule encryption, signature validation | Protocol negotiation ensuring suite compatibility |
| **Privilege Escalation**  | Role misuse                     | AuthZPolicy, lens filtering              | Step-up enforcement                               |
| **Data Leakage**          | Improper exfiltration           | ExfiltrationPolicy & Envelope            | Space lens boundaries                             |
| **Replay Attack**         | Capsule reuse                   | Nonces, timestamps, hash chains          | Agreement nonce validation                        |
| **Behavioral Compromise** | Account hijacking or automation | Risk Engine monitoring                   | Dynamic throttling                                |
| **Resource Exhaustion**   | Memory/compute flood            | Sustainer thresholds                     | Load shedding                                     |

---

## 11. Compliance and Auditability

### 11.1 Policy Provenance
All policies (AuthZ, Crypto, Exfiltration, Risk) are **holons**—self-describing, versioned, and signed.  
This ensures every enforcement event can be traced back to a verifiable descriptor.

### 11.2 Audit Trails
- Trust Channel emits **ValidationEvents** with timestamps, suite IDs, and results.
- Audit holons are queryable per Agreement.
- For privacy, sensitive payloads are hashed before storage.

### 11.3 Policy Amendments
Changes to security policies require Agreement version increments.  
All previous versions remain immutable for historic verification.

---

## 12. Summary

### 12.1 Key Properties
| Principle                 | Outcome                                                      |
|---------------------------|--------------------------------------------------------------|
| **Sovereignty by Design** | Agents control their keys, data, and Agreements.             |
| **Defense in Depth**      | Device, membrane, and agreement layers reinforce each other. |
| **Adaptive Security**     | Step-up and risk scoring adjust authentication dynamically.  |
| **Contextual Visibility** | Space lenses define what is visible or actionable.           |
| **Auditability**          | Every envelope validation and policy decision is recorded.   |
| **Resilience**            | Sustainer maintains secure operation under load.             |

### 12.2 Conclusion
The MAP Security Model is a **self-governing, adaptive security architecture** where sovereignty, trust, and resilience are not bolted on but **emerge from the system’s holonic structure**.  
By merging Trust Channels, contextual lenses, and behavioral risk intelligence, MAP creates a **living trust fabric**—a network where all participants interact securely, transparently, and autonomously.