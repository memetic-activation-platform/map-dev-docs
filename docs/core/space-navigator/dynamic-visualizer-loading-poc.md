# DAHN Dynamic Visualizer Loading — Design and POC Specification

## Status

UNREVIEWED DRAFT -- Proposed architecture and proof-of-concept specification.

## Purpose

DAHN must support visualizers that are not known when DAHN itself is compiled.

The set of useful visualizers is inherently open-ended. New visualizers may be contributed over time for:

- Value Types
- Properties
- Holons / nodes
- Relationships
- Collections
- Graphs
- Actions
- Canvases
- other future visualization kinds

This means DAHN cannot rely exclusively on visualizers compiled into its TypeScript frontend bundle.

At the same time, dynamic visualizer loading in DAHN is not merely a conventional browser dynamic-module-loading problem. The architecture must preserve MAP-specific properties around:

- visualizer selection
- provenance
- immutable executable identity
- stewardship
- runtime trust
- protocol compatibility
- eventual federation and distribution

The immediate objective is to establish an architecture and POC that proves the critical execution path without prematurely solving the complete federated artifact-distribution problem.

---

# 1. Architectural Context

## 1.1 Relationship to dynamically loaded Dance implementations

The dynamic visualizer problem is closely related to the previously established architecture for dynamically loaded Dance implementations.

For dynamically supplied Dances, the intended model is approximately:

- Dance implementations may be supplied as WASM artifacts.
- WASM can execute within isolated WASM sandboxes.
- An executable artifact can be content-addressed by digest.
- The artifact can be cryptographically signed by a MAP agent.
- MAP metadata can establish who stewards and attests to the implementation.
- The executable artifact can therefore receive strong guarantees around:
    - integrity
    - provenance
    - immutability
    - attribution
    - authentication of the publishing/stewarding agent

The physical bytes need not necessarily be stored directly in MAP data.

Instead, MAP can steward the semantic identity, provenance, versioning, signatures, applicability, and available retrieval locations of an executable artifact while the bulk executable content is stored elsewhere.

Dynamic visualizers should adopt the same general architectural model where possible.

However, visualizers introduce an additional execution-boundary concern:

> Dance WASM executes within a WASM runtime, while visualizer JavaScript ultimately has to become executable UI code inside the DAHN WebView.

That difference affects how verified executable artifacts are materialized and constrained.

---

# 2. Core Architectural Principle

A visualizer should not be conceptualized as merely a JavaScript or TypeScript module that DAHN happens to download.

Instead:

> A visualizer is a MAP-governed executable artifact. Rust determines which visualizer implementation is authorized for a particular visualization request, and the DAHN runtime securely materializes that implementation into the frontend execution environment.

This distinction preserves the MAP architecture instead of delegating visualizer discovery and authority to conventional frontend module resolution.

---

# 3. Required Separation of Concerns

Dynamic visualization should be decomposed into four distinct operations.

## 3.1 Selection

Determine which visualizer should be used for:

- the MAP object being visualized
- the visualization kind
- the current context
- the current human agent

Selection may consider:

- MAP type
- Value Type
- Holon Type
- visualization kind
- contextual suitability
- individual preferences
- collective or crowd-derived preferences
- prior behavior
- available visualizers
- compatibility
- trust or stewardship policy

This logic belongs exclusively in Rust.

The TypeScript layer must not contain an independent visualizer-selection mechanism.

---

## 3.2 Resolution

Once a visualizer has been selected, determine the immutable executable implementation corresponding to that visualizer and version.

Resolution establishes things such as:

- Visualizer identity
- Visualizer version
- implementation artifact identity
- artifact format
- digest
- protocol version
- entry point
- signer/steward
- signatures or attestations
- potential artifact locations

Resolution should also remain under Rust control.

---

## 3.3 Acquisition and Verification

Acquire the executable bytes and determine that they are exactly the artifact that was selected.

Eventually this may include:

- retrieving from local cache
- retrieving from a MAP artifact service
- retrieving from a steward's service
- retrieving from a mirror
- retrieving over HTTPS
- retrieving through a content-addressed network
- retrieving through some future MAP-native transport

Verification should establish at minimum:

- content digest matches the selected artifact

Eventually it should additionally establish:

- signature validity
- signing-agent identity
- relevant stewardship or trust policy
- protocol compatibility
- artifact format compatibility

This operation should also remain substantially under Rust control.

---

