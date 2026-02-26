# Distributed Query Semantics, Sovereignty, and Expansion Scope in MAP

## 1. Foundational Invariants

MAP is an agent-centric, sovereignty-preserving, federated graph system. The following invariants govern distributed query behavior:

1. **Every Holon has exactly one Home Space.**
2. **HolonIds are space-relative.** There are no universal identifiers.
3. **Holons are immutable (ActionHash-based).**
4. **Queries always return SmartReferences (never full holon bodies).**
5. **Resolution is always lazy and handled exclusively by HolonsCache.**
6. **TrustChannels govern all cross-space data exfiltration.**

These invariants eliminate global graph assumptions and require explicit domain semantics for distributed queries.

---

## 2. SmartReference Semantics

A SmartReference contains:

- A space-relative `HolonId`
- A best-effort, salience-ordered projection of properties
- A bound `TransactionContextHandle`

### Projection Rules

The projection subset is:

- TrustChannel-authorized
- Salience-ordered
- Size-bounded (e.g., 1KB LinkTag limit)

It is non-authoritative but correct (immutability guarantees no inconsistency).  
Missing properties trigger lazy resolution via HolonsCache.

### Consequences

- Filtering, sorting, and paging operate on SmartReferences.
- No eager fetch is required during query execution.
- Resolution always re-enforces TrustChannel permissions.

---

## 3. Execution Domain (Rootless Queries)

Rootless queries such as:

    MATCH (v:ValueMeme)

require an explicit **ExecutionDomain**.

There is no global scan primitive.

### ExecutionDomain defines:

- The set of spaces `Sx` in which the root pattern is evaluated.
- Typically includes:
    - Local space
    - Selected We-spaces
    - Spaces reachable via authorized TrustChannels

ExecutionDomain applies only to seed selection.

After the initial match, traversal is governed by ownership.

---

## 4. Expansion Scope Rule

### Core Rule

> Expansion is always executed in the Home Space of the source holon.

If:

- `Vl` is owned by space L → expand in L
- `Vx` is owned by space X → expand in X

Only the owning space has authoritative adjacency for a holon.

---

## 5. Cross-Space Expansion and Sovereignty

If expansion from `Vx` (in X) yields `u` (owned by Y):

1. X determines adjacency.
2. X filters results according to its TrustChannel agreement with the caller.
3. X may return `u` only if authorized to exfiltrate it.
4. Returned SmartReferences remain relative to X.

### Important

- Y granting X access to `u` does **not** imply X may share `u` with L.
- TrustChannel agreements are bilateral and non-transitive.
- No space may launder another space’s data beyond its promise.

---

## 6. Canonical Space Identity and Cross-Space Rebinding

External `HolonId`s are proxy-relative and therefore not portable across spaces:

    HolonId::External {
        space_id: Proxy_S_to_T,
        local_id: LocalId_T
    }

`Proxy_S_to_T` is defined only within space **S**.  
It has no meaning in any other space.

Therefore:

- X’s `ExternalId` for a Y-owned holon cannot be directly resolved by L.
- Proxy identifiers are strictly local wiring constructs.
- There are no universal identifiers in MAP.

---

### 6.1 Canonical Space Identity

To support federated reference exchange without leaking proxy internals, MAP introduces the concept of a **Canonical Space Identity**.

A Canonical Space Identity:

- Is a stable identifier for a space within a defined trust domain.
- Is negotiated or declared as part of TrustChannel agreements.
- Is shared among participants who intend to exchange references to that space.
- Is not required to be globally unique.
- May differ across federations or trust domains.

Important:

> A space may have multiple Canonical Space Identities, provided that any collaborating participants share the same canonical identifier for that space within their agreement scope.

The minimal requirement for rebinding is:

- If X shares a reference to a Y-owned holon with L,
- Then both X and L must recognize the same Canonical Space Identity for Y within their shared trust context.

---

### 6.2 Rebinding Rule

When X expands and encounters a holon `u` owned by Y, and is authorized to share it with L, X should return a reference expressed as:

    (canonical_space_id_Y, LocalId_Y)

Not:

    HolonId::External { proxy_X_to_Y, LocalId_Y }

Upon receiving the canonical reference, L performs rebinding:

1. L checks whether it has a TrustChannel with canonical_space_id_Y.
2. If yes:
    - L maps the canonical identity to its own proxy `Proxy_L_to_Y`.
    - L constructs:

      HolonId::External {
      space_id: Proxy_L_to_Y,
      local_id: LocalId_Y
      }

3. If no:
    - The reference is non-resolvable in L.
    - This is correct and sovereignty-preserving.

This preserves:

- Proxy isolation
- Bilateral trust semantics
- Non-universal identity
- Federated interoperability

---

### 6.3 Sovereignty and Re-Export Constraints

Canonical identity does not imply transitive trust.

Even if:

- Y grants X access to `u`, and
- X grants L access to some data,

It does not imply:

- Y has granted L access to `u`, nor
- X may re-export Y’s holons without permission.

Therefore:

- X may only return a canonical reference to `u` if permitted under its TrustChannel agreement with L.
- Re-export permission is a policy decision governed by TrustChannel terms.
- Trust is bilateral and non-transitive by default.

---

### 6.4 Correct Cross-Space Expansion Model

Cross-space expansion must respect:

1. Ownership authority (expansion executes in the home space).
2. TrustChannel exfiltration permissions.
3. Canonical identity agreement within the trust domain.
4. Proxy-relative rebinding in the receiving space.
5. Non-transitive trust constraints.

There is no implicit chain-of-trust identity propagation.
There is no universal identifier layer.
There is only negotiated canonical identity within explicit trust scopes.

---

## 7. Transitive Closure Semantics

For recursive patterns such as:

    MATCH (v)-[:RELATES_TO*]->(u)

Traversal proceeds as follows:

1. Seed set determined by ExecutionDomain.
2. Each expansion step executes in the Home Space of the current node.
3. Results are filtered by the TrustChannel between the expanding space and the caller.
4. Expansion migrates across spaces only when relationships cross space boundaries.
5. No implicit broadcast across all domains occurs.

Traversal forms a choreography of delegated expansions along trust channels.

---

## 8. No Global Graph Illusion

MAP does not model a single global graph.

It models:

- A network of sovereign graphs (one per space)
- Connected via TrustChannels
- With identity scoped per space
- And mediated expansion across boundaries

Therefore:

- There is no universal MATCH.
- There is no universal node identity.
- There is no transitive trust by default.

All distributed query behavior must respect:

- Ownership
- Mediation
- Bilateral promises
- Space-relative identity

---

## 9. Clean Responsibility Separation

| Concern              | Responsibility                      |
|----------------------|-------------------------------------|
| Seed selection       | Query layer (ExecutionDomain)       |
| Expansion locus      | Home Space of source node           |
| Data sharing         | TrustChannel policy                 |
| Resolution           | HolonsCache (lazy only)             |
| Identity scoping     | Space-relative HolonId              |

This separation preserves sovereignty while enabling federated navigation.

---

## 10. Summary

Distributed OpenCypher support in MAP must adhere to:

- Explicit ExecutionDomain for rootless queries
- Ownership-based expansion
- TrustChannel-filtered exfiltration
- Space-relative identity
- Lazy SmartReference resolution
- No implicit global graph semantics

Federated query in MAP is not global traversal.

It is mediated, delegated expansion across sovereign spaces.