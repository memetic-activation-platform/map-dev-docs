# Architecture Brief — for Holochain/Rust Architect to Review

**Audience:** Holochain/Rust dev with expertise in person-centric architecture

**Goal:** Get critical feedback on the data architecture we're about to commit to, *before* we commit to it. Speed is the priority right now, but we want to avoid baking in assumptions that make a future migration to Holochain (or any person-centric distributed model) brutally expensive.

**Status:** Pre-decision. Source docs: [[Backend Architecture Proposal]] and [[Supabase Migration Plan]].

---

## TL;DR

We're a single-dev React + D3 app currently on Airtable. Need to migrate to a real backend to support multi-user, real-time, RLS-style permissions, and the upcoming **Compass** vision (personal-scope app federated across networks the user belongs to).

**Current leaning** (after a black-hat review of two competing proposals):

1. **Supabase as the network-shared backend** — central authority for data shared across a network/community/fellowship.
2. **Local-first storage on the device for personal-scope data** — IndexedDB or wa-sqlite. The user's personal Compass data is sourced from the device, synced to Supabase as a backup/relay.
3. **Skip Supabase Auth.** Use **Better Auth** or Clerk so auth is a swappable layer, not the lock-in surface.
4. **Strict portability discipline** — raw SQL or Drizzle (no PostgREST DSL leak), FKs to our own user table not `auth.users`, capabilities flag pattern in DataService for feature gating.

The **hypothesis** behind the split: personal-scope-local-first is the only architectural choice today that meaningfully aligns with a future Holochain destination, because it forces us to design the app as "this user, working with their data, federating into networks" rather than "logged-in clients of a central server."

---

## Why we're talking about Holochain at all

Long-term direction is uncertain but the user has a real conviction toward:

- **Knowledge-graph-shaped data** (which Postgres/SQL handles fine, but graph DBs handle better)
- **Person-centric / data sovereignty** (your data lives with you, you grant access to it; not "log in to read shared data")
- **Possibly Holochain** as the eventual substrate, OR something else with the same shape (local-first + cryptographic identity + federated rather than centralized)

Speed is the priority *now*. We need to ship Compass features within ~6 months, support multiple workspaces, have working real-time and offline, and not melt the dev under a perfect-architecture spiral.

We'd like the eventual Holochain migration (if it happens) to be a *re-targeting of sync layer + identity*, not a rewrite of the whole app.

---

## What we're proposing to build

### Storage split

| Scope                                                                      | Storage                                               | Source of truth                      | Why                                                                            |
|----------------------------------------------------------------------------|-------------------------------------------------------|--------------------------------------|--------------------------------------------------------------------------------|
| Personal Compass data (notes, highlights, personal items, views, layouts)  | IndexedDB (or wa-sqlite) on device                    | The device                           | Already shaped like Holochain personal source chain                            |
| Network-shared data (community directory, network-published views, events) | Supabase (Postgres + RLS)                             | Server                               | Networks are inherently shared; needs central authority                        |
| User-uploaded images / attachments                                         | Supabase Storage (private bucket), referenced by hash | Server (with content addressing)     | Maps onto Holochain "binaries go to content-addressed store, not source chain" |
| Identity / auth                                                            | Better Auth or Clerk, JWTs Supabase accepts           | Whichever auth provider              | Decoupled from Supabase so it can be swapped                                   |
| Article/transcript caches                                                  | IndexedDB                                             | Cached external content, recoverable | Not user data, just convenience cache                                          |

### Sync model (personal-scope)

- Local writes are immediate; an **outbox** captures unsynced mutations.
- Sync engine drains outbox to server, pulls remote changes since last sync, merges into local stores.
- Conflicts surface to the user ("present, don't merge"), not auto-resolved by algorithm.
- Each row carries `localVersion`, `serverVersion`, `updatedAt`, soft `deletedAt`.

### What this maps onto in Holochain

| Today (proposed) | Holochain analogue |
|---|---|
| IndexedDB / wa-sqlite store | Agent's source chain + local cache |
| Outbox of pending mutations | Source chain entries (signed, append-only) |
| Sync to Supabase | Sync to DHT / agent-to-agent gossip |
| Network-shared Supabase tables | DHT-shared entries within a DNA |
| Better Auth / JWT | Agent key pair + capability tokens |
| Content-addressed image storage | DHT entries referenced by hash |
| Federation layer (API merging personal + network) | Multi-DNA composition |

