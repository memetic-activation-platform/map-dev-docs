# Adversarial Review: MAP Validation & Descriptor Architecture

**Date:** 2026-07-10
**Reviewer:** Claude (adversarial design review requested by Rashaan)

**Scope:** The recent architecture/validation doc set in `map-dev-docs`, read against Holochain's integrity-zome execution model and the current `map-holons` implementation.

**Documents reviewed:**

- `docs/core/architecture/arch-overview.md` (v0.1)
- `docs/core/validation/validation-arch.md` (v1.3)
- `docs/core/validation/dependency-gravity.md` (v2.1)
- `docs/core/descriptors/effective-descriptor.md`
- `docs/core/type-system/map-type-system.md` (v1.3)
- `docs/core/agent-spaces/agent-space-arch.md`
- `docs/mapp-dev/extensibility-model.md`
- `docs/mapp-dev/trust-channel.md`
- `docs/mapp-dev/map-security-model.md` (v1.0, Oct 2025)
- `docs/glossary/glossary.md` (consulted for terminology)

**Code grounding:** `happ/zomes/integrity/holons_integrity`, `happ/crates/holons_guest_integrity`, `shared_crates/shared_validation`, `shared_crates/type_system/core_types/src/ids.rs`, reference-layer `DescribedBy` handling in `shared_crates/holons_core`, and the canonical core-schema JSON in `host/import_files/map-schema/core-schema/`.

---

## 0. Overall Assessment

The v1.3 validation architecture is a sound resolution of the core tension (open, descriptor-driven ontology vs. immutable, deterministic integrity zome). Content-addressed compiled descriptor surfaces retrieved via deterministic dependency fetch is the right Holochain-native mechanism, and dependency gravity is the right classifier for where rules execute.

The findings below fall into five groups:

1. The **central peer-validation guarantee is weaker than some doc language implies**, and the composition that restores the full guarantee (read-time activation filtering) is implied but never specified. (§2)
2. Several **specific claims in the newest docs are not implementable as written** on Holochain — most concentrated in the `pvl_surface` example and the descriptor-retrieval mechanics. (§3, §4)
3. **SmartLink/relationship validation** needs to be split into classes with different PVL fates; one class (link authorship) is the only available defense against graph graffiti and must not leave PVL. (§5)
4. The **identity-type model in code** needs distinct types for route-sensitive vs. path-independent identity before canonical encodings ossify the current shape. (§6)
5. The **older security docs overclaim enforcement against insiders** and predate the AgentSpace consolidation; they need explicit supersession or rewrite. (§8)

Also included: a spam/resource-exhaustion threat analysis (§7) and a prioritized list of open design questions (§9).

---

## 1. Implementation Baseline (for calibration)

The current integrity zome is a skeleton:

- One entry type: `HolonNode { original_id, property_map }` — **no `described_by` or `effective_descriptor_hash` field** (`happ/crates/holons_guest_integrity/src/holon_node.rs`).
- Four link types (`AllHolonNodes`, `HolonNodeUpdates`, `LocalHolonSpace`, `SmartLink`).
- Every domain validation function in `shared_crates/shared_validation/src/validation_helpers.rs` returns `Ok(())` ("Deferring logic until Descriptors").
- `DescribedBy` exists only as an ordinary relationship (SmartLink) managed in the reference layer.

Implication: the proposed architecture requires an entry-type change plus a PVL interpreter in the integrity zome — a new DNA hash and fresh DHTs. Acceptable pre-production, but it means **the PVL kernel shipped at stabilization becomes the immutable floor for every AgentSpace created on it.** Every finding below should be read with that one-way door in mind.

---

## 2. The Central Guarantee — State It Honestly, Then Compose It

**Finding (highest priority).** Under the proposed design, any DHT member can author a well-formed `EffectiveDescriptor` — including a bogus one claiming `type_key: "Person"` with arbitrary constraints — commit it (it passes the fixed bootstrap rules of validation-arch §8.4), and commit holons referencing it. Peers validate those holons against the descriptor they *name* and accept them. PVL cannot check activation, because "is this descriptor activated?" is temporal, open-world, and revocable, while Holochain validation must return the same verdict for the same op forever. The docs correctly exclude activation from PVL — but `arch-overview.md` §14 then says the Space Manager will "ensure committed holons reference activated descriptor semantics," which a modified coordinator simply bypasses.

The honest statement of the peer-validation guarantee is:

