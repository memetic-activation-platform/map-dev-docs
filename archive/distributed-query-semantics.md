# Distributed Query Semantics, Sovereignty, And Expansion Scope In MAP v1.3

## Purpose

This document defines how MAP navigation/query behavior works when navigation crosses space boundaries.

It applies to:

- direct navigation operation Dances such as distributed `SeedHolons` or `Expand`
- interactive `ExecutionPlan` holons built from HumanAgent gestures
- saved and replayed `ExecutionPlan` holons
- future OpenCypher/GQL queries after they compile into MAP `ExecutionPlan` holons

Distributed MAP query is not global graph traversal.
It is delegated expansion across sovereign spaces, governed by ownership, TrustChannels, and space-relative identity.

---

## 1. Core Position

The local navigation runtime model still applies in distributed execution:

```text
Navigation operation Dance
  -> HolonCollection-centered execution
  -> optional ExecutionPlan holon / NavigationExecutionBindings layer
  -> derived views only where required
```

The distributed layer adds rules for:

- where an operation may execute
- which space owns authoritative adjacency
- which references or projections may cross a boundary
- how remote references are rebound
- how authorization is enforced

Rows, paths, graph-shaped results, and tabular outputs remain derived views.
They may be exchanged at explicit contract or projection boundaries, but they are not the foundational distributed execution carrier.

---

## 2. Foundational Invariants

MAP is an agent-centric, sovereignty-preserving, federated graph system.

The following invariants govern distributed query behavior:

1. Every holon has exactly one Home Space.
2. `HolonId`s are space-relative.
3. There are no universal holon identifiers.
4. Only a holon's Home Space has authoritative adjacency for that holon.
5. Cross-space data exchange is governed by TrustChannels.
6. Resolution is lazy and re-checks authorization.
7. Navigation/query execution may exchange authorized references and projections across boundaries.
8. Full holon bodies should not cross boundaries unless an explicit contract and TrustChannel policy allow it.

These rules prevent a distributed query from pretending that MAP is one global property graph.

---

## 3. Runtime Values Across Spaces

A distributed operation may be a direct navigation operation Dance or part of an `ExecutionPlan` holon.

When the operation is captured in a plan, it names inputs and outputs symbolically:

```text
Expand {
  input: "books",
  relationship: Authors,
  output: "authors"
}
```

At execution time, `NavigationExecutionBindings` maps those variables to runtime values:

```text
NavigationExecutionBindings["books"]   -> HolonCollection
NavigationExecutionBindings["authors"] -> HolonCollection
```

In a distributed query, a `HolonCollection` may contain references whose home spaces differ from the caller's local space. Those references must still obey MAP identity and TrustChannel rules.

A boundary may expose:

- authorized `SmartReference`s
- authorized property projections
- canonical references for rebinding
- derived row/path/projection views when a contract explicitly requires them

The boundary should not force internal execution into:

```text
RowSet -> Operation -> RowSet
```

---

## 4. Execution Domain For Seed Operations

Rootless or broad seed operations require an explicit `ExecutionDomain`.

For example, a future declarative query such as:

```text
MATCH (v:ValueMeme)
```

has no global scan in MAP.

The equivalent MAP seed must say where the initial search is allowed to run:

```text
SeedHolons {
  output: "value_memes",
  scope: ExecutionDomain(...),
  holon_type: ValueMeme
}
```

An `ExecutionDomain` defines the spaces in which the root selection is evaluated.
It may include:

- the local space
- selected We-spaces
- spaces reachable through authorized TrustChannels
- other host-defined query scopes

For the query seed model, `SeedHolons(scope: FocalSpace)` is the single-space case.
It expands the focal space's `OWNS` relationship to produce the holons owned by that space, then applies any type filter.
`Focal Space` is defined as a shared runtime context term in [runtime-shared-types.md](../docs/core/type-system/runtime-shared-types.md).

`SeedHolons(scope: ExecutionDomain([spaces...]))` generalizes that rule:

```text
Expand(space_a, OWNS) -> owned_holons_a
Expand(space_b, OWNS) -> owned_holons_b
...
merge authorized results
```

For local spaces, this can include all holons owned by the space in the current transaction or snapshot.
For remote spaces, returned holons are limited by TrustChannel authorization and boundary projection rules.

The execution domain applies to seed selection.
After the initial seed, traversal follows the Home Space rule.

---

## 5. Home Space Expansion Rule

Expansion is always executed in the Home Space of the source holon.

If:

- `b1` is owned by space L, expand from `b1` in L
- `b2` is owned by space X, expand from `b2` in X

Only the owning space has authoritative adjacency for a holon.

For an operation:

```text
Expand(input: "books", relationship: Authors, output: "authors")
```

the query layer partitions the input collection by source Home Space, delegates expansion to the appropriate spaces, and merges authorized returned references into the output `HolonCollection`.

The `ExecutionPlan` holon still records one logical `Expand`.
The distributed runtime may execute that logical operation as multiple delegated expansion calls.

---

## 6. Cross-Space Expansion And Trust

If expansion from a holon in space X yields a target holon owned by space Y:

1. X determines adjacency.
2. X applies its TrustChannel policy for the caller.
3. X may return a reference or projection for the Y-owned holon only if authorized.
4. The returned reference must be expressible in a form the caller can rebind or safely hold as unresolved.

Important rules:

- Y granting X access to a holon does not imply X may share that holon with L.
- TrustChannel agreements are bilateral and non-transitive.
- No space may launder another space's data beyond its promises.
- Authorization must be re-checked during lazy resolution.

---

## 7. SmartReference And Projection Semantics

A `SmartReference` may contain:

- a space-relative `HolonId`
- a best-effort, salience-ordered property projection
- enough transaction or context information for lazy resolution

The projection subset must be:

- TrustChannel-authorized
- salience-ordered
- size-bounded when required by the transport
- non-authoritative

Missing properties trigger lazy resolution through the host cache/resolution layer, such as `HolonsCache`, and that resolution must re-enforce TrustChannel permissions.

Filtering, sorting, and paging may operate over authorized projected data when enough information is available.
If an operation needs data that is not authorized or not projected, the runtime must either resolve it through the authorized path or report that the operation cannot be completed under the current boundary conditions.

Descriptor-owned value semantics still apply when predicates or projections depend on typed property meaning.

---

## 8. Canonical Space Identity And Rebinding

External `HolonId`s are proxy-relative and therefore not portable across spaces:

```text
HolonId::External {
  space_id: Proxy_S_to_T,
  local_id: LocalId_T
}
```

`Proxy_S_to_T` is defined only within space S.
It has no meaning in any other space.

Therefore:

- X's `ExternalId` for a Y-owned holon cannot be directly resolved by L.
- Proxy identifiers are local wiring constructs.
- MAP does not create a universal identifier layer.

### 8.1 Canonical Space Identity

To support federated reference exchange without leaking proxy internals, MAP uses Canonical Space Identity within explicit trust contexts.

A Canonical Space Identity:

- is a stable identifier for a space within a defined trust domain
- is negotiated or declared as part of TrustChannel agreements
- is shared among participants who intend to exchange references to that space
- is not required to be globally unique
- may differ across federations or trust domains

A space may have multiple Canonical Space Identities, as long as collaborating participants share the same canonical identifier for that space within the relevant agreement scope.

The minimal rebinding requirement is:

- if X shares a reference to a Y-owned holon with L
- then X and L must recognize the same Canonical Space Identity for Y within their shared trust context

### 8.2 Rebinding Rule

When X expands and encounters a holon `u` owned by Y, and X is authorized to share it with L, X should return a reference expressed as:

```text
(canonical_space_id_Y, LocalId_Y)
```

not:

```text
HolonId::External { proxy_X_to_Y, LocalId_Y }
```

Upon receiving the canonical reference, L performs rebinding:

1. L checks whether it has a TrustChannel with `canonical_space_id_Y`.
2. If yes, L maps the canonical identity to its own proxy `Proxy_L_to_Y`.
3. L constructs:

```text
HolonId::External {
  space_id: Proxy_L_to_Y,
  local_id: LocalId_Y
}
```

4. If no TrustChannel exists, the reference is non-resolvable in L.

This preserves:

- proxy isolation
- bilateral trust semantics
- non-universal identity
- federated interoperability

### 8.3 Re-Export Constraints

Canonical identity does not imply transitive trust.

Even if:

- Y grants X access to `u`
- X grants L access to some data

it does not imply:

- Y has granted L access to `u`
- X may re-export Y's holons without permission

X may return a canonical reference to `u` only if permitted under its TrustChannel agreement with L.
Re-export permission is a policy decision governed by TrustChannel terms.

---

## 9. Distributed Correlation

Distributed expansion may need to preserve source-to-target correlation.

For example:

```text
books
  -> Expand(Authors)
  -> authors
```

The default output may still be a flat `HolonCollection` of authors.
If a later result needs authors grouped by book, book-author pairs, path traces, or rows, MAP should derive those views from:

- `ExecutionPlan` holon topology
- operation identities
- delegated expansion provenance
- relationship-channel names
- returned source-target association metadata where authorized
- `RelationshipMap` and `RelationshipCache` structures where available
- transaction or snapshot scope

Distributed correlation should not require `RowSet` to become the internal execution carrier.

---

## 10. Transitive Closure Semantics

For recursive patterns such as:

```text
MATCH (v)-[:RELATES_TO*]->(u)
```

traversal proceeds as delegated expansion:

1. The seed set is determined by `ExecutionDomain`.
2. Each expansion step executes in the Home Space of the current source holon.
3. Each expanding space filters results through its TrustChannel policy.
4. Traversal migrates across spaces only when authorized relationships cross space boundaries.
5. No implicit broadcast across all domains occurs.

Descriptor-backed predicate and relationship semantics must remain consistent across the traversal.
Spaces must not reinterpret descriptor-backed predicates through ad hoc local client logic.

Path-like results are derived traversal traces.
They may be materialized when an output contract, explanation view, or future OpenCypher/GQL-compatible result requires them.

---

## 11. No Global Graph Illusion

MAP models:

- a network of sovereign graphs
- one authoritative Home Space per holon
- TrustChannel-mediated exchange
- space-relative identity
- delegated expansion across boundaries

Therefore:

- there is no universal `MATCH`
- there is no universal node identity
- there is no transitive trust by default
- there is no hidden global property graph inside MAP Core

All distributed query behavior must respect:

- ownership
- mediation
- bilateral promises
- authorization
- space-relative identity

---

## 12. Responsibility Separation

| Concern | Responsibility |
| --- | --- |
| Plan structure | `ExecutionPlan` HolonType and plan holons |
| Plan execution bindings | `NavigationExecutionBindings` |
| Local holon result carrier | `HolonCollection` |
| Seed selection | Query layer and `ExecutionDomain` |
| Expansion locus | Home Space of the source holon |
| Relationship legality | Descriptor-backed effective structure |
| Data sharing | TrustChannel policy |
| Lazy resolution | Host cache/resolution layer |
| Identity scoping | Space-relative `HolonId` |
| Cross-space exchange | Authorized references and projections |
| Row/path/tabular output | Derived boundary or projection view |

This separation preserves sovereignty while allowing federated navigation to remain part of the same MAP query model.

---

## Summary

Federated query in MAP is mediated, delegated expansion across sovereign spaces.

Distributed query execution must preserve:

- explicit `ExecutionDomain` for rootless seeds
- ownership-based expansion
- TrustChannel-filtered exchange
- canonical identity and local rebinding
- lazy resolution with authorization checks
- `ExecutionPlan` holon structure across delegated operations
- `HolonCollection` as the primary holon result carrier
- derived row/path/projection views only where boundaries or output contracts require them

OpenCypher and GQL compatibility can build on these rules later by compiling declarative forms into MAP `ExecutionPlan` holons.
They do not change the sovereignty model or require distributed MAP execution to become row-stream based.
