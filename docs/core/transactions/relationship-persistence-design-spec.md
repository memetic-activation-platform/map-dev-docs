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
- unresolved non-local inverse work;
- retry and repair observability; and
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

This document owns only the cross-direction commit invariant.

## 3. Terms

For a declared relationship descriptor `R`:

- a **declared occurrence** is an authored source-to-target relationship occurrence of `R`;
- an **inverse descriptor** is the target reached through `R.HasInverse`, required for every
  concrete declared relationship descriptor;
- an **inverse occurrence** is the target-to-source materialization described by that inverse
  descriptor; and
- a **relationship commitment** is the durable outcome for the declared occurrence and every
  inverse occurrence whose source belongs to the committing MAP Space.

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

A relationship commitment has one of these outcomes:

1. **Complete**: the declared occurrence and every required local directional occurrence are
   durably persisted.
2. **Failed**: the declared occurrence cannot be accepted or required local directional work
   cannot be prepared or persisted.

An implementation may use different type names, but it must preserve these semantic distinctions.

## 5. Local inverse materialization

Before accepting a declared relationship update, commit processing must evaluate every applicable
relationship constraint against the prospective occurrence collection of the current MAP Space:

    locally committed occurrences
    - locally removed or superseded occurrences in this Commit
    + locally staged declared occurrences in this Commit
    + locally derived inverse occurrences whose source is in this Space

This includes local source-side and local inverse-side cardinality, duplicate, ordering, endpoint,
and other applicable relationship constraints. A failing constraint rejects the declared update
before commit succeeds. This scope does not establish open-world or cross-space cardinality.

When both endpoints are locally resolvable, commit processing must:

1. validate the declared occurrence against its relationship descriptor;
2. resolve the required inverse descriptor;
3. prepare the declared and inverse directional occurrences;
4. assign or preserve shared semantic occurrence identity where the relationship model requires
   it; and
5. persist both directions as one semantic commit operation.

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

The declared forward occurrence may commit normally once all constraints within its own MAP Space
and commit scope pass. The committing Space does not claim that remote inverse constraints have
passed.

Cross-space inverse materialization follows MAP's pull model. The receiving Space may later
discover or obtain the declared occurrence and determine whether and how to materialize, expose,
or recognize its inverse occurrence under that Space's current descriptor, activation, governance,
and relationship constraints.

A later constraint violation in the receiving Space does not retroactively invalidate the
successfully committed forward occurrence. It is a Runtime Recognition, governance,
reconciliation, or repair concern of the receiving Space.

## 7. Cross-space identity continuity

An identity mechanism used to establish the declared occurrence, including an `ExternalId` or
trust-channel mapping, must remain available to a receiving Space that later performs pull-driven
inverse materialization.

The runtime must not treat identity resolution as a forward-only exception that makes a deferred
inverse unrecoverable.

## 8. Deferred inverse recognition and repair

The declaring commit does not create or own pending remote inverse work. A future cross-space
pull, Runtime Recognition, governance, reconciliation, or repair design must define how a
receiving Space detects, diagnoses, retries, or resolves deferred inverse materialization without
creating duplicate live occurrences.

That future work must preserve semantic occurrence identity where the relationship model requires
it. Physical storage actions may receive new storage identities as defined by the storage layer.

## 9. Commit and storage boundary

Commit processing owns:

- descriptor-aware relationship validation;
- inverse descriptor resolution;
- preparation of every local directional occurrence; and
- the complete or failed outcome for the current MAP Space.

The storage layer owns persistence of the already prepared local directional occurrences. It does
not infer missing inverse semantics from relationship names or repair deferred cross-space inverse
work implicitly.

Descriptor facades expose `HasInverse`, `InverseOf`, and related metadata but do not perform commit
or repair orchestration.

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

Those designs must preserve the complete, pending remote completion, and failed distinctions
defined here.
