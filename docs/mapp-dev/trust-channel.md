# 🩰 We-Space Trust Channels in Action
### How MAP Enforces Sovereignty, Privacy, and Agreement Integrity

This document uses the **life-cycle of a DanceRequest** to illustrate a deeper story:  
how the **We-Space application layer** and **Trust Channel services** in MAP protect data sovereignty and enforce agreements in a fully decentralized architecture.

---

## 🎯 Why This Matters

The **primary goals** of the We-Space and its Trust Channels are:

1. **Sovereignty and Privacy Without Central Servers**  
   MAP Agents never need to trust a central authority with their data. All routing, validation, and exchange happens **peer-to-peer**, with **no central custody** of private information.

2. **Infrastructure-Level Security and Governance Enforcement**  
   Authentication, authorization, cryptographic security, and privacy enforcement are **built into MAP’s infrastructure layer**. This means application developers:
  - Don’t have to implement security protocols themselves
  - Can rely on consistent adherence to the signed promises in Agreements
  - Work with validated, decrypted, role-checked requests — already safe to act upon

By handling these steps *before* a request reaches an application’s logic, the MAP ensures **consistency, trust, and interoperability** across the entire ecosystem.

---

## 📥 Inbound Flow: Envelopes and Membrane Functions

Every inbound DanceRequest travels through the We-Space membrane in a **layered sequence of envelopes**.  
Each envelope **contains the information** needed for the **membrane function** at that stage.  
The envelopes do not “do” the work themselves — the **Trust Channel functions** act on the envelope’s contents.

---

### 1. **Transport Envelope** → *Routing Function*
**Envelope contains:**
- `agreement_id` — identifies governing Agreement
- `sender_id` — request originator
- `recipient_id` — intended receiver
- `message_type = DanceRequest`

**Function performed:**  
The **We-Space messaging infrastructure** reads this metadata to select the allowed protocol (per Agreement) and route the message to the recipient’s membrane — without exposing any payload contents.

---

### 2. **Authentication Envelope** → *Identity Verification Function*
**Envelope contains:**
- Cryptographic signature over the hash of the encrypted payload

**Function performed:**  
The Trust Channel fetches the sender’s public key from the Agreement and verifies:
- The signature matches the payload hash
- The sender is an authorized Agreement participant

This step **proves authenticity** before any decryption occurs.

---

### 3. **Encryption Envelope** → *Confidentiality Function*
**Envelope contains:**
- Payload encrypted with the recipient’s public key

**Function performed:**  
The recipient’s membrane decrypts the payload with its private key.  
This ensures that even though transport and routing may cross multiple peers, only the final recipient can read the request.

---

### 4. **Authorization Envelope** → *Permission Check Function*
**Envelope contains:**
- Full `DanceRequest`
- Target `Dance`
- Agent roles
- Parameters, thresholds, and timing

**Function performed:**  
Agreement rules are applied to ensure:
- The requester’s role is permitted to invoke this Dance
- The role pairing is valid under the Agreement
- All scope and timing conditions are met

---

### 5. **Execution Context** → *Dispatch Function*
**Function performed:**  
Once validated, the We-Space hands the request to the recipient’s I-Space.  
Here, the MAP Choreographer invokes the Dance.  
If part of a DanceFlow, subsequent steps are dispatched automatically.

---

## 📤 Outbound Flow: Layering the Response

Outbound processing mirrors inbound, ensuring the response **leaves** the membrane as securely and intentionally as the request **entered**.

---

### 1. **Payload** → *Creation Function*
The application logic in the I-Space generates the raw `DanceResponse`.

---

### 2. **Exfiltration Envelope** → *Outbound Authorization Function*
**Function performed:**  
Filters response content against Agreement terms, type-level access policies, and trust thresholds before anything leaves the membrane.

---

### 3. **Encryption Envelope** → *Confidentiality Function*
Response is encrypted with the requester’s public key so only they can read it.

---

### 4. **Authentication Envelope** → *Integrity Verification Function*
Encrypted response is signed with the responder’s private key to prove origin and integrity.

---

### 5. **Transport Envelope** → *Routing Function*
Routing metadata is wrapped around the response and the Trust Channel selects the allowed protocol for delivery.

---

## 🧠 Why This is a Big Deal for Developers

Because the **We-Space application services and Trust Channel stack** do all of this *before* a request reaches app logic, developers can:
- Assume incoming requests are **authentic, authorized, and within scope**
- Skip building custom cryptographic or trust enforcement layers
- Focus entirely on the **business logic of the Dance** itself

At the same time, the MAP ensures **uniform adherence to Agreements**, so every response is also vetted, encrypted, and signed before leaving the agent’s control.

---

**In short:**  
The We-Space and Trust Channels are **sovereignty-preserving service layers**.  
They are the reason MAP can operate fully decentralized **without central servers** — and why MAP apps can remain secure, interoperable, and trust-aligned by default.