## 3.4 Instantiation

Only after the implementation has been selected, resolved, acquired, and verified should it become executable frontend code.

The TypeScript/WebView layer is responsible for:

- loading the verified implementation
- checking its runtime visualizer protocol contract
- instantiating it
- supplying its constrained runtime context
- rendering it

This is the portion of the process that intrinsically belongs in the frontend runtime.

---

# 4. Architectural Boundary

The intended flow is:

    Holon + visualization context + human agent
                    |
                    v
        Rust Visualizer Selector
                    |
                    | selected Visualizer
                    v
        Rust Artifact Resolver
                    |
                    | immutable implementation identity
                    v
        Artifact Acquisition
                    |
                    v
        Digest / signature verification
                    |
                    v
        Immutable local cache
                    |
                    v
        DAHN-controlled local artifact URL
                    |
                    v
        TypeScript Visualizer Loader
                    |
                    v
        Protocol validation
                    |
                    v
        Visualizer instantiation
                    |
                    v
             Live Visualizer

The critical architectural rule is:

> TypeScript instantiates a visualizer. It does not independently decide which visualizer should exist.

---

# 5. Rust Remains the Single Visualizer-Selection Authority

DAHN already places visualizer selection in the Rust layer.

That property should be preserved.

The Rust selector can consider substantially richer context than a conventional frontend component resolver, including:

- object MAP type
- visualization kind
- individual personalization
- collective preferences
- historical selection outcomes
- contextual relevance
- extensions installed or trusted by the agent
- future selector-function intelligence

This supports all visualizer classes uniformly.

For example, the same selector architecture should eventually select among:

- Value Visualizers
- Property Visualizers
- Node Visualizers
- Collection Visualizers
- Relationship Visualizers
- Graph Visualizers
- Action Visualizers
- Canvas Visualizers

Dynamic loading must therefore not introduce a second selector in TypeScript.

In particular, the frontend should not maintain mappings such as:

    HolonType -> Visualizer

nor should it independently determine:

    Visualizer -> implementation artifact

Those decisions belong to Rust.

---

# 6. Visualizer Identity Must Be Independent of Artifact Location

A Visualizer implementation should not be identified conceptually by a URL.

For example, this should not be the durable architecture:

    visualizer implementation =
        https://some-server.example/foo.js

A network location is mutable and does not establish executable identity.

Instead, the implementation artifact should be content-addressed.

Conceptually:

    Visualizer
        identity
        version
        visualizer_kind
        applicability
        visualizer_protocol_version

        implementation
            artifact_digest
            artifact_format
            entry_point
            signer
            signature
            artifact_locations*

The digest identifies the executable artifact.

Artifact locations answer only:

> Where can bytes matching this artifact identity currently be obtained?

---

# 7. Content-Addressed Executable Identity

Suppose an implementation artifact has digest:

    SHA-256 = abc123...

Any source that returns bytes matching that digest has returned the correct immutable executable artifact.

Two unrelated servers could therefore distribute the same artifact without either server becoming authoritative for its identity.

Conversely, changing even one byte produces a different artifact identity.

A new Visualizer version could therefore resolve as:

    Visualizer 2.3
        implementation digest = abc123

    Visualizer 2.4
        implementation digest = def456

This provides an important separation:

> MAP establishes semantic and cryptographic authority. Artifact transport merely supplies bytes.

---

# 8. Stewardship and Distribution Are Distinct

A MAP space such as a future Visualizer Commons may steward information such as:

    Visualizer: RichStringEditor
    Version: 2.3.1
    Steward: Alice
    Visualizer protocol: DAHN Visualizer 1.1
    Artifact digest: abcdef...
    Signature: ...

The artifact itself might simultaneously be obtainable from:

    local DAHN artifact cache
    MAP Artifact Service A
    MAP Artifact Service B
    steward-hosted endpoint
    HTTPS mirror
    content-addressed storage

None of those retrieval locations defines the executable's identity.

A completely untrusted party could mirror an artifact and still provide a useful distribution service.

They cannot silently substitute different executable code because the substituted bytes would fail digest verification.

This produces an important federation property:

> Distribution does not imply authority.

---

# 9. Provenance and Cryptographic Guarantees

Eventually Visualizer executable artifacts should support cryptographic attestation analogous to that envisioned for Dance WASM implementations.

Relevant guarantees include:

## Integrity

The bytes being executed are exactly the bytes represented by the artifact digest.