The bet: if these mappings are roughly right, the migration is "rewire the sync target" instead of "rebuild the app."

---

## What we're explicitly NOT doing yet

- **Generic API tier / headless CMS layer.** YAGNI — no actual external consumers asking for it.
- **Full multi-backend abstraction.** We have the DataService seam; that's enough for now.
- **CRDTs.** Conflict-present-to-user is simpler and safer than algorithmic merge.
- **Building Holochain integration now.** Ecosystem too immature for the velocity we need.

---

## Open questions for you to weigh in on

These are the decisions where strong opinions are most valuable. We'd rather hear "you're about to bake in a thing that will cost you a year later" *now* than discover it ourselves in 18 months.

The framing below assumes a **Dual POC strategy**.

Under that framing, the key question is not:

> “What is the ideal long-term architecture?”

It is:

> “Which investments in the Supabase path are durable, and which are likely to become transitional scaffolding, architectural gravity, or throwaway work if MAP convergence later becomes desirable?”

---

### Identity & auth

#### 1. **Cryptographic identity from day one — yes or no?**
We could use a per-device key pair now (sign every mutation locally, verify server-side), even with Better Auth/Clerk on top for "human" auth. Cost ~2–3 weeks now, but means our entire write path is already signed when we eventually move to agent identity. Or is this premature for the velocity we need?

**Response**

**Position:** Yes (lightweight version)

**Rationale:**  
This is about where identity lives—not event sourcing. Today identity is session-based (auth/JWT). Introducing lightweight signing shifts toward **data-bound authorship** without changing the architecture.

Unlike many MAP-aligned patterns, this is not likely to become throwaway work later. Signed mutations, provenance, and device-level authorship remain meaningful regardless of whether the runtime later converges toward MAP.

**Recommendation:**
- Generate per-device keypair
- Sign mutations locally
- Store signature + public key with writes

**Do NOT:**
- Implement full capability system
- Implement DID infrastructure

**Supabase POC guidance:**  
This is one of the few areas where lightweight early investment likely survives future architectural evolution cleanly.

---

#### 2. **DID (Decentralized Identifier) compatibility.**
Should our user identity model be DID-shaped from the start (`did:key:...`), so that today's "user ID" is already an agent key in the Holochain sense? Or is faking this without the underlying cryptography just cargo-culting?

**Response**

**Position:** No (defer)

**Rationale:**  
DID formatting without real infrastructure adds little value now.

MAP doesn't need or use DIDs. It doesn't rely on an external identity provider, whether decentralized or not.

This risks becoming purely symbolic alignment work that adds conceptual complexity without creating durable architectural value.

**Recommendation:**
- Use opaque IDs + optional public key
- Revisit later if needed

**Supabase POC guidance:**  
Avoid investing in identity-shape abstraction that does not materially change coordination semantics or migration difficulty.

---

#### 3. **Auth provider choice for *this* phase.**
Better Auth (own it, JWT shape we control), Clerk (buy it, organizations primitive built in), or something we haven't considered? Anything in the Rust ecosystem that bridges sensibly?

**Response**

**Position:** Defer / minimize investment

**Rationale:**  
Choosing Clerk vs Better Auth assumes a session-centric, app-provider security model. Catalist 2.5 already introduces a Space-based model (data partitioning, policy scope, mediated access), and MAP extends this toward agent-centric identity and agreement-based access. In that context, deeper investment in traditional auth may be misaligned.

Neither Better Auth nor Clerk are part of or needed by MAP.

The risk here is not technical incompatibility alone, but:
- mental-model entrenchment
- permission-model entrenchment
- and emotional investment in a security architecture that may later be displaced by Space-based coordination semantics.

**Recommendation:**
- Use the simplest solution for login/session only
- Keep auth as a thin, replaceable layer
- Avoid embedding auth assumptions into data model or permission logic
- Defer deeper investment until the Space/security model is explicitly defined

**Supabase POC guidance:**  
Treat auth as operational plumbing, not foundational architecture.

---

### Data model

