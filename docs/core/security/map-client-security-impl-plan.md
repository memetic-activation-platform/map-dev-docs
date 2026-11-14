# MAP Client Security Implementation Plan

**Version:** 0.1

**Date:** 2026-11-14

**Status:** Planned; minimum local contract unresolved, no implementation delivery claimed.

## 1. Authority and delivery boundary

The [Client Security design specification](map-client-security-design-spec.md) owns semantics. This plan delivers reusable security capabilities independently of Agent Spaces. AS2 consumes the bounded initial local capability; it does not implement a general security framework. Completing the entire future security roadmap is not an AS2 dependency.

## 2. CS-L1 — Initial local trust and authorization

The identifier CS-L1 is a documentation work item, not a newly created GitHub issue.

### Contract gate

Resolve design §8 in the owning specification before enabling usable constitution credentials or privileged execution. Record the supported configuration, trusted components, human-initiation evidence, local threats, ingress coverage, credential custody, scope/retirement, post-acquisition authority and restart checks. Keep security, semantic assessment and commitment decisions separate.

### Repository grounding and implementation

Inspect existing Tauri command/capability configuration, Holochain plugin origin/token/signing behavior, native runtime dispatch, conductor interfaces, guest session restoration and keystore integration on the actual implementation baseline. Candidate surfaces include `host/conductora/capabilities/`, `plugins/tauri-plugin-holochain/`, `src/runtime/dispatch_map_command.rs`, and `happ/crates/holons_guest/src/dances_guest/dance_adapter.rs`. Their existence is not proof of sufficient authorization.

Reuse adequate existing mechanisms. Deliver only:

- Trusted initiation/admission and constitution-specific scope enforcement.
- Credential issuance/custody and replay or equivalent repeated-acquisition protection.
- Durable principal/execution authorization binding and acquisition privilege retirement.
- Ordinary authorized operation and valid-credential restart; missing credentials fail closed.
- Integration with shared commitment outcomes and conflicts, without a competing persistence path.

No capability framework, general policy engine, TrustChannel implementation, external identity service or recovery framework is implied.

### Evidence and handoff

Own mechanism-level tests for unauthorized/direct callers, forged identities/flags, origin and permission boundaries, credential exposure/replay, operation/Space scope, post-completion privilege reuse, restart and missing credentials. Distinguish packaged from development configurations. Coordinate interruption/response-loss tests with shared persistence ownership.

Publish the supported API/contract and verified revision/configuration, guarantees, residual risks and unverified checks. AS2 runs selected end-to-end scenarios through its real lifecycle. Security assurance must cover the guarantees needed by the supported deployment; broader capability deferrals cannot waive those guarantees. No production-readiness claim follows from plan completion alone.

## 3. Later capabilities

General policy and delegation management, adaptive risk/step-up, rotation/revocation, credential recovery, multi-device continuity and interspace security are separately scoped. Their sequencing remains open and must not silently expand CS-L1 or AS2.
