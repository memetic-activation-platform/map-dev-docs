# Relationship Occurrence Persistence Design Spec

> **Status: Work in progress.** The ownership boundary is established, but the
> proposed cross-space completion and repair model still requires review
> against the transaction and storage designs.

## 1. Purpose

This specification defines the persistence invariant connecting a declared relationship occurrence
to its materialized inverse occurrence.

It covers:

- the semantic commit unit for declared and inverse directions;
- locally resolvable inverse materialization;
- deferred non-local inverse realization;
- source-chain conflict reload, revalidation, and retry/failure; and
- the boundary between commit processing and storage.

It does not define descriptor inheritance, relationship conformance, or physical SmartLink
encoding.

## 2. Authority and related specifications

Relationship descriptor structure and conformance are governed by:

- [`schema-design-spec.md`](../type-system/schema-design-spec.md); and
- [`descriptor-semantics-rules.md`](../type-system/descriptor-semantics-rules.md).

Relationship occurrence metadata and ordering are governed by
[`relationship-constraints-design-spec.md`](../type-system/relationship-constraints-design-spec.md).

Physical persistence is governed by:

- [`storage-layer-design-spec.md`](../guest/storage-layer-services/storage-layer-design-spec.md);
  and
- [`holons-shared-objects-layer-design-spec.md`](../architecture/holons-shared-objects-layer-design-spec.md).

This document owns Space-local relationship-bucket semantic authority, Commit-local write
authority, cross-direction preparation and persistence, concurrency retry, and the cross-Space
deferral boundary.

## 3. Terms

For a declared relationship descriptor `R`:

- a **declared occurrence** is an authored source-to-target relationship occurrence of `R`;
- an **inverse descriptor** is the target reached through `R.HasInverse`, required for every
  concrete declared relationship descriptor;
- an **inverse occurrence** is the target-to-source materialization described by that inverse
  descriptor; and
- a **relationship commitment** is the durable outcome for the declared occurrence and every
  inverse occurrence whose source belongs to the committing MAP Space.

A **Space-local relationship bucket** is identified by
`(source_holon_identity, relationship_descriptor_identity)`. The source holon's stewarding Space
is semantically authoritative for that bucket. Cardinality, duplicates, ordering, and other
collection policies are evaluated over the prospective value of each affected authoritative
bucket.

A MAP Space is a stewardship and containment unit. It is not by definition a single Holochain
write authority. A **Commit-local bucket** is one whose every write is authored by the single
Holochain cell and source chain executing this Commit. Semantic authority and write authority
coincide only where that condition holds — typically a single-cell Space, or a Space partitioned
so that each bucket has exactly one authoring cell. Where a bucket is stewarded by a Space but
written by more than one cell, this document's atomicity and conflict-retry guarantees do not
apply to it, and any rule requiring authority over its complete prospective value is a multi-cell
aggregate decision that fails closed with `RelationshipCoordinationRequired`.

The declared occurrence is the authoritative authored fact. Its inverse occurrence is a derived,
materialized traversal fact and is not authored independently.

Materialization reverses stored declared occurrences, not virtual values produced by applying
descriptor inheritance to the declared direction. An inverse traversal reads the resulting
materialized inverse occurrences, subject only to the kernel-selected inheritance rule of the
inverse relationship itself.

## 4. Space-local core invariant

For every concrete declared relationship, the declared occurrence and every inverse occurrence
whose source belongs to the committing MAP Space form one logical relationship commitment.

Commit must not report an unqualified successful commitment after persisting only the declared
direction and silently omitting required local inverse work. An inverse whose source belongs to
another MAP Space is outside this transaction's commitment and follows the deferred cross-space
model in Section 6.

A local relationship commitment has one of these outcomes:

1. **Complete**: the declared occurrence and every required local directional occurrence are
   durably persisted.
2. **Failed**: the declared occurrence cannot be accepted or required local directional work
   cannot be prepared or persisted.

An implementation may use different type names, but it must preserve these semantic distinctions.
Deferred realization of an inverse whose source belongs to another Space is outside this local
outcome; it does not make a complete local commitment pending or incomplete.

## 5. Local inverse materialization

Before accepting a declared relationship update, commit processing must evaluate every applicable
relationship constraint against each affected Commit-local bucket:

    committed occurrences in the Commit-local bucket
    - removed or superseded occurrences in this Commit
    + staged declared occurrences in this Commit
    + derived inverse occurrences whose source is Commit-local

This includes local source-side and local inverse-side cardinality, duplicate, ordering, endpoint,
and other applicable relationship constraints. If an applicable rule requires a complete bucket
that is not Commit-local, Commit rejects with `RelationshipCoordinationRequired` rather than
constructing that bucket from DHT reads. A failing constraint rejects the declared update before
commit succeeds. This scope does not establish open-world or cross-space cardinality.

When both directional sources are Commit-local — stewarded in the committing Space and written
by the source chain executing this Commit — commit processing must:

1. validate the declared occurrence against its relationship descriptor;
2. resolve the required inverse descriptor;
3. prepare the declared and inverse directional occurrences;
4. assign or preserve shared semantic occurrence identity where the relationship model requires
   it; and
5. persist both directions in one normal-order zome-call transaction.