#### 4. **Mutable rows vs append-only event log.**
Today's plan: rows in IndexedDB get updated in place, with an outbox for sync. Holochain source chains are append-only — every change is an entry. Should we event-source the local store now (every mutation is an immutable event, current state is a fold), so the migration is "swap the projection target"? Cost is real (~2x storage, more complex queries) but maps 1:1 onto Holochain.

**Response**

**Position:** Do not invest in full event sourcing now

**Rationale:**  
MAP already handles this at the platform layer. Its storage model provides a staging area / Nursery for accumulating transient and staged holons prior to commit, then commits immutable holons. That gives the benefits of immutability and provenance without requiring the application layer to implement an event-sourced architecture.

For Catalist-on-Supabase, trying to approximate Holochain/MAP’s append-only model with a custom local event log risks building a partial “MAP-lite” persistence layer that will likely be thrown away later. It may slow the Supabase path without substantially reducing the later transition to MAP, because MAP’s runtime semantics are not just event sourcing; they include:
- holon staging
- commit lifecycle
- provenance
- conflict handling
- and semantic transaction semantics.

**Recommendation:**
- Keep the Supabase/local model simple
- Use an outbox only as needed for practical offline/pending-write behavior
- Do not treat the outbox as a first-class attempt to model MAP/Holochain storage
- If MAP adoption becomes serious, rely on MAP Core’s Nursery/staging/commit model rather than reimplementing it

**Supabase POC guidance:**  
Avoid building custom persistence semantics that MAP already intends to own at the runtime layer.

---

#### 5. **Content-addressable IDs from day one.**
If an item's ID is `hash(content + creator + timestamp)`, IDs are stable across systems. UUIDs aren't. Should we be using content-hashing for IDs everywhere now, even though Postgres doesn't need it? Same question for connections, notes, highlights.

**Response**

**Position:** Partial adoption

**Rationale:**  
All-or-nothing is unnecessary.

Content-addressing has durable value in:
- attachments
- provenance-sensitive assets
- dedup-sensitive content
- integrity verification

But forcing the entire application model into content-derived identity now risks premature coupling and unnecessary complexity.

**Recommendation:**
- Keep UUIDs as primary IDs
- Use content hashes where useful (attachments, dedup-sensitive entities)

**Supabase POC guidance:**  
Use content-addressing where it creates durable value, not as a symbolic alignment exercise.

---

#### 6. **Entry type definitions.**
Holochain entries are typed Rust structs. Should we be defining our domain types in a way that's a 1:1 lift to Rust structs later — e.g., TypeScript types that map cleanly to Rust serde structs, no JS-only patterns like discriminated unions with arbitrary shapes?

**Response**

**Position:** No (do not constrain to Rust/Holochain types)

**Rationale:**  
MAP hides Holochain as a storage layer. The model exposed to developers is not Rust structs, but **self-describing, active holons** with properties, relationships, and behaviors (Dances). These are available through both Rust and TypeScript bindings.

Designing domain types to map cleanly to Rust structs is solving the wrong problem. It couples the application layer to an implementation detail (Holochain) rather than aligning with the MAP abstraction (holons). It also tends to produce rigid schemas that limit extensibility.

In MAP, extensibility is achieved through:
- self-describing holons
- additive properties and relationships
- dynamic composition

Strong, static domain schemas often get in the way of this.

**Recommendation:**
- Keep domain models flexible and evolvable
- Prefer self-describing, extensible structures over tightly constrained schemas
- Avoid premature coupling to Rust/Holochain serialization constraints
- If needed, add domain-specific types as a convenience layer, not as the core model

**Supabase POC guidance:**  
Avoid baking Holochain implementation assumptions into the application model. Align with MAP abstractions, not storage internals.

---

### Permissions

#### 7. **Capabilities vs RLS.**
Holochain uses signed capability tokens ("Alice grants Bob the ability to read her notes for 7 days"). Supabase uses RLS (server checks `auth.uid()` against policy). These are fundamentally different models. Should we model permissions as capability grants from day one — even on Supabase — or accept RLS now and rebuild permissions during the Holochain migration?

**Response**

**Position:** Use RLS for enforcement, but minimize investment in application-level access control and explicitly plan for a Space-based model

**Rationale:**  
The relevant comparison is not Holochain capabilities vs RLS, but **MAP’s agreement-driven security model vs RLS**.

In MAP:
- access control is externalized from application code
- policies are defined in digitally signed agreements
- enforcement occurs at the membrane / trust channel layer
- authority is tied to Spaces and relationships, not user/session identity

