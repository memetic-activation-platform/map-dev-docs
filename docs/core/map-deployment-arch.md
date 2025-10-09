# Single Process Deployment Architecture

This diagram illustrates the deployment architecture for a MAP installation using a **single-process embedded Holochain Conductor** within a **Tauri container**. All application layers—TypeScript, Rust client, Holochain conductor, and WASM guests—run within a single operating system process, communicating via serialized JSON-RPC or internal Rust interfaces.



![MAP Deployment Arch -- single process -- v1.0.jpg](../media/MAP%20Deployment%20Arch%20--%20single%20process%20--%20v1.0.jpg)

---

## Conductora Tauri Container
The **Conductora Tauri Container** hosts all MAP client and guest components. It integrates:
- The **TypeScript client UI**, running in a WebView.
- The **Rust Holons Client**, which maintains state and executes local operations.
- The **Holochain Conductor**, which manages WASM guest execution and DHT integration.
- The embedded **WASM sandbox**, which runs guest zomes in isolated execution contexts.

---

## TypeScript Client
The **TypeScript client** provides the human-facing interface (HI). It communicates with the Rust client through a Tauri **JSON-RPC bridge**, sending dance requests and receiving responses. The TypeScript layer is stateless with respect to Holon data—it holds only _**references**_ to Holons managed by the Rust client.


## Rust Holons Client (Stateful, In-Memory)
The Rust Holons Client serves as the central coordination layer for all runtime activity within the MAP process. It maintains the **active working state** for holons in memory, handles dances invoked by the UI, and also initiates dance requests directed to the guest for execution and persistence.

- **Client Dancer** — Handles dance calls from the TypeScript client, routes them to the correct dancer, and returns response. Does NOT ping-pong transaction state.

- **Holons Core** — Exposes external-facing API, reference layer, space manager, caching, staging, transient holon management. Makes calls on HolonServiceApi to initiate context-specific actions. Contains no environment-specific dependencies and is reused identically by both client and guest contexts.

- **HolonServiceApi (Trait)** — Defines the abstract interface through which `holons_core` accesses environment-specific capabilities such as commit, retrieval, and validation. Both `ClientHolonService` and `GuestHolonService` implement this trait, allowing the core logic to remain environment-agnostic and preventing circular dependencies between crates.

- **ClientHolonService** — Implements `HolonServiceApi` for the client runtime. Acts as a **dance relay**, converting trait method calls from `holons_core` into serialized **dance requests** and forwarding them to the guest for execution through the Conductor. After receiving responses, it reconciles results with the client’s in-memory Cache and Nursery.

- **ClientDanceCall Service** — Bridges between the client and the embedded Conductor. Serializes dance capsules, invokes the Conductor’s API, and deserializes results returned from the guest. Since guest dances are stateless, the Client Dance Call Service ping-pongs transaction state between client and guest. Serializing staged holons from the Nursery and transient holons from the TransientHolonManager and attaching them to outbound dance requests and does the inverse upon response.

Through these components, the Rust Holons Client both **handles incoming dances from the UI** and **initiates outbound dances** to the guest for transactional processing and persistence.


---

## Rust Holons Guest (WASM Sandbox)
The **WASM sandbox** hosts the **Rust Holons Guest** runtime within the same process. Each guest call executes in isolation and terminates after completion.

- **Guest Dancer** — Handles dance calls from the Rust Holons Client or other Rust Holons Guests. Since guest dances are stateless, the Guest Dancer ping-pongs transaction state between caller and guest. For the inbound Dance Request, this means inflating its Nursery and Transient Holon Manager by de-serializing staged holons and transient holons from request's session state. It then routes dance calls to the correct _dancer_. When the _dancer_  returns, it constructs the Dance Response, serializes the transaction state from Nursery and Transient Holon Manager, attaches this session state to the Dance Response and returns control to the Conductor.

- **Holons Core** — Shared logic reused in the guest context. See _Rust Holons Client_ above for a description of the operations it offers. In the guest, it only operates only on the state provided in the current invocation, but this difference is encapsulated by the Guest Dancer. 

- **Guest Holon Service** — The guest implementation of `HolonServiceApi`. Performs the **heavy-lifting** for holon operations, including validation, persistence to the DHT, and cross-cell interactions. Executes all commit logic and applies schema rules and capability checks enforced by the MAP and Holochain security models.

- **Guest Dance Call Service** — Allows the Rust Holons Guest to initiate dance requests to other guests (i.e., to other spaces). Serializes dance capsules, invokes the Conductor’s API, and deserializes results returned from the guest. Since guest dances are stateless, the Guest Dance Call Service ping-pongs transaction state between client and guest. Serializing staged holons from the Nursery and transient holons from the TransientHolonManager and attaching them to outbound dance requests and does the inverse upon response.

- **Persistence Layer** — Performs durable writes to the Holochain DHT via host functions and validation callbacks.

---

## Holochain Conductor Integration
The embedded **Holochain Conductor** mediates all calls between the Rust Holons Client and the WASM guests.

- The **Dance Call Services** (in both Client and Guest) invoke Conductor APIs directly (no sockets or separate processes).
- The **Conductor** either spins up the **WASM guest runtime** for each zome call and passes serialized envelopes or forwards the request to a different Conductor. 
- After processing, results are returned to the client and reconciled with its local state.
- The Conductor manages the local DHT node and connects via **WebRTC** to other Conductors for distributed storage and validation.

---

## Cross-Component Flow
1. **TypeScript Client** builds a Dance Request and sends it via a JSON-RPC request to the **Rust Holons Client**.
2. **Client Dancer** receives the Dance Request from the TypeScript client and routes it to the appropriate handler for that dance.
3. The dancers uses **Holons Core** API (imported via its prelude) to create, update, and access transient and staged holons. 
3. If the Holons Core needs Holon Service's it obtains the context-specific Holon Service and invokes the desired service.
4. The Client Holon Service delegates the call the guest but building a Dance Request and then using the **ClientDanceCall Service** to forward the dance request to the embedded **Conductor**.
4. The Conductor executes the request in a **WASM Guest**, which processes it through the **Guest Dancer** who inflates Nursery and Transient Holon Manager from transaction state passed on the request and then dispatches the appropriate dancer.
5. The dancer uses Holon Core functions which, in turn, may invoke **Guest Holon Services** via trait methods.
6. **Guest Holon Services** invokes services on the **Persistence Layer** to read/write locally saved holons to the DHT. If it needs to access dances offered by other spaces, it uses the **Guest Dance Call Service**.
5. Results return through the same path, with the Guest Dancer serializing the transaction state and attaching it to the response.
6. If required, the Conductor propagates DHT operations via **WebRTC** to peer Conductors.

---

## Summary
This architecture consolidates all runtime components—UI, client, conductor, and guest—into a single process for efficient local operation. The **Rust Holons Client** maintains all transient and staged state and handles dance orchestration, while the **Rust Holons Guest** performs validated, persistent commits to the Holochain DHT. The embedded **Conductor** provides the boundary between these layers, enforcing isolation, capability rules, and DHT persistence, while the TypeScript interface remains lightweight and stateless.