# MAP Client Security Design Specification

**Version:** 0.4

**Date:** 2026-11-15

**Status:** Architectural ownership, required guarantees and trusted packaged-Welcome boundary approved; remaining local authorization mechanisms and assurance gates are open. No implementation or production-readiness claim.

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

**No reachable privileged ingress may bypass the authorization required for the operation.** Checks are complementary; every layer need not redundantly evaluate the same policy. Technical permission to invoke a function is distinct from permission to effect a MAP sovereign operation.

| Boundary | Responsibility |
| --- | --- |
| Tauri/Rust host | Trusted client request admission and protection of host-held credentials/capabilities |
| Holochain conductor | Application connection authentication, signing and technical zome-call authorization under the deployed Holochain version |
| Coordinator/runtime | MAP-specific operation authorization and orchestration of applicable domain checks, including ingress callable without Welcome |
| Integrity validation | Its deterministic validation responsibilities under the owning integrity/validation architecture |
| Shared Commit validation | Descriptor-aware semantic assessment under the [Commit validation specification](../validation/commit-validation-design-spec.md); not caller authorization |
| Transactions/persistence | Commitment, conflicts, atomicity and recovery under their owning specifications; not security admission |

A trusted UI interaction can initiate a request but cannot replace backend authorization. Descriptor-dependent semantics must not be moved into integrity validation by implication.

The supported deployment must explicitly identify trusted components, credentials and code, permitted callers, untrusted inputs, protected resources, threat assumptions and residual risks. Development and packaged origin/permission configurations must not be treated as interchangeable security evidence. Possession of a valid transport credential does not automatically authorize every semantic operation.

A deliberate, explicit Welcome interaction expresses human intent; backend verification establishes that the request meets the approved local authorization contract. An ordinary click does not cryptographically prove human identity or intent. The trusted packaged-Welcome boundary and its exclusions are approved in §8.1; concrete mechanisms and assurance evidence remain open in §8.2. Independent native/OS confirmation is not required under that boundary.

## 4. Constitution authorization

For the Agent Spaces self-constitution policy, authorization MUST:

- Bind an explicit Welcome interaction expressing human intent to a backend-authorized request under the approved local assurance assumptions; do not claim that the interaction alone proves identity or intent.
- Be restricted to the eligible unclaimed installation/Space and the operations needed for constitution.
- Exclude arbitrary callers and prevent out-of-scope use and replay that could create another successful acquisition.
- Establish durable authorization binding the resulting principal to permitted execution.
- Retire acquisition-only privileges durably after successful completion, including across restart.

Retirement means that a subsequent constitution cannot succeed in establishing another sovereign association, even if a technically authorized HolochainAgent can still invoke the relevant zome function. Do not equate deletion of a capability grant with removal of the cell author's inherent invocation authority; verify author-grant and capability behavior against the deployed Holochain version before relying on it.

Durable acquired state and applicable lifecycle/authorization checks must prevent a second successful constitution through Welcome or direct zome ingress. An idempotent retry may recover the original completed result; it must not create another association. Constitution admission must integrate with shared validation and commitment/conflict handling for competing requests, replay and lost responses. Client Security owns authorization and privilege retirement, Agent Spaces owns eligibility/completion semantics, and shared validation/persistence owns its enforcement and commitment guarantees. Security checks alone do not supply persistence atomicity or concurrency safety. No new credential or entry type is implied.

An installation-bound single-use capability is a candidate, not an approved new capability framework. Existing MAP/Holochain authentication, signing and authorization mechanisms should be reused where they satisfy the contract. Issuance, custody, scope, invocation, consumption/retirement and interruption behavior must be specified before usable credentials are enabled.

## 5. Post-constitution execution and restart