Supabase RLS is also policy-driven, which makes it a reasonable short-term enforcement mechanism. However, it is still:
- server-centric
- session-based (`auth.uid()`)
- not aligned with Space-based or agreement-driven access

Building significant application-layer permission logic on top of RLS risks:
- duplicating logic that will later move into agreements
- coupling business logic to a specific enforcement mechanism
- making transition to a Space-based model more difficult

**Recommendation:**
- Use RLS for enforcement
- Minimize application-enforced access control logic
- Do not attempt to implement capabilities or agreements in the application layer
- Explicitly define how the Space-based access model will be represented conceptually
- Ensure permission logic is not tightly coupled to `auth.uid()` or specific auth-provider semantics

**Supabase POC guidance:**  
Avoid building large amounts of app-specific authorization logic that later becomes displaced by MAP’s agreement/membrane model.

---

#### 8. **Cell-level access.**
RLS only handles row + table. Cell-level (e.g., "this row's salary is hidden from non-admins") needs custom views or app-layer filters. Holochain capabilities can be field-scoped natively. Worth getting this right now or later?

**Response**

**Position:** Defer

**Rationale:**  
MAP provides attribute-level granularity, but importantly this is infrastructure/policy-driven rather than deeply embedded into application logic.

Building custom application-layer field filtering now risks creating throwaway security semantics that later become displaced by Space-, agreement-, and membrane-level enforcement.

**Recommendation:**
- Revisit only when real use cases appear
- Avoid elaborate app-specific field-filter infrastructure

**Supabase POC guidance:**  
Do not invest heavily in fine-grained custom authorization semantics unless absolutely required for immediate client delivery.

---

### Federation

#### 9. **Network = DNA?**
In Holochain, a DNA is an app/realm. A user's agent participates in many DNAs. Our "network scope" maps onto this. Should we structure our network model now as if each network is an independent realm (separate Postgres schemas? separate Supabase projects?), so the Holochain mapping is "network → DNA" with no flattening?

**Response**

**Position:** Reframe around Spaces, not DNAs

**Rationale:**  
The relevant MAP concept is not the Holochain DNA by itself, but the **Space**. In MAP, a Space is the fundamental unit of organization and security. Each Space has:
- its own context
- member agents
- governance/access conditions
- and underlying DHT participation model

So the important question is not:

> “Does network map to DNA?”

It is:

> “How does Catalist’s Network/Space model map to MAP Spaces?”

Catalist 2.5 already has a strong Space model:
- data partitioning
- access policy scope
- mediated cross-space access

That should be reconciled with the MAP Space model before deciding the Supabase backend structure.

**Recommendation:**
- Treat Space as the primary logical boundary
- Reconcile Catalist Spaces / Networks with MAP Spaces explicitly
- Do not start by splitting Supabase into separate schemas/projects
- First define:
  - What is a Space?
  - What data belongs to a Space?
  - What policies belong to a Space?
  - How is cross-space access mediated?
- Let the Supabase implementation follow from that model

**Supabase POC guidance:**  
Preserve the Space abstraction conceptually without prematurely committing to infrastructure partitioning strategies.

---

#### 10. **Cross-network identity.**
Person/Contact split is in the proposal. Claimed accounts use deterministic joins (`account_id`); unclaimed clusters use probabilistic dedup. In Holochain, agent identity is intrinsic. Does the Person/Contact model survive cleanly, or does Holochain force a different identity-resolution shape?

**Response**

**Position:** The Person/Contact split is likely not aligned with the MAP model and should be reconsidered

**Rationale:**  
The Holochain framing is not the relevant comparison. MAP introduces a fundamentally different approach to identity.

In MAP:
- identity is agent-centric
- Agents exist within Spaces
- relationships emerge through:
  - participation
  - agreements
  - shared context
  - and nested belonging

The AgentSpace model provides a topology of belonging that replaces much of the need for:
- deterministic identity joins
- probabilistic deduplication
- separate “contact” representations

This significantly simplifies the conceptual model for:
- developers
- users
- admins

**Recommendation:**
- Do not over-invest in the Person/Contact split as a foundational model
- Treat identity as agent-centric and space-contextual
- Revisit whether the current identity complexity is solving problems that disappear under a Space-oriented model

