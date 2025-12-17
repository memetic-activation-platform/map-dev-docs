# Trust Channel Entry-Point Architecture
### Summary of the Discussion, Reasoning, and Final Design Rules

## 1. Background: Why Trust Channel Routing Matters

The Trust Channel is the canonical path for **DanceRequest → DanceResponse** interactions.  
It applies envelope logic such as:

- Attaching / hydrating SessionState
- Adding cryptographic proofs
- Managing identity delegation
- Tracking request lineage
- Ensuring cross-space integrity of requests and responses

The open design question was:

> **Where should a DanceRequest *enter* the Trust Channel?  
> From the guest (WASM) or the client (native/Tauri)?**

The answer depends on which runtime is actually responsible for transmitting a particular Dance.

---

## 2. Key Insight: Only Holochain-Carried Dances Can Originate from the Guest

We established the foundational constraint:

### ✔ *Fact:*
**Holons in one Holochain space can only talk to holons in another space through the Holochain conductor.**

A guest zome call can trigger:

- `call` → local zome
- `call_remote` → remote agent, same DNA
- `emit_signal`
- Link traversal
- Validation callbacks

But NOT:

- HTTP
- WebSockets
- Local filesystem
- OS-level processes
- Local TCP/IPC
- Native embedding
- Tauri commands
- Database access
- Other Holochain DNAs on the same machine

### ⇒ Therefore:

> **Any Dance that uses one of the above non-Holochain transports can never originate from the guest.**  
It MUST originate from the native runtime (the client).

This is *the* architectural pivot point.

---

## 3. What This Means for “Trust Channel Entry Point”

A single Trust Channel implementation can *serve two environments*:

### **A. Guest → Holochain → Guest**
Used for:
- Zome → Zome coordination
- Calls between holons in the same DNA
- Calls between spaces in *the same conductor instance*

### **B. Client → Conductor → Guest**
Used for:
- The Tauri application
- Node.js / CLI clients
- Any non-holochain-originating request

But these two entry-points are different.

### **Guest entry-point constraints**
- Must be `wasm32-unknown-unknown` safe
- `async_trait(?Send)` required
- No tokio or threads
- No reactor, no filesystem
- No networking directly
- Requests must be sent via the conductor only
- Only valid for Holochain-backed Dances

### **Client entry-point constraints**
- Full async runtime
- Tokio available
- Can perform HTTP/WebSockets/FS/database
- Can call into the Holochain interface
- Can initiate non-Holochain Dances (e.g., for cloud, external services)

---

## 4. Why We Cannot Send “External Origin” Requests Through the Guest

One major conclusion from the discussion:

### ❌ A DanceRequest from the outside world cannot go:
**external → client → guest → conductor → guest**

Because:

1. The guest can't open external connections
2. The guest can only call back into the conductor or its own host agent
3. Routing external requests into guest first creates a circular trust dependency
4. The guest does NOT have access to:
    - external URLs
    - native OS
    - plugin permissions
    - local storage
    - local key stores

### ⇒ All non-Holochain Dances must enter *via the client side Trust Channel*.

---

## 5. The Reverse: Why Holochain-Carried Dances Should Start in the Guest

When the *initiating agent is a holon inside the same DNA*, routing the request up to the client first is:

- unnecessary
- slower
- less secure
- adds async complexity
- requires cross-boundary serde
- breaks locality of reference

Since the conductor can directly service the request:

### ✔ Correct path:
guest → TrustChannel → conductor → remote/other-cell → guest

---

## 6. Unifying the Two Pathways

Although the *entry point* differs, the **Trust Channel semantics must not**.

This was a major point of consensus:

### ✔ The Trust Channel encapsulation rules must be identical:
- session envelope
- identity envelope
- signatures
- request lineage
- consistency checks
- response hydration

Regardless of whether the message starts in:

- WASM
- Tauri
- Node
- Native Rust
- A mock test harness

---

## 7. The Final Design Rule (most important output)

We derived a crystal-clear rule:

---

### **🔥 Trust Channel Entry-Point Rule**

> **If the transport is Holochain, the Trust Channel entry point is the guest.
>
> If the transport is anything else, the Trust Channel entry point is the client.**

---

This rule avoids:
- awkward guest→client→guest routing
- unsafe invocation of external requests from WASM
- unnecessary cross-boundary serialization
- leaking Send/Sync requirements into WASM
- tight coupling between UI and guest code

While ensuring:
- unified envelope logic
- identical semantics regardless of environment
- consistent Dance orchestration
- evolvable multi-runtime API

---

## 8. How This Informs the 337 → 345 POC

This insight has major implications for the POC:

### ✔ TrustChannel must compile under WASM **and** Native
→ but with different entry-points.

### ✔ holons_client must remain client-only
→ DanceInitiator implementations for Tauri/Node live here.

### ✔ guest uses a WASM-safe DanceInitiator backend
→ typically the Holochain conductor.

### ✔ Shared logic (envelopes, state, protocol) lives in holons_core + holons_trust_channel
→ platform agnostic.

### ❌ Shared Receptor types should NOT leak into guest or core
→ they belong on the client side only.

This insight explains several errors we hit during the POC:  
holons_client being accidentally pulled into guest or core breaks WASM, contradicts this rule.

---

# End of Summary