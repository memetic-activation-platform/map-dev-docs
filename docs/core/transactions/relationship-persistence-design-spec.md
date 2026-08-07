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
  required inverse materialization.

The declared occurrence is the authoritative authored fact. Its inverse occurrence is a derived,
materialized traversal fact and is not authored independently.

Materialization reverses stored declared occurrences, not virtual values produced by applying
descriptor inheritance to the declared direction. An inverse traversal reads the resulting
materialized inverse occurrences, subject only to the effective `InheritanceMode` of the inverse
descriptor itself.

## 4. Core invariant

For every concrete declared relationship, the declared and inverse occurrences form one logical
relationship commitment.

The runtime must not report an unqualified successful commitment after persisting only the
declared direction and silently omitting required inverse work.

A relationship commitment has one of these outcomes:

1. **Complete**: every required local directional occurrence is durably persisted.
2. **Pending remote completion**: the declared occurrence is durably persisted together with
   durable, observable work describing an inverse occurrence that cannot yet be materialized
   across a non-local boundary.
3. **Failed**: neither a complete result nor an authorized durable pending result was established.

An implementation may use different type names, but it must preserve these semantic distinctions.

## 5. Local inverse materialization

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

## 6. Non-local inverse materialization

An inverse target may be unreachable because it belongs to another holon space, agent, trust
channel, or unresolved external identity domain.

If MAP permits the declared direction to persist before that inverse can be written, commit
processing must also persist durable pending work containing enough information to:

- identify the declared occurrence;
- identify the inverse descriptor and intended inverse source and target;
- preserve the relationship occurrence identity needed for reconciliation;
- explain why materialization is pending;
- retry through an authorized resolution or trust path; and
- detect completion, permanent rejection, or conflicting state.

The operation must report pending remote completion rather than complete success.

If no authorized durable pending mechanism exists, inability to materialize the required inverse
fails the relationship commitment.

## 7. Identity resolution symmetry

An identity mechanism used to establish the declared occurrence, including an `ExternalId` or
trust-channel mapping, must be applicable to inverse preparation or retained as durable information
for later inverse completion.

The runtime must not treat identity resolution as a forward-only exception that makes the inverse
unrecoverable.

## 8. Detection, retry, and repair

Pending inverse work must be queryable and diagnosable. The runtime must support:

- deterministic retry without creating duplicate live occurrences;
- detection of stale or permanently failing work;
- reconciliation when the remote side already contains the intended inverse;
- conflict reporting when the remote state is incompatible; and
- operator-visible remediation rather than silent abandonment.

Retry preserves semantic occurrence identity. Physical storage actions may receive new storage
identities as defined by the storage layer.

## 9. Commit and storage boundary

Commit processing owns:

- descriptor-aware relationship validation;
- inverse descriptor resolution;
- preparation of both directional occurrences;
- pending-remote-work creation when authorized; and
- the complete, pending, or failed outcome.

The storage layer owns persistence of the already prepared directional occurrences and pending
records supplied to it. It does not infer missing inverse semantics from relationship names or
repair omitted commit work implicitly.

Descriptor facades expose `HasInverse`, `InverseOf`, and related metadata but do not perform commit
or repair orchestration.

## 10. Diagnostics

A failed or pending relationship commitment should identify:

- the declared relationship descriptor;
- source and target identity;
- semantic occurrence identity when available;
- the required inverse descriptor;
- the failed phase; and
- whether retry is possible.

Source or loader adapters may enrich the failure with authored provenance.

## 11. Out of scope

This specification does not select:

- a concrete pending-work holon or entry schema;
- a trust-channel protocol;
- a cross-space transaction protocol;
- a retry schedule;
- SmartLink encoding;
- relationship ordering metadata;
- the `Allow`/`Block`/`Cascade` pairwise deletion matrix and cascade-closure algorithm; or
- user-interface remediation workflows.

Those designs must preserve the complete, pending remote completion, and failed distinctions
defined here.
