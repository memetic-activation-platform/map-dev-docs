# MAP Client Security Design Specification

**Version:** 0.1

**Date:** 2026-11-14

**Status:** Architectural ownership and required guarantees approved; minimum local trust/authorization contract remains open. No implementation or production-readiness claim.

## 1. Authority and scope

MAP Client Security owns the shared authentication and authorization model for MAP client installations: trusted execution boundaries, credential/capability lifecycle, principal/author/executor/delegation resolution, and security assurance. Its scope crosses webview, native host and embedded conductor/guest boundaries; client security does not mean frontend-only enforcement.

[Agent Spaces](../agent-spaces/agent-spaces-design-spec.md) owns Local Sovereign Constitution, sovereign association semantics and lifecycle outcomes. Client Security authenticates and enforces their exercise. It does not grant a human identity or sovereignty, impose external identity recognition, define AgentSpace ontology, or implement transaction/validation semantics.

Adjacent authorities remain distinct:

| Concern | Owner |
| --- | --- |
| AgentSpace domain policy, eligibility and lifecycle | Agent Spaces design |
| Public runtime execution and transport/domain binding | Commands, Dances and runtime specifications |
| Commit acceptance and configured semantic constraints | [Commit validation](../validation/commit-validation-design-spec.md) and descriptor/type-system specifications |
| Write authority, physical commitment, conflicts and persistence recovery | [Transactions](../transactions/transactions-design-spec.md) and [relationship persistence](../transactions/relationship-persistence-design-spec.md) |
| Cross-space trust and communication | TrustChannel and related owning specifications; not required for initial local constitution |

Security admission, semantic validity and durable commitment are separate decisions. None substitutes for another. This specification states target contracts; the [implementation plan](map-client-security-impl-plan.md) owns staged delivery and evidence.

## 2. Identity and authority concepts

| Concept | Meaning |
| --- | --- |
| Human | Initiates personal constitution and exercises legitimate installation control |
| PersonAgent | Resulting semantic sovereign principal; not the device or author key |
| HolochainAgent | Cryptographic author of Holochain operations |
| Device/installation | Execution and credential-custody environment |
| Constitution authorization | Narrow permission to perform eligible initial constitution |
| Executor | Runtime component performing authorized operations |
| Delegation | Authority granted to an executor or other actor, within an explicit scope |
| HolonSpace | Persistent container; its sovereign role is defined by Agent Spaces |

A supplied principal ID, Space ID, AgentPubKey or bootstrap flag is an assertion, not sufficient authorization evidence. Localhost transport, key possession and UI-only restrictions do not independently establish human authorization. A cryptographic author is not automatically a PersonAgent principal.

## 3. Trusted enforcement

Authorization MUST be resolved and enforced at trusted execution boundaries. Every reachable privileged ingress must be covered, including supported IPC, native calls and conductor/zome ingress. A trusted UI interaction can initiate a request but cannot replace backend authorization. The coordinator/integrity division must preserve the owning validation architecture; descriptor-dependent semantics must not be moved into integrity validation by implication.

The supported deployment must explicitly identify trusted components, credentials and code, permitted callers, untrusted inputs, protected resources, threat assumptions and residual risks. Development and packaged origin/permission configurations must not be treated as interchangeable security evidence. Possession of a valid transport credential does not automatically authorize every semantic operation.

The exact initial local trust boundary and admissible evidence of deliberate human initiation remain open in §8. Neither universal distrust of the installation nor blanket trust in every local process is approved by this specification.

## 4. Constitution authorization

For the Agent Spaces self-constitution policy, authorization MUST:

- Bind explicit human initiation through trusted Welcome to a backend-authorized request.
- Be restricted to the eligible unclaimed installation/Space and the operations needed for constitution.
- Exclude arbitrary callers and prevent out-of-scope use and replay that could create another successful acquisition.
- Establish durable authorization binding the resulting principal to permitted execution.
- Retire acquisition-only privileges durably after successful completion, including across restart.