**Supabase POC guidance:**  
Avoid deeply entrenching identity-resolution infrastructure that may become unnecessary under MAP’s Space/Agent topology.

---

### Sync & consistency

#### 11. **CRDT vs conflict-surfacing.**
Plan is to surface conflicts to the user. Holochain's eventual-consistency model often pairs with CRDTs for specific entry types. Are there parts of our data model where we should be using CRDTs from day one (e.g., note bodies as Yjs docs, tags as add-wins sets)? Or is conflict-surfacing fine for our use cases?

**Response**

**Position:** Conflict-surfacing is the correct default for now

**Rationale:**  
This question again risks overfitting to Holochain implementation patterns rather than focusing on the actual coordination semantics Catalist is trying to support.

MAP’s transaction model explicitly distinguishes between:
- structural correctness
- local semantic coherence
- agreement conformance
- and social truth

MAP is NOT fundamentally CRDT-oriented.

Its model is instead built around:
- staged semantic transactions
- explicit provenance
- MVCC-style divergence
- conflict detection
- attestation
- and agreement-mediated reconciliation

The key principle is:

> semantic correctness is more important than automatic convergence.

MAP therefore assumes:
- conflicts are normal
- divergence is expected
- reconciliation is often social/semantic rather than algorithmic

CRDTs solve a very specific class of problems:
- highly concurrent
- low-latency
- multi-writer editing

But they also introduce:
- semantic complexity
- synchronization opacity
- debugging difficulty
- hidden merge behavior
- maintenance burden

Most Catalist coordination semantics appear to be:
- socially mediated
- governance-aware
- context-sensitive
- and better resolved explicitly than silently merged

MAP’s transaction architecture already provides a richer coordination model through:
- Nursery-scoped semantic validation
- explicit validation outcomes
- provenance
- conflict detection
- compensating transactions
- deferred social reconciliation

That is fundamentally different from “always converge automatically” systems.

**Recommendation:**
- Keep conflict-surfacing as the default model
- Treat divergence as expected rather than exceptional
- Preserve explicit provenance and semantic transaction boundaries
- Introduce CRDTs only for narrowly scoped collaboration cases where clearly justified (e.g., rich-text co-editing)

Avoid:
- embedding CRDT semantics deeply into the overall coordination architecture
- optimizing prematurely for invisible automatic convergence

**Supabase POC guidance:**  
Avoid building deep synchronization semantics that MAP already intends to handle differently at the runtime/transaction layer.

#### 12. **Sync engine: roll our own or use ElectricSQL/PowerSync?**
Rolling our own gets us exactly the semantics we want and no vendor in the sync layer. ElectricSQL/PowerSync solve sync but assume Postgres-on-server, which is fine for now but adds a layer we'd shed in a Holochain migration.

**Response**

**Position:** Minimize investment in Supabase-specific synchronization infrastructure

**Rationale:**  
This is less a question about sync tooling and more a question about where synchronization semantics ultimately live.

ElectricSQL/PowerSync accelerate:
- local-first replication
- realtime synchronization
- conflict propagation
- client cache coherence

But they also reinforce:
- a Postgres-centric worldview
- JS/client-owned synchronization semantics
- and application-layer coordination ownership.

MAP already has a fundamentally different synchronization model centered around:
- staged transactions
- provenance
- semantic validation
- Spaces
- trust boundaries
- and runtime-managed coordination.

The risk is not merely “vendor lock-in.”

The deeper risk is:
- embedding synchronization semantics into frontend/runtime application logic
- building coordination assumptions around Postgres replication
- and accumulating synchronization infrastructure that later becomes architecturally stranded under MAP.

At the same time, building a sophisticated custom sync engine inside the Supabase path also risks:
- creating transitional coordination infrastructure
- reinventing semantics MAP already intends to own
- and slowing near-term delivery.

**Recommendation:**
- Keep synchronization semantics as simple as possible in the Supabase path
- Prefer pragmatic, operationally useful synchronization over architecturally ambitious synchronization
- Treat sync primarily as:
  - operational replication
  - cache coherence
  - pending-write propagation
- Keep synchronization boundaries explicit and replaceable

Avoid:
- deeply embedding synchronization semantics into React/client architecture
- building elaborate custom coordination infrastructure
- tightly coupling application behavior to Postgres replication assumptions
- prematurely recreating MAP-style runtime coordination semantics in JS

