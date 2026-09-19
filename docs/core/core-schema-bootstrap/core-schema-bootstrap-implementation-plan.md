# Core Schema Bootstrap Implementation Alignment

## Audit baseline

This reconciliation compares the bootstrap design branch with map-holons
`0d0b2a84` (PR #720). The [design specification](core-schema-bootstrap-design-spec.md)
remains authoritative; this page records implementation evidence and follow-up
work rather than weakening its readiness contract.

## Delivered behavior

Conductora invokes `ensure_core_schema_space` after runtime initialization and
before window creation. The service uses the ordinary `LoadHolons` command with
an internal bootstrap transaction, archives that transaction after execution,
and requires a local-space ID before opening its ingress gate. Packaged imports
are selected by a manifest and checked against SHA-256 digests. Bootstrap
participates in the application-launcher lifecycle before base-package activation
and Canvas realization.

Commit uses the common pre-persistence assessment gate. Ungoverned loader
assembly does not authorize descriptorless persistence or inverse authoring.

## Intrinsic package scope mismatch

The current bootstrap bundle includes Core and selected extension packages.
The newer [MAP Application Launcher design specification](https://github.com/memetic-activation-platform/map-dev-docs/blob/main/docs/dahn/map-application-launcher-design-spec.md)
requires Core Schema to be the only intrinsically loaded package; ordinary
runtime imports belong to the subsequent application activation flow. The
current bundle therefore does not yet conform to that package boundary.

Follow-up implementation work must reconcile bundle generation and startup
activation with the Launcher contract, including the dependencies needed for
Canvas realization. Keep package selection manifest-driven and do not treat
bundled extension holons as Core schema declarations. This documentation PR
records the mismatch; it neither changes the bundle nor broadens the Launcher’s
intrinsic-loading contract.

## Durable readiness verification gap

In `host/conductora/src/setup/core_schema_bootstrap.rs`, the service returns
ready immediately when the runtime already has a space ID. After a new load it
checks that a space ID was injected. Its manifest reader validates package
selection and file digests; these checks do not establish the specification’s
full durable graph predicate.

The reconciliation did not establish an equivalent end-to-end predicate in a
delegated layer. Follow-up work must trace discovery and command-result handling,
then implement or demonstrate each required check: unique anchor, canonical
identity, manifest-required stable keys, expected descriptors and ownership,
materialized inverses, and release compatibility. Reuse and restart paths need
the same proof. Absence detection must also distinguish a fresh space from a
partial graph left behind before its anchor was written; an absent anchor alone
cannot authorize replay. If that distinction cannot be established, startup must
fail closed. A successful transport result or an injected space ID alone
must not be presented as that proof.

The specification also requires serialized first-origin provisioning and safe
detection of partial or competing durable state. Verify those guarantees at the
orchestration and storage boundaries before claiming recovery is complete.

## Deferred scope

Later-space spawning, qualified transport, trust provisioning, and local mirror
semantics remain future design. This documentation consolidation does not add
multi-space support or define mirror cloning.
