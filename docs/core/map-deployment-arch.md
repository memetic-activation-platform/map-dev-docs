# Single Process Deployment Architecture

This diagram illustrates the deployment architecture for a MAP installation using a **single-process embedded Holochain Conductor** within a **Tauri container**. All application layers—TypeScript, Rust client, Holochain conductor, and WASM guests—run within a single operating system process, communicating via serialized JSON-RPC or internal Rust interfaces.


![MAP Deployment Arch.jpg](../media/MAP%20Deployment%20Arch.jpg)


---

## Conductora Tauri Container
The **Conductora Tauri Container** hosts all MAP client and guest components. It integrates:
- The **TypeScript client UI**, running in a WebView.
- The **Rust Holons Client**, which maintains state and executes local operations.
- The **Holochain Conductor**, which manages WASM guest execution and DHT integration.
- The embedded **WASM sandbox**, which runs guest zomes in isolated execution contexts.

---

---

## TypeScript Client
The **TypeScript client** provides the human-facing interface (HI). It communicates with the Rust client through a Tauri **JSON-RPC bridge**, sending dance requests and receiving responses. The TypeScript layer is stateless with respect to Holon data—it holds only references to Holons managed by the Rust client.


## Rust Holons Client (Stateful, In-Memory)
The Rust Holons Client serves as the central coordination layer for all runtime activity within the MAP process. It maintains the **active working state** for holons in memory, handles dances invoked by the UI, and also initiates dance requests directed to the guest for execution and persistence.

- **Holons Core** — Shared logic for caching, staging, transient holon management, and orchestration of commits. Contains no environment-specific dependencies and is reused identically by both client and guest contexts.

- **HolonServiceApi (Trait)** — Defines the abstract interface through which `holons_core` accesses environment-specific capabilities such as commit, retrieval, and validation. Both `ClientHolonService` and `GuestHolonService` implement this trait, allowing the core logic to remain environment-agnostic and preventing circular dependencies between crates.

- **ClientHolonService** — Implements `HolonServiceApi` for the client runtime.  
  Acts as a **dance relay**, converting trait method calls from `holons_core` into serialized **dance requests** and forwarding them to the guest for execution through the Conductor. After receiving responses, it reconciles results with the client’s in-memory Cache and Nursery.

- **DanceAPI / Client Dancer** — Provides high-level functions for initiating, handling, and dispatching dances. Processes dance requests from the TypeScript Client and coordinates their routing to the correct handlers within the Rust client. or to the guest.

- **ClientDanceCall Service** — Bridges between the client and the embedded Conductor.  
  Serializes dance capsules, invokes the Conductor’s API, and deserializes results returned from the guest.

Through these components, the Rust Holons Client both **handles incoming dances from the UI** and **initiates outbound dances** to the guest for transactional processing and persistence.


---

## WASM Sandbox (Rust Holons Guest)
The **WASM sandbox** hosts the **Rust Holons Guest** runtime within the same process. Each guest call executes in isolation and terminates after completion.

- **Holons Core** — Shared logic reused in the guest context, operating only on the state provided in the current invocation.

- **GuestHolonService** — The guest implementation of `HolonServiceApi`. Performs the **heavy-lifting** for holon operations, including validation, persistence to the DHT, and cross-cell interactions. Executes all commit logic and applies schema rules and capability checks enforced by the MAP and Holochain security models.

- **DanceAPI / DanceCaller API** — Defines the guest-side interfaces for receiving, dispatching, and responding to dance requests.

- **Dances Guest** — The dispatcher that routes inbound dance capsules to the appropriate guest handlers.

- **Persistence Layer** — Performs durable writes to the Holochain DHT via host functions and validation callbacks.

---

## Holochain Conductor Integration
The embedded **Holochain Conductor** mediates all calls between the Rust Holons Client and the WASM guests.

- The **ClientDanceCall Service** invokes Conductor APIs directly (no sockets or separate processes).
- The **Conductor** spins up the **WASM guest runtime** for each zome call and passes serialized envelopes.
- After processing, results are returned to the client and reconciled with its local state.
- The Conductor manages the local DHT node and connects via **WebRTC** to other Conductors for distributed storage and validation.

---

## Cross-Component Flow
1. **TypeScript Client** sends a JSON-RPC request to the **Rust Holons Client**.
2. **Client Dancer** builds a Dance capsule containing all staged and transient Holon state.
3. Capsule is sent via the **ClientDanceCall Service** to the embedded **Conductor**.
4. The Conductor executes the request in a **WASM Guest**, which processes it through the **Guest Holon Service** and **Persistence Layer**.
5. Results return through the same path, updating the client’s Nursery and Cache.
6. If required, the Conductor propagates DHT operations via **WebRTC** to peer Conductors.

---

## Summary
This architecture consolidates all runtime components—UI, client, conductor, and guest—into a single process for efficient local operation.  
The **Rust Holons Client** maintains state and user interaction logic, while the **Rust Holons Guest** executes all stateless transactional commits within the Holochain sandbox.  
The embedded **Conductor** provides the boundary between these layers, enforcing isolation, capability rules, and DHT persistence, while the TypeScript interface remains lightweight and stateless.