## Immutability

An artifact version is defined by immutable content.

Changing the executable creates a new artifact identity.

## Provenance

MAP metadata identifies the agent or organization that published, stewarded, or attested to the artifact.

## Authentication

Digital signatures can establish that an agent controlling a particular signing key signed a particular artifact identity.

## Durable attribution

An implementation can retain a cryptographically grounded relationship to its publisher or steward.

"Non-repudiation" may be useful shorthand, although the actual strength of such a claim depends upon assumptions about signing-key control, compromise, rotation, and identity governance.

---

# 10. Integrity Is Not the Same as Safety

Cryptographic verification proves which code is executing.

It does not prove that the code is safe.

A valid signature can establish:

> Alice published these exact bytes.

It cannot establish:

> These bytes cannot perform harmful operations.

This means dynamic visualizer execution requires two complementary trust mechanisms:

1. artifact identity and provenance
2. runtime authority restriction

The first tells DAHN what executable it has.

The second constrains what that executable is permitted to do.

---

# 11. Visualizer Runtime Protocol as a Security Boundary

Dynamically supplied visualizers should not automatically receive unrestricted access to the DAHN runtime.

Instead, contributed visualizers should operate through a constrained Visualizer Runtime Protocol.

Conceptually:

    VisualizerRuntimeContext
        readProperty(...)
        followRelationship(...)
        invokeDance(...)
        navigate(...)
        stageEdit(...)
        requestLayout(...)
        emitInteraction(...)
        requestAction(...)

The exact API remains to be designed.

The important architectural principle is that the visualizer receives specific MAP/DAHN affordances rather than arbitrary ambient authority.

A contributed visualizer should not automatically receive unrestricted access to:

    arbitrary Tauri commands
    filesystem
    shell
    arbitrary network resources
    conductor internals
    raw Rust APIs
    unrestricted operating-system capabilities

The visualizer protocol therefore serves two purposes:

1. interoperability between DAHN and independently developed visualizers
2. an execution-capability boundary

---

# 12. Relationship to Tauri Security Boundaries

DAHN's Tauri architecture already provides a useful separation between:

- Rust-side application authority
- WebView-side executable UI

The dynamic visualizer architecture should reinforce that separation rather than bypass it.

Where possible, Tauri capabilities, scopes, CSP controls, custom protocols, and DAHN-specific runtime APIs should be combined so that dynamically loaded visualizers operate with substantially less authority than the DAHN host itself.

The detailed sandboxing mechanism is intentionally deferred from the first POC, but the POC must not establish an architecture that inherently requires unrestricted dynamically loaded JavaScript.

---

# 13. DAHN-Controlled Artifact Materialization

After Rust has acquired and verified an implementation artifact, it must make that artifact available to the WebView.

A preferred conceptual mechanism is a DAHN-controlled local or custom protocol.

For example:

    map-visualizer://sha256/abc123/index.js

This URL is not the identity of the visualizer.

It is merely a local runtime handle meaning approximately:

> DAHN has authorized and verified the artifact having digest abc123 and has materialized it for this frontend runtime.

This allows TypeScript to use ordinary dynamic module loading while leaving artifact authority outside the browser.

---

# 14. Visualizer Resolution

The Rust selector should not simply return a JavaScript component name.

Nor should it return an arbitrary external URL.

Instead, selection should produce or lead to a concept approximately like:

    VisualizerResolution
        visualizer_id
        visualizer_version
        visualizer_kind

        implementation
            artifact_digest
            artifact_format
            entry_point

        visualizer_protocol_version

        authorization / trust result

        local_runtime_module_url

The final field is produced only after acquisition and verification.

The exact data structure is not yet fixed.

The architectural distinction is:

> Selection identifies the Visualizer and its authorized immutable implementation. Materialization subsequently gives the frontend a runtime mechanism for loading that implementation.

---

# 15. Visualizer Protocol Compatibility

A dynamically supplied visualizer must explicitly declare which DAHN Visualizer Protocol it implements.

For example:

    visualizer_protocol_version = 1

The runtime should reject incompatible implementations rather than attempting to infer compatibility.

The implementation should expose a standardized entry point.

Conceptually:

    createVisualizer(context)

or an equivalent protocol-defined interface.

The specific TypeScript contract should be established during the POC.

---

# 16. Candidate Architectural Alternatives

## 16.1 Alternative A — Frontend directly imports remote implementation

