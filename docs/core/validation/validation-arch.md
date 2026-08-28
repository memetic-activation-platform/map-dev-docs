# MAP Validation Architecture

> **Status:** Draft
>
> This document maps MAP's validation landscape: the guarantees MAP distinguishes, the layers in
> which they can be established, and the boundaries between them. It is not the authoritative
> design for a particular validation consumer or execution path.

---

## 1. Purpose and authority

MAP validation is not one mechanism. Different questions require different context, authority,
determinism, and time horizons. This architecture defines the boundaries among those questions so
that an implementation does not accidentally treat one kind of result as another.

This document is authoritative for:

- the validation guarantee model and layer boundaries;
- the distinction between validation layers and validation subjects;
- the separation of semantic rules from their implementations;
- the broad role of constraints, `ValidationBindings`, results, evidence, Dances, and Promise
  Theory; and
- the direction of future validation evolution.

It is intentionally not authoritative for detailed algorithms, Rust types, handler registries,
rule sequencing, persistence decisions, or schema shapes. Those decisions belong to focused
specifications:

| Concern | Authoritative document |
|---|---|
| Semantic, descriptor-aware decision to persist a staged Nursery | [Commit Validation Design Specification](commit-validation-design-spec.md) |
| Incremental delivery of Commit Validation | [Commit Validation Implementation Plan](commit-validation-impl-plan.md) |
| Validation-extension schema shape and its Core boundary | [Validation Extension Schema Design Specification](validation-schema-design-spec.md) |
| Descriptor conformance and effective-contract semantics | [Descriptor-Kernel Semantic Rules](../type-system/descriptor-semantics-rules.md) |
| Relationship persistence and cross-Space inverse materialization | [Relationship Occurrence Persistence Design Specification](../transactions/relationship-persistence-design-spec.md) |
| Deterministic Integrity-Zome validation | [PVL Design Specification](pvl-design-spec.md) |

Future Runtime Recognition, agreement, and social-validation specifications must refine this
architecture without collapsing their guarantees into Commit or peer validity.

## 2. Architectural principles

### 2.1 Validation is layered

No single environment has enough context or authority to establish every useful proposition about
MAP data. A concern belongs in the innermost layer that can evaluate it correctly and safely. As a
rule moves outward, its dependencies tend to become less bounded, less deterministic, more
temporal, more social, or more dependent on open-world state.

### 2.2 Validation may use declarative rules, but not every requirement is a `ValidationRule`

Validation rules give durable semantic identities to fixed or contextual checks such as
required-property presence, value-kind conformance, and relationship endpoint compatibility. A
configured definitional invariant such as length, range, or cardinality is instead a first-class
`Constraint` holon attached to its type definition. A stable rule identity does not require a
single uniform execution mechanism.

The architecture distinguishes:

- descriptor resolution and other bootstrap mechanics;
- single-subject rule evaluation;
- bounded aggregate validation;
- fixed platform invariants; and
- temporal governance or evolution policy.

`ValidationRule` is therefore a declarative mechanism, not a universal representation of every
validation requirement. Focused specifications decide which concerns are configured constraints,
which remain rule holons or fixed algorithms, how they are scheduled, and which context is
sufficient to execute them.

### 2.3 `ValidationRule` is a semantic object, not an implementation

A `ValidationRule` names the semantic condition. A Rust function, WASM module, Dance, or human
review process is an implementation capable of evaluating that condition in a particular context.
This separation permits one rule identity to acquire different implementations or evidence paths
over time without changing its meaning. It does not imply that every layer uses, discovers, or
executes `ValidationRule` holons.

| Architectural layer or concern | `ValidationRule` role |
|---|---|
| Commit Validation | Evaluates effective `Constraints` and applicable `ValidationBindings` / `ValidationRule` identities, as specified by the Commit Validation Design Specification. |
| Runtime Recognition | May later reuse rule identities or execution machinery, but has no defined `ValidationRule` execution contract yet. Its focused design must establish one if needed. |
| Application, agreement, and social layers | May adopt `ValidationRule` where declarative, inspectable commitments are useful; they may also enforce workflow, authorization, or governance requirements through their own models. |
| Descriptor kernel and other fixed Core semantics | Implement fixed semantic algorithms and invariants. They need not be represented by executable rule holons. |
| Peer Validation Layer | Makes **no use** of schema-authored `Constraint` holons, `ValidationRule` holons, `ValidationBindings`, descriptor lookup, rule registries, wrapper dispatch, or descriptor-aware `ValidationResult` objects. It executes its separate fixed descriptor-independent Integrity contract compiled into the DNA. |