> **Descriptor-relative validation:** Integrity/PVL proves that a holon conforms to the specific content-addressed semantic surface it names. It does not prove that the surface is activated, authorized, socially legitimate, or semantically canonical for the HolonSpace.

**Recommendation.** State this as a named principle, and then state the composition that restores the full guarantee — currently implied but specified nowhere:

- **Write time (PVL):** holon conforms to the surface it names. Proven once, by every peer.
- **Read time ("activation filtering"):** the named surface is one this space has activated. Checked as set membership: `holon.effective_descriptor_hash ∈ activated_set`.

Together these reconstruct "this holon is a valid instance of a type this space recognizes" without putting governance in the integrity zome — and read-time evaluation makes activation naturally *revocable* (disable a descriptor → its instances vanish from the space's semantic surface without deletion), which immutable integrity validation could never provide.

**Activation filtering needs a spec.** Suggested shape:

- Activation records are holons in the space's DHT (per validation-arch §5.3), **countersigned by space-steward role keys** so any reader can verify them cryptographically rather than trusting a coordinator. Sketch:

  ```text
  HolonNode:
    effective_descriptor_hash: EffectiveDescriptorHash

  ActivationRecord:
    activated_effective_descriptor_hash: EffectiveDescriptorHash
    semantic_type_identity
    semantic_version / version constraints
    activation_status  (Proposed | Active | Disabled | Deprecated)
    governance_evidence (steward countersignatures)
  ```

- The Reference Layer maintains the **activated set** (small, cacheable, invalidated on activation-record change).
- Every read ingress — holon fetch, collection resolution, query results, SmartLink traversal — applies the membership check. Failing holons are *unrecognized*: excluded by default, visible only via explicit diagnostic/quarantine views. Edges into unrecognized holons are dropped or flagged.
- The Nursery applies the same check write-side (binds honest coordinators only; the read-side check is what binds everyone).

Activation must stay separate from descriptor identity: PVL answers "conforms to the named surface"; activation answers "this space recognizes that surface." Do not bake activation state into the immutable validation path or into `EffectiveDescriptorHash`.

**Decision required:** mandatory Reference Layer behavior (enforced at the single read ingress, with explicit bypass for diagnostics) vs. per-consumer discipline. Strong recommendation for mandatory — if it is discipline, the guarantee evaporates the first time a query path forgets. A corollary the docs should acknowledge: unactivated-but-structurally-valid data in the DHT is now a first-class *expected* condition (spam surface, conflict-set noise), not an anomaly.

---

## 3. Contradictions / Non-Implementable Claims in the Newest Docs

### 3.1 The `pvl_surface` example contradicts the docs' own PVL boundary

`effective-descriptor.md` §5 places `min_cardinality: 1` (AUTHORED_BY) and `max_cardinality: 1` (PUBLISHED_BY) in `pvl_surface.relationship_checks`. Neither is enforceable:

- Holochain validates at **op granularity**. Even when multiple actions are written atomically, they are not validated together as one transaction; an action can depend on prior actions, never subsequent ones. The `HolonNode` StoreEntry op cannot see SmartLinks — so `min_cardinality ≥ 1` cannot be checked at entry time.
- validation-arch §16.2 itself states links cannot enforce the absence of other links — so `max_cardinality` cannot be checked at link time.
- `ordered: true` is likewise not an op-level invariant (link ordering is encoded in tags; tag *shape* is checkable, global order is not).

"Bounded cardinality where reconstructible" is doing unexamined work: at op granularity, essentially *no* cardinality is reconstructible unless transaction membership is explicitly carried in the op (a transaction-manifest entry enumerating the transaction's holons and links, or a countersigned commit). **Either specify that mechanism, or strip cardinality/ordering from `pvl_surface` (moving them to `non_pvl_semantics.nursery_rules`).**

### 3.2 Descriptor retrieval must be content-addressed: `must_get_entry`, not `must_get_valid_record`

The docs define `effective_descriptor_hash = EntryHash(EffectiveDescriptor)` and then call `must_get_valid_record(effective_descriptor_hash)` (validation-arch §8.3, effective-descriptor §9). In HDI, `must_get_valid_record` takes an `ActionHash`. The fix is not to switch identity to `ActionHash` — it is to name the right retrieval function and accept its consequences:

```text
HolonNode.effective_descriptor_hash : EffectiveDescriptorHash (EntryHash-based)
    ↓ must_get_entry(effective_descriptor_hash)
decode canonical effective_descriptor_bytes
    ↓
validate artifact with the fixed bootstrap PVL rules (§8.4)
    ↓
validate the HolonNode against the verified surface
```

- **`must_get_entry` carries no validity claim** — Holochain documents that `must_get_entry`/`must_get_action` do not verify the retrieved data was valid. That is acceptable *by design* here: PVL re-verifies the artifact with the fixed bootstrap rules on every use. Trust comes from re-verification of content, not from another peer's record validity. (The bootstrap rules are cheap and closed-world; see §3.8.)
- **`ActionHash` must never participate in descriptor identity.** The same compiled surface committed twice (or provisioned into two spaces) yields different ActionHashes and authors; ActionHash is route/context identity. It may exist locally for provenance, activation records, cache internals, and retrieval optimization — but never for definitional equivalence. Update validation-arch §3.3 and §8.3 accordingly.

Two precision requirements that neither the docs nor either review draft had fully pinned down:

1. **The retrieval key must literally be a Holochain `EntryHash`.** A MAP-level canonical hash computed over `effective_descriptor_bytes` alone cannot be dereferenced by `must_get_entry`. If MAP also wants a bytes-level identity (analogous to `DefinitionHash`, useful pre-commit and cross-substrate), the artifact must carry both, and PVL verifies their correspondence after fetch. Decide explicitly which one `effective_descriptor_hash` is.
2. **The carrier entry must be canonical.** `EntryHash` covers the *entire* `HolonNode` entry (`original_id` + the full `property_map`), not just the bytes payload. The EffectiveDescriptor carrier holon must therefore be fully determined by the compiled surface: `original_id = None`, a fixed minimal property set, no variable or cosmetic properties (display names, timestamps, notes). Otherwise identical compiled surfaces get different EntryHashes, breaking `DescriptorsCache` equivalence and cross-space recognition. This canonicality rule belongs in the fixed bootstrap validation (§8.4) itself.

### 3.3 Subtype checking is impossible against a fully flattened surface

`map-type-system.md` §12: relationship validity requires the target's type to be "equal to or **extend**" `R.TargetType`. But EffectiveDescriptors flatten inheritance away. When PVL validates a SmartLink, it fetches the *target's* EffectiveDescriptor and finds only a leaf `type_key` — it cannot determine that `PhysicianAuthor` extends `Person` without graph traversal, which PVL forbids.

**Missing structural element: a `conforms_to` set** — the transitive closure of ancestor type identities (with versions) — in every EffectiveDescriptor:

```text
conforms_to: [
  { semantic_type_id: "Holon",  version: "*"  },
  { semantic_type_id: "Agent",  version: "^1" },
  { semantic_type_id: "Person", version: "^2" }
]
```

Without it, PVL relationship typing degenerates to exact-type match, which breaks the extensibility model's core promise (extensions interoperate with parent-typed relationships), or typing leaves PVL entirely (see §5 for that trade). Runtime consumers (query engine, Nursery) need the same closure regardless of the PVL decision.

### 3.4 Hash-pinned target types make the descriptor DAG brittle under evolution

The example pins `target_type_definition_hash: defhash:type:person:...` in relationship checks. When Person evolves to v2, every descriptor pinning Person-v1 must be recompiled, reactivated, and (potentially) instances migrated before links to Person-v2 instances validate — a DAG-wide rebuild ripple on every edit of a widely-referenced type.

**Needed: an explicit position on version-tolerant type identity.** Keep the four identity notions separate and use each where it belongs:

```text
semantic_type_identity        — stable across versions; what relationship checks should target
semantic_version / range      — optional constraint on the above
DefinitionHash                — authored-surface content identity
EffectiveDescriptorHash       — compiled-surface content identity (retrieval + validation binding)
```

Relationship typing should match on `semantic_type_identity` (+ optional version range) against the target's `conforms_to` set (§3.3); pin a `DefinitionHash` only where exact-version matching is genuinely intended.

### 3.5 The `described_by` / `effective_descriptor_hash` binding — revise the model (v1 recommendation retracted)

validation-arch §8.3 says PVL should "confirm it applies to holon.described_by." How? `described_by` names a TypeDescriptor graph holon; the EffectiveDescriptor's link back to it is `CompiledFrom` — a SmartLink, which PVL must not traverse. Matching `type_key` strings is forgeable (§2).

v1 of this review suggested embedding the `CompiledFrom` source **ActionHash** in the artifact. **Retracted:** in a *consuming* space, the authored descriptor graph may not exist at all — only the provisioned compiled artifact (§4.4) — and the source's ActionHash is specific to the authoring space's DHT. ActionHash binding would break cross-space descriptor use outright.

Revised recommendation — two coherent options:

- **(a) Drop `described_by` from the committed representation entirely.** The holon's type claim is fully derivable from the artifact it names: the EffectiveDescriptor carries `semantic_type_identity`, version, and `conforms_to`. One binding, nothing to cross-check in PVL. The runtime `DescribedBy` SmartLink remains a graph/navigation convenience whose consistency with `effective_descriptor_hash` is a Nursery and read-side concern.
- **(b) Keep a committed type claim, but bind it path-independently.** Embed inside `effective_descriptor_bytes`:

  ```text
  compiled_from_definition_hash:  DefinitionHash
  semantic_type_identity:         SemanticTypeId
  compiler_identity / version:    CompilerId, SemVer
  canonical_encoding:             "map.effective-descriptor.v1"
  ```

  PVL then checks the holon's committed claim against fields it can read from the verified artifact — no traversal, no route-sensitive identity. The `CompiledFrom` SmartLink stays navigational/provenance-only.

Option (a) is simpler and is the recommended default; either way, effective-descriptor §8 should state that PVL never depends on the `CompiledFrom` link.

### 3.6 Updates must not change type — enforce it

The core schema settles this (`DescribedBy` is `is_definitional: true`, `max_cardinality: 1` in `core-schema/...relationship-types.json`): a holon cannot change type; retyping means a new holon. The validation doc should state the corresponding PVL rule explicitly: **reject any HolonNode update whose `effective_descriptor_hash` differs from the original's.** This is deterministic (the original record is already a `must_get` dependency of the update op) and cheap.

### 3.7 Compiler identity is missing from definitional identity

`DefinitionHash` is computed over the *authored* surface; `EffectiveDescriptorHash` over the *compiled* surface. Equal DefinitionHash implies equal compiled surface only under a fixed compiler and canonical encoding. The DescriptorsCache is keyed by DefinitionHash (arch-overview §10.2): after a compiler upgrade it can serve stale compiled surfaces, and spaces on different MAP releases will disagree about which compiled hash a DefinitionHash maps to.

**Key descriptor caches and activation mappings by the tuple:**

```text
(DefinitionHash, compiler_identity, compiler_version, canonical_encoding) → EffectiveDescriptorHash
```

and carry `compiler_identity`/`compiler_version` inside the artifact bytes (§3.5b), so the mapping is verifiable from the artifact alone.

### 3.8 The bootstrap base case is unspecified

EffectiveDescriptors are stored as ordinary HolonNodes with an `effective_descriptor_bytes` property (deliberately — no new EntryType). Unanswered:

- What is the `effective_descriptor_hash` **of an EffectiveDescriptor holon**? The §8.4 fixed-rules path needs a defined chain termination.
- How does integrity *recognize* a HolonNode as an EffectiveDescriptor artifact?
- The holon-data-loader has an unstated ordering constraint on fresh DHTs: compiled surfaces must be committed *before* the descriptor holons that reference them, including the `TypeDescriptor` self-description knot.

Proposed shape (avoids infinite regress):

```text
if HolonNode is an EffectiveDescriptor artifact:
    validate storage envelope with fixed bootstrap rules
    validate canonical carrier shape (§3.2.2) and bytes decode
    validate embedded compiled_from / compiler fields are well-formed
    require NO effective_descriptor_hash dependency
else:
    require effective_descriptor_hash; fetch and validate per §3.2
```

The discriminant mechanism is itself a design decision: an explicit entry field (e.g., `kind: EffectiveDescriptorArtifact`) vs. property presence. A field is cleaner and costs nothing since the entry type is changing anyway; if property-presence is chosen instead, the fixed rules must be safe when arbitrary agents decorate arbitrary holons with that property.

### 3.9 Dances are absent from the compiled surface

extensibility-model.md specifies `EffectiveDanceSet` computation and single-implementation-per-chain validation; arch-overview lists affordances in the Descriptor Graph; the Dance Dispatcher is listed as an EffectiveDescriptor consumer — but effective-descriptor.md's struct has no dance/affordance section. If dispatch is to be "no runtime search," the EffectiveDanceSet belongs in the compiled surface, and the chain-aware single-implementation check should be explicitly assigned to compile time (Descriptors component).

### 3.10 Clarify "no replication" in Holochain terms

"Every holon has exactly one Home Space; MAP avoids replication of stewarded state" is a *stewardship* claim, but reads as a *storage* claim. Holochain physically replicates DHT data among the peers of the Home Space's network — that is how validation and availability work. Suggested wording for arch-overview §2.1:

> MAP avoids **semantic replication of authoritative stewarded state across Home Spaces**. Holochain may still physically replicate DHT operations among peers within a Home Space's network for validation, storage, and availability.

This also sharpens the compiled-surface exception (§2.4): what is being exempted is *cross-space* persistence of deterministic artifacts, not intra-space DHT redundancy.

### 3.11 Minor: version/terminology alignment

- extensibility-model.md references "MAP Type System v2.0" and a "stabilization" concept; map-type-system.md is v1.3 and does not define stabilization.
- The glossary resolves HolonSpace ≡ AgentSpace; the architecture docs should cross-reference it (arch-overview and validation-arch use HolonSpace/Home Space; agent-space-arch uses AgentSpace exclusively).
- `TypeDescriptor` names a specific bootstrap holon in the type-system doc but is used generically ("TypeDescriptors, PropertyDescriptors…") in arch-overview §4.1.

---

## 4. Holochain-Mechanics Concerns

1. **Unresolvable dependencies as a poisoning vector.** A holon referencing a never-committed descriptor hash sits in "awaiting dependencies" limbo indefinitely — never rejected, never integrated, cheap to mass-produce. Needs a resource-handling note (validation-queue pressure; whether Sustainer covers it).
2. **Regex in PVL is a determinism/DoS hazard.** `pattern` value checks invite catastrophic backtracking; validation cost must be bounded and identical across peers. Specify a linear-time engine (RE2-class subset) as part of the PVL spec, or exclude patterns from PVL and keep them in the Nursery.
3. **PVL needs quantified resource bounds** as part of the format, not just the adjective "bounded": max `HolonNode` entry size; max property count; max property-key length; max scalar value size; max `effective_descriptor_bytes` size; max property/relationship check counts; max enum-value count; max pattern length; max link-tag size; max array/nesting depth (if arrays are admitted); **max validation-dependency count per op**. §8.4 says integrity checks "boundedness" — against undefined limits. Any peer divergence in interpretation is a permanent fork; there is no patch path for an integrity zome.
4. **Cross-space descriptor provisioning is unspecified.** A type authored in Space A, used in Space B: the compiled surface must exist *in B's DHT* for `must_get_entry` to succeed — PVL cannot dereference a TrustChannel during validation. Specify the flow: foreign descriptor discovered → compiled artifact obtained or reproduced → **artifact committed into the local DHT** (canonical carrier, so its EntryHash matches everywhere; author is whoever provisions, which is why authorship must not affect identity, §3.2) → activation record created → holons may reference it. This is where the compiled-surface exemption from no-replication (§3.10) meets practice.
5. **`Some(None)` in `PropertyMap`.** `BTreeMap<PropertyName, Option<PropertyValue>>` permits present-with-null. Required-property checks must define whether that satisfies requiredness — trivial, but a peer-divergence risk if left implicit.
6. **PVL evolution = DNA change.** The PVL interpreter + canonical encoding version is compiled into the DNA; a new opcode or format version means a new DNA, a new DHT, and migration of every AgentSpace. "Reject unknown opcodes" strands old spaces; "ignore unknown opcodes" silently weakens validation. No doc addresses migration. This is the deepest long-horizon question in the design.
7. **Receipt-verification scope.** dependency-gravity v2.1 lists receipt digest/signature checks under "PVL always includes"; validation-arch v1.3 conditions receipt verification on the acceptance rule being PVL-safe (validator identity fixed or reconstructible). Align the two — the validation-arch framing is the correct one.

---

## 5. SmartLink Validation: Split It Into Three Classes

Relationship validation is not one decision. Split it:

**(a) Authorship/shape envelope checks** — descriptor-independent: tag well-formedness, base/target are HolonNode action hashes, size caps, and *who may attach a link to this base*.
**(b) Descriptor-backed typing** — relationship name declared on the base's effective descriptor; target type conforms (requires `conforms_to`, §3.3).
**(c) Cardinality / exclusivity / ordering** — not PVL-enforceable at op granularity (§3.1); Nursery regardless.

**The critical adversarial fact:** in Holochain, *any member can create a link based at any holon, including holons they don't own.* Consequences if relationship validation leaves PVL wholesale:

- **Graffiti:** anyone can attach arbitrary edges that appear in a victim's relationship collections and traversals. With auto-inverse SmartLinks (issue 442), an attacker can forge inverse edges that *inject their holons into the collection views of holons they don't control*. Nursery validation is irrelevant — the attacker isn't running the honest coordinator.
- **Attacker-controlled read cost:** garbage edges are permanent (tombstones don't reclaim). Attach 10,000 junk links to a popular holon and every uncached traversal fetches and filters all of them, forever. Links rejected by integrity validation, by contrast, are never integrated, gossiped, or served. Write-time rejection is the only firewall with this property.

**Recommendation:**

- **Class (a) stays in PVL — non-negotiable.** It needs no descriptors and no EffectiveDescriptor fetches; it is tiny, closed-world, and it is the only graffiti defense available. Design wrinkle: strict `link author == base author` breaks legitimate inverse links (B relates B's holon → A's holon; the inverse is based at A's holon, authored by B). Fix: the inverse link's tag carries the forward link's `ActionHash`; PVL does a deterministic `must_get` to verify the forward link exists, corresponds (source/target/relationship), and shares the author. Inverse links become provenance-carrying and peer-checkable. Note also that *whether* third parties may attach edges to a holon is arguably a per-type policy (open annotation is legitimate) — without a PVL rule it is unconditionally open, which should be a decision, not a default.
- **Class (b) is a cost/benefit call and can defensibly be deferred to runtime** — with eyes open. Honest-mistake corruption is still caught by the Nursery. The bill: the peer-validated guarantee shrinks from "the graph is well-typed" to "the *nodes* are well-typed; edges are claims"; every consumer (query engine, DAHN, dance preconditions) must treat inbound edges as untrusted input and filter against descriptors at read time (target-conformance requires fetching the target before including an edge — read amplification on cold traversals, amortized by DescriptorsCache). Upside: the launch PVL kernel shrinks substantially (no two-descriptor fetch on link ops; `conforms_to` still needed for runtime filtering but not frozen into the DNA). **The trap:** adding (b) later is a DNA change; the realistic choice is "now vs. probably never for existing spaces."
- **Class (c) goes to the Nursery, full stop**, unless/until a transaction-manifest mechanism (§3.1) makes specific cases reconstructible.

---

## 6. Code-Level Identity Types (verified against current source)

The identity distinctions in §3.2/§3.4 need to land in code before canonical encodings ossify the current shapes.

1. **`ExternalId` lags the architecture doc.** arch-overview §2.2 defines `ExternalId = OutboundProxyId + RemoteObjectId`, but the code (`shared_crates/type_system/core_types/src/ids.rs:25`) has:

   ```rust
   pub struct ExternalId {
       pub space_id: OutboundProxyId,
       pub local_id: LocalId,   // LocalId = raw ActionHash bytes
   }
   ```

   The second component of a foreign reference is not necessarily a Holochain `ActionHash` — under TrustChannel mediation it may be an opaque alias, an agreement-scoped reference, or a revocable mapping key that only the remote steward can resolve. It should become `remote_object_id: RemoteObjectId` (opaque bytes, steward-interpreted).

2. **Urgency: the current shape is already being baked into canonical encodings.** `HolonId::to_canonical_bytes` (`ids.rs:75`) encodes `ExternalId` as `(proxy LocalId, LocalId)` inside the canonical `HolonIdValueType` byte format. Changing the remote-id shape later changes canonical value encoding — a versioning event. Decide before more canonical encodings depend on it.

3. **Introduce distinct hash newtypes.** No `DefinitionHash` or `EffectiveDescriptorHash` type exists in the codebase yet. When they land, they must be distinct newtypes — not aliases of `LocalId` — so route-sensitive and path-independent identities cannot be confused at compile time:

   ```rust
   pub struct DefinitionHash(pub Vec<u8>);          // authored-surface content identity
   pub struct EffectiveDescriptorHash(pub Vec<u8>); // compiled-surface identity (EntryHash-based, §3.2)
   ```

This is a code follow-up rather than a doc patch, but the docs (validation-arch §3, arch-overview §3) should name the type-level separation as intended design so the implementation doesn't drift back to `LocalId`-for-everything.

---

## 7. Spam / Resource-Exhaustion Threat Analysis

Semantic integrity is robust against spam: curation is positive designation (meaningful holons are those reachable from chosen anchors via authored relationships), and append-only + signed data means spam cannot alter, displace, or impersonate curated content. Spam attacks **resources and attention**, not meaning — with the one exception of edge graffiti, addressed by §5(a).

**Yes, a space can be degraded, and no current doc addresses it:**

- Only members can spam (non-members cannot author DHT ops; TrustChannel traffic is request/response, not DHT writes) — so it is strictly an insider problem, and the fractal AgentSpace model is itself the primary blast-radius control.
- In small spaces, every member effectively stores everything; entries are immutable and deletes are tombstones — **storage is never reclaimed**. A hostile member converts write access into permanent disk/bandwidth/CPU consumption on every peer. There is no gas/fee mechanism; nothing meters writes by default. Plus the limbo-op vector (§4.1).

**Mitigations, in order of leverage:**

1. **Membrane design is the primary control** (vouching, invitation, progressive trust for open commons). The security model should state explicitly that write-flood resistance is a membrane property.
2. **PVL-enforceable per-agent quotas.** Validation may deterministically inspect the author's own source chain up to the op being validated (`must_get_agent_activity` — the chain below a given action never changes). This supports entry-size caps, chain-rate caps, and payload limits as peer-reproducible rules, and it binds agents running their own conductors — the only *hard* write metering available. Recommend adding to the PVL construct list.
3. **Keep bulk bytes out of the DHT:** max entry sizes in PVL; media in separate content-addressed stores referenced by hash.
4. **Attribution and ejection — with honesty about limits.** Ops are signed and chain-anchored; spam is attributable and actionable by governance. But expelling an already-joined agent is weak at the infrastructure level, and committed data remains regardless.
5. **Space migration as the designed backstop.** A terminally flooded space can be abandoned: fresh DHT, re-commit curated holons (their one-Home-Space moves), re-establish TrustChannel routes. Recommend making "space migration/rescue" a first-class designed dance — the only true compaction mechanism Holochain permits, and its existence changes attacker calculus (flooding buys one disposable DHT's worth of damage).
6. Sustainer throttling/load-shedding is resilience for honest nodes, not defense; classify it accordingly.

---

## 8. Older Docs vs. the Consolidated Architecture

`trust-channel.md` and `map-security-model.md` predate the AgentSpace consolidation:

1. **Envelope stacks:** trust-channel.md hardcodes a five-envelope sequence; agent-space-arch makes capsule composition Agreement-defined via EnvelopeType descriptors. Mark the old doc superseded, or rewrite it as an *example* protocol suite.
2. **The security model overclaims enforcement against insiders.** Lens filtering, ExfiltrationPolicy, and audit events are enforced by cooperating coordinator/client code. Within a single AgentSpace DHT, every member's conductor holds and serves the full shared graph; a member running a modified coordinator reads everything, writes anything that passes (descriptor-relative) integrity validation, and emits no audit events. The §10 threat-model table lists "Privilege Escalation → lens filtering" as a mitigation — honest-client-only. **Restructure around the actual trust boundaries:**

   | Boundary | Hard enforcement | Honest-client / soft enforcement |
      |---|---|---|
   | Before joining a space | Membrane proof, invitation, governance admission | Social review |
   | Inside a space's DHT | PVL, source-chain signatures, PVL quotas (§7.2) | Lens filtering, UI policy, audit events |
   | Between spaces | TrustChannels: encryption, signatures, agreement-scoped capsules | Protocol negotiation, preferences |
   | After compromise/spam | Attribution, governance, migration/rescue (§7.5) | Throttling, quarantine views |

   ExfiltrationPolicy in particular should be reframed as honest-client compliance plus accountability, not prevention (data a member can read, a member can copy).
3. **Dynamic Dance Dispatch is unaddressed by the security model.** agent-space-arch: behaviors "dynamically loaded, verified, and executed" without DNA changes. Nothing specifies code provenance/signing, version pinning, capability boundaries, sandboxing, revocation, whether community-authored dances can read/write holons directly, or whether TrustChannel envelope wrap/unwrap can be dynamic code vs. declarative protocol configuration only (visualizers vs. executable dances also deserve distinct treatment). Given how carefully the architecture keeps dynamic execution out of integrity, host-side execution of community-authored dances is now the platform's largest attack surface, and it is undocumented.

---

## 9. Open Design Questions (prioritized)

1. **PVL evolution/migration story** (§4.6). How do existing AgentSpaces adopt a new PVL opcode or encoding version? This shapes how conservative the launch kernel should be.
2. **Activation filtering:** mandatory Reference Layer behavior or consumer discipline? Countersigned activation records? (§2)
3. **What exactly is `EffectiveDescriptorHash`** — literally the Holochain `EntryHash` of a canonical carrier entry, a MAP-level hash of the canonical bytes, or both carried and cross-verified? And what makes the carrier entry canonical? (§3.2)
4. **Transaction manifests:** will any mechanism ever make multi-op invariants (cardinality, transaction coherence) peer-checkable, or is the Nursery permanently the ceiling? (§3.1)
5. **`conforms_to` in EffectiveDescriptor + version-tolerant semantic type identity** for relationship targets. (§3.3, §3.4)
6. **`described_by` binding:** drop from the committed representation (derive from the artifact) or keep with embedded path-independent source binding? (§3.5)
7. **SmartLink PVL scope:** adopt the (a)/(b)/(c) split? Is class (b) in or out of the launch kernel (recognizing "out" is likely permanent for existing spaces)? Inverse-link provenance tags? (§5)
8. **Bootstrap base case** for EffectiveDescriptor holons (discriminant field vs. property presence) + loader ordering on fresh DHTs. (§3.8)
9. **Cross-space compiled-surface provisioning:** who commits a foreign type's artifact into the consuming space's DHT, and when? (§4.4)
10. **Compiler identity in definitional identity / cache keys.** (§3.7)
11. **Who vouches for compilation correctness** before reproducible compiler receipts exist — is steward review of compiled surfaces a defined governance step at activation?
12. **EffectiveDanceSet placement** in the compiled surface and compile-time enforcement of single-implementation-per-chain. (§3.9)
13. **Quantified PVL resource bounds.** (§4.3)
14. **Dynamic Dance Dispatch trust/sandbox model.** (§8.3)
15. **When does `ExternalId` adopt `RemoteObjectId`** — before or after canonical `HolonIdValueType` encoding proliferates? (§6)

---

## 10. Concrete Doc-Change Checklist

| Doc | Change |
|---|---|
| arch-overview.md | Add "descriptor-relative validation" + activation-filtering composition as named principles; soften §14 Space Manager claim to coordinator-scope; adopt the "no semantic replication" wording (§3.10); state the route-sensitive vs. path-independent identity type separation (§6). |
| validation-arch.md | Replace `must_get_valid_record(effective_descriptor_hash)` with `must_get_entry` + fixed-rule re-verification, and state that ActionHash never participates in descriptor identity (§3.2); revise §8.3 "applies to described_by" per §3.5 (drop the field, or bind path-independently); add update-type-immutability PVL rule (§3.6); add agent-activity quota constructs and quantified resource bounds to PVL (§4.3, §7.2); add limbo-op handling note (§4.1); align receipt-verification scope with dependency-gravity (§4.7); clarify PVL-safe vs. Nursery-only relationship constraints (§5). |
| effective-descriptor.md | Define `EffectiveDescriptorHash` precisely, incl. the canonical-carrier requirement (§3.2); remove cardinality/ordering from `pvl_surface` or specify transaction manifests (§3.1); add `conforms_to` (§3.3); switch pinned target hashes to semantic-identity matching (§3.4); embed `compiled_from_definition_hash` + `semantic_type_identity` + compiler identity/version in the bytes, and state `CompiledFrom` SmartLink is navigational only (§3.5, §3.7); define the bootstrap base case and discriminant (§3.8); add EffectiveDanceSet or explicitly defer it (§3.9); constrain or drop `pattern` (§4.2); warn that ActionHash must not participate in artifact identity (§3.2). |
| agent-space-arch.md | Add cross-space compiled-surface provisioning flow (§4.4); add a Dynamic Dance Dispatch security model section (or reference a new one) distinguishing declarative protocol config from executable code (§8.3). |
| map-security-model.md | Rewrite threat model around the trust-boundary table (§8.2); reframe ExfiltrationPolicy as compliance/accountability; add spam/resource-exhaustion section (§7); add Dynamic Dance Dispatch security section (§8.3). |
| trust-channel.md | Mark superseded by agent-space-arch, or recast as an example protocol suite. |
| extensibility-model.md | Align version references ("v2.0" vs. v1.3) and define or drop "stabilization"; cross-reference the glossary for space terminology. |

**Code follow-ups (map-holons, not docs):** `ExternalId.local_id` → `remote_object_id: RemoteObjectId` before canonical encodings proliferate (§6.2); introduce `DefinitionHash` / `EffectiveDescriptorHash` newtypes distinct from `LocalId` (§6.3).