Flow:

    Rust selects Visualizer
            |
            v
    Rust returns URL
            |
            v
    TypeScript dynamic import(remote URL)

### Advantages

- conventional web-development model
- simple
- minimal Rust involvement

### Problems

- URLs become entangled with implementation identity
- frontend becomes responsible for artifact acquisition
- provenance and verification logic leaks into frontend
- remote source becomes implicitly authoritative
- visualizer loading becomes partially independent of MAP governance
- easier to accidentally create a second implementation-resolution architecture

### Assessment

Not recommended as the target DAHN architecture.

---

## 16.2 Alternative B — Rust selects artifact metadata; frontend retrieves it

Flow:

    Rust selects Visualizer
            |
            v
    Rust supplies URL + expected digest
            |
            v
    frontend retrieves / verifies / imports

### Advantages

- stronger than direct URL loading
- retains some Rust authority
- can use conventional browser mechanisms

### Problems

- acquisition and verification responsibility remains split
- frontend still participates in trust establishment
- MAP artifact-resolution semantics leak into TypeScript
- browser-oriented mechanisms begin to dictate architecture

### Assessment

Plausible but unnecessarily divides responsibility.

Not preferred.

---

## 16.3 Alternative C — Rust acquires and verifies; frontend only instantiates

Flow:

    Rust selects Visualizer
            |
            v
    Rust resolves artifact
            |
            v
    Rust retrieves bytes
            |
            v
    Rust verifies digest/signature
            |
            v
    Rust caches artifact
            |
            v
    Rust exposes verified local artifact
            |
            v
    frontend dynamic-imports local module
            |
            v
    frontend instantiates Visualizer

### Advantages

- Rust remains authoritative
- artifact identity remains content-addressed
- MAP-specific trust logic remains out of frontend
- physical retrieval can evolve independently
- browser dynamic import remains usable as an implementation mechanism
- clean path to federation
- supports local caching naturally
- maintains one selector and one artifact-resolution authority

### Assessment

Preferred architecture.

---

# 17. Unified Executable-Artifact Pattern

Dynamic Dance implementations and dynamic Visualizers differ in runtime technology but can share a common higher-level architecture.

Conceptually:

                          MAP
                           |
             executable artifact metadata
                           |
                +----------+----------+
                |                     |
         Dance Artifact       Visualizer Artifact
              WASM                    JS
                |                     |
                v                     v
         WASM sandbox           UI execution
                |                 boundary
                |                     |
                v                     v
         Dance Protocol       Visualizer Protocol
                |                     |
                +----------+----------+
                           |
                           v
                        MAP/DAHN

The common pattern is:

> MAP identifies and stewards executable artifacts.

> Executable artifacts are immutable and content-addressed.

> Agents may cryptographically attest to artifacts.

> Runtime policy determines whether an artifact may execute.

> Executable code interacts with its host through a constrained protocol boundary.

The execution mechanisms differ, but the governance and artifact model can remain coherent.

---

# 18. Caching Model

Because implementation artifacts are immutable and content-addressed, they are naturally cacheable.

Conceptually:

    ~/.dahn/artifacts/
        sha256/
            abc123...
            def456...

or an equivalent application-controlled store.

If Rust already possesses an artifact with the expected digest, network acquisition is unnecessary.

This means repeated loading can become:

    resolve
        ->
    cache hit
        ->
    verify cache identity if required
        ->
    materialize local runtime URL
        ->
    instantiate

The eventual cache design can therefore provide both performance and offline benefits without compromising artifact identity.

---

# 19. Core Visualizers and Dynamic Visualizers

This architecture does not require all visualizers to become external artifacts.

DAHN may continue to ship a set of core visualizers in its application bundle.

The selector can treat bundled and externally supplied visualizers uniformly at the semantic level.

For example:

    selected Visualizer
        |
        +-- implementation = bundled/core
        |
        +-- implementation = external immutable artifact

The important point is that the caller does not have to know which case applies.

This also allows DAHN to retain reliable fallback visualizers while permitting increasingly specialized visualizers to be discovered and loaded dynamically.

---

# 20. Failure and Fallback Semantics

Dynamic visualizer loading will eventually require explicit failure semantics.

Examples include:

- selected Visualizer metadata unavailable
- artifact unavailable
- digest mismatch
- invalid signature
- untrusted steward
- unsupported artifact format
- unsupported Visualizer Protocol version
- module load failure
- visualizer initialization failure
- runtime capability violation

