# Test Harness Design Spec

This document is normative for the **dance test** harness: fixture support, execution support, and
the step adders. It does not apply to conductor tests, which use no fixture, no `TestReference`, and
no executor — see the [Conductor Test Framework](conductor-test-spec.md) and the routing rule in the
[Testing Strategy](../map-holons-testing-strategy.md).

---

## What a TestReference Is

A **TestReference** is an immutable fixture-time contract identifying a step's source holon and
expected holon state. It is reusable across steps, but is neither a runtime handle nor a unique
logical-holon identity.

The enclosing `DanceTestStep` carries the operation and step-level expectations; see
[Step Parameters and Expected Outcomes](#step-parameters-and-expected-outcomes).

---

## Structural Overview

A TestReference consists of **two role-specific components**:

    TestReference
      ├─ SourceSnapshot    (execution input)
      └─ ExpectedSnapshot  (execution expectation)

These two components use a shared lifecycle vocabulary but serve **distinct purposes**.

---

## Snapshot Identity

Snapshots are identified by a dedicated alias rather than by the reference itself:

    pub type SnapshotId = TemporaryId;

Both `SourceSnapshot::id()` and `ExpectedSnapshot::id()` derive their `SnapshotId` from the
underlying `TransientReference`'s temporary id. Snapshot lookup maps use `SnapshotId`;
logical-holon maps use `FixtureHolonId`.

---

## Shared Lifecycle Vocabulary

All fixture-time holon intent is expressed using a shared descriptive enum.

    #[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd, Hash)]
    pub enum TestHolonState {
        Transient,
        Staged,
        Saved,
        SavedLookup,
        Abandoned,
        Deleted,
    }

This enum is:

- Descriptive, not behavioral
- Interpreted differently depending on context (source vs expected)
- Used by fixture support and execution support

`SavedLookup` marks a partial saved-holon expectation originating from lookup. It stays partial
through subsequent staging and Commit; see [Saved-Content Comparison Semantics](#saved-content-comparison-semantics).

---

## SourceSnapshot — Execution Input

`SourceSnapshot` identifies the holon an executor should operate on and its intended lifecycle
state. Its snapshot identity locates a recorded runtime handle.

    pub struct SourceSnapshot {
        snapshot: TransientReference,
        state: TestHolonState,
    }

The embedded snapshot is immutable. When authoring a later step, adders select a new source from
the logical holon's current fixture head; they do not redirect an existing token.

---

## ExpectedSnapshot — Execution Expectation

`ExpectedSnapshot` describes the expected holon content and lifecycle state after execution.

    pub struct ExpectedSnapshot {
        snapshot: TransientReference,
        state: TestHolonState,
    }

The snapshot is always present and remains an immutable historical expectation. For `Deleted`,
it conveys identity only; its content must not be compared.

Its identity also locates recorded results through `ResolveBy::Expected`. Fixture-time chaining
and relationship construction instead follow the logical holon's current head; see
[Head Selection](#head-selection-where-it-actually-lives).

---

## TestReference — Combined Contract

    pub struct TestReference {
        source: SourceSnapshot,
        expected: ExpectedSnapshot,
    }

Both fields are private. `TestReference::new` is crate-internal, and `FixtureHolons` owns token
minting by harness convention. TestCase authors pass opaque tokens to adders; harness code
reads the halves through snapshot, identity, and reference accessors.

---

## Tight Chaining Rule (Essential Invariant)

The design enforces **tight chaining**:

> The ExpectedSnapshot produced by step *N* is the conceptual SourceSnapshot for step *N+1*.

This chaining is fixture-time and intent-based.

In Rust terms, this is supported by an explicit conversion:

    impl ExpectedSnapshot {
        pub fn as_source(&self) -> SourceSnapshot {
            SourceSnapshot::new(self.snapshot.clone(), self.state)
        }
    }

`as_source` is total — it never panics, and it does not itself decide whether a `Deleted`
expectation is a usable source. That decision belongs to `FixtureHolon`; see
[Deleted Heads and Source Fallback](#deleted-heads-and-source-fallback).

---

## Fixture-Time Head Advancement (Commit Semantics)

Commit advances fixture heads internally. Authors keep using their existing tokens; later adders
follow the logical holon's current head rather than copying a stale embedded snapshot.
[Commit Semantics](#commit-semantics-fixture-time) defines the result tokens and advancement rules.

## Why FixtureHolons Exist

Snapshots describe step-level holon intent. `FixtureHolons` separately tracks which snapshots
belong to the same logical holon and which snapshot is its current head.

---

## FixtureHolon — Logical Holon Identity (Fixture-Time)

A **FixtureHolon** is the mutable fixture-time representation of one logical holon across steps.
It owns lifecycle state and head selection and is internal to fixture support.

### Rust Structure

    #[derive(Clone, Debug)]
    pub struct FixtureHolon {
        head_snapshot: ExpectedSnapshot,
        last_live_snapshot: ExpectedSnapshot,
        pub staging_source: StagingSource,
        pub saved_identity: Option<SavedIdentity>,
    }

Logical identity is the **map key**, not a field: `FixtureHolonId` is a `Uuid` newtype under which
`FixtureHolons` stores the entry. Lifecycle state is likewise **derived**, not stored — `state()`
returns `head_snapshot.state()`.

    pub enum StagingSource {
        NewRoot,
        Version { source: FixtureHolonId },
    }

    pub enum SavedIdentity {
        OwnNode,
        AliasOf(FixtureHolonId),
    }

---

### Field Semantics

- `head_snapshot` is the current expected content and lifecycle state, advanced by adders and Commit.
- `last_live_snapshot` supplies the source when the head is `Deleted`.
- `staging_source` records what staging established: `NewRoot` for a create or independent clone,
  or `Version` naming the saved logical holon used as the source. It validates declarations;
  it must never infer an update's disposition from fixture mutations.
- `saved_identity` is initially `None`. Commit records `OwnNode` for a newly persisted node or
  `AliasOf(source)` when an unchanged or graph-only update reuses the source node.

Typical progressions are `Transient` → `Staged` → `Saved`, `Saved` → `Deleted`, and
`Staged` → `Abandoned`. Staging from a saved version creates a separate logical candidate;
a partial lookup source produces a candidate whose committed expectation remains `SavedLookup`.

### Deleted Heads and Source Fallback

A deleted holon remains a legitimate source for later steps, including delete-after-delete.
`FixtureHolon` selects the last live snapshot through `resolve_snapshot_as_source`; adders must
not duplicate this fallback:

    fn resolve_snapshot_as_source(&self) -> SourceSnapshot {
        if self.head_snapshot.state() == TestHolonState::Deleted {
            self.last_live_snapshot.as_source()
        } else {
            self.head_snapshot.as_source()
        }
    }

---

## FixtureHolons — Fixture-Time Registry

`FixtureHolons` is the **sole authority** for logical fixture holons, token minting, head
advancement, and snapshot-to-holon interpretation: no adder or executor mints a token or advances
a head itself. It is neither a runtime registry nor an execution cache and is not exposed to
executors. It validates fixture contracts; runtime semantic validation and execution assertions
belong to the execution phase.

### Rust Structure

    pub struct FixtureHolons {
        fixture_context: Arc<TransactionContext>,
        pub tokens: Vec<TestReference>,
        pub holons: BTreeMap<FixtureHolonId, FixtureHolon>,
        pub snapshot_to_fixture_holon: BTreeMap<SnapshotId, FixtureHolonId>,
    }

`FixtureHolons::new(context)` binds the registry to its fixture transaction.
`copy_fixture_snapshot` clones transient snapshots into that transaction, preserving incomplete
or undescribed content for later validation without weakening saved-holon clone semantics.

### Field Semantics

- `tokens` is the append-only ledger of authored step tokens, used for diagnostics and executor
  coordination. It excludes Commit result tokens (fresh snapshots registered by head advancement)
  and head relabelings (tokens reusing an existing snapshot).
- `holons` maps each logical `FixtureHolonId` to its current fixture representation.
- `snapshot_to_fixture_holon` maps registered historical snapshot identities to their owners,
  keeping older tokens usable after head advancement.

---

## Head Selection — Where It Actually Lives

Fixture-time head selection belongs to `FixtureHolons`:

1. Read the token's **expected** `SnapshotId`.
2. Find its owner through `snapshot_to_fixture_holon`.
3. Select that logical holon's current head.

The expected half identifies the holon produced by the step. For a staged version or clone,
the source half identifies the original holon, so following it would select the wrong owner.

For the next operation's source, `resolve_snapshot_as_source` converts the head, substituting
the last live snapshot if deleted. For a relationship target, the adder embeds the current head
in the new expected graph.

Execution-time resolution instead selects a token half through `ResolveBy` and looks up its
recorded runtime handle in `ExecutionHolons`: ordinary inputs use `Source`; relationship targets,
Commit declarations, and rejected-candidate assertions use `Expected`.

---

## Commit Semantics (Fixture-Time)

Commit expectations declare each candidate's persistence disposition. The harness checks these
against independently observed runtime behavior; neither side may be inferred from the other.

### Declared Dispositions

Each live candidate in an expected `Complete` or supported `Incomplete` attempt declares one
`ExpectedDisposition`:

| Disposition | Persistence intent | Resulting identity |
| --- | --- | --- |
| `NewRoot` | A create or an independent clone writes a new node | New, with no inherited lineage |
| `NoAction` | An unchanged update writes nothing | None; after `Complete`, later steps resolve to the saved source |
| `GraphOnly` | Graph changes are anchored to the existing node | The saved source's identity, lineage untouched |
| `NewVersion` | A version-producing update writes a new node version | New, with the staging source as its single predecessor |

Fixture mutations never rewrite declarations. A property write promotes a graph-only candidate
to a new version; a stale `GraphOnly` declaration must fail as a disposition mismatch.

Authors declare through two expectation types, with operational-error expectations attached
independently of disposition:

- `ExpectedCommitCandidate` — one live candidate's disposition and expected *new* operational
  errors
- `ExpectedRetryParticipant` — a retained committed entry eligible only for a relationship retry.
  It has no disposition and must produce no further saved result

The create-only convenience derives `NewRoot` when staging established only new roots.
Any saved-version staging provenance requires explicit declarations and otherwise fails at
authoring time.

### Commit Responsibilities

For an expected `Rejected` Commit — and for an attempt expected to fail at the command level — the
adder takes no declarations, mints no result tokens, and leaves fixture heads unchanged;
`VerifyCommitRejection` checks the retained candidates separately.

Otherwise `commit` validates the whole expectation set **before advancing anything**, so a
rejected expectation leaves fixture state untouched:

1. Every `Staged` head is declared exactly once
2. Each declared disposition is compatible with the candidate's `staging_source`
3. Retry participants already have saved heads with a resolved `saved_identity`, and are disjoint
   from the live candidates

It prepares declarations in **author order** for deterministic results and diagnostics. For each
candidate that advances:

1. Clones the candidate's head snapshot, leaving the original untouched
2. Authors the expected persisted lineage from the declared disposition
3. Mints one result TestReference — **including for `NoAction` under `Complete`**
4. Advances `FixtureHolon.head_snapshot` to the result snapshot and records `saved_identity`

Head advancement and result-token behavior are attempt-specific:

| Candidate or participant | Expected status | Head after attempt | Result token |
| --- | --- | --- | --- |
| `NewRoot`, `GraphOnly`, `NewVersion` | `Complete` or supported `Incomplete` | Advances to persisted expectation | Minted and bound to saved result |
| `NoAction` | `Complete` | Advances to saved-source expectation | Minted and bound to saved source |
| `NoAction` | `Incomplete` | Remains `Staged` | None |
| Relationship-retry participant | Either | Existing saved head retained | None |

A retained `NoAction` candidate must be declared again on retry. Persisted operations between
attempts use its saved-source token. Commit tokens remain internal; authors keep using
prior tokens. Preparation must leave all existing tokens and source snapshots untouched.

The result's state is `Saved`, except that a candidate staged from a partial `SavedLookup` source
remains `SavedLookup`, so a stub never becomes a supposedly complete saved-content snapshot.

### Staged Content and Expected Persisted Content Are Distinct

Staging a new version or an independent clone clears copied predecessor lineage, matching the
runtime staging surface. Commit then authors the difference between staged content and the
expected persisted snapshot:

- `NewRoot` — no inherited lineage; an independent clone has neither predecessor nor successor
- `NewVersion` — exactly the saved source used for staging becomes the predecessor
- `NoAction` and `GraphOnly` — the source version's existing predecessor is retained untouched

For A → B, reusing B preserves its predecessor A; producing C from B gives C predecessor B.
These changes apply to fresh result snapshots, never to the saved source.

### Node Ownership and Aliasing

A `NoAction` or `GraphOnly` result realizes a node another logical holon owns. Several `Saved`
heads may therefore realize one persisted node, and `count_saved()` counts only non-deleted
`OwnNode` heads. Comparing multiple saved snapshots against one reused node is sound only because
graph-only mutations are non-definitional by construction; saved-content comparison ignores
non-definitional edges, so the aliased snapshots cannot disagree about the content it checks.

### Correspondence at Execution

The executor retains staged handles across dispatch and matches saved results by **committed
identity**, never by key: versions may share a key. Each saved result must have exactly one
claimant; unmatched, duplicated, or ambiguous correspondence fails clearly. Observed dispositions
come from staged state, recorded source identity, and saved-result membership.

Declared-versus-observed mismatches precede saved-count and snapshot assertions. A `NoAction`
result consumes no saved entry; under `Complete`, its token binds directly to the recorded saved source.

### Operational Errors

Operational errors are independent of disposition, of command-level failure, and of semantic
validation findings. They accumulate on a staged entry across attempts, so expectations compare
**newly appended occurrences** against a per-attempt baseline, preserving kind and multiplicity: a
repeated failure of the same kind is another occurrence, not a duplicate to be collapsed. An
omitted expectation asserts that no new errors appeared, and that assertion applies to every
retained entry, not only to declared candidates.

A retry in a still-open transaction may present zero live candidates and produce no saved results
while relationship persistence still runs against previously committed entries and appends another
error. Such an entry keeps its existing saved mapping. Each attempt, including a corrected retry,
requires a fresh expectation set.

#### Worked Retry Example

1. Declare unchanged update `U` as `NoAction` and create `C` as `NewRoot`. Expect `Incomplete`
   because `C`'s node commits but a relationship write fails. `U` keeps its staged head with no
   result token; `C` advances to a saved head.
2. Correct the relationship input. For the retry, declare `U` again as `NoAction` and `C` as
   an `ExpectedRetryParticipant`, with no new operational errors expected.
3. Expect `Complete`: `U` advances and binds to its saved source; `C` retains its saved mapping
   and produces no further saved result or result token.

### Supported Partial Outcomes

An `Incomplete` attempt is supported when Pass 1 succeeds and relationship persistence then fails.
A failure before a candidate reaches a saved outcome is a distinct case: it is **unsupported**,
must never be classified as no action, and establishes nothing about whether a node write
occurred. The four dispositions above cannot represent it, so the harness must report it as an
unsupported outcome naming the candidate.

---

## Step Parameters and Expected Outcomes

`DanceTestStep` carries operation parameters and expectations beyond the token's source and
expected snapshot: command errors, Commit status, dispositions, operational errors, and
persisted-graph subjects. Expected failure is a step outcome, not a holon lifecycle state;
a matching failure is a successful test outcome and execution continues.

---

## Saved-Content Comparison Semantics

`MatchSavedContent` compares saved roots by:

1. essential holon content
2. exact definitional relationship presence/member agreement

Implications:

- non-definitional persisted edges, including commit-generated inverse
  SmartLinks, are intentionally ignored by saved-content equality
- definitional relationship members are matched by saved holon identity where
  the harness has recorded the committed realization
- each saved fixture holon is still compared independently as its own root, so
  nested member content is not recursively revalidated from every relationship
  occurrence

Because Commit authors the expected lineage of a version-producing result, saved-content
comparison applies after a version-producing Commit as well as after a create.

Saved-lookup stubs remain a harness-specific special case for holons created
outside the fixture ledger. A stub is matched by key only and is excluded from saved-content
comparison, so a partial snapshot is never treated as complete.

Direct persisted-graph assertions cover materialized inverses, non-definitional changes,
duplicate suppression, and exact target collections for lineage and other named relationships.
Per-target occurrence checks cannot reject undeclared extra targets; exact collections reject
extra or duplicate members. Exact checks require all expected members to be known, so use
partial checks for shared inverse collections unless all contributing sources are known,
as in an isolated runtime. These checks read fresh persisted relationships and remain separate
from saved-content equality, which covers essential content and definitional membership.