### 2.4 Validation is declaratively extensible

Open-ended design is a cornerstone of MAP. Core owns the declarative vocabulary that defines
Commit acceptance through two complementary declarative surfaces: the type-system-owned
`Constraints` relationship for configured invariants, and `ValidationRule` / `ValidationBindings`
for remaining Commit-relevant rule commitments. The one-way Validation Schema extension carries
implementations, result/evidence, `Validate`, rule sets, and non-Commit rule families.
`ValidationBindings` is the Core relationship through which a type makes compatible non-constraint
rule commitments applicable. Its exact Commit selection semantics are defined by the Commit
Validation Design Specification.

### 2.5 Validation results are contextual evidence

A result records that a rule was evaluated over an identified subject in a particular context and
produced an outcome. It does not, by itself, establish that the rule was appropriate, the context
was complete, the implementation was trustworthy, or the result is still current.

## 3. Validation guarantee model

MAP distinguishes the following guarantees.

### 3.1 Descriptor-relative structural validity

Descriptor-relative validation establishes that a subject conforms to its applicable effective
descriptor contract. Depending on scope, this can include required and permitted properties,
value-kind and value constraints, local relationship typing, and instantiability.

It does not establish that the descriptor is currently recognized, socially legitimate, or active
in every AgentSpace.

### 3.2 Peer admissibility

Peer validation establishes that a DHT operation satisfies the deterministic integrity rules
compiled into the DNA. It is the responsibility of PVL. It does not establish descriptor-relative
conformance, current type activation, agreement compliance, or open-world graph claims.

### 3.3 Commit validity

Commit validation establishes whether a complete staged Nursery may become persisted MAP state.
It is a semantic acceptance decision for the local Commit, not peer consensus and not Runtime
Recognition. The Commit Validation Design Specification defines this guarantee, including its
descriptor-aware rule traversal and bounded relationship scope.

### 3.4 Runtime Recognition

Runtime Recognition establishes whether the current AgentSpace recognizes descriptors
and data committed by other agents under its current activation and governance state.

Recognition is:

- temporal;
- revocable;
- AgentSpace-specific; and
- governance-mediated.

It must not be conflated with Commit validity or immutable peer admissibility. Committed data may
remain structurally valid while becoming unrecognized in an AgentSpace; recognition may also need
to account for later cross-Space information or governance decisions.

### 3.5 Agreement and access validity

Agreement-layer validation establishes whether an access, projection, or behavior is permitted by
the applicable agreement, role, capability, and TrustChannel context. It belongs outside PVL and
does not alter the historical fact that a version passed Commit validation.

### 3.6 Social and attested validity

Social processes may establish that an agent or recognized process asserted, reviewed, approved,
disputed, or resolved a claim. These results are important evidence but are not deterministic peer
validation.

## 4. Validation layers

Validation layers answer **where** a concern executes and **what context is available**. They are
orthogonal to validation subjects, which answer **what** is being assessed.

| Layer | Typical context | Primary guarantee |
|---|---|---|
| Peer Validation Layer | DHT operation, Integrity context, fixed bounded dependencies | Peer admissibility |
| Commit | complete staged Nursery, local transaction services, bounded current-Space view | Commit validity |
| Runtime Recognition | runtime reads, active descriptors, AgentSpace governance state | Current recognition |
| Application | workflow, form, command, or Dance context | Domain-specific decision support |
| Trust and Agreement | agreements, roles, capabilities, TrustChannels | Access and projection validity |
| Attestation and Social | agents, attestations, review and dispute processes | Social evidence and resolution |

### 4.1 Peer Validation Layer

PVL is the fixed deterministic validation contract in the Integrity Zome. It validates the native
write envelope and bounded integrity requirements. PVL does not resolve descriptors, execute
descriptor-kernel semantics, select `Constraints` or `ValidationBindings`, consult runtime
activation, or query open-world graph state. The PVL Design Specification is authoritative for its
rules, dependency model, and resource limits.

### 4.2 Commit

Commit is the semantic persistence boundary. Every producer—including loader, API, Dance,
migration, and programmatic callers—may stage content differently, but no producer owns a separate
semantic acceptance gate. The Commit Validation Design Specification defines the complete-Nursery
algorithm and its failure/persistence semantics.

### 4.3 Runtime Recognition