**Supabase POC guidance:**  
Use only as much synchronization infrastructure as is necessary to achieve the POC goals. Avoid investing heavily in synchronization semantics that MAP already intends to own at the runtime/platform layer.

---

### Local storage

#### 13. **Dexie/IndexedDB vs wa-sqlite vs PouchDB vs sqlocal.**
SQLite-via-WASM gives us SQL parity with the server (cleaner schema migrations, same query language). PouchDB has the longest history of person-centric sync. Dexie is simplest. Anything Rust-side you'd lean toward (e.g., something WASM-compiled from Rust that bridges naturally to a Holochain agent later)?

**Response**

**Position:** Prefer the simplest local storage model that satisfies the actual POC requirements

**Rationale:**  
This question again risks prematurely optimizing for future runtime alignment rather than current POC goals.

The important architectural concern is not:
- SQL parity
- Rust interoperability
- or Holochain compatibility

It is:
- how much synchronization/runtime semantics become embedded into the client storage layer.

MAP already abstracts storage behind:
- holon lifecycle semantics
- staging/commit semantics
- runtime-managed coordination
- and SDK-level abstractions.

That means much of the sophistication being considered here may become transitional scaffolding later.

The local storage layer in the Supabase POC should primarily support:
- offline usability
- cache persistence
- local responsiveness
- pending-write durability

—not become an attempt to reproduce MAP’s runtime/storage semantics.

SQLite parity is attractive operationally, but may encourage:
- tighter coupling to relational assumptions
- shared query semantics between client/server
- and deeper embedding of synchronization logic into the application layer.

PouchDB carries even stronger synchronization-model assumptions that may diverge significantly from MAP’s transaction/provenance-oriented architecture.

Dexie/IndexedDB is comparatively simple and lightweight, which may actually be an advantage under a Dual POC strategy because it minimizes architectural commitment.

**Recommendation:**
- Prefer the simplest viable local storage layer
- Treat local storage primarily as:
  - cache
  - offline support
  - pending-write durability
- Keep synchronization semantics outside the storage engine itself
- Avoid deep coupling between local storage model and backend/runtime assumptions

If additional capability is truly needed:
- wa-sqlite is likely preferable to PouchDB because it adds less opinionated synchronization architecture

Avoid:
- embedding synchronization semantics deeply into the storage layer
- tightly coupling local storage to Supabase query semantics
- prematurely optimizing for Holochain/Rust interoperability
- treating local storage as a proto-MAP runtime

**Supabase POC guidance:**  
Optimize for minimal architectural commitment and operational sufficiency, not for speculative long-term runtime convergence.

---

#### 14. **OPFS for blobs.** 
Plan is OPFS for thumbnails/cached binaries, Supabase Storage for canonical images. Any reason to bias toward something else (e.g., always content-address blobs and ship them through a Rust-compiled WASM layer that already knows how to do CAS)?


**Position:** Use OPFS for local caching, but keep canonical blob identity content-addressed and avoid making Supabase Storage the architectural authority.

**Supabase Recommendation:**  
Supabase Storage is a reasonable near-term backing store, provided it is treated as a provider, not as the long-term source of truth for blob identity or authority.

**Rationale:**  
OPFS is a good fit for:

- thumbnails
- cached binaries
- offline-friendly local blob access
- reducing repeated remote fetches

But OPFS is only browser-local persistence. It should not define:

- canonical blob identity
- integrity guarantees
- authorization semantics

The important architectural separation is:

- **Storage**: where the bytes physically live
- **Integrity**: how we identify the bytes we mean
- **Authority / access**: who is allowed to retrieve, use, or share them

If we want to preserve future flexibility, the durable identity should be content-addressed rather than location-addressed. That means:

- hash-based blob references
- pluggable backing stores
- authority decisions above the storage layer

Under that model:

- OPFS is a local cache
- Supabase Storage is a practical current provider
- neither one becomes the architectural source of truth

That also keeps the door open for later evolution toward:

- CAS-backed storage
- IPFS-style distribution
- Rust/WASM blob tooling that already understands content addressing
- MAP-mediated access, provenance, and agreement semantics

**Recommendation:**