The selector/runtime should ultimately be capable of falling back to another suitable visualizer rather than treating every external visualizer failure as fatal to visualization.

For the initial POC, only a minimal subset of this behavior needs to be implemented.

---

# 21. Proof of Concept

## 21.1 Objective

Prove the MAP-specific dynamic visualizer architecture:

> A visualizer selected in Rust can resolve to an executable artifact that is not compiled into the DAHN frontend, can be content-verified by Rust, and can subsequently be dynamically instantiated by the TypeScript runtime through the DAHN Visualizer Protocol.

The POC is not intended to prove general-purpose browser dynamic imports. That technology is already well established.

It is intended to prove the DAHN-specific architectural seam.

---

# 22. POC Scope

The POC should include two simple interchangeable visualizers for the same visualization requirement.

For example:

    CoreNodeVisualizer

and:

    DynamicNodeVisualizer

The core visualizer may remain compiled into the normal frontend bundle.

The dynamic visualizer must exist outside the compile-time frontend bundle.

The Rust selector must be capable of selecting the dynamic visualizer.

---

# 23. POC Artifact Manifest

The dynamic visualizer should have a minimal artifact manifest containing approximately:

    visualizer_id
    visualizer_version
    visualizer_kind
    visualizer_protocol_version

    artifact_format
    artifact_digest
    entry_point

For the POC, this metadata may be fixture data rather than fully represented as production MAP holons.

The important thing is to preserve the shape of the eventual architecture.

---

# 24. POC Artifact Storage

The executable artifact may initially reside in a simple fixture directory or other local external location.

For example:

    fixtures/
        visualizers/
            dynamic-node-visualizer/
                manifest.json
                index.js

The artifact must not be part of the normal TypeScript application bundle.

This proves that the visualizer is genuinely being loaded dynamically.

No distributed or MAP-native artifact transport is required for the first POC.

---

# 25. POC Execution Sequence

The POC should demonstrate the following complete sequence.

## Step 1 — Visualization request

A Holon is presented for visualization.

The request includes sufficient context for the existing Rust Visualizer Selector.

---

## Step 2 — Rust selection

The Rust selector chooses:

    DynamicNodeVisualizer

The TypeScript application does not participate in the choice.

---

## Step 3 — Implementation resolution

Rust resolves the selected Visualizer to its artifact manifest.

This yields at least:

    artifact_digest
    artifact_format
    entry_point
    visualizer_protocol_version

---

## Step 4 — Artifact acquisition

Rust reads the dynamic executable artifact from the configured POC artifact source.

This is deliberately a trivial local source.

Acquisition must nevertheless occur behind an abstraction that can later support other sources.

---

## Step 5 — Digest verification

Rust computes the executable artifact's SHA-256 digest.

It compares the computed value with the digest recorded in the Visualizer artifact metadata.

If they differ, loading must stop.

The frontend must never be given an executable handle for an artifact that failed verification.

---

## Step 6 — Immutable cache/materialization

Rust places or references the verified artifact in an application-controlled location keyed by digest.

Conceptually:

    artifact-cache/
        sha256/
            abc123.../
                index.js

The exact cache structure is not important to the POC.

Content-addressed identity is.

---

## Step 7 — DAHN-controlled frontend URL

Rust exposes the verified artifact to the WebView through an appropriately constrained mechanism.

Preferably this will resemble:

    map-visualizer://sha256/abc123/index.js

The exact protocol name is provisional.

The important requirement is that the frontend receives a DAHN-controlled handle to previously verified code rather than an arbitrary external network location.

---

## Step 8 — Dynamic import

TypeScript dynamically imports the supplied module URL.

Conceptually:

    const module = await import(resolution.moduleUrl);

The frontend does not independently calculate where the module originated.

---

## Step 9 — Protocol validation

The runtime confirms that the loaded module implements the required Visualizer Protocol.

At minimum the POC should require a well-known exported entry point.

For example:

    createVisualizer(context)

The implementation should also be associated with the expected protocol version.

---

## Step 10 — Instantiate visualizer

DAHN supplies a minimal Visualizer Runtime Context and instantiates the visualizer.

The dynamic visualizer renders successfully.

---

## Step 11 — Demonstrate integrity enforcement

Modify one byte of the dynamic artifact without updating its expected digest.

Repeat the visualization request.

Rust must reject the artifact.

The TypeScript runtime must never execute the modified implementation.

