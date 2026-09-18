# MAP Runtime Transaction Design Specification

> **Status: Draft — reverse-engineered from current architecture and implementation.**
>
> This specification defines MAP runtime transaction semantics. It does not define the Commands IPC contract, structural undo/redo, crash-recovery persistence, or a future persistent transaction-record/audit model.

## 1. Purpose and document boundaries

This specification owns:

- `TransactionContext` as the runtime transaction-scoped execution surface;
- transaction ownership of transient and staged state;
- public versus private transaction contexts;
- `TxId` registration and lookup semantics;
- Space-scoped saved-reference reads and restricted cache-read frames;
- host/guest projection of transaction state;
- semantic clone versus raw staging transfer; and
- the boundary between local transaction coherence and distributed consistency.

Related documents own adjacent concerns:

- [MAP Commands Specification](../commands-and-runtime/commands.md) owns TypeScript-to-host IPC, wire/domain binding, command scope, and command lifecycle enforcement.
- [Structural Experience-Level Undo / Redo Specification](../commands-and-runtime/struct-exp-undo-redo.md) owns transaction-scoped editing history, checkpoints, redo, and crash-recovery snapshot semantics.
- [Relationship Occurrence Persistence Design Spec](relationship-persistence-design-spec.md) owns declared/inverse relationship commitment and persistence semantics.
- Descriptor and relationship-conformance specifications own schema inheritance, declared/inverse classification, and relationship policy semantics.
- A future transaction-record/audit specification will own durable transaction-history holons, if MAP introduces them.

## 2. Core runtime model

A `TransactionContext` is MAP’s transaction-scoped execution surface. It owns the mutable runtime state needed to execute one bounded unit of work:

    TransactionContext
      TxId
      lifecycle state
      host commit-ingress guard
      bootstrap-provisioning authorization
      Space manager
      Nursery
      TransientHolonManager

Runtime mutation, staging, validation, and commit must flow through `TransactionContext`. MAP must not introduce parallel mutation, lookup, or commit surfaces that bypass the Reference Layer and transaction lifecycle policy.

A transaction establishes local semantic coherence over its available read basis. It does not establish a globally serializable DHT snapshot.

## 3. Scoped state and reference binding

| Runtime state or reference | Scope | Owner |
| --- | --- | --- |
| `TransientHolonManager` | Transaction | One `TransactionContext` |
| Nursery | Transaction | One `TransactionContext` |
| `TransientReference` | Transaction | Its owning transient manager |
| `StagedReference` | Transaction | Its owning Nursery |
| Holons cache | MAP Space | Its `HolonSpaceManager` |
| `SmartReference` | MAP Space | Its `SpaceReadHandle` |

`TransientReference` and `StagedReference` are transaction-bound because their referenced holons can be dereferenced only through the pools of their owning transaction.

`SmartReference` is Space-bound, not transaction-bound. It resolves immutable saved holons and cacheable relationship state through a `SpaceReadHandle`.

Ordinary reference operations remain self-resolving. Callers must not pass transaction contexts into ordinary reference reads or writes merely to compensate for reference binding.

### 3.1 Reference Layer capability matrix

`HolonReference` is the ordinary caller-facing handle. It dispatches an
operation to its transient, staged, or saved reference variant without making
the caller branch on backing lifecycle state. Bound runtime references do not
cross a transport boundary directly; wire values are bound to references at
ingress and runtime results are projected at egress.

| Capability | `TransientReference` | `StagedReference` | `SmartReference` |
| --- | --- | --- | --- |
| Resolution owner | Owning transaction's `TransientHolonManager` | Owning transaction's Nursery | Owning MAP Space's `SpaceReadHandle` |
| Ordinary holon and property reads | Yes | Yes | Yes; immutable saved state is resolved through the Space cache/read path |
| Named relationship read | Yes; reads the transaction-local authored relationship map | Yes; reads the transaction-local authored relationship map | Yes; definitional declared membership may use the Space cache, while non-definitional and inverse membership is read fresh |
| All-relationship read | Yes; transaction-local authored map | Yes; transaction-local authored map | Yes; combines the same eligibility policy for each available outbound relationship |
| Property and relationship mutation | Yes | Yes, subject to lifecycle and descriptor policy | No; saved state is immutable |
| Stage or commit directly | No; it may be supplied to `stage_new_holon` | Commit candidate only; it is already staged | No |
| Supply a clone model | Yes; preserves in-progress authored state without requiring a descriptor | Yes; preserves in-progress authored state without requiring a descriptor | Yes; requires a descriptor and copies only declared relationships |

