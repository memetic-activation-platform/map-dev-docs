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

---

### Identity & auth

#### 1. **Cryptographic identity from day one — yes or no?**
We could use a per-device key pair now (sign every mutation locally, verify server-side), even with Better Auth/Clerk on top for "human" auth. Cost ~2–3 weeks now, but means our entire write path is already signed when we eventually move to agent identity. Or is this premature for the velocity we need?

**Response**

**Position:** Yes (lightweight version)

**Rationale:**  
This is about where identity lives—not event sourcing. Today identity is session-based (auth/JWT). Introducing lightweight signing shifts toward **data-bound authorship** without changing the architecture.

**Recommendation:**
- Generate per-device keypair
- Sign mutations locally
- Store signature + public key with writes

**Do NOT:**
- Implement full capability system
- Implement DID infrastructure

**Velocity cost:** ~3–5 days  
**Payoff:** Very high

---

#### 2. **DID (Decentralized Identifier) compatibility.**
Should our user identity model be DID-shaped from the start (`did:key:...`), so that today's "user ID" is already an agent key in the Holochain sense? Or is faking this without the underlying cryptography just cargo-culting?

**Response**

**Position:** No (defer)

**Rationale:**  
DID formatting without real infrastructure adds little value now.

**Recommendation:**
- Use opaque IDs + optional public key
- Revisit later if needed

**Velocity cost:** 0  
**Payoff:** Low

---

#### 3. **Auth provider choice for *this* phase.**
Better Auth (own it, JWT shape we control), Clerk (buy it, organizations primitive built in), or something we haven't considered? Anything in the Rust ecosystem that bridges sensibly?

**Response**

**Position:** Defer / minimize investment

**Rationale:**  
Choosing Clerk vs Better Auth assumes a session-centric, app-provider security model. Catalist 2.5 already introduces a Space-based model (data partitioning, policy scope, mediated access), and MAP extends this toward agent-centric identity and agreement-based access. In that context, deeper investment in traditional auth may be misaligned.

**Recommendation:**
- Use the simplest solution for login/session only
- Keep auth as a thin, replaceable layer
- Avoid embedding auth assumptions into data model or permission logic
- Defer deeper investment until the Space/security model is explicitly defined

**Velocity cost:** Minimal  
**Payoff:** Avoids locking into a potentially throwaway or misaligned security model

---

### Data model

#### 4. **Mutable rows vs append-only event log.**
Today's plan: rows in IndexedDB get updated in place, with an outbox for sync. Holochain source chains are append-only — every change is an entry. Should we event-source the local store now (every mutation is an immutable event, current state is a fold), so the migration is "swap the projection target"? Cost is real (~2x storage, more complex queries) but maps 1:1 onto Holochain.

**Response**

**Position:** Hybrid (mutable state + mutation log)

**Rationale:**  
Full event sourcing is expensive now, but a mutation log preserves history and aligns with future models.

**Recommendation:**
- Keep mutable rows
- Treat outbox/mutation log as first-class (not just queue)

**Velocity cost:** ~5–7 days  
**Payoff:** High

---

#### 5. **Content-addressable IDs from day one.**
If an item's ID is `hash(content + creator + timestamp)`, IDs are stable across systems. UUIDs aren't. Should we be using content-hashing for IDs everywhere now, even though Postgres doesn't need it? Same question for connections, notes, highlights.

**Response**

**Position:** Partial adoption

**Rationale:**  
All-or-nothing is unnecessary.

**Recommendation:**
- Keep UUIDs as primary IDs
- Use content hashes where useful (attachments, dedup-sensitive entities)

**Velocity cost:** ~2–3 days  
**Payoff:** Medium

---

#### 6. **Entry type definitions.**
Holochain entries are typed Rust structs. Should we be defining our domain types in a way that's a 1:1 lift to Rust structs later — e.g., TypeScript types that map cleanly to Rust serde structs, no JS-only patterns like discriminated unions with arbitrary shapes?

**Response**

**Position:** Yes (constrain now)

**Rationale:**  
Loose schemas create friction later.

**Recommendation:**
- Use explicit, stable schemas
- Avoid dynamic/unstructured shapes
- Ensure clean serialization

**Velocity cost:** ~2–4 days  
**Payoff:** High

---

### Permissions

#### 7. **Capabilities vs RLS.**
Holochain uses signed capability tokens ("Alice grants Bob the ability to read her notes for 7 days"). Supabase uses RLS (server checks `auth.uid()` against policy). These are fundamentally different models. Should we model permissions as capability grants from day one — even on Supabase — or accept RLS now and rebuild permissions during the Holochain migration?

**Response**

**Position:** Use RLS now, design for capability overlay later

**Rationale:**  
Full capability systems are heavy, but permission logic should not be tightly coupled to RLS.

**Recommendation:**
- Use RLS for enforcement
- Model permissions conceptually (capability-like), not tightly bound to RLS

**Velocity cost:** ~2–3 days  
**Payoff:** High

---

#### 8. **Cell-level access.**
RLS only handles row + table. Cell-level (e.g., "this row's salary is hidden from non-admins") needs custom views or app-layer filters. Holochain capabilities can be field-scoped natively. Worth getting this right now or later?

**Response**

**Position:** Defer

**Rationale:**  
Premature optimization.

**Recommendation:**
- Handle in application layer if needed
- Revisit when real use cases appear

**Velocity cost:** 0  
**Payoff:** Low

---

### Federation

