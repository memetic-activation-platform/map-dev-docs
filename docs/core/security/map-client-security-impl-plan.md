# MAP Client Security Implementation Plan

**Version:** 0.2

**Date:** 2026-11-14

**Status:** Planned; minimum local contract unresolved, no implementation delivery claimed.

## 1. Authority and delivery boundary

The [Client Security design specification](map-client-security-design-spec.md) owns semantics. This plan delivers reusable security capabilities independently of Agent Spaces. AS2 consumes the bounded initial local capability; it does not implement a general security framework. Completing the entire future security roadmap is not an AS2 dependency.

## 2. CS-L1 — Initial local trust and authorization

The identifier CS-L1 is a documentation work item, not a newly created GitHub issue.

### Contract gate

Resolve design §8 before enabling usable constitution credentials or the bounded privileged paths. Record one supported configuration, OS-account/host/webview assumptions, trusted components, limits of human-initiation assurance, local threats, ingress coverage, credential custody, scope/retirement and lifecycle restart checks. Approve the finite operation inventory below and map it to concrete AS2 integration tests. Keep security, semantic assessment and commitment decisions separate; D2 Local Sovereign Constitution remains resolved.

### Repository grounding and implementation

Inspect existing Tauri command/capability configuration, Holochain plugin origin/token/signing behavior, native runtime dispatch, conductor interfaces, guest session restoration and keystore integration on the actual implementation baseline. Candidate surfaces include `host/conductora/capabilities/`, `plugins/tauri-plugin-holochain/`, `src/runtime/dispatch_map_command.rs`, and `happ/crates/holons_guest/src/dances_guest/dance_adapter.rs`. Their existence is not proof of sufficient authorization.

**Inspected baseline — 2026-11-14:** map-holons `36a577c2fa5b6c78419897ecdfcca4e56b32b79b`; `host/Cargo.lock` resolves Holochain 0.7.1 and Tauri 2.12.4. Inspection of Holochain 0.7.1 `holochain_state::source_chain::SourceChain::valid_cap_grant` shows an author-access check before stored remote grants are consulted. Removing a stored grant must not be assumed to disable the author's inherent call rights. The current host issues reusable app tokens, and guest context restoration enables bootstrap mode from wire session state; neither establishes semantic constitution authority. Recheck the actual implementation revision and dependency sources when delivering CS-L1. These are inspection findings, not security-test evidence.

Reuse adequate existing mechanisms. Deliver only:

- Trusted initiation/admission and constitution-specific scope enforcement.
- Credential issuance/custody and replay or equivalent repeated-acquisition protection.
- Durable principal/execution authorization binding and acquisition privilege retirement.
- Authorization for opening/restarting the same acquired AgentSpace and only the minimum operations inventoried below; missing credentials fail closed. No general ordinary-operation or Dancer authorization delivery is implied.
- Integration with shared commitment outcomes and conflicts, without a competing persistence path.

No capability framework, general policy engine, arbitrary Dancer/delegation authorization, WeSpace role system, TrustChannel implementation, external identity service or recovery framework is implied. Any unsupported privileged path exposed by the configuration must be disabled or protected, not admitted through bootstrap authority.

### Minimum operation inventory

`AS2-Local-Lifecycle` names the proposed concrete integration acceptance scenario, not an existing implemented test. Its finite operation inventory is:

| Scenario step | Required authorization scope |
| --- | --- |
| Trusted startup provisions one unclaimed Space and packaged foundation | Existing narrowly scoped internal provisioning; no general UI bootstrap privilege |
| Welcome requests and resolves/retries constitution | Only the eligible installation/Space and complete initial acquisition operation |
| Close, restart and Open the same acquired AgentSpace | Retained-credential verification and reconstruction of its principal/executor context |
| Verify reopened identity/content continuity | Reads of the established Agent/Space identity, Home Space/interior association and retained fixture holons needed by this scenario |
| Exercise the explicitly supported AS2 Upgrade transition, if exposed | Only the versioned transition declared by that AS2 test; enumerate its exact entrypoints before enabling it |

Before implementation, map each step to named IPC/runtime/zome entrypoints and actual AS2 test identifiers. No unrestricted mutation, arbitrary Dance dispatch or unspecified additional local operation is admitted by this table. Tests needing additional authorized operations must explicitly reconcile that finite inventory; shared versioning/validation tests do not automatically expand CS-L1. CS-L1 must also demonstrate denial of unsupported operational Dancers and other reachable out-of-scope privileged paths.

### Acceptance contract

For the explicitly supported configuration, demonstrate:

1. Explicit Welcome initiation reaches the approved trusted backend path under the documented assurance assumptions; it is not described as cryptographic proof of human identity or intent.
2. Backend authorization admits only an eligible initial acquisition within the approved operation/installation/Space scope.
3. Unauthorized or alternate reachable paths cannot successfully constitute an AgentSpace; include direct conductor/zome ingress where applicable.
4. Completed acquisition cannot produce a second successful sovereign association, including when called by a technically authorized author. Idempotent retry may recover the original result. Competing requests and lost-response/retry behavior integrate with shared transaction guarantees; deleting a grant is not sufficient retirement evidence.
5. Durable principal/executor authorization evidence and valid retained credentials support opening the same acquired AgentSpace after restart without reacquisition.
6. Missing or inconsistent authorization evidence/credentials fails closed; acquisition-only privileges cannot become a standing operational bypass.
7. Only the minimum inventoried AS2 operations are supported; other privileged paths remain unavailable or appropriately protected. Broader security capabilities remain deferred.
8. Evidence identifies the verified code/dependency revisions, deployment mode (development versus packaged), assumptions, residual risks and unverified guarantees.

Client Security owns mechanism-level security tests; AS2 owns the end-to-end `AS2-Local-Lifecycle` integration; shared Transactions/persistence owns commitment and concurrency guarantees. This acceptance contract does not make CS-L1 alone proof of physical atomicity or full production readiness.

### Evidence and handoff

Own mechanism-level tests for unauthorized/direct callers, forged identities/flags, origin and permission boundaries, credential exposure/replay, operation/Space scope, post-completion privilege reuse, restart and missing credentials. Distinguish packaged from development configurations. Coordinate interruption/response-loss tests with shared persistence ownership.

Publish the supported API/contract and verified revision/configuration, guarantees, residual risks and unverified checks. AS2 runs selected end-to-end scenarios through its real lifecycle. Security assurance must cover the guarantees needed by the supported deployment; broader capability deferrals cannot waive those guarantees. No production-readiness claim follows from plan completion alone.

## 3. Later capabilities

General Dancer authorization, arbitrary delegation, WeSpace roles, universal operation-policy management, adaptive risk/step-up, rotation/revocation, credential recovery, multi-device continuity and interspace security are separately scoped. Their sequencing remains open and must not silently expand CS-L1 or AS2.