Step 5 is what the single-source-chain condition buys. A normal-order zome call is atomic over one
source chain, so it makes the paired declared and inverse writes succeed or fail together only
when both land on that chain. A directional source outside this Commit's write authority is not
covered by that guarantee, and which case applies depends on where that source lives:

- **same Space, same Commit write authority**: persist both directions atomically, as above;
- **same Space, a different cell**: the Section 4 local commitment covers this inverse but cannot
  presently be completed, so Commit fails closed with `RelationshipCoordinationRequired`. It is
  neither deferred nor silently one-sided;
- **another Space**: the inverse is outside this commitment and follows the deferred model in
  Section 6.

The prepared plan contains the normalized declared operations, their paired local inverse
operations, resolved source anchors, and the read basis required to detect source-chain conflicts.
Internal SmartLink operations consume this plan; they do not infer inverses or expose a parallel
public persistence path.

Failure to prepare or persist either required direction fails the relationship commitment. The
runtime must not leave an apparently successful one-sided local relationship.

Adding, removing, or replacing a declared occurrence applies the corresponding inverse change as
part of the same commitment.

## 6. Deferred cross-space inverse materialization

When the source of a required inverse occurrence belongs to another MAP Space, that inverse is
outside the declaring transaction's validation and persistence scope. The declaring commit must
not wait for remote inverse materialization, push a mutation into the other Space, reserve remote
relationship capacity, or report the declared relationship as pending or transitional because of
the deferred inverse.

The declared forward occurrence may commit normally once all applicable constraints within its
Commit-local authority and commit scope pass. The committing Space does not claim that remote
inverse constraints have passed.

Cross-space inverse materialization follows MAP's pull model. The receiving Space may later
discover or obtain the declared occurrence and determine whether and how to materialize, expose,
or recognize its inverse occurrence under that Space's current descriptor, activation, governance,
and relationship constraints.

A later constraint violation in the receiving Space does not retroactively invalidate the
successfully committed forward occurrence. It is a Runtime Recognition, governance,
reconciliation, or repair concern of the receiving Space.

This deferral applies only to ordinary remote inverse realization. If an applicable acceptance
rule requires a multi-cell aggregate decision, the local Commit cannot establish that proposition
from DHT reads. It rejects with the `RelationshipCoordinationRequired` finding until a future
Relationship Coordination capability can supply the required authority.

## 7. Cross-space identity continuity

An identity mechanism used to establish the declared occurrence, including an `ExternalId` or
trust-channel mapping, must remain available to a receiving Space that later performs pull-driven
inverse materialization.

The runtime must not treat identity resolution as a forward-only exception that makes a deferred
inverse unrecoverable.

## 8. Deferred inverse recognition and coordination

The declaring commit does not create or own pending remote inverse work. A future cross-space
pull, Runtime Recognition, governance, reconciliation, or repair design must define how a
receiving Space detects, diagnoses, retries, or resolves deferred inverse materialization without
creating duplicate live occurrences.

That future work must preserve semantic occurrence identity where the relationship model requires
it. Physical storage actions may receive new storage identities as defined by the storage layer.
Future Relationship Coordination must separately define protocols for rules that require
authoritative multi-cell aggregate assessment. Ordinary DHT reads do not form a serializable
cross-cell snapshot and must not be presented as one.

## 9. Commit and storage boundary

Commit processing owns:

- descriptor-aware relationship validation;
- inverse descriptor resolution;
- preparation of every local directional occurrence;
- reload and revalidation of affected Commit-local buckets after a source-chain conflict; and
- the complete or failed outcome for the relationship commitment within the committing cell's
  authority, or an explicit coordination rejection when that authority is insufficient.

The storage layer owns persistence of the already prepared local directional occurrences. It does
not infer missing inverse semantics from relationship names or repair deferred cross-space inverse
work implicitly.

Descriptor facades expose `HasInverse`, `InverseOf`, and related metadata but do not perform commit
or repair orchestration.

Source-chain conflict handling covers concurrent writes to the committing cell's own chain; it is
not a cross-cell concurrency protocol. When persistence reports such a conflict, Commit discards
the stale prepared relationship portion, reloads every affected Commit-local bucket, reconstructs
the prospective view, and reruns all applicable relationship validation before preparing a new
plan. It may retry within a bounded policy. Exhausting that policy or receiving a non-retryable
persistence error is an operational failure, distinct from semantic rejection. A retry must never
reuse a report assessed against the stale buckets.

## 10. Diagnostics

A failed relationship commitment should identify:

- the declared relationship descriptor;
- source and target identity;
- semantic occurrence identity when available;
- the required inverse descriptor;
- the failed phase; and
- whether local retry is possible.

Source or loader adapters may enrich the failure with authored provenance.

## 11. Out of scope

This specification does not select:

- a trust-channel protocol;
- a cross-space pull or inverse-materialization protocol;
- a retry schedule;
- a Runtime Recognition outcome model;
- SmartLink encoding;
- relationship ordering metadata;
- the `Allow`/`Block`/`Cascade` pairwise deletion matrix and cascade-closure algorithm; or
- user-interface remediation workflows.

Those designs must preserve the distinction between a complete or failed local commitment and
separately deferred remote inverse realization.
