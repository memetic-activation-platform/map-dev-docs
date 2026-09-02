# Validation Dependency Gravity

> **Status:** Draft

## 1. Purpose and authority

Dependency gravity is the principle that a validation concern belongs at the innermost execution
boundary that has enough bounded, authoritative context to evaluate it reliably. A rule moves
outward as its dependencies become less bounded, more temporal, more open-world, or more social.

This document is authoritative for:

- the dependency-placement principle;
- the seven dependency classes; and
- the placement decision test.

It does not define MAP's validation layers, individual rule semantics, handler contracts, or final
execution placement. Those authorities are:

- [Validation Architecture](validation-arch.md) for current layer names, guarantees, and
  boundaries;
- [PVL Design Specification](pvl-design-spec.md) for descriptor-independent Integrity rules;
- [Commit Validation Design Specification](commit-validation-design-spec.md) for complete-Nursery
  semantic assessment;
- [Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md) for `DS-*`
  invariants;
- the focused value and relationship constraint specifications for configured semantics; and
- future focused Runtime Recognition, agreement, trust, and social-validation designs.

The classes below are dependency classes, not enforcement categories. A `Constraint`,
`ValidationRule`, or fixed kernel invariant may fall into a class without acquiring a new semantic
identity or implementation mechanism.

## 2. Placement principle

Place a concern only where all information required to decide it is:

1. available through the boundary's allowed dependencies;
2. bounded enough for that boundary's determinism and resource limits;
3. authoritative for the proposition being asserted; and
4. stable for the duration of the decision.

Do not pull descriptor runtime, transaction services, remote reads, governance, or social judgment
inward merely to execute more rules earlier. Earlier execution is useful only when it can establish
the same proposition reliably.

The shared descriptor-aware validation framework is a reusable mechanism. It supplies typed
contexts, registries, handlers, collectors, and reports to consumers that already own an
appropriate bounded context. It is not itself an authority layer and does not enlarge the
dependencies available to PVL, Commit, or another consumer.

## 3. Boundary examples

### 3.1 Peer Validation Layer

PVL receives a DHT operation, fixed DNA constants, and only the deterministic bounded dependencies
permitted by Holochain Integrity callbacks. It establishes peer admissibility. It does not resolve
runtime descriptors, execute schema-authored bindings or constraints, invoke coordinator services,
or claim transaction-wide semantic validity.

The PVL specification owns its actual representation, lifecycle, provenance, resource, and
dependency rules. This document does not infer PVL responsibilities from descriptor semantics.

### 3.2 Commit

Commit receives the complete Nursery, transaction-scoped runtime services, and bounded state for
which the committing cell has authority. Its context includes all staged holons, even when a
particular aggregate owner such as a Schema holon was not itself staged. Commit can therefore
evaluate prospective persisted-plus-staged Schema components, affected Commit-local relationship
buckets, and other bounded transaction claims before any write.

The Nursery is data within Commit's bounded context, not an independent validation layer. The
public persistence decision belongs to Commit.

### 3.3 Runtime and outer contexts

Runtime Recognition may use current activation and AgentSpace governance state. Agreement and
TrustChannel evaluation may use roles, capabilities, disclosures, and counterpart commitments.
Social processes may use attestations, review, dispute, and open-world information. Their future
focused designs must state exactly what proposition each outcome establishes.

## 4. Declarative rules and execution

A semantic commitment and its executor are separate:

- a configured `Constraint` is an intrinsic mandatory part of a type definition;
- a `ValidationRule` gives a stable identity to a non-constraint commitment when the schema model
  calls for one;
- a fixed kernel or PVL invariant need not be represented by a `ValidationRule`; and
- a Rust handler, WASM implementation, Dance, or review process executes only in a context that
  satisfies the commitment's dependency class.

Descriptor-driven dispatch begins only after the caller has resolved the governing descriptor and
obtained its ordinary effective products. The handler receives the narrow typed context required by
its subject. It does not perform a second lineage traversal, infer a broader snapshot, or promote an
incomplete observation to a pass.

All current Commit rules and configured constraints are blocking. Missing support for an effective
constraint or authored binding fails closed. Durable validation evidence is a separate future use
of `ValidationResult`; transient Commit assessment uses `CommitValidationReport` and
`CommitValidationViolation`.