This is the key negative-path demonstration of the POC.

---

# 26. Minimal Visualizer Protocol for POC

The POC should establish the smallest useful executable contract.

For example:

    interface VisualizerModule {
        createVisualizer(
            context: VisualizerRuntimeContext
        ): VisualizerInstance;
    }

The actual shape may be adapted to the current DAHN frontend architecture.

The POC should avoid attempting to define the complete long-term Visualizer Protocol.

Its purpose is to prove that independently compiled visualizer code can reliably instantiate behind a stable DAHN-owned boundary.

---

# 27. Artifact Resolver Abstraction

Even though the POC uses a local fixture source, artifact acquisition should be hidden behind an abstraction.

Conceptually:

    ArtifactResolver.resolve(
        artifact_identity
    ) -> VerifiedArtifact

The initial implementation may be:

    LocalFixtureArtifactResolver

Future implementations might include:

    LocalCacheArtifactResolver
    MapArtifactServiceResolver
    HttpsArtifactResolver
    ContentAddressedNetworkResolver

The Selector should not know or care which resolver ultimately supplies the bytes.

Likewise, the TypeScript visualizer loader should not know how the artifact was acquired.

---

# 28. What the POC Should Deliberately Defer

The following should not be required to prove the initial architecture.

## 28.1 Digital signatures

The POC should verify SHA-256 content identity.

Agent signatures can be added once the artifact-verification seam is proven.

---

## 28.2 Full MAP representation

The Visualizer, artifact metadata, signatures, and locations do not initially need to be represented as production MAP holons.

Fixture metadata is sufficient.

The structures should nevertheless anticipate eventual MAP representation.

---

## 28.3 Visualizer Commons

No federated discovery service is required.

The selected Visualizer may be known directly to the POC.

---

## 28.4 Distributed artifact storage

Artifacts may be loaded from the local filesystem.

The resolver abstraction preserves the eventual transition to federated distribution.

---

## 28.5 Complete sandboxing

The POC need not solve the full JavaScript isolation/capability problem.

However, it should avoid unnecessarily granting the dynamic visualizer broad authority.

The POC should also clearly preserve the future Visualizer Runtime Protocol as the intended authority boundary.

---

## 28.6 Sophisticated trust policy

The initial policy can simply be:

    expected digest matches -> executable accepted

Future policies may additionally consider:

- artifact signatures
- trusted agents
- trusted stewardship spaces
- explicit agent approvals
- organizational policies
- collective reputation
- capability requirements

---

## 28.7 Production-grade version negotiation

A single Visualizer Protocol version is sufficient for the POC.

Version negotiation and backwards compatibility can follow later.

---

# 29. POC Acceptance Criteria

The POC is successful when all of the following are demonstrated.

- [ ] A Visualizer implementation exists outside the DAHN compile-time frontend bundle.
- [ ] The Rust Visualizer Selector chooses that Visualizer.
- [ ] TypeScript does not independently select or substitute another Visualizer.
- [ ] The selected Visualizer resolves to an immutable artifact identity.
- [ ] Rust acquires the implementation artifact.
- [ ] Rust calculates its content digest.
- [ ] Rust rejects an artifact whose digest does not match the expected digest.
- [ ] A successfully verified artifact is materialized through a DAHN-controlled frontend-accessible mechanism.
- [ ] TypeScript dynamically loads the verified implementation.
- [ ] The implementation exposes a standardized Visualizer Protocol entry point.
- [ ] DAHN successfully instantiates and renders the dynamic visualizer.
- [ ] Changing the artifact without changing its recorded identity prevents execution.
- [ ] Artifact acquisition is separated behind an abstraction suitable for future retrieval mechanisms.
- [ ] No visualizer-selection logic is duplicated in TypeScript.

---

# 30. Expected Follow-On Work

Successful completion of the POC should enable subsequent work in roughly this order.

## 30.1 Formalize the Visualizer Protocol

Define:

- module contract
- lifecycle
- rendering context
- MAP interaction surface
- navigation
- editing
- dance invocation
- interaction reporting
- error handling
- capability requests

---

## 30.2 Introduce signed executable artifacts

Add:

- signing-agent identity
- signatures
- signature verification
- key handling
- stewardship relationships
- trust policy

---

## 30.3 Represent Visualizers and implementations in MAP

Define MAP types and relationships for concepts such as:

- Visualizer
- Visualizer Version
- Executable Artifact
- Artifact Digest
- Artifact Signature
- Artifact Location
- Visualizer Protocol
- Visualizer applicability
- stewardship

The exact ontology should be developed independently of the POC implementation details.

---

## 30.4 Add Visualizer Commons discovery

Allow the Rust Selector to discover available Visualizers from federated MAP spaces rather than from a static application registry.

---

## 30.5 Add distributed artifact acquisition

Allow verified bytes to be sourced from one or more artifact providers.

Because identity is content-addressed, the provider does not need to be trusted to define artifact correctness.

---

## 30.6 Introduce explicit runtime capability controls

Define what contributed visualizers are permitted to do.

Move from broad host access toward narrowly granted Visualizer Runtime capabilities.

---

## 30.7 Add caching and offline semantics

Exploit immutable content addressing to allow:

- persistent caching
- deterministic reuse
- offline execution of previously acquired visualizers
- deduplication across Visualizers referencing the same implementation artifact

---

# 31. Architectural Invariants

The following should be treated as durable design constraints.

### INV-1 — Single selector

Rust is the sole authority for selecting which Visualizer should satisfy a visualization request.

### INV-2 — No frontend type-to-visualizer registry

TypeScript must not maintain an independent mapping from MAP types or visualization contexts to Visualizers.

### INV-3 — Executable identity is content-based

An external implementation is identified by immutable content identity, not by network location.

### INV-4 — Retrieval source is not authority

Where executable bytes are retrieved from must remain independent from who stewards or attests to the artifact.

### INV-5 — Verification precedes execution

An external implementation must be verified before the WebView is permitted to execute it.

### INV-6 — Artifact resolution remains host-controlled

The frontend should receive an authorized executable artifact, not independently discover one.

### INV-7 — Visualizers execute through a DAHN protocol

Dynamically supplied visualizers must conform to a DAHN-owned Visualizer Protocol.

### INV-8 — Provenance does not imply safety

Cryptographic identity and signatures establish artifact provenance and integrity but do not eliminate the need for runtime authority constraints.

### INV-9 — Artifact transport is replaceable

Local files, MAP services, HTTPS, content-addressed storage, mirrors, or future transports must be able to evolve independently of visualizer selection.

### INV-10 — Core and external visualizers remain conceptually uniform

Whether a Visualizer implementation is bundled or dynamically supplied should not alter the semantics of visualizer selection.

---

# 32. Resulting Architectural Model

The resulting model can be summarized as:

    visualization request
            |
            v
    Rust Selector
            |
            | chooses semantic Visualizer
            v
    Visualizer implementation resolution
            |
            | chooses immutable executable artifact
            v
    Artifact Resolver
            |
            | obtains bytes from any valid source
            v
    Artifact Verifier
            |
            | establishes content identity
            | and eventually provenance
            v
    Local immutable artifact
            |
            | DAHN-controlled runtime handle
            v
    TypeScript Visualizer Loader
            |
            | dynamic import
            v
    Visualizer Protocol
            |
            v
    instantiated visualizer

This preserves the open-ended extensibility of web-style dynamic code loading while relocating authority into the MAP/DAHN architecture.

The frontend retains the mechanism required to execute UI modules dynamically.

Rust retains responsibility for deciding:

- what should execute
- which immutable implementation represents it
- whether that implementation is acceptable
- which verified artifact the frontend receives

---

# 33. Broader Design Insight

Dynamic Dance implementations and dynamic Visualizers expose a more general MAP architectural concept:

> Executable behavior can itself become a first-class, stewarded, immutable, attestable resource in the MAP.

MAP need not physically contain all executable bytes.

Instead, it can provide the semantic and trust substrate by which executable artifacts are:

- identified
- described
- versioned
- stewarded
- signed
- discovered
- selected
- located
- verified
- executed under explicit protocols

For Dances, the executable boundary is naturally WASM.

For Visualizers, the executable boundary is frontend JavaScript/TypeScript.

The runtime mechanisms differ, but both can participate in the same broader federated executable-artifact architecture.

The immediate Visualizer POC should therefore prove the smallest end-to-end slice of that architecture:

> **Rust-selected → content-addressed → Rust-verified → locally materialized → dynamically imported → protocol-conforming Visualizer.**

Once that seam works, provenance, signatures, federation, distributed artifact storage, stronger sandboxing, and the Visualizer Commons can be layered onto it without changing the fundamental architecture.