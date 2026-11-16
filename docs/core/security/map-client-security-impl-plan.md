# MAP Client Security Implementation Plan

**Version:** 0.4

**Date:** 2026-11-15

**Status:** Independent CS1 boundary protections implemented with mechanism and basic packaged-page evidence; constitution and authorized reopening remain disabled pending CS2–CS4. Verification scope and limitations are recorded below; no complete CS-L1 or production-readiness claim.

## 1. Authority and delivery boundary

The [Client Security design specification](map-client-security-design-spec.md) owns semantics. This plan delivers reusable security capabilities independently of Agent Spaces. AS2 consumes the bounded initial local capability; it does not implement a general security framework. Completing the entire future security roadmap is not an AS2 dependency.

## 2. CS-L1 — Initial local trust and authorization

The identifier CS-L1 is a documentation work item, not a newly created GitHub issue.

### Contract gate

Apply the approved boundary in design §8.1 and resolve the remaining §8.2 implementation/assurance gates before enabling usable constitution credentials or the bounded privileged paths. Record one supported configuration, its enforcement controls, ingress coverage, backend credential custody, scope/retirement and lifecycle restart checks. Map the finite operation inventory below to concrete AS2 integration tests. Keep security, semantic assessment and commitment decisions separate; AS2's scope and D2 Local Sovereign Constitution remain unchanged.

### Approved local trust boundary

Trust the legitimate packaged application and approved Welcome code, Rust host, embedded conductor and protected signing facilities within an uncompromised OS environment. The OS account is an environmental assumption, not a grant to its other processes. Unrelated WebViews, remote/displayed content, supplied IDs and bootstrap flags remain untrusted. Implement and verify isolation, origin restrictions and command permissions so that displayed content cannot inherit constitution authority. Keep credentials and authorization enforcement in the backend; do not place reusable constitution authority in frontend JavaScript.

Exclude compromise of trusted Welcome code, the native host and OS from the initial assurance claim. Retain exposed-interface, unauthorized-local-caller and untrusted-content attacks in the test scope; do not use the integrity assumption to waive admission/isolation verification. Explicit Welcome initiation and backend request-path verification express the approved human-initiation assurance, not cryptographic proof of identity or intent.

Independent native/OS confirmation is not a CS-L1 prerequisite. Reuse existing facilities; introduce neither independent native confirmation nor a new credential framework unless investigation demonstrates a concrete inability to enforce the approved boundary otherwise. Record such a finding and its bounded implications before changing the implementation contract.

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

1. Explicit initiation by approved packaged Welcome reaches the authorized backend path under design §8.1, without requiring independent native/OS confirmation. It is not described as cryptographic proof of human identity or intent.
2. Backend authorization admits only an eligible initial acquisition within the approved operation/installation/Space scope.
3. Unauthorized or alternate reachable paths cannot successfully constitute an AgentSpace; include direct conductor/zome ingress where applicable. Other local processes, unrelated WebViews and untrusted displayed content cannot inherit constitution authority through exposed interfaces, origin/permission gaps or a supplied identity/bootstrap flag. Frontend JavaScript receives no reusable constitution authority.
4. Completed acquisition cannot produce a second successful sovereign association, including when called by a technically authorized author. Idempotent retry may recover the original result. Competing requests and lost-response/retry behavior integrate with shared transaction guarantees; deleting a grant is not sufficient retirement evidence.
5. Durable principal/executor authorization evidence and valid retained credentials support opening the same acquired AgentSpace after restart without reacquisition.
6. Missing or inconsistent authorization evidence/credentials fails closed; acquisition-only privileges cannot become a standing operational bypass.
7. Only the minimum inventoried AS2 operations are supported; other privileged paths remain unavailable or appropriately protected. Broader security capabilities remain deferred.
8. Evidence identifies the verified code/dependency revisions, deployment mode (development versus packaged), the approved trust assumptions/exclusions, in-scope interface/local-caller/content attacks, residual risks and unverified guarantees. Integrity of approved packaged code is an assumption; correct enforcement of content isolation and caller admission must be demonstrated.

Client Security owns mechanism-level security tests; AS2 owns the end-to-end `AS2-Local-Lifecycle` integration; shared Transactions/persistence owns commitment and concurrency guarantees. This acceptance contract does not make CS-L1 alone proof of physical atomicity or full production readiness.

### Evidence and handoff

Own mechanism-level tests for unauthorized/direct callers, forged identities/flags, origin and permission boundaries, credential exposure/replay, operation/Space scope, post-completion privilege reuse, restart and missing credentials. Distinguish packaged from development configurations. Coordinate interruption/response-loss tests with shared persistence ownership.

Publish the supported API/contract and verified revision/configuration, guarantees, residual risks and unverified checks. AS2 runs selected end-to-end scenarios through its real lifecycle. Security assurance must cover the guarantees needed by the supported deployment; broader capability deferrals cannot waive those guarantees. No production-readiness claim follows from plan completion alone.

## 3. Later capabilities

General Dancer authorization, arbitrary delegation, WeSpace roles, universal operation-policy management, adaptive risk/step-up, rotation/revocation, credential recovery, multi-device continuity and interspace security are separately scoped. Their sequencing remains open and must not silently expand CS-L1 or AS2.