Semantic cloning is not an ordinary reference mutation. The destination
`TransactionContext` owns transient allocation and invokes the source
reference only to produce its phase-specific clone model. The detailed clone rule
is specified in [§8](#8-semantic-cloning-and-staging).

The relationship-read rows are read-policy statements, not authoring policy.
Direct relationship authoring uses the source's effective declared contract.
Inverse relationship occurrences are materialized by Commit from declared
relationship persistence; they are not independently authored input.

## 4. Public and private transactions

### 4.1 Public transactions

A public transaction is manager-addressable: another component may later resolve its `TxId` to resume, mutate, commit, recover, or otherwise coordinate that specific transaction.

Public transactions are registered in the owning Space’s `TransactionManager`.

Use a public transaction when:

- a client command later identifies the transaction by `TxId`;
- an ordinary host/guest dance session reconstructs the transaction by `TxId`;
- the transaction may outlive the immediate call stack; or
- later lifecycle work may independently address that transaction.

Public constructors are:

    TransactionManager::open_public_transaction(...)
    TransactionManager::open_public_transaction_with_id(...)

### 4.2 Private transactions

A private transaction is a bounded internal execution frame. Its context is passed directly through one operation and cannot later be retrieved by `TxId`.

Private transactions are not registered in the `TransactionManager`.

A private transaction still has a `TxId` for tracing, diagnostics, and dance-envelope correlation. Its `TxId` is not a lookup capability.

Use a private transaction when:

- its context is passed directly to all participating operations;
- it cannot be resumed, committed, or externally mutated later;
- it exists only for a bounded internal operation; and
- it is discarded when that operation completes.

The initial private use case is restricted saved-cache resolution:

    TransactionManager::open_private_restricted_cache_read_transaction(...)
    TransactionManager::open_private_restricted_cache_read_transaction_with_id(...)

## 5. Saved-reference resolution and cache-read frames

A `SmartReference` resolves saved state through its `SpaceReadHandle`.

On a cache hit, the Space cache returns the immutable saved holon or eligible relationship collection.

Saved-holon reads check the holon cache before creating a private restricted cache-read transaction; a cache hit requires no frame. Named and all-relationship reads currently create a fresh private restricted frame before consulting the relationship cache, including on cache hits. These frames remain unregistered. A frame may create transient request and response holons needed by the ordinary dance path, but it may not stage or commit changes.

A restricted cache-read frame:

- does not borrow another transaction’s Nursery;
- does not borrow another transaction’s transient manager;
- does not mutate staged state;
- is not registered or externally addressable; and
- is dropped when its read completes.

This permits reuse of the normal host/guest dance path without exposing or modifying arbitrary in-flight public transaction state.

## 6. Host/guest transaction projection

Dances may project transaction-scoped transient and staged state between host and guest when the invoked work requires it.

For an ordinary public transaction:

1. The initiating side identifies the public transaction by `TxId`.
2. The receiving side binds or reconstructs the corresponding public context.
3. Staged and transient pools are projected through the dance boundary as required.
4. The response projects resulting transaction-scoped state to the caller.

For a private restricted cache-read transaction:

1. The host creates a private restricted frame.
2. Its `TxId` is carried only for dance correlation.
3. The guest creates a matching private restricted frame directly from the envelope.
4. Only that frame’s transient request/response state is projected.
5. Neither side registers the frame or exposes it for subsequent lookup.

The detailed dance protocol, wire types, and command ingress behavior remain owned by the Commands and Dances specifications.

## 7. Lifecycle and operation policy

Transaction lifecycle policy distinguishes ordinary public work from restricted cache-read work.

| Operation class | Public transaction | Private restricted cache-read transaction |
| --- | ---: | ---: |
| Read saved holon or relationship | Yes | Yes |
| Create or update transient request/response holon | Yes | Yes |
| Stage holon | Yes | No |
| Mutate staged holon | Yes | No |
| Validate commit candidates | Yes | No |
| Commit | Yes | No |
| External host mutation ingress | Yes, while permitted | No |

The host commit-ingress guard prevents external request mutations from racing in-flight commit ingress. It is a host-concurrency guard, not a general distributed-isolation mechanism.

`bootstrap_provisioning` is a narrowly scoped host-authorized exception for first Core Schema Space provisioning. It does not relax ordinary transaction or reference invariants outside that bootstrap operation.

Command-specific lifecycle enforcement is specified by the Commands specification.

## 8. Semantic cloning and staging

Semantic cloning is destination-transaction-owned:

    TransactionContext::clone_holon(&source)

The destination context creates the resulting transient holon. The source reference supplies a `HolonCloneModel` through its variant implementation; `HolonReference` delegates without imposing shared descriptor policy.

A source may be saved, staged, or transient and may originate in another transaction or MAP Space. The resulting clone belongs to the destination transaction.

Clone-model construction preserves version, original identity, and authored properties, and excludes validation outcomes, staging metadata, and commit metadata. Relationship handling depends on the source phase:

- `TransientReference` and `StagedReference` preserve their current authored relationship state without requiring a descriptor. In-progress holons may precede their descriptors during bootstrap; downstream validation and relationship persistence constraints still apply.
- `SmartReference` requires a described saved source and copies only effective declared relationship collections, including both definitional and non-definitional declared relationships. It omits inverse collections exposed by saved-state navigation. Clone inclusion and cache eligibility are separate policies.

No separate ungoverned clone API or alternate state representation is required. This phase distinction does not authorize direct inverse relationship authoring.

Staging is different. Transient-to-staged transfer preserves authored transient input, including incomplete or invalid input, so Commit validation can diagnose it. Staging is not semantic cloning.

Loader assembly may use ungoverned staged relationship writes while the import's own descriptor contracts are incomplete. Before any candidate node or relationship is persisted, Commit assesses every live candidate against the completed graph. It resolves each candidate's descriptor once for validation, then requires every nonempty authored relationship collection to be licensed by that descriptor's effective declared relationship contract. Inverse names and unknown names both produce blocking `RuleViolation` findings with code `UndeclaredRelationship`; no target-descriptor lookup or materialized inverse-index inference participates. Empty collections are ignored. Missing or ambiguous descriptors retain the existing `NoDescriptor` finding. Other contract-resolution errors abort assessment without installing partial outcomes.

Any blocking finding rejects the entire persistence-candidate set before writes. Removing the offending occurrences allows a fresh validation pass and corrected retry. This authored-state check belongs to Commit candidate validation, not general validation of saved navigation surfaces, which legitimately expose materialized inverses.


## 9. Relationship-read policy

Relationship cache eligibility follows relationship mutability semantics:

- Definitional declared relationship membership is version-bound with the immutable saved source and is eligible for Space-scoped cache reuse. Inverse collections are never cached, regardless of their descriptor’s definitional flag.
- Non-definitional relationship membership may change without a new source version and is not eligible for indefinite reuse.
- Named and all-relationship reads must apply one coherent cache policy.

Named reads check the eligible-collection cache before descriptor resolution, including during recursive semantics resolution. A hit returns the sealed collection immediately. On a miss, the service result is fetched and sealed before eligibility is resolved for insertion, with cache locks released. Recursive classification may decline insertion while still reusing existing cache entries; the kernel structural-relationship eligibility rules remain applicable.

All-relationship reads enumerate the source’s available outbound relationship names and assemble their results through named reads, retaining the returned collection handles. Descriptor-discovery recursion guards end before these named reads apply cache policy. This path does not additionally fetch the full persisted relationship map. In both request-local and Space-scoped caches, only definitional declared membership is reusable; non-definitional and inverse membership is read fresh. Returned saved collections are sealed against mutation.

Outbound relationship discovery is source-oriented. Declared and inverse outbound relationship availability is determined from the source holon type’s effective relationship contract. Discovering whether a source occurrence is declared or inverse must not require traversal of the requested relationship target.

Relationship descriptor semantics and persistence outcomes remain owned by the relationship specifications.

## 10. Local coherence and distributed limits

MAP transactions provide a local execution and semantic-validation boundary. They do not guarantee:

- a globally stable DHT snapshot;
- serializable ordering across agents;
- global uniqueness;
- absence of concurrent conflicting writes; or
- atomic commitment across independent MAP Spaces or Holochain write authorities.

Remote state may advance between reads. Commit and relationship-persistence processing must therefore use their explicit conflict, retry, and coordination rules rather than assuming database-style global snapshot isolation.

## 11. Invariants

- A transient or staged reference resolves only through its owning transaction.
- A SmartReference resolves saved state through its owning MAP Space.
- Public `TxId` values are transaction-manager lookup capabilities.
- Private `TxId` values are correlation identifiers, not lookup capabilities.
- A private transaction must never become accidentally registered.
- The transaction registry must not accumulate entries for private internal frames.
- Cache reads must not borrow or mutate another transaction’s transient or staged state.
- Saved-source clone models must never include inverse relationship occurrences; transient and staged clones preserve in-progress state for downstream enforcement.
- A saved descriptor need not reside in the same transaction or MAP Space as the holon it describes.
- Local transaction validation does not imply global DHT snapshot or serializability guarantees.

## 12. Open design questions

- Specify complete lifecycle transitions, cancellation, recovery, and terminal-state behavior.
- Specify proactive cleanup policy for terminal public transaction registry entries.
- Define a separate persistent transaction-record/audit model.
- Define future invalidation or subscription semantics for non-definitional relationship caching.
- Define distributed coordination for relationship commitments spanning multiple write authorities.
- Reconcile source-owned inverse relationship discovery with physical descriptor indexes and schema-loading order.