All privileged MAP operations require appropriate authorization: a resolved principal or valid delegation, operation-specific authority and the consumer's runtime/domain preconditions. This general architectural rule does not require CS-L1 to deliver arbitrary Dancer authorization or general delegation. CS-L1 provides only the authority needed for initial constitution, opening the same acquired AgentSpace and the explicitly identified local operations in its [AS2 lifecycle acceptance scenario](map-client-security-impl-plan.md#minimum-operation-inventory). Unsupported privileged paths must remain unavailable or otherwise protected; deferral never grants a bypass.

Constitution does not authorize every operation or turn acquisition credentials into a permanent administrative bypass. A caller-supplied bootstrap flag or assertion that provisioning occurred cannot restore privileges.

Ordinary restart requires valid retained authorizing credentials and compatible durable authorization evidence. It reconstructs authority for the existing principal without reissuing initial acquisition privileges. Missing credentials or unverifiable authorization MUST fail closed unless an independently approved recovery protocol applies. The space-management cache Session is not by itself an authenticated security session.

Credential compromise may allow misuse of technically valid credentials. Their possession does not establish continued presence or intent of the original human. Evidence formats must not unnecessarily preclude future approved recovery.

## 6. Evidence and production readiness

Client Security owns the meaning of authorization evidence and its binding to principal, author/executor, resource and permitted operation. Shared persistence owns reliable storage and commitment; consumers define domain completion predicates. No particular evidence holon, generic audit journal or completion-marker format is selected here. A durable marker alone cannot make partial acquisition writes atomic.

Local Sovereign Constitution is a production-oriented authority model. Production readiness is a separate assurance conclusion for a concrete supported implementation and threat model. It requires evidence protecting issuance/custody, trusted invocation, scoped and single-use or equivalent acquisition enforcement, durable authorization, privilege retirement, restart and relevant local attack surfaces. Unverified guarantees and limitations must be explicit; completion of a document or transport handshake is not security assurance.

## 7. Bounded initial capability and later capabilities

CS-L1 applies the general contracts in §§3–6 to one explicitly supported installation configuration and the bounded initial AS2 lifecycle: constitution, opening/restarting the same acquired Space and its specifically inventoried minimum local operations. The implementation plan maps those operations to a concrete acceptance scenario; it does not admit an unlimited category of ordinary operations. General Dancer authorization, arbitrary delegation, WeSpace roles, TrustChannels and a universal operation-policy engine are later work. Every privileged path actually exposed by the supported configuration must nevertheless be authorized or unavailable. Required guarantees cannot be waived because broader features are deferred.

External identity proofing, legal/biological uniqueness attestation, SSI/DID infrastructure, general policy/delegation management, adaptive risk/step-up frameworks, cross-device sovereign recovery, credential-loss/compromise recovery and general rotation/revocation are not prerequisites for initial personal constitution. Collective admission, governance and interspace TrustChannels retain their separate ownership.

## 8. Minimum local trust and authorization contract

### 8.1 Approved trusted packaged-Welcome boundary

The initial CS-L1 trust boundary is approved as follows:

1. Trust the integrity of the legitimate packaged MAP application, including its approved Welcome code, native Rust host, embedded Holochain conductor and protected signing facilities, operating within an uncompromised OS environment.
2. The OS account is an environmental trust assumption, not authorization for every process under that account. Other local processes, unrelated WebViews, remote content, caller-supplied identifiers and bootstrap flags remain untrusted.
3. Trusted packaged Welcome code is distinct from arbitrary or externally supplied content it displays. Such content MUST NOT inherit constitution authority. Appropriate WebView isolation, origin restrictions and command permissions must enforce that distinction; sharing a display or execution environment does not make content approved code.
4. Compromise of trusted packaged Welcome code, the native host or the OS is outside the initial assurance claim. Attacks through exposed interfaces, unauthorized local callers and untrusted content remain in scope. The integrity assumption does not waive verification of the isolation and admission controls protecting these interfaces.
5. Credentials and authorization enforcement MUST remain within the approved backend trust boundary. Reusable constitution authority MUST NOT be exposed to frontend JavaScript.
6. Constitution requires explicit Welcome initiation and backend verification of the authorized request path. This does not establish cryptographic proof of human identity or intent.
7. Independent native/OS confirmation is not required. Do not introduce independent native confirmation or a new credential framework unless implementation investigation demonstrates that this approved boundary cannot otherwise be enforced. Any such finding must identify the concrete enforcement gap rather than reopen the sovereignty model.