Constitution admission must integrate with shared commitment/conflict handling so that authorized competing requests cannot yield conflicting successful acquisitions. Security checks alone do not supply persistence atomicity or concurrency safety.

An installation-bound single-use capability is a candidate, not an approved new capability framework. Existing MAP/Holochain authentication, signing and authorization mechanisms should be reused where they satisfy the contract. Issuance, custody, scope, invocation, consumption/retirement and interruption behavior must be specified before usable credentials are enabled.

## 5. Post-constitution execution and restart

Ordinary operations require a resolved principal or valid delegation, operation-specific authorization and the runtime/domain preconditions defined by the consumer. Constitution does not authorize every operation or turn acquisition credentials into a permanent administrative bypass. A caller-supplied bootstrap flag or assertion that provisioning occurred cannot restore privileges.

Ordinary restart requires valid retained authorizing credentials and compatible durable authorization evidence. It reconstructs authority for the existing principal without reissuing initial acquisition privileges. Missing credentials or unverifiable authorization MUST fail closed unless an independently approved recovery protocol applies. The space-management cache Session is not by itself an authenticated security session.

Credential compromise may allow misuse of technically valid credentials. Their possession does not establish continued presence or intent of the original human. Evidence formats must not unnecessarily preclude future approved recovery.

## 6. Evidence and production readiness

Client Security owns the meaning of authorization evidence and its binding to principal, author/executor, resource and permitted operation. Shared persistence owns reliable storage and commitment; consumers define domain completion predicates. No particular evidence holon, generic audit journal or completion-marker format is selected here. A durable marker alone cannot make partial acquisition writes atomic.

Local Sovereign Constitution is a production-oriented authority model. Production readiness is a separate assurance conclusion for a concrete supported implementation and threat model. It requires evidence protecting issuance/custody, trusted invocation, scoped and single-use or equivalent acquisition enforcement, durable authorization, privilege retirement, restart and relevant local attack surfaces. Unverified guarantees and limitations must be explicit; completion of a document or transport handshake is not security assurance.

## 7. Bounded initial capability and later capabilities

The minimum local capability provides the contracts in §§3–6 for one supported initial installation configuration. It does not require a universal authorization engine or completion of every future security capability. Required guarantees for that configuration cannot be waived because broader features are deferred.

External identity proofing, legal/biological uniqueness attestation, SSI/DID infrastructure, general policy/delegation management, adaptive risk/step-up frameworks, cross-device sovereign recovery, credential-loss/compromise recovery and general rotation/revocation are not prerequisites for initial personal constitution. Collective admission, governance and interspace TrustChannels retain their separate ownership.

## 8. Open minimum local contract

Before enabling the initial privileged paths, resolve:

1. The supported deployment, trusted computing boundary and local attacker assumptions.
2. Who may initiate constitution, how deliberate Welcome initiation is authenticated at the backend, and how alternate ingress is denied or equivalently checked.
3. Issuance authority, credential custody, resource/operation binding and replay/consumption rules using existing mechanisms where sufficient.
4. Principal/author/executor binding after acquisition, durable privilege retirement and valid-credential restart authorization.
5. The evidence required for assurance, and the interface to shared commitment for conflicts, interrupted consumption, lost responses and completed acquisition.

These are implementation-security decisions, not a reopening of the Agent Spaces sovereignty model. Credential encodings, internal APIs, diagnostics and interaction details may be resolved during implementation within the approved contract.

## 9. Earlier security material

This specification supersedes overlapping client identity, local authentication/authorization, credential lifecycle and enforcement claims in the October 2025 [MAP Security Model draft](../../mapp-dev/map-security-model.md). In particular, device-equals-Agent wording, mandatory Agreement-based initial authorization and frontend-only enforcement are not authoritative. Historical descriptions of particular keystore or security capabilities do not establish implementation guarantees.

The [Catalist security migration proposal](../map-catalist-security-models.md) remains a proposal, not an authorization contract or initial constitution dependency. Broader interspace, governance and risk material remains subject to its owning specifications and future reconciliation; this document does not approve it wholesale.