## 5. Seven dependency classes

### Class 1 — Native structural

Inputs are the current entry or link, fixed DNA constants, and native callback metadata. The check
requires no descriptor lookup or coordinator service.

Typical placement: PVL, when the PVL specification includes the rule.

Examples include supported native encoding, fixed size bounds, and operation-shape invariants.

### Class 2 — Bounded deterministic dependencies

The check requires a fixed, explicitly bounded set of dependencies available to the Integrity
callback. Its cost and missing-dependency behavior are deterministic.

Typical placement: PVL only when the PVL specification explicitly admits the dependency pattern.

### Class 3 — Descriptor-aware local

The check requires a resolved descriptor, effective contract, configured constraint, or
`ValidationBindings` occurrence, but no transaction aggregate or runtime-governance service.

Typical placement: Commit or another descriptor-aware consumer using the shared framework.

Examples include required-property presence, native value-kind compatibility, enum membership, and
single-occurrence endpoint compatibility.

### Class 4 — Transaction and bounded aggregate

The check requires the complete Nursery or a prospective persisted-plus-staged local view. The
scope must identify exactly which aggregate, buckets, or keys are authoritative.

Typical placement: Commit.

Examples include affected-Schema aggregate invariants, Commit-local relationship
cardinality, paired local inverse preparation, and bounded key uniqueness.

Cross-Space information is not silently included. If a rule needs a remote cell to establish the
proposition, the local observation is insufficient.

### Class 5 — Runtime Recognition

The check depends on current type activation, descriptor recognition, local governance state, or
later-arriving cross-Space information.

Typical placement: Runtime Recognition.

### Class 6 — Agreement and trust

The check depends on an agreement, role, capability, TrustChannel, counterparty, disclosure policy,
or other negotiated context.

Typical placement: agreement, access, or trust processing.

### Class 7 — Social and open-world

The check depends on global absence, community judgment, attestation, governance deliberation,
dispute resolution, or another unbounded/open-world proposition.

Typical placement: social, governance, attestation, or asynchronous coordination processes.

## 6. Relationship coordination example

For a relationship update, Commit can authoritatively assess and persist the affected Commit-local
directional buckets — those whose every write is authored by the source chain executing this
Commit. It can derive the local inverse, validate both local directions, and retry after a
source-chain conflict.

Commit cannot claim that DHT reads form a serializable snapshot across cells. When acceptance
requires a multi-cell aggregate property, it records the blocking
`RelationshipCoordinationRequired` finding rather than treating missing remote information as a
pass. A future Relationship Coordination capability belongs in Class 5, 6, or 7 according to the
authority and protocol it ultimately requires.

Deferred materialization of an ordinary remote inverse is different: the local forward occurrence
may complete when every Commit-local rule passes because remote inverse realization is
outside that local relationship commitment. The relationship-persistence specification owns this
boundary.

## 7. Practical placement test

Ask the following questions in order:

1. Can the proposition be decided from the current entry or link and fixed DNA constants?
   If yes, consider Class 1 and confirm PVL actually owns the rule.
2. Does it require only a fixed bounded set of deterministic Integrity dependencies?
   If yes, consider Class 2 and confirm PVL admits that dependency pattern.
3. Does it require a resolved descriptor or effective products but no aggregate context?
   If yes, use Class 3 in a descriptor-aware consumer.
4. Does it require the complete Nursery or a named prospective local aggregate?
   If yes, use Class 4 at Commit.
5. Does it depend on current activation, recognition, or later cross-Space observations?
   If yes, use Class 5.
6. Does it depend on agreements, roles, capabilities, or TrustChannels?
   If yes, use Class 6.
7. Does it depend on global absence, social judgment, governance, or dispute resolution?
   If yes, use Class 7.

If no boundary has all required authoritative inputs, the rule is not currently decidable. Emit the
focused design's blocking coordination or unsupported outcome; do not weaken the proposition.

## 8. Summary

Dependency gravity preserves trustworthy guarantees by keeping each decision at the smallest
boundary with sufficient context. PVL establishes descriptor-independent peer admissibility;
Commit assesses the complete Nursery and bounded local aggregates; Runtime Recognition and outer
layers address increasingly temporal, negotiated, and open-world propositions. The shared
validation framework can serve several consumers without becoming a layer or changing those
authority boundaries.