Runtime Recognition applies activation, governance, diagnostic, and recognition policy when data
is read, navigated, projected, or used. A future focused specification must define its inputs,
outcomes, caching/revalidation policy, and treatment of later cross-Space inverse conflicts.

### 4.4 Application, agreement, and social layers

Applications may add workflow, form, command, publication, and domain-specific checks. Agreement
and TrustChannel layers may assess membership, roles, capabilities, disclosure permissions, and
projection policies. Social layers may incorporate human review, steward approval, attestations,
reputation, and dispute resolution. None of these should be presented as peer consensus merely
because they produce a validation-like outcome.

## 5. Validation subjects and scope

The validator hierarchy is a decomposition by subject, not a hierarchy of authority. A broad
orchestrator may delegate to narrower subject validators, but lower-level validators should not
need to navigate upward into their containing object.

| Subject level | Typical governing semantic surface |
|---|---|
| Holon | its governing HolonDescriptor |
| Property | the applicable PropertyType |
| Value | the selected ValueType |
| Declared relationship | the DeclaredRelationshipType |
| Multi-hop pattern | a bounded occurrence/graph scope |

The Commit Validation Design Specification defines the exact inputs, dependency direction, rule
selection, and canonical traversal for these subjects. In particular, it keeps intrinsic value
validation independent of the property and holon that happen to contain that value.

## 6. Rule applicability and implementations

`Constraints` communicates configured definitional invariants. `ValidationBindings` communicates
the remaining declarative rule applicability. Both effective collections may accumulate through
ordinary descriptor relationship semantics. Constraint applicability is declared by concrete
constraint types through `ApplicableToDescriptorTypes` and evaluated against the constrained
descriptor's `Extends` lineage; malformed attachment, the handling of unbound rules, and the
failure behavior of unsupported attached constraints and active rules are defined by focused Commit and schema
specifications.

Implementation profiles may include:

- built-in static Rust dispatch for the initial Commit capability;
- future Dance-mediated or WASM execution;
- diagnostic or advisory execution; and
- human or social review.

An implementation profile must state its context requirements, determinism bounds, authority, and
evidence semantics. No profile may silently strengthen a result beyond what its available context
supports.

## 7. Dance and Promise Theory alignment

Validation aligns naturally with MAP's behavioral model without requiring every validation action
to be a Dance today.

- A `Constraint` describes and configures a definitional invariant.
- A `ValidationRule` describes a fixed or contextual condition to assess.
- A type's `Constraints` and `ValidationBindings` declare the corresponding commitments applicable
  to its governed subjects.
- A `ValidationImplementation` or future `Validate` Dance supplies a capability to enact that
  assessment in a particular layer.
- A `ValidationResult`, receipt, attestation, or governance decision can record evidence of the
  enactment.

This vocabulary clarifies the difference between a rule's semantic identity, an executor's
capability, and the evidence produced by execution. The Validation Extension Schema Specification
owns the corresponding schema model.

## 8. Results, evidence, and time

Commit validation uses transient runtime state and diagnostics to decide persistence. That state is
not automatically part of persisted holon content. Other layers may persist evidence when a
separate design establishes why it is useful and how it is interpreted.

Possible durable evidence includes signed import reports, steward approvals, external audits,
publication certification, deferred-review completion, and dispute records. Receipt verification
can establish that an assertion was made over a particular input; it cannot establish semantic
correctness unless the receipt's acceptance rule is independently enforceable.

## 9. Evolution and focused follow-on designs

This architecture anticipates, but does not specify:

- Runtime Recognition design and implementation plans;
- dynamic `ValidationImplementation` activation and selection;
- Dance-based dispatch and multiple execution engines;
- validation profiles and reusable rule sets;
- persisted validation evidence and receipts; and
- application, agreement, and social-validation integrations.

The architectural constraint is preservation of guarantee boundaries. A later design may reuse
rule identities or execution machinery, but it must not treat a Commit verdict as present-tense
recognition, treat recognition as a persistence gate, or treat social evidence as deterministic
peer admissibility.

## 10. Summary

MAP validation is layered and contextual. PVL establishes deterministic peer admissibility; Commit
Validation decides whether a staged Nursery may persist; Runtime Recognition decides whether a
current AgentSpace recognizes committed data; and agreement or social layers establish their own
distinct propositions.

`Constraint` identities and configuration, `ValidationRule` identities, `ValidationBindings`,
implementations, and results provide a common vocabulary across those layers. Focused
specifications—not this architecture document—define the algorithms and data contracts that
realize each guarantee.