This approves the trust boundary, not a claim that the current implementation enforces it or is production-ready. AS2's bounded lifecycle scope and the resolved D2 Local Sovereign Constitution decision remain unchanged.

### 8.2 Remaining implementation contract gates

Before enabling the initial privileged paths, resolve within §8.1:

1. The concrete supported installation configuration, isolation/origin/permission controls and finite operation inventory mapped to AS2 integration entrypoints/tests.
2. How explicit Welcome initiation is bound to backend verification of the authorized request path, and how untrusted content, unauthorized local callers and alternate ingress are denied or equivalently checked without inheriting constitution authority.
3. Issuance authority, backend credential custody, resource/operation binding and replay/consumption rules using existing mechanisms where sufficient.
4. Principal/author/executor binding for the bounded lifecycle, durable retirement despite remaining technical author invocation rights, idempotent retry/replay handling and valid-credential restart authorization.
5. Assurance evidence under the approved boundary, including its exclusions and in-scope interface/content attacks, and the shared commitment interface for conflicts, interrupted consumption, lost responses and completed acquisition.

These remaining gates concern implementation and assurance, not whether to adopt the trusted packaged-Welcome boundary or Local Sovereign Constitution. Credential encodings, internal APIs, diagnostics and interaction details may be resolved during implementation within the approved contract.

### 8.3 Initial packaged execution boundary

The initial supported client configuration is a packaged macOS application on Apple Silicon, using packaged assets, one embedded conductor and one provisioned MAP cell, with persistent signing facilities held by the native backend. Development-server builds, test keystores, configuration overrides and additional privileged windows are outside this configuration. The initial assurance target must name the tested OS/build revision; a package's minimum OS version is not evidence of testing every compatible OS release.

Conductor administration and the initial privileged Dance transport remain in process. The supported configuration exposes neither admin nor app WebSocket listeners and provides no generic signing command or reusable conductor token to frontend JavaScript. Persisted listener configuration must be assessed before conductor startup can restore external interfaces; incompatible stores require explicit reconciliation, preserving existing identities and content. This is a bounded first-client configuration, not a requirement that all future MAP Dances execute through the Rust host.

Approved Welcome executes in a dedicated packaged WebView whose command permissions and backend admission bind the expected window and local page. It imports no materialized visualizer code or externally supplied executable content. Untrusted content must not inherit its native command access. Ordinary development Canvas/loader execution remains a distinct configuration and supplies no packaged security assurance.

Before constitution authorization and durable principal binding are implemented, the Welcome request path remains disabled and generic privileged client ingress is unavailable in this configuration. Internal provisioning continues through existing staging, assessment and Commit; security admission does not alter diagnostics, partial persistence, remediation or resubmission. Holochain author invocation rights remain technical rights, not semantic authorization. Credential protection, request scope, retirement and retained-credential restart retain their CS2–CS5 contracts.

## 9. Earlier security material

This specification supersedes overlapping client identity, local authentication/authorization, credential lifecycle and enforcement claims in the October 2025 [MAP Security Model draft](../../mapp-dev/map-security-model.md). In particular, device-equals-Agent wording, mandatory Agreement-based initial authorization and frontend-only enforcement are not authoritative. Historical descriptions of particular keystore or security capabilities do not establish implementation guarantees.

The [Catalist security migration proposal](../map-catalist-security-models.md) remains a proposal, not an authorization contract or initial constitution dependency. Broader interspace, governance and risk material remains subject to its owning specifications and future reconciliation; this document does not approve it wholesale.