## CS1 implementation record — 2026-11-15

### Configuration and ingress disposition

The working implementation targets packaged macOS on Apple Silicon. Tauri packaging declares macOS 14.0 as its minimum; the current verification machine is macOS 26.5.2 arm64. These are distinct from a claim of assurance across supported OS releases. The packaged build uses the custom-protocol feature, an embedded fixed storage configuration and the Tauri resource mapping for the hApp. Release binaries cannot fall back to development privileges. Development overrides are rejected for packaged Welcome.

| Surface | Packaged disposition | Development disposition |
| --- | --- | --- |
| Conductor administration | Existing in-process Holochain admin handler; no admin listener | Existing admin WebSocket workflow retained |
| Dance transport | Native caller fixed to the selected cell and holons::dance; no app listener or frontend token | Existing authenticated app-WebSocket transport retained |
| Generic signing / additional hApp windows | Rejected by the native-only runtime | Existing explicit plugin capabilities retained |
| Generic MAP IPC, legacy map_request and auxiliary client commands | Not registered in packaged handler | Existing handler registered with explicit application-command permissions |
| Welcome | Dedicated fixed local page, narrow capability and backend window/URL check; no materialized modules | Not an authorized constitution surface |
| Constitution | Narrow request command exists but always refuses; no principal or supplied bootstrap flag enables it | No constitution authority supplied |
| Direct node / SmartLink exports and supplied guest bootstrap state | Existing WASM semantics unchanged; no external local conductor interface, generic client dispatch or signing route reaches them in this configuration | Existing development/test paths retained |
| Open / restart | Existing Space discovery and content preservation; no authorized sovereign execution supplied | Existing development behavior retained |
| Upgrade | No semantic AS2 Upgrade enabled | Existing development behavior is not AS2 Upgrade evidence |

Before starting the native-only conductor, its own persisted-state loader checks for saved app listeners and refuses incompatible state before those listeners can reopen. No identity reset, replacement Space, or implicit migration is performed. The absence of an app listener is independent of the author's inherent capability rights; deleting a remote grant is not used as retirement evidence. Startup compares persisted DNA/coordinator definitions with the packaged hApp and refuses mismatches or active remote grants in this initial local-only execution profile. Broader remote execution is not implemented by these checks.

### Verification and remaining gates

Focused tests exercise exact Welcome URL/window admission, narrow command permissions, native provisioning through the existing loader/Commit path, retained Space discovery and persisted-listener rejection. Results must distinguish library/conductor mechanism tests from actual packaged WebView evidence. Full packaged assurance, hostile content/local-caller coverage, credential-store protection and the CS2–CS5 lifecycle remain separately identified checks.

Existing Lair signing is reused; native backend custody does not itself establish protection of the credential store against all local attack surfaces. The existing empty-passphrase setup is not evidence of protected custody. CS3 must establish and verify the actual storage/custody guarantee before constitution is enabled. CS2 supplies backend admission and the eligible installation/Space operation scope; CS4 supplies principal binding, durable retirement and restart authorization. Commit remediation/resubmission semantics remain unchanged.

### Verification results — working tree, macOS 26.5.2 arm64

- `cargo test --manifest-path host/Cargo.toml -p Conductora -p holochain_runtime --lib --locked -- --test-threads=1`: 31 Conductora and 5 embedded-runtime tests passed. The real persistent-conductor case loads the production hApp and full Core bootstrap through the native transport, observes Complete, restarts and discovers the same Space without bootstrap authority. The separate listener case seeds a saved external interface and verifies rejection before it can be restored. These run outside the managed sandbox because Holochain requires network-monitor access.
- The two Welcome admission/capability tests were rerun after narrowing the capability to the exact WebView label; both passed. These are unit/configuration tests, not live-WebView attack tests.
- Production Angular build passed with the matching ARM64 Node runtime outside the managed sandbox. The sandboxed process aborted; no dependency or lockfile workaround was introduced. Existing size/CommonJS warnings remain.
- An unsigned debug macOS app bundle built with `custom-protocol`; its mapped hApp, bootstrap manifest and import resources were verified. It was launched from `/private/tmp`, outside the checkout. A process-level check observed no TCP listeners. This is packaged-asset/debug-build evidence, not a signed release or production-readiness claim.
- Initial UI inspection timed out while first-time loader/validation work was active and dependency warning output was excessive. Welcome creation was moved before background provisioning. The updated unsigned debug bundle was then relaunched from `/private/tmp` with retained state and quieter logging: native inspection observed `tauri://localhost/welcome.html`, the expected unavailable message from the backend status response and the disabled personal-space button. This verifies basic packaged rendering, script execution and the narrow status path; adversarial CSP, hostile-content and alternate-WebView checks remain unverified. The earlier verification process was stopped without deleting or resetting data; its complete first-run configured-import outcome was not established.

No MAP schema, guest Commit or sovereign-state semantics changed. Acquired-space authorization and operational execution remain disabled pending CS2–CS4. Full packaged security assurance, credential-store protection, P2P/remote-grant negative cases and local filesystem attack coverage remain explicit follow-up evidence; no claim of complete CS-L1 follows from these checks.