- Keep OPFS for local blob caching
- Use Supabase Storage as the current canonical backing store
- Make content-addressing first-class in blob references
- Treat storage provider choice as replaceable
- Keep access-control and authority semantics above the storage layer
- If a Rust/WASM CAS layer is likely, shape interfaces now so it can be introduced without changing blob identity semantics

---

### Migration economics

#### 15. **Honest sanity check.**
If someone gave you this stack a year from now (Supabase Postgres + Better Auth JWT + IndexedDB local-first + signed-from-day-one mutations + content-addressed IDs + capability-shaped permissions), how long does the Holochain migration actually take? 3 months? 9 months? Are there specific patterns we should add to that list to drop that number significantly, at acceptable upfront cost?

**Response**

**Position:** The primary risk is not backend migration difficulty, but architectural gravity and coordination ownership entrenchment

**Rationale:**  
The original question frames migration primarily as:
- storage migration
- sync migration
- auth migration
- or Holochain replacement.

But the deeper concern is that the Supabase path naturally encourages:
- application-owned synchronization
- frontend-managed coordination
- JS-centric collaboration semantics
- client/server mental models
- and operational dependence on centralized runtime assumptions.

If those patterns become deeply embedded over the next year, the later challenge is not:
- “swap databases”

It becomes:
- relocating runtime responsibilities
- rewriting synchronization semantics
- restructuring coordination ownership
- retraining architectural thinking
- and potentially discarding large amounts of application-layer coordination infrastructure.

In other words:

> the migration burden increasingly becomes organizational and architectural rather than purely technical.

At the same time, not all Supabase-path investments are equal.

Some investments are likely durable:
- lightweight cryptographic identity
- provenance-aware mutation recording
- Space-oriented conceptual boundaries
- clean service abstractions
- avoiding deep coupling to Supabase semantics

Others are more likely transitional:
- custom synchronization infrastructure
- elaborate JS coordination semantics
- app-layer collaboration engines
- Supabase-centric permission models
- frontend-owned conflict semantics

The key issue is not:
- “how long would migration take?”

It is:

> “How much application-owned coordination architecture accumulates before MAP becomes operationally viable?”

That determines:
- migration complexity
- emotional resistance to convergence
- organizational lock-in
- and long-term architectural coherence.

**Recommendation:**
- Treat runtime coordination semantics as the highest-risk area for architectural gravity
- Minimize investment in custom application-layer synchronization infrastructure
- Keep:
  - permissions
  - synchronization
  - provenance
  - and collaboration semantics
    behind explicit boundaries
- Avoid deeply coupling application behavior to:
  - Supabase replication semantics
  - frontend-managed coordination
  - or JS-centric runtime assumptions
- Explicitly distinguish:
  - operational plumbing
  - from foundational coordination architecture

Avoid:
- assuming migration is primarily a storage/backend problem
- measuring migration complexity only in engineering-month estimates
- allowing the first operationally successful architecture to silently become the permanent conceptual model

**Supabase POC guidance:**  
The most important thing is not minimizing future database migration effort. It is minimizing long-term architectural gravity and avoiding deep entrenchment of application-owned coordination semantics before MAP viability becomes clear.

---

## Source docs

If you want full context before answering:

- [[Backend Architecture Proposal]] — the ambitious vision (tiered architecture, Compass federation, Person/Contact identity, Views/Layouts/Templates, AI-assisted config). Good for understanding *where we want to end up*.
- [[Supabase Migration Plan]] — the focused near-term plan. Phases A through G. Good for understanding *what we're about to build first*.

The conversation that produced this brief covered: black-hat critique of both docs, RLS row vs cell granularity, what "shape-locked into Supabase" actually means, where IndexedDB lives and what binaries to put where, and the rationale for the personal/network split. Available on request if helpful.

---

## Goal


1. Identify which of the 15 questions above you have the strongest opinions on.
2. For each: what we'd be doing wrong under our current plan, what to do instead, and rough cost (days/weeks of velocity tax now).
3. Flag anything we're *not* asking that should be in the question list.
4. Give us a calibrated honest take: is the proposed split (Supabase + local-first personal scope) actually a meaningful step toward MAP, or is it cosplay that won't matter?

Speed matters. We don't need a perfect architecture. We need to know which 3-5 things, if we get them right *now*, will save us a year later — and which "Holochain-aligned" patterns are nice-to-have we should skip.