#### 9. **Network = DNA?**
In Holochain, a DNA is an app/realm. A user's agent participates in many DNAs. Our "network scope" maps onto this. Should we structure our network model now as if each network is an independent realm (separate Postgres schemas? separate Supabase projects?), so the Holochain mapping is "network → DNA" with no flattening?

**Response**

**Position:** Yes conceptually, not physically

**Rationale:**  
Important to preserve boundary semantics without adding infrastructure complexity.

**Recommendation:**
- Treat networks as logical isolation boundaries
- Avoid splitting infrastructure early

**Velocity cost:** ~2–3 days  
**Payoff:** Medium–High

---

#### 10. **Cross-network identity.**
Person/Contact split is in the proposal. Claimed accounts use deterministic joins (`account_id`); unclaimed clusters use probabilistic dedup. In Holochain, agent identity is intrinsic. Does the Person/Contact model survive cleanly, or does Holochain force a different identity-resolution shape?

**Response**

**Position:** Current model is sufficient

**Rationale:**  
Person/Contact split is flexible and can evolve.

**Recommendation:**
- Keep model
- Ensure stable identifiers and clean linking

**Velocity cost:** 0  
**Payoff:** Medium

---

### Sync & consistency

#### 11. **CRDT vs conflict-surfacing.**
Plan is to surface conflicts to the user. Holochain's eventual-consistency model often pairs with CRDTs for specific entry types. Are there parts of our data model where we should be using CRDTs from day one (e.g., note bodies as Yjs docs, tags as add-wins sets)? Or is conflict-surfacing fine for our use cases?

**Response**

**Position:** Conflict-surfacing (correct)

**Rationale:**  
Simpler and safer.

**Recommendation:**
- Stick with current approach
- Introduce CRDTs only for specific cases (e.g., text)

**Velocity cost:** 0  
**Payoff:** High

---

#### 12. **Sync engine: roll our own or use ElectricSQL/PowerSync?**
Rolling our own gets us exactly the semantics we want and no vendor in the sync layer. ElectricSQL/PowerSync solve sync but assume Postgres-on-server, which is fine for now but adds a layer we'd shed in a Holochain migration.

**Response**

**Position:** Roll your own (for now)

**Rationale:**  
External tools introduce hidden constraints.

**Recommendation:**
- Maintain control
- Keep architecture simple and explicit

**Velocity cost:** already accounted  
**Payoff:** High

---

### Local storage

#### 13. **Dexie/IndexedDB vs wa-sqlite vs PouchDB vs sqlocal.**
SQLite-via-WASM gives us SQL parity with the server (cleaner schema migrations, same query language). PouchDB has the longest history of person-centric sync. Dexie is simplest. Anything Rust-side you'd lean toward (e.g., something WASM-compiled from Rust that bridges naturally to a Holochain agent later)?

**Response**

**Position:** wa-sqlite (preferred) or Dexie (acceptable)

**Rationale:**  
SQLite gives better long-term parity; Dexie is simpler.

**Recommendation:**
- Use wa-sqlite if acceptable complexity
- Otherwise Dexie for speed

**Velocity cost:**
- Dexie: low
- wa-sqlite: +3–5 days

**Payoff:** Medium

---

#### 14. **OPFS for blobs.**
Plan is OPFS for thumbnails/cached binaries, Supabase Storage for canonical images. Any reason to bias toward something else (e.g., always content-address blobs and ship them through a Rust-compiled WASM layer that already knows how to do CAS)?

**Response**

**Position:** OPFS is appropriate as a local cache, but the authoritative storage model should remain decoupled

**Rationale:**  
OPFS works well for local caching and offline access, but it is not authoritative storage. The current proposal implicitly treats Supabase Storage as both storage and authority, which reinforces a centralized model. If we want to preserve flexibility (including MAP alignment), it’s useful to separate:

- **Storage** (where the bytes live)
- **Integrity** (content-addressing via hash)
- **Authority / access** (who is allowed to use it)

In a MAP-aligned model, storage could be content-addressed (e.g., IPFS/Filecoin or similar), while MAP mediates access and binds content to spaces, identities, and agreements. Even if we don’t adopt that now, the architecture should avoid assuming a single canonical storage location.

**Recommendation:**
- Keep OPFS for local caching (good fit)
- Make content-addressing first-class (hash-based references, not just URLs)
- Treat Supabase Storage as a storage provider, not the authority
- Avoid coupling access control to storage layer permissions

**Velocity cost:** Minimal  
**Payoff:** Preserves flexibility for future storage and authority models without changing current implementation

---

### Migration economics

#### 15. **Honest sanity check.**
If someone gave you this stack a year from now (Supabase Postgres + Better Auth JWT + IndexedDB local-first + signed-from-day-one mutations + content-addressed IDs + capability-shaped permissions), how long does the Holochain migration actually take? 3 months? 9 months? Are there specific patterns we should add to that list to drop that number significantly, at acceptable upfront cost?

**Response**

**Position:** Substantial effort (closer to 6–12 months)

**Rationale:**  
Migration involves more than storage/sync:
- permission model shift (RLS → capabilities)
- authority model shift (server → agent)
- boundary model (spaces, mediation)
- UX paradigm differences

**Recommendation:**
Prioritize now:
- Q1: cryptographic identity
- Q4: mutation log
- Q6: type discipline
- Q7: permission abstraction

Defer:
- DID
- CRDTs
- cell-level access
- full capability system

**Velocity cost:** selective (~1–2 weeks total)  
**Payoff:** High

---

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
